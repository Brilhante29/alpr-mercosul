from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "tools" / "validate-project.ps1"

pytestmark = pytest.mark.skipif(
    shutil.which("pwsh") is None,
    reason="pwsh is required to execute the portfolio validator",
)


def run_validator(cwd: Path) -> subprocess.CompletedProcess[str]:
    # $ErrorActionPreference is set to "stop" the same way GitHub Actions sets it
    # for `shell: pwsh`, because that is what turns Write-Error into a terminating
    # error and previously truncated the failure list.
    return subprocess.run(
        [
            "pwsh",
            "-NoProfile",
            "-Command",
            '$ErrorActionPreference = "stop"; ./tools/validate-project.ps1 -SkipDocker',
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


class TestValidatorFailureReporting:
    def test_reports_every_failure_not_only_the_first(self, tmp_path: Path) -> None:
        project = tmp_path / "project"
        project.mkdir()
        (project / "tools").mkdir()
        shutil.copy(VALIDATOR, project / "tools" / "validate-project.ps1")

        # No required files and no benchmark JSON: several gates fail at once.
        result = run_validator(project)

        assert result.returncode == 1
        assert "portfolio project validation failed" in result.stdout
        reported = [
            line.strip()[2:]
            for line in result.stdout.splitlines()
            if line.startswith("  - ")
        ]
        # A single reported failure means the list was truncated by the first
        # terminating Write-Error, which is the regression this guards against.
        assert len(reported) > 1, f"only {len(reported)} failure(s) reported: {reported}"
        assert any("REFERENCES.md" in failure for failure in reported)
        assert any("benchmark JSON" in failure for failure in reported)

    def test_passing_project_exits_zero(self) -> None:
        result = run_validator(REPO_ROOT)

        assert result.returncode == 0, result.stdout + result.stderr
        assert "portfolio project validation passed" in result.stdout
