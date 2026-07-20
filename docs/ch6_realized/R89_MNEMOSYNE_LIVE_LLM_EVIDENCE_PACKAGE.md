# R89 Mnemosyne Live-LLM Chapter 6 Evidence Package

## Purpose

R89 consolidates the Mnemosyne and REALM-Bench live-LLM Tier-6 reports into a Chapter 6 pilot evidence package.

It collects the pipeline from manual live-LLM responses through Mnemosyne admission, kernel tracing, runtime evaluation, REALM handoff, REALM import, and REALM Tier-6 scoring.

## Inputs

REALM-Bench inputs:

- `runs/realm_tier6/mnemosyne_live_llm_scorer_import/mnemosyne_live_llm_import_report.json`
- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_score_report.json`

Mnemosyne inputs:

- `results/realm_tier6_live_llm_manual/kernel_import_report/comparison_report.json`
- `results/realm_tier6_live_llm_manual/kernel_trace_report/kernel_trace_report.json`
- `results/realm_tier6_live_llm_manual/runtime_evaluator_report/runtime_evaluator_report.json`
- `results/realm_tier6_live_llm_manual/realm_score_bridge_report/realm_score_bridge_report.json`
- `results/realm_tier6_live_llm_manual/realm_scorer_handoff/realm_scorer_handoff_bundle.json`

## Command

    python -m analysis.realm_tier6.mnemosyne_live_llm_ch6_package build

## Outputs

Default output directory:

- `runs/realm_tier6/mnemosyne_live_llm_ch6_package/`

Generated files:

- `ch6_evidence_package.json`
- `ch6_evidence_package.md`
- `chapter6_pilot_results_table.json`

## Chapter 6 Use

R89 is suitable for:

- Chapter 6 implementation narrative
- Chapter 6 pilot scoring table
- results ledger update
- claim-boundary statement

R89 is not suitable for:

- final confirmatory claims
- full-scale statistical conclusions
- claims of AGI, wisdom, or autonomous scientific reasoning

## Current Pilot Result

The R88 scorer integration reports:

- 40 handoff-derived events
- public REALM Tier-6 scorer invoked
- safety passed
- horizon reward mean 0.90125
- grounded admission rate 0.725

These are pilot results for one E7 sequence.
