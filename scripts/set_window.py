#!/usr/bin/env python3
"""Generate a code-node snippet with configurable reminder windows.

Sanitized example of the pattern used in production:
- convert current time into a target timezone
- compute minutes-of-day
- compare against explicit window boundaries
- read shared state from a mounted file
"""
import sys

morning_start = int(sys.argv[1]) if len(sys.argv) > 1 else 600
morning_end = int(sys.argv[2]) if len(sys.argv) > 2 else 690

logic_js = f"""const now = new Date();
const local = new Date(now.toLocaleString('en-US', {{ timeZone: 'Europe/Kyiv' }}));
const minutesOfDay = local.getHours() * 60 + local.getMinutes();

const MORNING_START = {morning_start};
const MORNING_END = {morning_end};

if (minutesOfDay < MORNING_START || minutesOfDay > MORNING_END) {{
  return [];
}}

return items;
"""

print(logic_js)
