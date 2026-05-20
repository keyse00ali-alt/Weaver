# Weaver Local App

Weaver is intended to run locally for each household. The user's browser, backend, database, schedules, and Matter controller all live on that user's own computer or home server. Nothing needs to report back to the developer.

## Local User Mode

For a normal user on their own computer:

1. Start Podman/Matter services if they are using Matter devices through this local machine.
2. Double-click `Start Weaver.vbs`.
3. Weaver opens at `http://127.0.0.1:3000`.
4. Double-click `Stop Weaver.vbs` when finished.

The launcher starts:

- FastAPI backend on `127.0.0.1:8000`
- Next.js frontend on `127.0.0.1:3000`
- Browser UI pointed at the local frontend

The backend is local-only in this mode.

## LAN Test Mode

For the current test where the virtual appliances run on this laptop but the browser opens from another computer, start the backend/frontend manually with LAN binding:

```powershell
cd C:\Users\keyse\Desktop\Weaver\Models\MatterEnergyScheduler

$env:MATTER_SERVER_WS_URL="ws://127.0.0.1:5580/ws"
$env:FRONTEND_ORIGINS="http://localhost:3000,http://127.0.0.1:3000,http://YOUR_LAPTOP_IP:3000"
$env:WEAVER_LIVE_PRICES="0"

C:\Users\keyse\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000
```

In another window:

```powershell
cd C:\Users\keyse\Desktop\Weaver\frontend

$env:NEXT_PUBLIC_API_URL="http://YOUR_LAPTOP_IP:8000"
npm.cmd run dev -- --hostname 0.0.0.0
```

Then open this from the other computer:

```text
http://YOUR_LAPTOP_IP:3000
```

## Installer Target

The launcher is a near-term developer/test convenience. The production target should be an installer that bundles or provisions:

- The backend runtime
- The frontend build
- A local desktop/browser shell
- Optional Podman/Matter helper setup

The installed app should start its local backend automatically and open the UI without asking users to run terminal commands.
