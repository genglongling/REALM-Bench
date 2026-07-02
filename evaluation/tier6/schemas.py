"""REALM-Bench Tier 6 trace schema.

Tier 6 evaluates cross-episode causal-loop behavior from boundary-observable
traces. This module intentionally uses only the Python standard library so the
public scorer has no heavy dependency.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


VALID_EVENTS = {"propose", "admit", "reject", "commit", "repair", "observe"}

REQUIRED_EVENT_FIELDS = {
    "sequence_id",
    "episode_id",
    "seed",
    "t",
    "event",
    "proposal_id",
    "failure_signature",
    "predicted_outcome",
    "observed_outcome",
    "delta",
    "constraint_violations",
    "repair",
    "cost",
    "time_to_correction",
    "time_to_correction_censored",
    "invalid_commit_count",
    "evidence_destroying_repair_count",
    "orphaned_dependent_count",
}

REQUIRED_REPAIR_FIELDS = {"radius", "evidence_preserved"}
REQUIRED_COST_FIELDS = {"tokens_in", "tokens_out", "wallclock_ms"}


class Tier6SchemaError(ValueError):
    """Raised when a Tier-6 trace record violates the public schema."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Tier6SchemaError(message)


def validate_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Validate one Tier-6 event record and return it unchanged.

    The schema is deliberately strict because Tier-6 metrics must be computed
    from submitted traces, not from model-internal or post-hoc information.
    """

    missing = sorted(REQUIRED_EVENT_FIELDS - set(event))
    _require(not missing, f"missing required event fields: {missing}")

    _require(event["event"] in VALID_EVENTS, f"invalid event type: {event['event']}")
    _require(isinstance(event["sequence_id"], str) and event["sequence_id"], "sequence_id must be nonempty string")
    _require(isinstance(event["episode_id"], int) and event["episode_id"] >= 1, "episode_id must be positive int")
    _require(isinstance(event["seed"], int), "seed must be int")
    _require(isinstance(event["proposal_id"], str), "proposal_id must be string")
    _require(isinstance(event["failure_signature"], str), "failure_signature must be string")
    _require(isinstance(event["constraint_violations"], list), "constraint_violations must be list")

    repair = event["repair"]
    _require(isinstance(repair, dict), "repair must be dict")
    missing_repair = sorted(REQUIRED_REPAIR_FIELDS - set(repair))
    _require(not missing_repair, f"missing repair fields: {missing_repair}")
    _require(isinstance(repair["radius"], int) and repair["radius"] >= 0, "repair.radius must be nonnegative int")
    _require(isinstance(repair["evidence_preserved"], bool), "repair.evidence_preserved must be bool")

    cost = event["cost"]
    _require(isinstance(cost, dict), "cost must be dict")
    missing_cost = sorted(REQUIRED_COST_FIELDS - set(cost))
    _require(not missing_cost, f"missing cost fields: {missing_cost}")
    for key in REQUIRED_COST_FIELDS:
        _require(isinstance(cost[key], (int, float)) and cost[key] >= 0, f"cost.{key} must be nonnegative number")

    for key in (
        "invalid_commit_count",
        "evidence_destroying_repair_count",
        "orphaned_dependent_count",
    ):
        _require(isinstance(event[key], int) and event[key] >= 0, f"{key} must be nonnegative int")

    if event["event"] == "reject":
        _require(
            isinstance(event.get("rejection_reason_code"), str)
            and bool(event.get("rejection_reason_code")),
            "rejected event requires rejection_reason_code",
        )

    if event["time_to_correction"] is None:
        _require(
            event["time_to_correction_censored"] is True,
            "null time_to_correction requires time_to_correction_censored=true",
        )
    else:
        _require(
            isinstance(event["time_to_correction"], int)
            and event["time_to_correction"] >= 0,
            "time_to_correction must be null or nonnegative int",
        )
        _require(
            isinstance(event["time_to_correction_censored"], bool),
            "time_to_correction_censored must be bool",
        )

    return event


def validate_trace(events: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate a complete trace and return validated events."""

    validated = [validate_event(event) for event in events]
    _require(len(validated) > 0, "trace must contain at least one event")
    return validated
