from __future__ import annotations

import json

from analysis.realm_tier6 import expanded_live_llm_pilot_plan as module


def sample_r88_report() -> dict:
    sequences = module.generator.generate_development_sequences(
        module.REPO_ROOT,
        max_families=1,
    )
    non_control = [
        sequence for sequence in sequences if not sequence["is_control_sequence"]
    ][0]
    return {
        "sequence_id": non_control["sequence_id"],
        "config_id": "E7",
        "condition_label": "full_crt_stack",
    }


def test_select_one_non_control_sequence_per_family() -> None:
    sequences = module.generator.generate_development_sequences(
        module.REPO_ROOT,
        max_families=3,
    )
    selected = module.select_one_non_control_sequence_per_family(
        sequences,
        target_families=module.TARGET_FAMILIES,
    )

    assert set(selected) == set(module.TARGET_FAMILIES)
    assert all(not sequence["is_control_sequence"] for sequence in selected.values())


def test_build_collection_matrix_counts_existing_and_planned(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=3,
        r88_score_report_path=r88_path,
        proposer_packs=module.DEFAULT_PROPOSER_PACKS,
        configs=["E7"],
    )

    summary = report["matrix_summary"]

    assert summary["total_cases"] == 120
    assert summary["existing_r88_collected"] == 40
    assert summary["planned_not_collected"] == 80
    assert report["chapter6_status"]["bounded_pilot_ready"] is True
    assert report["chapter6_status"]["family_generalized_live_llm_ready"] is False


def test_missing_r88_means_all_cases_planned(tmp_path) -> None:
    report = module.build_report(
        max_families=3,
        r88_score_report_path=tmp_path / "missing.json",
        proposer_packs=module.DEFAULT_PROPOSER_PACKS,
        configs=["E7"],
    )

    summary = report["matrix_summary"]

    assert summary["total_cases"] == 120
    assert summary["existing_r88_collected"] == 0
    assert summary["planned_not_collected"] == 120


def test_render_markdown_contains_claim_boundary(tmp_path) -> None:
    r88_path = tmp_path / "r88.json"
    r88_path.write_text(json.dumps(sample_r88_report()), encoding="utf-8")

    report = module.build_report(
        max_families=3,
        r88_score_report_path=r88_path,
        proposer_packs=module.DEFAULT_PROPOSER_PACKS,
        configs=["E7"],
    )
    markdown = module.render_markdown(report)

    assert "Expanded Live-LLM Pilot Plan" in markdown
    assert "Family-generalized live-LLM ready" in markdown
    assert "bounded pilot evidence" in markdown
    assert "not family-generalized evidence" in markdown
