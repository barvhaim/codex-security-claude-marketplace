#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "code-security-skills"


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="code-security-finalize-") as temporary:
        scan_dir = Path(temporary) / "scan"
        shutil.copytree(PLUGIN / "examples" / "completed-scan", scan_dir)
        subprocess.run(
            [
                "python3",
                str(PLUGIN / "scripts" / "finalize_scan_contract.py"),
                "--scan-dir",
                str(scan_dir),
                "--schema-dir",
                str(PLUGIN / "schemas"),
                "--source-root",
                str(PLUGIN),
            ],
            check=True,
        )
        manifest = json.loads((scan_dir / "scan-manifest.json").read_text())
        required = [
            scan_dir / "report.md",
            scan_dir / "exports" / "results.sarif",
            scan_dir / "findings.json",
            scan_dir / "coverage.json",
        ]
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise SystemExit(f"finalizer did not create required artifacts: {missing}")
        if manifest["scan"]["status"] != "completed":
            raise SystemExit("finalized manifest status is not completed")
        if not manifest["scan"].get("sealedAt"):
            raise SystemExit("finalized manifest is not sealed")
        print(
            "Finalizer smoke test passed: canonical JSON sealed, report.md and SARIF generated."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
