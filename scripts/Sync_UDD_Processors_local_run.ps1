<#
.SYNOPSIS
    Synchronizes UDD Chatlog Processors (Bat + Button) from Project to Central Hub.
.DESCRIPTION
    Copies the master versions from unified_data_dictionary to 00_dev.
#>

# ==============================================================================
# CONFIGURATION
# ==============================================================================
$SourceDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\scripts"
$DestDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\00_dev\scripts\DOpus\buttons\chatlog_processors"

$FilesToSync = @(
    "Process_UDD_Chatlog.bat",
    "DOpus_Process_UDD_Chatlog_Button.dcf"
)

# ==============================================================================
# EXECUTION
# ==============================================================================
Clear-Host
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   UDD PROCESSOR SYNC (Project -> Central Hub)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $SourceDir)) {
    Write-Error "Source directory not found: $SourceDir"
    exit
}

if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
}

foreach ($File in $FilesToSync) {
    $SourceFile = Join-Path $SourceDir $File
    $DestFile = Join-Path $DestDir $File

    if (Test-Path $SourceFile) {
        Write-Host "Syncing: $File" -NoNewline
        try {
            Copy-Item -Path $SourceFile -Destination $DestFile -Force
            Write-Host " [OK]" -ForegroundColor Green
        }
        catch {
            Write-Host " [FAILED] $_" -ForegroundColor Red
        }
    }
    else {
        Write-Host "Missing Source: $File" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "SYNC COMPLETE" -ForegroundColor Cyan
Write-Host "Central Location: $DestDir" -ForegroundColor Gray
pause
