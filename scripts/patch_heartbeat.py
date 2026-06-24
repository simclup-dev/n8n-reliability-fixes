#!/usr/bin/env python3
"""Inject heartbeat logic into a code node for independent trigger verification.

This is a sanitized example. The important idea is:
- append one short line to a mounted file on every run
- do it before the business logic returns early
- keep the file path inside the container-visible mount
"""
HEARTBEAT_JS = r"""const fs = require('fs');
const now = new Date();
const heartbeatFile = '/home/node/.n8n/workflow-heartbeat.log';

try {
  fs.appendFileSync(heartbeatFile, now.toISOString() + '\n');
} catch (error) {}

return items;
"""


if __name__ == "__main__":
    print(HEARTBEAT_JS)
