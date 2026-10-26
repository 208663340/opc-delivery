import json
import sys

results = {
    "version": {"version": "B", "artifact": "fixture-B", "environment": "staging"},
    "health": {"http": 200},
    "business": {"version": "B", "path": "create quote then retrieve", "expected_records": 1, "actual_records": 2, "status": "failed"},
}
result = results[sys.argv[1]]
print(json.dumps(result))
sys.exit(1 if result.get("status") == "failed" else 0)
