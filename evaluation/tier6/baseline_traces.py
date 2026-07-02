"""Concrete trace emitters for REALM-Bench Tier 6 baselines.

B0 memoryless replay and B* oracle memory are reference baselines. They emit
Tier-6-compatible traces from generated sequences and can be scored by the
same public scorer as any submitted system.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
T6_DIR = REPO_ROOT / "datasets" / "T6"

for path_entry in (str(REPO_ROOT), str(T6_DIR)):
    if path_entry not in sys.path:
        sys.path.insert(0, path_entry)


from evaluation.tier6.scorer import score_trace  # noqa: E402
from evaluation.tier6.schemas import validate_trace  # noqa: E402


FIXTURE_TIMESTAMP_UTC = "2026-07-02T00:00:00Z"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


generator = _load_module("tier6_generator_for_baselines", T6_DIR / "generator.py")


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
    horizon_reward: float | None = None,
    baseline_id: str,
) -> Dict[str, Any]:
    event = {
        "sequence_id": sequence["sequence_id"],
        "episode_id": episode["episode_id"],
        "seed": sequence["sequence_seed"],
        "t": FIXTURE_TIMESTAMP_UTC,
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
        "is_control_sequence": sequence["is_control_sequence"],
        "base_instance_id": episode["base_instance_id"],
        "family": episode["family"],
        "source_path": episode["source_path"],
        "dictionary_version": "tier6-signature-dictionary-v0",
        "generator_version": "tier6-generator-v0",
        "baseline_id": baseline_id,
        "claim_status": "baseline_reference_only",
    }

    if horizon_reward is not None:
        event["horizon_reward"] = horizon_reward

    return event


def emit_b0_memoryless_events(sequences: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Emit B0 memoryless replay traces.

    Non-control sequences repeat the same observed failure because no correction
    is retained across episodes. All time-to-correction values remain censored.
    """

    events: List[Dict[str, Any]] = []

    for sequence in sequences:
        for episode in sequence["episodes"]:
            if sequence["is_control_sequence"] or not sequence["hazard_signatures"]:
                events.append(make_event(
                    sequence=sequence,
                    episode=episode,
                    event_type="observe",
                    proposal_id=f"{sequence['sequence_id']}-e{episode['episode_id']}-b0-control",
                    failure_signature="",
                    predicted_outcome="no_recurring_structure",
                    observed_outcome="no_recurring_structure",
                    delta="",
                    constraint_violations=[],
                    horizon_reward=0.0,
                    baseline_id="B0_memoryless_replay",
                ))
                continue

            signature = sequence["hazard_signatures"][0]
            episode_id = episode["episode_id"]

            if episode_id == 1:
                events.append(make_event(
                    sequence=sequence,
                    episode=episode,
                    event_type="observe",
                    proposal_id=f"{sequence['sequence_id']}-e{episode_id}-b0-observe",
                    failure_signature=signature,
                    predicted_outcome="expected_success",
                    observed_outcome="failure_observed",
                    delta="failure_observed",
                    constraint_violations=[signature],
                    horizon_reward=0.0,
                    baseline_id="B0_memoryless_replay",
                ))
            elif episode_id == 2:
                events.append(make_event(
                    sequence=sequence,
                    episode=episode,
                    event_type="repair",
                    proposal_id=f"{sequence['sequence_id']}-e{episode_id}-b0-local-repair",
                    failure_signature=signature,
                    predicted_outcome="local_repair",
                    observed_outcome="local_repair_applied",
                    delta="corrected",
                    constraint_violations=[],
                    repair_radius=1,
                    evidence_preserved=True,
                    time_to_correction=1,
                    time_to_correction_censored=False,
                    horizon_reward=0.0,
                    baseline_id="B0_memoryless_replay",
                ))
            else:
                events.append(make_event(
                    sequence=sequence,
                    episode=episode,
                    event_type="observe",
                    proposal_id=f"{sequence['sequence_id']}-e{episode_id}-b0-recur",
                    failure_signature=signature,
                    predicted_outcome="expected_success",
                    observed_outcome="failure_recurred",
                    delta="failure_recurred",
                    constraint_violations=[signature],
                    horizon_reward=0.0,
                    baseline_id="B0_memoryless_replay",
                ))

    validate_trace(events)
    return events


def emit_bstar_oracle_events(sequences: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Emit B* oracle memory traces.

    Non-control sequences observe a signature once, receive an oracle correction,
    and avoid recurrence in later episodes.
    """

    events: List[Dict[str, Any]] = []

    for sequence in sequences:
        episodes = sequence["episodes"]

        if sequence["is_control_sequence"] or not sequence["hazard_signatures"]:
            for episode in episodes:
                events.append(make_event(
                    sequence=sequence,
                    episode=episode,
                    event_type="observe",
                    proposal_id=f"{sequence['sequence_id']}-e{episode['episode_id']}-bstar-control",
                    failure_signature="",
                    predicted_outcome="no_recurring_structure",
                    observed_outcome="no_recurring_structure",
                    delta="",
                    constraint_violations=[],
                    horizon_reward=1.0,
                    baseline_id="Bstar_oracle_memory",
                ))
            continue

        signature = sequence["hazard_signatures"][0]

        events.append(make_event(
            sequence=sequence,
            episode=episodes[0],
            event_type="observe",
            proposal_id=f"{sequence['sequence_id']}-e1-bstar-observe",
            failure_signature=signature,
            predicted_outcome="expected_success",
            observed_outcome="failure_observed",
            delta="failure_observed",
            constraint_violations=[signature],
            horizon_reward=0.5,
            baseline_id="Bstar_oracle_memory",
        ))

        events.append(make_event(
            sequence=sequence,
            episode=episodes[1],
            event_type="repair",
            proposal_id=f"{sequence['sequence_id']}-e2-bstar-repair",
            failure_signature=signature,
            predicted_outcome="oracle_correction",
            observed_outcome="oracle_correction_applied",
            delta="corrected",
            constraint_violations=[],
            repair_radius=1,
            evidence_preserved=True,
            time_to_correction=1,
            time_to_correction_censored=False,
            horizon_reward=1.0,
            baseline_id="Bstar_oracle_memory",
        ))

        for episode in episodes[2:]:
            events.append(make_event(
                sequence=sequence,
                episode=episode,
                event_type="observe",
                proposal_id=f"{sequence['sequence_id']}-e{episode['episode_id']}-bstar-clean",
                failure_signature=signature,
                predicted_outcome="corrected_success",
                observed_outcome="corrected_success",
                delta="",
                constraint_violations=[],
                horizon_reward=1.0,
                baseline_id="Bstar_oracle_memory",
            ))

    validate_trace(events)
    return events


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def emit_baseline_run(
    *,
    baseline_id: str,
    output_dir: Path,
    sequences: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    sequences = sequences if sequences is not None else generator.generate_development_sequences(REPO_ROOT)

    if baseline_id == "B0_memoryless_replay":
        events = emit_b0_memoryless_events(sequences)
    elif baseline_id == "Bstar_oracle_memory":
        events = emit_bstar_oracle_events(sequences)
    else:
        raise ValueError(f"unknown baseline_id: {baseline_id}")

    summary = score_trace(events)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": f"tier6_{baseline_id}_v0",
        "phase": "baseline_reference",
        "claim_status": "baseline_reference_only",
        "baseline_id": baseline_id,
        "num_sequences": len(sequences),
        "num_episodes": sum(len(seq["episodes"]) for seq in sequences),
        "num_events": len(events),
        "families": sorted({seq["base_instance"]["family"] for seq in sequences}),
        "dictionary_version": "tier6-signature-dictionary-v0",
        "generator_version": "tier6-generator-v0",
        "scorer_version": "tier6-scorer-v0",
    }

    write_json(output_dir / "manifest.json", manifest)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "summary.json", summary)

    return {
        "manifest": manifest,
        "summary": summary,
        "events": events,
        "output_dir": str(output_dir),
    }


def main() -> None:
    base_output = REPO_ROOT / "runs" / "realm_tier6"
    results = {}
    for baseline_id in ("B0_memoryless_replay", "Bstar_oracle_memory"):
        result = emit_baseline_run(
            baseline_id=baseline_id,
            output_dir=base_output / f"tier6_{baseline_id}_v0",
        )
        results[baseline_id] = {
            "num_events": result["manifest"]["num_events"],
            "safety_passed": result["summary"]["safety_passed"],
            "repeated_failure_rate": result["summary"]["repeated_failure_rate"],
            "horizon_reward_mean": result["summary"]["horizon_reward_mean"],
        }

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
