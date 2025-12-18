# Examples

Usage examples for the unified data dictionary CLI and API.

---

## 📁 Structure

```
examples/
├── cli/          → Command-line interface examples
└── api/          → Python API usage examples
```

---

## 🎯 Purpose

Provides practical examples for:
- Using the `udd` CLI commands
- Working with the Python API
- Common workflows and patterns
- Integration scenarios

---

## 📋 Examples Organization

### **cli/** - CLI Examples
**Purpose**: Command-line usage examples

**Examples**:
- `basic_usage.md` - Getting started with udd CLI
- `extract_schemas.md` - Extracting schemas from repositories
- `build_dictionary.md` - Building the unified dictionary
- `validate_mappings.md` - Validating field mappings
- `generate_excel.md` - Generating Excel outputs

**Format**: Markdown files with command examples and explanations

---

### **api/** - API Examples
**Purpose**: Python API usage examples

**Examples**:
- `basic_api_usage.py` - Getting started with the Python API
- `schema_extraction.py` - Extracting schemas programmatically
- `field_mapping.py` - Working with field mappings
- `validation.py` - Validating data against schemas
- `custom_workflows.py` - Building custom workflows

**Format**: Python scripts with comments and documentation

---

## 🚀 CLI Examples

### **Basic Usage**:
```bash
# Show project status
udd status

# Extract schemas from repositories
udd extract --source /path/to/cad/repo --system cad

# Build unified dictionary
udd build

# Validate field mappings
udd validate

# Generate Excel output
udd excel --output unified_dictionary.xlsx
```

### **Advanced Workflows**:
```bash
# Extract, build, and validate in one go
udd extract --source /path/to/repos && udd build && udd validate

# Generate reports
udd excel --output reports/dictionary_$(date +%Y%m%d).xlsx
```

---

## 🐍 Python API Examples

### **Basic Usage**:
```python
from unified_data_dictionary import DictionaryBuilder, SchemaExtractor

# Extract schemas
extractor = SchemaExtractor()
cad_schema = extractor.extract_from_repo('/path/to/cad/repo')

# Build dictionary
builder = DictionaryBuilder()
builder.add_schema('cad', cad_schema)
dictionary = builder.build()

# Validate mappings
validation_results = builder.validate()
```

### **Advanced Workflows**:
```python
# Custom validation
from unified_data_dictionary import Validator

validator = Validator(dictionary)
results = validator.validate_field_mappings()
results = validator.validate_data_types()
results = validator.validate_constraints()

# Generate reports
from unified_data_dictionary import ExcelGenerator

generator = ExcelGenerator(dictionary)
generator.create_workbook('output.xlsx')
```

---

## 📖 Example Categories

### **Getting Started**:
- Basic CLI usage
- Simple API usage
- Project setup

### **Schema Management**:
- Extracting schemas from repositories
- Defining custom schemas
- Updating existing schemas
- Schema versioning

### **Field Mappings**:
- Creating field mappings
- Bidirectional mappings
- Transformation rules
- Validation rules

### **Validation**:
- Schema validation
- Data validation
- Mapping validation
- Custom validation rules

### **Output Generation**:
- Excel generation
- JSON export
- HTML reports
- Custom formats

### **Integration**:
- Integrating with CAD systems
- Integrating with RMS systems
- ETL pipelines
- API endpoints

---

## 🎨 Example Format

### **CLI Examples** (Markdown):
```markdown
# Example: Extracting CAD Schema

## Description
Extract schema from CAD repository and save to schemas folder.

## Command
`bash
udd extract \
  --source /path/to/cad/repo \
  --system cad \
  --output schemas/cad_fields_schema.json
`

## Expected Output
`
Extracting schema from /path/to/cad/repo...
Found 45 fields
Saved to schemas/cad_fields_schema.json
`

## Notes
- Ensure repository path is correct
- Schema file will be validated automatically
- Use --verbose for detailed output
```

### **API Examples** (Python):
```python
"""
Example: Building Unified Dictionary

This example demonstrates how to build a unified data dictionary
from CAD and RMS schemas.
"""

from unified_data_dictionary import DictionaryBuilder

# Initialize builder
builder = DictionaryBuilder()

# Load schemas
builder.load_schema('schemas/cad_fields_schema.json', 'cad')
builder.load_schema('schemas/rms_fields_schema.json', 'rms')

# Load mappings
builder.load_mappings('mappings/cad_to_rms_mapping.csv')

# Build dictionary
dictionary = builder.build()

# Validate
if builder.validate():
    print("✅ Dictionary is valid")
    dictionary.save('output/unified_dictionary.json')
else:
    print("❌ Validation failed")
    for error in builder.get_errors():
        print(f"  - {error}")
```

---

## 🔍 Finding Examples

### **Need CLI Help?**
```bash
# Check CLI examples
examples/cli/

# Or use built-in help
udd --help
udd extract --help
```

### **Need API Help?**
```python
# Check API examples
examples/api/

# Or use docstrings
from unified_data_dictionary import DictionaryBuilder
help(DictionaryBuilder)
```

---

## 📝 Contributing Examples

### **Adding CLI Examples**:
1. Create markdown file in `examples/cli/`
2. Use descriptive filename (e.g., `extract_schemas.md`)
3. Include description, command, output, and notes
4. Test the example before committing

### **Adding API Examples**:
1. Create Python file in `examples/api/`
2. Use descriptive filename (e.g., `schema_extraction.py`)
3. Include docstring with description
4. Add inline comments for clarity
5. Make it runnable (if possible)
6. Test the example before committing

---

## 🎯 Example Standards

### **CLI Examples**:
- Show realistic use cases
- Include expected output
- Document common issues
- Provide troubleshooting tips

### **API Examples**:
- Use clear variable names
- Include type hints
- Add comprehensive comments
- Handle errors gracefully
- Show best practices

### **Both**:
- Keep examples simple and focused
- One concept per example
- Build complexity gradually
- Link to related examples
- Keep examples up to date with code

---

## 📊 Current Status

| Folder | Status | Files |
|--------|--------|-------|
| **cli/** | 🚧 Ready for examples | 0 files |
| **api/** | 🚧 Ready for examples | 0 files |

---

## 🚀 Next Steps

1. **Create basic CLI examples** → Getting started guide
2. **Create basic API examples** → Simple Python usage
3. **Add workflow examples** → End-to-end scenarios
4. **Add integration examples** → Real-world use cases
5. **Create Jupyter notebooks** → Interactive examples

---

## 💡 Ideas for Examples

### **CLI**:
- [ ] Getting started with udd
- [ ] Extracting schemas from multiple repos
- [ ] Building custom dictionaries
- [ ] Validating against standards
- [ ] Generating reports
- [ ] Automating with bash scripts

### **API**:
- [ ] Basic dictionary building
- [ ] Custom schema definitions
- [ ] Programmatic validation
- [ ] Integration with pandas
- [ ] ETL pipeline example
- [ ] REST API wrapper

### **Jupyter Notebooks**:
- [ ] Interactive schema exploration
- [ ] Visual field mapping
- [ ] Data quality dashboard
- [ ] Validation report analysis

---

**Last Updated**: 2025-12-17  
**Status**: Ready for examples

