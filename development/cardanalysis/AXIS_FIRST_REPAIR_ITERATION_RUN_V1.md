# Axis-First Repair Iteration Run V1

## Purpose

`axis_first_repair_iteration_run_v1` is a report-only closure surface for one
Silent axis-first repair iteration.

It answers:

```text
Given the current exam repair advice, what revised draft attempt was tried,
how did it re-enter the existing exam chain, did score or visibility move, and
what failure families still remain?
```

## Workflow Position

```text
axis_first_integrated_exam_summary_v1
  + axis_first_rehearsal_scorecard_comparison_v1
  + baseline/latest complete_card_draft_v1
  + unreviewed revised complete_card_draft_v1
  -> rebuilt axis_first_rehearsal_scorecard_comparison_v1 re-exams
  -> axis_first_repair_iteration_run_v1
```

The V1 runner starts with the current Silent fixture lane:

- baseline: `silent_poison_retain_shiv_exam_draft_v1`;
- previous latest: `silent_axis_first_codex_poison_retain_shiv_attempt_v1`;
- revised attempt: `silent_axis_first_codex_poison_retain_shiv_revised_attempt_v1`.

It rebuilds three comparisons:

- baseline -> previous latest;
- baseline -> revised;
- previous latest -> revised.

The revised draft is owner/Codex-supplied, unreviewed, and advisory only. It is
not generated at runtime, not reviewed evidence, not runtime card data, and not
a formal card promotion.

## Readouts

The run reports:

- selected repair priorities from integrated `repair_advice`;
- repair rationale and draft revision constraints;
- unreviewed revised draft attempt metadata;
- re-exam result references;
- scorecard delta summary;
- scorecard visibility and lane-quality reason deltas;
- campaign timing draft-signal proxy deltas;
- remaining failure families.

Selected repair priorities are read through the shared
`axis_first_repair_advice_read_model` helper. The helper preserves the existing
payload shape: role-specific advice is selected first, same-lane repair lanes
are matched against the previous comparison's lane-quality reasons, and campaign
timing context is appended only as report-only planning guidance when available.

For the current Silent fixture, aggregate score remains static while the revised
attempt reduces the selected visibility reasons for `axis_precision_loss`,
`sts1_wording_drift`, and `fail_state_floor_drop`. The remaining gaps are still
`lane_review_sensitivity`, `score_static_after_revised_attempt`, and real
campaign curve re-exam coverage.

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

The run is a planning/audit surface only. It consumes existing report-only
outputs and records one unreviewed revised attempt.

## Entrypoints

```powershell
python scripts/run_axis_first_repair_iteration_run.py --use-current-silent-fixtures --output-dir tmp/combat_analysis/axis_first_repair_iteration_run_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_axis_first_repair_iteration_run_v1.py tests/scripts/test_run_axis_first_repair_iteration_run.py -q
```

Explicit inputs can also be supplied:

```powershell
python scripts/run_axis_first_repair_iteration_run.py --integrated-summary <axis_first_integrated_exam_summary_v1_snapshot.json> --axis-search <mechanism_axis_search_bundle_v1.json> --design-brief <mechanism_axis_design_brief_v1.json> --package-seed <card_package_proposal_v1.json> --target <sts1_exam_target_v1.json> --variant-set <card_package_variant_set_v1.json> --baseline-draft <complete_card_draft_v1.json> --latest-draft <complete_card_draft_v1.json> --revised-draft <complete_card_draft_v1.json> --output-dir tmp/combat_analysis/axis_first_repair_iteration_run_current
```

## Interpretation

A clean repair iteration run means the advisory loop can move from repair advice
to a supplied revised draft attempt and back through the existing exam chain. It
does not prove card quality, balance, reviewed status, or promotion readiness.
