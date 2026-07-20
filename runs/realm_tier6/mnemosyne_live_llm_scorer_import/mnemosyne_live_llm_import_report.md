# R87 REALM Tier-6 Mnemosyne Live-LLM Scorer Import

## Claim Boundary

REALM-Bench-side deterministic import report only. This consumes the Mnemosyne R86 handoff bundle and validates official-scorer-facing cases. It does not yet claim final official REALM scoring or confirmatory Chapter 6 evidence.

## Imported Pilot

- Sequence: `T6-7e17ef0cc5f3`
- Config: `E7`
- Condition label: `full_crt_stack`
- Official REALM score: `False`
- Import type: `mnemosyne_live_llm_scorer_handoff_import`

## Summary

- Cases: `40`
- Validation passed: `40`
- Validation failed: `0`
- All cases valid: `True`

## Disposition Counts

| Disposition | Count |
|---|---:|
| eligible_for_official_realm_admitted_scoring | 29 |
| eligible_for_official_realm_flagged_scoring | 5 |
| eligible_for_official_realm_protective_rejection_scoring | 6 |

## Pack Summary

| Pack | Cases | Passed | Failed | Admission labels | Dispositions |
|---|---:|---:|---:|---|---|
| claude | 10 | 10 | 0 | `{'clean_admission': 10}` | `{'eligible_for_official_realm_admitted_scoring': 10}` |
| gpt | 10 | 10 | 0 | `{'clean_admission': 7, 'protective_rejection': 3}` | `{'eligible_for_official_realm_admitted_scoring': 7, 'eligible_for_official_realm_protective_rejection_scoring': 3}` |
| deepseek_expert | 10 | 10 | 0 | `{'clean_admission': 5, 'flagged_admission': 4, 'protective_rejection': 1}` | `{'eligible_for_official_realm_admitted_scoring': 5, 'eligible_for_official_realm_flagged_scoring': 4, 'eligible_for_official_realm_protective_rejection_scoring': 1}` |
| deepseek_instant | 10 | 10 | 0 | `{'protective_rejection': 2, 'clean_admission': 7, 'flagged_admission': 1}` | `{'eligible_for_official_realm_protective_rejection_scoring': 2, 'eligible_for_official_realm_admitted_scoring': 7, 'eligible_for_official_realm_flagged_scoring': 1}` |

## Per-Case Import

| Pack | Episode | Valid | Admission label | Scorer action | Import disposition | Unsupported | Summary |
|---|---:|---|---|---|---|---:|---|
| claude | 1 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Verify breakdown state, then repair the existing schedule via minimal right-shift with optional m... |
| claude | 2 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Reactive partial reschedule for the J4 breakdown instance: freeze operations already completed or... |
| claude | 3 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 2 | Affected-operations rescheduling (right-shift + local re-sequencing) for the J4 jobshop breakdown... |
| claude | 4 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Localized right-shift repair of the broken machine's queue with optional migration of feasible op... |
| claude | 5 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Apply an affected-operations rescheduling (AOR) repair for the J4 breakdown instance: freeze all ... |
| claude | 6 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Affected-operations local reschedule after breakdown: freeze failed machine, reroute or right-shi... |
| claude | 7 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Treat episode 7 as a machine-breakdown disruption on the J4 instance: freeze the pre-breakdown sc... |
| claude | 8 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Verify the breakdown signal against a fresh state observation, then apply a minimal right-shift r... |
| claude | 9 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Affected-operations right-shift repair on the broken machine with one availability observation be... |
| claude | 10 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 2 | Reactive right-shift repair for the J4 breakdown: freeze completed/in-progress operations, rerout... |
| gpt | 1 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Start with evidence-preserving inspection only; no repair or schedule mutation yet. |
| gpt | 2 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Continue with conservative observation/preservation rather than speculative repair. |
| gpt | 3 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Preserve state and validate; do not repair without visible violation evidence. |
| gpt | 4 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Use a conservative audit-first recovery step and only apply a minimal local job-shop repair if di... |
| gpt | 5 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 1 | Do not commit a concrete repair from the visible information; reject irreversible action and pres... |
| gpt | 6 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 1 | Conservative diagnostic-first recovery: preserve all visible facts, reject unsupported repair, an... |
| gpt | 7 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Do not reject yet; preserve evidence and perform a fresh constraint/schedule validation checkpoin... |
| gpt | 8 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 1 | Insufficient visible state for a concrete job-shop repair; recommend observation-only rejection o... |
| gpt | 9 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Conservative no-op/observation step: preserve state, reject unsupported repairs, and wait for vis... |
| gpt | 10 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Continue conservatively; preserve all visible metadata and prior prompt-emission history; do not ... |
| deepseek_expert | 1 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Gather initial system state observation before acting |
| deepseek_expert | 2 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 3 | Immediate M2 repair with right-shift rescheduling prioritizing non-critical-path operations |
| deepseek_expert | 3 | True | flagged_admission | score_admitted_with_grounding_flags | eligible_for_official_realm_flagged_scoring | 6 | Run spindle health diagnostic on Machine-2 before committing to full production schedule |
| deepseek_expert | 4 | True | flagged_admission | score_admitted_with_grounding_flags | eligible_for_official_realm_flagged_scoring | 6 | Inspect M2, reroute its jobs, and preserve diagnostic data. |
| deepseek_expert | 5 | True | flagged_admission | score_admitted_with_grounding_flags | eligible_for_official_realm_flagged_scoring | 9 | Observe M2 reliability for 20 units, then apply Johnson's rule if stable; fall back to SPT dispat... |
| deepseek_expert | 6 | True | flagged_admission | score_admitted_with_grounding_flags | eligible_for_official_realm_flagged_scoring | 9 | Repair M2 immediately and reschedule downstream operations to mitigate breakdown impact on J3/J4. |
| deepseek_expert | 7 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Conduct full system state observation before intervening |
| deepseek_expert | 8 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Observe system state and prepare a conditional recovery plan for the most critical job in case of... |
| deepseek_expert | 9 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 14 | Apply targeted repair R to machine M2 based on observed intermittent failure signature, preservin... |
| deepseek_expert | 10 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 4 | Defer M2 repair; continue J4 with active monitoring and plan inspection after job end. |
| deepseek_instant | 1 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 16 | Conduct emergent maintenance on C1 based on sensor history, pause non-critical jobs, and restart ... |
| deepseek_instant | 2 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Observe current machine states and job queues; re-sequence only operations impacted by the breakd... |
| deepseek_instant | 3 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Halt and restart with enhanced CRT diagnostics to resolve invisible state uncertainty. |
| deepseek_instant | 4 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 3 | Reset schedule and re-sequence remaining operations with SPT rule and due-date priority. |
| deepseek_instant | 5 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Run a full resource-deadlock scan, then release the least critical blocked job to restore flow. |
| deepseek_instant | 6 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 0 | Pause and observe to fully characterize the breakdown before acting, reducing future missteps. |
| deepseek_instant | 7 | True | protective_rejection | score_rejection_as_protective_screening | eligible_for_official_realm_protective_rejection_scoring | 17 | Shift J4, op3 from M1 start t=8 to M1 start t=12, preserving other assignments and precedence. |
| deepseek_instant | 8 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 1 | Execute full maintenance release on all machines to counter potential CRT-stack-induced wear, sac... |
| deepseek_instant | 9 | True | flagged_admission | score_admitted_with_grounding_flags | eligible_for_official_realm_flagged_scoring | 6 | Insert one extra maintenance pause on M1 before the most congested period, and re-sequence the tw... |
| deepseek_instant | 10 | True | clean_admission | score_admitted_proposal | eligible_for_official_realm_admitted_scoring | 2 | Proceed with a state-gathering observation of machine loads and queues, focusing on bottleneck ma... |

## Interpretation

This report verifies that the Mnemosyne R86 handoff bundle can be consumed on the REALM-Bench side and converted into deterministic official-scorer-facing import cases.

The next step is to connect these imported cases to the actual Tier-6 scorer rather than only validating the handoff contract.
