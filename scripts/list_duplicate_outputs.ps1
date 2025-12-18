$root = 'C:\Users\carucci_r\OneDrive - City of Hackensack\KB_Shared\04_output'
if (-not (Test-Path $root)) {
    Write-Host "CHUNKER_OUTPUT not found: $root" -ForegroundColor Red
    exit 1
}

$dirs = Get-ChildItem -Path $root -Directory
$summary = @()
foreach ($d in $dirs) {
    $files = Get-ChildItem -Path $d.FullName -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object { $_.FullName.Substring($d.FullName.Length + 1) + '|' + $_.Length }
    $sig = ($files | Sort-Object) -join "`n"
    if ($sig -eq '') {
        $hash = 'EMPTY'
    }
    else {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($sig)
        $md5 = [System.Security.Cryptography.MD5]::Create()
        $hash = ($md5.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
    }
    $summary += [PSCustomObject]@{
        Dir           = $d.FullName
        Name          = $d.Name
        Hash          = $hash
        LastWriteTime = $d.LastWriteTime
        FileCount     = ($files | Measure-Object).Count
    }
}

$groups = $summary | Group-Object -Property Hash
$foundAny = $false
foreach ($g in $groups) {
    if ($g.Count -gt 1) {
        $foundAny = $true
        $sorted = $g.Group | Sort-Object -Property LastWriteTime -Descending
        Write-Host "\nDuplicate group (same content):" -ForegroundColor Yellow
        $sorted | Select-Object Name, Dir, LastWriteTime, FileCount | Format-Table -AutoSize
    }
}

if (-not $foundAny) {
    Write-Host "No duplicates found." -ForegroundColor Green
}
else {
    Write-Host "\nReview the groups above; if you'd like me to delete older entries, tell me to proceed (I will keep newest per group)." -ForegroundColor Cyan
}