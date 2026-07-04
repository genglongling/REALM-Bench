#!/usr/bin/env python3
"""R99 REALM-side dynamic disruption scoring.

This module consumes Mnemosyne R98 dynamic replay events, converts them into
Tier-6 schema-valid REALM events, validates the trace, and invokes the public
Tier-6 scorer.

Claim boundary:
R99 is the first REALM-side official scorer invocation for the dynamic
disruption pilot. It scores one bounded jobshop/E7 dynamic pilot, not a
family-generalized or confirmatory-scale benchmark.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from evaluation.tier6.scorer import score_trace
from evaluation.tier6.schemas import validate_trace


SCHEMA = "realm_tier6_mnemosyne_dynamic_disruption_score_report_v0"

DEFAULT_MNEMOSYNE_DYNAMIC_EVENTS = (
    "/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/"
    "results/realm_tier6_dynamic_disruption_replay/jobshop_e7_dynamic_pilot/"
    "dynamic_replay_events.jsonl"
)

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/dynamic_disruption_official_score"

FIXTURE_TIMESTAMP_UTC = "2026-07-02T00:00:00Z"


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"expected JSON object at {path}:{line_number}")
        rows.append(value)
    return rows


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def realm_event_type(dynamic_event: Dict[str, Any]) -> str:
    decision = dynamic_event.get("admission_decision")
    if decision == "admit":
        return "repair"
    if decision == "observe":
        return "observe"
    return "reject"


def failure_signature(dynamic_event: Dict[str, Any]) -> str:
    signature = str(dynamic_event.get("failure_signature") or "")
    if dynamic_event.get("admission_decision") == "reject":
        return signature or "mnemosyne_dynamic_disruption.screened_before_commit"
    return signature


def delta_for_event(dynamic_event: Dict[str, Any]) -> str:
    outcome = dynamic_event.get("dynamic_outcome")
    if outcome == "admitted_repair":
        return "corrected"
    if outcome == "safe_rejection":
        return "screened_before_commit"
    if outcome == "observation_requested":
        return "observation_requested"
    if outcome == "rejected_other":
        return "rejected_before_commit"
    return str(outcome or "")


def constraint_violations(dynamic_event: Dict[str, Any]) -> List[str]:
    if dynamic_event.get("admitted"):
        return []
    if dynamic_event.get("safe_rejection"):
        return []
    if dynamic_event.get("observed"):
        return []

    reasons = dynamic_event.get("admission_reasons", [])
    if not isinstance(reasons, list):
        return ["mnemosyne_dynamic_disruption.rejected_other"]

    return [f"mnemosyne_dynamic_disruption.{str(reason)}" for reason in reasons]


def repair_radius(dynamic_event: Dict[str, Any]) -> int:
    if dynamic_event.get("admission_decision") == "admit":
        return 1
    return 0


def evidence_preserved(dynamic_event: Dict[str, Any]) -> bool:
    safety = dynamic_event.get("safety", {})
    return not bool(safety.get("evidence_destroying_repair_count", 0))


def time_to_correction(dynamic_event: Dict[str, Any]) -> int | None:
    value = dynamic_event.get("time_to_correction")
    if isinstance(value, int) and value >= 0:
        return value
    return None


def horizon_reward(dynamic_event: Dict[str, Any]) -> float:
    value = dynamic_event.get("horizon_reward_proxy")
    if isinstance(value, (int, float)):
        return float(value)
    return 0.0


def grounded_admission(dynamic_event: Dict[str, Any]) -> bool:
    return dynamic_event.get("admission_decision") == "admit"


def make_tier6_event(dynamic_event: Dict[str, Any], *, seed: int) -> Dict[str, Any]:
    ttc = time_to_correction(dynamic_event)
    safety = dynamic_event.get("safety", {})

    event = {
        "sequence_id": f"{dynamic_event['sequence_id']}::{dynamic_event['pack_name']}",
        "base_sequence_id": dynamic_event["sequence_id"],
        "episode_id": int(dynamic_event["episode_id"]),
        "seed": seed,
        "t": FIXTURE_TIMESTAMP_UTC,
        "event": realm_event_type(dynamic_event),
        "proposal_id": str(dynamic_event["prompt_id"]),
        "failure_signature": failure_signature(dynamic_event),
        "predicted_outcome": str(dynamic_event.get("action", "")),
        "observed_outcome": str(dynamic_event.get("dynamic_outcome", "")),
        "delta": delta_for_event(dynamic_event),
        "constraint_violations": constraint_violations(dynamic_event),
        "repair": {
            "radius": repair_radius(dynamic_event),
            "evidence_preserved": evidence_preserved(dynamic_event),
        },
        "cost": {
            "tokens_in": 0,
            "tokens_out": 0,
            "wallclock_ms": 0,
        },
        "time_to_correction": ttc,
        "time_to_correction_censored": ttc is None,
        "invalid_commit_count": int(safety.get("invalid_commit_count", 0)),
        "evidence_destroying_repair_count": int(
            safety.get("evidence_destroying_repair_count", 0)
        ),
        "orphaned_dependent_count": int(safety.get("orphaned_dependent_count", 0)),
        "is_control_sequence": False,
        "horizon_reward": horizon_reward(dynamic_event),
        "grounded_admission": grounded_admission(dynamic_event),
        "pack_name": dynamic_event["pack_name"],
        "base_instance_id": dynamic_event.get("base_instance_id"),
        "family": dynamic_event.get("family"),
        "dynamic_phase": dynamic_event.get("dynamic_phase"),
        "admission_decision": dynamic_event.get("admission_decision"),
        "admission_reasons": dynamic_event.get("admission_reasons", []),
        "safe_rejection": dynamic_event.get("safe_rejection"),
        "mnemosyne_dynamic_outcome": dynamic_event.get("dynamic_outcome"),
        "claim_status": "dynamic_disruption_pilot_scoring_only",
    }

    if event["event"] == "reject":
        event["rejection_reason_code"] = str(
            dynamic_event.get("dynamic_outcome", "rejected_before_commit")
        )

    return event


def build_events(dynamic_events: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    dynamic_events = list(dynamic_events)
    pack_names = sorted({str(event["pack_name"]) for event in dynamic_events})
    seed_by_pack = {
        pack_name: 99000 + index
        for index, pack_name in enumerate(pack_names)
    }

    events = [
        make_tier6_event(event, seed=seed_by_pack[str(event["pack_name"])])
        for event in dynamic_events
    ]

    events = sorted(events, key=lambda item: (item["pack_name"], item["episode_id"]))
    validate_trace(events)
    return events


def summarize_pack_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_pack: Dict[str, List[Dict[str, Any]]] = {}
    for event in events:
        by_pack.setdefault(str(event["pack_name"]), []).append(event)

    summaries: Dict[str, Any] = {}
    for pack_name, pack_events in by_pack.items():
        score = score_trace(pack_events)
        summaries[pack_name] = {
            "num_events": score["num_events"],
            "safety_passed": score["safety_passed"],
            "safety_counts": score["safety_counts"],
            "repeated_failure_rate": score["repeated_failure_rate"],
            "horizon_reward_mean": score["horizon_reward_mean"],
            "grounded_admission_rate": score["grounded_admission_rate"],
            "time_to_correction_mean_observed": score[
                "time_to_correction_mean_observed"
            ],
            "time_to_correction_observed_count": score[
                "time_to_correction_observed_count"
            ],
            "time_to_correction_censored_count": score[
                "time_to_correction_censored_count"
            ],
            "bracket": score["bracket"],
        }

    return summaries


def dynamic_summary(dynamic_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    decisions: Dict[str, int] = {}
    outcomes: Dict[str, int] = {}

    for event in dynamic_events:
        decision = str(event.get("admission_decision"))
        outcome = str(event.get("dynamic_outcome"))
        decisions[decision] = decisions.get(decision, 0) + 1
        outcomes[outcome] = outcomes.get(outcome, 0) + 1

    return {
        "decisions": decisions,
        "outcomes": outcomes,
        "dynamic_admit_count": decisions.get("admit", 0),
        "dynamic_reject_count": decisions.get("reject", 0),
        "dynamic_observe_count": decisions.get("observe", 0),
        "dynamic_safe_rejection_count": outcomes.get("safe_rejection", 0),
    }


def build_score_report(dynamic_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    events = build_events(dynamic_events)
    overall_score = score_trace(events)
    pack_scores = summarize_pack_events(events)

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "REALM Tier-6 public scorer invoked on Mnemosyne R98 dynamic "
            "disruption replay events. This is a bounded dynamic jobshop/E7 "
            "pilot score, not a family-generalized or confirmatory-scale result."
        ),
        "official_scorer_invoked": True,
        "score_scope": "mnemosyne_dynamic_disruption_replay_events",
        "num_events": len(events),
        "sequence_id": dynamic_events[0].get("sequence_id") if dynamic_events else None,
        "config_id": dynamic_events[0].get("config_id") if dynamic_events else None,
        "condition_label": (
            dynamic_events[0].get("condition_label") if dynamic_events else None
        ),
        "dynamic_summary": dynamic_summary(dynamic_events),
        "overall_score": overall_score,
        "pack_scores": pack_scores,
        "events": events,
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []
    overall = report["overall_score"]
    dyn = report["dynamic_summary"]

    lines.append("# R99 REALM Tier-6 Dynamic Disruption Scoring Report")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Pilot")
    lines.append("")
    lines.append(f"- Sequence: `{report['sequence_id']}`")
    lines.append(f"- Config: `{report['config_id']}`")
    lines.append(f"- Condition label: `{report['condition_label']}`")
    lines.append(f"- Official scorer invoked: `{report['official_scorer_invoked']}`")
    lines.append(f"- Score scope: `{report['score_scope']}`")
    lines.append(f"- Events: `{report['num_events']}`")
    lines.append("")
    lines.append("## Dynamic Replay Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Dynamic admits | {dyn['dynamic_admit_count']} |")
    lines.append(f"| Dynamic rejects | {dyn['dynamic_reject_count']} |")
    lines.append(f"| Dynamic observes | {dyn['dynamic_observe_count']} |")
    lines.append(f"| Dynamic safe rejections | {dyn['dynamic_safe_rejection_count']} |")
    lines.append("")
    lines.append("## Overall Tier-6 Score")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Safety passed | {overall['safety_passed']} |")
    lines.append(f"| Repeated failure rate | {overall['repeated_failure_rate']} |")
    lines.append(f"| Horizon reward mean | {overall['horizon_reward_mean']} |")
    lines.append(f"| Grounded admission rate | {overall['grounded_admission_rate']} |")
    lines.append(
        f"| TTC observed mean | {overall['time_to_correction_mean_observed']} |"
    )
    lines.append(
        f"| TTC observed count | {overall['time_to_correction_observed_count']} |"
    )
    lines.append(
        f"| TTC censored count | {overall['time_to_correction_censored_count']} |"
    )
    lines.append("")
    lines.append("## Pack Scores")
    lines.append("")
    lines.append(
        "| Pack | Events | Safety | RFR | Horizon reward | Grounded admission | TTC mean |"
    )
    lines.append("|---|---:|---|---:|---:|---:|---:|")
    for pack_name, score in sorted(report["pack_scores"].items()):
        lines.append(
            f"| {pack_name} | {score['num_events']} | {score['safety_passed']} | "
            f"{score['repeated_failure_rate']} | {score['horizon_reward_mean']} | "
            f"{score['grounded_admission_rate']} | "
            f"{score['time_to_correction_mean_observed']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "R99 is the REALM-side official scoring step for the bounded dynamic "
        "disruption pilot. It consumes Mnemosyne R98 replay events, validates "
        "Tier-6 trace schema, invokes the public Tier-6 scorer, and reports "
        "safety, repeated-failure, horizon-reward, grounded-admission, and "
        "time-to-correction metrics."
    )
    lines.append("")
    return "\n".join(lines)


def write_outputs(report: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    events_path = output_dir / "dynamic_disruption_events.jsonl"
    with events_path.open("w", encoding="utf-8") as f:
        for event in report["events"]:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    write_json(output_dir / "dynamic_disruption_score_report.json", report)
    (output_dir / "dynamic_disruption_score_report.md").write_text(
        render_markdown(report),
        encoding="utf-8",
    )

    import_report = {
        "schema": "realm_tier6_mnemosyne_dynamic_disruption_import_report_v0",
        "source_events": report["num_events"],
        "converted_events": len(report["events"]),
        "validation_passed": True,
        "official_scorer_required": True,
        "official_scorer_invoked": report["official_scorer_invoked"],
        "score_report": str(output_dir / "dynamic_disruption_score_report.json"),
        "events_path": str(events_path),
    }
    write_json(output_dir / "dynamic_disruption_import_report.json", import_report)


def cmd_score(args: argparse.Namespace) -> None:
    dynamic_events = read_jsonl(Path(args.input_events))
    report = build_score_report(dynamic_events)
    write_outputs(report, Path(args.output_dir))

    overall = report["overall_score"]
    dyn = report["dynamic_summary"]

    print(
        json.dumps(
            {
                "output_dir": args.output_dir,
                "num_events": report["num_events"],
                "official_scorer_invoked": report["official_scorer_invoked"],
                "safety_passed": overall["safety_passed"],
                "repeated_failure_rate": overall["repeated_failure_rate"],
                "horizon_reward_mean": overall["horizon_reward_mean"],
                "grounded_admission_rate": overall["grounded_admission_rate"],
                "time_to_correction_mean_observed": overall[
                    "time_to_correction_mean_observed"
                ],
                "dynamic_admit_count": dyn["dynamic_admit_count"],
                "dynamic_reject_count": dyn["dynamic_reject_count"],
                "dynamic_safe_rejection_count": dyn[
                    "dynamic_safe_rejection_count"
                ],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="R99 dynamic disruption REALM score")
    sub = parser.add_subparsers(dest="command", required=True)

    score_cmd = sub.add_parser("score", help="score Mnemosyne dynamic disruption replay events")
    score_cmd.add_argument("--input-events", default=DEFAULT_MNEMOSYNE_DYNAMIC_EVENTS)
    score_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    score_cmd.set_defaults(func=cmd_score)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
