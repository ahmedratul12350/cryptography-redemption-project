param(
    [Parameter(Mandatory=$true)]
    [string]$FileName
)

if (-not $env:OPENSSL_PASS) {
    Write-Error "Set OPENSSL_PASS first: `$env:OPENSSL_PASS='CourseDemoPass123!'"
    exit 1
}

$Base = $PSScriptRoot
$InputFile = Join-Path $Base "sender\plaintext\$FileName"
$Encrypted = Join-Path $Base "sender\encrypted\$FileName.enc"
$Inbox = Join-Path $Base "receiver\inbox\$FileName.enc"

openssl enc -aes-256-cbc -salt -pbkdf2 -iter 200000 -md sha256 `
    -in $InputFile -out $Encrypted -pass env:OPENSSL_PASS
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Copy-Item $Encrypted $Inbox -Force
Write-Host "Encrypted: $Encrypted"
Write-Host "Transferred to receiver inbox: $Inbox"
