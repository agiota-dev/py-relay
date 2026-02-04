import asyncio
import json
import websockets
from config import HOST, PORT
from db import init_db
from relay.handlers import handle_event, handle_req
from relay.subscriptions import remove_ws

async def handler(websocket):
    try:
        async for message in websocket:
            msg = json.loads(message)

            if msg[0] == "EVENT":
                await handle_event(msg[1], websocket)

            elif msg[0] == "REQ":
                await handle_req(msg[1], msg[2:], websocket)

            elif msg[0] == "CLOSE":
                pass
    finally:
        remove_ws(websocket)

async def main():
    init_db()
    print(f"Relay rodando em ws://{HOST}:{PORT}")
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

asyncio.run(main())
