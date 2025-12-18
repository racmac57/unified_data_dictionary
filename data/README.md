# Data

Sample and test data for development and validation.

---

## 📁 Structure

```
data/
├── sample/          → Sample datasets for demonstrations
└── test/            → Test datasets for validation
```

---

## 🎯 Purpose

Provides data for:
- Testing schema validation
- Demonstrating transformations
- Validating field mappings
- Benchmarking performance
- Training and documentation

---

## 📋 Data Organization

### **sample/** - Sample Datasets
**Purpose**: Representative data for demonstrations and examples

**Use Cases**:
- Documentation examples
- Training materials
- Demo scenarios
- Proof of concept

**Examples**:
- `sample_cad_incidents.csv` - Sample CAD incident data
- `sample_rms_cases.csv` - Sample RMS case data
- `sample_canonical.json` - Sample unified format

**Characteristics**:
- Small datasets (10-100 records)
- Anonymized/synthetic data
- Covers typical scenarios
- Clean, well-formed data

---

### **test/** - Test Datasets
**Purpose**: Data for testing edge cases and validation

**Use Cases**:
- Unit testing
- Integration testing
- Validation testing
- Edge case verification

**Examples**:
- `test_invalid_dates.csv` - Date validation testing
- `test_missing_fields.csv` - Missing field handling
- `test_edge_cases.json` - Edge case scenarios
- `test_large_dataset.csv` - Performance testing

**Characteristics**:
- Includes edge cases
- Contains validation challenges
- Tests error handling
- Various data quality levels

---

## 🔒 Data Privacy

### **Guidelines**:
- ✅ **DO**: Use synthetic/anonymized data
- ✅ **DO**: Generate fake data for testing
- ✅ **DO**: Sanitize real data before adding
- ❌ **DON'T**: Include PII (Personal Identifiable Information)
- ❌ **DON'T**: Include actual case numbers
- ❌ **DON'T**: Include real addresses (use fake addresses)
- ❌ **DON'T**: Include sensitive information

### **Data Sanitization**:
```python
# Example: Sanitizing CAD data
- Replace names with "JOHN DOE", "JANE DOE"
- Replace addresses with fake addresses
- Replace phone numbers with (555) 555-xxxx
- Replace case numbers with sequential IDs
- Anonymize all identifiable information
```

---

## 📊 Data Formats

### **Supported Formats**:
- **CSV** - Tabular data (most common)
- **JSON** - Structured data
- **YAML** - Configuration-style data
- **Excel** - Multi-sheet datasets (.xlsx)

### **Naming Conventions**:
```
sample_[system]_[type].ext
test_[scenario]_[type].ext

Examples:
sample_cad_incidents.csv
sample_rms_cases.json
test_invalid_dates.csv
test_missing_required_fields.json
```

---

## 🚀 Usage

### **Adding Sample Data**:
```bash
# Create sample file
data/sample/sample_new_system.csv

# Add to documentation
Update docs/guides/ to reference the sample
```

### **Adding Test Data**:
```bash
# Create test file
data/test/test_validation_scenario.csv

# Add test case
Update tests/ to use the test data
```

### **Using in Tests**:
```python
import pandas as pd

# Load test data
df = pd.read_csv('data/test/test_invalid_dates.csv')

# Run validation
results = validate_schema(df)
```

---

## 📝 Data Documentation

### **Each Dataset Should Include**:
- Purpose/use case
- Record count
- Date created
- Data source (if applicable)
- Known issues/limitations

### **Example**:
```markdown
# sample_cad_incidents.csv

**Purpose**: Sample CAD incident data for demonstrations
**Records**: 50
**Created**: 2025-12-17
**Source**: Synthetic data generated for testing
**Fields**: incident_id, datetime, location, type, status
**Notes**: All data is synthetic. No real incident information.
```

---

## 🎯 Data Standards

### **CSV Standards**:
- Use comma delimiters
- Include header row
- Quote text fields with commas
- Use UTF-8 encoding
- Use ISO 8601 for dates (YYYY-MM-DD HH:MM:SS)

### **JSON Standards**:
- Pretty-print with 2-space indentation
- Use consistent field naming
- Include schema version
- Validate against schemas

### **Quality Guidelines**:
- Realistic but synthetic data
- Cover common scenarios
- Include edge cases in test data
- Document data generation method

---

## 🔍 Finding Data

### **Need Sample Data?**
```
Look in data/sample/
```

### **Need Test Cases?**
```
Look in data/test/
```

### **Need More Data?**
```
Use data generation scripts in scripts/
Or create synthetic data manually
```

---

## ⚠️ Important Notes

1. **Never commit real data** - Always use synthetic/anonymized data
2. **Keep datasets small** - Sample data should be < 1 MB
3. **Test data is version controlled** - Keep it in Git
4. **Document everything** - Explain what each dataset contains
5. **Update regularly** - Keep test data aligned with schemas

---

## 📊 Current Status

| Folder | Status | Files |
|--------|--------|-------|
| **sample/** | 🚧 Ready for data | 0 files |
| **test/** | 🚧 Ready for data | 0 files |

---

## 🚀 Next Steps

1. **Generate sample CAD data** → `sample/sample_cad_incidents.csv`
2. **Generate sample RMS data** → `sample/sample_rms_cases.csv`
3. **Create test datasets** → Edge cases and validation tests
4. **Document each dataset** → README for each data file
5. **Add to tests** → Reference in test suite

---

**Last Updated**: 2025-12-17  
**Status**: Ready for data

