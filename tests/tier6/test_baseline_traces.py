from evaluation.tier6.baseline_traces import (
    emit_b0_memoryless_events,
    emit_baseline_run,
    emit_bstar_oracle_events,
)
from evaluation.tier6.scorer import score_trace

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR_PATH = ROOT / "datasets" / "T6" / "generator.py"


spec = importlib.util.spec_from_file_location("tier6_generator_for_baseline_tests", GENERATOR_PATH)
generator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = generator
spec.loader.exec_module(generator)


def test_b0_memoryless_baseline_scores_as_lower_anchor():
    sequences = generator.generate_development_sequences(ROOT, max_families=1)
    events = emit_b0_memoryless_events(sequences)
    summary = score_trace(events)

    assert summary["safety_passed"] is True
    assert summary["repeated_failure_rate"] == 1.0
    assert summary["horizon_reward_mean"] == 0.0


def test_bstar_oracle_baseline_scores_as_upper_anchor():
    sequences = generator.generate_development_sequences(ROOT, max_families=1)
    events = emit_bstar_oracle_events(sequences)
    summary = score_trace(events)

    assert summary["safety_passed"] is True
    assert summary["repeated_failure_rate"] == 0.0
    assert summary["horizon_reward_mean"] > 0.8


def test_baseline_run_writes_required_files(tmp_path):
    sequences = generator.generate_development_sequences(ROOT, max_families=1)
    result = emit_baseline_run(
        baseline_id="B0_memoryless_replay",
        output_dir=tmp_path / "b0",
        sequences=sequences,
    )

    assert (tmp_path / "b0" / "manifest.json").exists()
    assert (tmp_path / "b0" / "events.jsonl").exists()
    assert (tmp_path / "b0" / "summary.json").exists()
    assert result["manifest"]["baseline_id"] == "B0_memoryless_replay"
