# R88 REALM Tier-6 Mnemosyne Live-LLM Scoring Report

## Claim Boundary

REALM Tier-6 public scorer invoked on deterministic Mnemosyne handoff-derived events. This is pilot scoring integration over one E7 sequence, not final confirmatory Chapter 6 evidence.

## Pilot

- Sequence: `T6-7e17ef0cc5f3`
- Config: `E7`
- Condition label: `full_crt_stack`
- Official scorer invoked: `True`
- Score scope: `mnemosyne_live_llm_handoff_derived_events`
- Events: `40`

## Overall Tier-6 Score

| Metric | Value |
|---|---:|
| Safety passed | True |
| Repeated failure rate | 0.0 |
| Horizon reward mean | 0.90125 |
| Grounded admission rate | 0.725 |
| TTC observed count | 0 |
| TTC censored count | 40 |

## Pack Scores

| Pack | Events | Safety | RFR | Horizon reward | Grounded admission | Invalid commits |
|---|---:|---|---:|---:|---:|---:|
| claude | 10 | True | 0.0 | 1.0 | 1.0 | 0 |
| deepseek_expert | 10 | True | 0.0 | 0.855 | 0.5 | 0 |
| deepseek_instant | 10 | True | 0.0 | 0.885 | 0.7 | 0 |
| gpt | 10 | True | 0.0 | 0.865 | 0.7 | 0 |

## Per-Event Scorer Inputs

| Pack | Episode | Event | Disposition | Horizon reward | Grounded | Failure signature |
|---|---:|---|---|---:|---|---|
| claude | 1 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 2 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 3 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 4 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 5 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 6 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 7 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 8 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 9 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| claude | 10 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_expert | 1 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_expert | 2 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_expert | 3 | admit | eligible_for_official_realm_flagged_scoring | 0.75 | False |  |
| deepseek_expert | 4 | admit | eligible_for_official_realm_flagged_scoring | 0.75 | False |  |
| deepseek_expert | 5 | admit | eligible_for_official_realm_flagged_scoring | 0.75 | False |  |
| deepseek_expert | 6 | admit | eligible_for_official_realm_flagged_scoring | 0.75 | False |  |
| deepseek_expert | 7 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_expert | 8 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_expert | 9 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| deepseek_expert | 10 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 1 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| deepseek_instant | 2 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 3 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 4 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 5 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 6 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 7 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| deepseek_instant | 8 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| deepseek_instant | 9 | admit | eligible_for_official_realm_flagged_scoring | 0.75 | False |  |
| deepseek_instant | 10 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 1 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 2 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 3 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 4 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 5 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| gpt | 6 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| gpt | 7 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 8 | reject | eligible_for_official_realm_protective_rejection_scoring | 0.55 | False | mnemosyne_live_llm.screened_before_commit |
| gpt | 9 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |
| gpt | 10 | admit | eligible_for_official_realm_admitted_scoring | 1.0 | True |  |

## Interpretation

R88 is the first REALM-Bench-side scoring integration for the Mnemosyne live-LLM admission pipeline. The public Tier-6 scorer is invoked on schema-valid events derived from the R87 imported handoff cases.

The result is suitable for the Chapter 6 implementation/results ledger as pilot scoring integration. It is not yet confirmatory-scale evidence.
