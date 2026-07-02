import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR_PATH = ROOT / "datasets" / "T6" / "generator.py"


spec = importlib.util.spec_from_file_location("tier6_generator", GENERATOR_PATH)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)


def test_discover_base_instances_uses_existing_realm_datasets():
    instances = generator.discover_base_instances(ROOT)
    assert instances, "Tier-6 generator must discover existing REALM base instances"
    families = {item["family"] for item in instances}
    assert "jobshop_breakdown" in families or "ride_or_routing_disruption" in families
    for item in instances[:5]:
        assert item["source_path"].startswith("datasets/")
        assert len(item["source_sha256"]) == 64


def test_generate_sequence_has_ten_episodes_and_base_provenance():
    base = generator.discover_base_instances(ROOT)[0]
    seq = generator.generate_sequence(base, sequence_seed=17, episodes_per_sequence=10)
    assert len(seq["episodes"]) == 10
    assert seq["episodes"][0]["base_instance_id"] == base["base_instance_id"]
    assert seq["episodes"][0]["source_sha256"] == base["source_sha256"]


def test_generation_is_deterministic_for_same_seed():
    base = generator.discover_base_instances(ROOT)[0]
    seq1 = generator.generate_sequence(base, sequence_seed=42)
    seq2 = generator.generate_sequence(base, sequence_seed=42)
    assert seq1 == seq2


def test_control_sequence_has_no_hazards():
    base = generator.discover_base_instances(ROOT)[0]
    seq = generator.generate_sequence(base, sequence_seed=17, force_control=True)
    assert seq["is_control_sequence"] is True
    assert seq["hazard_signatures"] == []


def test_non_control_sequence_has_versioned_hazards():
    base = generator.discover_base_instances(ROOT)[0]
    seq = generator.generate_sequence(base, sequence_seed=17, force_control=False)
    assert seq["is_control_sequence"] is False
    assert 1 <= len(seq["hazard_signatures"]) <= 3
    for episode in seq["episodes"]:
        assert episode["hazard_signatures"] == seq["hazard_signatures"]
        assert episode["perturbation"]["operators"] == ["jitter", "rename", "resample"]


def test_development_sequences_are_generated_from_public_seeds():
    seqs = generator.generate_development_sequences(ROOT, max_families=1)
    assert len(seqs) == 5
    assert all(len(seq["episodes"]) == 10 for seq in seqs)
