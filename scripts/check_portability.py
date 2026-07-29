#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-security-skills"
FORBIDDEN = (
    "$codex-security:",
    "<python_command>",
    "<plugin_dir>",
    "/tmp/codex-security",
)
HOST_CALLS = (
    "open_codex_security_workspace",
    "complete_codex_security_scan",
    "start_codex_security_deep_scan",
    "get_codex_security_scan_context",
    "request_codex_security_user_input",
    "update_codex_security_scan_progress",
    "fail_codex_security_scan",
    "cancel_codex_security_scan",
)


def main() -> int:
    errors: list[str] = []
    markdown_files = sorted(PLUGIN.rglob("*.md"))
    for path in markdown_files:
        text = path.read_text()
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{path.relative_to(ROOT)} contains forbidden token {token!r}")

    for path in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for token in HOST_CALLS:
                if token not in line:
                    continue
                allowed_explanation = (
                    "Do not call Codex-specific MCP tools" in line
                    or "Do not call Codex Security MCP tools" in line
                )
                if not allowed_explanation:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{number} invokes or discusses unsupported host call {token}"
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
        f"{len(markdown_files)} Markdown files, no unresolved host placeholders."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
