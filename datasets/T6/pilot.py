"""Frozen pilot subset utilities for REALM-Bench Tier 6."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[1]
DEFAULT_PILOT_PATH = THIS_DIR / "pilot_subset_v0.json"


def _load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot import {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_generator = _load_module("tier6_generator_for_pilot", THIS_DIR / "generator.py")


def load_pilot_subset(path: str | Path | None = None) -> Dict[str, Any]:
    pilot_path = Path(path) if path is not None else DEFAULT_PILOT_PATH
    with pilot_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    required = {
        "pilot_subset_version",
        "families",
        "sequences_per_family",
        "episodes_per_sequence",
        "public_sequence_seeds",
        "control_seed_policy",
        "not_for_confirmatory_claims",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"pilot subset missing required fields: {missing}")

    if data["not_for_confirmatory_claims"] is not True:
        raise ValueError("pilot subset must be marked not_for_confirmatory_claims=true")

    return data


def generate_pilot_sequences(
    repo_root: str | Path = REPO_ROOT,
    pilot_path: str | Path | None = None,
) -> List[Dict[str, Any]]:
    """Generate the frozen Tier-6 pilot subset.

    This returns one base instance per listed family and the frozen public seed
    list. The first seed per family is forced to be a control sequence.
    """

    pilot = load_pilot_subset(pilot_path)
    family_dirs = {
        family: _generator.DEFAULT_BASE_FAMILIES[family]
        for family in pilot["families"]
    }

    base_instances = _generator.discover_base_instances(
        repo_root=repo_root,
        families=family_dirs,
        max_per_family=1,
    )

    expected_families = set(pilot["families"])
    discovered_families = {item["family"] for item in base_instances}
    missing = expected_families - discovered_families
    if missing:
        raise ValueError(f"pilot subset missing base families: {sorted(missing)}")

    sequences = []
    control_seed = pilot["control_seed_policy"]["control_seed"]

    for base_instance in base_instances:
        for seed in pilot["public_sequence_seeds"]:
            sequences.append(_generator.generate_sequence(
                base_instance,
                sequence_seed=seed,
                episodes_per_sequence=pilot["episodes_per_sequence"],
                force_control=(seed == control_seed),
            ))

    return sequences


def main() -> None:
    sequences = generate_pilot_sequences()
    print(json.dumps({
        "pilot_subset_version": load_pilot_subset()["pilot_subset_version"],
        "num_sequences": len(sequences),
        "num_episodes": sum(len(seq["episodes"]) for seq in sequences),
        "families": sorted({seq["base_instance"]["family"] for seq in sequences}),
        "control_sequences": sum(1 for seq in sequences if seq["is_control_sequence"]),
        "not_for_confirmatory_claims": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
