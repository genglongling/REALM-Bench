# REALM-Bench Tier 6: Cross-Episode Causal Loop

Tier 6 extends REALM-Bench with cross-episode causal-loop sequences.

It derives episode sequences from existing Tier-4/5-style REALM-Bench task
families rather than introducing a competing benchmark. A Tier-6 sequence tests
whether a system can commit, observe outcomes, record discrepancy, and improve
future behavior across related episodes while preserving safety.

## Status

Draft implementation for REALM-Bench v2.

This directory currently provides:

- deterministic sequence generation
- perturbation metadata
- versioned failure-signature dictionary
- public development seed set
- frozen public pilot subset
- deterministic harness fixture generation

## Claim boundary

The deterministic fixture and baselines validate the Tier-6 harness, trace
schema, scorer, censoring discipline, control-sequence separation, baseline
bracket, and analysis regeneration.

They are not Quadrivium/Mnemosyne system results and must not be used as
evidence for H1-H5.

Canonical sentence:

> This implements and validates the REALM-Bench Tier-6 causal-loop harness;
> pilot and confirmatory runs follow under the registered protocol.

## Key files

```text
datasets/T6/
  README.md
  dictionary_v0.json
  public_seeds_v0.json
  pilot_subset_v0.json
  signatures.py
  perturbations.py
  generator.py
  fixture_emitter.py

evaluation/tier6/
  schemas.py
  scorer.py
  baselines.py
  baseline_traces.py

analysis/realm_tier6/
  analyze_run.py

runs/realm_tier6/
  tier6_harness_validation_v0/
  tier6_B0_memoryless_replay_v0/
  tier6_Bstar_oracle_memory_v0/
```

## Validation commands

Run from the repository root:

```bash
python -m pytest -q tests/tier6
python datasets/T6/pilot.py
python datasets/T6/generator.py
python datasets/T6/fixture_emitter.py
python evaluation/tier6/baseline_traces.py
python analysis/realm_tier6/analyze_run.py runs/realm_tier6/tier6_harness_validation_v0
```

Expected current validation:

```text
37 Tier-6 tests passing

pilot subset:
  5 sequences
  50 episodes
  1 control sequence
  family: jobshop_breakdown

development generator:
  15 sequences
  150 episodes
  3 families:
    jobshop_breakdown
    ride_or_routing_disruption
    wedding_recovery
  3 control sequences

fixture harness:
  90 events
  safety passed

B0 memoryless replay:
  repeated_failure_rate = 1.0
  horizon_reward_mean = 0.0
  safety_passed = true

B* oracle memory:
  repeated_failure_rate = 0.0
  horizon_reward_mean = 0.96
  safety_passed = true
```

## Trace contract

A Tier-6 submission emits one JSONL event stream per run. The scorer computes
all metrics from boundary-observable trace records.

Core event fields include:

```text
sequence_id
episode_id
seed
event
proposal_id
failure_signature
predicted_outcome
observed_outcome
delta
constraint_violations
repair
cost
time_to_correction
time_to_correction_censored
invalid_commit_count
evidence_destroying_repair_count
orphaned_dependent_count
```

## Primary metrics

```text
repeated_failure_rate
time_to_correction with right-censoring
horizon_reward
grounded_admission_rate
```

## Safety gate

The following counters must remain exactly zero:

```text
invalid_commit_count
evidence_destroying_repair_count
orphaned_dependent_count
```

A system that improves learning metrics but violates the safety gate fails
Tier 6.

## Baselines

Tier 6 currently includes two reference trace emitters:

```text
B0 memoryless replay
  no cross-episode correction retained

B* oracle memory
  receives ground-truth correction after observation
```

These define the initial bracket for interpreting realized cross-episode gain.
