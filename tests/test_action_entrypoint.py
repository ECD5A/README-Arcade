"""Tests for the composite-action entrypoint."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ActionEntrypointTests(unittest.TestCase):
    def test_generates_both_themes_and_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            output_file = workdir / "github-output.txt"
            env = os.environ.copy()
            env.update(
                {
                    "GITHUB_OUTPUT": str(output_file),
                    "GITHUB_REPOSITORY_OWNER": "octocat",
                    "INPUT_CONFIG": "missing-config.json",
                    "INPUT_OUTPUT_DIR": "generated",
                    "INPUT_MODE": "snake",
                    "INPUT_BASE_NAME": "arcade-test",
                    "INPUT_SEED": "test-seed",
                    "INPUT_GITHUB_TOKEN": "",
                }
            )

            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "action_entrypoint.py")],
                cwd=workdir,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )

            light = workdir / "generated" / "arcade-test.svg"
            dark = workdir / "generated" / "arcade-test-dark.svg"
            self.assertTrue(light.is_file())
            self.assertTrue(dark.is_file())
            outputs = output_file.read_text(encoding="utf-8")
            self.assertIn("light-svg=generated/arcade-test.svg", outputs)
            self.assertIn("dark-svg=generated/arcade-test-dark.svg", outputs)


if __name__ == "__main__":
    unittest.main()
