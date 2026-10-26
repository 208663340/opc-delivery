"""Prepare one offline arm without exposing rubric or previous outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("skill_root", type=Path)
parser.add_argument("destination", type=Path)
args = parser.parse_args()
here = Path(__file__).resolve().parent
args.destination.mkdir(parents=True, exist_ok=False)
snapshot = args.destination / "skill"
snapshot.mkdir()
for name in ["SKILL.md", "references", "skills", "assets", "scripts"]:
    src, dst = args.skill_root / name, snapshot / name
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
for case in json.loads((here / "cases.json").read_text()):
    root = args.destination / case["id"]
    shutil.copytree(here / "fixtures" / case["id"], root / "project")
    (root / "task.json").write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n")
hashes = {str(p.relative_to(args.destination)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(args.destination.rglob("*")) if p.is_file()}
(args.destination / "initial-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
print(args.destination.resolve())
