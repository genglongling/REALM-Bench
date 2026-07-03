#!/usr/bin/env python3
"""R90 full deterministic REALM Tier-6 report.

This report scores the public Tier-6 deterministic development set using the
reference B0 and B* baseline trace emitters, then places the R88 Mnemosyne
live-LLM pilot result beside those anchors.

Claim boundary:
R90 is a deterministic benchmark/reference report plus one live-LLM pilot row.
It supports Chapter 6 closure as pilot-plus-baseline evidence. It is not yet
confirmatory-scale evidence over a large benchmark release.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
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


SCHEMA = "realm_tier6_full_deterministic_report_v0"

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/full_deterministic_report"

DEFAULT_R88_SCORE_REPORT = (
    "runs/realm_tier6/mnemosyne_live_llm_official_score/"
    "mnemosyne_live_llm_score_report.json"
)


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


generator = load_module("tier6_generator_for_full_deterministic_report", T6_GENERATOR_PATH)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_read_json(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    return read_json(path)


def summarize_sequences(sequences: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "num_sequences": len(sequences),
        "num_episodes": sum(len(sequence["episodes"]) for sequence in sequences),
        "num_control_sequences": sum(
            1 for sequence in sequences if sequence["is_control_sequence"]
        ),
        "num_non_control_sequences": sum(
            1 for sequence in sequences if not sequence["is_control_sequence"]
        ),
        "families": sorted(
            {sequence["base_instance"]["family"] for sequence in sequences}
        ),
        "episodes_per_sequence": (
            sequences[0]["episodes_per_sequence"] if sequences else None
        ),
        "sequence_ids": [sequence["sequence_id"] for sequence in sequences],
    }


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


def baseline_row(
    *,
    system_id: str,
    display_name: str,
    evidence_type: str,
    score: Dict[str, Any],
) -> Dict[str, Any]:
    safety_counts = score["safety_counts"]
    bracket = score["bracket"]

    return {
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
        "repeated_failure_rate_controls": score[
            "repeated_failure_rate_controls"
        ],
        "horizon_reward_mean": score["horizon_reward_mean"],
        "grounded_admission_rate": score["grounded_admission_rate"],
        "rfr_bracket_position": bracket["position_repeated_failure_rate"],
        "horizon_bracket_position": bracket["position_horizon_reward"],
    }


def live_llm_pilot_row(r88_report: Dict[str, Any] | None) -> Dict[str, Any] | None:
    if not r88_report:
        return None

    score = r88_report["overall_score"]
    row = baseline_row(
        system_id="mnemosyne_live_llm_r88_pilot",
        display_name="Mnemosyne live-LLM pilot",
        evidence_type="manual_live_llm_pilot",
        score=score,
    )
    row["sequence_id"] = r88_report.get("sequence_id")
    row["config_id"] = r88_report.get("config_id")
    row["condition_label"] = r88_report.get("condition_label")
    row["official_scorer_invoked"] = r88_report.get("official_scorer_invoked")
    row["score_scope"] = r88_report.get("score_scope")
    return row


def build_report(
    *,
    max_families: int,
    r88_score_report_path: Path,
) -> Dict[str, Any]:
    sequences = generator.generate_development_sequences(
        REPO_ROOT,
        max_families=max_families,
    )

    b0_events = emit_b0_memoryless_events(sequences)
    bstar_events = emit_bstar_oracle_events(sequences)

    b0_score = score_trace(b0_events)
    bstar_score = score_trace(bstar_events)
    r88_report = maybe_read_json(r88_score_report_path)

    rows = [
        baseline_row(
            system_id="B0_memoryless_replay",
            display_name="B0 memoryless replay",
            evidence_type="deterministic_reference_baseline",
            score=b0_score,
        ),
        baseline_row(
            system_id="Bstar_oracle_memory",
            display_name="B* oracle memory",
            evidence_type="deterministic_reference_baseline",
            score=bstar_score,
        ),
    ]

    pilot = live_llm_pilot_row(r88_report)
    if pilot is not None:
        rows.append(pilot)

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "R90 scores the deterministic Tier-6 development set with B0 and "
            "B* reference baselines and reports the R88 Mnemosyne live-LLM pilot "
            "beside those anchors. This supports Chapter 6 pilot-plus-baseline "
            "evidence, not confirmatory-scale evidence."
        ),
        "development_set": summarize_sequences(sequences),
        "source_paths": {
            "generator": str(T6_GENERATOR_PATH),
            "r88_score_report": str(r88_score_report_path),
        },
        "baseline_scores": {
            "B0_memoryless_replay": compact_score(b0_score),
            "Bstar_oracle_memory": compact_score(bstar_score),
        },
        "r88_live_llm_pilot_available": r88_report is not None,
        "chapter6_table": rows,
        "allowed_claims": [
            "The Tier-6 deterministic development set can be scored end to end.",
            "B0 and B* reference baselines bracket the repeated-failure and horizon-reward metrics.",
            "The R88 Mnemosyne live-LLM pilot can be reported beside deterministic Tier-6 anchors.",
            "The evidence supports Chapter 6 pilot-plus-baseline closure.",
        ],
        "disallowed_claims": [
            "confirmatory-scale benchmark evidence",
            "API-automated live LLM evidence",
            "production CTL-domain StateView realization",
            "proof of AGI, wisdom, or autonomous scientific reasoning",
        ],
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R90 Full Deterministic REALM Tier-6 Report")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Development Set")
    lines.append("")
    dev = report["development_set"]
    lines.append(f"- Sequences: `{dev['num_sequences']}`")
    lines.append(f"- Episodes: `{dev['num_episodes']}`")
    lines.append(f"- Control sequences: `{dev['num_control_sequences']}`")
    lines.append(f"- Non-control sequences: `{dev['num_non_control_sequences']}`")
    lines.append(f"- Episodes per sequence: `{dev['episodes_per_sequence']}`")
    lines.append(f"- Families: `{', '.join(dev['families'])}`")
    lines.append("")
    lines.append("## Chapter 6 Deterministic + Pilot Table")
    lines.append("")
    lines.append(
        "| System | Evidence type | Events | Safety | RFR | Horizon reward | "
        "Grounded admission | RFR bracket | Horizon bracket |"
    )
    lines.append("|---|---|---:|---|---:|---:|---:|---:|---:|")

    for row in report["chapter6_table"]:
        lines.append(
            f"| {row['display_name']} | {row['evidence_type']} | "
            f"{row['num_events']} | {row['safety_passed']} | "
            f"{row['repeated_failure_rate']} | {row['horizon_reward_mean']} | "
            f"{row['grounded_admission_rate']} | {row['rfr_bracket_position']} | "
            f"{row['horizon_bracket_position']} |"
        )

    lines.append("")
    lines.append("## Baseline Interpretation")
    lines.append("")
    b0 = report["baseline_scores"]["B0_memoryless_replay"]
    bstar = report["baseline_scores"]["Bstar_oracle_memory"]
    lines.append(
        f"B0 memoryless replay scores RFR = `{b0['repeated_failure_rate']}` "
        f"and horizon reward = `{b0['horizon_reward_mean']}`."
    )
    lines.append("")
    lines.append(
        f"B* oracle memory scores RFR = `{bstar['repeated_failure_rate']}` "
        f"and horizon reward = `{bstar['horizon_reward_mean']}`."
    )
    lines.append("")

    if report["r88_live_llm_pilot_available"]:
        pilot = [
            row
            for row in report["chapter6_table"]
            if row["system_id"] == "mnemosyne_live_llm_r88_pilot"
        ][0]
        lines.append("## R88 Live-LLM Pilot Placement")
        lines.append("")
        lines.append(
            "The R88 Mnemosyne live-LLM pilot is placed beside the deterministic "
            "B0/B* anchors as a pilot row, not as confirmatory-scale evidence."
        )
        lines.append("")
        lines.append(
            f"It reports safety passed = `{pilot['safety_passed']}`, "
            f"horizon reward mean = `{pilot['horizon_reward_mean']}`, and "
            f"grounded admission rate = `{pilot['grounded_admission_rate']}`."
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
        "The full deterministic Tier-6 development set was scored with two "
        "reference anchors: B0 memoryless replay and B* oracle memory. B0 "
        f"establishes the lower anchor with repeated failure rate "
        f"`{b0['repeated_failure_rate']}` and horizon reward "
        f"`{b0['horizon_reward_mean']}`; B* establishes the upper anchor with "
        f"repeated failure rate `{bstar['repeated_failure_rate']}` and horizon "
        f"reward `{bstar['horizon_reward_mean']}`. The R88 Mnemosyne live-LLM "
        "pilot is reported beside these anchors as pilot integration evidence. "
        "This closes the deterministic baseline-and-pilot evidence layer for "
        "Chapter 6, while leaving confirmatory-scale evaluation to the next "
        "benchmark expansion."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(
        max_families=args.max_families,
        r88_score_report_path=Path(args.r88_score_report),
    )

    json_path = output_dir / "full_deterministic_report.json"
    md_path = output_dir / "full_deterministic_report.md"
    table_path = output_dir / "chapter6_full_deterministic_table.json"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")
    table_path.write_text(
        json.dumps(report["chapter6_table"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "chapter_table": str(table_path),
                "num_sequences": report["development_set"]["num_sequences"],
                "num_episodes": report["development_set"]["num_episodes"],
                "families": report["development_set"]["families"],
                "r88_live_llm_pilot_available": report[
                    "r88_live_llm_pilot_available"
                ],
                "rows": len(report["chapter6_table"]),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build R90 full deterministic report")
    build_cmd.add_argument("--max-families", type=int, default=3)
    build_cmd.add_argument("--r88-score-report", default=DEFAULT_R88_SCORE_REPORT)
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
