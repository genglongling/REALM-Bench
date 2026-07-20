#!/usr/bin/env python3
"""R89 Chapter 6 evidence package for Mnemosyne live-LLM REALM Tier 6.

This script consolidates the Mnemosyne-side R83.5b-R86 reports and the
REALM-Bench-side R87-R88 reports into a chapter-ready pilot evidence package.

Claim boundary:
R89 is a Chapter 6 pilot evidence package. It is not confirmatory-scale
evidence and does not claim AGI, wisdom, autonomous science, API automation,
or production CTL-domain realization.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


DEFAULT_OUTPUT_DIR = "runs/realm_tier6/mnemosyne_live_llm_ch6_package"

DEFAULT_SCORE_REPORT = (
    "runs/realm_tier6/mnemosyne_live_llm_official_score/"
    "mnemosyne_live_llm_score_report.json"
)

DEFAULT_IMPORT_REPORT = (
    "runs/realm_tier6/mnemosyne_live_llm_scorer_import/"
    "mnemosyne_live_llm_import_report.json"
)

MNEMOSYNE_ROOT = Path("/Users/edward.chang/ALAS/AGIV3/mnemosyne_product")

DEFAULT_MNEMOSYNE_REPORTS = {
    "r835b_comparison": (
        MNEMOSYNE_ROOT
        / "results/realm_tier6_live_llm_manual/kernel_import_report/comparison_report.json"
    ),
    "r835c_kernel_trace": (
        MNEMOSYNE_ROOT
        / "results/realm_tier6_live_llm_manual/kernel_trace_report/kernel_trace_report.json"
    ),
    "r84_runtime_evaluator": (
        MNEMOSYNE_ROOT
        / "results/realm_tier6_live_llm_manual/runtime_evaluator_report/runtime_evaluator_report.json"
    ),
    "r85_score_bridge": (
        MNEMOSYNE_ROOT
        / "results/realm_tier6_live_llm_manual/realm_score_bridge_report/realm_score_bridge_report.json"
    ),
    "r86_scorer_handoff": (
        MNEMOSYNE_ROOT
        / "results/realm_tier6_live_llm_manual/realm_scorer_handoff/realm_scorer_handoff_bundle.json"
    ),
}

SCHEMA = "realm_tier6_mnemosyne_live_llm_ch6_package_v0"


def load_json(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def maybe_load_json(path: Path) -> Dict[str, Any] | None:
    if not path.exists():
        return None
    return load_json(path)


def load_sources(
    *,
    score_report_path: Path,
    import_report_path: Path,
    mnemosyne_report_paths: Dict[str, Path],
) -> Dict[str, Any]:
    return {
        "r87_import_report": load_json(import_report_path),
        "r88_score_report": load_json(score_report_path),
        "mnemosyne_reports": {
            key: maybe_load_json(path)
            for key, path in mnemosyne_report_paths.items()
        },
        "source_paths": {
            "r87_import_report": str(import_report_path),
            "r88_score_report": str(score_report_path),
            **{key: str(path) for key, path in mnemosyne_report_paths.items()},
        },
    }


def classify_pack(pack_name: str) -> str:
    mapping = {
        "claude": "Claude",
        "gpt": "GPT",
        "deepseek_e7_pilot": "DeepSeek expert",
        "deepseek_expert": "DeepSeek expert",
        "deepseek_instant": "DeepSeek instant",
        "deepseek_instant_e7_pilot": "DeepSeek instant",
    }
    return mapping.get(pack_name, pack_name)


def build_chapter_table(score_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for pack_name, score in score_report.get("pack_scores", {}).items():
        safety_counts = score.get("safety_counts", {})
        rows.append(
            {
                "model_pack": pack_name,
                "display_name": classify_pack(pack_name),
                "events": score.get("num_events"),
                "safety_passed": score.get("safety_passed"),
                "repeated_failure_rate": score.get("repeated_failure_rate"),
                "horizon_reward_mean": score.get("horizon_reward_mean"),
                "grounded_admission_rate": score.get("grounded_admission_rate"),
                "invalid_commit_count": safety_counts.get("invalid_commit_count"),
                "evidence_destroying_repair_count": safety_counts.get(
                    "evidence_destroying_repair_count"
                ),
                "orphaned_dependent_count": safety_counts.get(
                    "orphaned_dependent_count"
                ),
            }
        )

    return sorted(rows, key=lambda row: row["display_name"])


def build_overall_summary(score_report: Dict[str, Any]) -> Dict[str, Any]:
    overall = score_report.get("overall_score", {})
    safety_counts = overall.get("safety_counts", {})

    return {
        "sequence_id": score_report.get("sequence_id"),
        "config_id": score_report.get("config_id"),
        "condition_label": score_report.get("condition_label"),
        "official_scorer_invoked": score_report.get("official_scorer_invoked"),
        "score_scope": score_report.get("score_scope"),
        "num_events": score_report.get("num_events"),
        "safety_passed": overall.get("safety_passed"),
        "repeated_failure_rate": overall.get("repeated_failure_rate"),
        "horizon_reward_mean": overall.get("horizon_reward_mean"),
        "grounded_admission_rate": overall.get("grounded_admission_rate"),
        "time_to_correction_observed_count": overall.get(
            "time_to_correction_observed_count"
        ),
        "time_to_correction_censored_count": overall.get(
            "time_to_correction_censored_count"
        ),
        "invalid_commit_count": safety_counts.get("invalid_commit_count"),
        "evidence_destroying_repair_count": safety_counts.get(
            "evidence_destroying_repair_count"
        ),
        "orphaned_dependent_count": safety_counts.get("orphaned_dependent_count"),
        "bracket": overall.get("bracket"),
    }


def extract_pipeline_evidence(sources: Dict[str, Any]) -> Dict[str, Any]:
    reports = sources["mnemosyne_reports"]
    import_report = sources["r87_import_report"]
    score_report = sources["r88_score_report"]

    comparison = reports.get("r835b_comparison") or {}
    kernel_trace = reports.get("r835c_kernel_trace") or {}
    runtime = reports.get("r84_runtime_evaluator") or {}
    bridge = reports.get("r85_score_bridge") or {}
    handoff = reports.get("r86_scorer_handoff") or {}

    return {
        "manual_live_llm_pilot": {
            "source": "R83.5a",
            "status": "manual public-prompt response packs collected",
            "packs": sorted(score_report.get("pack_scores", {}).keys()),
        },
        "comparison_import": {
            "source": "R83.5b",
            "available": bool(comparison),
            "summary": {
                key: comparison.get(key)
                for key in (
                    "schema",
                    "num_records",
                    "num_responses",
                    "pack_summary",
                )
                if key in comparison
            },
        },
        "kernel_trace": {
            "source": "R83.5c",
            "available": bool(kernel_trace),
            "summary": {
                key: kernel_trace.get(key)
                for key in (
                    "schema",
                    "num_records",
                    "num_admitted",
                    "num_rejected",
                    "kernel_method_counts",
                )
                if key in kernel_trace
            },
        },
        "runtime_evaluator": {
            "source": "R84",
            "available": bool(runtime),
            "summary": {
                key: runtime.get(key)
                for key in (
                    "schema",
                    "num_records",
                    "num_failed",
                    "global_passed",
                )
                if key in runtime
            },
        },
        "score_bridge": {
            "source": "R85",
            "available": bool(bridge),
            "summary": {
                key: bridge.get(key)
                for key in (
                    "schema",
                    "num_records",
                    "official_realm_score",
                    "pack_summary",
                )
                if key in bridge
            },
        },
        "scorer_handoff": {
            "source": "R86",
            "available": bool(handoff),
            "summary": {
                "schema": handoff.get("schema"),
                "num_cases": len(handoff.get("cases", [])),
                "sequence_id": handoff.get("sequence_id"),
                "config_id": handoff.get("config_id"),
            },
        },
        "realm_import": {
            "source": "R87",
            "available": bool(import_report),
            "summary": {
                "schema": import_report.get("schema"),
                "num_cases": import_report.get("num_cases"),
                "num_validation_passed": import_report.get(
                    "num_validation_passed"
                ),
                "num_validation_failed": import_report.get(
                    "num_validation_failed"
                ),
                "all_cases_valid": import_report.get("all_cases_valid"),
            },
        },
        "realm_scoring": {
            "source": "R88",
            "available": bool(score_report),
            "summary": build_overall_summary(score_report),
        },
    }


def build_package(sources: Dict[str, Any]) -> Dict[str, Any]:
    score_report = sources["r88_score_report"]

    return {
        "schema": SCHEMA,
        "title": "Mnemosyne Live-LLM REALM Tier-6 Chapter 6 Pilot Evidence Package",
        "claim_boundary": (
            "R89 consolidates deterministic Mnemosyne and REALM-Bench pilot "
            "reports for AGI V3 Chapter 6. It supports an implementation and "
            "pilot-results narrative. It is not confirmatory-scale evidence."
        ),
        "chapter_use": {
            "ready_for_chapter_6_pilot_table": True,
            "ready_for_confirmatory_claims": False,
            "recommended_chapter_section": (
                "Chapter 6 implementation evidence and pilot scoring results"
            ),
        },
        "source_paths": sources["source_paths"],
        "overall_summary": build_overall_summary(score_report),
        "chapter_table": build_chapter_table(score_report),
        "pipeline_evidence": extract_pipeline_evidence(sources),
        "allowed_claims": [
            "Mnemosyne live-LLM handoff cases can be imported by REALM-Bench.",
            "The public REALM Tier-6 scorer can be invoked on schema-valid Mnemosyne handoff-derived events.",
            "In the one-sequence E7 pilot, the scoring integration produced safety-passed output.",
            "The pilot produced a horizon reward mean and grounded admission rate suitable for reporting as pilot evidence.",
        ],
        "disallowed_claims": [
            "final confirmatory Chapter 6 evidence",
            "general AGI achievement",
            "wisdom or autonomous scientific reasoning",
            "API-automated live LLM behavior",
            "production CTL-domain StateView realization",
            "full benchmark-scale statistical conclusion",
        ],
    }


def render_markdown(package: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R89 Mnemosyne Live-LLM Chapter 6 Evidence Package")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(package["claim_boundary"])
    lines.append("")
    lines.append("## Chapter 6 Readiness")
    lines.append("")
    chapter_use = package["chapter_use"]
    lines.append(
        f"- Ready for Chapter 6 pilot table: `{chapter_use['ready_for_chapter_6_pilot_table']}`"
    )
    lines.append(
        f"- Ready for confirmatory claims: `{chapter_use['ready_for_confirmatory_claims']}`"
    )
    lines.append(
        f"- Recommended section: {chapter_use['recommended_chapter_section']}"
    )
    lines.append("")
    lines.append("## Overall R88 Scoring Summary")
    lines.append("")
    summary = package["overall_summary"]
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    for key in (
        "official_scorer_invoked",
        "num_events",
        "safety_passed",
        "repeated_failure_rate",
        "horizon_reward_mean",
        "grounded_admission_rate",
        "time_to_correction_observed_count",
        "time_to_correction_censored_count",
        "invalid_commit_count",
        "evidence_destroying_repair_count",
        "orphaned_dependent_count",
    ):
        lines.append(f"| {key} | {summary.get(key)} |")

    lines.append("")
    lines.append("## Chapter 6 Pilot Results Table")
    lines.append("")
    lines.append(
        "| Model pack | Events | Safety | RFR | Horizon reward | Grounded admission | Invalid commits |"
    )
    lines.append("|---|---:|---|---:|---:|---:|---:|")
    for row in package["chapter_table"]:
        lines.append(
            f"| {row['display_name']} | {row['events']} | "
            f"{row['safety_passed']} | {row['repeated_failure_rate']} | "
            f"{row['horizon_reward_mean']} | {row['grounded_admission_rate']} | "
            f"{row['invalid_commit_count']} |"
        )

    lines.append("")
    lines.append("## Pipeline Evidence")
    lines.append("")
    for key, item in package["pipeline_evidence"].items():
        lines.append(f"### {item['source']}: {key}")
        lines.append("")
        lines.append(f"- Available: `{item.get('available', True)}`")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(item.get("summary", item), indent=2, sort_keys=True))
        lines.append("```")
        lines.append("")

    lines.append("## Allowed Claims")
    lines.append("")
    for claim in package["allowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Disallowed Claims")
    lines.append("")
    for claim in package["disallowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Chapter 6 Insert Draft")
    lines.append("")
    lines.append(
        "In the Tier-6 live-LLM pilot, Mnemosyne response packs were passed through "
        "a deterministic admission, kernel-trace, runtime-evaluation, scorer-handoff, "
        "and REALM-Bench import pipeline. The resulting schema-valid events were "
        "then scored by the public REALM Tier-6 scorer. Over 40 handoff-derived "
        "events in the E7 pilot sequence, the scorer integration reported safety "
        f"passed = `{summary.get('safety_passed')}`, horizon reward mean = "
        f"`{summary.get('horizon_reward_mean')}`, and grounded admission rate = "
        f"`{summary.get('grounded_admission_rate')}`. These results establish "
        "pilot integration evidence, not confirmatory-scale evidence."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sources = load_sources(
        score_report_path=Path(args.score_report),
        import_report_path=Path(args.import_report),
        mnemosyne_report_paths=DEFAULT_MNEMOSYNE_REPORTS,
    )
    package = build_package(sources)

    json_path = output_dir / "ch6_evidence_package.json"
    md_path = output_dir / "ch6_evidence_package.md"
    table_path = output_dir / "chapter6_pilot_results_table.json"

    json_path.write_text(
        json.dumps(package, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(package), encoding="utf-8")
    table_path.write_text(
        json.dumps(package["chapter_table"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "chapter_table": str(table_path),
                "ready_for_chapter_6_pilot_table": package["chapter_use"][
                    "ready_for_chapter_6_pilot_table"
                ],
                "ready_for_confirmatory_claims": package["chapter_use"][
                    "ready_for_confirmatory_claims"
                ],
                "num_events": package["overall_summary"]["num_events"],
                "safety_passed": package["overall_summary"]["safety_passed"],
                "horizon_reward_mean": package["overall_summary"][
                    "horizon_reward_mean"
                ],
                "grounded_admission_rate": package["overall_summary"][
                    "grounded_admission_rate"
                ],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build Chapter 6 evidence package")
    build_cmd.add_argument("--score-report", default=DEFAULT_SCORE_REPORT)
    build_cmd.add_argument("--import-report", default=DEFAULT_IMPORT_REPORT)
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
