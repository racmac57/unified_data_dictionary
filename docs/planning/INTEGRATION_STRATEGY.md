# 🕒 2025-12-17-19-50-00
# unified_data_dictionary/docs/INTEGRATION_STRATEGY.md
# Author: R. A. Carucci
# Purpose: Cross-repository integration architecture defining data flow, join keys, shared vocabulary, synchronization protocols, and lineage tracking across dv_doj and CAD_Data_Cleaning_Engine

# Cross-Repository Integration Strategy

**Document Version**: 1.0  
**Last Updated**: 2025-12-17  
**Owner**: R. A. Carucci (Principal Analyst)

---

## Overview

This document defines integration architecture for the unified data dictionary with existing repositories:
- **dv_doj** - Domestic Violence DOJ reporting system
- **CAD_Data_Cleaning_Engine** - CAD/RMS data processing pipeline

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  UNIFIED DATA DICTIONARY                         │
│                  (Canonical Schemas)                             │
└────────────┬─────────────────────────────────┬─────────────────┘
             │                                 │
             │ Schema Pull                     │ Schema Pull
             │ (Weekly)                        │ (Weekly)
             │                                 │
┌────────────▼─────────────┐      ┌───────────▼──────────────────┐
│      dv_doj              │      │  CAD_Data_Cleaning_Engine    │
│  ┌─────────────────────┐ │      │  ┌─────────────────────────┐ │
│  │ DV Schema           │ │      │  │ CAD Schema              │ │
│  │ DOJ Mappings        │ │      │  │ RMS Schema              │ │
│  │ Validation Rules    │ │      │  │ Field Mappings          │ │
│  └─────────────────────┘ │      │  │ Validation Engine       │ │
│           │               │      │  └─────────────────────────┘ │
│           │ Export        │      │           │                  │
│           ▼               │      │           │ Export           │
│  ┌─────────────────────┐ │      │           ▼                  │
│  │ DV Exports          │ │      │  ┌─────────────────────────┐ │
│  │ (xlsx, json)        │ │      │  │ CAD/RMS Exports         │ │
│  └─────────────────────┘ │      │  │ (xlsx, json)            │ │
└──────────┬───────────────┘      └───────────┬──────────────────┘
           │                                   │
           │ Join on Incident Number          │
           │                                   │
           └────────────┬──────────────────────┘
                        │
           ┌────────────▼─────────────┐
           │   INTEGRATED ANALYSIS    │
           │   - Cross-system views   │
           │   - Combined dashboards  │
           │   - Unified reporting    │
           └──────────────────────────┘
```

---

## Integration Points

### 1. Schema Synchronization

#### **Pull Strategy (Recommended)**
Unified dictionary **pulls** schemas from source repositories via Git API.

**Frequency**: Weekly automated extraction  
**Trigger**: GitHub Actions scheduled workflow  
**Process**:
```bash
# Automated weekly sync
make extract  # Pulls latest schemas
make build    # Rebuilds dictionary
make excel    # Regenerates docs
git commit -am "Auto-sync: schemas updated"
git push
```

**Advantages**:
- Single source of truth (source repos)
- No disruption to existing workflows
- Dictionary stays current automatically

#### **Push Strategy (Alternative)**
Source repositories push schema updates to dictionary repo.

**Use Case**: When schema changes are critical and need immediate propagation  
**Implementation**: GitHub Actions webhook on schema file changes

---

### 2. Join Key Strategy

#### **Primary Join Key: Incident Number**

All systems use `incident_number` as universal identifier.

**Format Standards**:
```
CAD System:     2025-00012345  (YYYY-NNNNNNNN)
RMS System:     2025-00012345  (YYYY-NNNNNNNN)
DV System:      2025-00012345  (YYYY-NNNNNNNN)
```

**Canonical Definition**:
```json
{
  "incident_number": {
    "data_type": "string",
    "pattern": "^\\d{4}-\\d{8}$",
    "required": true,
    "unique": true,
    "description": "Universal incident identifier across all systems"
  }
}
```

#### **Secondary Join Keys**

| Join Type | Key Field | Systems | Use Case |
|-----------|-----------|---------|----------|
| Location | `location_id` | CAD, RMS | Spatial analysis |
| Person | `person_id` | RMS, DV | Recidivism tracking |
| Officer | `officer_id` | CAD, RMS, DV | Workload analysis |
| Unit | `unit_number` | CAD, RMS | Response metrics |

#### **Join Key Validation Rules**

```python
# Validation logic enforced by unified dictionary
validation_rules = {
    'incident_number': {
        'not_null': True,
        'unique': True,
        'format': r'^\d{4}-\d{8}$',
        'referential_integrity': ['CAD', 'RMS', 'DV']
    },
    'person_id': {
        'not_null': False,
        'format': r'^P\d{6}$',
        'referential_integrity': ['RMS', 'DV']
    }
}
```

---

### 3. Shared Vocabulary Management

#### **Enumerated Values**

Unified dictionary maintains canonical enumerations shared across systems.

**Example: Disposition Codes**

```json
{
  "disposition": {
    "data_type": "enum",
    "canonical_values": [
      {"code": "ARR", "label": "Arrest Made", "systems": ["CAD", "RMS"]},
      {"code": "REP", "label": "Report Filed", "systems": ["CAD", "RMS"]},
      {"code": "GOA", "label": "Gone on Arrival", "systems": ["CAD"]},
      {"code": "UTL", "label": "Unable to Locate", "systems": ["CAD"]},
      {"code": "UNF", "label": "Unfounded", "systems": ["RMS"]}
    ],
    "mappings": {
      "CAD_to_RMS": {
        "GOA": "UTL",
        "UTL": "UTL"
      }
    }
  }
}
```

**Implementation**:
- Source repos import canonical enums from dictionary
- Validation enforces enum constraints
- New values require dictionary update first

#### **Code Mappings**

**UCR/NIBRS Codes**:
```json
{
  "ucr_mappings": {
    "source": "FBI UCR Handbook 2024",
    "codes": {
      "13A": {"crime": "Aggravated Assault", "category": "Violent"},
      "23A": {"crime": "Larceny - Pocket-picking", "category": "Property"}
    }
  }
}
```

**Statute Codes (NJ)**:
```json
{
  "statute_mappings": {
    "source": "NJ Revised Statutes",
    "codes": {
      "2C:12-1b": {"offense": "Simple Assault", "degree": "Disorderly"},
      "2C:33-2": {"offense": "Disorderly Conduct", "degree": "Petty Disorderly"}
    }
  }
}
```

---

### 4. Data Lineage Tracking

#### **Lineage Metadata**

Each field in unified dictionary tracks its lineage:

```json
{
  "incident_datetime": {
    "source_systems": ["CAD", "RMS", "DV"],
    "lineage": {
      "CAD": {
        "source_field": "CALL_TIME",
        "extraction_date": "2025-12-17",
        "extraction_method": "Git API",
        "transformations": ["timezone_normalization"]
      },
      "RMS": {
        "source_field": "INCIDENT_DT",
        "extraction_date": "2025-12-17",
        "extraction_method": "Git API",
        "transformations": ["format_standardization"]
      }
    }
  }
}
```

#### **Version Control**

Dictionary maintains version history of schema changes:

```json
{
  "version_history": [
    {
      "version": "1.0.0",
      "date": "2026-01-15",
      "changes": ["Initial canonical schema"],
      "schemas_extracted": {
        "dv_doj": "commit:abc123",
        "CAD_Data_Cleaning_Engine": "commit:def456"
      }
    },
    {
      "version": "1.1.0",
      "date": "2026-02-01",
      "changes": ["Added DV-specific fields"],
      "schemas_extracted": {
        "dv_doj": "commit:ghi789"
      }
    }
  ]
}
```

---

### 5. Synchronization Protocols

#### **Automated Sync Workflow**

**GitHub Actions Pipeline**:
```yaml
name: Schema Sync
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Extract schemas
        run: make extract
      
      - name: Build dictionary
        run: make build
      
      - name: Validate
        run: make validate --strict
      
      - name: Generate Excel
        run: make excel
      
      - name: Commit changes
        run: |
          git config user.name "Schema Bot"
          git add .
          git commit -m "Auto-sync: $(date +'%Y-%m-%d')"
          git push
      
      - name: Notify team
        run: ./scripts/send_notification.sh
```

#### **Manual Sync (Emergency)**

When critical schema changes need immediate propagation:

```bash
# 1. Pull latest from source repos
make extract

# 2. Rebuild dictionary
make build

# 3. Validate changes
make validate --strict

# 4. Generate documentation
make excel

# 5. Review conflicts
cat output/dictionary_statistics.json | jq '.conflicts'

# 6. Commit and deploy
git add .
git commit -m "Emergency sync: [reason]"
git push
```

---

### 6. Integration Use Cases

#### **Use Case 1: DV Hot Spot Analysis**

**Objective**: Identify domestic violence hot spots using unified address data

**Data Flow**:
```
dv_doj (DV incidents)
    └─> Unified Dictionary (canonical address fields)
        └─> CAD_Data_Cleaning_Engine (address validation)
            └─> ArcGIS Pro (hot spot analysis)
```

**Integration Points**:
- **Field Mapping**: DV.location_address → CAD.ADDRESS_CLEANED
- **Validation**: 97.3% address quality via CAD engine
- **Join Key**: incident_number (for cross-reference)

**Implementation**:
```python
# Import unified schema
from unified_data_dictionary import canonical_schema

# Apply address validation from CAD engine
dv_data['validated_address'] = validate_address(
    dv_data['location_address'],
    rules=canonical_schema['address_validation_rules']
)

# Join with CAD for additional context
merged = dv_data.merge(
    cad_data,
    on='incident_number',
    how='left'
)
```

#### **Use Case 2: Cross-System Dashboard**

**Objective**: Power BI dashboard showing CAD response + RMS outcomes + DV flags

**Data Integration**:
```python
# Query unified exports
cad_export = pl.read_parquet('CAD_ESRI_Final_20251124_COMPLETE.xlsx')
rms_export = pl.read_parquet('rms_export_latest.parquet')
dv_export = pl.read_parquet('dv_export_latest.parquet')

# Join on canonical key
unified_view = (
    cad_export
    .join(rms_export, on='incident_number', how='left')
    .join(dv_export, on='incident_number', how='left')
    .select(canonical_schema.get_power_bi_columns())
)
```

**Shared Measures** (defined in dictionary):
- Response Time (CAD)
- Case Clearance Rate (RMS)
- DV Recidivism (DV)

#### **Use Case 3: DOJ Submission**

**Objective**: Generate DOJ-compliant DV reports using canonical mappings

**Transformation Pipeline**:
```
DV Raw Data
    └─> Unified Dictionary (DV → DOJ mapping)
        └─> Validation (DOJ schema compliance)
            └─> Export (DOJ XML format)
```

**Mapping Example**:
```json
{
  "dv_to_doj_mapping": {
    "DV_INCIDENT_NUM": "DOJ_CASE_ID",
    "DV_INCIDENT_DT": "DOJ_OCCURRENCE_DATE",
    "DV_VICTIM_AGE": "DOJ_VICTIM_AGE_AT_INCIDENT",
    "DV_OFFENDER_RELATIONSHIP": "DOJ_OFFENDER_RELATIONSHIP_CODE"
  }
}
```

---

### 7. Conflict Resolution Workflow

When source repos have conflicting definitions:

**Detection**:
```python
conflicts = dictionary_builder.detect_conflicts()
# Output: [
#   {
#     'field': 'incident_datetime',
#     'conflict_type': 'data_type',
#     'CAD': 'string',
#     'RMS': 'datetime'
#   }
# ]
```

**Resolution Priority**:
1. **More specific type wins** (datetime > string)
2. **Required=True wins** (more restrictive)
3. **Longer description wins** (more informative)
4. **Manual review** (if above rules don't resolve)

**Escalation**:
- Conflicts logged in `output/conflicts.json`
- Weekly review by Principal Analyst
- Resolution documented in dictionary metadata

---

### 8. Data Governance

#### **Schema Change Protocol**

**Minor Changes** (backward compatible):
- Add new field
- Extend enum values
- Add validation rule

**Process**: Automated sync, no approval needed

**Major Changes** (breaking):
- Remove field
- Change data type
- Modify enum values

**Process**:
1. Source repo submits change request
2. Principal Analyst reviews impact
3. Integration tests run
4. Approval from department leadership
5. Coordinated deployment

#### **Access Control**

| Role | Source Repos | Dictionary Repo | Permissions |
|------|--------------|-----------------|-------------|
| Principal Analyst | Read/Write | Read/Write | Full control |
| Data Analyst | Read | Read | View only |
| Developer | Read | Read | View only |
| GitHub Actions | Read | Read/Write | Automated sync |

---

### 9. Performance Considerations

#### **Extraction Optimization**

```bash
# Shallow clone for faster extraction
git clone --depth 1 <repo_url>

# Sparse checkout (only schema files)
git sparse-checkout set schemas/ mappings/
```

#### **Build Optimization**

```python
# Parallel schema processing
from multiprocessing import Pool

with Pool(processes=4) as pool:
    results = pool.map(process_schema, schema_files)
```

#### **Validation Optimization**

Leverage CAD engine's 26.7x speedup:
```python
import polars as pl

# Use polars for vectorized validation
validated = pl.read_csv('data.csv').with_columns([
    pl.col('address').map(validate_address_vectorized)
])
```

---

### 10. Monitoring & Alerting

#### **Health Checks**

**Daily**:
- CI/CD pipeline status
- Last successful extraction timestamp
- Dictionary build success rate

**Weekly**:
- Schema drift detection
- Conflict count trending
- Validation performance metrics

#### **Alerts**

**Critical** (immediate notification):
- Dictionary build failure
- Schema extraction error
- Validation failure >5%

**Warning** (daily digest):
- New conflicts detected
- Performance degradation >10%
- Schema version mismatch

**Notification Channels**:
- Email: [Principal Analyst]
- Slack: #data-analytics
- Dashboard: Grafana

---

### 11. Rollback Strategy

#### **Dictionary Rollback**

```bash
# Revert to last known good version
git log --oneline  # Find commit hash
git checkout <commit_hash>
make build
make validate
```

#### **Source Repo Rollback**

If source repo schema breaks dictionary:
```bash
# Pin to specific commit in extraction
export DV_DOJ_COMMIT=abc123def
export CAD_ENGINE_COMMIT=ghi789jkl
make extract
```

---

### 12. Future Enhancements

**Phase 2** (Q3 2026):
- Real-time schema synchronization
- GraphQL API for dictionary queries
- Automated mapping generation via ML

**Phase 3** (Q4 2026):
- Multi-agency integration (county sheriff, state police)
- NIBRS 2026 compliance automation
- Predictive data quality scoring

---

## Summary

| Integration Aspect | Implementation | Status |
|-------------------|----------------|--------|
| Schema Sync | Weekly automated pull | ✅ Designed |
| Join Strategy | incident_number primary | ✅ Designed |
| Shared Vocab | Canonical enums | ✅ Designed |
| Data Lineage | Metadata tracking | ✅ Designed |
| Sync Protocol | GitHub Actions | ✅ Designed |
| Monitoring | Health checks + alerts | ✅ Designed |

---

**Next Steps**:
1. Implement extraction automation
2. Deploy schema sync workflow
3. Test cross-repo data joins
4. Monitor integration health

**Contact**: R. A. Carucci (Principal Analyst)  
**Last Updated**: 2025-12-17  
**Version**: 1.0
