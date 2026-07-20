from __future__ import annotations

import json

from analysis.realm_tier6 import family_stratified_report as module


def sample_r88_report() -> dict:
    return {
        "sequence_id": "T6-7e17ef0cc5f3",
        "config_id": "E7",
        "condition_label": "full_crt_stack",
        "official_scorer_invoked": True,
        "overall_score": {
            "num_events": 40,
            "num_control_events": 0,
            "num_non_control_events": 40,
            "safety_passed": True,
            "safety_counts": {
                "invalid_commit_count": 0,
                "evidence_destroying_repair_count": 0,
                "orphaned_dependent_count": 0,
            },
            "repeated_failure_rate": 0.0,
            "repeated_failure_rate_controls": 0.0,
            "time_to_correction_mean_observed": None,
            "time_to_correction_observed_count": 0,
            "time_to_correction_censored_count": 40,
            "horizon_reward_mean": 0.90125,
            "grounded_admission_rate": 0.725,
            "bracket": {
                "position_repeated_failure_rate": 1.0,
                "position_horizon_reward": 0.90125,
            },
        },
    }


def test_sequence_summary_by_family() -> None:
    sequences = module.generator.generate_development_sequences(
        module.REPO_ROOT,
        max_families=2,
    )
    summary = module.sequence_summary_by_family(sequences)

    assert len(summary) == 2
    for item in summary.values():
        assert item["num_sequences"] == 5
        assert item["num_episodes"] == 50
        assert item["num_control_sequences"] == 1


def test_score_events_by_family_has_expected_families() -> None:
    sequences = module.generator.generate_development_sequences(
        module.REPO_ROOT,
        max_families=2,
    )
    events = module.emit_b0_memoryless_events(sequences)
    scores = module.score_events_by_family(events)

    assert len(scores) == 2
    for score in scores.values():
        assert score["safety_passed"] is True
        assert score["repeated_failure_rate"] == 1.0
        assert score["horizon_reward_mean"] == 0.0


def test_build_report_without_live_pilot() -> None:
    report = module.build_report(
        max_families=1,
        r88_score_report_path=module.Path("/tmp/does-not-exist-r88.json"),
        live_pilot_family="jobshop_breakdown",
    )

    assert report["schema"] == module.SCHEMA
    assert report["r88_live_llm_pilot_available"] is False
    assert len(report["families"]) == 1
    assert len(report["chapter6_family_table"]) == 2


def test_build_report_with_live_pilot(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=1,
        r88_score_report_path=r88_path,
        live_pilot_family="jobshop_breakdown",
    )

    assert report["r88_live_llm_pilot_available"] is True
    assert len(report["chapter6_family_table"]) == 3

    pilot_rows = [
        row
        for row in report["chapter6_family_table"]
        if row["system_id"] == "mnemosyne_live_llm_r88_pilot"
    ]
    assert len(pilot_rows) == 1
    assert pilot_rows[0]["family"] == "jobshop_breakdown"
    assert pilot_rows[0]["horizon_reward_mean"] == 0.90125


def test_render_markdown_contains_claim_boundary(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=1,
        r88_score_report_path=r88_path,
        live_pilot_family="jobshop_breakdown",
    )
    markdown = module.render_markdown(report)

    assert "Family-Stratified REALM Tier-6 Report" in markdown
    assert "Chapter 6 Family-Stratified Table" in markdown
    assert "not yet family-generalized live-LLM evidence" in markdown
