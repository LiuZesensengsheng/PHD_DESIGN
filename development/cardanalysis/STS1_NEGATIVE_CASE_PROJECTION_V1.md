# STS1 Negative Case Projection V1

## Purpose

`sts1_negative_case_projection_v1` is a deterministic report-only projection
over the first STS1 negative case pack.

It answers:

```text
Which risk features and exam-calibration dimensions do the first-round STS1
negative cases support, and which adjacent labels must remain human-review
context only?
```

## Scope

V1 consumes the 16 generated `cardanalysis_case_input_v1` cases from
`sts1_negative_case_pack_v1` and reuses the generic
`cardanalysis_feature_projection_v1` payload for per-case feature buckets.

It then adds STS1-specific readouts for:

- risk feature families;
- current calibration-dimension support;
- label-only features that cannot enter the scorecard yet;
- a report-only next review queue.

This deepens the first case round. It does not add a second case pack and does
not start the control-candidate case line.

## Current Calibration Support

The projection keeps the two current STS1 calibration dimensions visible:

- `primary_axis_dominance`
- `early_floor_late_ceiling_balance`

Direct support means a case explicitly names the dimension in
`contexts.deck_or_package.expected_scorecard_dimensions`.

Risk-family context means a case's failure families map to the dimension even
when the case was authored with a more adjacent label.

Both forms are advisory. Neither changes scorecard weights, exam outcomes, or
hard gates.

## Label-Only Features

V1 keeps these adjacent labels visible but explicitly non-authoritative:

- `secondary_axis_containment`
- `character_texture_fit`
- `numeric_band_grounding`
- `fail_state_floor_specificity`
- `package_role_structure`
- `decision_surface_preservation`
- `sts1_text_compactness`
- `fun_tension`
- `strength_risk_control`

These labels can guide later human review and fixture selection. They cannot
be treated as reviewed scorecard dimensions without a separate review-backed PR.

## Boundary

V1 does not:

- generate formal card text;
- write runtime card data;
- modify official card data;
- create hard gates;
- change scorecard dimensions or weights;
- change exam outcomes;
- claim reviewed evidence;
- enable default synthesis;
- call an LLM/API;
- enable learned or reranker behavior;
- create a second-round case pack;
- create the control candidate case pack line.

The projection is advisory context only. Human review still owns fun judgment,
archetype identity, character texture acceptance, numeric bands, evidence
promotion, and runtime or formal-card promotion.

## Output Shape

Required top-level fields:

- `contract_version`: `sts1_negative_case_projection_v1`
- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `projection_scope`
- `hard_gate_impact`: `none`
- `score_weight_impact`: `none`
- `projection_id`
- `source_case_pack_ref`
- `source_calibration_ref`
- `source_feature_projection_contract`
- `case_count`
- `feature_family_summary`
- `calibration_dimension_support`
- `label_only_feature_notes`
- `per_case_projections`
- `recommended_next_review_queue`
- `exam_blind_spot_notes`
- `human_judgment_still_required_for`
- `boundary_assertions`

## Entrypoint

```powershell
python scripts/run_sts1_negative_case_projection.py --input tests/fixtures/combat_analysis/sts1_negative_case_pack_v1/sts1_negative_case_pack_v1_cases.json --calibration tests/fixtures/combat_analysis/sts1_exam_capability_calibration_v1/sts1_exam_capability_calibration_v1_snapshot.json --case-pack-snapshot tests/fixtures/combat_analysis/sts1_negative_case_pack_v1/sts1_negative_case_pack_v1_snapshot.json --output-dir tmp/combat_analysis/sts1_negative_case_projection_current
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_negative_case_projection_v1.py tests/scripts/test_run_sts1_negative_case_projection.py -q
```

## Fixture

The first fixture output lives under:

```text
tests/fixtures/combat_analysis/sts1_negative_case_projection_v1/
```

It includes:

- `sts1_negative_case_projection_v1_snapshot.json`
- `sts1_negative_case_projection_v1_report.md`
- `sts1_negative_case_projection_v1_manifest.json`

## Intended Follow-Up

Good next report-only work:

- compare this projection against current STS1 exam feedback blind spots;
- select a small human-review queue from high-priority projected cases;
- decide later, with human review, which label-only features deserve reviewed
  examples.

Do not use this projection to promote cards, reject packages, alter scores, or
claim reviewed evidence.
