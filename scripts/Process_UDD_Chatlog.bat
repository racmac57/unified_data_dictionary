@echo off
REM ============================================================================
REM Process Chatlog for unified_data_dictionary
REM ============================================================================
REM Purpose: Automated chatlog processing for unified_data_dictionary project
REM Author: R. A. Carucci
REM Date: 2025-12-17
REM Version: 1.0.0
REM ============================================================================

setlocal enabledelayedexpansion

REM Project paths
set "PROJECT_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
set "RAW_DIR=%PROJECT_ROOT%\docs\chatlogs\raw"
set "CHUNKED_DIR=%PROJECT_ROOT%\docs\chatlogs\chunked"
set "CHUNKER_BATCH=C:\_chunker\opus\Chunker_Move.bat"
set "CHUNKER_OUTPUT=C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

REM Check if file was provided
if "%~1"=="" (
    echo.
    echo ============================================================================
    echo  UNIFIED DATA DICTIONARY - CHATLOG PROCESSOR
    echo ============================================================================
    echo.
    echo ERROR: No file provided!
    echo.
    echo Usage:
    echo   1. Drag and drop a chatlog .md file onto this script
    echo   2. Or run from DOpus button with selected file
    echo.
    echo ============================================================================
    pause
    exit /b 1
)

set "INPUT_FILE=%~1"
set "FILENAME=%~nx1"

REM Verify input file exists
if not exist "%INPUT_FILE%" (
    echo.
    echo ERROR: File not found: %INPUT_FILE%
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo  UNIFIED DATA DICTIONARY - CHATLOG PROCESSOR
echo ============================================================================
echo.
echo Processing: %FILENAME%
echo Project: unified_data_dictionary
echo.
echo ============================================================================

REM ============================================================================
REM STEP 1: Move to raw/
REM ============================================================================
echo.
echo [STEP 1/4] Moving to raw folder...

if not exist "%RAW_DIR%" (
    echo Creating raw directory...
    mkdir "%RAW_DIR%"
)

copy "%INPUT_FILE%" "%RAW_DIR%\" >nul
if errorlevel 1 (
    echo ERROR: Failed to copy to raw folder
    pause
    exit /b 1
)

echo   [OK] Saved to: docs\chatlogs\raw\%FILENAME%

REM ============================================================================
REM STEP 2: Chunk the file
REM ============================================================================
echo.
echo [STEP 2/4] Chunking file...

REM Check if chunker exists
if not exist "%CHUNKER_BATCH%" (
    echo ERROR: Chunker not found at %CHUNKER_BATCH%
    pause
    exit /b 1
)

REM Run chunker on the raw file
call "%CHUNKER_BATCH%" "%RAW_DIR%\%FILENAME%" >nul 2>&1

REM Wait for chunking to complete (max 30 seconds)
set "TIMEOUT_COUNT=0"
:WAIT_FOR_CHUNK
timeout /t 1 /nobreak >nul
set /a TIMEOUT_COUNT+=1

REM Check if chunked file appeared in output
dir "%CHUNKER_OUTPUT%\%FILENAME%" >nul 2>&1
if errorlevel 1 (
    if %TIMEOUT_COUNT% lss 30 goto WAIT_FOR_CHUNK
    echo ERROR: Chunking timed out
    pause
    exit /b 1
)

echo   [OK] File chunked successfully

REM ============================================================================
REM STEP 3: Move chunked file
REM ============================================================================
echo.
echo [STEP 3/4] Moving chunked file...

if not exist "%CHUNKED_DIR%" (
    echo Creating chunked directory...
    mkdir "%CHUNKED_DIR%"
)

REM Wait a moment for file system
timeout /t 2 /nobreak >nul

REM Move chunked file
if exist "%CHUNKER_OUTPUT%\%FILENAME%" (
    move /Y "%CHUNKER_OUTPUT%\%FILENAME%" "%CHUNKED_DIR%\" >nul
    if errorlevel 1 (
        echo ERROR: Failed to move chunked file
        pause
        exit /b 1
    )
    echo   [OK] Saved to: docs\chatlogs\chunked\%FILENAME%
) else (
    echo ERROR: Chunked file not found in output directory
    pause
    exit /b 1
)

REM ============================================================================
REM STEP 4: Cleanup
REM ============================================================================
echo.
echo [STEP 4/4] Cleaning up...

REM Delete original file from Downloads (optional, comment out if you want to keep)
REM del "%INPUT_FILE%" >nul 2>&1

echo   [OK] Process complete

REM ============================================================================
REM SUMMARY
REM ============================================================================
echo.
echo ============================================================================
echo  PROCESSING COMPLETE
echo ============================================================================
echo.
echo File: %FILENAME%
echo.
echo Locations:
echo   Raw:     %RAW_DIR%\%FILENAME%
echo   Chunked: %CHUNKED_DIR%\%FILENAME%
echo.
echo ============================================================================

REM Success - auto-close after 3 seconds
timeout /t 3 /nobreak >nul
exit /b 0

