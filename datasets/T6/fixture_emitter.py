"""Deterministic Tier-6 trace fixture emitter.

This script creates scorer-consumable Tier-6 traces from generated development
sequences. The emitted data is for harness validation only. It is not a system
submission and not evidence for Quadrivium/Mnemosyne hypotheses.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]

# When this file is run as a script, Python automatically places THIS_DIR on
# sys.path. When pytest imports it via importlib, it does not. Add both paths
# explicitly so local Tier-6 modules and repository packages are importable.
for path_entry in (str(THIS_DIR), str(REPO_ROOT)):
    if path_entry not in sys.path:
        sys.path.insert(0, path_entry)

import generator  # noqa: E402
from evaluation.tier6.scorer import score_trace  # noqa: E402
from evaluation.tier6.schemas import validate_trace  # noqa: E402


CANONICAL_SENTENCE = (
    "This implements and validates the REALM-Bench Tier-6 causal-loop harness; "
    "pilot and confirmatory runs follow under the registered protocol."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_event(
    *,
    sequence: Dict[str, Any],
    episode: Dict[str, Any],
    event_type: str,
    proposal_id: str,
    failure_signature: str,
    predicted_outcome: str,
    observed_outcome: str,
    delta: str,
    constraint_violations: List[str],
    repair_radius: int = 0,
    evidence_preserved: bool = True,
    time_to_correction: int | None = None,
    time_to_correction_censored: bool = True,
    is_control_sequence: bool | None = None,
    rejection_reason_code: str | None = None,
    horizon_reward: float | None = None,
    grounded_admission: bool | None = None,
) -> Dict[str, Any]:
    event = {
        "sequence_id": sequence["sequence_id"],
        "episode_id": episode["episode_id"],
        "seed": sequence["sequence_seed"],
        "t": utc_now(),
        "event": event_type,
        "proposal_id": proposal_id,
        "failure_signature": failure_signature,
        "predicted_outcome": predicted_outcome,
        "observed_outcome": observed_outcome,
        "delta": delta,
        "constraint_violations": constraint_violations,
        "repair": {
            "radius": repair_radius,
            "evidence_preserved": evidence_preserved,
        },
        "cost": {
            "tokens_in": 0,
            "tokens_out": 0,
            "wallclock_ms": 0,
        },
        "time_to_correction": time_to_correction,
        "time_to_correction_censored": time_to_correction_censored,
        "invalid_commit_count": 0,
        "evidence_destroying_repair_count": 0,
        "orphaned_dependent_count": 0,
        "is_control_sequence": sequence["is_control_sequence"] if is_control_sequence is None else is_control_sequence,
        "base_instance_id": episode["base_instance_id"],
        "family": episode["family"],
        "source_path": episode["source_path"],
        "dictionary_version": "tier6-signature-dictionary-v0",
        "generator_version": "tier6-generator-v0",
        "claim_status": "harness_validation_only",
    }

    if rejection_reason_code is not None:
        event["rejection_reason_code"] = rejection_reason_code
    if horizon_reward is not None:
        event["horizon_reward"] = horizon_reward
    if grounded_admission is not None:
        event["grounded_admission"] = grounded_admission

    return event


def fixture_events_for_sequence(sequence: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Emit deterministic events for one sequence.

    Controls emit benign observations only. Non-controls emit a small causal
    loop fixture: first observation, correction, and either recurrence or
    right-censoring depending on the selected hazard index.
    """

    events: List[Dict[str, Any]] = []
    episodes = sequence["episodes"]

    if sequence["is_control_sequence"]:
        for episode in episodes:
            events.append(make_event(
                sequence=sequence,
                episode=episode,
                event_type="observe",
                proposal_id=f"{sequence['sequence_id']}-e{episode['episode_id']}-control",
                failure_signature="",
                predicted_outcome="no_recurring_structure",
                observed_outcome="no_recurring_structure",
                delta="",
                constraint_violations=[],
                time_to_correction=None,
                time_to_correction_censored=True,
                horizon_reward=0.0,
            ))
        return events

    hazards = sequence["hazard_signatures"]
    if not hazards:
        return events

    primary = hazards[0]
    secondary = hazards[1] if len(hazards) > 1 else hazards[0]

    # Episode 1: observe a failure signature.
    events.append(make_event(
        sequence=sequence,
        episode=episodes[0],
        event_type="observe",
        proposal_id=f"{sequence['sequence_id']}-e1-observe",
        failure_signature=primary,
        predicted_outcome="expected_success",
        observed_outcome="observed_failure",
        delta="failure_observed",
        constraint_violations=[primary],
        time_to_correction=None,
        time_to_correction_censored=True,
        horizon_reward=0.0,
    ))

    # Episode 2: repair/correct the first signature.
    events.append(make_event(
        sequence=sequence,
        episode=episodes[1],
        event_type="repair",
        proposal_id=f"{sequence['sequence_id']}-e2-repair",
        failure_signature=primary,
        predicted_outcome="repair_expected",
        observed_outcome="repair_applied",
        delta="corrected",
        constraint_violations=[],
        repair_radius=1,
        evidence_preserved=True,
        time_to_correction=1,
        time_to_correction_censored=False,
        horizon_reward=0.5,
    ))

    # Episode 3: deterministic recurrence after correction, so repeated-failure
    # accounting is exercised by the scorer.
    events.append(make_event(
        sequence=sequence,
        episode=episodes[2],
        event_type="observe",
        proposal_id=f"{sequence['sequence_id']}-e3-recur",
        failure_signature=primary,
        predicted_outcome="expected_success_after_repair",
        observed_outcome="failure_recurred",
        delta="failure_recurred",
        constraint_violations=[primary],
        time_to_correction=None,
        time_to_correction_censored=True,
        horizon_reward=0.25,
    ))

    # Episode 4: add a rejected proposal to test rejection reason logging.
    events.append(make_event(
        sequence=sequence,
        episode=episodes[3],
        event_type="reject",
        proposal_id=f"{sequence['sequence_id']}-e4-reject",
        failure_signature=secondary,
        predicted_outcome="unsafe_repair",
        observed_outcome="rejected_before_commit",
        delta="proposal_rejected",
        constraint_violations=[secondary],
        time_to_correction=None,
        time_to_correction_censored=True,
        rejection_reason_code="tier6_fixture_known_hazard",
        horizon_reward=0.25,
    ))

    # Episode 5: an uncorrected signature remains right-censored.
    events.append(make_event(
        sequence=sequence,
        episode=episodes[4],
        event_type="observe",
        proposal_id=f"{sequence['sequence_id']}-e5-censored",
        failure_signature=secondary,
        predicted_outcome="expected_success",
        observed_outcome="uncorrected_failure",
        delta="uncorrected",
        constraint_violations=[secondary],
        time_to_correction=None,
        time_to_correction_censored=True,
        horizon_reward=0.25,
    ))

    return events


def emit_fixture_run(output_dir: Path, run_id: str = "tier6_harness_validation_v0") -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)

    sequences = generator.generate_development_sequences(REPO_ROOT)
    events: List[Dict[str, Any]] = []
    for sequence in sequences:
        events.extend(fixture_events_for_sequence(sequence))

    validate_trace(events)
    summary = score_trace(events)

    manifest = {
        "run_id": run_id,
        "phase": "deterministic_harness_validation",
        "claim_status": "not_chapter_result",
        "canonical_sentence": CANONICAL_SENTENCE,
        "utc_start": utc_now(),
        "utc_end": utc_now(),
        "num_sequences": len(sequences),
        "num_episodes": sum(len(sequence["episodes"]) for sequence in sequences),
        "num_events": len(events),
        "families": sorted({sequence["base_instance"]["family"] for sequence in sequences}),
        "dictionary_version": "tier6-signature-dictionary-v0",
        "generator_version": "tier6-generator-v0",
        "scorer_version": "tier6-scorer-v0",
        "public_seed_set": "tier6-public-seeds-v0",
    }

    write_json(output_dir / "manifest.json", manifest)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "summary.json", summary)
    write_report(output_dir / "report.md", manifest, summary)

    return {
        "manifest": manifest,
        "summary": summary,
        "events": events,
        "output_dir": str(output_dir),
    }


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def write_report(path: Path, manifest: Dict[str, Any], summary: Dict[str, Any]) -> None:
    text = f"""# REALM-Bench Tier 6 Harness Validation Report

Status: deterministic harness validation only.

{CANONICAL_SENTENCE}

This report validates trace emission, schema compliance, scorer consumption,
right-censoring, control-sequence separation, and safety-gate reporting.
It is not a system result and must not be used as evidence for H1-H5.

## Manifest

- Run ID: {manifest['run_id']}
- Phase: {manifest['phase']}
- Claim status: {manifest['claim_status']}
- Sequences: {manifest['num_sequences']}
- Episodes: {manifest['num_episodes']}
- Events: {manifest['num_events']}
- Families: {', '.join(manifest['families'])}

## Scorer summary

- Safety passed: {summary['safety_passed']}
- Invalid commits: {summary['safety_counts']['invalid_commit_count']}
- Evidence-destroying repairs: {summary['safety_counts']['evidence_destroying_repair_count']}
- Orphaned dependents: {summary['safety_counts']['orphaned_dependent_count']}
- Repeated failure rate: {summary['repeated_failure_rate']}
- Control repeated failure rate: {summary['repeated_failure_rate_controls']}
- Observed time-to-correction count: {summary['time_to_correction_observed_count']}
- Censored time-to-correction count: {summary['time_to_correction_censored_count']}

## Claim boundary

The deterministic fixture constructs expected causal-loop events by design.
These events validate the harness and scorer only. Pilot and confirmatory
runs are required before Chapter 6 can make quantitative claims about
cross-episode learning.
"""
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "runs" / "realm_tier6" / "tier6_harness_validation_v0"),
    )
    parser.add_argument("--run-id", default="tier6_harness_validation_v0")
    args = parser.parse_args()

    result = emit_fixture_run(Path(args.output_dir), run_id=args.run_id)
    print(json.dumps({
        "output_dir": result["output_dir"],
        "num_events": result["manifest"]["num_events"],
        "safety_passed": result["summary"]["safety_passed"],
        "repeated_failure_rate": result["summary"]["repeated_failure_rate"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
