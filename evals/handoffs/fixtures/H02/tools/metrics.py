"""Synthetic read-only CLI: no network, credentials or persistent mutations."""
import json
import sys

args = sys.argv[1:]
if args == ["--version"]:
    print("metrics 3.2.0")
elif args in (["--help"], []):
    print("metrics 3.2.0\nUsage: --version | status --env prod | events --env prod\nAll commands are read-only; no install/login/write commands.")
elif args == ["status", "--env", "prod"]:
    print(json.dumps({"revision": "B", "environment": "prod", "coverage_percent": 10, "age_days": 2, "login": "valid", "business_smoke": "not_recorded", "event_schema": "v3"}))
elif args == ["events", "--env", "prod"]:
    print(json.dumps({"error": "missing_scope", "required": "events:read:prod", "environment": "prod", "owner": "data-admin"}))
    sys.exit(3)
else:
    print(json.dumps({"error": "unsupported_command", "help": "--help"}))
    sys.exit(2)
