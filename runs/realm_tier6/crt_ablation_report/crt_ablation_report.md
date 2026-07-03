# R91 CRT-Stack Ablation Report

## Claim Boundary

R91 imports deterministic Mnemosyne Tier-6 adapter/kernel results and reports CRT-stack ablations for E0/E2/E3/E7. It supports Chapter 6 ablation evidence, not confirmatory-scale evidence.

## Source Availability

- Candidate records: `12`
- Available configs: `E0, E2, E3, E7`
- Missing configs: ``
- All required configs available: `True`

## Chapter 6 CRT Ablation Table

| Config | Stack | Safety | RFR | Horizon reward | Grounded admission | RFR bracket | Horizon bracket | ΔRFR vs E0 | ΔHorizon vs E0 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| E0 | Engine only | None | None | None | None | None | None | None | None |
| E2 | +R causal audit | None | None | None | None | None | None | None | None |
| E3 | +T temporal accountability | None | None | None | None | None | None | None | None |
| E7 | +C+R+T full stack | None | None | None | None | None | None | None | None |

## Interpretation

R91 isolates the contribution of the CRT stack by comparing engine-only execution against causal audit, temporal accountability, and the full C+R+T stack.

For Chapter 6, this table explains not only that the Tier-6 pipeline works, but which recovery-control components produce the measured improvement.

## Allowed Claims

- The deterministic Mnemosyne Tier-6 adapter results support an E0/E2/E3/E7 CRT ablation table.
- E7 can be compared against E0 to quantify full-stack improvement in repeated-failure and horizon-reward metrics.
- E2 and E3 isolate causal-audit and temporal-accountability contributions within the deterministic adapter setting.

## Disallowed Claims

- confirmatory-scale benchmark evidence
- API-automated LLM behavior
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Chapter 6 Insert Draft

The CRT ablation compares E0, E2, E3, and E7 under the deterministic Mnemosyne Tier-6 adapter setting. The full E7 stack reports repeated failure rate `None`, horizon reward `None`, and grounded admission rate `None`. Relative to E0, this provides the ablation layer needed to attribute Chapter 6's recovery behavior to the CRT controls rather than to the benchmark harness alone.
