import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EMITTER_PATH = ROOT / "datasets" / "T6" / "fixture_emitter.py"


spec = importlib.util.spec_from_file_location("tier6_fixture_emitter", EMITTER_PATH)
emitter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = emitter
spec.loader.exec_module(emitter)


def test_fixture_emitter_writes_required_outputs(tmp_path):
    out = tmp_path / "run"
    result = emitter.emit_fixture_run(out)

    assert (out / "manifest.json").exists()
    assert (out / "events.jsonl").exists()
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()

    assert result["summary"]["safety_passed"] is True


def test_fixture_events_are_schema_consumable(tmp_path):
    out = tmp_path / "run"
    emitter.emit_fixture_run(out)

    events = [
        json.loads(line)
        for line in (out / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert events
    assert any(event["is_control_sequence"] for event in events)
    assert any(not event["is_control_sequence"] for event in events)
    assert all("time_to_correction_censored" in event for event in events)


def test_fixture_report_preserves_claim_boundary(tmp_path):
    out = tmp_path / "run"
    emitter.emit_fixture_run(out)

    report = (out / "report.md").read_text(encoding="utf-8")
    assert "deterministic harness validation only" in report
    assert "must not be used as evidence for H1-H5" in report
    assert emitter.CANONICAL_SENTENCE in report


def test_fixture_summary_has_expected_safety_gate(tmp_path):
    out = tmp_path / "run"
    emitter.emit_fixture_run(out)

    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["safety_passed"] is True
    assert summary["safety_counts"]["invalid_commit_count"] == 0
    assert summary["time_to_correction_censored_count"] > 0
