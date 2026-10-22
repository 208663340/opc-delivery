#!/usr/bin/env python3
"""Behavior tests; all writes are isolated in temporary directories."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import check_release_receipt as receipt
import inspect_project as project

SCRIPTS = Path(__file__).resolve().parent
COMMIT = "a" * 40
DIGEST = "sha256:" + "b" * 64


def example(claim="business_verified"):
    checks = []
    for kind in ("test", "build", "deploy", "smoke"):
        item = {"id": kind, "kind": kind, "status": "passed", "commit": COMMIT,
                "scope": "Synthetic fixture only", "evidence": "fixtures/local-run.log"}
        if kind != "test":
            item["artifact_digest"] = DIGEST
        if kind in ("deploy", "smoke"):
            item["environment"] = "staging"
        checks.append(item)
    return {"schema_version": 1, "claim": claim,
            "release": {"commit": COMMIT, "artifact_digest": DIGEST, "environment": "staging"},
            "rollback_plan": "Restore the previous fixture artifact; no schema changes.", "checks": checks}


class ReceiptTests(unittest.TestCase):
    def test_matching_evidence_accepts_all_claim_levels(self):
        for claim in receipt.REQUIRED:
            with self.subTest(claim=claim):
                self.assertEqual(receipt.validate(example(claim)), [])

    def test_stale_test_commit_rejected(self):
        data = example()
        data["checks"][0]["commit"] = "c" * 40
        self.assertTrue(any("commit" in err for err in receipt.validate(data)))

    def test_wrong_artifact_rejected(self):
        data = example()
        data["checks"][2]["artifact_digest"] = "sha256:" + "d" * 64
        self.assertTrue(any("artifact_digest" in err for err in receipt.validate(data)))

    def test_staging_smoke_cannot_prove_production(self):
        data = example()
        data["release"]["environment"] = "production"
        self.assertTrue(any("environment" in err for err in receipt.validate(data)))

    def test_skipped_or_failed_tests_never_pass(self):
        for status in ("not_run", "blocked", "failed"):
            data = example()
            data["checks"][0]["status"] = status
            self.assertTrue(receipt.validate(data))

    def test_health_and_deploy_do_not_replace_smoke(self):
        data = example()
        data["checks"] = data["checks"][:-1]
        self.assertTrue(any("smoke" in err for err in receipt.validate(data)))

    def test_failed_smoke_allows_only_lower_claim(self):
        data = example("deployed")
        data["checks"][-1]["status"] = "failed"
        self.assertEqual(receipt.validate(data), [])
        data["claim"] = "business_verified"
        self.assertTrue(receipt.validate(data))

    def test_missing_evidence_or_scope_rejected(self):
        for field in ("evidence", "scope"):
            data = example()
            data["checks"][0][field] = " "
            self.assertTrue(receipt.validate(data))

    def test_mutable_tag_and_short_sha_rejected(self):
        data = example()
        data["release"].update(commit="a" * 7, artifact_digest="latest")
        self.assertGreaterEqual(len(receipt.validate(data)), 2)

    def test_duplicate_check_and_missing_rollback_rejected(self):
        data = example()
        data["checks"].append(copy.deepcopy(data["checks"][0]))
        data["rollback_plan"] = None
        self.assertGreaterEqual(len(receipt.validate(data)), 2)

    def test_malformed_types_do_not_crash(self):
        for key, value in (("claim", []), ("release", []), ("checks", {}), ("schema_version", True)):
            data = example()
            data[key] = value
            self.assertTrue(receipt.validate(data))
        for key in ("id", "kind", "status", "commit", "artifact_digest"):
            data = example()
            data["checks"][1][key] = []
            self.assertTrue(receipt.validate(data))

    def test_template_cannot_be_mistaken_for_evidence(self):
        data = json.loads((SCRIPTS.parent / "assets/release-receipt.example.json").read_text())
        self.assertTrue(receipt.validate(data))

    def test_cli_duplicate_keys_are_rejected_without_echo(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text('{"claim":"SYNTHETIC_SECRET_MARKER","claim":"deployed"}')
            result = subprocess.run([sys.executable, str(SCRIPTS / "check_release_receipt.py"), str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("SYNTHETIC_SECRET_MARKER", result.stdout + result.stderr)

    def test_evidence_is_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "not-created"
            data = example()
            data["checks"][0]["evidence"] = f"$(touch {marker})"
            self.assertEqual(receipt.validate(data), [])
            self.assertFalse(marker.exists())


class InventoryTests(unittest.TestCase):
    def test_does_not_read_secrets_or_execute_project_scripts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text("SYNTHETIC_SECRET_MARKER")
            (root / ".secrets").mkdir()
            (root / ".secrets/package.json").write_text('{"scripts":{"test":"hidden"}}')
            marker = root / "not-created"
            (root / "package.json").write_text(json.dumps({"scripts": {"check": f"touch {marker}", "postinstall": "SYNTHETIC_SECRET_MARKER"}}))
            result = project.inspect(root)
            self.assertEqual(result["candidate_commands"][0]["argv"], ["npm", "run", "check"])
            self.assertNotIn("SYNTHETIC_SECRET_MARKER", json.dumps(result))
            self.assertNotIn(".env", result["entrypoints"])
            self.assertFalse(marker.exists())

    def test_symlink_manifests_are_not_followed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside.json"
            outside.write_text('{"scripts":{"test":"SYNTHETIC_SECRET_MARKER"}}')
            work = root / "work"
            work.mkdir()
            (work / "package.json").symlink_to(outside)
            self.assertEqual(project.inspect(work)["candidate_commands"], [])

    def test_parent_workspace_lock_is_used(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pnpm-lock.yaml").write_text("")
            package = root / "apps/web"
            package.mkdir(parents=True)
            (package / "package.json").write_text('{"scripts":{"test":"node --test"}}')
            self.assertEqual(project.inspect(root)["candidate_commands"][0]["argv"], ["pnpm", "run", "test"])

    def test_conflicting_locks_are_not_guessed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("package-lock.json", "yarn.lock"):
                (root / name).write_text("")
            (root / "package.json").write_text('{"scripts":{"check":"x"}}')
            result = project.inspect(root)
            self.assertEqual(result["candidate_commands"], [])
            self.assertTrue(result["warnings"])

    def test_bounded_inventory_marks_incomplete_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a/b").mkdir(parents=True)
            (root / "a/b/pyproject.toml").write_text("")
            result = project.inspect(root, max_depth=0)
            self.assertTrue(result["inventory_limits"]["truncated"])
            result = project.inspect(root, max_entries=1)
            self.assertTrue(result["inventory_limits"]["truncated"])

    def test_malformed_manifest_does_not_echo_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package.json").write_text('{SYNTHETIC_SECRET_MARKER')
            result = project.inspect(root)
            self.assertTrue(result["warnings"])
            self.assertNotIn("SYNTHETIC_SECRET_MARKER", json.dumps(result))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_git_state_and_fsmonitor_hook_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            marker = root / "not-created"
            hook = root / "monitor.sh"
            hook.write_text(f"#!/bin/sh\ntouch '{marker}'\n")
            hook.chmod(0o700)
            subprocess.run(["git", "-C", str(root), "config", "core.fsmonitor", str(hook)], check=True)
            result = project.inspect(root)
            self.assertTrue(result["git"]["available"])
            self.assertIsNone(result["git"]["dirty"])
            self.assertFalse(marker.exists())

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_project_clean_filter_is_not_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            marker = root / "filter-called"
            script = root / "filter.sh"
            script.write_text(f"#!/bin/sh\ntouch '{marker}'\ncat\n")
            script.chmod(0o700)
            subprocess.run(["git", "-C", str(root), "config", "filter.fixture.clean", str(script)], check=True)
            (root / ".gitattributes").write_text("sample.txt filter=fixture\n")
            sample = root / "sample.txt"
            sample.write_text("aaaa\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "baseline"], check=True)
            marker.unlink(missing_ok=True)
            sample.write_text("bbbb\n")
            result = project.inspect(root)
            self.assertIsNone(result["git"]["dirty"])
            self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
