from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "scripts" / "repository_inventory.py"
COUPLING = ROOT / "scripts" / "git_change_coupling.py"


class InventoryTests(unittest.TestCase):
    def test_inventory_finds_candidates_without_generated_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / "src").mkdir()
            (repo / "tests").mkdir()
            (repo / "node_modules" / "pkg").mkdir(parents=True)
            (repo / "src" / "app.py").write_text("print('ok')\n", encoding="utf-8")
            (repo / "tests" / "test_app.py").write_text("pass\n", encoding="utf-8")
            (repo / "README.md").write_text("# Example\n", encoding="utf-8")
            (repo / "package.json").write_text("{}\n", encoding="utf-8")
            (repo / "node_modules" / "pkg" / "index.js").write_text("x\n", encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, str(INVENTORY), str(repo)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            result = json.loads(completed.stdout)

            self.assertEqual(result["summary"]["file_count"], 4)
            self.assertEqual(result["languages_by_file_count"]["Python"], 2)
            self.assertIn("tests/test_app.py", result["evidence_candidates"]["tests"])
            self.assertIn("README.md", result["evidence_candidates"]["documentation"])
            self.assertNotIn("node_modules/pkg/index.js", json.dumps(result))


@unittest.skipUnless(shutil.which("git"), "git is required")
class CouplingTests(unittest.TestCase):
    def test_change_coupling_reports_hotspots_and_pairs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test User"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)

            for name in ("a.py", "b.py"):
                (repo / name).write_text("v1\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "a.py", "b.py"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "initial"], check=True)

            for name in ("a.py", "b.py"):
                (repo / name).write_text("v2\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "a.py", "b.py"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m", "change"], check=True)

            completed = subprocess.run(
                [sys.executable, str(COUPLING), str(repo), "--top", "10"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            result = json.loads(completed.stdout)

            self.assertEqual(result["commit_count"], 2)
            self.assertEqual(result["hotspots"][0]["commits_changed"], 2)
            pair = next(item for item in result["cochange_pairs"] if {item["left"], item["right"]} == {"a.py", "b.py"})
            self.assertEqual(pair["commits_together"], 2)
            self.assertEqual(pair["jaccard"], 1.0)


class PackageContractTests(unittest.TestCase):
    def test_skill_package_has_no_scaffold_placeholders(self) -> None:
        required = [
            ROOT / "SKILL.md",
            ROOT / "agents" / "openai.yaml",
            ROOT / "assets" / "audit-report-template.md",
            ROOT / "assets" / "audit-result.schema.json",
        ]
        for path in required:
            self.assertTrue(path.is_file(), path)
            self.assertNotIn("TODO", path.read_text(encoding="utf-8"))

    def test_json_schema_is_valid_json_with_expected_contract(self) -> None:
        schema = json.loads((ROOT / "assets" / "audit-result.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("production_readiness", schema["required"])
        self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1")

    def test_sample_result_validates_and_scores_reconcile(self) -> None:
        schema = json.loads((ROOT / "assets" / "audit-result.schema.json").read_text(encoding="utf-8"))
        sample = json.loads((ROOT / "examples" / "audit-result.sample.json").read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(sample)

        dimension_total = round(sum(item["weighted_score"] for item in sample["dimensions"]), 1)
        self.assertEqual(dimension_total, 66.6)
        self.assertEqual(sample["engineering_health"]["score"], round(dimension_total))

        ratings = [item["rating"] for item in sample["vibe_slop_risk"]["signals"]]
        calculated_risk = round(min(100, sum(ratings) / (5 * 7) * 100 * sample["vibe_slop_risk"]["mismatch_factor"]))
        self.assertEqual(calculated_risk, sample["vibe_slop_risk"]["score"])

    def test_behavioral_prompt_catalog_is_well_formed(self) -> None:
        catalog = json.loads((ROOT / "test-prompts.json").read_text(encoding="utf-8"))
        ids = [case["id"] for case in catalog["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 5)
        for case in catalog["cases"]:
            self.assertTrue(case["objective"])
            self.assertTrue(case["prompt"])
            self.assertGreaterEqual(len(case["assertions"]), 2)


if __name__ == "__main__":
    unittest.main()
