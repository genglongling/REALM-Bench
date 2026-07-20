"""REALM-Bench Tier 6 failure-signature dictionary utilities."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


DEFAULT_DICTIONARY_PATH = Path(__file__).with_name("dictionary_v0.json")
SIGNATURE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")


class SignatureDictionaryError(ValueError):
    """Raised when a Tier-6 failure signature is invalid."""


def canonicalize_signature(raw: str) -> str:
    """Convert a surface signature string to the Tier-6 canonical form."""

    if not isinstance(raw, str):
        raise SignatureDictionaryError("signature must be a string")

    value = raw.strip().lower()
    value = value.replace("-", "_")
    value = re.sub(r"\s+", "_", value)
    value = value.replace("_.", ".").replace("._", ".")
    return value


def load_dictionary(path: str | Path | None = None) -> Dict[str, Any]:
    """Load the versioned Tier-6 signature dictionary."""

    dictionary_path = Path(path) if path is not None else DEFAULT_DICTIONARY_PATH
    with dictionary_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if "dictionary_version" not in data:
        raise SignatureDictionaryError("dictionary_version missing")
    if "signatures" not in data or not isinstance(data["signatures"], dict):
        raise SignatureDictionaryError("signatures mapping missing")

    for signature, metadata in data["signatures"].items():
        _validate_signature_shape(signature)
        for field in ("constraint_class", "entity_role", "disruption_class", "faculty_axis"):
            if field not in metadata:
                raise SignatureDictionaryError(f"{signature} missing metadata field {field}")

    return data


def list_signatures(dictionary: Dict[str, Any] | None = None) -> Iterable[str]:
    """Return canonical signatures in sorted order."""

    data = dictionary if dictionary is not None else load_dictionary()
    return sorted(data["signatures"])


def validate_signature(raw: str, dictionary: Dict[str, Any] | None = None) -> str:
    """Validate a signature and return its canonical form."""

    signature = canonicalize_signature(raw)
    _validate_signature_shape(signature)

    data = dictionary if dictionary is not None else load_dictionary()
    if signature not in data["signatures"]:
        raise SignatureDictionaryError(f"unknown Tier-6 signature: {signature}")

    return signature


def get_signature_metadata(raw: str, dictionary: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Return metadata for a valid signature."""

    data = dictionary if dictionary is not None else load_dictionary()
    signature = validate_signature(raw, data)
    return data["signatures"][signature]


def signature_tuple(raw: str, dictionary: Dict[str, Any] | None = None) -> Tuple[str, str, str]:
    """Return the canonical tuple: constraint_class, entity_role, disruption_class."""

    metadata = get_signature_metadata(raw, dictionary)
    return (
        metadata["constraint_class"],
        metadata["entity_role"],
        metadata["disruption_class"],
    )


def _validate_signature_shape(signature: str) -> None:
    if not SIGNATURE_PATTERN.match(signature):
        raise SignatureDictionaryError(
            "signature must match constraint_class.disruption_class using lowercase letters, digits, and underscores"
        )
