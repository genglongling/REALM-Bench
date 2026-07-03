from __future__ import annotations

from analysis.realm_tier6 import mnemosyne_live_llm_ch6_package as module


def sample_score_report() -> dict:
    return {
        "schema": "realm_tier6_mnemosyne_live_llm_score_report_v0",
        "sequence_id": "T6-7e17ef0cc5f3",
        "config_id": "E7",
        "condition_label": "full_crt_stack",
        "official_scorer_invoked": True,
        "score_scope": "mnemosyne_live_llm_handoff_derived_events",
        "num_events": 4,
        "overall_score": {
            "safety_passed": True,
            "repeated_failure_rate": 0.0,
            "horizon_reward_mean": 0.875,
            "grounded_admission_rate": 0.75,
            "time_to_correction_observed_count": 0,
            "time_to_correction_censored_count": 4,
            "safety_counts": {
                "invalid_commit_count": 0,
                "evidence_destroying_repair_count": 0,
                "orphaned_dependent_count": 0,
            },
            "bracket": {
                "position_repeated_failure_rate": "above_B0",
                "position_horizon_reward": "near_Bstar",
            },
        },
        "pack_scores": {
            "claude": {
                "num_events": 1,
                "safety_passed": True,
                "safety_counts": {
                    "invalid_commit_count": 0,
                    "evidence_destroying_repair_count": 0,
                    "orphaned_dependent_count": 0,
                },
                "repeated_failure_rate": 0.0,
                "horizon_reward_mean": 1.0,
                "grounded_admission_rate": 1.0,
            },
            "gpt": {
                "num_events": 1,
                "safety_passed": True,
                "safety_counts": {
                    "invalid_commit_count": 0,
                    "evidence_destroying_repair_count": 0,
                    "orphaned_dependent_count": 0,
                },
                "repeated_failure_rate": 0.0,
                "horizon_reward_mean": 0.55,
                "grounded_admission_rate": 0.0,
            },
        },
    }


def sample_import_report() -> dict:
    return {
        "schema": "realm_tier6_mnemosyne_live_llm_import_report_v0",
        "num_cases": 4,
        "num_validation_passed": 4,
        "num_validation_failed": 0,
        "all_cases_valid": True,
    }


def sample_sources() -> dict:
    return {
        "r87_import_report": sample_import_report(),
        "r88_score_report": sample_score_report(),
        "mnemosyne_reports": {
            "r835b_comparison": {"schema": "comparison", "num_records": 40},
            "r835c_kernel_trace": {
                "schema": "trace",
                "num_records": 40,
                "num_admitted": 34,
                "num_rejected": 6,
                "kernel_method_counts": {"accept_via_kernel": 29},
            },
            "r84_runtime_evaluator": {
                "schema": "runtime",
                "num_records": 40,
                "num_failed": 0,
                "global_passed": True,
            },
            "r85_score_bridge": {
                "schema": "bridge",
                "num_records": 40,
                "official_realm_score": False,
            },
            "r86_scorer_handoff": {
                "schema": "handoff",
                "sequence_id": "T6-7e17ef0cc5f3",
                "config_id": "E7",
                "cases": [{}, {}, {}, {}],
            },
        },
        "source_paths": {
            "r87_import_report": "import.json",
            "r88_score_report": "score.json",
        },
    }


def test_build_overall_summary() -> None:
    summary = module.build_overall_summary(sample_score_report())

    assert summary["official_scorer_invoked"] is True
    assert summary["num_events"] == 4
    assert summary["safety_passed"] is True
    assert summary["horizon_reward_mean"] == 0.875
    assert summary["grounded_admission_rate"] == 0.75


def test_build_chapter_table() -> None:
    rows = module.build_chapter_table(sample_score_report())

    assert len(rows) == 2
    assert rows[0]["display_name"] == "Claude"
    assert rows[1]["display_name"] == "GPT"
    assert rows[0]["horizon_reward_mean"] == 1.0


def test_extract_pipeline_evidence() -> None:
    evidence = module.extract_pipeline_evidence(sample_sources())

    assert evidence["runtime_evaluator"]["summary"]["global_passed"] is True
    assert evidence["scorer_handoff"]["summary"]["num_cases"] == 4
    assert evidence["realm_import"]["summary"]["all_cases_valid"] is True
    assert evidence["realm_scoring"]["summary"]["official_scorer_invoked"] is True


def test_build_package_sets_claim_boundary() -> None:
    package = module.build_package(sample_sources())

    assert package["schema"] == module.SCHEMA
    assert package["chapter_use"]["ready_for_chapter_6_pilot_table"] is True
    assert package["chapter_use"]["ready_for_confirmatory_claims"] is False
    assert "final confirmatory Chapter 6 evidence" in package["disallowed_claims"]


def test_render_markdown_contains_chapter_insert() -> None:
    package = module.build_package(sample_sources())
    markdown = module.render_markdown(package)

    assert "Chapter 6 Pilot Results Table" in markdown
    assert "Chapter 6 Insert Draft" in markdown
    assert "pilot integration evidence" in markdown
