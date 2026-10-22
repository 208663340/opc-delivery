#!/usr/bin/env python3
"""Bounded, read-only project inventory. No network or project script execution."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess

SKIP_DIRS = {
    ".git", ".secrets", ".ssh", ".aws", ".venv", "venv", "node_modules",
    "target", "dist", "build", "coverage", "__pycache__", "artifacts",
    "e2e-artifacts", "vendor", ".next", ".cache", ".mypy_cache", ".pytest_cache",
}
MANIFESTS = {
    "package.json", "pyproject.toml", "requirements.txt", "pom.xml", "Makefile",
    "go.mod", "Cargo.toml", "Gemfile", "build.gradle", "build.gradle.kts",
    "mvnw", "gradlew", "Dockerfile", ".cnb.yml", ".gitlab-ci.yml",
}
DOCS = {"AGENTS.md", "README.md", "DOD.md", "ARCHITECTURE-CONTRACT.md", "local-dev.md"}
LOCKS = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb", "uv.lock", "poetry.lock"}
SAFE_SCRIPT_NAMES = ("check", "test", "build", "lint", "typecheck", "format:check")


def git_read(root, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    try:
        result = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", *args], cwd=root, env=env,
            capture_output=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None


def inventory(root, max_depth, max_entries):
    found, warnings = [], []
    pending = [(root, 0)]
    visited = 0
    truncated = False
    while pending:
        directory, depth = pending.pop()
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    visited += 1
                    if visited > max_entries:
                        return sorted(found), warnings, True
                    if entry.is_symlink():
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name in SKIP_DIRS or (entry.name.startswith(".") and entry.name != ".github"):
                            continue
                        if depth < max_depth:
                            pending.append((Path(entry.path), depth + 1))
                        else:
                            truncated = True
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    rel = Path(entry.path).relative_to(root).as_posix()
                    name = entry.name
                    is_workflow = ".github/workflows/" in rel and name.endswith((".yml", ".yaml"))
                    is_compose = name.startswith(("docker-compose", "compose.")) and name.endswith((".yml", ".yaml"))
                    if name in MANIFESTS | DOCS | LOCKS or is_workflow or is_compose:
                        found.append(rel)
        except OSError:
            warnings.append("An inventory directory was unreadable; coverage is incomplete.")
    return sorted(found), warnings, truncated


def read_small(path):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 262144:
        return None
    return path.read_text(encoding="utf-8")


def inspect(root, max_depth=3, max_entries=12000):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Project directory does not exist or is not a directory.")
    files, warnings, truncated = inventory(root, max_depth, max_entries)
    candidates = []
    known = set(files)
    for rel in files:
        path = root / rel
        cwd = path.parent.relative_to(root).as_posix()
        if path.name == "package.json":
            try:
                raw = read_small(path)
                data = json.loads(raw) if raw is not None else None
                if not isinstance(data, dict) or not isinstance(data.get("scripts", {}), dict):
                    raise ValueError("Invalid manifest structure")
            except (OSError, UnicodeError, ValueError):
                warnings.append(f"Cannot inspect scripts in {rel}; inspect the manifest manually.")
                continue
            manager = "npm"
            # Prefer the nearest lockfile. Conflicting same-directory locks stay explicit.
            cursor = path.parent
            while True:
                lock_managers = []
                for lock, executable in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lock", "bun"), ("bun.lockb", "bun"), ("package-lock.json", "npm")):
                    if (cursor / lock).relative_to(root).as_posix() in known:
                        lock_managers.append(executable)
                if lock_managers:
                    if len(set(lock_managers)) > 1:
                        warnings.append(f"Conflicting package-manager lockfiles for {rel}; no command inferred.")
                        manager = None
                    else:
                        manager = lock_managers[0]
                    break
                if cursor == root:
                    break
                cursor = cursor.parent
            if manager:
                for name in SAFE_SCRIPT_NAMES:
                    if isinstance(data.get("scripts", {}).get(name), str):
                        candidates.append({"cwd": cwd, "argv": [manager, "run", name], "source": rel})
        elif path.name == "mvnw":
            candidates.append({"cwd": cwd, "argv": ["./mvnw", "-B", "-ntp", "verify"], "source": rel})
    top = git_read(root, "rev-parse", "--show-toplevel")
    git = {"available": top is not None}
    if top is not None:
        git.update({
            "root": top.strip(),
            "head": (git_read(root, "rev-parse", "--verify", "HEAD") or "").strip() or None,
            "branch": (git_read(root, "symbolic-ref", "--quiet", "--short", "HEAD") or "").strip() or None,
            "dirty": None,
            "dirty_note": "Not inspected: status/working-tree comparisons can invoke repository clean filters. Verify status separately after trusting the repository configuration.",
        })
    return {
        "project_root": str(root), "git": git, "entrypoints": files,
        "candidate_commands": candidates,
        "available_executables": {name: shutil.which(name) is not None for name in ("git", "python3", "node", "npm", "pnpm", "yarn", "bun", "java", "docker")},
        "inventory_limits": {"max_depth": max_depth, "max_entries": max_entries, "truncated": truncated},
        "warnings": warnings,
        "note": "Hints only. Commands were not run; credentials, remote access and production state were not inspected.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--max-depth", type=int, choices=range(0, 9), default=3)
    parser.add_argument("--max-entries", type=int, default=12000)
    args = parser.parse_args()
    if args.max_entries < 1 or args.max_entries > 100000:
        parser.error("--max-entries must be between 1 and 100000")
    try:
        result = inspect(args.project, args.max_depth, args.max_entries)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
