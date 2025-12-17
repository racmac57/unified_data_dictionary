# 🕒 2025-12-17-20-00-00
# unified_data_dictionary/CREATE_STRUCTURE.bat
# Author: R. A. Carucci
# Purpose: Batch script to create complete folder structure for unified data dictionary project

@echo off
echo Creating unified_data_dictionary folder structure...

REM Main directories
mkdir src\utils
mkdir schemas
mkdir mappings
mkdir validators
mkdir tests\fixtures
mkdir benchmarks\results
mkdir output
mkdir logs
mkdir docs
mkdir scripts
mkdir .github\workflows

REM Create placeholder files
type nul > src\__init__.py
type nul > src\utils\__init__.py
type nul > tests\__init__.py

echo.
echo ✅ Folder structure created successfully!
echo.
echo Next steps:
echo 1. Run the MOVE_FILES.bat script to organize downloaded files
echo 2. Review the FILE_PLACEMENT_GUIDE.md for details
echo.
pause
