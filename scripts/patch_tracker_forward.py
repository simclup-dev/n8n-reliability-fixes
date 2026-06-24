#!/usr/bin/env python3
"""Example patch for forwarding foreign Telegram callback buttons to n8n.

Sanitized example:
- shared Telegram bot receives all callbacks
- non-owned buttons can be forwarded to another automation endpoint
- the callback target is configuration, not a hardcoded production URL
"""
PATCH_NOTE = """
Example logic:

if callback and data_str and N8N_CALLBACK_URL:
    async with httpx.AsyncClient(timeout=8) as client:
        await client.post(N8N_CALLBACK_URL, json=body)
"""


if __name__ == "__main__":
    print(PATCH_NOTE.strip())
