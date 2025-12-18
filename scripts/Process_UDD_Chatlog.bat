@echo off
REM ============================================================================
REM Process Chatlog for unified_data_dictionary
REM ============================================================================
REM Version: 1.0.7 (Fixed: Atomic Staging to prevent duplicate processing)
REM ============================================================================

setlocal enabledelayedexpansion

REM Project paths
set "PROJECT_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
set "RAW_DIR=%PROJECT_ROOT%\docs\chatlogs\raw"
set "CHUNKED_DIR=%PROJECT_ROOT%\docs\chatlogs\chunked"
set "CHUNKER_ROOT=C:\_chunker\opus"

REM External paths
set "CHUNKER_INPUT=C:\_chunker\02_data"
set "CHUNKER_OUTPUT=C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

REM ============================================================================
REM CHECK: File Selection
REM ============================================================================
if "%~1"=="" (
    echo [ERROR] No file selected.
    pause
    exit /b 1
)

set "INPUT_FILE=%~1"
set "FILENAME=%~nx1"
set "BASENAME=%~n1"

echo.
echo ============================================================================
echo  UNIFIED DATA DICTIONARY - CHATLOG PROCESSOR v1.0.7
echo ============================================================================
echo.
echo Processing: %FILENAME%

REM ============================================================================
REM STEP 1: Move to Project Raw Folder
REM ============================================================================
echo [STEP 1/4] Saving to project raw folder...

if not exist "%RAW_DIR%" mkdir "%RAW_DIR%"

if /i "%~dp1"=="%RAW_DIR%\" (
    echo   [INFO] File is already in raw folder.
) else (
    move /Y "%INPUT_FILE%" "%RAW_DIR%\" >nul
    if errorlevel 1 (
        echo ERROR: Failed to move to raw folder.
        pause
        exit /b 1
    )
    echo   [OK] Saved to: docs\chatlogs\raw\%FILENAME%
)

REM ============================================================================
REM STEP 2: Send Atomic Copy to Chunker
REM ============================================================================
echo.
echo [STEP 2/4] Sending atomic copy to chunker...

REM 1. Copy as .part (Watcher ignores this)
copy /Y "%RAW_DIR%\%FILENAME%" "%CHUNKER_INPUT%\%FILENAME%.part" >nul

REM 2. Rename to final .md (Watcher sees ONE event)
ren "%CHUNKER_INPUT%\%FILENAME%.part" "%FILENAME%"

echo   Starting Watcher...
start "Chunker Watcher" cmd /c "cd /d %CHUNKER_ROOT% && Start_Chunker_Watcher.bat"

echo   [OK] File queued for processing

REM ============================================================================
REM STEP 3: Monitor for Output
REM ============================================================================
echo.
echo [STEP 3/4] Waiting for processed files...
echo   Target: %BASENAME%...

set "TIMEOUT_COUNT=0"
set "FOUND_PATH="

:WAIT_FOR_CHUNK
timeout /t 2 /nobreak >nul
set /a TIMEOUT_COUNT+=1

REM Debug ticker every 10 seconds
set /a MOD_CHECK=%TIMEOUT_COUNT% %% 5
if %MOD_CHECK%==0 echo   ...scanning (%TIMEOUT_COUNT%s)

REM Look for a DIRECTORY containing the basename
for /d %%D in ("%CHUNKER_OUTPUT%\*%BASENAME%*") do (
    set "FOUND_PATH=%%D"
    goto FILES_FOUND
)

REM Wait max 90 seconds
if %TIMEOUT_COUNT% lss 45 goto WAIT_FOR_CHUNK

echo.
echo [ERROR] Chunking Timed Out
echo The watcher may be busy or the file is very large.
echo Please check: %CHUNKER_OUTPUT%
pause
exit /b 1

:FILES_FOUND
echo   [OK] Found output: %FOUND_PATH%

REM ============================================================================
REM STEP 4: Copy Output to Project
REM ============================================================================
echo.
echo [STEP 4/4] Retrieving chunked files...

if not exist "%CHUNKED_DIR%" mkdir "%CHUNKED_DIR%"
timeout /t 1 /nobreak >nul

REM Copy the results back to the project
xcopy "%FOUND_PATH%" "%CHUNKED_DIR%\" /E /I /Y >nul

if errorlevel 0 (
    echo   [OK] Copied data to: docs\chatlogs\chunked\
) else (
    echo [WARNING] Copy might have failed.
)

echo.
echo ============================================================================
echo  PROCESSING COMPLETE
echo ============================================================================
echo.
echo Raw Source:  docs\chatlogs\raw\%FILENAME%
echo Processed:   docs\chatlogs\chunked\%BASENAME%...
echo.
echo ============================================================================

timeout /t 4 /nobreak >nul
exit /b 0