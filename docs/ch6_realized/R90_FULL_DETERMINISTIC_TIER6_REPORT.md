# R90 Full Deterministic REALM Tier-6 Report

## Purpose

R90 builds the deterministic baseline-and-pilot evidence layer for Chapter 6.

It scores the public Tier-6 development set with:

- B0 memoryless replay
- B* oracle memory

It then places the R88 Mnemosyne live-LLM pilot beside those deterministic anchors.

## Inputs

Tier-6 generator:

- `datasets/T6/generator.py`

Baseline emitters:

- `evaluation/tier6/baseline_traces.py`

R88 live-LLM pilot score report:

- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_score_report.json`

## Command

    python -m analysis.realm_tier6.full_deterministic_report build

Default output directory:

- `runs/realm_tier6/full_deterministic_report/`

Generated files:

- `full_deterministic_report.json`
- `full_deterministic_report.md`
- `chapter6_full_deterministic_table.json`

## Chapter 6 Use

R90 supports a Chapter 6 table with:

- B0 lower deterministic anchor
- B* upper deterministic anchor
- Mnemosyne live-LLM pilot placement

This gives Chapter 6 two evidence layers:

1. deterministic reference baselines
2. live-LLM pilot integration evidence

## Claim Boundary

R90 supports Chapter 6 pilot-plus-baseline closure.

It does not claim:

- confirmatory-scale benchmark evidence
- API-automated live LLM evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Next Step

R91 should add CRT-stack ablations, especially E0/E2/E3/E7, so the chapter can show not only that the pipeline works, but which pieces of the CRT stack matter.
