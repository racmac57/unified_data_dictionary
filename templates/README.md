# Templates

Reusable templates for schemas, configurations, and mappings.

---

## 📁 Structure

```
templates/
├── schemas/          → Schema templates (CAD, RMS, canonical)
├── configs/          → Configuration templates
└── mappings/         → Field mapping templates
```

---

## 🎯 Purpose

Templates provide starting points for:
- Creating new schema definitions
- Configuring new data sources
- Defining field mappings between systems

---

## 📋 Templates

### **schemas/** - Schema Templates
**Purpose**: Templates for defining data schemas

**Use Cases**:
- Adding new CAD system schema
- Adding new RMS system schema
- Extending canonical schema

**Example**: `cad_schema_template.json`

---

### **configs/** - Configuration Templates
**Purpose**: Templates for system configurations

**Use Cases**:
- Configuring new data source
- Setting up extraction rules
- Defining validation rules

**Example**: `data_source_config_template.yaml`

---

### **mappings/** - Field Mapping Templates
**Purpose**: Templates for field mappings between systems

**Use Cases**:
- Mapping new CAD system to canonical
- Mapping new RMS system to canonical
- Defining transformation rules

**Example**: `cad_to_canonical_template.json`

---

## 🚀 Usage

### **Creating from Template**:
```bash
# Copy template
cp templates/schemas/cad_schema_template.json schemas/new_cad_schema.json

# Customize for your system
# Edit schemas/new_cad_schema.json
```

### **Adding New Template**:
```bash
# Create in appropriate folder
templates/schemas/your_template.json
templates/configs/your_config_template.yaml
templates/mappings/your_mapping_template.json
```

---

## 📝 Template Standards

### **Naming**:
- Use `*_template.json` or `*_template.yaml`
- Descriptive names (e.g., `cad_schema_template.json`)

### **Content**:
- Include comments/descriptions for each field
- Use example values
- Document required vs optional fields
- Include validation rules where applicable

### **Versioning**:
- Version templates when making breaking changes
- Keep old versions for compatibility

---

## 🎨 Template Examples

### **Schema Template Structure**:
```json
{
  "name": "Example CAD System",
  "version": "1.0.0",
  "fields": [
    {
      "name": "field_name",
      "type": "string",
      "required": true,
      "description": "Field description",
      "validation": {
        "pattern": "regex_pattern",
        "max_length": 100
      }
    }
  ]
}
```

### **Config Template Structure**:
```yaml
data_source:
  name: "Source Name"
  type: "CAD"  # or "RMS"
  connection:
    host: "hostname"
    port: 5432
    database: "dbname"
  extraction:
    tables: []
    fields: []
```

### **Mapping Template Structure**:
```json
{
  "source_system": "CAD_System_Name",
  "target_system": "canonical",
  "version": "1.0.0",
  "mappings": [
    {
      "source_field": "cad_field_name",
      "target_field": "canonical_field_name",
      "transformation": "direct|transform|lookup",
      "notes": "Mapping explanation"
    }
  ]
}
```

---

**Last Updated**: 2025-12-17  
**Status**: Ready for templates

