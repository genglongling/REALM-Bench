# R88 Mnemosyne Live-LLM REALM Tier-6 Scoring Integration

## Purpose

R88 connects the Mnemosyne live-LLM handoff pipeline back to the REALM Tier-6 public scorer.

It consumes the R87 REALM-side import report, converts imported Mnemosyne handoff cases into Tier-6 schema-valid events, and invokes `evaluation.tier6.scorer.score_trace`.

## Input

Default input:

- `runs/realm_tier6/mnemosyne_live_llm_scorer_import/mnemosyne_live_llm_import_report.json`

This file is produced by R87.

## Command

    python -m evaluation.tier6.mnemosyne_live_llm_score score

Default output:

- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_score_report.json`
- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_score_report.md`
- `runs/realm_tier6/mnemosyne_live_llm_official_score/mnemosyne_live_llm_events.jsonl`

## What R88 Scores

R88 maps Mnemosyne-side import dispositions into Tier-6 scorer events:

- admitted proposal -> `admit`
- flagged admission -> `admit`
- protective rejection -> `reject`
- safety failure -> `commit`
- rejection -> `reject`

The resulting events are validated by the Tier-6 schema and scored by the public Tier-6 scorer.

## Claim Boundary

R88 invokes the REALM Tier-6 public scorer on deterministic Mnemosyne handoff-derived events.

It is pilot scoring integration over one E7 sequence.

It does not claim:

- final confirmatory Chapter 6 evidence
- API-automated LLM behavior
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

Mnemosyne owns admission. REALM owns scoring.

## Chapter 6 Use

R88 can support the first Chapter 6 pilot scoring table.

R89 should consolidate the R83.5a through R88 reports into a chapter-ready evidence package with explicit claim boundaries.
