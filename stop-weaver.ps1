$ErrorActionPreference = "Continue"

foreach ($port in @(3000, 8000, 5580)) {
  Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique |
    ForEach-Object {
      Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Weaver stopped."
