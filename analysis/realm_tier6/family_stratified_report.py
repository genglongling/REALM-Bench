#!/usr/bin/env python3
"""R92 family-stratified REALM Tier-6 report.

This report stratifies deterministic Tier-6 B0/B* baseline scores by family
and places the R88 Mnemosyne live-LLM pilot as a jobshop-family pilot row.

Claim boundary:
R92 supports Chapter 6 family-stratified pilot-plus-baseline evidence. It does
not claim confirmatory-scale benchmark evidence, API-automated live-LLM behavior,
or production CTL-domain realization.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
T6_GENERATOR_PATH = REPO_ROOT / "datasets" / "T6" / "generator.py"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evaluation.tier6.baseline_traces import (  # noqa: E402
    emit_b0_memoryless_events,
    emit_bstar_oracle_events,
)
from evaluation.tier6.scorer import score_trace  # noqa: E402


SCHEMA = "realm_tier6_family_stratified_report_v0"

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/family_stratified_report"

DEFAULT_R88_SCORE_REPORT = (
    "runs/realm_tier6/mnemosyne_live_llm_official_score/"
    "mnemosyne_live_llm_score_report.json"
)

DEFAULT_LIVE_PILOT_FAMILY = "jobshop_breakdown"


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


generator = load_module("tier6_generator_for_family_stratified_report", T6_GENERATOR_PATH)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_read_json(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    return read_json(path)


def group_by_family(events: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    by_family: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_family[str(event.get("family", "unknown"))].append(event)
    return dict(by_family)


def sequence_summary_by_family(sequences: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    summary: Dict[str, Dict[str, Any]] = {}

    for sequence in sequences:
        family = sequence["base_instance"]["family"]
        entry = summary.setdefault(
            family,
            {
                "num_sequences": 0,
                "num_control_sequences": 0,
                "num_non_control_sequences": 0,
                "num_episodes": 0,
                "sequence_ids": [],
            },
        )
        entry["num_sequences"] += 1
        entry["num_control_sequences"] += 1 if sequence["is_control_sequence"] else 0
        entry["num_non_control_sequences"] += 0 if sequence["is_control_sequence"] else 1
        entry["num_episodes"] += len(sequence["episodes"])
        entry["sequence_ids"].append(sequence["sequence_id"])

    return summary


def compact_score(score: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "num_events": score["num_events"],
        "num_control_events": score["num_control_events"],
        "num_non_control_events": score["num_non_control_events"],
        "safety_passed": score["safety_passed"],
        "safety_counts": score["safety_counts"],
        "repeated_failure_rate": score["repeated_failure_rate"],
        "repeated_failure_rate_controls": score["repeated_failure_rate_controls"],
        "time_to_correction_mean_observed": score[
            "time_to_correction_mean_observed"
        ],
        "time_to_correction_observed_count": score[
            "time_to_correction_observed_count"
        ],
        "time_to_correction_censored_count": score[
            "time_to_correction_censored_count"
        ],
        "horizon_reward_mean": score["horizon_reward_mean"],
        "grounded_admission_rate": score["grounded_admission_rate"],
        "bracket": score["bracket"],
    }


def score_events_by_family(events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for family, family_events in sorted(group_by_family(events).items()):
        result[family] = compact_score(score_trace(family_events))
    return result


def table_row(
    *,
    family: str,
    system_id: str,
    display_name: str,
    evidence_type: str,
    score: Dict[str, Any],
) -> Dict[str, Any]:
    bracket = score["bracket"]
    safety_counts = score["safety_counts"]

    return {
        "family": family,
        "system_id": system_id,
        "display_name": display_name,
        "evidence_type": evidence_type,
        "num_events": score["num_events"],
        "safety_passed": score["safety_passed"],
        "invalid_commit_count": safety_counts["invalid_commit_count"],
        "evidence_destroying_repair_count": safety_counts[
            "evidence_destroying_repair_count"
        ],
        "orphaned_dependent_count": safety_counts["orphaned_dependent_count"],
        "repeated_failure_rate": score["repeated_failure_rate"],
        "repeated_failure_rate_controls": score["repeated_failure_rate_controls"],
        "horizon_reward_mean": score["horizon_reward_mean"],
        "grounded_admission_rate": score["grounded_admission_rate"],
        "rfr_bracket_position": bracket["position_repeated_failure_rate"],
        "horizon_bracket_position": bracket["position_horizon_reward"],
    }


def live_pilot_family_row(
    *,
    r88_report: Dict[str, Any] | None,
    live_pilot_family: str,
) -> Dict[str, Any] | None:
    if not r88_report:
        return None

    score = r88_report["overall_score"]
    row = table_row(
        family=live_pilot_family,
        system_id="mnemosyne_live_llm_r88_pilot",
        display_name="Mnemosyne live-LLM pilot",
        evidence_type="manual_live_llm_pilot",
        score=score,
    )
    row["sequence_id"] = r88_report.get("sequence_id")
    row["config_id"] = r88_report.get("config_id")
    row["condition_label"] = r88_report.get("condition_label")
    row["official_scorer_invoked"] = r88_report.get("official_scorer_invoked")
    row["family_assignment_note"] = (
        "R88 pilot sequence was generated from the jobshop_breakdown pilot pack; "
        "R92 assigns it to the configured live_pilot_family."
    )
    return row


def build_family_rows(
    *,
    b0_by_family: Dict[str, Dict[str, Any]],
    bstar_by_family: Dict[str, Dict[str, Any]],
    r88_report: Dict[str, Any] | None,
    live_pilot_family: str,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    families = sorted(set(b0_by_family) | set(bstar_by_family))

    for family in families:
        if family in b0_by_family:
            rows.append(
                table_row(
                    family=family,
                    system_id="B0_memoryless_replay",
                    display_name="B0 memoryless replay",
                    evidence_type="deterministic_reference_baseline",
                    score=b0_by_family[family],
                )
            )
        if family in bstar_by_family:
            rows.append(
                table_row(
                    family=family,
                    system_id="Bstar_oracle_memory",
                    display_name="B* oracle memory",
                    evidence_type="deterministic_reference_baseline",
                    score=bstar_by_family[family],
                )
            )

    pilot = live_pilot_family_row(
        r88_report=r88_report,
        live_pilot_family=live_pilot_family,
    )
    if pilot is not None:
        rows.append(pilot)

    return rows


def build_report(
    *,
    max_families: int,
    r88_score_report_path: Path,
    live_pilot_family: str,
) -> Dict[str, Any]:
    sequences = generator.generate_development_sequences(
        REPO_ROOT,
        max_families=max_families,
    )

    b0_events = emit_b0_memoryless_events(sequences)
    bstar_events = emit_bstar_oracle_events(sequences)

    b0_by_family = score_events_by_family(b0_events)
    bstar_by_family = score_events_by_family(bstar_events)
    r88_report = maybe_read_json(r88_score_report_path)

    table = build_family_rows(
        b0_by_family=b0_by_family,
        bstar_by_family=bstar_by_family,
        r88_report=r88_report,
        live_pilot_family=live_pilot_family,
    )

    families = sorted(sequence_summary_by_family(sequences))

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "R92 stratifies deterministic Tier-6 B0/B* baselines by family and "
            "places the R88 Mnemosyne live-LLM pilot as a family-assigned pilot "
            "row. This supports Chapter 6 family-stratified pilot-plus-baseline "
            "evidence, not confirmatory-scale evidence."
        ),
        "development_set_by_family": sequence_summary_by_family(sequences),
        "families": families,
        "source_paths": {
            "generator": str(T6_GENERATOR_PATH),
            "r88_score_report": str(r88_score_report_path),
        },
        "live_pilot_family": live_pilot_family,
        "r88_live_llm_pilot_available": r88_report is not None,
        "baseline_scores_by_family": {
            "B0_memoryless_replay": b0_by_family,
            "Bstar_oracle_memory": bstar_by_family,
        },
        "chapter6_family_table": table,
        "allowed_claims": [
            "Tier-6 deterministic baseline behavior can be stratified by family.",
            "The Chapter 6 evidence covers jobshop, routing, and wedding recovery families at the deterministic baseline layer.",
            "The R88 live-LLM pilot can be reported as a jobshop-family pilot row with explicit claim boundary.",
        ],
        "disallowed_claims": [
            "family-generalized live-LLM evidence across all families",
            "confirmatory-scale benchmark evidence",
            "API-automated live LLM evidence",
            "production CTL-domain StateView realization",
            "proof of AGI, wisdom, or autonomous scientific reasoning",
        ],
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R92 Family-Stratified REALM Tier-6 Report")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Families")
    lines.append("")
    for family, item in report["development_set_by_family"].items():
        lines.append(
            f"- `{family}`: sequences `{item['num_sequences']}`, "
            f"episodes `{item['num_episodes']}`, controls "
            f"`{item['num_control_sequences']}`"
        )

    lines.append("")
    lines.append("## Chapter 6 Family-Stratified Table")
    lines.append("")
    lines.append(
        "| Family | System | Evidence type | Events | Safety | RFR | Horizon reward | "
        "Grounded admission | RFR bracket | Horizon bracket |"
    )
    lines.append("|---|---|---|---:|---|---:|---:|---:|---:|---:|")

    for row in report["chapter6_family_table"]:
        lines.append(
            f"| {row['family']} | {row['display_name']} | {row['evidence_type']} | "
            f"{row['num_events']} | {row['safety_passed']} | "
            f"{row['repeated_failure_rate']} | {row['horizon_reward_mean']} | "
            f"{row['grounded_admission_rate']} | {row['rfr_bracket_position']} | "
            f"{row['horizon_bracket_position']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The deterministic baseline layer is stratified across all available "
        "Tier-6 development families. This prevents Chapter 6 from appearing "
        "to rely only on a single task family."
    )
    lines.append("")
    lines.append(
        "The R88 live-LLM pilot remains a jobshop-family pilot row. It is not yet "
        "family-generalized live-LLM evidence."
    )
    lines.append("")
    lines.append("## Allowed Claims")
    lines.append("")
    for claim in report["allowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Disallowed Claims")
    lines.append("")
    for claim in report["disallowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Chapter 6 Insert Draft")
    lines.append("")
    lines.append(
        "To test whether the Tier-6 evidence is tied to a single task family, "
        "we stratified the deterministic B0/B* baseline layer by family. The "
        "development set covers job-shop breakdown, routing disruption, and "
        "wedding recovery families. For each family, B0 and B* remain valid "
        "reference anchors under the same public Tier-6 scorer. The R88 "
        "Mnemosyne live-LLM pilot is reported separately as a jobshop-family "
        "pilot row. Thus, Chapter 6 has family-stratified deterministic "
        "baseline evidence, while live-LLM family generalization remains a "
        "future expansion."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(
        max_families=args.max_families,
        r88_score_report_path=Path(args.r88_score_report),
        live_pilot_family=args.live_pilot_family,
    )

    json_path = output_dir / "family_stratified_report.json"
    md_path = output_dir / "family_stratified_report.md"
    table_path = output_dir / "chapter6_family_stratified_table.json"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")
    table_path.write_text(
        json.dumps(report["chapter6_family_table"], indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "chapter_table": str(table_path),
                "families": report["families"],
                "live_pilot_family": report["live_pilot_family"],
                "r88_live_llm_pilot_available": report[
                    "r88_live_llm_pilot_available"
                ],
                "rows": len(report["chapter6_family_table"]),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build family-stratified report")
    build_cmd.add_argument("--max-families", type=int, default=3)
    build_cmd.add_argument("--r88-score-report", default=DEFAULT_R88_SCORE_REPORT)
    build_cmd.add_argument("--live-pilot-family", default=DEFAULT_LIVE_PILOT_FAMILY)
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
