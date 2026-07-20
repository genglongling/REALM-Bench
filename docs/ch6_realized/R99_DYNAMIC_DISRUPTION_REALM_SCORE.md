# R99 Dynamic Disruption REALM-Bench Score

## Purpose

R99 imports Mnemosyne R98 dynamic disruption replay events into REALM-Bench and invokes the public Tier-6 scorer.

This is the first REALM-side official scoring step for the dynamic live-repair pilot.

## Input

Default input:

- `/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/results/realm_tier6_dynamic_disruption_replay/jobshop_e7_dynamic_pilot/dynamic_replay_events.jsonl`

The input is produced by Mnemosyne R98.

## Output

Default output directory:

- `runs/realm_tier6/dynamic_disruption_official_score/`

Generated files:

- `dynamic_disruption_import_report.json`
- `dynamic_disruption_score_report.json`
- `dynamic_disruption_score_report.md`
- `dynamic_disruption_events.jsonl`

## Scoring Path

R99 uses the public Tier-6 scoring path:

- `evaluation.tier6.schemas.validate_trace`
- `evaluation.tier6.scorer.score_trace`

It does not introduce a private scoring formula.

## Claim Boundary

R99 scores one bounded dynamic jobshop/E7 pilot.

It does not claim:

- family-generalized dynamic live-LLM behavior
- confirmatory-scale benchmark evidence
- API-automated live-LLM evaluation
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Next Step

R100 should build the final Chapter 6 dynamic closure ledger by combining:

- R89 static live-LLM pilot evidence
- R90 deterministic baseline report
- R91 CRT ablation
- R92 family stratification
- R93 expansion gate
- R96 dynamic prompt pack
- R97 dynamic response collection
- R98 Mnemosyne dynamic admission/replay
- R99 REALM-Bench dynamic score
