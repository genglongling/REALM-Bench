# R92 Family-Stratified REALM Tier-6 Report

## Claim Boundary

R92 stratifies deterministic Tier-6 B0/B* baselines by family and places the R88 Mnemosyne live-LLM pilot as a family-assigned pilot row. This supports Chapter 6 family-stratified pilot-plus-baseline evidence, not confirmatory-scale evidence.

## Families

- `jobshop_breakdown`: sequences `5`, episodes `50`, controls `1`
- `ride_or_routing_disruption`: sequences `5`, episodes `50`, controls `1`
- `wedding_recovery`: sequences `5`, episodes `50`, controls `1`

## Chapter 6 Family-Stratified Table

| Family | System | Evidence type | Events | Safety | RFR | Horizon reward | Grounded admission | RFR bracket | Horizon bracket |
|---|---|---|---:|---|---:|---:|---:|---:|---:|
| jobshop_breakdown | B0 memoryless replay | deterministic_reference_baseline | 50 | True | 1.0 | 0.0 | None | 0.0 | 0.0 |
| jobshop_breakdown | B* oracle memory | deterministic_reference_baseline | 50 | True | 0.0 | 0.96 | None | 1.0 | 0.96 |
| ride_or_routing_disruption | B0 memoryless replay | deterministic_reference_baseline | 50 | True | 1.0 | 0.0 | None | 0.0 | 0.0 |
| ride_or_routing_disruption | B* oracle memory | deterministic_reference_baseline | 50 | True | 0.0 | 0.96 | None | 1.0 | 0.96 |
| wedding_recovery | B0 memoryless replay | deterministic_reference_baseline | 50 | True | 1.0 | 0.0 | None | 0.0 | 0.0 |
| wedding_recovery | B* oracle memory | deterministic_reference_baseline | 50 | True | 0.0 | 0.96 | None | 1.0 | 0.96 |
| jobshop_breakdown | Mnemosyne live-LLM pilot | manual_live_llm_pilot | 40 | True | 0.0 | 0.90125 | 0.725 | 1.0 | 0.90125 |

## Interpretation

The deterministic baseline layer is stratified across all available Tier-6 development families. This prevents Chapter 6 from appearing to rely only on a single task family.

The R88 live-LLM pilot remains a jobshop-family pilot row. It is not yet family-generalized live-LLM evidence.

## Allowed Claims

- Tier-6 deterministic baseline behavior can be stratified by family.
- The Chapter 6 evidence covers jobshop, routing, and wedding recovery families at the deterministic baseline layer.
- The R88 live-LLM pilot can be reported as a jobshop-family pilot row with explicit claim boundary.

## Disallowed Claims

- family-generalized live-LLM evidence across all families
- confirmatory-scale benchmark evidence
- API-automated live LLM evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Chapter 6 Insert Draft

To test whether the Tier-6 evidence is tied to a single task family, we stratified the deterministic B0/B* baseline layer by family. The development set covers job-shop breakdown, routing disruption, and wedding recovery families. For each family, B0 and B* remain valid reference anchors under the same public Tier-6 scorer. The R88 Mnemosyne live-LLM pilot is reported separately as a jobshop-family pilot row. Thus, Chapter 6 has family-stratified deterministic baseline evidence, while live-LLM family generalization remains a future expansion.
