$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "Models\MatterEnergyScheduler"
$matterServer = Join-Path $backend ".venv\Scripts\matter-server.exe"
$dataDir = Join-Path $root ".weaver\matter-server"
$logDir = Join-Path $root ".weaver\logs"
$logFile = Join-Path $logDir "matter-server.log"

if (-not (Test-Path $matterServer)) {
  Write-Error "Matter Server was not found. Run .\install.ps1 first."
}

$existing = Get-NetTCPConnection -LocalPort 5580 -ErrorAction SilentlyContinue |
  Where-Object { $_.State -eq "Listen" } |
  Select-Object -First 1

if ($existing) {
  Write-Host "Matter Server already appears to be listening at ws://127.0.0.1:5580/ws."
  exit 0
}

New-Item -ItemType Directory -Force $dataDir | Out-Null
New-Item -ItemType Directory -Force $logDir | Out-Null

Write-Host "Starting local Matter Server at ws://127.0.0.1:5580/ws..."
Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
  "-NoExit",
  "-Command",
  "& '$matterServer' --storage-path '$dataDir' --port 5580 --listen-address 127.0.0.1 --log-file '$logFile'"
)
