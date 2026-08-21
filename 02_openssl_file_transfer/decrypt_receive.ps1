param(
    [Parameter(Mandatory=$true)]
    [string]$FileName
)

if (-not $env:OPENSSL_PASS) {
    Write-Error "Set OPENSSL_PASS first."
    exit 1
}

$Base = $PSScriptRoot
$InputFile = Join-Path $Base "receiver\inbox\$FileName.enc"
$OutputFile = Join-Path $Base "receiver\decrypted\$FileName"

openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 `
    -in $InputFile -out $OutputFile -pass env:OPENSSL_PASS
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Decrypted: $OutputFile"
