# Decision Log

**Project**: Unified Data Dictionary Framework  
**Author**: R. A. Carucci  
**Purpose**: Document design decisions and resolution of cross-system rule conflicts

---

## Decision #001: Join Key Strategy

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Need to establish primary join strategy between CAD and RMS systems

**Decision**: Use `CAD.ReportNumberNew ↔ RMS.CaseNumber` as primary join key with LEFT JOIN strategy (CAD drives merge)

**Rationale**:
- Both systems use identical `YY-NNNNNN` format
- CAD records always exist (operational requirement)
- RMS records may not exist for all CAD incidents (not all calls generate reports)
- LEFT JOIN preserves all CAD records while enriching with available RMS data

**Alternatives Considered**:
1. INNER JOIN - Rejected: Would lose CAD-only incidents
2. FULL OUTER JOIN - Rejected: Would include orphaned RMS records (data quality issue indicator)
3. Multiple join keys - Rejected: Single key provides sufficient uniqueness

**Consequences**:
- Orphaned CAD records (without RMS) are valid
- Orphaned RMS records (without CAD) indicate data sync issues and should be investigated

---

## Decision #002: Address Backfill Precedence

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Both CAD and RMS have address fields; need conflict resolution strategy

**Decision**: Use CAD.FullAddress2 as primary source; backfill from RMS.Location only when CAD address is NULL or invalid

**Rationale**:
- CAD addresses are more current (real-time data entry)
- RMS addresses may lag behind CAD updates
- Validation against Hackensack street names identifies invalid CAD addresses
- RMS provides quality fallback when CAD fails validation

**Precedence Order**:
1. CAD.FullAddress2 (if present and valid)
2. Rule-based corrections (parks, landmarks, intersections)
3. RMS.Location (conditional backfill)
4. Manual corrections (last resort)

**Alternatives Considered**:
1. Always use RMS - Rejected: RMS may have stale data
2. Merge/concatenate both - Rejected: Creates inconsistent formatting
3. Use most recent timestamp - Rejected: Timestamps not reliably available

---

## Decision #003: Incident Type Backfill Hierarchy

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: CAD has single Incident field; RMS has IncidentType1/2/3; need backfill strategy when CAD.Incident is NULL

**Decision**: Implement three-level hierarchical backfill: IncidentType1 → IncidentType2 → IncidentType3

**Rationale**:
- RMS incident types are ordered by significance
- IncidentType1 is primary classification
- IncidentType2/3 are secondary/tertiary
- Preserves RMS classification logic

**Precedence Logic**:
```python
if pd.isna(cad_incident):
    if not pd.isna(rms_incident_type1):
        cad_incident = rms_incident_type1
    elif not pd.isna(rms_incident_type2):
        cad_incident = rms_incident_type2
    elif not pd.isna(rms_incident_type3):
        cad_incident = rms_incident_type3
```

**Alternatives Considered**:
1. Concatenate all three types - Rejected: Creates verbose, inconsistent values
2. Use most specific (Type3 first) - Rejected: Reverses RMS priority logic
3. Use CallType mapping - Accepted: Applied after backfill

---

## Decision #004: Narrative Field Handling

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Both CAD (CADNotes) and RMS (Narrative) have free-text fields with different purposes

**Decision**: Preserve both narratives; append RMS.Narrative to CAD.CADNotes with delimiter ` | RMS: `

**Rationale**:
- CAD notes contain dispatcher/operational information
- RMS narratives contain investigative details
- Both provide value for analysis
- Delimiter clearly separates sources

**Implementation**:
```python
if pd.notna(rms_narrative):
    combined = f"{cad_notes} | RMS: {rms_narrative}"
```

**Alternatives Considered**:
1. Replace CAD notes with RMS narrative - Rejected: Loses operational context
2. Keep only CAD notes - Rejected: Loses investigative detail
3. Separate columns - Rejected: Complicates downstream text analysis

---

## Decision #005: Excel Date Artifact Handling

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Excel converts "9-1-1" to date (Sept 1, 1901) in HowReported field

**Decision**: Implement pattern-based detection and auto-correction during standardization stage

**Detection Patterns**:
- `1901-09-01` (ISO format)
- `September 1, 1901` (text format)
- Serial number `44197`
- Various date-like patterns containing "1901"

**Auto-Correction**:
Replace all detected patterns with `'9-1-1'`

**Rationale**:
- Well-known Excel data corruption issue
- Patterns are unique and unambiguous
- Auto-correction safer than manual review (volume too high)
- No valid data should contain these patterns

**Alternatives Considered**:
1. Manual review - Rejected: Too time-consuming for volume
2. Flag for review - Rejected: Patterns are unambiguous
3. Leave as-is - Rejected: Corrupts 911 analysis

---

## Decision #006: Time Sequence Violation Handling

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Some records have time sequences that violate logical order (e.g., dispatch before call)

**Decision**: Flag violations but don't auto-correct; report in validation output

**Validation Check**:
```
TimeOfCall <= TimeDispatched <= TimeOut <= TimeIn
```

**Action on Violation**:
- Add to validation error list
- Set quality flag field
- Include in validation report
- **DO NOT** auto-correct timestamps

**Rationale**:
- Violations may indicate valid edge cases (e.g., pre-positioned units, delayed data entry)
- Auto-correction could mask data quality issues
- Allows subject matter experts to review and correct
- Preserves data integrity

**Alternatives Considered**:
1. Auto-correct to logical sequence - Rejected: May mask valid edge cases
2. Drop records with violations - Rejected: Loses data unnecessarily
3. Set to NULL - Rejected: Loses partial information

---

## Decision #007: Coordinate Validation Bounds

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Need geographic bounds for coordinate validation

**Decision**: Use approximate Hackensack bounds with validation flag (not hard rejection)

**Bounds**:
- Latitude: 40.85 to 40.91
- Longitude: -74.07 to -74.03

**Action on Out-of-Bounds**:
- Flag record in validation report
- Set `Coordinates_Out_Of_Bounds` flag
- **DO NOT** reject or NULL coordinates

**Rationale**:
- Incidents can occur just outside city limits (mutual aid, pursuit, etc.)
- Strict rejection would lose valid data
- Flags allow downstream filtering if needed
- Preserves data for investigation

**Alternatives Considered**:
1. Strict bounds with rejection - Rejected: Loses legitimate out-of-jurisdiction incidents
2. No bounds validation - Rejected: Allows obviously incorrect coordinates
3. Expand bounds significantly - Rejected: Reduces validation effectiveness

---

## Decision #008: Controlled Vocabulary Enforcement

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Need strategy for handling values not in controlled vocabularies

**Decision**: Flag violations but don't block pipeline; maintain vocabulary reference files

**Enforcement Strategy**:
- Validate against controlled vocabulary lists
- Flag non-compliant values in validation report
- Track new values for vocabulary expansion
- Allow pipeline to complete with flagged data

**Reference Files**:
- `HowReported`: Inline list in schema
- `Disposition`: `ref/Disposition_Types.csv`
- `Incident`: `ref/CallType_Categories.csv`
- `PDZone`: Inline list in schema

**Rationale**:
- Vocabularies evolve over time (new incident types, dispositions)
- Strict enforcement would reject valid new values
- Flagging allows review and vocabulary updates
- Preserves data integrity while enabling evolution

**Alternatives Considered**:
1. Strict enforcement with rejection - Rejected: Would lose valid new values
2. No vocabulary validation - Rejected: Allows typos and inconsistencies
3. Auto-add new values - Rejected: No quality control on additions

---

## Decision #009: Data Quality Scoring Algorithm

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Need quantitative measure of record completeness and quality

**Decision**: Implement 100-point scoring system with weighted components

**Scoring Weights**:
- Case number present: 20 points (critical identifier)
- Address present: 20 points (critical for mapping)
- Call time present: 10 points
- Dispatch time present: 10 points
- Officer present: 20 points (critical for workload analysis)
- Disposition present: 10 points
- Incident type present: 10 points

**Usage**:
- Filter high-quality records (score ≥80) for critical analysis
- Identify low-quality records (score <50) for review
- Track quality trends over time
- Quality gate for ESRI exports (score ≥70)

**Rationale**:
- Objective measure enables automated filtering
- Weighted by analytical importance
- Simple calculation (no complex algorithms)
- Interpretable scores (0-100 intuitive)

**Alternatives Considered**:
1. Binary quality flag - Rejected: Too coarse-grained
2. Complex ML-based scoring - Rejected: Overcomplicated, not interpretable
3. Unweighted scoring - Rejected: All fields not equally important

---

## Decision #010: Parallel Processing Strategy

**Date**: 2025-12-17  
**Status**: Accepted  
**Context**: Large datasets (700K+ records) require optimization for validation performance

**Decision**: Implement dual-strategy approach: vectorized pandas for small/medium datasets, multiprocessing for large datasets

**Strategy Selection**:
- **Small (<10K records)**: Single-batch vectorized pandas
- **Medium (10K-100K)**: Vectorized pandas with chunking
- **Large (>100K)**: Multiprocessing with ProcessPoolExecutor

**Configuration Parameters**:
- `--workers`: Number of parallel processes (default: 4)
- `--chunk-size`: Records per chunk (default: 10000)
- `--engine`: pandas | pandas_parallel | polars

**Performance Target**:
- >50,000 records/second for validation

**Rationale**:
- Vectorized pandas fastest for small datasets (minimal overhead)
- Multiprocessing provides linear speedup for large datasets
- Configurable parameters allow tuning for hardware
- Maintains identical validation logic across strategies

**Alternatives Considered**:
1. Always use multiprocessing - Rejected: Overhead hurts small dataset performance
2. GPU acceleration - Rejected: Not available on target systems
3. Dask/Ray - Rejected: Adds dependencies for marginal benefit

---

## Future Decisions

### Under Consideration

**DC-011**: Incremental validation (only validate changed records)  
**DC-012**: GPU acceleration for 1M+ record datasets  
**DC-013**: Real-time validation API service  
**DC-014**: Automated vocabulary expansion workflow  
**DC-015**: Cross-year case number format transition strategy

---

## References

- Canonical Schema: `docs/schema/canonical_schema.json`
- Mapping Rules: `docs/mappings/mapping_rules.md`
- Transformation Spec: `docs/transforms/transformation_spec.json`
- Performance Benchmarks: `docs/benchmarks/benchmark_results.json`
