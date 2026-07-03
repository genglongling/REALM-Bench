#!/usr/bin/env python3
"""R94 final Chapter 6 closure ledger.

This module consolidates R89-R93 into a final evidence ledger for AGI V3
Chapter 6. It does not add new experiments. It closes the chapter by separating
completed evidence, bounded pilot evidence, and future non-claims.

Claim boundary:
R94 supports Chapter 6 closure as deterministic baseline + CRT ablation +
family-stratified baseline + bounded live-LLM pilot evidence. It does not claim
confirmatory-scale benchmark evidence, family-generalized live-LLM evidence,
API-automated live-LLM evidence, production CTL-domain realization, AGI, wisdom,
or autonomous scientific reasoning.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


SCHEMA = "realm_tier6_chapter6_closure_ledger_v0"

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/chapter6_closure_ledger"

DEFAULT_SOURCE_PATHS = {
    "R89_ch6_package": (
        "runs/realm_tier6/mnemosyne_live_llm_ch6_package/"
        "ch6_evidence_package.json"
    ),
    "R90_full_deterministic": (
        "runs/realm_tier6/full_deterministic_report/"
        "full_deterministic_report.json"
    ),
    "R91_crt_ablation": (
        "runs/realm_tier6/crt_ablation_report/"
        "crt_ablation_report.json"
    ),
    "R92_family_stratified": (
        "runs/realm_tier6/family_stratified_report/"
        "family_stratified_report.json"
    ),
    "R93_expanded_live_llm_plan": (
        "runs/realm_tier6/expanded_live_llm_pilot_plan/"
        "expanded_live_llm_pilot_plan.json"
    ),
}


def read_json(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def load_sources(source_paths: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    sources: Dict[str, Dict[str, Any]] = {}
    for key, raw_path in source_paths.items():
        path = Path(raw_path)
        if not path.exists():
            raise FileNotFoundError(f"missing required R94 source {key}: {path}")
        sources[key] = read_json(path)
    return sources


def extract_r89_summary(source: Dict[str, Any]) -> Dict[str, Any]:
    overall = source.get("overall_summary", {})
    chapter_use = source.get("chapter_use", {})
    return {
        "ready_for_chapter_6_pilot_table": chapter_use.get(
            "ready_for_chapter_6_pilot_table"
        ),
        "ready_for_confirmatory_claims": chapter_use.get(
            "ready_for_confirmatory_claims"
        ),
        "num_events": overall.get("num_events"),
        "safety_passed": overall.get("safety_passed"),
        "horizon_reward_mean": overall.get("horizon_reward_mean"),
        "grounded_admission_rate": overall.get("grounded_admission_rate"),
    }


def extract_r90_summary(source: Dict[str, Any]) -> Dict[str, Any]:
    dev = source.get("development_set", {})
    table = source.get("chapter6_table", [])
    return {
        "num_sequences": dev.get("num_sequences"),
        "num_episodes": dev.get("num_episodes"),
        "families": dev.get("families"),
        "num_table_rows": len(table),
        "has_b0": any(row.get("system_id") == "B0_memoryless_replay" for row in table),
        "has_bstar": any(row.get("system_id") == "Bstar_oracle_memory" for row in table),
        "has_live_llm_pilot": any(
            row.get("system_id") == "mnemosyne_live_llm_r88_pilot"
            for row in table
        ),
    }


def extract_r91_summary(source: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "available_configs": source.get("available_configs", []),
        "missing_configs": source.get("missing_configs", []),
        "all_required_configs_available": source.get(
            "all_required_configs_available"
        ),
        "e7_summary": source.get("e7_summary"),
    }


def extract_r92_summary(source: Dict[str, Any]) -> Dict[str, Any]:
    table = source.get("chapter6_family_table", [])
    return {
        "families": source.get("families", []),
        "r88_live_llm_pilot_available": source.get(
            "r88_live_llm_pilot_available"
        ),
        "num_family_table_rows": source.get("num_family_table_rows", len(table)),
        "live_pilot_family": source.get("live_pilot_family"),
    }


def extract_r93_summary(source: Dict[str, Any]) -> Dict[str, Any]:
    status = source.get("chapter6_status", {})
    matrix = source.get("matrix_summary", {})
    return {
        "bounded_pilot_ready": status.get("bounded_pilot_ready"),
        "family_generalized_live_llm_ready": status.get(
            "family_generalized_live_llm_ready"
        ),
        "additional_cases_needed_for_three_family_live_pilot": status.get(
            "additional_cases_needed_for_three_family_live_pilot"
        ),
        "total_target_cases": matrix.get("total_cases"),
        "existing_r88_collected": matrix.get("existing_r88_collected"),
        "planned_not_collected": matrix.get("planned_not_collected"),
    }


def build_closure_checks(summaries: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    r89 = summaries["R89_ch6_package"]
    r90 = summaries["R90_full_deterministic"]
    r91 = summaries["R91_crt_ablation"]
    r92 = summaries["R92_family_stratified"]
    r93 = summaries["R93_expanded_live_llm_plan"]

    checks = [
        {
            "name": "pilot_table_ready",
            "passed": r89.get("ready_for_chapter_6_pilot_table") is True,
            "evidence": r89,
        },
        {
            "name": "confirmatory_claims_not_ready",
            "passed": r89.get("ready_for_confirmatory_claims") is False,
            "evidence": r89,
        },
        {
            "name": "live_llm_pilot_safety_passed",
            "passed": r89.get("safety_passed") is True,
            "evidence": r89,
        },
        {
            "name": "deterministic_baselines_present",
            "passed": r90.get("has_b0") is True and r90.get("has_bstar") is True,
            "evidence": r90,
        },
        {
            "name": "full_deterministic_development_shape_present",
            "passed": r90.get("num_sequences") == 15 and r90.get("num_episodes") == 150,
            "evidence": r90,
        },
        {
            "name": "crt_ablation_configs_present",
            "passed": (
                r91.get("all_required_configs_available") is True
                and isinstance(r91.get("e7_summary"), dict)
                and r91["e7_summary"].get("repeated_failure_rate") is not None
                and r91["e7_summary"].get("horizon_reward_mean") is not None
            ),
            "evidence": r91,
        },
        {
            "name": "family_stratified_baselines_present",
            "passed": len(r92.get("families", [])) >= 3
            and r92.get("num_family_table_rows", 0) >= 6,
            "evidence": r92,
        },
        {
            "name": "bounded_live_llm_pilot_expansion_gate_present",
            "passed": r93.get("bounded_pilot_ready") is True
            and r93.get("family_generalized_live_llm_ready") is False,
            "evidence": r93,
        },
        {
            "name": "additional_live_llm_cases_are_explicit",
            "passed": isinstance(
                r93.get("additional_cases_needed_for_three_family_live_pilot"),
                int,
            ),
            "evidence": r93,
        },
    ]

    return checks


def build_ledger(sources: Dict[str, Dict[str, Any]], source_paths: Dict[str, str]) -> Dict[str, Any]:
    summaries = {
        "R89_ch6_package": extract_r89_summary(sources["R89_ch6_package"]),
        "R90_full_deterministic": extract_r90_summary(
            sources["R90_full_deterministic"]
        ),
        "R91_crt_ablation": extract_r91_summary(sources["R91_crt_ablation"]),
        "R92_family_stratified": extract_r92_summary(
            sources["R92_family_stratified"]
        ),
        "R93_expanded_live_llm_plan": extract_r93_summary(
            sources["R93_expanded_live_llm_plan"]
        ),
    }

    checks = build_closure_checks(summaries)
    closed = all(check["passed"] for check in checks)

    return {
        "schema": SCHEMA,
        "title": "Chapter 6 REALM Tier-6 Closure Ledger",
        "source_paths": source_paths,
        "claim_boundary": (
            "Chapter 6 is closed as deterministic baseline, CRT ablation, "
            "family-stratified deterministic baseline, and bounded live-LLM pilot "
            "evidence. It is not closed as confirmatory-scale, family-generalized "
            "live-LLM, API-automated, or production CTL-domain evidence."
        ),
        "chapter6_closed_for_book": closed,
        "closure_mode": "bounded_pilot_plus_deterministic_evidence",
        "summaries": summaries,
        "closure_checks": checks,
        "chapter6_allowed_claims": [
            "REALM-Bench Tier 6 extends the benchmark to cross-episode causal-loop recovery.",
            "The public Tier-6 deterministic development set is scored with B0 and B* reference anchors.",
            "Mnemosyne produces bounded live-LLM pilot evidence through admission, kernel trace, runtime replay, handoff, import, and Tier-6 scoring.",
            "The CRT stack has deterministic ablation evidence over E0/E2/E3/E7.",
            "The deterministic baseline layer is family-stratified across jobshop, routing, and wedding recovery families.",
            "Chapter 6 closes as a realized pilot-and-baseline implementation chapter.",
        ],
        "chapter6_disallowed_claims": [
            "confirmatory-scale benchmark proof",
            "family-generalized live-LLM result across all families",
            "API-automated live-LLM evaluation",
            "production CTL-domain StateView realization",
            "proof of AGI",
            "proof of wisdom",
            "proof of autonomous scientific reasoning",
        ],
        "book_update_targets": [
            "Chapter 6 results subsection",
            "Chapter 6 claim-boundary paragraph",
            "Chapter 6 closing paragraph",
            "results ledger",
            "Part II opener claim alignment",
            "Chapter 1 claims register",
            "REALM-Bench tier description in Chapter 4 or benchmark overview",
        ],
    }


def render_markdown(ledger: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R94 Chapter 6 Closure Ledger")
    lines.append("")
    lines.append("## Closure Decision")
    lines.append("")
    lines.append(f"- Chapter 6 closed for book: `{ledger['chapter6_closed_for_book']}`")
    lines.append(f"- Closure mode: `{ledger['closure_mode']}`")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(ledger["claim_boundary"])
    lines.append("")
    lines.append("## Evidence Summary")
    lines.append("")
    for key, summary in ledger["summaries"].items():
        lines.append(f"### {key}")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(summary, indent=2, sort_keys=True))
        lines.append("```")
        lines.append("")

    lines.append("## Closure Checks")
    lines.append("")
    lines.append("| Check | Passed |")
    lines.append("|---|---|")
    for check in ledger["closure_checks"]:
        lines.append(f"| {check['name']} | {check['passed']} |")

    lines.append("")
    lines.append("## Chapter 6 Allowed Claims")
    lines.append("")
    for claim in ledger["chapter6_allowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Chapter 6 Disallowed Claims")
    lines.append("")
    for claim in ledger["chapter6_disallowed_claims"]:
        lines.append(f"- {claim}")

    lines.append("")
    lines.append("## Book Update Targets")
    lines.append("")
    for target in ledger["book_update_targets"]:
        lines.append(f"- {target}")

    lines.append("")
    lines.append("## Final Chapter 6 Insert Draft")
    lines.append("")
    r89 = ledger["summaries"]["R89_ch6_package"]
    r90 = ledger["summaries"]["R90_full_deterministic"]
    r91 = ledger["summaries"]["R91_crt_ablation"]
    r92 = ledger["summaries"]["R92_family_stratified"]
    r93 = ledger["summaries"]["R93_expanded_live_llm_plan"]

    lines.append(
        "The realized Chapter 6 evaluation closes at the level of bounded "
        "pilot-plus-deterministic evidence. The Tier-6 development set contains "
        f"`{r90.get('num_sequences')}` sequences and `{r90.get('num_episodes')}` "
        "episodes, scored against B0 memoryless replay and B* oracle memory "
        "anchors. The Mnemosyne live-LLM pilot contributes "
        f"`{r89.get('num_events')}` handoff-derived scorer events, with safety "
        f"passed = `{r89.get('safety_passed')}`, horizon reward mean = "
        f"`{r89.get('horizon_reward_mean')}`, and grounded admission rate = "
        f"`{r89.get('grounded_admission_rate')}`. The CRT ablation layer covers "
        f"`{', '.join(r91.get('available_configs', []))}`, and the deterministic "
        f"baseline layer is stratified across `{', '.join(r92.get('families', []))}`. "
        "An expanded three-family live-LLM pilot remains future work: R93 "
        f"identifies `{r93.get('additional_cases_needed_for_three_family_live_pilot')}` "
        "additional cases needed before family-generalized live-LLM evidence can "
        "be claimed."
    )
    lines.append("")

    lines.append(
        "Thus Chapter 6 may claim that the infrastructure arc has been realized: "
        "public Tier-6 scoring, deterministic baselines, Mnemosyne admission and "
        "runtime replay, CRT ablation, family-stratified deterministic anchors, "
        "and a bounded live-LLM pilot. It must not claim confirmatory-scale "
        "benchmark proof, family-generalized live-LLM behavior, API automation, "
        "or production CTL-domain realization."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    source_paths = dict(DEFAULT_SOURCE_PATHS)
    sources = load_sources(source_paths)
    ledger = build_ledger(sources, source_paths)

    json_path = output_dir / "chapter6_closure_ledger.json"
    md_path = output_dir / "chapter6_closure_ledger.md"
    checks_path = output_dir / "chapter6_closure_checks.json"

    json_path.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(ledger), encoding="utf-8")
    checks_path.write_text(
        json.dumps(ledger["closure_checks"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "checks": str(checks_path),
                "chapter6_closed_for_book": ledger["chapter6_closed_for_book"],
                "closure_mode": ledger["closure_mode"],
                "num_checks": len(ledger["closure_checks"]),
                "num_failed_checks": sum(
                    1 for check in ledger["closure_checks"] if not check["passed"]
                ),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build final Chapter 6 closure ledger")
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
