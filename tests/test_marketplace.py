from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "code-security-skills"
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
    def test_provider_neutral_marketplace_and_plugin_identity(self) -> None:
        marketplace = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text()
        )
        plugin_manifest = json.loads(
            (PLUGIN / ".claude-plugin" / "plugin.json").read_text()
        )

        self.assertEqual(marketplace["name"], "code-security")
        self.assertEqual(marketplace["owner"]["name"], "barvhaim")
        self.assertEqual(marketplace["version"], "1.0.0")
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "code-security-skills")
        self.assertEqual(entry["name"], plugin_manifest["name"])
        self.assertEqual(entry["version"], plugin_manifest["version"])
        self.assertEqual(plugin_manifest["version"], "1.0.0")
        self.assertEqual(entry["author"]["name"], "barvhaim")
        self.assertEqual(plugin_manifest["author"]["name"], "barvhaim")
        self.assertEqual(entry["license"], "Apache-2.0")
        self.assertEqual(entry["source"], "./plugins/code-security-skills")
        self.assertNotIn("..", Path(entry["source"]).parts)
        self.assertNotIn("codex", json.dumps(marketplace).lower())
        self.assertNotIn("codex", json.dumps(plugin_manifest).lower())

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
                self.assertIn("Code Security Skills provenance:", text)

    def test_skill_procedures_are_provider_neutral(self) -> None:
        for path in sorted((PLUGIN / "skills").rglob("*.md")):
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if "codex" not in line.lower():
                    continue
                with self.subTest(path=path.relative_to(ROOT), line=number):
                    self.assertIn("Code Security Skills provenance:", line)
                    self.assertIn("OpenAI", line)

    def test_runtime_contract_has_no_codex_identifiers(self) -> None:
        runtime_roots = [PLUGIN / "scripts", PLUGIN / "schemas", PLUGIN / "examples"]
        for runtime_root in runtime_roots:
            for path in sorted(runtime_root.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                try:
                    text = path.read_text()
                except UnicodeDecodeError:
                    continue
                if runtime_root.name == "scripts":
                    text = "\n".join(
                        line
                        for line in text.splitlines()
                        if not line.startswith("# Modified from OpenAI Codex Security")
                    )
                elif runtime_root.name == "schemas" and path.suffix == ".json":
                    schema = json.loads(text)
                    schema.pop("x-code-security-provenance", None)
                    text = json.dumps(schema)
                with self.subTest(path=path.relative_to(ROOT)):
                    self.assertNotIn("codex", text.lower())

    def test_neutral_artifact_contract(self) -> None:
        example = PLUGIN / "examples" / "completed-scan"
        manifest = json.loads((example / "scan-manifest.json").read_text())
        findings = json.loads((example / "findings.json").read_text())
        coverage = json.loads((example / "coverage.json").read_text())
        sarif = json.loads((example / "exports" / "results.sarif").read_text())

        self.assertEqual(manifest["documentType"], "code-security.scan-manifest")
        self.assertEqual(
            manifest["scan"]["producer"]["name"], "code-security-skills"
        )
        self.assertTrue(
            manifest["scan"]["target"]["snapshotDigest"].startswith(
                "code-security-snapshot/v1:sha256:"
            )
        )
        self.assertEqual(findings["documentType"], "code-security.findings")
        self.assertEqual(coverage["documentType"], "code-security.coverage")
        self.assertTrue(
            findings["findings"][0]["fingerprints"]["primary"].startswith(
                "code-security/v1:sha256:"
            )
        )
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertIn("codeSecuritySchemaVersion", sarif["runs"][0]["properties"])

        for path in sorted((PLUGIN / "schemas").glob("*.json")):
            schema = json.loads(path.read_text())
            self.assertIn("code-security", schema["$id"])
            self.assertNotIn("Codex", schema.get("title", ""))

    def test_attribution_and_license_ship_inside_cached_plugin(self) -> None:
        source = json.loads((PLUGIN / "UPSTREAM_SOURCE.json").read_text())
        self.assertRegex(source["revision"], r"^[0-9a-f]{40}$")
        self.assertEqual(source["license"], "Apache-2.0")
        self.assertIn("openai/codex-security", source["upstream"])
        self.assertTrue((PLUGIN / "LICENSE").is_file())
        self.assertTrue((PLUGIN / "THIRD_PARTY_NOTICES.md").is_file())
        self.assertTrue((PLUGIN / "PROVENANCE.md").is_file())
        self.assertFalse((PLUGIN / "ADAPTATION.md").exists())
        self.assertIn(
            "OpenAI Codex Security",
            (PLUGIN / "THIRD_PARTY_NOTICES.md").read_text(),
        )

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

    def test_source_host_runtime_is_not_shipped(self) -> None:
        self.assertFalse((PLUGIN / ".mcp.json").exists())
        self.assertFalse((PLUGIN / ".codex-plugin").exists())
        self.assertFalse((PLUGIN / "mcp").exists())
        self.assertFalse((PLUGIN / ".app.json").exists())
        self.assertFalse((PLUGIN / "preflight").exists())
        self.assertFalse((PLUGIN / "scripts" / "config_preflight.py").exists())
        self.assertFalse((PLUGIN / "references" / "config-preflight.md").exists())

    def test_runtime_surface_contains_only_standalone_helpers(self) -> None:
        expected = {
            "finalize_scan_contract.py",
            "generate_rank_input.py",
            "normalize_candidates.py",
            "rank_preview.py",
            "report_projection.py",
            "resolve_security_md.py",
            "validate_report_format.py",
            "validate_scan_contract.py",
            "validate_tracking_source.py",
            "windows_scan_local_files.py",
        }
        actual = {
            path.name
            for path in (PLUGIN / "scripts").glob("*.py")
            if path.name != "__init__.py"
        }
        self.assertEqual(actual, expected)

    def test_modified_derivative_files_carry_notices(self) -> None:
        provenance = "Code Security Skills provenance: adapted from OpenAI's Codex Security"
        for path in sorted(PLUGIN.rglob("*.md")):
            if path.name in {"PROVENANCE.md", "THIRD_PARTY_NOTICES.md"} or "examples" in path.parts:
                continue
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(provenance, path.read_text())

        for path in sorted((PLUGIN / "scripts").glob("*.py")):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(
                    "Modified from OpenAI Codex Security",
                    "\n".join(path.read_text().splitlines()[:3]),
                )

        for path in sorted((PLUGIN / "schemas").glob("*.json")):
            schema = json.loads(path.read_text())
            self.assertIn("Modified from OpenAI Codex Security", schema["x-code-security-provenance"])

    def test_source_host_protocols_are_absent(self) -> None:
        forbidden = {
            "open_code_security_triage_results",
            "CODE_SECURITY_WORKER_STATUS",
            "fork_turns",
            "interrupt_agent",
            "reviewItemsTotal",
            "reviewItemsCompleted",
            "native v2",
            "completion_binding",
        }
        paths = [*PLUGIN.rglob("*.md"), *(PLUGIN / "scripts").glob("*.py")]
        for path in sorted(paths):
            text = path.read_text()
            for token in forbidden:
                with self.subTest(path=path.relative_to(ROOT), token=token):
                    self.assertNotIn(token, text)
            if path.suffix == ".md":
                self.assertIsNone(re.search(r"\$[a-z][a-z0-9-]+", text))

    def test_public_documentation_uses_neutral_identity(self) -> None:
        readme = (ROOT / "README.md").read_text()
        self.assertIn(
            "/plugin marketplace add barvhaim/code-security-skills",
            readme,
        )
        self.assertIn(
            "/plugin install code-security-skills@code-security",
            readme,
        )
        self.assertIn("/code-security-skills:security-scan", readme)
        self.assertNotIn("codex-security-skills", readme.lower())
        self.assertNotIn("codex-security-for-claude", readme.lower())
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


if __name__ == "__main__":
    unittest.main()
