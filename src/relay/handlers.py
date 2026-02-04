import json
from nostr.crypto import event_id, verify_signature
from relay.broadcast import broadcast_event
from relay.subscriptions import add_subscription
from db import insert_event, query_events

async def handle_event(evt, websocket):
    if event_id(evt) != evt["id"]:
        await websocket.send(json.dumps(["NOTICE", "invalid event id"]))
        return

    if not verify_signature(evt):
        await websocket.send(json.dumps(["NOTICE", "invalid signature"]))
        return

    insert_event(evt)
    await websocket.send(json.dumps(["OK", evt["id"], True, ""]))
    await broadcast_event(evt)

async def handle_req(sub_id, filters, websocket):
    add_subscription(websocket, sub_id, filters)

    for row in query_events(filters):
        evt = dict(row)
        evt["tags"] = json.loads(evt["tags"])
        await websocket.send(json.dumps(["EVENT", sub_id, evt]))

    await websocket.send(json.dumps(["EOSE", sub_id]))
