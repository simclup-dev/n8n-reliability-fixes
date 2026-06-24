#!/usr/bin/env python3
"""Replace a schedule trigger rule in a SQLite-backed n8n workflow.

Sanitized example:
- backs up the database first
- patches the draft workflow row
- expects exactly one schedule trigger in the workflow
"""
import datetime
import json
import shutil
import sqlite3

DB_PATH = "/path/to/n8n/database.sqlite"
WORKFLOW_ID = "workflow_id_here"
MINUTES_INTERVAL = 15


def main() -> None:
    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{DB_PATH}.bak-{ts}"
    shutil.copy2(DB_PATH, backup_path)
    print("backup:", backup_path)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    row = cur.execute(
        "SELECT nodes FROM workflow_entity WHERE id=?",
        (WORKFLOW_ID,),
    ).fetchone()
    if not row:
        raise SystemExit("workflow not found")

    nodes = json.loads(row[0])
    patched = 0
    for node in nodes:
        if node.get("type") == "n8n-nodes-base.scheduleTrigger":
            node["parameters"] = {
                "rule": {"interval": [{"field": "minutes", "minutesInterval": MINUTES_INTERVAL}]}
            }
            patched += 1

    if patched != 1:
        raise SystemExit(f"expected exactly 1 trigger, found {patched}")

    now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    cur.execute(
        "UPDATE workflow_entity SET nodes=?, updatedAt=? WHERE id=?",
        (json.dumps(nodes, ensure_ascii=False), now_iso, WORKFLOW_ID),
    )
    con.commit()
    con.close()
    print("done")


if __name__ == "__main__":
    main()
