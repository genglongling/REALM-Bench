from evaluation.tier6.baselines import (
    bracket_position,
    compute_bracket_positions,
    default_baseline_bracket,
)


def test_default_baseline_bracket_has_required_anchors():
    bracket = default_baseline_bracket()
    assert bracket["baseline_version"] == "tier6-baselines-v0"
    assert bracket["B0_memoryless_replay"]["repeated_failure_rate"] == 1.0
    assert bracket["Bstar_oracle_memory"]["repeated_failure_rate"] == 0.0


def test_lower_is_better_bracket_position():
    assert bracket_position(1.0, 1.0, 0.0, higher_is_better=False) == 0.0
    assert bracket_position(0.0, 1.0, 0.0, higher_is_better=False) == 1.0
    assert bracket_position(0.5, 1.0, 0.0, higher_is_better=False) == 0.5


def test_higher_is_better_bracket_position():
    assert bracket_position(0.0, 0.0, 1.0, higher_is_better=True) == 0.0
    assert bracket_position(1.0, 0.0, 1.0, higher_is_better=True) == 1.0
    assert bracket_position(0.25, 0.0, 1.0, higher_is_better=True) == 0.25


def test_compute_bracket_positions():
    result = compute_bracket_positions(
        repeated_failure_rate=0.25,
        horizon_reward=0.75,
    )
    assert result["position_repeated_failure_rate"] == 0.75
    assert result["position_horizon_reward"] == 0.75
