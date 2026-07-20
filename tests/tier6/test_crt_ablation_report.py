from __future__ import annotations

import json

from analysis.realm_tier6 import crt_ablation_report as module


def write_sample_result(path, config_id, rfr, horizon, grounded=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "config_id": config_id,
                "summary": {
                    "num_events": 78,
                    "safety_passed": True,
                    "repeated_failure_rate": rfr,
                    "horizon_reward_mean": horizon,
                    "grounded_admission_rate": grounded,
                },
            }
        ),
        encoding="utf-8",
    )


def test_collect_and_select_records(tmp_path) -> None:
    write_sample_result(tmp_path / "kernel" / "E0" / "summary.json", "E0", 1.0, 0.0)
    write_sample_result(tmp_path / "kernel" / "E7" / "summary.json", "E7", 0.0, 0.8423076923076923, 1.0)

    records = module.collect_candidate_records([tmp_path / "kernel"])
    selected = module.select_best_records(records)

    assert set(selected) == {"E0", "E7"}
    assert selected["E7"]["horizon_reward_mean"] == 0.8423076923076923


def test_build_ablation_table_computes_deltas(tmp_path) -> None:
    write_sample_result(tmp_path / "kernel" / "E0" / "summary.json", "E0", 1.0, 0.0)
    write_sample_result(tmp_path / "kernel" / "E1" / "summary.json", "E1", 0.5, 0.5, 0.5)
    write_sample_result(tmp_path / "kernel" / "E2" / "summary.json", "E2", 0.0, 0.3076923076923077)
    write_sample_result(tmp_path / "kernel" / "E3" / "summary.json", "E3", 1.0, 0.75)
    write_sample_result(tmp_path / "kernel" / "E7" / "summary.json", "E7", 0.0, 0.8423076923076923, 1.0)

    report = module.build_report([tmp_path / "kernel"])

    assert report["all_required_configs_available"] is True
    assert report["missing_configs"] == []

    rows = {row["config_id"]: row for row in report["chapter6_table"]}
    assert rows["E0"]["delta_horizon_vs_e0"] == 0.0
    assert rows["E1"]["label"] == "+C contextual admission"
    assert rows["E7"]["delta_rfr_vs_e0"] == -1.0
    assert rows["E7"]["delta_horizon_vs_e0"] == 0.8423076923076923


def test_missing_configs_are_reported(tmp_path) -> None:
    write_sample_result(tmp_path / "kernel" / "E0" / "summary.json", "E0", 1.0, 0.0)

    report = module.build_report([tmp_path / "kernel"])

    assert report["all_required_configs_available"] is False
    assert report["missing_configs"] == ["E1", "E2", "E3", "E7"]


def test_render_markdown_contains_chapter_insert(tmp_path) -> None:
    write_sample_result(tmp_path / "kernel" / "E0" / "summary.json", "E0", 1.0, 0.0)
    write_sample_result(tmp_path / "kernel" / "E1" / "summary.json", "E1", 0.5, 0.5, 0.5)
    write_sample_result(tmp_path / "kernel" / "E2" / "summary.json", "E2", 0.0, 0.3076923076923077)
    write_sample_result(tmp_path / "kernel" / "E3" / "summary.json", "E3", 1.0, 0.75)
    write_sample_result(tmp_path / "kernel" / "E7" / "summary.json", "E7", 0.0, 0.8423076923076923, 1.0)

    report = module.build_report([tmp_path / "kernel"])
    markdown = module.render_markdown(report)

    assert "CRT-Stack Ablation Report" in markdown
    assert "Chapter 6 CRT Ablation Table" in markdown
    assert "Chapter 6 Insert Draft" in markdown
    assert "0.8423076923076923" in markdown
