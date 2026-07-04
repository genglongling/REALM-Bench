#!/usr/bin/env python3
"""R100 dynamic closure ledger for Chapter 6.

R100 combines the static and dynamic evidence trail:

- R89 static live-LLM pilot package
- R90 deterministic baselines
- R91 CRT ablation
- R92 family stratification
- R93 expansion gate
- R96 dynamic prompt pack
- R97 dynamic response collection
- R98 Mnemosyne dynamic replay
- R99 REALM-Bench dynamic score

It also extracts qualitative case studies:

- one admitted local repair
- one safe rejection
- optionally one non-safe rejection / limitation case

Claim boundary:
R100 closes bounded Part I dynamic feasibility and safety evidence. It does not
claim optimality, family-generalized dynamic behavior, production CTL-domain
realization, AGI, wisdom, or autonomous scientific reasoning.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SCHEMA = "realm_tier6_dynamic_closure_ledger_v0"

DEFAULT_R99_SCORE_REPORT = (
    "runs/realm_tier6/dynamic_disruption_official_score/"
    "dynamic_disruption_score_report.json"
)

DEFAULT_R99_EVENTS = (
    "runs/realm_tier6/dynamic_disruption_official_score/"
    "dynamic_disruption_events.jsonl"
)

DEFAULT_R98_EVENTS = (
    "/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/"
    "results/realm_tier6_dynamic_disruption_replay/jobshop_e7_dynamic_pilot/"
    "dynamic_replay_events.jsonl"
)

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/dynamic_closure_ledger"

OPTIONAL_EVIDENCE_PATHS = {
    "R89_static_live_llm_package": [
        "runs/realm_tier6/mnemosyne_live_llm_ch6_package/"
        "mnemosyne_live_llm_ch6_package.json",
        "runs/realm_tier6/ch6_mnemosyne_live_llm_package/"
        "mnemosyne_live_llm_ch6_package.json",
    ],
    "R90_deterministic_baselines": [
        "runs/realm_tier6/full_deterministic_report/full_deterministic_report.json",
    ],
    "R91_crt_ablation": [
        "runs/realm_tier6/crt_ablation_report/crt_ablation_report.json",
    ],
    "R92_family_stratification": [
        "runs/realm_tier6/family_stratified_report/family_stratified_report.json",
    ],
    "R93_expansion_gate": [
        "runs/realm_tier6/expanded_live_llm_pilot_plan/"
        "expanded_live_llm_pilot_plan.json",
    ],
}


def read_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def read_json_optional(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    return read_json(path)


def read_jsonl_optional(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

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


def first_existing(paths: Iterable[str]) -> Optional[Path]:
    for item in paths:
        path = Path(item)
        if path.exists():
            return path
    return None


def compact_optional_report(name: str, paths: List[str]) -> Dict[str, Any]:
    path = first_existing(paths)
    if path is None:
        return {
            "name": name,
            "present": False,
            "path": None,
            "summary": "not found in local checkout",
        }

    report = read_json(path)
    summary: Dict[str, Any] = {}

    for key in [
        "schema",
        "ready_for_chapter_6_pilot_table",
        "ready_for_confirmatory_claims",
        "official_scorer_invoked",
        "num_events",
        "num_sequences",
        "num_episodes",
    ]:
        if key in report:
            summary[key] = report[key]

    if "overall_summary" in report:
        summary["overall_summary"] = report["overall_summary"]
    if "overall_score" in report:
        score = report["overall_score"]
        summary["overall_score"] = {
            "num_events": score.get("num_events"),
            "safety_passed": score.get("safety_passed"),
            "repeated_failure_rate": score.get("repeated_failure_rate"),
            "horizon_reward_mean": score.get("horizon_reward_mean"),
            "grounded_admission_rate": score.get("grounded_admission_rate"),
        }

    return {
        "name": name,
        "present": True,
        "path": str(path),
        "summary": summary,
    }


def operation_ids(items: Any) -> List[str]:
    if not isinstance(items, list):
        return []
    values: List[str] = []
    for item in items:
        if isinstance(item, dict) and "operation_id" in item:
            values.append(str(item["operation_id"]))
    return values


def case_from_r98_event(event: Dict[str, Any], case_type: str) -> Dict[str, Any]:
    episode = event.get("episode", {})
    response = event.get("response", {})

    return {
        "case_type": case_type,
        "pack_name": event.get("pack_name"),
        "episode_id": event.get("episode_id"),
        "failure_signature": event.get("failure_signature"),
        "dynamic_phase": event.get("dynamic_phase"),
        "admission_decision": event.get("admission_decision"),
        "dynamic_outcome": event.get("dynamic_outcome"),
        "admission_reasons": event.get("admission_reasons", []),
        "committed_operations": operation_ids(episode.get("committed_operations")),
        "affected_steps": response.get("affected_steps", []),
        "repair_summary": response.get("repair_summary", ""),
        "preserve_evidence": response.get("preserve_evidence"),
        "rollback_scope": response.get("rollback_scope"),
        "time_to_correction": event.get("time_to_correction"),
        "interpretation": interpretation_for_case(case_type, event),
    }


def case_from_scored_event(event: Dict[str, Any], case_type: str) -> Dict[str, Any]:
    return {
        "case_type": case_type,
        "pack_name": event.get("pack_name"),
        "episode_id": event.get("episode_id"),
        "failure_signature": event.get("failure_signature"),
        "dynamic_phase": event.get("dynamic_phase"),
        "admission_decision": event.get("admission_decision"),
        "dynamic_outcome": event.get("mnemosyne_dynamic_outcome"),
        "admission_reasons": event.get("admission_reasons", []),
        "committed_operations": [],
        "affected_steps": [],
        "repair_summary": event.get("predicted_outcome", ""),
        "preserve_evidence": event.get("repair", {}).get("evidence_preserved"),
        "rollback_scope": None,
        "time_to_correction": event.get("time_to_correction"),
        "interpretation": interpretation_for_case(case_type, event),
    }


def interpretation_for_case(case_type: str, event: Dict[str, Any]) -> str:
    if case_type == "admitted_local_repair":
        return (
            "The proposal passed admission because it remained local, preserved "
            "evidence, and did not rewrite committed operations."
        )
    if case_type == "safe_rejection":
        return (
            "The proposal did not enter execution. The rejection is a system-level "
            "safety success because the admission gate blocked an unsafe or "
            "unsupported repair before commit."
        )
    return (
        "This case illustrates a protective model-side rejection. The model "
        "recognized that global rollback would violate committed evidence and "
        "therefore rejected the rollback request before execution. R98 records "
        "this conservatively as rejected_other rather than safe_rejection because "
        "the rejection was requested by the model itself, not derived from an "
        "admission-guard violation. In Part II, such rejection reasons can feed "
        "iterative re-evaluation and replanning."
    )


def select_case_studies(
    *,
    r98_events: List[Dict[str, Any]],
    r99_events: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    source = r98_events if r98_events else r99_events
    if not source:
        return []

    def outcome(event: Dict[str, Any]) -> str:
        return str(event.get("dynamic_outcome") or event.get("mnemosyne_dynamic_outcome") or "")

    def decision(event: Dict[str, Any]) -> str:
        return str(event.get("admission_decision") or "")

    selected: List[Dict[str, Any]] = []

    admitted = next(
        (
            item for item in source
            if decision(item) == "admit" and outcome(item) == "admitted_repair"
        ),
        None,
    )
    if admitted is not None:
        selected.append(
            case_from_r98_event(admitted, "admitted_local_repair")
            if r98_events else case_from_scored_event(admitted, "admitted_local_repair")
        )

    safe = next(
        (
            item for item in source
            if outcome(item) == "safe_rejection" or item.get("safe_rejection") is True
        ),
        None,
    )
    if safe is not None:
        selected.append(
            case_from_r98_event(safe, "safe_rejection")
            if r98_events else case_from_scored_event(safe, "safe_rejection")
        )

    limitation = next(
        (
            item for item in source
            if decision(item) == "reject" and outcome(item) == "rejected_other"
        ),
        None,
    )
    if limitation is not None:
        selected.append(
            case_from_r98_event(limitation, "rejected_other_limitation")
            if r98_events else case_from_scored_event(limitation, "rejected_other_limitation")
        )

    return selected


def build_dynamic_summary(r99_report: Dict[str, Any]) -> Dict[str, Any]:
    overall = r99_report.get("overall_score", {})
    dyn = r99_report.get("dynamic_summary", {})

    return {
        "official_scorer_invoked": r99_report.get("official_scorer_invoked"),
        "num_events": r99_report.get("num_events"),
        "safety_passed": overall.get("safety_passed"),
        "repeated_failure_rate": overall.get("repeated_failure_rate"),
        "horizon_reward_mean": overall.get("horizon_reward_mean"),
        "grounded_admission_rate": overall.get("grounded_admission_rate"),
        "time_to_correction_mean_observed": overall.get(
            "time_to_correction_mean_observed"
        ),
        "time_to_correction_observed_count": overall.get(
            "time_to_correction_observed_count"
        ),
        "time_to_correction_censored_count": overall.get(
            "time_to_correction_censored_count"
        ),
        "dynamic_admit_count": dyn.get("dynamic_admit_count"),
        "dynamic_reject_count": dyn.get("dynamic_reject_count"),
        "dynamic_observe_count": dyn.get("dynamic_observe_count"),
        "dynamic_safe_rejection_count": dyn.get("dynamic_safe_rejection_count"),
    }


def build_evidence_items(r99_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = [
        {
            "id": "R89",
            "name": "static live-LLM pilot package",
            "role": "plan-entry live-LLM baseline evidence",
            "status": "static evidence layer",
            "claim_boundary": (
                "Supports bounded static pilot reporting, not dynamic repair closure."
            ),
        },
        {
            "id": "R90",
            "name": "deterministic baseline report",
            "role": "B0 and B* reference anchors",
            "status": "deterministic baseline layer",
            "claim_boundary": "Supports baseline bracketing, not live dynamic behavior.",
        },
        {
            "id": "R91",
            "name": "CRT ablation",
            "role": "condition-stack ablation over E0/E2/E3/E7",
            "status": "ablation evidence layer",
            "claim_boundary": "Supports condition sensitivity, not dynamic optimality.",
        },
        {
            "id": "R92",
            "name": "family stratification",
            "role": "family-level deterministic stratification",
            "status": "stratified evidence layer",
            "claim_boundary": "Supports family coverage context, not dynamic generalization.",
        },
        {
            "id": "R93",
            "name": "expansion gate",
            "role": "defines scale needed for broader confirmatory claims",
            "status": "claim-boundary guard",
            "claim_boundary": "Prevents overclaiming from pilot evidence.",
        },
        {
            "id": "R96",
            "name": "dynamic prompt pack",
            "role": "mid-execution disruption prompts",
            "status": "dynamic input generation",
            "claim_boundary": "Prompt generation only; no outcome claim.",
        },
        {
            "id": "R97",
            "name": "dynamic response collection",
            "role": "40 live-LLM dynamic repair proposals",
            "status": "response collection",
            "claim_boundary": "Schema-valid collection only; no admission or score claim.",
        },
        {
            "id": "R98",
            "name": "Mnemosyne dynamic admission replay",
            "role": "admit / reject / observe under evidence-preserving guards",
            "status": "Mnemosyne-side dynamic replay",
            "claim_boundary": "Replay and proxy metrics only; not REALM official score.",
        },
        {
            "id": "R99",
            "name": "REALM-Bench dynamic score",
            "role": "public Tier-6 scorer invocation over dynamic replay events",
            "status": "official dynamic pilot score",
            "claim_boundary": r99_report.get("claim_boundary"),
        },
    ]
    return items


def build_closure_ledger(
    *,
    r99_score_report: Path,
    r99_events_path: Path,
    r98_events_path: Path,
) -> Dict[str, Any]:
    r99_report = read_json(r99_score_report)
    r99_events = read_jsonl_optional(r99_events_path)
    r98_events = read_jsonl_optional(r98_events_path)

    optional_reports = [
        compact_optional_report(name, paths)
        for name, paths in OPTIONAL_EVIDENCE_PATHS.items()
    ]

    dynamic_summary = build_dynamic_summary(r99_report)
    case_studies = select_case_studies(
        r98_events=r98_events,
        r99_events=r99_events,
    )

    bounded_dynamic_closure = (
        dynamic_summary["official_scorer_invoked"] is True
        and dynamic_summary["num_events"] == 40
        and dynamic_summary["safety_passed"] is True
    )

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "R100 closes bounded Part I dynamic feasibility and safety evidence: "
            "live disruption, live proposal, admission-gated repair or rejection, "
            "evidence-preserving replay, and public Tier-6 scoring. It does not "
            "claim optimality, family-generalized dynamic behavior, production "
            "CTL-domain realization, AGI, wisdom, or autonomous scientific reasoning."
        ),
        "bounded_dynamic_closure": bounded_dynamic_closure,
        "dynamic_summary": dynamic_summary,
        "evidence_items": build_evidence_items(r99_report),
        "optional_local_reports": optional_reports,
        "case_studies": case_studies,
        "claims_supported": [
            "bounded dynamic live-repair loop exists",
            "unsafe or unsupported proposals can be rejected before commit",
            "accepted repairs preserve evidence under admission constraints",
            "dynamic events can be emitted as Tier-6-valid traces",
            "public REALM-Bench Tier-6 scorer was invoked for the dynamic pilot",
        ],
        "claims_not_supported": [
            "repair optimality",
            "family-generalized dynamic live-LLM behavior",
            "confirmatory-scale benchmark evidence",
            "API-automated live-LLM evaluation",
            "production CTL-domain StateView realization",
            "proof of AGI",
            "proof of wisdom",
            "proof of autonomous scientific reasoning",
        ],
        "part_ii_bridge": [
            "turn rejection reasons into iterative replanning feedback",
            "compare feasible repairs by regret, cost, delay, and horizon reward",
            "use multi-LLM critique or debate for repair revision",
            "study optimality after feasibility and safety are established",
        ],
    }


def render_case_studies(case_studies: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# R100 Dynamic Repair Case Studies")
    lines.append("")

    if not case_studies:
        lines.append("No case studies were available from the local R98/R99 artifacts.")
        lines.append("")
        return "\n".join(lines)

    for index, case in enumerate(case_studies, start=1):
        lines.append(f"## Case {index}: {case['case_type']}")
        lines.append("")
        lines.append(f"- Pack: `{case.get('pack_name')}`")
        lines.append(f"- Episode: `{case.get('episode_id')}`")
        lines.append(f"- Failure signature: `{case.get('failure_signature')}`")
        lines.append(f"- Admission decision: `{case.get('admission_decision')}`")
        lines.append(f"- Dynamic outcome: `{case.get('dynamic_outcome')}`")
        lines.append(f"- Time to correction: `{case.get('time_to_correction')}`")
        lines.append(f"- Preserve evidence: `{case.get('preserve_evidence')}`")
        lines.append(f"- Rollback scope: `{case.get('rollback_scope')}`")
        lines.append("")
        lines.append("### Committed Evidence")
        lines.append("")
        committed = case.get("committed_operations") or []
        if committed:
            for op in committed:
                lines.append(f"- `{op}`")
        else:
            lines.append("- Not available in this artifact.")
        lines.append("")
        lines.append("### Affected Steps")
        lines.append("")
        affected = case.get("affected_steps") or []
        if affected:
            for step in affected:
                lines.append(f"- `{step}`")
        else:
            lines.append("- Not available in this artifact.")
        lines.append("")
        lines.append("### Admission Reasons")
        lines.append("")
        reasons = case.get("admission_reasons") or []
        if reasons:
            for reason in reasons:
                lines.append(f"- `{reason}`")
        else:
            lines.append("- None recorded.")
        lines.append("")
        lines.append("### Proposal Summary")
        lines.append("")
        summary = case.get("repair_summary") or "No proposal summary recorded."
        lines.append(summary)
        lines.append("")
        lines.append("### Interpretation")
        lines.append("")
        lines.append(case.get("interpretation", ""))
        lines.append("")

    return "\n".join(lines)


def render_ledger_markdown(ledger: Dict[str, Any]) -> str:
    summary = ledger["dynamic_summary"]

    lines: List[str] = []
    lines.append("# R100 Dynamic Closure Ledger")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(ledger["claim_boundary"])
    lines.append("")
    lines.append("## Closure Status")
    lines.append("")
    lines.append(f"- Bounded dynamic closure: `{ledger['bounded_dynamic_closure']}`")
    lines.append(f"- Official scorer invoked: `{summary['official_scorer_invoked']}`")
    lines.append(f"- Dynamic events: `{summary['num_events']}`")
    lines.append(f"- Safety passed: `{summary['safety_passed']}`")
    lines.append("")
    lines.append("## Dynamic Score Summary")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    for key in [
        "dynamic_admit_count",
        "dynamic_reject_count",
        "dynamic_observe_count",
        "dynamic_safe_rejection_count",
        "repeated_failure_rate",
        "horizon_reward_mean",
        "grounded_admission_rate",
        "time_to_correction_mean_observed",
        "time_to_correction_observed_count",
        "time_to_correction_censored_count",
    ]:
        lines.append(f"| {key} | {summary.get(key)} |")

    lines.append("")
    lines.append("## Evidence Chain")
    lines.append("")
    lines.append("| ID | Evidence | Role | Status |")
    lines.append("|---|---|---|---|")
    for item in ledger["evidence_items"]:
        lines.append(
            f"| {item['id']} | {item['name']} | {item['role']} | {item['status']} |"
        )

    lines.append("")
    lines.append("## What Part I Now Supports")
    lines.append("")
    for item in ledger["claims_supported"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## What Part I Does Not Yet Support")
    lines.append("")
    for item in ledger["claims_not_supported"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Part II Bridge")
    lines.append("")
    for item in ledger["part_ii_bridge"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The dynamic pilot should not be read as evidence that LLMs are reliable "
        "repair planners by themselves. The result is that unreliable repair "
        "proposals can be placed behind an admission-gated execution substrate "
        "that preserves committed evidence, rejects unsafe rollback, bounds "
        "repair radius, and emits auditable recovery traces."
    )
    lines.append("")
    lines.append(
        "A pass means the repair loop remained safe and feasible under disruption. "
        "It does not mean the selected repair was optimal."
    )
    lines.append("")

    return "\n".join(lines)


def write_outputs(ledger: Dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    write_json(output_dir / "dynamic_closure_ledger.json", ledger)
    (output_dir / "dynamic_closure_ledger.md").write_text(
        render_ledger_markdown(ledger),
        encoding="utf-8",
    )
    write_json(output_dir / "case_studies.json", ledger["case_studies"])
    (output_dir / "case_studies.md").write_text(
        render_case_studies(ledger["case_studies"]),
        encoding="utf-8",
    )


def cmd_build(args: argparse.Namespace) -> None:
    ledger = build_closure_ledger(
        r99_score_report=Path(args.r99_score_report),
        r99_events_path=Path(args.r99_events),
        r98_events_path=Path(args.r98_events),
    )
    write_outputs(ledger, Path(args.output_dir))

    print(
        json.dumps(
            {
                "output_dir": args.output_dir,
                "bounded_dynamic_closure": ledger["bounded_dynamic_closure"],
                "official_scorer_invoked": ledger["dynamic_summary"][
                    "official_scorer_invoked"
                ],
                "num_events": ledger["dynamic_summary"]["num_events"],
                "safety_passed": ledger["dynamic_summary"]["safety_passed"],
                "dynamic_admit_count": ledger["dynamic_summary"][
                    "dynamic_admit_count"
                ],
                "dynamic_reject_count": ledger["dynamic_summary"][
                    "dynamic_reject_count"
                ],
                "dynamic_safe_rejection_count": ledger["dynamic_summary"][
                    "dynamic_safe_rejection_count"
                ],
                "num_case_studies": len(ledger["case_studies"]),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="R100 dynamic closure ledger")
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build dynamic closure ledger")
    build_cmd.add_argument("--r99-score-report", default=DEFAULT_R99_SCORE_REPORT)
    build_cmd.add_argument("--r99-events", default=DEFAULT_R99_EVENTS)
    build_cmd.add_argument("--r98-events", default=DEFAULT_R98_EVENTS)
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
