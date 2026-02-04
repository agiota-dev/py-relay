import asyncio
import json
import time
import hashlib
import websockets
from ecdsa import SigningKey, SECP256k1
import datetime


DATETIME = datetime.datetime.now()
RELAY_URL = "ws://localhost:8863"
PRIVATE_KEY_HEX = "1" * 64

def serialize_event(evt):
    return json.dumps(
        [
            0,
            evt["pubkey"],
            evt["created_at"],
            evt["kind"],
            evt["tags"],
            evt["content"],
        ],
        separators=(",", ":"),
        ensure_ascii=False,
    )

def get_event_id(evt):
    return hashlib.sha256(
        serialize_event(evt).encode()
    ).hexdigest()

def sign_event(evt, sk):
    evt_id = get_event_id(evt)
    evt["id"] = evt_id
    evt["sig"] = sk.sign(
        serialize_event(evt).encode()
    ).hex()
    return evt

# ------------------ MAIN LOGIC ------------------

async def post_notes():
    sk = SigningKey.from_string(
        bytes.fromhex(PRIVATE_KEY_HEX),
        curve=SECP256k1
    )

    pubkey = sk.verifying_key.to_string().hex()

    notes = [
        f"{DATETIME} - Hello, World!",
        f"{DATETIME} - Enviando mais uma mensagem.",
        f"{DATETIME} - Diga algo mais.",
    ]

    async with websockets.connect(RELAY_URL) as ws:
        for content in notes:
            evt = {
                "pubkey": pubkey,
                "created_at": int(time.time()),
                "kind": 1,       # NIP-01: note
                "tags": [],
                "content": content,
            }

            evt = sign_event(evt, sk)

            msg = ["EVENT", evt]
            await ws.send(json.dumps(msg))

            response = await ws.recv()
            print("Relay respondeu:", response)

            await asyncio.sleep(0.5)

asyncio.run(post_notes())
