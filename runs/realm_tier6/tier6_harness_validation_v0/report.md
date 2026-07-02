# REALM-Bench Tier 6 Harness Validation Report

Status: deterministic harness validation only.

This implements and validates the REALM-Bench Tier-6 causal-loop harness; pilot and confirmatory runs follow under the registered protocol.

This report validates trace emission, schema compliance, scorer consumption,
right-censoring, control-sequence separation, and safety-gate reporting.
It is not a system result and must not be used as evidence for H1-H5.

## Manifest

- Run ID: tier6_harness_validation_v0
- Phase: deterministic_harness_validation
- Claim status: not_chapter_result
- Sequences: 15
- Episodes: 150
- Events: 90
- Families: jobshop_breakdown, ride_or_routing_disruption, wedding_recovery

## Scorer summary

- Safety passed: True
- Invalid commits: 0
- Evidence-destroying repairs: 0
- Orphaned dependents: 0
- Repeated failure rate: 1.0
- Control repeated failure rate: 0.0
- Observed time-to-correction count: 12
- Censored time-to-correction count: 78

## Claim boundary

The deterministic fixture constructs expected causal-loop events by design.
These events validate the harness and scorer only. Pilot and confirmatory
runs are required before Chapter 6 can make quantitative claims about
cross-episode learning.
