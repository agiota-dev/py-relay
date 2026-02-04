def match_filter(evt, flt):
    if "kinds" in flt and evt["kind"] not in flt["kinds"]:
        return False
    if "authors" in flt and evt["pubkey"] not in flt["authors"]:
        return False
    if "since" in flt and evt["created_at"] < flt["since"]:
        return False
    if "until" in flt and evt["created_at"] > flt["until"]:
        return False
    return True
