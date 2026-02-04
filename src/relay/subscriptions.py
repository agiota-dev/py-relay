subscriptions = {}

def add_subscription(ws, sub_id, filters):
    subscriptions.setdefault(ws, {})[sub_id] = filters

def remove_ws(ws):
    subscriptions.pop(ws, None)
