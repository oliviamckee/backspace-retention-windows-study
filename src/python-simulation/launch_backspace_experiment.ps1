$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$outputDirectory = Join-Path $repoRoot 'new-output'
Set-Location -LiteralPath $repoRoot
$Host.UI.RawUI.WindowTitle = 'Backspace Gate Delete-Key Experiment'

Write-Host ''
Write-Host 'This trial intentionally records erased text.' -ForegroundColor Yellow
Write-Host 'Use a made-up, non-sensitive English phrase with ordinary keyboard characters.' -ForegroundColor Yellow
Write-Host ''

python (Join-Path $PSScriptRoot 'run_backspace_experiment.py') --output-dir $outputDirectory

Write-Host ''
Write-Host 'Trial finished. Leave this window open and return to the Codex chat.' -ForegroundColor Cyan
