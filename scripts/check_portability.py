#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "code-security-skills"
FORBIDDEN = (
    "$codex-security:",
    "<python_command>",
    "<plugin_dir>",
    "/tmp/codex-security",
    "app://",
    "/codex-security-skills:",
    "codex-security-plugin",
)
SOURCE_HOST_CALLS = (
    "open_codex_security_workspace",
    "complete_codex_security_scan",
    "start_codex_security_deep_scan",
    "get_codex_security_scan_context",
    "request_codex_security_user_input",
    "update_codex_security_scan_progress",
    "fail_codex_security_scan",
    "cancel_codex_security_scan",
    "open_code_security_triage_results",
)
SOURCE_HOST_PROTOCOLS = (
    "CODE_SECURITY_WORKER_STATUS",
    "fork_turns",
    "interrupt_agent",
    "reviewItemsTotal",
    "reviewItemsCompleted",
    "native v2",
)
PROVENANCE_PREFIX = "> Code Security Skills provenance:"


def main() -> int:
    errors: list[str] = []
    markdown_files = sorted(PLUGIN.rglob("*.md"))
    for path in markdown_files:
        text = path.read_text()
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden token {token!r}")
        for number, line in enumerate(text.splitlines(), 1):
            if "codex" in line.lower() and path.name not in {
                "PROVENANCE.md",
                "THIRD_PARTY_NOTICES.md",
            }:
                if not line.startswith(PROVENANCE_PREFIX):
                    errors.append(
                        f"{path.relative_to(ROOT)}:{number} contains non-provenance Codex wording"
                    )
            for token in SOURCE_HOST_CALLS:
                if token in line:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{number} contains source-host call {token}"
                    )
            for token in SOURCE_HOST_PROTOCOLS:
                if token in line:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{number} contains source-host protocol {token}"
                    )
            if re.search(r"\$[a-z][a-z0-9-]+", line):
                errors.append(
                    f"{path.relative_to(ROOT)}:{number} contains ambiguous source-host skill syntax"
                )

    for path in sorted((PLUGIN / "scripts").glob("*.py")):
        text = path.read_text()
        for token in (*SOURCE_HOST_CALLS, *SOURCE_HOST_PROTOCOLS, "completion_binding"):
            if token in text:
                errors.append(
                    f"{path.relative_to(ROOT)} contains source-host runtime token {token}"
                )

    symlinks = [path for path in PLUGIN.rglob("*") if path.is_symlink()]
    if symlinks:
        errors.extend(f"unexpected symlink: {path.relative_to(ROOT)}" for path in symlinks)

    if errors:
        print("Portability checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    skill_count = len(list((PLUGIN / "skills").glob("*/SKILL.md")))
    print(
        f"Portability checks passed: {skill_count} skills, "
        f"{len(markdown_files)} Markdown files, provider-neutral procedures."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
