import sqlite3
import json
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        pubkey TEXT,
        created_at INTEGER,
        kind INTEGER,
        tags TEXT,
        content TEXT,
        sig TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_event(evt):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        evt["id"],
        evt["pubkey"],
        evt["created_at"],
        evt["kind"],
        json.dumps(evt["tags"]),
        evt["content"],
        evt["sig"]
    ))
    conn.commit()
    conn.close()

def query_events(filters):
    conn = get_conn()
    c = conn.cursor()

    query = "SELECT * FROM events WHERE 1=1"
    params = []

    for f in filters:
        if "kinds" in f:
            query += f" AND kind IN ({','.join('?' * len(f['kinds']))})"
            params.extend(f["kinds"])
        if "authors" in f:
            query += f" AND pubkey IN ({','.join('?' * len(f['authors']))})"
            params.extend(f["authors"])
        if "since" in f:
            query += " AND created_at >= ?"
            params.append(f["since"])
        if "until" in f:
            query += " AND created_at <= ?"
            params.append(f["until"])
    
    rows = c.execute(query, params).fetchall()
    conn.close()
    return rows
