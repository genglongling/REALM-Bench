from evaluation.tier6.scorer import score_trace


def event(**overrides):
    base = {
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
    base.update(overrides)
    return base


def test_nonzero_invalid_commit_fails_safety_gate():
    result = score_trace([event(event="commit", invalid_commit_count=1)])
    assert result["safety_passed"] is False
    assert result["safety_counts"]["invalid_commit_count"] == 1


def test_scorer_separates_control_sequences():
    result = score_trace([
        event(sequence_id="noncontrol", is_control_sequence=False),
        event(sequence_id="control", is_control_sequence=True),
    ])
    assert result["num_control_events"] == 1
    assert result["num_non_control_events"] == 1


def test_repeated_failure_after_correction_is_counted():
    records = [
        event(episode_id=1, event="observe", delta="late"),
        event(
            episode_id=2,
            event="repair",
            delta="corrected",
            time_to_correction=1,
            time_to_correction_censored=False,
        ),
        event(episode_id=3, event="observe", delta="late_again"),
    ]
    result = score_trace(records)
    assert result["repeated_failure_rate"] == 1.0


def test_bracket_fields_exist():
    result = score_trace([event()])
    assert "bracket" in result
    assert "B0_memoryless_replay" in result["bracket"]
    assert "Bstar_oracle_memory" in result["bracket"]
    assert "position_repeated_failure_rate" in result["bracket"]
    assert "position_horizon_reward" in result["bracket"]
