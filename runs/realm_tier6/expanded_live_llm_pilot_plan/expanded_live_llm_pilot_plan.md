# R93 Expanded Live-LLM Pilot Plan

## Claim Boundary

R93 defines the expanded live-LLM collection matrix needed to move from the R88 one-sequence E7 jobshop pilot to a three-family E7 pilot. It does not collect or score new LLM responses.

## Chapter 6 Status

- Bounded pilot ready: `True`
- Family-generalized live-LLM ready: `False`
- Additional cases needed for three-family live pilot: `120`

## Selected Sequences

| Family | Sequence | Base instance | Episodes | Hazards |
|---|---|---|---:|---|
| jobshop_breakdown | `T6-76095aec5ba1` | `jobshop_breakdown:datasets/J4/custom/j4_custom_001.json` | 10 | repair.deleted_trigger_evidence |
| ride_or_routing_disruption | `T6-c574beceb46d` | `ride_or_routing_disruption:datasets/P4/disruptions/p4_instance_001.json` | 10 | repair.deleted_trigger_evidence |
| wedding_recovery | `T6-6039d2a74221` | `wedding_recovery:datasets/P8/disruptions/p8_instance_001.json` | 10 | stale_world.route_time_underestimated, temporal.myopic_choice_causes_later_failure |

## Collection Matrix Summary

- Total target cases: `120`
- Existing R88 collected cases: `0`
- Planned not collected cases: `120`

| Family | Total | Existing R88 | Planned not collected |
|---|---:|---:|---:|
| jobshop_breakdown | 40 | 0 | 40 |
| ride_or_routing_disruption | 40 | 0 | 40 |
| wedding_recovery | 40 | 0 | 40 |

## Interpretation

R93 keeps Chapter 6 honest. The chapter can close with bounded pilot evidence, but it should not claim family-generalized live-LLM evidence until the planned cases are actually collected and scored.

The expanded three-family E7 live-LLM pilot would require the existing jobshop R88 cases plus new routing and wedding-family response packs.

## Allowed Claims

- Chapter 6 has bounded live-LLM pilot evidence from R88.
- R93 defines the exact additional cases needed for a three-family live-LLM pilot.
- The expanded collection target is auditable before new manual or API responses are collected.

## Disallowed Claims

- new live-LLM results beyond R88
- family-generalized live-LLM evidence
- API-automated live LLM evidence
- confirmatory-scale benchmark evidence
- production CTL-domain StateView realization
- proof of AGI, wisdom, or autonomous scientific reasoning

## Chapter 6 Insert Draft

To determine whether the R88 live-LLM pilot should be expanded before publication, we generated an explicit three-family collection matrix. The matrix targets one non-control E7 sequence per development family and four proposer packs per sequence. The existing R88 jobshop pilot accounts for `0` cases; a full three-family live-LLM pilot would require `120` additional cases. We therefore treat the current Chapter 6 live-LLM result as bounded pilot evidence, not family-generalized evidence.
