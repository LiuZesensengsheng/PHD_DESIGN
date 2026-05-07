# Campaign Experience Curve V1

## Purpose

`campaign_experience_curve_v1` is a report-only design model for campaign feel.
It complements `campaign_power_curve_report_v1` by reviewing experience shape:
fun pressure, release, recovery, growth payoff, event surprise, fatigue, pivots,
and player agency.

It is not campaign runtime implementation and does not tune encounters or
monster numbers.

## Authority Boundary

- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `hard_gate_impact`: `none`

The model must not:

- modify campaign runtime,
- modify BBS runtime,
- connect to `cardanalysis_evidence_bundle`,
- change synthesis or default recommendation behavior,
- create hard gates,
- enable learned or reranker defaults,
- redefine `campaign_power_curve_report_v1` semantics.

## Dimensions

V1 reports these dimensions:

- `pressure_arc`: how pressure accumulates and releases.
- `recovery_windows`: whether relief windows and their costs are clear.
- `growth_payoff`: whether campaign growth is felt by the player.
- `event_texture`: surprise, risk, and narrative flavor.
- `fatigue_risk`: repetition and too-long pressure.
- `pivot_moments`: visible campaign turning points.
- `agency_windows`: route, resource, and combat choice windows.
- `stress_resolve_relation`: advisory relationship to
  `stress_resolve_model_v1`.
- `power_curve_relation`: advisory relationship to
  `campaign_power_curve_report_v1`.

## Advisory Relations

The model may read concepts from `stress_resolve_model_v1` and
`campaign_power_curve_report_v1` only as advisory context. It must not import or
rewrite their implementation, register graph edges, or require their outputs.

Expected future MasterAgent graph shape:

- capability node: `campaign_experience_curve_v1`
- provided artifact: `campaign_experience_curve_summary`
- optional consumes: `stress_resolve_summary`,
  `campaign_power_curve_summary`, `normalized_design_case`,
  `feature_projection_payload`
- review-gated with: `stress_resolve_model_v1`,
  `campaign_power_curve_report_v1`, and possibly
  `evaluation_autonomous_design_model_v1`

## CLI

Write a template:

```powershell
python scripts/run_campaign_experience_curve.py --write-template tmp/campaign_experience_curve_template.json
```

Run fixtures:

```powershell
python scripts/run_campaign_experience_curve.py --input tests/fixtures/combat_analysis/campaign_experience_curve_v1/campaign_experience_curve_cases_v1.json --output-dir tmp/combat_analysis/campaign_experience_curve_v1
```

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_experience_curve_v1.py tests/scripts/test_run_campaign_experience_curve.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_stress_resolve_model_v1.py tests/scripts/test_run_stress_resolve_model.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_power_curve_model_v1.py tests/scripts/test_run_campaign_power_curve_report.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```
