@echo off
REM ============================================================================
REM quick_process_chatlog.bat - Quick Chatlog Processing for DOpus
REM ============================================================================
REM Right-click a .md file in DOpus and run this script
REM Or drag/drop a file onto this script
REM ============================================================================

set "PROJECT_ROOT=C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
set "RAW_DIR=%PROJECT_ROOT%\docs\chatlogs\raw"

if "%~1"=="" (
    echo Drag and drop a .md file onto this script
    pause
    exit /b 1
)

REM Move file to raw directory
move /Y "%~1" "%RAW_DIR%\"

REM Open the raw directory
explorer "%RAW_DIR%"

REM Open chunker in new window
start "Chunker" cmd /k "cd /d C:\_chunker\opus && Chunker_Move.bat "%RAW_DIR%\%~nx1" && Start_Chunker_Watcher.bat"

echo.
echo File moved to: %RAW_DIR%\%~nx1
echo Chunker started in new window
echo.
pause

