# R87 Mnemosyne Live-LLM Scorer Handoff Import

## Purpose

R87 imports the Mnemosyne R86 official-scorer handoff bundle into REALM-Bench.

It validates that the live-LLM cases admitted, flagged, or rejected by Mnemosyne can be consumed on the REALM side as deterministic official-scorer-facing cases.

## Input

Default input:

- `/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/results/realm_tier6_live_llm_manual/realm_scorer_handoff/realm_scorer_handoff_bundle.json`

The input can also be supplied explicitly:

    python -m evaluation.tier6.mnemosyne_live_llm_import import \
      --handoff-bundle /path/to/realm_scorer_handoff_bundle.json

## Output

Default output directory:

- `runs/realm_tier6/mnemosyne_live_llm_scorer_import/`

Generated files:

- `mnemosyne_live_llm_import_report.json`
- `mnemosyne_live_llm_import_report.md`

## What R87 Validates

For each imported case, R87 checks:

- case id is present
- episode id is present
- model pack name is present
- Mnemosyne admission label is valid
- REALM-facing scorer action is valid
- the case does not claim official REALM score yet
- the case declares that official REALM scorer is still required

## Claim Boundary

R87 phase 1 is a REALM-Bench-side deterministic import report.

It does not claim:

- final official REALM scoring
- confirmatory Chapter 6 evidence
- API-automated LLM behavior
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

Mnemosyne owns admission. REALM owns scoring.

## Next Step

R88 should connect these imported cases to the actual Tier-6 scorer rather than only validating the handoff contract.
