from __future__ import annotations

import json

from analysis.realm_tier6 import dynamic_closure_ledger as module


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    path.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )


def sample_r99_report():
    return {
        "schema": "realm_tier6_mnemosyne_dynamic_disruption_score_report_v0",
        "claim_boundary": "bounded dynamic pilot score",
        "official_scorer_invoked": True,
        "num_events": 40,
        "dynamic_summary": {
            "dynamic_admit_count": 24,
            "dynamic_reject_count": 16,
            "dynamic_observe_count": 0,
            "dynamic_safe_rejection_count": 4,
        },
        "overall_score": {
            "safety_passed": True,
            "repeated_failure_rate": 0.0,
            "horizon_reward_mean": 0.925,
            "grounded_admission_rate": 0.6,
            "time_to_correction_mean_observed": 0.725,
            "time_to_correction_observed_count": 40,
            "time_to_correction_censored_count": 0,
        },
    }


def sample_r98_event(outcome, decision):
    return {
        "sequence_id": "T6-DYN-jobshop-e7-0001",
        "episode_id": 1,
        "pack_name": "gpt",
        "failure_signature": "machine_unavailable.M2_after_commit",
        "dynamic_phase": "mid_execution",
        "admission_decision": decision,
        "dynamic_outcome": outcome,
        "admission_reasons": ["passed_admission_guards"]
        if decision == "admit"
        else ["committed_operation_touched:J1-O1"],
        "time_to_correction": 1,
        "safe_rejection": outcome == "safe_rejection",
        "episode": {
            "committed_operations": [
                {"operation_id": "J1-O1"},
            ],
        },
        "response": {
            "affected_steps": ["J4-O2"],
            "repair_summary": "Repair one uncommitted operation.",
            "preserve_evidence": True,
            "rollback_scope": "local",
        },
    }


def test_build_closure_ledger_marks_bounded_dynamic_closure(tmp_path) -> None:
    r99_report = tmp_path / "r99.json"
    r99_events = tmp_path / "r99.jsonl"
    r98_events = tmp_path / "r98.jsonl"

    write_json(r99_report, sample_r99_report())
    write_jsonl(r99_events, [])
    write_jsonl(
        r98_events,
        [
            sample_r98_event("admitted_repair", "admit"),
            sample_r98_event("safe_rejection", "reject"),
            sample_r98_event("rejected_other", "reject"),
        ],
    )

    ledger = module.build_closure_ledger(
        r99_score_report=r99_report,
        r99_events_path=r99_events,
        r98_events_path=r98_events,
    )

    assert ledger["schema"] == module.SCHEMA
    assert ledger["bounded_dynamic_closure"] is True
    assert ledger["dynamic_summary"]["dynamic_admit_count"] == 24
    assert len(ledger["case_studies"]) == 3


def test_select_case_studies_prefers_r98_detail() -> None:
    cases = module.select_case_studies(
        r98_events=[
            sample_r98_event("admitted_repair", "admit"),
            sample_r98_event("safe_rejection", "reject"),
        ],
        r99_events=[],
    )

    assert cases[0]["case_type"] == "admitted_local_repair"
    assert cases[0]["committed_operations"] == ["J1-O1"]
    assert cases[1]["case_type"] == "safe_rejection"


def test_render_ledger_markdown_has_claim_boundary() -> None:
    ledger = {
        "claim_boundary": "bounded claim only",
        "bounded_dynamic_closure": True,
        "dynamic_summary": {
            "official_scorer_invoked": True,
            "num_events": 40,
            "safety_passed": True,
            "dynamic_admit_count": 24,
            "dynamic_reject_count": 16,
            "dynamic_observe_count": 0,
            "dynamic_safe_rejection_count": 4,
            "repeated_failure_rate": 0.0,
            "horizon_reward_mean": 0.925,
            "grounded_admission_rate": 0.6,
            "time_to_correction_mean_observed": 0.725,
            "time_to_correction_observed_count": 40,
            "time_to_correction_censored_count": 0,
        },
        "evidence_items": module.build_evidence_items(
            {"claim_boundary": "bounded dynamic pilot score"}
        ),
        "claims_supported": ["bounded dynamic live-repair loop exists"],
        "claims_not_supported": ["repair optimality"],
        "part_ii_bridge": ["iterative replanning"],
    }

    text = module.render_ledger_markdown(ledger)

    assert "R100 Dynamic Closure Ledger" in text
    assert "repair loop remained safe and feasible" in text
    assert "It does not mean the selected repair was optimal" in text
