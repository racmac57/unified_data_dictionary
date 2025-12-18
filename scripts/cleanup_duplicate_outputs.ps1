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
$toDelete = @()
foreach ($g in $groups) {
    if ($g.Count -gt 1) {
        $sorted = $g.Group | Sort-Object -Property LastWriteTime -Descending
        $del = $sorted | Select-Object -Skip 1
        foreach ($x in $del) { $toDelete += $x }
    }
}

if ($toDelete.Count -eq 0) {
    Write-Host "No duplicates found." -ForegroundColor Green
    exit 0
}

Write-Host "Duplicates detected. The following directories will be DELETED (keeping newest per group):" -ForegroundColor Yellow
$toDelete | Select-Object Name, Dir, LastWriteTime, FileCount | Format-Table -AutoSize
Write-Host ""

foreach ($d in $toDelete) {
    Write-Host "Deleting: $($d.Dir)" -ForegroundColor Red
    Remove-Item -LiteralPath $d.Dir -Recurse -Force -ErrorAction Stop
}

Write-Host "Deletion complete." -ForegroundColor Green
Get-ChildItem -Path $root -Directory | Select-Object Name, LastWriteTime, @{Name = 'FileCount'; Expression = { (Get-ChildItem -Path $_.FullName -File -Recurse -ErrorAction SilentlyContinue).Count } } | Format-Table -AutoSize
