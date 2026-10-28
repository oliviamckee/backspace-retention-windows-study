$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$executable = Join-Path $PSScriptRoot 'bin\Release\net9.0\ConPTYBackspace.exe'
$outputDirectory = Join-Path $repoRoot 'new-output'
Set-Location -LiteralPath $repoRoot
$Host.UI.RawUI.WindowTitle = 'Native Windows ConPTY Experiment'

Write-Host ''
Write-Host 'This trial records the real Windows ConPTY output stream.' -ForegroundColor Yellow
Write-Host 'Use a made-up, non-sensitive English phrase.' -ForegroundColor Yellow
Write-Host ''

& $executable --output-dir $outputDirectory

Write-Host ''
Write-Host 'Trial finished. Leave this window open and return to the Codex chat.' -ForegroundColor Cyan
