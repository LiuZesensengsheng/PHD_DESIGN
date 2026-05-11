# Campaign Advisory Bundle V1

## Purpose

`campaign_advisory_bundle_v1` is a standalone report-only bundle that reads
campaign-layer advisory surfaces together:

- `campaign_power_curve_summary`
- `stress_resolve_summary`
- `campaign_experience_curve_summary`

It exists to surface cross-section review conflicts without promoting any one
surface into pass/fail authority.

## Authority Boundary

- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `hard_gate_impact`: `none`

The bundle must not:

- change campaign runtime, encounter tuning, or monster stats,
- create hard gates or pass/fail authority,
- change synthesis or default recommendation behavior,
- enable learned or reranker defaults,
- rewrite the semantics of the three upstream surfaces,
- claim registry or graph ownership on this branch.

## Output Shape

V1 reports:

- `present_sections`
- `missing_sections`
- `campaign_pressure_alignment`
- `recovery_alignment`
- `growth_alignment`
- `event_texture_alignment`
- `campaign_risk_flags`
- `review_conflicts`
- `advisory_summary_notes`
- `review_required`

Each alignment stays advisory and must preserve
`authority_boundary = advisory_context_only`.

## Conflict Rules

V1 specifically highlights:

- strong campaign power progress with weak experience texture,
- high stress carryover with weak or missing recovery,
- contradictory advisory mixes where surfaces disagree on recovery,
- missing sections as missing context, not silent zero-fill.
- coherent package/power context that still carries Act 2 transition shock or
  recovery-window collapse risk.

The bundle may consume partial inputs, but partial inputs must remain partial in
the output.

## Input Compatibility

The bundle accepts either:

- summary-shaped sections, or
- the current report payload shapes produced by
  `campaign_power_curve_report_v1`,
  `stress_resolve_model_v1`, and
  `campaign_experience_curve_v1`.

That compatibility is advisory only. The bundle does not import graph or
registry ownership from those surfaces.

## CLI

Write a template:

```powershell
python scripts/run_campaign_advisory_bundle.py --write-template tmp/campaign_advisory_bundle_template.json
```

Run fixtures:

```powershell
python scripts/run_campaign_advisory_bundle.py --input tests/fixtures/combat_analysis/campaign_advisory_bundle_v1/campaign_advisory_bundle_cases_v1.json --output-dir tmp/combat_analysis/campaign_advisory_bundle_v1
```

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_advisory_bundle_v1.py tests/scripts/test_run_campaign_advisory_bundle.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_power_curve_model_v1.py tests/scripts/test_run_campaign_power_curve_report.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_stress_resolve_model_v1.py tests/scripts/test_run_stress_resolve_model.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_experience_curve_v1.py tests/scripts/test_run_campaign_experience_curve.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```
