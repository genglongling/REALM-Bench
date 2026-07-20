# R91 CRT-Stack Ablation Report

## Purpose

R91 adds the CRT ablation layer needed to close Chapter 6 experimentally.

It imports deterministic Mnemosyne Tier-6 adapter/kernel results and compares:

- E0: engine only
- E2: +R causal audit
- E3: +T temporal accountability
- E7: +C+R+T full stack

## Default Mnemosyne Search Roots

- `/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/results/realm_tier6_mnemosyne_kernel`
- `/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/results/realm_tier6_mnemosyne_runtime`
- `/Users/edward.chang/ALAS/AGIV3/mnemosyne_product/results/realm_tier6_mnemosyne`

## Command

    python -m analysis.realm_tier6.crt_ablation_report build

## Outputs

Default output directory:

- `runs/realm_tier6/crt_ablation_report/`

Generated files:

- `crt_ablation_report.json`
- `crt_ablation_report.md`
- `chapter6_crt_ablation_table.json`

## Chapter 6 Use

R91 explains which CRT components matter.

R90 showed the deterministic baseline-and-pilot evidence layer. R91 adds the ablation layer:

- E0 establishes engine-only behavior.
- E2 isolates causal audit.
- E3 isolates temporal accountability.
- E7 shows the full CRT stack.

## Claim Boundary

R91 supports deterministic CRT ablation evidence.

It does not claim:

- confirmatory-scale benchmark evidence
- API-automated LLM behavior
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Next Step

R92 should stratify results by Tier-6 family so Chapter 6 can show whether recovery behavior is consistent across job-shop breakdown, routing disruption, and wedding recovery families.
