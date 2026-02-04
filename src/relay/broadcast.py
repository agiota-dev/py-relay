import json
from nostr.filters import match_filter
from relay.subscriptions import subscriptions


async def broadcast_event(evt):
    for ws, subs in subscriptions.items():
        for sub_id, filters in subs.items():
            for flt in filters:
                if match_filter(evt, flt):
                    await ws.send(json.dumps(["EVENT", sub_id, evt]))
                    break
