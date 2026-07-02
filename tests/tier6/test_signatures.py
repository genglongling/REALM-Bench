import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SIGNATURES_PATH = ROOT / "datasets" / "T6" / "signatures.py"
DICTIONARY_PATH = ROOT / "datasets" / "T6" / "dictionary_v0.json"
SEEDS_PATH = ROOT / "datasets" / "T6" / "public_seeds_v0.json"


spec = importlib.util.spec_from_file_location("tier6_signatures", SIGNATURES_PATH)
signatures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signatures)


def test_dictionary_loads_and_has_version():
    data = signatures.load_dictionary(DICTIONARY_PATH)
    assert data["dictionary_version"] == "tier6-signature-dictionary-v0"
    assert "stale_world.route_time_underestimated" in data["signatures"]


def test_signature_validation_accepts_known_signature():
    data = signatures.load_dictionary(DICTIONARY_PATH)
    value = signatures.validate_signature("stale_world.route_time_underestimated", data)
    assert value == "stale_world.route_time_underestimated"


def test_signature_canonicalization():
    value = signatures.canonicalize_signature("Stale World.Route Time Underestimated")
    assert value == "stale_world.route_time_underestimated"


def test_unknown_signature_fails():
    data = signatures.load_dictionary(DICTIONARY_PATH)
    with pytest.raises(signatures.SignatureDictionaryError):
        signatures.validate_signature("unknown.failure", data)


def test_signature_tuple_is_available():
    data = signatures.load_dictionary(DICTIONARY_PATH)
    tup = signatures.signature_tuple("temporal.myopic_choice_causes_later_failure", data)
    assert tup == (
        "temporal",
        "sequence_policy",
        "myopic_choice_causes_later_failure",
    )


def test_public_seed_file_has_five_development_seeds():
    with SEEDS_PATH.open("r", encoding="utf-8") as handle:
        seeds = json.load(handle)

    assert seeds["episodes_per_sequence"] == 10
    assert len(seeds["public_sequence_seeds"]) == 5
    assert seeds["control_sequence_fraction_minimum"] >= 0.2
