# R89 Mnemosyne Live-LLM Chapter 6 Evidence Package

## Claim Boundary

R89 consolidates deterministic Mnemosyne and REALM-Bench pilot reports for AGI V3 Chapter 6. It supports an implementation and pilot-results narrative. It is not confirmatory-scale evidence.

## Chapter 6 Readiness

- Ready for Chapter 6 pilot table: `True`
- Ready for confirmatory claims: `False`
- Recommended section: Chapter 6 implementation evidence and pilot scoring results

## Overall R88 Scoring Summary

| Metric | Value |
|---|---:|
| official_scorer_invoked | True |
| num_events | 40 |
| safety_passed | True |
| repeated_failure_rate | 0.0 |
| horizon_reward_mean | 0.90125 |
| grounded_admission_rate | 0.725 |
| time_to_correction_observed_count | 0 |
| time_to_correction_censored_count | 40 |
| invalid_commit_count | 0 |
| evidence_destroying_repair_count | 0 |
| orphaned_dependent_count | 0 |

## Chapter 6 Pilot Results Table

| Model pack | Events | Safety | RFR | Horizon reward | Grounded admission | Invalid commits |
|---|---:|---|---:|---:|---:|---:|
| Claude | 10 | True | 0.0 | 1.0 | 1.0 | 0 |
| DeepSeek expert | 10 | True | 0.0 | 0.855 | 0.5 | 0 |
| DeepSeek instant | 10 | True | 0.0 | 0.885 | 0.7 | 0 |
| GPT | 10 | True | 0.0 | 0.865 | 0.7 | 0 |

## Pipeline Evidence

### R83.5a: manual_live_llm_pilot

- Available: `True`

```json
{
  "packs": [
    "claude",
    "deepseek_expert",
    "deepseek_instant",
    "gpt"
  ],
  "source": "R83.5a",
  "status": "manual public-prompt response packs collected"
}
```

### R83.5b: comparison_import

- Available: `True`

```json
{
  "schema": "realm_tier6_live_llm_kernel_import_report_v0"
}
```

### R83.5c: kernel_trace

- Available: `True`

```json
{
  "kernel_method_counts": {
    "accept_via_kernel": 29,
    "accept_via_kernel_with_flags": 5,
    "reject_before_commit": 6
  },
  "num_admitted": 34,
  "num_records": 40,
  "num_rejected": 6,
  "schema": "realm_tier6_live_llm_kernel_trace_report_v0"
}
```

### R84: runtime_evaluator

- Available: `True`

```json
{
  "global_passed": true,
  "num_failed": 0,
  "num_records": 40,
  "schema": "realm_tier6_live_llm_runtime_evaluator_report_v0"
}
```

### R85: score_bridge

- Available: `True`

```json
{
  "num_records": 40,
  "official_realm_score": false,
  "pack_summary": [
    {
      "admission_adjusted_utility_proxy": 0.7457,
      "admission_rate": 1.0,
      "clean_admission_rate": 1.0,
      "flagged_admission_rate": 0.0,
      "num_admitted": 10,
      "num_clean_admissions": 10,
      "num_failed_runtime_checks": 0,
      "num_flagged_admissions": 0,
      "num_high_unsupported_specificity": 0,
      "num_moderate_unsupported_specificity": 0,
      "num_passed_runtime_checks": 10,
      "num_protective_rejections": 0,
      "num_records": 10,
      "num_rejected": 0,
      "num_unsafe_admissions": 0,
      "pack_name": "claude",
      "policy_counts": {
        "mixed": 10
      },
      "protective_rejection_rate": 0.0,
      "realm_score_bridge": {
        "grounded_admission_rate": 1.0,
        "official_realm_score": false,
        "post_admission_availability_rate": 1.0,
        "protective_screening_rate": 0.0,
        "safety_passed": true,
        "score_type": "deterministic_proxy",
        "unsupported_specificity_pressure": 1.1
      },
      "rejection_rate": 0.0,
      "unsafe_admission_rate": 0.0,
      "unsupported_specificity_mean": 1.1,
      "unsupported_specificity_total": 11
    },
    {
      "admission_adjusted_utility_proxy": 0.5816,
      "admission_rate": 0.7,
      "clean_admission_rate": 0.7,
      "flagged_admission_rate": 0.0,
      "num_admitted": 7,
      "num_clean_admissions": 7,
      "num_failed_runtime_checks": 0,
      "num_flagged_admissions": 0,
      "num_high_unsupported_specificity": 0,
      "num_moderate_unsupported_specificity": 0,
      "num_passed_runtime_checks": 10,
      "num_protective_rejections": 3,
      "num_records": 10,
      "num_rejected": 3,
      "num_unsafe_admissions": 0,
      "pack_name": "gpt",
      "policy_counts": {
        "observation_first": 10
      },
      "protective_rejection_rate": 0.3,
      "realm_score_bridge": {
        "grounded_admission_rate": 0.7,
        "official_realm_score": false,
        "post_admission_availability_rate": 0.7,
        "protective_screening_rate": 0.3,
        "safety_passed": true,
        "score_type": "deterministic_proxy",
        "unsupported_specificity_pressure": 1.0
      },
      "rejection_rate": 0.3,
      "unsafe_admission_rate": 0.0,
      "unsupported_specificity_mean": 1.0,
      "unsupported_specificity_total": 10
    },
    {
      "admission_adjusted_utility_proxy": 0.6096,
      "admission_rate": 0.9,
      "clean_admission_rate": 0.5,
      "flagged_admission_rate": 0.4,
      "num_admitted": 9,
      "num_clean_admissions": 5,
      "num_failed_runtime_checks": 0,
      "num_flagged_admissions": 4,
      "num_high_unsupported_specificity": 1,
      "num_moderate_unsupported_specificity": 4,
      "num_passed_runtime_checks": 10,
      "num_protective_rejections": 1,
      "num_records": 10,
      "num_rejected": 1,
      "num_unsafe_admissions": 0,
      "pack_name": "deepseek_expert",
      "policy_counts": {
        "active_repair": 1,
        "mixed": 6,
        "observation_first": 3
      },
      "protective_rejection_rate": 0.1,
      "realm_score_bridge": {
        "grounded_admission_rate": 0.5,
        "official_realm_score": false,
        "post_admission_availability_rate": 0.9,
        "protective_screening_rate": 0.1,
        "safety_passed": true,
        "score_type": "deterministic_proxy",
        "unsupported_specificity_pressure": 5.2
      },
      "rejection_rate": 0.1,
      "unsafe_admission_rate": 0.0,
      "unsupported_specificity_mean": 5.2,
      "unsupported_specificity_total": 52
    },
    {
      "admission_adjusted_utility_proxy": 0.681,
      "admission_rate": 0.8,
      "clean_admission_rate": 0.7,
      "flagged_admission_rate": 0.1,
      "num_admitted": 8,
      "num_clean_admissions": 7,
      "num_failed_runtime_checks": 0,
      "num_flagged_admissions": 1,
      "num_high_unsupported_specificity": 2,
      "num_moderate_unsupported_specificity": 1,
      "num_passed_runtime_checks": 10,
      "num_protective_rejections": 2,
      "num_records": 10,
      "num_rejected": 2,
      "num_unsafe_admissions": 0,
      "pack_name": "deepseek_instant",
      "policy_counts": {
        "active_repair": 2,
        "mixed": 7,
        "observation_first": 1
      },
      "protective_rejection_rate": 0.2,
      "realm_score_bridge": {
        "grounded_admission_rate": 0.7,
        "official_realm_score": false,
        "post_admission_availability_rate": 0.8,
        "protective_screening_rate": 0.2,
        "safety_passed": true,
        "score_type": "deterministic_proxy",
        "unsupported_specificity_pressure": 4.6
      },
      "rejection_rate": 0.2,
      "unsafe_admission_rate": 0.0,
      "unsupported_specificity_mean": 4.6,
      "unsupported_specificity_total": 46
    }
  ],
  "schema": "realm_tier6_live_llm_realm_score_bridge_report_v0"
}
```

### R86: scorer_handoff

- Available: `True`

```json
{
  "config_id": "E7",
  "num_cases": 40,
  "schema": "realm_tier6_live_llm_realm_scorer_handoff_bundle_v0",
  "sequence_id": "T6-7e17ef0cc5f3"
}
```

### R87: realm_import

- Available: `True`

```json
{
  "all_cases_valid": true,
  "num_cases": 40,
  "num_validation_failed": 0,
  "num_validation_passed": 40,
  "schema": "realm_tier6_mnemosyne_live_llm_import_report_v0"
}
```

### R88: realm_scoring

- Available: `True`

```json
{
  "bracket": {
    "B0_memoryless_replay": {
      "horizon_reward": 0.0,
      "repeated_failure_rate": 1.0
    },
    "Bstar_oracle_memory": {
      "horizon_reward": 1.0,
      "repeated_failure_rate": 0.0
    },
    "baseline_version": "tier6-baselines-v0",
    "position_horizon_reward": 0.90125,
    "position_repeated_failure_rate": 1.0
  },
  "condition_label": "full_crt_stack",
  "config_id": "E7",
  "evidence_destroying_repair_count": 0,
  "grounded_admission_rate": 0.725,
  "horizon_reward_mean": 0.90125,
  "invalid_commit_count": 0,
  "num_events": 40,
  "official_scorer_invoked": true,
  "orphaned_dependent_count": 0,
  "repeated_failure_rate": 0.0,
  "safety_passed": true,
  "score_scope": "mnemosyne_live_llm_handoff_derived_events",
  "sequence_id": "T6-7e17ef0cc5f3",
  "time_to_correction_censored_count": 40,
  "time_to_correction_observed_count": 0
}
```

## Allowed Claims

- Mnemosyne live-LLM handoff cases can be imported by REALM-Bench.
- The public REALM Tier-6 scorer can be invoked on schema-valid Mnemosyne handoff-derived events.
- In the one-sequence E7 pilot, the scoring integration produced safety-passed output.
- The pilot produced a horizon reward mean and grounded admission rate suitable for reporting as pilot evidence.

## Disallowed Claims

- final confirmatory Chapter 6 evidence
- general AGI achievement
- wisdom or autonomous scientific reasoning
- API-automated live LLM behavior
- production CTL-domain StateView realization
- full benchmark-scale statistical conclusion

## Chapter 6 Insert Draft

In the Tier-6 live-LLM pilot, Mnemosyne response packs were passed through a deterministic admission, kernel-trace, runtime-evaluation, scorer-handoff, and REALM-Bench import pipeline. The resulting schema-valid events were then scored by the public REALM Tier-6 scorer. Over 40 handoff-derived events in the E7 pilot sequence, the scorer integration reported safety passed = `True`, horizon reward mean = `0.90125`, and grounded admission rate = `0.725`. These results establish pilot integration evidence, not confirmatory-scale evidence.
