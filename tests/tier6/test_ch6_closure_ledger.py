from __future__ import annotations

from analysis.realm_tier6 import ch6_closure_ledger as module


def sample_sources() -> dict:
    return {
        "R89_ch6_package": {
            "chapter_use": {
                "ready_for_chapter_6_pilot_table": True,
                "ready_for_confirmatory_claims": False,
            },
            "overall_summary": {
                "num_events": 40,
                "safety_passed": True,
                "horizon_reward_mean": 0.90125,
                "grounded_admission_rate": 0.725,
            },
        },
        "R90_full_deterministic": {
            "development_set": {
                "num_sequences": 15,
                "num_episodes": 150,
                "families": [
                    "jobshop_breakdown",
                    "ride_or_routing_disruption",
                    "wedding_recovery",
                ],
            },
            "chapter6_table": [
                {"system_id": "B0_memoryless_replay"},
                {"system_id": "Bstar_oracle_memory"},
                {"system_id": "mnemosyne_live_llm_r88_pilot"},
            ],
        },
        "R91_crt_ablation": {
            "available_configs": ["E0", "E2", "E3", "E7"],
            "missing_configs": [],
            "all_required_configs_available": True,
            "e7_summary": {
                "repeated_failure_rate": 0.0,
                "horizon_reward_mean": 0.8423076923076923,
            },
        },
        "R92_family_stratified": {
            "families": [
                "jobshop_breakdown",
                "ride_or_routing_disruption",
                "wedding_recovery",
            ],
            "r88_live_llm_pilot_available": True,
            "num_family_table_rows": 7,
            "live_pilot_family": "jobshop_breakdown",
        },
        "R93_expanded_live_llm_plan": {
            "chapter6_status": {
                "bounded_pilot_ready": True,
                "family_generalized_live_llm_ready": False,
                "additional_cases_needed_for_three_family_live_pilot": 80,
            },
            "matrix_summary": {
                "total_cases": 120,
                "existing_r88_collected": 40,
                "planned_not_collected": 80,
            },
        },
    }


def test_extract_summaries() -> None:
    sources = sample_sources()

    r89 = module.extract_r89_summary(sources["R89_ch6_package"])
    r90 = module.extract_r90_summary(sources["R90_full_deterministic"])
    r93 = module.extract_r93_summary(sources["R93_expanded_live_llm_plan"])

    assert r89["horizon_reward_mean"] == 0.90125
    assert r90["has_b0"] is True
    assert r90["has_bstar"] is True
    assert r93["additional_cases_needed_for_three_family_live_pilot"] == 80


def test_build_closure_checks_all_pass() -> None:
    sources = sample_sources()
    summaries = {
        "R89_ch6_package": module.extract_r89_summary(sources["R89_ch6_package"]),
        "R90_full_deterministic": module.extract_r90_summary(
            sources["R90_full_deterministic"]
        ),
        "R91_crt_ablation": module.extract_r91_summary(sources["R91_crt_ablation"]),
        "R92_family_stratified": module.extract_r92_summary(
            sources["R92_family_stratified"]
        ),
        "R93_expanded_live_llm_plan": module.extract_r93_summary(
            sources["R93_expanded_live_llm_plan"]
        ),
    }

    checks = module.build_closure_checks(summaries)

    assert len(checks) == 9
    assert all(check["passed"] for check in checks)


def test_build_ledger_closes_chapter() -> None:
    ledger = module.build_ledger(
        sample_sources(),
        {key: f"{key}.json" for key in sample_sources()},
    )

    assert ledger["schema"] == module.SCHEMA
    assert ledger["chapter6_closed_for_book"] is True
    assert ledger["closure_mode"] == "bounded_pilot_plus_deterministic_evidence"
    assert "confirmatory-scale benchmark proof" in ledger["chapter6_disallowed_claims"]


def test_render_markdown_contains_final_insert() -> None:
    ledger = module.build_ledger(
        sample_sources(),
        {key: f"{key}.json" for key in sample_sources()},
    )
    markdown = module.render_markdown(ledger)

    assert "R94 Chapter 6 Closure Ledger" in markdown
    assert "Final Chapter 6 Insert Draft" in markdown
    assert "bounded pilot-plus-deterministic evidence" in markdown
    assert "80" in markdown
