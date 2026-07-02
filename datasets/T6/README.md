# REALM-Bench Tier 6: Cross-Episode Causal Loop

Tier 6 extends REALM-Bench with cross-episode causal-loop sequences.
It derives episode sequences from existing Tier-4/5 instances rather than
introducing a competing benchmark.

A Tier-6 sequence tests whether a system can commit, observe outcomes,
record discrepancy, and improve future behavior across related episodes
while preserving safety.

This directory will contain:

- deterministic sequence generator
- perturbation operators
- failure-signature dictionary
- public seed list
- pilot subset definition
