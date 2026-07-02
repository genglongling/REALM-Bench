"""Analyze a REALM-Bench Tier-6 run directory.

Reads events.jsonl, validates/scorers it, and regenerates summary.json,
summary.csv, and report.md. This script performs no LLM calls.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evaluation.tier6.scorer import score_trace  # noqa: E402


CANONICAL_SENTENCE = (
    "This implements and validates the REALM-Bench Tier-6 causal-loop harness; "
    "pilot and confirmatory runs follow under the registered protocol."
)


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def summary_rows(summary: Dict[str, Any]) -> Iterable[tuple[str, Any]]:
    yield "num_events", summary["num_events"]
    yield "num_control_events", summary["num_control_events"]
    yield "num_non_control_events", summary["num_non_control_events"]
    yield "safety_passed", summary["safety_passed"]
    yield "invalid_commit_count", summary["safety_counts"]["invalid_commit_count"]
    yield "evidence_destroying_repair_count", summary["safety_counts"]["evidence_destroying_repair_count"]
    yield "orphaned_dependent_count", summary["safety_counts"]["orphaned_dependent_count"]
    yield "repeated_failure_rate", summary["repeated_failure_rate"]
    yield "repeated_failure_rate_controls", summary["repeated_failure_rate_controls"]
    yield "time_to_correction_mean_observed", summary["time_to_correction_mean_observed"]
    yield "time_to_correction_observed_count", summary["time_to_correction_observed_count"]
    yield "time_to_correction_censored_count", summary["time_to_correction_censored_count"]
    yield "horizon_reward_mean", summary["horizon_reward_mean"]
    yield "grounded_admission_rate", summary["grounded_admission_rate"]
    yield "bracket_position_repeated_failure_rate", summary["bracket"]["position_repeated_failure_rate"]
    yield "bracket_position_horizon_reward", summary["bracket"]["position_horizon_reward"]
    yield "tokens_in", summary["cost"]["tokens_in"]
    yield "tokens_out", summary["cost"]["tokens_out"]
    yield "wallclock_ms", summary["cost"]["wallclock_ms"]


def write_summary_csv(path: Path, summary: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerows(summary_rows(summary))


def write_report(path: Path, manifest: Dict[str, Any], summary: Dict[str, Any]) -> None:
    text = f"""# REALM-Bench Tier 6 Analysis Report

Status: deterministic harness validation only.

{CANONICAL_SENTENCE}

This report is regenerated from `events.jsonl` and `manifest.json`.
It validates analysis reproducibility only. It is not a system result and must
not be used as evidence for H1-H5.

## Manifest

- Run ID: {manifest.get('run_id')}
- Phase: {manifest.get('phase')}
- Claim status: {manifest.get('claim_status')}
- Sequences: {manifest.get('num_sequences')}
- Episodes: {manifest.get('num_episodes')}
- Events: {manifest.get('num_events')}
- Families: {', '.join(manifest.get('families', []))}

## Scorer summary

| Metric | Value |
|---|---:|
| Safety passed | {summary['safety_passed']} |
| Invalid commits | {summary['safety_counts']['invalid_commit_count']} |
| Evidence-destroying repairs | {summary['safety_counts']['evidence_destroying_repair_count']} |
| Orphaned dependents | {summary['safety_counts']['orphaned_dependent_count']} |
| Repeated failure rate | {summary['repeated_failure_rate']} |
| Control repeated failure rate | {summary['repeated_failure_rate_controls']} |
| Observed TTC count | {summary['time_to_correction_observed_count']} |
| Censored TTC count | {summary['time_to_correction_censored_count']} |
| Horizon reward mean | {summary['horizon_reward_mean']} |
| RFR bracket position | {summary['bracket']['position_repeated_failure_rate']} |
| Horizon bracket position | {summary['bracket']['position_horizon_reward']} |

## Claim boundary

The deterministic fixture constructs expected causal-loop events by design.
These outputs validate trace generation, schema validation, scoring,
censoring, and analysis regeneration only. Pilot and confirmatory runs are
required before Chapter 6 can make quantitative claims about cross-episode
learning.
"""
    path.write_text(text, encoding="utf-8")


def analyze_run(run_dir: Path) -> Dict[str, Any]:
    manifest = read_json(run_dir / "manifest.json")
    events = read_jsonl(run_dir / "events.jsonl")
    summary = score_trace(events)

    write_json(run_dir / "summary.json", summary)
    write_summary_csv(run_dir / "summary.csv", summary)
    write_report(run_dir / "report.md", manifest, summary)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    summary = analyze_run(args.run_dir)
    print(json.dumps({
        "run_dir": str(args.run_dir),
        "num_events": summary["num_events"],
        "safety_passed": summary["safety_passed"],
        "repeated_failure_rate": summary["repeated_failure_rate"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
