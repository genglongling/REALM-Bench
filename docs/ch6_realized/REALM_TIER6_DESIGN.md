# REALM-Bench Tier 6 Design Notes

Tier 6 adds cross-episode causal-loop structure to existing REALM-Bench
Tier-4/5 task families. It does not introduce a competing benchmark.

A Tier-6 sequence is an ordered set of related episodes generated
deterministically from a base instance and seed.

Core principles:

1. Inheritance, not replacement.
2. Determinism.
3. Boundary-observable traces.
4. Safety as a gate.
5. Control sequences for anti-overfitting.

Primary metrics:

- repeated_failure_rate
- time_to_correction with right-censoring
- horizon_reward
- grounded_admission_rate

Safety counters:

- invalid_commit_count
- evidence_destroying_repair_count
- orphaned_dependent_count
