@echo off
REM ============================================================================
REM process_chatlog.bat - Automated Chatlog Processing
REM ============================================================================
REM Usage: process_chatlog.bat <filename.md>
REM This script:
REM   1. Moves the chatlog to docs/chatlogs/raw/
REM   2. Runs the chunker on it
REM   3. Monitors for output
REM   4. Copies chunked files to docs/chatlogs/chunked/
REM ============================================================================

setlocal enabledelayedexpansion

REM Define paths
set "PROJECT_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
set "RAW_DIR=%PROJECT_ROOT%\docs\chatlogs\raw"
set "CHUNKED_DIR=%PROJECT_ROOT%\docs\chatlogs\chunked"
set "CHUNKER_DIR=C:\_chunker\opus"
set "OUTPUT_DIR=C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

REM Check if filename provided
if "%~1"=="" (
    echo ERROR: No filename provided
    echo Usage: process_chatlog.bat ^<filename.md^>
    pause
    exit /b 1
)

set "FILENAME=%~1"
set "BASENAME=%~n1"

echo.
echo ============================================================================
echo  CHATLOG PROCESSING AUTOMATION
echo ============================================================================
echo.
echo File: %FILENAME%
echo.

REM Step 1: Move to raw directory
echo [1/5] Moving chatlog to raw directory...
if exist "%FILENAME%" (
    move /Y "%FILENAME%" "%RAW_DIR%\" >nul 2>&1
    if !errorlevel! equ 0 (
        echo   [OK] Moved to: %RAW_DIR%\%FILENAME%
    ) else (
        echo   [ERROR] Failed to move file
        pause
        exit /b 1
    )
) else (
    echo   [ERROR] File not found: %FILENAME%
    pause
    exit /b 1
)

REM Step 2: Run Chunker
echo.
echo [2/5] Running chunker...
cd /d "%CHUNKER_DIR%"
call Chunker_Move.bat "%RAW_DIR%\%FILENAME%"
echo   [OK] Chunker started

REM Step 3: Start watcher
echo.
echo [3/5] Starting chunker watcher...
start "Chunker Watcher" cmd /c "cd /d %CHUNKER_DIR% && Start_Chunker_Watcher.bat"
echo   [OK] Watcher started in new window

REM Step 4: Monitor output directory
echo.
echo [4/5] Monitoring output directory...
echo   Waiting for chunked files to appear...
set TIMEOUT=60
set COUNT=0

:WAIT_LOOP
timeout /t 2 /nobreak >nul
set /a COUNT+=2

REM Check if chunked files exist
if exist "%OUTPUT_DIR%\%BASENAME%*.md" (
    echo   [OK] Chunked files detected!
    goto COPY_FILES
)

if %COUNT% geq %TIMEOUT% (
    echo   [WARNING] Timeout reached. Files may still be processing.
    echo   Check: %OUTPUT_DIR%
    pause
    goto COPY_FILES
)

goto WAIT_LOOP

:COPY_FILES
REM Step 5: Copy chunked files
echo.
echo [5/5] Copying chunked files...
xcopy /Y "%OUTPUT_DIR%\%BASENAME%*.md" "%CHUNKED_DIR%\" >nul 2>&1
if !errorlevel! equ 0 (
    echo   [OK] Chunked files copied to: %CHUNKED_DIR%
    
    REM List copied files
    echo.
    echo Files created:
    dir /B "%CHUNKED_DIR%\%BASENAME%*.md"
) else (
    echo   [WARNING] No files found or copy failed
    echo   Check: %OUTPUT_DIR%
)

echo.
echo ============================================================================
echo  PROCESSING COMPLETE
echo ============================================================================
echo.
echo Raw chatlog:     %RAW_DIR%\%FILENAME%
echo Chunked files:   %CHUNKED_DIR%\%BASENAME%_*.md
echo Output monitor:  %OUTPUT_DIR%
echo.
echo ============================================================================

pause

