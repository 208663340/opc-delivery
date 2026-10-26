"""Existing local input check only; no model call or outcome grading."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=Path, required=True)
parser.add_argument("--dry-run", action="store_true", required=True)
args = parser.parse_args()
ids = set()
for line in args.dataset.read_text().splitlines():
    row = json.loads(line)
    assert set(row) == {"case_id", "input", "fixture_ref"}
    assert row["case_id"] not in ids
    ids.add(row["case_id"])
    json.loads((Path("evals") / row["fixture_ref"]).read_text())
print(json.dumps({"cases_validated": len(ids), "agent_executed": False, "graded": False}))
