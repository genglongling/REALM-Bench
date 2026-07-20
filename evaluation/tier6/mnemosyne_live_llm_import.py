#!/usr/bin/env python3
"""R87 Mnemosyne live-LLM scorer handoff importer for REALM Tier 6.

This module consumes the Mnemosyne R86 handoff bundle and produces a deterministic
REALM-Bench-side import report.

Claim boundary:
R87 phase 1 validates and imports Mnemosyne live-LLM scorer handoff cases into a
REALM-facing report. It does not yet claim final confirmatory Chapter 6 scoring,
API-automated LLM execution, or production CTL-domain realization.
"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from pathlib import Path
from typing import Any


DEFAULT_MNEMOSYNE_BUNDLE = (
    "/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/"
    "results/realm_tier6_live_llm_manual/realm_scorer_handoff/"
    "realm_scorer_handoff_bundle.json"
)

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/mnemosyne_live_llm_scorer_import"

SCHEMA = "realm_tier6_mnemosyne_live_llm_import_report_v0"
CASE_SCHEMA = "realm_tier6_mnemosyne_live_llm_import_case_v0"

VALID_SCORER_ACTIONS = {
    "score_admitted_proposal",
    "score_admitted_with_grounding_flags",
    "score_rejection_as_protective_screening",
    "score_as_safety_failure",
    "score_rejection",
    "score_unknown",
}

VALID_ADMISSION_LABELS = {
    "clean_admission",
    "flagged_admission",
    "protective_rejection",
    "unsafe_admission",
    "rejected",
    "unknown",
}


def deterministic_id(kind: str, *parts: object) -> str:
    seed = ":".join([kind, *[str(part) for part in parts]])
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data


def resolve_default_bundle() -> Path:
    env_path = os.environ.get("MNEMOSYNE_REALM_HANDOFF_BUNDLE")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_MNEMOSYNE_BUNDLE)


def validate_handoff_case(case: dict[str, Any]) -> list[dict[str, Any]]:
    admission = case.get("mnemosyne_admission", {})
    handoff = case.get("realm_scorer_handoff", {})

    checks: list[dict[str, Any]] = []

    checks.append(
        {
            "name": "case_id_present",
            "passed": bool(case.get("case_id")),
            "detail": {"case_id": case.get("case_id")},
        }
    )

    checks.append(
        {
            "name": "episode_id_present",
            "passed": isinstance(case.get("episode_id"), int),
            "detail": {"episode_id": case.get("episode_id")},
        }
    )

    checks.append(
        {
            "name": "pack_name_present",
            "passed": bool(case.get("pack_name")),
            "detail": {"pack_name": case.get("pack_name")},
        }
    )

    label = admission.get("label")
    checks.append(
        {
            "name": "valid_admission_label",
            "passed": label in VALID_ADMISSION_LABELS,
            "detail": {"label": label},
        }
    )

    action = handoff.get("scorer_action")
    checks.append(
        {
            "name": "valid_scorer_action",
            "passed": action in VALID_SCORER_ACTIONS,
            "detail": {"scorer_action": action},
        }
    )

    checks.append(
        {
            "name": "official_score_not_claimed",
            "passed": handoff.get("official_realm_score") is False,
            "detail": {"official_realm_score": handoff.get("official_realm_score")},
        }
    )

    checks.append(
        {
            "name": "requires_official_scorer",
            "passed": handoff.get("requires_official_realm_scorer") is True,
            "detail": {
                "requires_official_realm_scorer": handoff.get(
                    "requires_official_realm_scorer"
                )
            },
        }
    )

    return checks


def realm_import_disposition(case: dict[str, Any]) -> str:
    """Map Mnemosyne handoff action to REALM-side import disposition."""
    action = case.get("realm_scorer_handoff", {}).get("scorer_action")

    if action == "score_admitted_proposal":
        return "eligible_for_official_realm_admitted_scoring"
    if action == "score_admitted_with_grounding_flags":
        return "eligible_for_official_realm_flagged_scoring"
    if action == "score_rejection_as_protective_screening":
        return "eligible_for_official_realm_protective_rejection_scoring"
    if action == "score_as_safety_failure":
        return "eligible_for_official_realm_safety_failure_scoring"
    if action == "score_rejection":
        return "eligible_for_official_realm_rejection_scoring"
    return "requires_manual_review_before_official_scoring"


def build_import_case(bundle: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    checks = validate_handoff_case(case)
    passed = all(check["passed"] for check in checks)

    admission = case.get("mnemosyne_admission", {})
    handoff = case.get("realm_scorer_handoff", {})

    import_id = deterministic_id(
        "realm-tier6-mnemosyne-live-llm-import-case",
        bundle.get("sequence_id"),
        bundle.get("config_id"),
        case.get("pack_name"),
        case.get("episode_id"),
        case.get("case_id"),
    )

    return {
        "schema": CASE_SCHEMA,
        "import_id": import_id,
        "source_case_id": case.get("case_id"),
        "sequence_id": case.get("sequence_id"),
        "config_id": case.get("config_id"),
        "condition_label": case.get("condition_label"),
        "pack_name": case.get("pack_name"),
        "episode_id": case.get("episode_id"),
        "mnemosyne_admission_label": admission.get("label"),
        "mnemosyne_admitted": admission.get("admitted"),
        "mnemosyne_rejected": admission.get("rejected"),
        "grounding_flags": admission.get("grounding_flags", []),
        "unsupported_specificity_count": admission.get(
            "unsupported_specificity_count"
        ),
        "policy_style": admission.get("policy_style"),
        "realm_scorer_action": handoff.get("scorer_action"),
        "realm_import_disposition": realm_import_disposition(case),
        "safety_passed_before_official_scoring": handoff.get(
            "safety_passed_before_official_scoring"
        ),
        "screened_before_commit": handoff.get("screened_before_commit"),
        "proposal_summary": handoff.get("proposal_summary", ""),
        "validation_checks": checks,
        "validation_passed": passed,
    }


def build_import_report(bundle: dict[str, Any]) -> dict[str, Any]:
    cases = list(bundle.get("cases", []))
    imported_cases = [build_import_case(bundle, case) for case in cases]

    pack_summary: dict[str, dict[str, Any]] = {}
    disposition_counts: dict[str, int] = {}

    for item in imported_cases:
        pack_name = str(item["pack_name"])
        disposition = str(item["realm_import_disposition"])
        label = str(item["mnemosyne_admission_label"])

        pack_entry = pack_summary.setdefault(
            pack_name,
            {
                "cases": 0,
                "validation_passed": 0,
                "validation_failed": 0,
                "admission_labels": {},
                "dispositions": {},
            },
        )

        pack_entry["cases"] += 1
        pack_entry["validation_passed"] += 1 if item["validation_passed"] else 0
        pack_entry["validation_failed"] += 0 if item["validation_passed"] else 1
        pack_entry["admission_labels"][label] = (
            pack_entry["admission_labels"].get(label, 0) + 1
        )
        pack_entry["dispositions"][disposition] = (
            pack_entry["dispositions"].get(disposition, 0) + 1
        )

        disposition_counts[disposition] = disposition_counts.get(disposition, 0) + 1

    num_passed = sum(1 for item in imported_cases if item["validation_passed"])
    num_failed = len(imported_cases) - num_passed

    return {
        "schema": SCHEMA,
        "source_schema": bundle.get("schema"),
        "claim_boundary": (
            "REALM-Bench-side deterministic import report only. "
            "This consumes the Mnemosyne R86 handoff bundle and validates "
            "official-scorer-facing cases. It does not yet claim final official "
            "REALM scoring or confirmatory Chapter 6 evidence."
        ),
        "sequence_id": bundle.get("sequence_id"),
        "config_id": bundle.get("config_id"),
        "condition_label": bundle.get("condition_label"),
        "official_realm_score": False,
        "import_type": "mnemosyne_live_llm_scorer_handoff_import",
        "num_cases": len(imported_cases),
        "num_validation_passed": num_passed,
        "num_validation_failed": num_failed,
        "all_cases_valid": num_failed == 0,
        "disposition_counts": disposition_counts,
        "pack_summary": pack_summary,
        "cases": imported_cases,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("# R87 REALM Tier-6 Mnemosyne Live-LLM Scorer Import")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Imported Pilot")
    lines.append("")
    lines.append(f"- Sequence: `{report['sequence_id']}`")
    lines.append(f"- Config: `{report['config_id']}`")
    lines.append(f"- Condition label: `{report['condition_label']}`")
    lines.append(f"- Official REALM score: `{report['official_realm_score']}`")
    lines.append(f"- Import type: `{report['import_type']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Cases: `{report['num_cases']}`")
    lines.append(f"- Validation passed: `{report['num_validation_passed']}`")
    lines.append(f"- Validation failed: `{report['num_validation_failed']}`")
    lines.append(f"- All cases valid: `{report['all_cases_valid']}`")
    lines.append("")
    lines.append("## Disposition Counts")
    lines.append("")
    lines.append("| Disposition | Count |")
    lines.append("|---|---:|")
    for disposition, count in sorted(report["disposition_counts"].items()):
        lines.append(f"| {disposition} | {count} |")

    lines.append("")
    lines.append("## Pack Summary")
    lines.append("")
    lines.append("| Pack | Cases | Passed | Failed | Admission labels | Dispositions |")
    lines.append("|---|---:|---:|---:|---|---|")
    for pack_name, item in report["pack_summary"].items():
        lines.append(
            f"| {pack_name} | {item['cases']} | "
            f"{item['validation_passed']} | {item['validation_failed']} | "
            f"`{item['admission_labels']}` | `{item['dispositions']}` |"
        )

    lines.append("")
    lines.append("## Per-Case Import")
    lines.append("")
    lines.append("| Pack | Episode | Valid | Admission label | Scorer action | Import disposition | Unsupported | Summary |")
    lines.append("|---|---:|---|---|---|---|---:|---|")
    for item in report["cases"]:
        summary = str(item.get("proposal_summary", "")).replace("|", "\\|")
        if len(summary) > 100:
            summary = summary[:97] + "..."
        lines.append(
            f"| {item['pack_name']} | {item['episode_id']} | "
            f"{item['validation_passed']} | {item['mnemosyne_admission_label']} | "
            f"{item['realm_scorer_action']} | {item['realm_import_disposition']} | "
            f"{item['unsupported_specificity_count']} | {summary} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "This report verifies that the Mnemosyne R86 handoff bundle can be consumed "
        "on the REALM-Bench side and converted into deterministic official-scorer-facing "
        "import cases."
    )
    lines.append("")
    lines.append(
        "The next step is to connect these imported cases to the actual Tier-6 scorer "
        "rather than only validating the handoff contract."
    )
    lines.append("")

    return "\n".join(lines)


def cmd_import(args: argparse.Namespace) -> None:
    handoff_path = Path(args.handoff_bundle)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle = load_json(handoff_path)
    report = build_import_report(bundle)

    json_path = output_dir / "mnemosyne_live_llm_import_report.json"
    md_path = output_dir / "mnemosyne_live_llm_import_report.md"

    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print(
        json.dumps(
            {
                "handoff_bundle": str(handoff_path),
                "output_dir": str(output_dir),
                "json": str(json_path),
                "markdown": str(md_path),
                "num_cases": report["num_cases"],
                "num_validation_passed": report["num_validation_passed"],
                "num_validation_failed": report["num_validation_failed"],
                "all_cases_valid": report["all_cases_valid"],
                "official_realm_score": report["official_realm_score"],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    import_cmd = sub.add_parser("import", help="import Mnemosyne R86 handoff bundle")
    import_cmd.add_argument(
        "--handoff-bundle",
        default=str(resolve_default_bundle()),
    )
    import_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    import_cmd.set_defaults(func=cmd_import)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
