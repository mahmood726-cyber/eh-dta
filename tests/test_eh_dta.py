import importlib.util
import json
from pathlib import Path


def load_module():
    script_path = Path(__file__).resolve().parents[1] / "simulation.py"
    spec = importlib.util.spec_from_file_location("eh_dta_simulation", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_main_writes_relative_outputs(tmp_path):
    module = load_module()

    result = module.main(seed=1392, project_root=tmp_path)

    certification_path = tmp_path / "certification.json"
    landscape_path = tmp_path / "landscape.csv"

    assert certification_path.exists()
    assert landscape_path.exists()

    certification = json.loads(certification_path.read_text(encoding="utf-8"))
    assert certification["system"] == "Evidence Horizon (EH-DTA)"
    assert len(certification["prescriptions"]) <= 3
    assert result["dataframe"].shape[0] == 60
