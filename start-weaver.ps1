$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "Models\MatterEnergyScheduler"
$frontend = Join-Path $root "frontend"
$python = Join-Path $backend ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
  Write-Error "Backend virtual environment not found. Run .\install.ps1 first."
}

& (Join-Path $root "start-matter-server.ps1")

$env:MATTER_SERVER_WS_URL = "ws://127.0.0.1:5580/ws"
$env:FRONTEND_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"
$env:WEAVER_LIVE_PRICES = "0"

Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$backend'; `$env:MATTER_SERVER_WS_URL='$env:MATTER_SERVER_WS_URL'; `$env:FRONTEND_ORIGINS='$env:FRONTEND_ORIGINS'; `$env:WEAVER_LIVE_PRICES='$env:WEAVER_LIVE_PRICES'; & '$python' -m uvicorn main:app --host 127.0.0.1 --port 8000"
)

Start-Sleep -Seconds 2

Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$frontend'; `$env:NEXT_PUBLIC_API_URL='http://127.0.0.1:8000'; npm.cmd run dev -- --hostname 127.0.0.1"
)

Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:3000"
