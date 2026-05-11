# Axis-First Integrated Exam Summary V1

## Purpose

`axis_first_integrated_exam_summary_v1` is a report-only integration view for the
current STS1 axis-first exam loop.

It answers:

```text
Across the four STS1 axis-first rehearsal comparisons, what can the exam see,
where is score movement still blind to content movement, and what case/campaign
context should guide the next capability slice?
```

## Workflow Position

```text
axis_first_rehearsal_scorecard_comparison_v1 snapshots
  + optional cardanalysis_feature_projection_v1 payloads
  + optional card_package_exam_v1 campaign-curve context
  -> axis_first_integrated_exam_summary_v1
```

The current default CLI can rebuild the four-character fixture comparisons from:

- Silent poison + retain + shiv;
- Ironclad exhaust + block engine + strength scaling;
- Defect orb control + frost control + focus scaling;
- Watcher stance/mantra + retain + scry control.

It then attaches advisory case-projection samples and the campaign curve-fit
fixture manifest/validation report so one report can show card-lane visibility,
case visibility, and campaign phase warnings together.

## Readouts

The summary reports:

- axis-first role coverage and ready-role count;
- per-character baseline/latest score, same-lane status, and sensitivity status;
- scorecard visibility patch lane counts and affected dimensions;
- lane quality reason counts across same-score/same-lane comparisons;
- case-projection source status and exam-sensitivity projection samples;
- campaign curve risk tags, online timing labels, and phase failure reasons;
- one advisory next capability gap.

In the current four-character fixture run, all four roles can produce a
same-lane axis-first comparison with dimension visibility notes. The recurring
gap remains `lane_review_sensitivity`: same-lane card content changes are visible
in notes, aggregate scores remain static, and the summary now shows which
advisory quality reasons recur most often. The current quality reason families
are `axis_precision_loss`, `generic_goodstuff_drift`, `fail_state_floor_drop`,
`setup_tax_increase`, and `sts1_wording_drift`.

## Boundary

This surface does not:

- call an LLM API;
- generate complete-card draft text at runtime;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change scorecard weights;
- change `card_package_exam_v1` outcomes;
- change campaign runtime behavior;
- enable default synthesis, learned behavior, or reranker behavior.

The integrated summary is a planning/audit surface only. It aggregates existing
report-only outputs and does not replace their canonical ownership.

## Entrypoints

```powershell
python scripts/run_axis_first_integrated_exam_summary.py --use-current-fixtures --output-dir tmp/combat_analysis/axis_first_integrated_exam_summary_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_axis_first_integrated_exam_summary_v1.py tests/scripts/test_run_axis_first_integrated_exam_summary.py -q
```

Explicit snapshots can also be supplied:

```powershell
python scripts/run_axis_first_integrated_exam_summary.py --axis-first-comparison <axis_first_rehearsal_scorecard_comparison_v1_snapshot.json> --case-projection <feature_projection_or_sample_pack.json> --campaign-curve-fit <card_package_exam_or_curve_context.json> --output-dir tmp/combat_analysis/axis_first_integrated_exam_summary_current
```

## Interpretation

A clean integrated summary means the current exam outputs can be read together
across role coverage, scorecard visibility, case projection, and campaign timing.
It does not prove autonomous card-design quality, balance, reviewed evidence
status, or card-promotion readiness.

