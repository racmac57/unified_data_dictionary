# Configuration
$TargetDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output"

# Check path
if (-not (Test-Path $TargetDir)) {
    Write-Error "Path not found: $TargetDir"
    exit
}

Write-Host "Scanning for duplicates in: $TargetDir" -ForegroundColor Cyan

# Get all folders
$folders = Get-ChildItem -Path $TargetDir -Directory

# Group folders by the "Real Filename" (ignoring the YYYY_MM_DD timestamp prefix)
$groups = $folders | Group-Object -Property {
    # Regex to capture text after the timestamp prefix
    if ($_.Name -match '^\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}_(.*)$') {
        $Matches[1]
    }
    else {
        $_.Name # Fallback for folders without timestamps
    }
}

$deletedCount = 0

foreach ($group in $groups) {
    # If we have more than 1 folder for the same file...
    if ($group.Count -gt 1) {
        Write-Host "`nFound duplicate group: '$($group.Name)'" -ForegroundColor Yellow
        
        # Sort by Name Descending (Newest timestamp is always alphabetically last)
        # 2025_12_17_22_24_16 (Newest - Keep)
        # 2025_12_17_22_24_15 (Older - Delete)
        $sorted = $group.Group | Sort-Object Name -Descending
        
        $keep = $sorted[0]
        $removeList = $sorted | Select-Object -Skip 1
        
        Write-Host "  [KEEP]   $($keep.Name)" -ForegroundColor Green
        
        foreach ($item in $removeList) {
            Write-Host "  [DELETE] $($item.Name)" -ForegroundColor Red
            Remove-Item -LiteralPath $item.FullName -Recurse -Force
            $deletedCount++
        }
    }
}

Write-Host "`n--------------------------------------------------"
Write-Host "Cleanup Complete. Removed $deletedCount folders." -ForegroundColor Cyan
Write-Host "--------------------------------------------------"