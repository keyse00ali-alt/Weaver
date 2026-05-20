import asyncio
import json
import os
import uuid
from typing import Any, Optional

import websockets


class MatterServerError(RuntimeError):
    pass


class MatterServerWsClient:
    """
    Minimal WebSocket client for python-matter-server.

    We intentionally keep this thin (MVP): open a WS connection per request and
    wait for a matching result message.
    """

    def __init__(self, ws_url: Optional[str] = None):
        self.ws_url = ws_url or os.getenv("MATTER_SERVER_WS_URL", "ws://127.0.0.1:5580/ws")

    async def call(self, command: str, args: Optional[dict[str, Any]] = None, timeout_s: float = 60.0) -> Any:
        message_id = str(uuid.uuid4())
        payload: dict[str, Any] = {"message_id": message_id, "command": command}
        if args is not None:
            payload["args"] = args

        try:
            async with websockets.connect(self.ws_url, open_timeout=10) as ws:
                await ws.send(json.dumps(payload))

                end_time = asyncio.get_running_loop().time() + timeout_s
                while True:
                    remaining = end_time - asyncio.get_running_loop().time()
                    if remaining <= 0:
                        raise MatterServerError(f"Timed out waiting for response to '{command}'")

                    raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
                    msg = json.loads(raw)

                    if msg.get("message_id") != message_id:
                        # Events / other messages; ignore for this MVP.
                        continue

                    if "error" in msg and msg["error"]:
                        raise MatterServerError(str(msg["error"]))

                    # Different server versions use slightly different keys.
                    if "result" in msg:
                        return msg["result"]
                    if "data" in msg:
                        return msg["data"]
                    if "payload" in msg:
                        return msg["payload"]
                    if msg.get("success") is True and "value" in msg:
                        return msg["value"]

                    return msg
        except MatterServerError:
            raise
        except Exception as exc:
            raise MatterServerError(f"Matter server call failed ({command}): {exc}") from exc

