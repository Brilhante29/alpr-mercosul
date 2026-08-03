from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
V1_PATH = ROOT / "benchmarks/results/baseline.json"
V2_PATH = ROOT / "benchmarks/publication/alpr-baseline-v2.json"
CONFIG_PATH = ROOT / "benchmarks/config/alpr-synthetic-v1.json"


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
    assert v2["workload"]["fixture_digest"] == sha256(ROOT / "src/alpr_mercosul/fixture.py")
    assert v2["workload"]["config_digest"] == sha256(CONFIG_PATH)
    assert v2["provenance"]["dependency_lock_digest"] == sha256(ROOT / "requirements.txt")
    assert v2["provenance"]["clean_tree"] is True
    assert re.fullmatch(r"[0-9a-f]{40}", v2["provenance"]["source_commit"])
    assert v2["provenance"]["image_ref"].endswith(v2["provenance"]["image_digest"])
    assert "template-matching-v1" in v2["comparability_key"]
    windows_home = "C:" + "/" + "Users" + "/"
    windows_home_backslash = "\\" + "Users" + "\\"
    assert windows_home not in v2["execution"]["command"]
    assert windows_home_backslash not in v2["execution"]["command"]
