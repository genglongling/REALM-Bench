from __future__ import annotations

from evaluation.tier6 import mnemosyne_dynamic_disruption_score as module


def dynamic_event(decision: str = "admit", outcome: str = "admitted_repair") -> dict:
    return {
        "schema": "realm_tier6_dynamic_disruption_event_v0",
        "sequence_id": "T6-DYN-jobshop-e7-0001",
        "episode_id": 1,
        "family": "jobshop_breakdown",
        "base_instance_id": "jobshop_breakdown:datasets/J4/custom/j4_custom_001.json",
        "config_id": "E7",
        "condition_label": "full_crt_stack",
        "pack_name": "gpt",
        "prompt_id": "prompt-1",
        "dynamic_phase": "mid_execution",
        "failure_signature": "machine_unavailable.M2_after_commit",
        "action": "repair",
        "admission_decision": decision,
        "admission_reasons": ["passed_admission_guards"],
        "dynamic_outcome": outcome,
        "admitted": decision == "admit",
        "rejected": decision == "reject",
        "observed": decision == "observe",
        "safe_rejection": outcome == "safe_rejection",
        "time_to_correction": 1,
        "horizon_reward_proxy": 1.0,
        "safety": {
            "invalid_commit_count": 0,
            "evidence_destroying_repair_count": 0,
            "orphaned_dependent_count": 0,
        },
        "response": {},
        "episode": {},
    }


def test_make_tier6_event_admitted_repair_validates() -> None:
    event = module.make_tier6_event(dynamic_event(), seed=99000)

    assert event["event"] == "repair"
    assert event["horizon_reward"] == 1.0
    assert event["grounded_admission"] is True
    assert event["time_to_correction"] == 1
    assert event["time_to_correction_censored"] is False


def test_make_tier6_event_reject_has_rejection_reason() -> None:
    event = module.make_tier6_event(
        dynamic_event(decision="reject", outcome="safe_rejection"),
        seed=99000,
    )

    assert event["event"] == "reject"
    assert event["grounded_admission"] is False
    assert event["rejection_reason_code"] == "safe_rejection"


def test_build_events_invokes_schema_validation() -> None:
    events = module.build_events([dynamic_event()])

    assert len(events) == 1
    assert events[0]["event"] == "repair"


def test_build_score_report_invokes_public_scorer() -> None:
    report = module.build_score_report(
        [
            dynamic_event(decision="admit", outcome="admitted_repair"),
            dynamic_event(decision="reject", outcome="safe_rejection"),
        ]
    )

    assert report["official_scorer_invoked"] is True
    assert report["num_events"] == 2
    assert report["overall_score"]["safety_passed"] is True
    assert report["dynamic_summary"]["dynamic_admit_count"] == 1
    assert report["dynamic_summary"]["dynamic_reject_count"] == 1
    assert report["dynamic_summary"]["dynamic_safe_rejection_count"] == 1


def test_render_markdown_contains_dynamic_score() -> None:
    report = module.build_score_report([dynamic_event()])
    text = module.render_markdown(report)

    assert "R99 REALM Tier-6 Dynamic Disruption Scoring Report" in text
    assert "Official scorer invoked" in text
    assert "Overall Tier-6 Score" in text
