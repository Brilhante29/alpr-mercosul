from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
V1_PATH = ROOT / "benchmarks/results/baseline.json"
V2_PATH = ROOT / "benchmarks/publication/alpr-baseline-v2.json"
CONFIG_PATH = ROOT / "benchmarks/config/alpr-synthetic-v1.json"
FIXTURE_PATH = ROOT / "src/alpr_mercosul/fixture.py"
LOCK_PATH = ROOT / "requirements.txt"
MODULE_SPEC = importlib.util.spec_from_file_location(
    "publication_validator", ROOT / "tools/validate_publication.py"
)
assert MODULE_SPEC is not None and MODULE_SPEC.loader is not None
validator = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(validator)


def sha256(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def test_publication_evidence_matches_raw_pixel_ocr_run():
    v1 = json.loads(V1_PATH.read_text())
    v2 = json.loads(V2_PATH.read_text())
    config = json.loads(CONFIG_PATH.read_text())

    total_plates = v1["metrics"]["total_plates"]
    assert total_plates == config["n_plates"] == 100
    assert len(v1["plates"]) == total_plates
    assert v1["metrics"]["total_characters"] == 700
    assert v1["environment"]["ocr_backend"] == "template-matching-v1"
    assert v1["proof"]["prediction_input"] == "image_pixels_only"
    assert v1["failures"] == 0

    metric = next(item for item in v2["metrics"] if item["name"] == "character_accuracy")
    assert metric["value"] == metric["samples"][0] == v1["value"]
    assert metric["failures"] == v1["failures"]
    assert v2["execution"]["repeat"] == len(metric["samples"]) == 1
    assert v2["workload"]["measured_iterations"] == total_plates
    assert v2["provenance"]["artifact_digest"] == sha256(V1_PATH)
    validator.validate_committed_digests(v2, FIXTURE_PATH, CONFIG_PATH, LOCK_PATH)
    assert v2["provenance"]["clean_tree"] is True
    assert re.fullmatch(r"[0-9a-f]{40}", v2["provenance"]["source_commit"])
    assert v2["provenance"]["image_ref"].endswith(v2["provenance"]["image_digest"])
    assert "template-matching-v1" in v2["comparability_key"]
    windows_home = "C:" + "/" + "Users" + "/"
    windows_home_backslash = "\\" + "Users" + "\\"
    assert windows_home not in v2["execution"]["command"]
    assert windows_home_backslash not in v2["execution"]["command"]


def test_current_dependency_changes_preserve_historical_validation(monkeypatch):
    v2 = json.loads(V2_PATH.read_text())
    original_read_bytes = Path.read_bytes

    def changed_checkout(path):
        if path == LOCK_PATH:
            return b"pillow==12.3.0\nnumpy==1.26.4\n"
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", changed_checkout)
    assert sha256(LOCK_PATH) != v2["provenance"]["dependency_lock_digest"]
    validator.validate_committed_digests(v2, FIXTURE_PATH, CONFIG_PATH, LOCK_PATH)


@pytest.mark.parametrize(
    ("section", "field", "message"),
    [
        ("provenance", "dependency_lock_digest", "committed dependency lock digest mismatch"),
        ("workload", "fixture_digest", "committed fixture digest mismatch"),
        ("workload", "config_digest", "committed config digest mismatch"),
    ],
)
def test_historical_digest_tampering_is_rejected(section, field, message):
    v2 = json.loads(V2_PATH.read_text())
    v2[section][field] = "sha256:" + "0" * 64
    with pytest.raises(AssertionError, match=message):
        validator.validate_committed_digests(v2, FIXTURE_PATH, CONFIG_PATH, LOCK_PATH)


def test_unavailable_historical_commit_is_rejected():
    v2 = json.loads(V2_PATH.read_text())
    v2["provenance"]["source_commit"] = "0" * 40
    with pytest.raises(AssertionError, match="source commit unavailable"):
        validator.validate_committed_digests(v2, FIXTURE_PATH, CONFIG_PATH, LOCK_PATH)
