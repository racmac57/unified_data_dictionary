# 🕒 2025-12-17-20-02-00
# FILE_PLACEMENT_GUIDE.md
# Author: R. A. Carucci
# Purpose: Complete guide for organizing downloaded files into unified_data_dictionary project structure

# File Placement Guide
**Project**: Unified Data Dictionary  
**Base Directory**: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary`

---

## Step 1: Run Folder Structure Script

```batch
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"

REM Copy and run the CREATE_STRUCTURE.bat script (provided separately)
CREATE_STRUCTURE.bat
```

---

## Step 2: Move Files from Downloads

### Core Documentation Files

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `README.md` or `README (1).md` or `README (2).md` | `.\README.md` | Main project README - use the most complete version |
| `DELIVERABLES_SUMMARY.md` | `.\DELIVERABLES_SUMMARY.md` | Executive summary |
| `IMPLEMENTATION_ROADMAP.md` | `.\docs\IMPLEMENTATION_ROADMAP.md` | 20-week plan |
| `INTEGRATION_STRATEGY.md` | `.\docs\INTEGRATION_STRATEGY.md` | Cross-repo integration |

### Configuration Files

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `pyproject.toml` | `.\pyproject.toml` | Python dependencies |
| `Makefile` | `.\Makefile` | Build automation |
| `.gitignore` | `.\.gitignore` | Git exclusions |
| `.env.example` | `.\.env.example` | Environment template |

### Python Source Files

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `extract_from_repos.py` | `.\src\extract_from_repos.py` | Schema extraction |
| `build_dictionary.py` | `.\src\build_dictionary.py` | Dictionary builder |
| `generate_excel_output.py` | `.\src\generate_excel_output.py` | Excel generator |
| `cli.py` | `.\src\cli.py` | CLI interface |

### Schema & Mapping Files (from CAD repos)

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `cad_field_map_latest.json` | `.\mappings\cad_field_map.json` | CAD field definitions |
| `cad_fields_schema_latest.json` | `.\schemas\cad_schema.json` | CAD schema |
| `rms_field_map_latest.json` | `.\mappings\rms_field_map.json` | RMS field definitions |
| `rms_fields_schema_latest.json` | `.\schemas\rms_schema.json` | RMS schema |
| `cad_to_rms_field_map_latest.json` | `.\mappings\cad_to_rms_map.json` | CAD→RMS mapping |
| `rms_to_cad_field_map_latest.json` | `.\mappings\rms_to_cad_map.json` | RMS→CAD mapping |
| `transformation_spec.json` | `.\mappings\transformation_spec.json` | Transformation rules |

### Test Files (if needed)

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `test_allowed_values.py` | `.\tests\test_allowed_values.py` | Optional |
| `test_coordinate_validation.py` | `.\tests\test_coordinate_validation.py` | Optional |
| `test_datetime_parsing.py` | `.\tests\test_datetime_parsing.py` | Optional |
| `test_join_keys.py` | `.\tests\test_join_keys.py` | Optional |

### Archive Chat Logs

| Source (Downloads) | Destination | Notes |
|-------------------|-------------|-------|
| `2025_12_17_17_00_00_Repository_code_review_for_data_analysis_projects\` | `.\docs\chats\2025_12_17_review\` | Original chat |
| `2025_12_17_17_00_00_Claude-Repository_code_review_for_data_analysis_projects\` | `.\docs\chats\2025_12_17_continuation\` | Continuation chat |

---

## Step 3: Automated Move Script

Save this as `MOVE_FILES.bat` and run it from the unified_data_dictionary directory:

```batch
@echo off
echo Moving files from Downloads to unified_data_dictionary...

set DOWNLOADS=C:\Users\carucci_r\Downloads
set TARGET=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary

REM Documentation
if exist "%DOWNLOADS%\README.md" copy "%DOWNLOADS%\README.md" "%TARGET%\README.md"
if exist "%DOWNLOADS%\DELIVERABLES_SUMMARY.md" copy "%DOWNLOADS%\DELIVERABLES_SUMMARY.md" "%TARGET%\DELIVERABLES_SUMMARY.md"
if exist "%DOWNLOADS%\IMPLEMENTATION_ROADMAP.md" copy "%DOWNLOADS%\IMPLEMENTATION_ROADMAP.md" "%TARGET%\docs\IMPLEMENTATION_ROADMAP.md"
if exist "%DOWNLOADS%\INTEGRATION_STRATEGY.md" copy "%DOWNLOADS%\INTEGRATION_STRATEGY.md" "%TARGET%\docs\INTEGRATION_STRATEGY.md"

REM Configuration
if exist "%DOWNLOADS%\pyproject.toml" copy "%DOWNLOADS%\pyproject.toml" "%TARGET%\pyproject.toml"
if exist "%DOWNLOADS%\Makefile" copy "%DOWNLOADS%\Makefile" "%TARGET%\Makefile"
if exist "%DOWNLOADS%\.gitignore" copy "%DOWNLOADS%\.gitignore" "%TARGET%\.gitignore"
if exist "%DOWNLOADS%\.env.example" copy "%DOWNLOADS%\.env.example" "%TARGET%\.env.example"

REM Python source
if exist "%DOWNLOADS%\extract_from_repos.py" copy "%DOWNLOADS%\extract_from_repos.py" "%TARGET%\src\extract_from_repos.py"
if exist "%DOWNLOADS%\build_dictionary.py" copy "%DOWNLOADS%\build_dictionary.py" "%TARGET%\src\build_dictionary.py"
if exist "%DOWNLOADS%\generate_excel_output.py" copy "%DOWNLOADS%\generate_excel_output.py" "%TARGET%\src\generate_excel_output.py"
if exist "%DOWNLOADS%\cli.py" copy "%DOWNLOADS%\cli.py" "%TARGET%\src\cli.py"

REM Schemas
if exist "%DOWNLOADS%\cad_fields_schema_latest.json" copy "%DOWNLOADS%\cad_fields_schema_latest.json" "%TARGET%\schemas\cad_schema.json"
if exist "%DOWNLOADS%\rms_fields_schema_latest.json" copy "%DOWNLOADS%\rms_fields_schema_latest.json" "%TARGET%\schemas\rms_schema.json"
if exist "%DOWNLOADS%\canonical_schema.json" copy "%DOWNLOADS%\canonical_schema.json" "%TARGET%\schemas\canonical_schema.json"

REM Mappings
if exist "%DOWNLOADS%\cad_field_map_latest.json" copy "%DOWNLOADS%\cad_field_map_latest.json" "%TARGET%\mappings\cad_field_map.json"
if exist "%DOWNLOADS%\rms_field_map_latest.json" copy "%DOWNLOADS%\rms_field_map_latest.json" "%TARGET%\mappings\rms_field_map.json"
if exist "%DOWNLOADS%\cad_to_rms_field_map_latest.json" copy "%DOWNLOADS%\cad_to_rms_field_map_latest.json" "%TARGET%\mappings\cad_to_rms_map.json"
if exist "%DOWNLOADS%\rms_to_cad_field_map_latest.json" copy "%DOWNLOADS%\rms_to_cad_field_map_latest.json" "%TARGET%\mappings\rms_to_cad_map.json"
if exist "%DOWNLOADS%\transformation_spec.json" copy "%DOWNLOADS%\transformation_spec.json" "%TARGET%\mappings\transformation_spec.json"

REM Archive chat logs
mkdir "%TARGET%\docs\chats\2025_12_17_review" 2>nul
mkdir "%TARGET%\docs\chats\2025_12_17_continuation" 2>nul
xcopy "%DOWNLOADS%\2025_12_17_17_00_00_Repository_code_review_for_data_analysis_projects\*" "%TARGET%\docs\chats\2025_12_17_review\" /E /I /Y
xcopy "%DOWNLOADS%\2025_12_17_17_00_00_Claude-Repository_code_review_for_data_analysis_projects\*" "%TARGET%\docs\chats\2025_12_17_continuation\" /E /I /Y

echo.
echo ✅ Files moved successfully!
echo.
echo Next steps:
echo 1. Review files in target directory
echo 2. Delete duplicate files from Downloads
echo 3. Initialize Git repository
echo.
pause
```

---

## Step 4: Verify File Structure

After running the scripts, your directory should look like this:

```
unified_data_dictionary\
├── README.md                           ✅
├── DELIVERABLES_SUMMARY.md            ✅
├── CHANGELOG.md                        ✅ (create new)
├── Makefile                            ✅
├── pyproject.toml                      ✅
├── .gitignore                          ✅
├── .env.example                        ✅
│
├── src\
│   ├── __init__.py                     ✅
│   ├── extract_from_repos.py          ✅
│   ├── build_dictionary.py            ✅
│   ├── generate_excel_output.py       ✅
│   ├── cli.py                          ✅
│   └── utils\
│       └── __init__.py                 ✅
│
├── schemas\
│   ├── canonical_schema.json          ✅
│   ├── cad_schema.json                ✅
│   └── rms_schema.json                ✅
│
├── mappings\
│   ├── cad_field_map.json             ✅
│   ├── rms_field_map.json             ✅
│   ├── cad_to_rms_map.json            ✅
│   ├── rms_to_cad_map.json            ✅
│   └── transformation_spec.json        ✅
│
├── validators\                         📁 (empty for now)
├── tests\                              📁 (optional test files)
├── benchmarks\                         📁 (empty for now)
├── output\                             📁 (empty, created on build)
├── logs\                               📁 (empty, created on run)
│
├── docs\
│   ├── IMPLEMENTATION_ROADMAP.md      ✅
│   ├── INTEGRATION_STRATEGY.md        ✅
│   └── chats\
│       ├── 2025_12_17_review\         ✅
│       └── 2025_12_17_continuation\   ✅
│
├── scripts\                            📁 (empty for now)
└── .github\
    └── workflows\                      📁 (empty, for CI/CD)
```

---

## Step 5: Missing Files Checklist

You may need to download or create these files:

### From This Chat (if not already downloaded):
- [ ] `DELIVERABLES_SUMMARY.md`
- [ ] `IMPLEMENTATION_ROADMAP.md`
- [ ] `INTEGRATION_STRATEGY.md`
- [ ] `Makefile`
- [ ] `.gitignore`
- [ ] `.env.example`
- [ ] `canonical_schema.json`

### To Be Created:
- [ ] `CHANGELOG.md` (see separate file)
- [ ] `src\utils\json_handler.py`
- [ ] `src\utils\schema_merger.py`
- [ ] `src\utils\performance_profiler.py`
- [ ] Test files in `tests\`
- [ ] GitHub Actions workflow in `.github\workflows\`

---

## Step 6: Initialize Git Repository

After organizing files:

```batch
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"

git init
git add .
git commit -m "Initial commit: Unified data dictionary structure"

REM If creating GitHub repo
git remote add origin https://github.com/racmac57/unified_data_dictionary.git
git branch -M main
git push -u origin main
```

---

## Notes

- **Files to Keep**: All JSON schema/mapping files are valuable for the extraction process
- **Files to Archive**: Chat transcripts in `docs\chats\`
- **Files to Create**: CHANGELOG.md (see separate artifact)
- **Optional**: Test files can be added later as needed

---

**Last Updated**: 2025-12-17  
**Status**: Ready for organization
