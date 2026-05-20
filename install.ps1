$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $root "Models\MatterEnergyScheduler"
$frontend = Join-Path $root "frontend"

Write-Host "Installing Weaver backend dependencies..."
Set-Location $backend
if (-not (Test-Path ".venv\Scripts\python.exe")) {
  Write-Host "Creating backend Python environment..."
  python -m venv .venv
} else {
  Write-Host "Backend Python environment already exists. Reusing it."
}
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt

Write-Host "Installing Weaver frontend dependencies..."
Set-Location $frontend
if (Test-Path "node_modules") {
  Write-Host "Frontend dependencies already exist. Running npm install to verify them."
} else {
  Write-Host "Installing frontend dependencies for the first time..."
}
npm.cmd install

Write-Host "Matter Server is installed with the backend Python dependencies."
Write-Host "Weaver install complete."
