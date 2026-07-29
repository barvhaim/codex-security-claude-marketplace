#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "codex-security-skills"
CLAUDE_PACKAGE = "@anthropic-ai/claude-code@2.1.220"
EXPECTED = "Loaded 13 skills from plugin codex-security-skills default directory"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="claude-plugin-loader-") as temporary:
        debug_log = Path(temporary) / "debug.log"
        environment = os.environ.copy()
        environment.pop("ANTHROPIC_API_KEY", None)
        environment.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
        result = subprocess.run(
            [
                "npx",
                "--yes",
                CLAUDE_PACKAGE,
                "--plugin-dir",
                str(PLUGIN),
                "--debug-file",
                str(debug_log),
                "--tools",
                "",
                "--no-session-persistence",
                "--print",
                "/codex-security-skills:threat-model Return only the skill title.",
            ],
            cwd=ROOT,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
            check=False,
        )
        log = debug_log.read_text(errors="replace") if debug_log.exists() else ""
        if EXPECTED not in log:
            print(result.stdout)
            raise SystemExit(
                "Claude Code did not report loading all 13 plugin skills. "
                f"CLI exit code: {result.returncode}"
            )
        print(
            "Claude loader smoke test passed: the real Claude Code loader discovered all 13 skills."
        )
        if result.returncode != 0:
            print("Model invocation was intentionally not required; this environment may be unauthenticated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
