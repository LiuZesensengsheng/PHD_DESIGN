# STS1 Negative Case Pack V1

## Purpose

`sts1_negative_case_pack_v1` is a deterministic report-only case expansion for
the STS1 card-package exam line.

It answers:

```text
Which unreviewed negative and boundary cases should the STS1 exam preserve
before any future human review or scorecard change?
```

## Scope

V1 deepens the first negative-case round only. It does not start the later
control-candidate case line.

The first pack contains 16 normalized `cardanalysis_case_input_v1` cases:

- four Silent cases;
- four Ironclad cases;
- four Defect cases;
- four Watcher cases.

Every case is a generated hypothesis with:

- `evidence_tier = speculative`;
- `review_status = hypothesis_draft`;
- `authority_boundary = advisory_context_only`;
- `case_status = generated_unreviewed_report_only_case`.

## Failure Families

The V1 coverage matrix includes:

- `primary_axis_drift`
- `secondary_axis_swallows_primary`
- `generic_goodstuff_drift`
- `early_weak_late_explosion`
- `numeric_fantasy`
- `weak_fail_state`
- `character_texture_mismatch`
- `anti_combo_role_collision`

The pack intentionally supports the two current STS1 calibration dimensions:

- `primary_axis_dominance`
- `early_floor_late_ceiling_balance`

It also records adjacent future-review dimensions such as character texture,
numeric grounding, fail-state specificity, and role collision without changing
scorecard weights.

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
- create the control candidate case pack line.

The cases are advisory material for exam preparation. Human review still owns
fun judgment, archetype identity, numeric bands, which warnings should become
exam expectations, reviewed evidence promotion, and any runtime or formal-card
promotion.

## Output Shape

Required top-level fields:

- `contract_version`: `sts1_negative_case_pack_v1`
- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `case_pack_scope`
- `hard_gate_impact`
- `score_weight_impact`
- `pack_id`
- `source_input_ref`
- `source_case_schema_version`
- `source_calibration_ref`
- `case_count`
- `coverage_summary`
- `per_case_readouts`
- `next_report_only_automation_tasks`
- `human_judgment_still_required_for`
- `boundary_assertions`

## Entrypoint

```powershell
python scripts/run_sts1_negative_case_pack.py --input tests/fixtures/combat_analysis/sts1_negative_case_pack_v1/sts1_negative_case_pack_v1_cases.json --calibration tests/fixtures/combat_analysis/sts1_exam_capability_calibration_v1/sts1_exam_capability_calibration_v1_snapshot.json --output-dir tmp/combat_analysis/sts1_negative_case_pack_current
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_negative_case_pack_v1.py tests/scripts/test_run_sts1_negative_case_pack.py -q
```

## Fixture

The first fixture lives under:

```text
tests/fixtures/combat_analysis/sts1_negative_case_pack_v1/
```

It includes:

- `sts1_negative_case_pack_v1_cases.json`
- `sts1_negative_case_pack_v1_snapshot.json`
- `sts1_negative_case_pack_v1_report.md`
- `sts1_negative_case_pack_v1_manifest.json`

## Intended Follow-Up

Good next report-only work:

- project these cases into feature-projection samples;
- compare this case family depth against STS1 exam and calibration readouts;
- prepare an unattended review queue that uses the cases as unreviewed context.

Do not use this pack to promote cards, reject packages, or claim reviewed
evidence.
