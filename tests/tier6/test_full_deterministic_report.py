from __future__ import annotations

import json

from analysis.realm_tier6 import full_deterministic_report as module


def sample_r88_report() -> dict:
    return {
        "sequence_id": "T6-7e17ef0cc5f3",
        "config_id": "E7",
        "condition_label": "full_crt_stack",
        "official_scorer_invoked": True,
        "score_scope": "mnemosyne_live_llm_handoff_derived_events",
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


def test_summarize_sequences_uses_public_development_shape() -> None:
    sequences = module.generator.generate_development_sequences(
        module.REPO_ROOT,
        max_families=1,
    )
    summary = module.summarize_sequences(sequences)

    assert summary["num_sequences"] == 5
    assert summary["num_episodes"] == 50
    assert summary["num_control_sequences"] == 1
    assert summary["episodes_per_sequence"] == 10


def test_build_report_scores_b0_and_bstar(tmp_path) -> None:
    missing_r88 = tmp_path / "missing_r88.json"
    report = module.build_report(
        max_families=1,
        r88_score_report_path=missing_r88,
    )

    assert report["schema"] == module.SCHEMA
    assert report["development_set"]["num_sequences"] == 5
    assert report["r88_live_llm_pilot_available"] is False

    b0 = report["baseline_scores"]["B0_memoryless_replay"]
    bstar = report["baseline_scores"]["Bstar_oracle_memory"]

    assert b0["safety_passed"] is True
    assert b0["repeated_failure_rate"] == 1.0
    assert b0["horizon_reward_mean"] == 0.0

    assert bstar["safety_passed"] is True
    assert bstar["repeated_failure_rate"] == 0.0
    assert bstar["horizon_reward_mean"] > 0.8


def test_live_llm_pilot_row(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=1,
        r88_score_report_path=r88_path,
    )

    assert report["r88_live_llm_pilot_available"] is True
    assert len(report["chapter6_table"]) == 3

    pilot_rows = [
        row
        for row in report["chapter6_table"]
        if row["system_id"] == "mnemosyne_live_llm_r88_pilot"
    ]
    assert len(pilot_rows) == 1
    assert pilot_rows[0]["horizon_reward_mean"] == 0.90125
    assert pilot_rows[0]["grounded_admission_rate"] == 0.725


def test_render_markdown_contains_claim_boundary(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=1,
        r88_score_report_path=r88_path,
    )
    markdown = module.render_markdown(report)

    assert "Claim Boundary" in markdown
    assert "Chapter 6 Deterministic + Pilot Table" in markdown
    assert "Mnemosyne live-LLM pilot" in markdown
    assert "confirmatory-scale evidence" in markdown
