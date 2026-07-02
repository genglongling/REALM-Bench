"""Deterministic perturbation utilities for REALM-Bench Tier 6."""

from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, Iterable, List


def stable_digest(*parts: Any) -> str:
    text = "::".join(str(part) for part in parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_int(*parts: Any, modulo: int | None = None) -> int:
    value = int(stable_digest(*parts)[:16], 16)
    return value % modulo if modulo else value


def jitter_number(value: float, seed: int, key: str, pct: float = 0.10) -> float:
    """Apply deterministic numeric jitter within +/- pct."""

    rng = random.Random(stable_int("jitter", seed, key))
    factor = 1.0 + rng.uniform(-pct, pct)
    return round(value * factor, 6)


def rename_identifier(identifier: str, seed: int, namespace: str = "entity") -> str:
    """Rename an entity while preserving deterministic reproducibility."""

    suffix = stable_digest("rename", namespace, seed, identifier)[:8]
    return f"{namespace}_{suffix}"


def resample_list(items: Iterable[Any], seed: int, key: str, min_keep: int = 1) -> List[Any]:
    """Return a deterministic nonempty subset preserving item type."""

    values = list(items)
    if not values:
        return []

    rng = random.Random(stable_int("resample", seed, key))
    shuffled = list(values)
    rng.shuffle(shuffled)
    keep = max(min_keep, 1 + stable_int("keep", seed, key, modulo=len(values)))
    return shuffled[:keep]


def perturbation_manifest(base_instance_id: str, sequence_seed: int, episode_id: int) -> Dict[str, Any]:
    """Describe deterministic perturbations applied to one episode.

    The first implementation records perturbation metadata rather than mutating
    every underlying REALM instance format. Format-specific mutation can be
    added later behind the same manifest contract.
    """

    episode_key = f"{base_instance_id}:{sequence_seed}:{episode_id}"
    return {
        "operators": ["jitter", "rename", "resample"],
        "jitter_scale": jitter_number(1.0, sequence_seed + episode_id, episode_key),
        "rename_salt": stable_digest("rename", episode_key)[:12],
        "resample_salt": stable_digest("resample", episode_key)[:12],
    }
