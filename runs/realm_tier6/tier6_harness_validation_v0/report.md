# REALM-Bench Tier 6 Analysis Report

Status: deterministic harness validation only.

This implements and validates the REALM-Bench Tier-6 causal-loop harness; pilot and confirmatory runs follow under the registered protocol.

This report is regenerated from `events.jsonl` and `manifest.json`.
It validates analysis reproducibility only. It is not a system result and must
not be used as evidence for H1-H5.

## Manifest

- Run ID: tier6_harness_validation_v0
- Phase: deterministic_harness_validation
- Claim status: not_chapter_result
- Sequences: 15
- Episodes: 150
- Events: 90
- Families: jobshop_breakdown, ride_or_routing_disruption, wedding_recovery

## Scorer summary

| Metric | Value |
|---|---:|
| Safety passed | True |
| Invalid commits | 0 |
| Evidence-destroying repairs | 0 |
| Orphaned dependents | 0 |
| Repeated failure rate | 1.0 |
| Control repeated failure rate | 0.0 |
| Observed TTC count | 12 |
| Censored TTC count | 78 |
| Horizon reward mean | 0.16666666666666666 |
| RFR bracket position | 0.0 |
| Horizon bracket position | 0.16666666666666666 |

## Claim boundary

The deterministic fixture constructs expected causal-loop events by design.
These outputs validate trace generation, schema validation, scoring,
censoring, and analysis regeneration only. Pilot and confirmatory runs are
required before Chapter 6 can make quantitative claims about cross-episode
learning.
