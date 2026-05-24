$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "Models\MatterEnergyScheduler"
$frontend = Join-Path $root "frontend"
$python = Join-Path $backend ".venv\Scripts\python.exe"

function Test-VenvPython {
  param([string]$PythonPath)

  if (-not (Test-Path $PythonPath)) {
    return $false
  }

  try {
    & $PythonPath -c "import sys; raise SystemExit(0 if (3, 12) <= sys.version_info[:2] < (3, 14) else 1)" 2>$null | Out-Null
    return $LASTEXITCODE -eq 0
  } catch {
    return $false
  }
}

if (-not (Test-VenvPython $python)) {
  Write-Error "Backend Python environment is missing, broken, or using an unsupported Python version. Run .\install.ps1 first. Weaver currently requires Python 3.12 or 3.13 for Matter Server support."
}

if ($env:WEAVER_START_LOCAL_MATTER_SERVER -eq "1") {
  & (Join-Path $root "start-matter-server.ps1")
} else {
  Write-Host "Skipping local Matter Server startup. Native Windows Matter Server support is not available with the current CHIP dependency."
  Write-Host "Set MATTER_SERVER_WS_URL if you have Matter Server running on a Raspberry Pi."
}

if (-not $env:MATTER_SERVER_WS_URL) {
  $env:MATTER_SERVER_WS_URL = "ws://127.0.0.1:5580/ws"
}
$env:FRONTEND_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"

function Get-DotEnvValue {
  param(
    [string]$Path,
    [string]$Name
  )

  if (-not (Test-Path $Path)) {
    return $null
  }

  $line = Get-Content $Path | Where-Object { $_ -match "^\s*$Name\s*=" } | Select-Object -First 1
  if (-not $line) {
    return $null
  }

  return ($line -replace "^\s*$Name\s*=\s*", "").Trim().Trim('"').Trim("'")
}

$backendEnvFile = Join-Path $backend ".env"
$hasEntsoeToken = $env:ENTSOE_API_KEY -or $env:ENTSOE_TOKEN -or (Get-DotEnvValue $backendEnvFile "ENTSOE_API_KEY") -or (Get-DotEnvValue $backendEnvFile "ENTSOE_TOKEN")
if ($hasEntsoeToken) {
  Write-Host "ENTSO-E token found. Weaver will attempt live day-ahead prices."
} else {
  Write-Host "No ENTSO-E token found. Weaver will use fallback price estimates."
}

$backendCommand = "Set-Location '$backend'; `$env:MATTER_SERVER_WS_URL='$env:MATTER_SERVER_WS_URL'; `$env:FRONTEND_ORIGINS='$env:FRONTEND_ORIGINS'"
if ($env:WEAVER_LIVE_PRICES) {
  $backendCommand = "$backendCommand; `$env:WEAVER_LIVE_PRICES='$env:WEAVER_LIVE_PRICES'"
}
$backendCommand = "$backendCommand; & '$python' -m uvicorn main:app --host 127.0.0.1 --port 8000"

Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
  "-NoExit",
  "-Command",
  $backendCommand
)

Start-Sleep -Seconds 2

Start-Process powershell.exe -WindowStyle Normal -ArgumentList @(
  "-NoExit",
  "-Command",
  "Set-Location '$frontend'; `$env:NEXT_PUBLIC_API_URL='http://127.0.0.1:8000'; npm.cmd run dev -- --hostname 127.0.0.1"
)

Start-Sleep -Seconds 4
Start-Process "http://127.0.0.1:3000"
