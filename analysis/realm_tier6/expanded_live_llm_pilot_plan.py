#!/usr/bin/env python3
"""R93 expanded live-LLM pilot plan for Chapter 6.

This report defines the collection matrix needed to expand the R88 live-LLM
pilot beyond one E7 jobshop sequence.

Claim boundary:
R93 is a coverage and collection-plan report. It does not collect new LLM
responses, does not score new live-LLM cases, and does not claim family-
generalized live-LLM evidence.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
T6_GENERATOR_PATH = REPO_ROOT / "datasets" / "T6" / "generator.py"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


SCHEMA = "realm_tier6_expanded_live_llm_pilot_plan_v0"

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/expanded_live_llm_pilot_plan"

DEFAULT_R88_SCORE_REPORT = (
    "runs/realm_tier6/mnemosyne_live_llm_official_score/"
    "mnemosyne_live_llm_score_report.json"
)

DEFAULT_CONFIGS = ["E7"]

DEFAULT_PROPOSER_PACKS = [
    "claude",
    "gpt",
    "deepseek_expert",
    "deepseek_instant",
]

TARGET_FAMILIES = [
    "jobshop_breakdown",
    "ride_or_routing_disruption",
    "wedding_recovery",
]


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


generator = load_module("tier6_generator_for_expanded_live_llm_plan", T6_GENERATOR_PATH)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_read_json(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    return read_json(path)


def select_one_non_control_sequence_per_family(
    sequences: List[Dict[str, Any]],
    *,
    target_families: List[str],
    preferred_sequence_id: str | None = None,
) -> Dict[str, Dict[str, Any]]:
    """Select one non-control sequence per family.

    If a preferred sequence id is supplied and belongs to a target family, it is
    selected for that family. This keeps the existing R88 jobshop pilot aligned.
    """

    selected: Dict[str, Dict[str, Any]] = {}

    if preferred_sequence_id:
        for sequence in sequences:
            family = sequence["base_instance"]["family"]
            if (
                family in target_families
                and sequence["sequence_id"] == preferred_sequence_id
                and not sequence["is_control_sequence"]
            ):
                selected[family] = sequence

    for family in target_families:
        if family in selected:
            continue
        candidates = [
            sequence
            for sequence in sequences
            if sequence["base_instance"]["family"] == family
            and not sequence["is_control_sequence"]
        ]
        if candidates:
            selected[family] = candidates[0]

    return selected


def existing_r88_sequence(r88_report: Dict[str, Any] | None) -> str | None:
    if not r88_report:
        return None
    value = r88_report.get("sequence_id")
    return value if isinstance(value, str) and value else None


def is_existing_r88_case(
    *,
    sequence: Dict[str, Any],
    r88_sequence_id: str | None,
) -> bool:
    return bool(r88_sequence_id and sequence["sequence_id"] == r88_sequence_id)


def build_collection_matrix(
    *,
    selected_sequences: Dict[str, Dict[str, Any]],
    proposer_packs: List[str],
    configs: List[str],
    r88_sequence_id: str | None,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for family in TARGET_FAMILIES:
        sequence = selected_sequences.get(family)
        if not sequence:
            continue

        existing = is_existing_r88_case(
            sequence=sequence,
            r88_sequence_id=r88_sequence_id,
        )

        for config_id in configs:
            for pack_name in proposer_packs:
                for episode in sequence["episodes"]:
                    rows.append(
                        {
                            "status": (
                                "existing_r88_collected"
                                if existing
                                else "planned_not_collected"
                            ),
                            "family": family,
                            "sequence_id": sequence["sequence_id"],
                            "base_instance_id": sequence["base_instance"][
                                "base_instance_id"
                            ],
                            "source_path": sequence["base_instance"]["source_path"],
                            "config_id": config_id,
                            "condition_label": (
                                "full_crt_stack"
                                if config_id == "E7"
                                else "non_e7_expansion"
                            ),
                            "pack_name": pack_name,
                            "episode_id": episode["episode_id"],
                            "is_control_sequence": sequence["is_control_sequence"],
                            "hazard_signatures": sequence["hazard_signatures"],
                            "collection_unit": (
                                f"{family}:{sequence['sequence_id']}:{config_id}:"
                                f"{pack_name}:e{episode['episode_id']:02d}"
                            ),
                        }
                    )

    return rows


def summarize_matrix(matrix: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_cases = len(matrix)
    existing_cases = sum(1 for row in matrix if row["status"] == "existing_r88_collected")
    planned_cases = sum(1 for row in matrix if row["status"] == "planned_not_collected")

    by_family: Dict[str, Dict[str, int]] = {}
    for row in matrix:
        item = by_family.setdefault(
            row["family"],
            {
                "total_cases": 0,
                "existing_r88_collected": 0,
                "planned_not_collected": 0,
            },
        )
        item["total_cases"] += 1
        item[row["status"]] += 1

    return {
        "total_cases": total_cases,
        "existing_r88_collected": existing_cases,
        "planned_not_collected": planned_cases,
        "by_family": by_family,
    }


def build_report(
    *,
    max_families: int,
    r88_score_report_path: Path,
    proposer_packs: List[str],
    configs: List[str],
) -> Dict[str, Any]:
    r88_report = maybe_read_json(r88_score_report_path)
    r88_sequence_id = existing_r88_sequence(r88_report)

    sequences = generator.generate_development_sequences(
        REPO_ROOT,
        max_families=max_families,
    )

    selected_sequences = select_one_non_control_sequence_per_family(
        sequences,
        target_families=TARGET_FAMILIES,
        preferred_sequence_id=r88_sequence_id,
    )

    matrix = build_collection_matrix(
        selected_sequences=selected_sequences,
        proposer_packs=proposer_packs,
        configs=configs,
        r88_sequence_id=r88_sequence_id,
    )

    matrix_summary = summarize_matrix(matrix)

    selected_summary = {
        family: {
            "sequence_id": sequence["sequence_id"],
            "base_instance_id": sequence["base_instance"]["base_instance_id"],
            "source_path": sequence["base_instance"]["source_path"],
            "episodes": len(sequence["episodes"]),
            "is_control_sequence": sequence["is_control_sequence"],
            "hazard_signatures": sequence["hazard_signatures"],
        }
        for family, sequence in selected_sequences.items()
    }

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "R93 defines the expanded live-LLM collection matrix needed to move "
            "from the R88 one-sequence E7 jobshop pilot to a three-family E7 "
            "pilot. It does not collect or score new LLM responses."
        ),
        "source_paths": {
            "generator": str(T6_GENERATOR_PATH),
            "r88_score_report": str(r88_score_report_path),
        },
        "target_families": TARGET_FAMILIES,
        "configs": configs,
        "proposer_packs": proposer_packs,
        "r88_sequence_id": r88_sequence_id,
        "selected_sequences": selected_summary,
        "matrix_summary": matrix_summary,
        "collection_matrix": matrix,
        "chapter6_status": {
            "bounded_pilot_ready": True,
            "family_generalized_live_llm_ready": matrix_summary[
                "planned_not_collected"
            ]
            == 0,
            "additional_cases_needed_for_three_family_live_pilot": matrix_summary[
                "planned_not_collected"
            ],
        },
        "allowed_claims": [
            "Chapter 6 has bounded live-LLM pilot evidence from R88.",
            "R93 defines the exact additional cases needed for a three-family live-LLM pilot.",
            "The expanded collection target is auditable before new manual or API responses are collected.",
        ],
        "disallowed_claims": [
            "new live-LLM results beyond R88",
            "family-generalized live-LLM evidence",
            "API-automated live LLM evidence",
            "confirmatory-scale benchmark evidence",
            "production CTL-domain StateView realization",
            "proof of AGI, wisdom, or autonomous scientific reasoning",
        ],
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R93 Expanded Live-LLM Pilot Plan")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Chapter 6 Status")
    lines.append("")
    status = report["chapter6_status"]
    lines.append(f"- Bounded pilot ready: `{status['bounded_pilot_ready']}`")
    lines.append(
        f"- Family-generalized live-LLM ready: "
        f"`{status['family_generalized_live_llm_ready']}`"
    )
    lines.append(
        f"- Additional cases needed for three-family live pilot: "
        f"`{status['additional_cases_needed_for_three_family_live_pilot']}`"
    )
    lines.append("")
    lines.append("## Selected Sequences")
    lines.append("")
    lines.append("| Family | Sequence | Base instance | Episodes | Hazards |")
    lines.append("|---|---|---|---:|---|")
    for family, item in report["selected_sequences"].items():
        hazards = ", ".join(item["hazard_signatures"])
        lines.append(
            f"| {family} | `{item['sequence_id']}` | "
            f"`{item['base_instance_id']}` | {item['episodes']} | {hazards} |"
        )

    lines.append("")
    lines.append("## Collection Matrix Summary")
    lines.append("")
    summary = report["matrix_summary"]
    lines.append(f"- Total target cases: `{summary['total_cases']}`")
    lines.append(f"- Existing R88 collected cases: `{summary['existing_r88_collected']}`")
    lines.append(f"- Planned not collected cases: `{summary['planned_not_collected']}`")
    lines.append("")
    lines.append("| Family | Total | Existing R88 | Planned not collected |")
    lines.append("|---|---:|---:|---:|")
    for family, item in summary["by_family"].items():
        lines.append(
            f"| {family} | {item['total_cases']} | "
            f"{item['existing_r88_collected']} | {item['planned_not_collected']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "R93 keeps Chapter 6 honest. The chapter can close with bounded pilot "
        "evidence, but it should not claim family-generalized live-LLM evidence "
        "until the planned cases are actually collected and scored."
    )
    lines.append("")
    lines.append(
        "The expanded three-family E7 live-LLM pilot would require the existing "
        "jobshop R88 cases plus new routing and wedding-family response packs."
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
        "To determine whether the R88 live-LLM pilot should be expanded before "
        "publication, we generated an explicit three-family collection matrix. "
        "The matrix targets one non-control E7 sequence per development family "
        "and four proposer packs per sequence. The existing R88 jobshop pilot "
        f"accounts for `{summary['existing_r88_collected']}` cases; a full "
        f"three-family live-LLM pilot would require "
        f"`{summary['planned_not_collected']}` additional cases. We therefore "
        "treat the current Chapter 6 live-LLM result as bounded pilot evidence, "
        "not family-generalized evidence."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(
        max_families=args.max_families,
        r88_score_report_path=Path(args.r88_score_report),
        proposer_packs=args.proposer_packs,
        configs=args.configs,
    )

    json_path = output_dir / "expanded_live_llm_pilot_plan.json"
    md_path = output_dir / "expanded_live_llm_pilot_plan.md"
    matrix_path = output_dir / "collection_matrix.json"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")
    matrix_path.write_text(
        json.dumps(report["collection_matrix"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "collection_matrix": str(matrix_path),
                "bounded_pilot_ready": report["chapter6_status"][
                    "bounded_pilot_ready"
                ],
                "family_generalized_live_llm_ready": report["chapter6_status"][
                    "family_generalized_live_llm_ready"
                ],
                "additional_cases_needed_for_three_family_live_pilot": report[
                    "chapter6_status"
                ]["additional_cases_needed_for_three_family_live_pilot"],
                "total_target_cases": report["matrix_summary"]["total_cases"],
                "existing_r88_collected": report["matrix_summary"][
                    "existing_r88_collected"
                ],
                "planned_not_collected": report["matrix_summary"][
                    "planned_not_collected"
                ],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build expanded live-LLM pilot plan")
    build_cmd.add_argument("--max-families", type=int, default=3)
    build_cmd.add_argument("--r88-score-report", default=DEFAULT_R88_SCORE_REPORT)
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.add_argument("--configs", nargs="+", default=DEFAULT_CONFIGS)
    build_cmd.add_argument("--proposer-packs", nargs="+", default=DEFAULT_PROPOSER_PACKS)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
