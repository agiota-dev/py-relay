import json
import hashlib
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError


def serialize_event(evt):
    return json.dumps([
        0,
        evt["pubkey"],
        evt["created_at"],
        evt["kind"],
        evt["tags"],
        evt["content"]
    ], separators=(",", ":"), ensure_ascii=False)

def event_id(evt):
    return hashlib.sha256(serialize_event(evt).encode()).hexdigest()

def verify_signature(evt):
    try:
        vk = VerifyingKey.from_string(
            bytes.fromhex(evt["pubkey"]),
            curve=SECP256k1
        )
        vk.verify(
            bytes.fromhex(evt["sig"]),
            serialize_event(evt).encode()
        )
        return True
    except BadSignatureError:
        return False
