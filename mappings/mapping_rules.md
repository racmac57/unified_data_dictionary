# Field Mapping Rules and Strategy

**Document Version**: 1.0.0  
**Author**: R. A. Carucci  
**Last Updated**: 2025-12-17  
**Purpose**: Define cross-system field mapping logic, precedence rules, and edge case handling

---

## Overview

This document defines how fields are mapped between CAD (Computer-Aided Dispatch) and RMS (Records Management System) during ETL operations. The framework supports bidirectional mapping with clear precedence rules and validation logic.

---

## Primary Join Strategy

### Join Key

**CAD.ReportNumberNew ↔ RMS.CaseNumber**

- Format: `YY-NNNNNN` (e.g., `24-123456`)
- Both systems use the same case number format
- Join type: **LEFT JOIN** (CAD drives merge; RMS enriches)
- Orphaned records:
  - CAD records without RMS match: Valid (incident may not have generated RMS report)
  - RMS records without CAD match: **Data quality issue** (investigate sync failures)

### Join Validation Rules

```python
# Validation checks during merge
assert cad_df['ReportNumberNew'].notna().all(), "CAD must have case numbers"
assert cad_df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$').all(), "Invalid case number format"

# Check for orphaned RMS records
orphaned_rms = rms_df[~rms_df['CaseNumber'].isin(cad_df['ReportNumberNew'])]
if len(orphaned_rms) > 0:
    log_warning(f"Found {len(orphaned_rms)} orphaned RMS records")
```

---

## Field Mapping Types

### 1. DIRECT_MAP
**Definition**: 1:1 field correspondence with no transformation  
**Example**: `RMS.CaseNumber → CAD.ReportNumberNew`  
**Logic**: Direct assignment after validation

### 2. CONDITIONAL_FILL
**Definition**: Fill target field only if it's NULL or invalid  
**Example**: `RMS.Location → CAD.FullAddress2` (only if CAD address is blank)  
**Logic**:
```python
if pd.isna(cad_address) or is_invalid(cad_address):
    cad_address = rms_location
```

### 3. ADDRESS_BACKFILL
**Definition**: Specialized conditional fill for addresses  
**Example**: `RMS.Location → CAD.FullAddress2`  
**Precedence Rules**:
1. Use CAD.FullAddress2 if present and valid
2. Validate against Hackensack street names
3. Backfill from RMS.Location if CAD fails validation
4. Flag records where backfill was applied

**Edge Cases**:
- Parks/landmarks: Use rule-based corrections first
- Intersections: Validate both street names exist
- Apartment numbers: Preserve unit information
- Out-of-jurisdiction: Flag but preserve

### 4. INCIDENT_BACKFILL
**Definition**: Multi-level fallback for incident classification  
**Example**: `RMS.IncidentType1/2/3 → CAD.Incident`  
**Precedence Rules**:
```python
if pd.isna(cad_incident):
    if not pd.isna(rms_incident_type1):
        cad_incident = rms_incident_type1
    elif not pd.isna(rms_incident_type2):
        cad_incident = rms_incident_type2
    elif not pd.isna(rms_incident_type3):
        cad_incident = rms_incident_type3
```

**Vocabulary Mapping**: Apply `CallType_Categories.csv` lookup after backfill

### 5. TEXT_APPEND
**Definition**: Concatenate text fields with delimiter  
**Example**: `RMS.Narrative + CAD.CADNotes`  
**Logic**:
```python
if pd.notna(rms_narrative):
    combined = f"{cad_notes} | RMS: {rms_narrative}"
```

### 6. VOCABULARY_MAP
**Definition**: Map between different controlled vocabularies  
**Example**: `CAD.HowReported → RMS.ReportMethod`  
**Mapping Table**:

| CAD Value | RMS Value |
|-----------|-----------|
| 9-1-1 | Emergency Call |
| Phone | Non-Emergency Call |
| Walk-in | In-Person Report |
| Self-Initiated | Officer Initiated |

### 7. DATETIME_EXTRACT
**Definition**: Extract date or time component from datetime  
**Example**: `CAD.TimeOfCall → RMS.IncidentDate + RMS.IncidentTime`  
**Logic**:
```python
incident_date = time_of_call.date()
incident_time = time_of_call.time()
```

---

## Precedence Rules

### General Hierarchy

1. **CAD data takes precedence** for operational fields (address, time, incident)
2. **RMS data takes precedence** for investigative fields (UCR code, arrest details)
3. **Derived fields** calculated from most reliable source

### Field-Specific Precedence

**Address**:
1. CAD.FullAddress2 (if valid)
2. Rule-based corrections (parks, landmarks)
3. RMS.Location (backfill only)
4. Manual corrections

**Incident Classification**:
1. CAD.Incident (primary)
2. RMS.IncidentType1 (first fallback)
3. RMS.IncidentType2 (second fallback)
4. RMS.IncidentType3 (third fallback)

**Officer Information**:
1. Parse CAD.Officer for operational data
2. Enrich with RMS.OfficerName for complete names
3. Validate against Assignment_Master_V2.xlsx

**Disposition**:
1. Use CAD.Disposition for outcome
2. Standardize vocabulary across systems
3. Enrich with RMS.FinalDisposition details

---

## Edge Cases and Special Handling

### 1. Excel Date Artifacts

**Problem**: Excel converts "9-1-1" to date (Sept 1, 1901)  
**Detection Patterns**:
- `1901-09-01`
- `September 1, 1901`
- Serial number `44197`

**Fix**:
```python
date_patterns = [r'.*1901.*', r'.*44197.*', r'.*sep.*1.*1901.*']
for pattern in date_patterns:
    df.loc[df['HowReported'].str.contains(pattern, na=False, case=False), 'HowReported'] = '9-1-1'
```

### 2. Multi-Officer Cases

**CAD Format**: Comma-separated list  
**RMS Format**: Single primary officer

**Logic**:
```python
officers = cad_officer.split(',')
primary_officer = officers[0].strip()
```

### 3. Geocoding Conflicts

**When**: CAD and RMS have different lat/long for same address  
**Resolution**:
1. Compare coordinate distance
2. If distance > 100m, flag for review
3. Use most recent geocoding attempt
4. Validate coordinates are within Hackensack bounds

### 4. Time Sequence Violations

**Check**: `TimeOfCall <= TimeDispatched <= TimeOut <= TimeIn`  
**Action**: Flag violations but don't auto-correct (may indicate valid delays)

### 5. Orphaned Records

**CAD without RMS**: Valid (not all CAD calls generate RMS reports)  
**RMS without CAD**: **Data quality issue** (requires investigation)

---

## Validation Rules

### Pre-Merge Validation

```python
def validate_pre_merge(cad_df, rms_df):
    """Run before merge operation"""
    # Check for duplicate case numbers
    assert cad_df['ReportNumberNew'].is_unique
    assert rms_df['CaseNumber'].is_unique
    
    # Validate case number format
    assert cad_df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$').all()
    
    # Check required fields
    assert cad_df['TimeOfCall'].notna().all()
    assert cad_df['Incident'].notna().sum() > 0.95 * len(cad_df)
```

### Post-Merge Validation

```python
def validate_post_merge(merged_df):
    """Run after merge operation"""
    # Check merge success rate
    merge_rate = merged_df['CaseNumber'].notna().sum() / len(merged_df)
    assert merge_rate > 0.70, f"Low merge rate: {merge_rate:.1%}"
    
    # Validate backfill applications
    backfilled = merged_df['Address_Backfilled'].sum()
    log_info(f"Applied address backfill to {backfilled} records")
    
    # Check for data quality improvements
    assert merged_df['Data_Quality_Score'].mean() >= cad_df['Data_Quality_Score'].mean()
```

---

## Transform Pipeline Order

ETL stages must be executed in this order:

1. **Ingest**: Load CAD and RMS exports
2. **Normalize**: Standardize field names and types
3. **Validate Pre-Merge**: Run validation checks
4. **Merge**: Join on case number
5. **Backfill**: Apply conditional fills (address, incident, etc.)
6. **Standardize**: Apply vocabulary mappings
7. **Derive**: Calculate derived fields
8. **Validate Post-Merge**: Final quality checks
9. **Export**: Write to output formats

---

## Controlled Vocabularies

### HowReported (CAD)
- `9-1-1` - Emergency call via 911
- `Phone` - Non-emergency phone call
- `Walk-in` - In-person at station
- `Self-Initiated` - Officer-initiated
- `Radio` - Radio dispatch
- `Other` - Other methods

### Disposition (Both Systems)
- `Report Taken` / `Report Filed`
- `Arrest Made` / `Arrest`
- `GOA` - Gone on Arrival
- `UTL` - Unable to Locate
- `Unfounded`
- `See Report` / `Report Required`

### ResponseType (CAD)
- `Emergency` - Immediate response required
- `Priority` - Elevated priority
- `Routine` - Standard response
- `Not Specified` - Missing/unknown

---

## Conflict Resolution Strategy

When CAD and RMS data conflict:

1. **Temporal fields**: Use CAD (real-time data)
2. **Classification**: Use CAD.Incident, backfill if NULL
3. **Location**: Use CAD, validate and backfill if invalid
4. **Narrative**: Preserve both (append)
5. **Disposition**: Standardize vocabulary, prefer CAD
6. **Officer**: Parse CAD, enrich with RMS names

---

## Performance Considerations

### Batch Size Recommendations

- **Small datasets** (<10K records): Process in single batch
- **Medium datasets** (10K-100K): Use 10K record chunks
- **Large datasets** (>100K): Use 5K record chunks with multiprocessing

### Indexing Strategy

Create indexes on join keys before merge:
```python
cad_df = cad_df.set_index('ReportNumberNew')
rms_df = rms_df.set_index('CaseNumber')
```

### Memory Optimization

Use categorical dtypes for controlled vocabularies:
```python
for col in ['HowReported', 'Disposition', 'ResponseType']:
    df[col] = df[col].astype('category')
```

---

## Change Log

| Date | Author | Changes |
|------|--------|---------|
| 2025-12-17 | R. A. Carucci | Initial framework creation |

---

## References

- `cad_field_map.json` - CAD field definitions
- `rms_field_map.json` - RMS field definitions
- `CallType_Categories.csv` - Incident type mapping
- `Assignment_Master_V2.xlsx` - Officer name standardization
- `Hackensack_Street_Names.csv` - Address validation
