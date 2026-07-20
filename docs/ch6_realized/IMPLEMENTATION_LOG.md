# REALM-Bench Tier 6 Implementation Log

## C6-M0: Chapter 6 alignment and skeleton

Commit: 8ec9728e

Implemented the initial documentation and repository skeleton for
REALM-Bench Tier 6: Cross-Episode Causal Loop.

Key decision:
Tier 6 is a REALM-Bench v2 augmentation, not a standalone Quadrivium or
Mnemosyne benchmark.

## C6-M2: Trace schema and initial scorer

Commit: 755b318b

Implemented the first Tier-6 public trace schema and reference scorer.

Files:
- evaluation/tier6/schemas.py
- evaluation/tier6/scorer.py
- tests/tier6/test_schema.py
- tests/tier6/test_scorer.py

Important design choices:
- Tier-6 schema is lightweight and standard-library only.
- Parent evaluation package now uses lazy imports so Tier-6 modules do not
  require pandas or legacy evaluator dependencies.
- Scorer includes the safety gate, censoring discipline, control/non-control
  separation, cost aggregation, and placeholder B0/B* bracket fields.

Claim boundary:
This implements trace/scorer infrastructure only. It is not evidence for
H1-H5 or for Quadrivium learning performance.

## C6-M3: Deterministic Tier-6 sequence generator

Implemented deterministic Tier-6 sequence generation from existing REALM-Bench
families.

Files:
- datasets/T6/perturbations.py
- datasets/T6/generator.py
- tests/tier6/test_generator.py

Validation:
- python -m pytest -q tests/tier6
- python datasets/T6/generator.py

Observed development split:
- 20 Tier-6 tests passed
- 15 sequences
- 150 episodes
- 3 base families:
  - jobshop_breakdown
  - ride_or_routing_disruption
  - wedding_recovery
- 3 control sequences

Design notes:
The development split uses one base instance per family and five public seeds.
The first seed per family is forced to be a control sequence, giving a stable
20 percent control rate.

Claim boundary:
This milestone validates deterministic sequence construction and provenance.
It is not a system result and does not support H1-H5.
