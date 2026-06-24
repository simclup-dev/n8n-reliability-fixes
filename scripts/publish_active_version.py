#!/usr/bin/env python3
"""Copy draft workflow JSON into the active workflow_history snapshot.

Sanitized example of the root-cause fix:
- reads `activeVersionId` from `workflow_entity`
- copies draft `nodes` and `connections` into `workflow_history`
- keeps a database backup before writing
"""
import datetime
import shutil
import sqlite3

DB_PATH = "/path/to/n8n/database.sqlite"
WORKFLOW_ID = "workflow_id_here"


def main() -> None:
    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{DB_PATH}.bak-{ts}"
    shutil.copy2(DB_PATH, backup_path)
    print("backup:", backup_path)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    row = cur.execute(
        "SELECT activeVersionId, nodes, connections FROM workflow_entity WHERE id=?",
        (WORKFLOW_ID,),
    ).fetchone()
    if not row:
        raise SystemExit("workflow not found")

    active_version_id, draft_nodes, draft_connections = row
    now_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    cur.execute(
        "UPDATE workflow_history SET nodes=?, connections=?, updatedAt=? WHERE versionId=?",
        (draft_nodes, draft_connections, now_iso, active_version_id),
    )
    cur.execute(
        "UPDATE workflow_entity SET updatedAt=? WHERE id=?",
        (now_iso, WORKFLOW_ID),
    )
    con.commit()
    con.close()
    print("done")


if __name__ == "__main__":
    main()
