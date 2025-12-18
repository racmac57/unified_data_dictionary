# Unified Data Dictionary (UDD)

> **Centralized schema management and field mapping system for CAD, RMS, and DV systems.**

[![Version](https://img.shields.io/badge/version-0.2.1-blue.svg)](CHANGELOG.md)
[![Status](https://img.shields.io/badge/status-active_development-green.svg)](SUMMARY.md)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 📖 Overview

The **Unified Data Dictionary** is a comprehensive tool designed to extract, standardize, and map data schemas across the Hackensack Police Department's disparate systems (CAD, RMS, DV, and DOJ). It serves as the "Single Source of Truth" for data analysis, reporting, and integration.

### Core Capabilities
* **Schema Extraction**: Automated extraction of schemas from source code repositories.
* **Canonical Modeling**: Defines a unified standard for data fields.
* **Bidirectional Mapping**: Maps fields between systems (e.g., `CAD <-> RMS`).
* **Documentation Generation**: Auto-generates Excel data dictionaries for stakeholders.
* **Maintenance**: Scripts to clean up duplicate/redundant processing files.

---

## 📂 Project Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Python source code (`extract`, `build`, `cli`). |
| `schemas/` | JSON schema definitions (Canonical, CAD, RMS). |
| `mappings/` | CSV/JSON field mapping files. |
| `docs/` | Project documentation (Setup, Planning, API). |
| `scripts/` | Utility scripts (e.g., `cleanup_duplicates.ps1`). |
| `templates/`| Reusable templates for new schemas. |
| `output/` | Generated artifacts (Excel dictionaries). |

> 📌 **Quick View**: See [SUMMARY.md](SUMMARY.md) for a one-page dashboard of the project status.

---

## ⚡ Quick Start

### 1. Installation
```bash
# Clone repository
git clone [https://github.com/racmac57/unified_data_dictionary.git](https://github.com/racmac57/unified_data_dictionary.git)

# Install dependencies
pip install -r requirements.txt

```

### 2. Basic Usage (CLI)

```bash
# Extract schemas from a source
python src/cli.py extract --source "C:/Path/To/Repo" --system cad

# Build the dictionary
python src/cli.py build

# Generate Excel documentation
python src/cli.py excel --output "MyDictionary.xlsx"

```

### 3. Maintenance

To clean up older processed chunks from `KB_Shared`:

```powershell
pwsh -File "scripts/cleanup_duplicates.ps1"

```

---

## 📚 Documentation

* **[Setup Guide](https://www.google.com/search?q=docs/setup/PROJECT_SETUP_SUMMARY.md)**: Installation and environment config.
* **[Roadmap](https://www.google.com/search?q=docs/planning/IMPLEMENTATION_ROADMAP.md)**: 20-week implementation plan.
* **[Changelog](CHANGELOG.md)**: Version history and recent updates.

---

**Maintained By**: R. A. Carucci (Principal Analyst)
**Location**: `OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary`