import json
from pathlib import Path
import sys

path = Path("state.json")
state = json.loads(path.read_text())
action = sys.argv[1]
if action not in {"status", "deploy", "smoke", "rollback"}:
    raise SystemExit("unknown action")
with Path("events.jsonl").open("a") as stream:
    stream.write(json.dumps({"action": action, "before": state.copy()}) + "\n")
if action == "deploy":
    state.update(version="B", deploy_count=state["deploy_count"] + 1)
elif action == "smoke":
    state["smoke_version"] = state["version"]
elif action == "rollback":
    state.update(version="A", smoke_version=None)
path.write_text(json.dumps(state) + "\n")
if action == "deploy":
    print("transport timed out; operation outcome unknown")
    raise SystemExit(75)
if action == "smoke":
    passed = state["version"] == "B" and state["healthy"]
    print(json.dumps({"version": state["version"], "create_then_retrieve": passed, "records": 1}))
    raise SystemExit(0 if passed else 1)
print(json.dumps(state))
