# R90 Full Deterministic REALM Tier-6 Report

## Claim Boundary

R90 scores the deterministic Tier-6 development set with B0 and B* reference baselines and reports the R88 Mnemosyne live-LLM pilot beside those anchors. This supports Chapter 6 pilot-plus-baseline evidence, not confirmatory-scale evidence.

## Development Set

- Sequences: `15`
- Episodes: `150`
- Control sequences: `3`
- Non-control sequences: `12`
- Episodes per sequence: `10`
- Families: `jobshop_breakdown, ride_or_routing_disruption, wedding_recovery`

## Chapter 6 Deterministic + Pilot Table

| System | Evidence type | Events | Safety | RFR | Horizon reward | Grounded admission | RFR bracket | Horizon bracket |
|---|---|---:|---|---:|---:|---:|---:|---:|
| B0 memoryless replay | deterministic_reference_baseline | 150 | True | 1.0 | 0.0 | None | 0.0 | 0.0 |
| B* oracle memory | deterministic_reference_baseline | 150 | True | 0.0 | 0.96 | None | 1.0 | 0.96 |
| Mnemosyne live-LLM pilot | manual_live_llm_pilot | 40 | True | 0.0 | 0.90125 | 0.725 | 1.0 | 0.90125 |

## Baseline Interpretation

B0 memoryless replay scores RFR = `1.0` and horizon reward = `0.0`.

B* oracle memory scores RFR = `0.0` and horizon reward = `0.96`.

## R88 Live-LLM Pilot Placement

The R88 Mnemosyne live-LLM pilot is placed beside the deterministic B0/B* anchors as a pilot row, not as confirmatory-scale evidence.

It reports safety passed = `True`, horizon reward mean = `0.90125`, and grounded admission rate = `0.725`.

## Allowed Claims

- The Tier-6 deterministic development set can be scored end to end.
- B0 and B* reference baselines bracket the repeated-failure and horizon-reward metrics.
- The R88 Mnemosyne live-LLM pilot can be reported beside deterministic Tier-6 anchors.
- The evidence supports Chapter 6 pilot-plus-baseline closure.

## Disallowed Claims

- confirmatory-scale benchmark evidence
- API-automated live LLM evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Chapter 6 Insert Draft

The full deterministic Tier-6 development set was scored with two reference anchors: B0 memoryless replay and B* oracle memory. B0 establishes the lower anchor with repeated failure rate `1.0` and horizon reward `0.0`; B* establishes the upper anchor with repeated failure rate `0.0` and horizon reward `0.96`. The R88 Mnemosyne live-LLM pilot is reported beside these anchors as pilot integration evidence. This closes the deterministic baseline-and-pilot evidence layer for Chapter 6, while leaving confirmatory-scale evaluation to the next benchmark expansion.
