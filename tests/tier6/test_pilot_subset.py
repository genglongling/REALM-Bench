import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PILOT_PATH = ROOT / "datasets" / "T6" / "pilot.py"


spec = importlib.util.spec_from_file_location("tier6_pilot", PILOT_PATH)
pilot = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = pilot
spec.loader.exec_module(pilot)


def test_pilot_subset_loads_and_is_not_confirmatory():
    data = pilot.load_pilot_subset()
    assert data["pilot_subset_version"] == "tier6-pilot-subset-v0"
    assert data["not_for_confirmatory_claims"] is True


def test_pilot_generates_one_family_five_sequences():
    sequences = pilot.generate_pilot_sequences(ROOT)
    assert len(sequences) == 5
    assert {seq["base_instance"]["family"] for seq in sequences} == {"jobshop_breakdown"}
    assert all(len(seq["episodes"]) == 10 for seq in sequences)


def test_pilot_has_exactly_one_control_sequence():
    sequences = pilot.generate_pilot_sequences(ROOT)
    controls = [seq for seq in sequences if seq["is_control_sequence"]]
    assert len(controls) == 1
    assert controls[0]["sequence_seed"] == 17


def test_pilot_sequences_have_base_provenance():
    sequences = pilot.generate_pilot_sequences(ROOT)
    for seq in sequences:
        base = seq["base_instance"]
        assert base["source_path"].startswith("datasets/")
        assert len(base["source_sha256"]) == 64
