from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-security-skills"
EXPECTED_SKILLS = {
    "attack-path-analysis",
    "deep-security-scan",
    "define-security-policy",
    "finding-discovery",
    "fix-finding",
    "propose-security-hardening",
    "security-diff-scan",
    "security-scan",
    "threat-model",
    "track-findings",
    "triage-finding",
    "validation",
    "vulnerability-writeup",
}


class MarketplaceTests(unittest.TestCase):
    def test_marketplace_and_plugin_manifests_agree(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text()
        )
        plugin_manifest = json.loads(
            (PLUGIN / ".claude-plugin" / "plugin.json").read_text()
        )

        self.assertEqual(marketplace["name"], "codex-security-for-claude")
        self.assertEqual(marketplace["owner"]["name"], "barvhaim")
        self.assertEqual(marketplace["version"], "0.1.1")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], plugin_manifest["name"])
        self.assertEqual(entry["version"], plugin_manifest["version"])
        self.assertEqual(plugin_manifest["version"], "0.1.1")
        self.assertEqual(entry["author"]["name"], "barvhaim")
        self.assertEqual(plugin_manifest["author"]["name"], "barvhaim")
        self.assertEqual(entry["license"], "Apache-2.0")
        self.assertEqual(entry["source"], "./plugins/codex-security-skills")
        self.assertNotIn("..", Path(entry["source"]).parts)

    def test_all_thirteen_skills_are_packaged(self) -> None:
        actual = {
            path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(actual, EXPECTED_SKILLS)

    def test_skill_frontmatter_is_claude_discoverable(self) -> None:
        for name in sorted(EXPECTED_SKILLS):
            with self.subTest(skill=name):
                text = (PLUGIN / "skills" / name / "SKILL.md").read_text()
                self.assertTrue(text.startswith("---\n"))
                end = text.find("\n---\n", 4)
                self.assertGreater(end, 4)
                frontmatter = text[4:end]
                self.assertRegex(frontmatter, rf"(?m)^name:\s*{re.escape(name)}\s*$")
                self.assertRegex(frontmatter, r"(?m)^description:\s*.+$")
                self.assertIn("Claude Code adaptation notice:", text)

    def test_attribution_and_license_ship_inside_cached_plugin(self) -> None:
        source = json.loads((PLUGIN / "UPSTREAM_SOURCE.json").read_text())
        self.assertRegex(source["revision"], r"^[0-9a-f]{40}$")
        self.assertEqual(source["license"], "Apache-2.0")
        self.assertTrue((PLUGIN / "LICENSE").is_file())
        self.assertTrue((PLUGIN / "THIRD_PARTY_NOTICES.md").is_file())
        self.assertTrue((PLUGIN / "ADAPTATION.md").is_file())

    def test_required_runtime_assets_are_packaged(self) -> None:
        for relative in [
            "references/scan-contract.md",
            "references/final-report.md",
            "schemas/scan-manifest.schema.json",
            "schemas/findings.schema.json",
            "schemas/coverage.schema.json",
            "scripts/finalize_scan_contract.py",
            "examples/completed-scan/scan-manifest.json",
            "examples/completed-scan/report.md",
            "examples/completed-scan/exports/results.sarif",
        ]:
            with self.subTest(path=relative):
                self.assertTrue((PLUGIN / relative).is_file())

    def test_codex_only_plugin_runtime_is_not_accidentally_shipped(self) -> None:
        self.assertFalse((PLUGIN / ".mcp.json").exists())
        self.assertFalse((PLUGIN / ".codex-plugin").exists())
        self.assertFalse((PLUGIN / "mcp").exists())
        self.assertFalse((PLUGIN / ".app.json").exists())

    def test_public_launch_documentation_is_consistent(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn(
            "/plugin marketplace add barvhaim/codex-security-claude-marketplace",
            readme,
        )
        self.assertIn(
            "/plugin install codex-security-skills@codex-security-for-claude",
            readme,
        )
        self.assertNotIn("njs-" + "security-skills", readme)
        self.assertNotIn("access to the private repository", readme)
        for relative in [
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            ".github/ISSUE_TEMPLATE/bug.yml",
            ".github/ISSUE_TEMPLATE/feature.yml",
            ".github/PULL_REQUEST_TEMPLATE.md",
        ]:
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file())

    def test_social_preview_has_github_dimensions(self) -> None:
        data = (ROOT / "docs" / "social-preview.png").read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (1280, 640))

    def test_example_sarif_is_parseable(self) -> None:
        sarif = json.loads(
            (PLUGIN / "examples/completed-scan/exports/results.sarif").read_text()
        )
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertGreaterEqual(len(sarif["runs"]), 1)


if __name__ == "__main__":
    unittest.main()
