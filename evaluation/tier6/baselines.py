"""Baseline anchors for REALM-Bench Tier 6.

B0 is memoryless replay: each episode is solved independently, so no
cross-episode correction is retained.

B* is oracle memory: after observing a signature, the system receives the
ground-truth correction for subsequent episodes.

These anchors define normalized bracket positions. They are not submitted
systems; they are scoring references.
"""

from __future__ import annotations

from typing import Any, Dict


BASELINE_VERSION = "tier6-baselines-v0"


def default_baseline_bracket() -> Dict[str, Any]:
    """Return default Tier-6 baseline anchors.

    For repeated_failure_rate, lower is better:
      B0 = 1.0, B* = 0.0

    For horizon_reward, higher is better:
      B0 = 0.0, B* = 1.0
    """

    return {
        "baseline_version": BASELINE_VERSION,
        "B0_memoryless_replay": {
            "repeated_failure_rate": 1.0,
            "horizon_reward": 0.0,
        },
        "Bstar_oracle_memory": {
            "repeated_failure_rate": 0.0,
            "horizon_reward": 1.0,
        },
    }


def bracket_position(
    value: float | None,
    b0: float,
    bstar: float,
    *,
    higher_is_better: bool,
) -> float | None:
    """Return normalized position in [B0, B*].

    0.0 means equal to B0.
    1.0 means equal to B*.
    Values outside the bracket are clipped to [0, 1].
    """

    if value is None:
        return None

    if b0 == bstar:
        return None

    if higher_is_better:
        raw = (value - b0) / (bstar - b0)
    else:
        raw = (b0 - value) / (b0 - bstar)

    return max(0.0, min(1.0, raw))


def compute_bracket_positions(
    *,
    repeated_failure_rate: float | None,
    horizon_reward: float | None,
    bracket: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Compute bracket positions for primary Tier-6 metrics."""

    anchors = bracket if bracket is not None else default_baseline_bracket()
    b0 = anchors["B0_memoryless_replay"]
    bstar = anchors["Bstar_oracle_memory"]

    return {
        **anchors,
        "position_repeated_failure_rate": bracket_position(
            repeated_failure_rate,
            b0["repeated_failure_rate"],
            bstar["repeated_failure_rate"],
            higher_is_better=False,
        ),
        "position_horizon_reward": bracket_position(
            horizon_reward,
            b0["horizon_reward"],
            bstar["horizon_reward"],
            higher_is_better=True,
        ),
    }
