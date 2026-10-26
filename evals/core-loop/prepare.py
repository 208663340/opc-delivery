"""Create fresh, offline executor inputs; never copy the evaluator rubric."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_root", type=Path)
    parser.add_argument("destination", type=Path, help="New directory; must not exist")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    cases = json.loads((here / "cases.json").read_text())
    args.destination.mkdir(parents=True, exist_ok=False)
    snapshot = args.destination / "skill"
    snapshot.mkdir()
    for name in ("SKILL.md", "references", "skills", "assets", "scripts"):
        src, dst = args.skill_root / name, snapshot / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    for case in cases:
        case_root = args.destination / case["id"]
        project = case_root / "project"
        shutil.copytree(here / "fixtures" / case["id"], project)
        (case_root / "task.json").write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n")
        if case["id"] == "C02":
            subprocess.run(["git", "init", "-q", str(project)], check=True)
            subprocess.run(["git", "add", "."], cwd=project, check=True)
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture"], cwd=project, check=True)
            with (project / "notes.txt").open("a") as stream:
                stream.write("用户未提交的想法：保留这行，周五讨论。\n")
    hashes = {
        str(path.relative_to(args.destination)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(args.destination.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }
    (args.destination / "initial-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print(args.destination.resolve())


if __name__ == "__main__":
    main()
