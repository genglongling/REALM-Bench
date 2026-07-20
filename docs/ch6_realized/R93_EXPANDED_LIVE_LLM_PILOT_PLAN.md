# R93 Expanded Live-LLM Pilot Plan

## Purpose

R93 defines the collection matrix needed to expand the R88 live-LLM pilot beyond one E7 jobshop sequence.

It does not collect new LLM responses and does not score new live-LLM cases.

## Why This Exists

R88 gives Chapter 6 a real live-LLM pilot:

- one E7 full CRT-stack sequence
- one jobshop-family sequence
- four proposer packs
- 40 handoff-derived scorer events

R92 shows deterministic family-stratified baseline evidence across:

- `jobshop_breakdown`
- `ride_or_routing_disruption`
- `wedding_recovery`

R93 asks what additional collection would be required to make the live-LLM pilot family-generalized.

## Default Expansion Target

R93 targets:

- one non-control E7 sequence per family
- three families
- four proposer packs:
  - Claude
  - GPT
  - DeepSeek expert
  - DeepSeek instant
- ten episodes per sequence

Total target cases:

- 3 families × 1 sequence × 4 packs × 10 episodes = 120 cases

Existing R88 jobshop cases:

- 40 cases

Additional cases needed:

- 80 cases

## Command

    python -m analysis.realm_tier6.expanded_live_llm_pilot_plan build

## Outputs

Default output directory:

- `runs/realm_tier6/expanded_live_llm_pilot_plan/`

Generated files:

- `expanded_live_llm_pilot_plan.json`
- `expanded_live_llm_pilot_plan.md`
- `collection_matrix.json`

## Chapter 6 Use

R93 is useful for claim discipline.

It supports saying:

- Chapter 6 has bounded live-LLM pilot evidence.
- The exact expansion path to family-generalized live-LLM evidence is defined.
- Family-generalized live-LLM evidence is not yet claimed.

## Claim Boundary

R93 does not claim:

- new live-LLM results beyond R88
- family-generalized live-LLM evidence
- API-automated live LLM evidence
- confirmatory-scale benchmark evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Next Step

R94 should build the final Chapter 6 closure ledger by combining R89, R90, R91, R92, and R93.
