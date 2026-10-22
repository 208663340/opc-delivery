#!/usr/bin/env python3
"""Check release evidence metadata; does not verify logs, access systems or approve release."""
import argparse
import json
from pathlib import Path
import re

COMMIT = re.compile(r"(?:[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\Z")
DIGEST = re.compile(r"sha256:[a-fA-F0-9]{64}\Z")
REQUIRED = {
    "build_verified": ("test", "build"),
    "deployed": ("test", "build", "deploy"),
    "business_verified": ("test", "build", "deploy", "smoke"),
}
KINDS = {"test", "build", "deploy", "smoke"}
STATUSES = {"passed", "failed", "blocked", "not_run"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def matches(pattern, value):
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def same(a, b):
    return isinstance(a, str) and isinstance(b, str) and a.lower() == b.lower()


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["Receipt must be a JSON object."]
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be integer 1.")
    claim = data.get("claim")
    if not isinstance(claim, str) or claim not in REQUIRED:
        errors.append("claim must be build_verified, deployed or business_verified.")
        claim = None
    release = data.get("release")
    if not isinstance(release, dict):
        errors.append("release must be an object.")
        release = {}
    if not matches(COMMIT, release.get("commit")):
        errors.append("release.commit must be a full 40- or 64-character Git commit ID.")
    if not matches(DIGEST, release.get("artifact_digest")):
        errors.append("release.artifact_digest must be a SHA-256 digest, not a mutable tag.")
    if not nonempty(release.get("environment")):
        errors.append("release.environment must name the target environment.")
    checks = data.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be an array.")
        checks = []
    grouped = {kind: [] for kind in KINDS}
    ids = set()
    for index, check in enumerate(checks):
        prefix = f"checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        check_id = check.get("id")
        if not nonempty(check_id):
            errors.append(f"{prefix}.id must be a nonempty string.")
        elif check_id in ids:
            errors.append(f"{prefix}.id duplicates an earlier check.")
        else:
            ids.add(check_id)
        kind, status = check.get("kind"), check.get("status")
        if not isinstance(kind, str) or kind not in KINDS:
            errors.append(f"{prefix}.kind must be test, build, deploy or smoke.")
            continue
        grouped[kind].append(check)
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{prefix}.status must be passed, failed, blocked or not_run.")
        if status != "passed":
            continue
        for field in ("evidence", "scope"):
            if not nonempty(check.get(field)):
                errors.append(f"{prefix}.{field} is required for a passed check.")
        if not matches(COMMIT, check.get("commit")) or not same(check.get("commit"), release.get("commit")):
            errors.append(f"{prefix}.commit does not match the release commit.")
        if kind != "test" and (not matches(DIGEST, check.get("artifact_digest")) or not same(check.get("artifact_digest"), release.get("artifact_digest"))):
            errors.append(f"{prefix}.artifact_digest does not match the release artifact.")
        if kind in ("deploy", "smoke") and check.get("environment") != release.get("environment"):
            errors.append(f"{prefix}.environment does not match the target environment.")
    if claim is not None:
        for kind in REQUIRED[claim]:
            if not grouped[kind]:
                errors.append(f"The requested claim requires at least one {kind} check.")
            elif any(check.get("status") != "passed" for check in grouped[kind]):
                errors.append(f"All listed {kind} checks must pass for the requested claim.")
        if claim != "build_verified" and not nonempty(data.get("rollback_plan")):
            errors.append("rollback_plan must describe recovery for the deployment claim.")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON keys are not allowed.")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        if not args.receipt.is_file() or args.receipt.stat().st_size > 1048576:
            raise ValueError("Receipt must be a regular JSON file no larger than 1 MiB.")
        data = json.loads(args.receipt.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        errors = validate(data)
    except (OSError, UnicodeError, ValueError):
        # Do not echo input fragments, which may contain credentials.
        errors = ["Cannot read receipt: require valid UTF-8 JSON, unique keys and size <= 1 MiB."]
    print(json.dumps({
        "consistent": not errors,
        "errors": errors,
        "note": "Metadata consistency only. Original evidence, production state, authorization and business behavior were not verified.",
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
