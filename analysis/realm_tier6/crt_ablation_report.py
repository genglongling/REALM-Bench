#!/usr/bin/env python3
"""R91 CRT-stack ablation report for Chapter 6.

This report imports Mnemosyne deterministic Tier-6 adapter results for E0/E2/E3/E7
and builds a Chapter 6 CRT ablation table.

Claim boundary:
R91 reports deterministic CRT-stack ablation evidence from the Mnemosyne
Tier-6 adapter/kernel results. It does not claim API-automated LLM behavior,
production CTL-domain realization, or confirmatory-scale evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List


SCHEMA = "realm_tier6_crt_ablation_report_v0"

DEFAULT_OUTPUT_DIR = "runs/realm_tier6/crt_ablation_report"

MNEMOSYNE_ROOT = Path("/Users/edward.chang/ALAS/AGIV3/mnemosyne_product")

DEFAULT_SEARCH_ROOTS = [
    MNEMOSYNE_ROOT / "results/realm_tier6_mnemosyne_kernel",
    MNEMOSYNE_ROOT / "results/realm_tier6_mnemosyne_runtime",
    MNEMOSYNE_ROOT / "results/realm_tier6_mnemosyne",
]

CONFIG_ORDER = ["E0", "E2", "E3", "E7"]

CONFIG_LABELS = {
    "E0": "Engine only",
    "E2": "+R causal audit",
    "E3": "+T temporal accountability",
    "E7": "+C+R+T full stack",
}

CONFIG_SWITCHES = {
    "E0": {"A": 0, "C": 0, "R": 0, "T": 0},
    "E2": {"A": 0, "C": 0, "R": 1, "T": 0},
    "E3": {"A": 0, "C": 0, "R": 0, "T": 1},
    "E7": {"A": 0, "C": 1, "R": 1, "T": 1},
}

METRIC_KEYS = {
    "num_events",
    "safety_passed",
    "repeated_failure_rate",
    "horizon_reward_mean",
    "grounded_admission_rate",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_json_files(roots: Iterable[Path]) -> Iterable[Path]:
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.json")):
            if path.is_file():
                yield path


def looks_like_metric_record(value: Dict[str, Any]) -> bool:
    return bool(set(value) & METRIC_KEYS) and (
        "config_id" in value
        or "config" in value
        or "condition" in value
        or "summary" in value
    )


def normalize_config_id(value: Any) -> str | None:
    if isinstance(value, str) and value in CONFIG_ORDER:
        return value
    return None


def infer_config_id(path: Path, value: Dict[str, Any]) -> str | None:
    for key in ("config_id", "config"):
        config = normalize_config_id(value.get(key))
        if config:
            return config

    # Prefer path-derived config ids when summaries live under directories such
    # as mnemosyne_tier6_E7_kernel_adapter_v0/summary.json.
    path_text = "/".join(path.parts)
    tokens = re.split(r"[^A-Za-z0-9]+", path_text)
    for token in tokens:
        config = normalize_config_id(token)
        if config:
            return config

    return None

def normalize_metric_value(value: Any) -> Any:
    if isinstance(value, float):
        if math.isnan(value):
            return None
        return value
    return value


def metric_record_from_dict(
    *,
    path: Path,
    config_id: str,
    value: Dict[str, Any],
) -> Dict[str, Any] | None:
    summary = value.get("summary") if isinstance(value.get("summary"), dict) else value

    if not isinstance(summary, dict):
        return None

    if not set(summary) & METRIC_KEYS:
        return None

    return {
        "source_path": str(path),
        "config_id": config_id,
        "num_events": normalize_metric_value(summary.get("num_events")),
        "safety_passed": normalize_metric_value(summary.get("safety_passed")),
        "repeated_failure_rate": normalize_metric_value(
            summary.get("repeated_failure_rate")
        ),
        "horizon_reward_mean": normalize_metric_value(
            summary.get("horizon_reward_mean")
        ),
        "grounded_admission_rate": normalize_metric_value(
            summary.get("grounded_admission_rate")
        ),
        "raw_keys": sorted(summary.keys()),
    }


def walk_records(path: Path, value: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(value, dict):
        direct_config = infer_config_id(path, value)

        if direct_config:
            record = metric_record_from_dict(
                path=path,
                config_id=direct_config,
                value=value,
            )
            if record:
                yield record

        for key, child in value.items():
            key_config = normalize_config_id(key)
            if key_config and isinstance(child, dict):
                record = metric_record_from_dict(
                    path=path,
                    config_id=key_config,
                    value=child,
                )
                if record:
                    yield record

            yield from walk_records(path, child)

    elif isinstance(value, list):
        for child in value:
            yield from walk_records(path, child)


def collect_candidate_records(search_roots: List[Path]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    for path in iter_json_files(search_roots):
        try:
            value = read_json(path)
        except Exception:
            continue

        records.extend(walk_records(path, value))

    return records


def completeness_score(record: Dict[str, Any]) -> int:
    score = 0
    for key in (
        "num_events",
        "safety_passed",
        "repeated_failure_rate",
        "horizon_reward_mean",
        "grounded_admission_rate",
    ):
        if record.get(key) is not None:
            score += 1

    source = record.get("source_path", "")

    # Prefer actual scorer summaries over manifests. Manifests often contain
    # config_id and num_events but not the Tier-6 metrics needed by Chapter 6.
    if source.endswith("/summary.json"):
        score += 8
    if source.endswith("/manifest.json"):
        score -= 8

    if "kernel" in source:
        score += 3
    if "runtime" in source:
        score += 1

    return score

def select_best_records(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    selected: Dict[str, Dict[str, Any]] = {}

    for record in records:
        config_id = record["config_id"]
        if config_id not in CONFIG_ORDER:
            continue

        current = selected.get(config_id)
        if current is None or completeness_score(record) > completeness_score(current):
            selected[config_id] = record

    return selected


def bracket_position_rfr(value: float | None) -> float | None:
    if value is None:
        return None
    return max(0.0, min(1.0, 1.0 - float(value)))


def bracket_position_horizon(value: float | None) -> float | None:
    if value is None:
        return None
    return max(0.0, min(1.0, float(value)))


def delta(value: float | None, base: float | None) -> float | None:
    if value is None or base is None:
        return None
    return float(value) - float(base)


def build_ablation_table(selected: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    e0 = selected.get("E0", {})
    e0_rfr = e0.get("repeated_failure_rate")
    e0_horizon = e0.get("horizon_reward_mean")

    rows: List[Dict[str, Any]] = []

    for config_id in CONFIG_ORDER:
        record = selected.get(config_id)
        if not record:
            rows.append(
                {
                    "config_id": config_id,
                    "label": CONFIG_LABELS[config_id],
                    "switches": CONFIG_SWITCHES[config_id],
                    "available": False,
                }
            )
            continue

        rfr = record.get("repeated_failure_rate")
        horizon = record.get("horizon_reward_mean")

        rows.append(
            {
                "config_id": config_id,
                "label": CONFIG_LABELS[config_id],
                "switches": CONFIG_SWITCHES[config_id],
                "available": True,
                "source_path": record.get("source_path"),
                "num_events": record.get("num_events"),
                "safety_passed": record.get("safety_passed"),
                "repeated_failure_rate": rfr,
                "horizon_reward_mean": horizon,
                "grounded_admission_rate": record.get("grounded_admission_rate"),
                "rfr_bracket_position": bracket_position_rfr(rfr),
                "horizon_bracket_position": bracket_position_horizon(horizon),
                "delta_rfr_vs_e0": delta(rfr, e0_rfr),
                "delta_horizon_vs_e0": delta(horizon, e0_horizon),
            }
        )

    return rows


def build_report(search_roots: List[Path]) -> Dict[str, Any]:
    candidates = collect_candidate_records(search_roots)
    selected = select_best_records(candidates)
    table = build_ablation_table(selected)

    available_configs = [
        row["config_id"]
        for row in table
        if row.get("available") is True
    ]

    e7 = next((row for row in table if row["config_id"] == "E7"), None)

    return {
        "schema": SCHEMA,
        "claim_boundary": (
            "R91 imports deterministic Mnemosyne Tier-6 adapter/kernel results "
            "and reports CRT-stack ablations for E0/E2/E3/E7. It supports "
            "Chapter 6 ablation evidence, not confirmatory-scale evidence."
        ),
        "search_roots": [str(path) for path in search_roots],
        "num_candidate_records": len(candidates),
        "available_configs": available_configs,
        "missing_configs": [
            config for config in CONFIG_ORDER if config not in available_configs
        ],
        "all_required_configs_available": set(available_configs) >= set(CONFIG_ORDER),
        "chapter6_table": table,
        "e7_summary": e7,
        "allowed_claims": [
            "The deterministic Mnemosyne Tier-6 adapter results support an E0/E2/E3/E7 CRT ablation table.",
            "E7 can be compared against E0 to quantify full-stack improvement in repeated-failure and horizon-reward metrics.",
            "E2 and E3 isolate causal-audit and temporal-accountability contributions within the deterministic adapter setting.",
        ],
        "disallowed_claims": [
            "confirmatory-scale benchmark evidence",
            "API-automated LLM behavior",
            "production CTL-domain StateView realization",
            "proof of AGI, wisdom, or autonomous scientific reasoning",
        ],
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = []

    lines.append("# R91 CRT-Stack Ablation Report")
    lines.append("")
    lines.append("## Claim Boundary")
    lines.append("")
    lines.append(report["claim_boundary"])
    lines.append("")
    lines.append("## Source Availability")
    lines.append("")
    lines.append(f"- Candidate records: `{report['num_candidate_records']}`")
    lines.append(f"- Available configs: `{', '.join(report['available_configs'])}`")
    lines.append(f"- Missing configs: `{', '.join(report['missing_configs'])}`")
    lines.append(
        f"- All required configs available: `{report['all_required_configs_available']}`"
    )
    lines.append("")
    lines.append("## Chapter 6 CRT Ablation Table")
    lines.append("")
    lines.append(
        "| Config | Stack | Safety | RFR | Horizon reward | Grounded admission | "
        "RFR bracket | Horizon bracket | ΔRFR vs E0 | ΔHorizon vs E0 |"
    )
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")

    for row in report["chapter6_table"]:
        if not row.get("available"):
            lines.append(
                f"| {row['config_id']} | {row['label']} | missing |  |  |  |  |  |  |  |"
            )
            continue

        lines.append(
            f"| {row['config_id']} | {row['label']} | {row['safety_passed']} | "
            f"{row['repeated_failure_rate']} | {row['horizon_reward_mean']} | "
            f"{row['grounded_admission_rate']} | {row['rfr_bracket_position']} | "
            f"{row['horizon_bracket_position']} | {row['delta_rfr_vs_e0']} | "
            f"{row['delta_horizon_vs_e0']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "R91 isolates the contribution of the CRT stack by comparing engine-only "
        "execution against causal audit, temporal accountability, and the full "
        "C+R+T stack."
    )
    lines.append("")
    lines.append(
        "For Chapter 6, this table explains not only that the Tier-6 pipeline works, "
        "but which recovery-control components produce the measured improvement."
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
    e7 = report.get("e7_summary") or {}
    if e7 and e7.get("available"):
        lines.append(
            "The CRT ablation compares E0, E2, E3, and E7 under the deterministic "
            "Mnemosyne Tier-6 adapter setting. The full E7 stack reports repeated "
            f"failure rate `{e7.get('repeated_failure_rate')}`, horizon reward "
            f"`{e7.get('horizon_reward_mean')}`, and grounded admission rate "
            f"`{e7.get('grounded_admission_rate')}`. Relative to E0, this provides "
            "the ablation layer needed to attribute Chapter 6's recovery behavior "
            "to the CRT controls rather than to the benchmark harness alone."
        )
    else:
        lines.append(
            "The CRT ablation table was generated, but E7 was not available from "
            "the searched Mnemosyne result roots."
        )
    lines.append("")

    return "\n".join(lines)


def cmd_build(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    search_roots = [Path(path) for path in args.search_roots]
    report = build_report(search_roots)

    json_path = output_dir / "crt_ablation_report.json"
    md_path = output_dir / "crt_ablation_report.md"
    table_path = output_dir / "chapter6_crt_ablation_table.json"

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
                "num_candidate_records": report["num_candidate_records"],
                "available_configs": report["available_configs"],
                "missing_configs": report["missing_configs"],
                "all_required_configs_available": report[
                    "all_required_configs_available"
                ],
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_cmd = sub.add_parser("build", help="build CRT ablation report")
    build_cmd.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    build_cmd.add_argument(
        "--search-roots",
        nargs="+",
        default=[str(path) for path in DEFAULT_SEARCH_ROOTS],
    )
    build_cmd.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
