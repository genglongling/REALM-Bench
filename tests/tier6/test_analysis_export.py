import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EMITTER_PATH = ROOT / "datasets" / "T6" / "fixture_emitter.py"
ANALYZER_PATH = ROOT / "analysis" / "realm_tier6" / "analyze_run.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


emitter = load_module("tier6_fixture_emitter_for_analysis_test", EMITTER_PATH)
analyzer = load_module("tier6_analyze_run", ANALYZER_PATH)


def test_analysis_regenerates_summary_csv_and_report(tmp_path):
    run_dir = tmp_path / "run"
    emitter.emit_fixture_run(run_dir)

    summary = analyzer.analyze_run(run_dir)

    assert (run_dir / "summary.json").exists()
    assert (run_dir / "summary.csv").exists()
    assert (run_dir / "report.md").exists()

    csv_text = (run_dir / "summary.csv").read_text(encoding="utf-8")
    report_text = (run_dir / "report.md").read_text(encoding="utf-8")

    assert "bracket_position_repeated_failure_rate" in csv_text
    assert "deterministic harness validation only" in report_text
    assert summary["safety_passed"] is True


def test_analysis_summary_matches_json(tmp_path):
    run_dir = tmp_path / "run"
    emitter.emit_fixture_run(run_dir)
    summary = analyzer.analyze_run(run_dir)

    saved = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    assert saved["num_events"] == summary["num_events"]
    assert saved["bracket"]["position_repeated_failure_rate"] == summary["bracket"]["position_repeated_failure_rate"]
