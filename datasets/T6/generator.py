"""REALM-Bench Tier 6 deterministic sequence generator.

Tier 6 derives cross-episode sequences from existing Tier-4/5-style REALM
dataset families. This module does not solve tasks and does not evaluate
Mnemosyne; it creates reproducible episode metadata and hazard structure.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
DEFAULT_SEEDS_PATH = THIS_DIR / "public_seeds_v0.json"
DEFAULT_DICTIONARY_PATH = THIS_DIR / "dictionary_v0.json"

DEFAULT_BASE_FAMILIES = {
    "jobshop_breakdown": "datasets/J4",
    "ride_or_routing_disruption": "datasets/P4",
    "wedding_recovery": "datasets/P8",
    "thanksgiving_recovery": "datasets/P9",
    "supply_chain": "datasets/P10",
}

DATA_EXTENSIONS = {".json", ".jsonl", ".csv", ".txt", ".yaml", ".yml"}


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_signatures = _load_module("tier6_signatures", THIS_DIR / "signatures.py")
_perturbations = _load_module("tier6_perturbations", THIS_DIR / "perturbations.py")


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_public_seeds(path: Path = DEFAULT_SEEDS_PATH) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def discover_base_instances(
    repo_root: Path | str = REPO_ROOT,
    families: Dict[str, str] | None = None,
    max_per_family: int = 20,
) -> List[Dict[str, Any]]:
    """Discover existing REALM base instances for Tier-6 sequence derivation."""

    root = Path(repo_root)
    family_map = families or DEFAULT_BASE_FAMILIES
    instances: List[Dict[str, Any]] = []

    for family_name, rel_dir in family_map.items():
        family_dir = root / rel_dir
        if not family_dir.exists():
            continue

        candidates = []
        for path in sorted(family_dir.rglob("*")):
            if not path.is_file():
                continue
            if path.name.startswith("."):
                continue
            if path.name.lower() == "readme.md":
                continue
            if path.suffix.lower() not in DATA_EXTENSIONS:
                continue
            candidates.append(path)

        for idx, path in enumerate(candidates[:max_per_family]):
            rel_path = path.relative_to(root)
            base_id = f"{family_name}:{rel_path.as_posix()}"
            instances.append({
                "base_instance_id": base_id,
                "family": family_name,
                "source_path": rel_path.as_posix(),
                "source_sha256": sha256_file(path),
            })

    return instances


def select_hazards(
    base_instance_id: str,
    sequence_seed: int,
    is_control_sequence: bool,
    max_hazards: int = 3,
) -> List[str]:
    """Select 1-3 versioned hazards for a non-control sequence."""

    if is_control_sequence:
        return []

    dictionary = _signatures.load_dictionary(DEFAULT_DICTIONARY_PATH)
    available = list(_signatures.list_signatures(dictionary))
    n = 1 + _perturbations.stable_int("hazard-count", base_instance_id, sequence_seed, modulo=max_hazards)

    ranked = sorted(
        available,
        key=lambda sig: _perturbations.stable_digest("hazard", base_instance_id, sequence_seed, sig),
    )
    return ranked[:n]


def is_control_sequence(base_instance_id: str, sequence_seed: int) -> bool:
    """Return true for deterministic negative-control sequences.

    The threshold implements the Tier-6 minimum-control policy at the sequence
    construction level. Exact release splits can be frozen later in seed files.
    """

    bucket = _perturbations.stable_int("control", base_instance_id, sequence_seed, modulo=5)
    return bucket == 0


def generate_sequence(
    base_instance: Dict[str, Any],
    sequence_seed: int,
    episodes_per_sequence: int = 10,
    force_control: bool | None = None,
) -> Dict[str, Any]:
    """Generate one deterministic Tier-6 cross-episode sequence."""

    base_id = base_instance["base_instance_id"]
    control = is_control_sequence(base_id, sequence_seed) if force_control is None else force_control
    hazards = select_hazards(base_id, sequence_seed, control)

    sequence_id = f"T6-{_perturbations.stable_digest(base_id, sequence_seed)[:12]}"
    episodes = []

    for episode_id in range(1, episodes_per_sequence + 1):
        episodes.append({
            "sequence_id": sequence_id,
            "episode_id": episode_id,
            "seed": sequence_seed,
            "base_instance_id": base_id,
            "family": base_instance["family"],
            "source_path": base_instance["source_path"],
            "source_sha256": base_instance["source_sha256"],
            "is_control_sequence": control,
            "hazard_signatures": hazards,
            "perturbation": _perturbations.perturbation_manifest(base_id, sequence_seed, episode_id),
        })

    return {
        "sequence_id": sequence_id,
        "sequence_seed": sequence_seed,
        "episodes_per_sequence": episodes_per_sequence,
        "base_instance": base_instance,
        "is_control_sequence": control,
        "hazard_signatures": hazards,
        "episodes": episodes,
    }


def select_one_base_per_family(
    repo_root: Path | str = REPO_ROOT,
    max_families: int = 3,
) -> List[Dict[str, Any]]:
    """Select one discovered base instance per family for the development set."""

    instances = discover_base_instances(repo_root)
    selected = []
    seen = set()

    for item in instances:
        family = item["family"]
        if family in seen:
            continue
        selected.append(item)
        seen.add(family)
        if len(selected) >= max_families:
            break

    return selected


def generate_development_sequences(
    repo_root: Path | str = REPO_ROOT,
    max_families: int = 3,
) -> List[Dict[str, Any]]:
    """Generate a small public development set from existing REALM instances.

    The development split uses one base instance per family and five public
    seeds per family. Exactly one sequence per family is forced to be a control
    sequence, giving a stable 20 percent control rate for the public seed set.
    """

    seeds = load_public_seeds()
    public_seeds = list(seeds["public_sequence_seeds"])
    base_instances = select_one_base_per_family(repo_root, max_families=max_families)
    sequences = []

    for base_instance in base_instances:
        for seed_index, seed in enumerate(public_seeds):
            force_control = seed_index == 0
            sequences.append(generate_sequence(
                base_instance,
                seed,
                episodes_per_sequence=seeds["episodes_per_sequence"],
                force_control=force_control,
            ))

    return sequences


def main() -> None:
    sequences = generate_development_sequences()
    print(json.dumps({
        "num_sequences": len(sequences),
        "num_episodes": sum(len(seq["episodes"]) for seq in sequences),
        "families": sorted({seq["base_instance"]["family"] for seq in sequences}),
        "control_sequences": sum(1 for seq in sequences if seq["is_control_sequence"]),
    }, indent=2))


if __name__ == "__main__":
    main()
