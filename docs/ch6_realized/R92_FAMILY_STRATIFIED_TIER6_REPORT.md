# R92 Family-Stratified REALM Tier-6 Report

## Purpose

R92 adds family stratification to the Chapter 6 evidence package.

It scores deterministic B0/B* Tier-6 baselines separately for each public development family and places the R88 Mnemosyne live-LLM pilot as a jobshop-family pilot row.

## Families

The deterministic development set covers:

- `jobshop_breakdown`
- `ride_or_routing_disruption`
- `wedding_recovery`

Each family contributes five sequences and fifty episodes in the default three-family development set.

## Inputs

Tier-6 generator:

- `datasets/T6/generator.py`

Baseline emitters:

- `evaluation/tier6/baseline_traces.py`

R88 score report:

- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_score_report.json`

## Command

    python -m analysis.realm_tier6.family_stratified_report build

## Outputs

Default output directory:

- `runs/realm_tier6/family_stratified_report/`

Generated files:

- `family_stratified_report.json`
- `family_stratified_report.md`
- `chapter6_family_stratified_table.json`

## Chapter 6 Use

R92 supports the claim that the deterministic Tier-6 baseline layer is not tied to one task family.

It does not yet support the stronger claim that live-LLM Mnemosyne behavior generalizes across all families. The live-LLM pilot remains a jobshop-family pilot row.

## Claim Boundary

R92 supports family-stratified pilot-plus-baseline evidence.

It does not claim:

- family-generalized live-LLM evidence across all families
- confirmatory-scale benchmark evidence
- API-automated live LLM evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Next Step

R93 should expand the live-LLM pilot beyond one E7 jobshop sequence, or prepare the final Chapter 6 closure ledger if the book only needs bounded pilot evidence.
