# R99 REALM Tier-6 Dynamic Disruption Scoring Report

## Claim Boundary

REALM Tier-6 public scorer invoked on Mnemosyne R98 dynamic disruption replay events. This is a bounded dynamic jobshop/E7 pilot score, not a family-generalized or confirmatory-scale result.

## Pilot

- Sequence: `T6-DYN-jobshop-e7-0001`
- Config: `E7`
- Condition label: `full_crt_stack`
- Official scorer invoked: `True`
- Score scope: `mnemosyne_dynamic_disruption_replay_events`
- Events: `40`

## Dynamic Replay Summary

| Metric | Value |
|---|---:|
| Dynamic admits | 24 |
| Dynamic rejects | 16 |
| Dynamic observes | 0 |
| Dynamic safe rejections | 4 |

## Overall Tier-6 Score

| Metric | Value |
|---|---:|
| Safety passed | True |
| Repeated failure rate | 0.0 |
| Horizon reward mean | 0.925 |
| Grounded admission rate | 0.6 |
| TTC observed mean | 0.725 |
| TTC observed count | 40 |
| TTC censored count | 0 |

## Pack Scores

| Pack | Events | Safety | RFR | Horizon reward | Grounded admission | TTC mean |
|---|---:|---|---:|---:|---:|---:|
| claude | 10 | True | 0.0 | 0.975 | 0.9 | 0.9 |
| deepseek_expert | 10 | True | 0.0 | 0.95 | 0.5 | 0.8 |
| deepseek_instant | 10 | True | 0.0 | 0.9 | 0.5 | 0.7 |
| gpt | 10 | True | 0.0 | 0.875 | 0.5 | 0.5 |

## Interpretation

R99 is the REALM-side official scoring step for the bounded dynamic disruption pilot. It consumes Mnemosyne R98 replay events, validates Tier-6 trace schema, invokes the public Tier-6 scorer, and reports safety, repeated-failure, horizon-reward, grounded-admission, and time-to-correction metrics.
