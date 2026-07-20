import pytest

from evaluation.tier6.schemas import Tier6SchemaError, validate_event


def valid_event(**overrides):
    event = {
        "sequence_id": "T6-P4-0001-s17",
        "episode_id": 1,
        "seed": 17,
        "t": "2026-07-02T00:00:00Z",
        "event": "observe",
        "proposal_id": "p1",
        "failure_signature": "stale_world.route_time_underestimated",
        "predicted_outcome": "arrive_on_time",
        "observed_outcome": "late",
        "delta": "late_by_15m",
        "constraint_violations": [],
        "repair": {"radius": 0, "evidence_preserved": True},
        "cost": {"tokens_in": 0, "tokens_out": 0, "wallclock_ms": 0},
        "time_to_correction": None,
        "time_to_correction_censored": True,
        "invalid_commit_count": 0,
        "evidence_destroying_repair_count": 0,
        "orphaned_dependent_count": 0,
    }
    event.update(overrides)
    return event


def test_valid_event_passes_schema():
    assert validate_event(valid_event())["sequence_id"] == "T6-P4-0001-s17"


def test_missing_sequence_id_fails():
    event = valid_event()
    del event["sequence_id"]
    with pytest.raises(Tier6SchemaError):
        validate_event(event)


def test_null_time_to_correction_requires_censoring_flag():
    event = valid_event(time_to_correction=None, time_to_correction_censored=False)
    with pytest.raises(Tier6SchemaError):
        validate_event(event)


def test_reject_requires_rejection_reason_code():
    event = valid_event(event="reject")
    with pytest.raises(Tier6SchemaError):
        validate_event(event)

    event["rejection_reason_code"] = "stale_world"
    assert validate_event(event)["rejection_reason_code"] == "stale_world"
