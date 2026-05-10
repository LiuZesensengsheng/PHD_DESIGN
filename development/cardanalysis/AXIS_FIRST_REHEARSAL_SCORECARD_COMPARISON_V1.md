# Axis-First Rehearsal Scorecard Comparison V1

## Purpose

`axis_first_rehearsal_scorecard_comparison_v1` is a report-only comparison for
two supplied `complete_card_draft_v1` files that both start from the same
axis-first Silent context.

It answers:

```text
When a fresh owner/Codex-supplied draft enters the axis-first rehearsal path,
does the existing scorecard delta show improvement, regression, or an exam
visibility gap relative to the Silent fixture baseline?
```

## Workflow Position

```text
mechanism_axis_search_bundle_v1
  -> mechanism_axis_design_brief_v1
  -> card_package_proposal_v1 seed
  -> sts1_exam_target_v1
  -> card_package_variant_set_v1
  -> baseline complete_card_draft_v1
  -> latest complete_card_draft_v1
  -> axis_first_draft_writing_rehearsal_v1 for each draft
  -> autonomous_card_package_design_run_v1 for each draft
  -> card_design_scorecard_delta_report_v1
  -> axis_first_rehearsal_scorecard_comparison_v1
```

The surface is deliberately narrow. It rebuilds both rehearsals from supplied
files, compares their existing scorecards, and reports audit warnings when the
scorecard delta lacks a matched case pair.

## Current Silent Result

The first fresh Codex-supplied Silent attempt is:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/
  silent_axis_first_codex_poison_retain_shiv_attempt_v1.json
```

It validates as `complete_card_draft_v1`, remains `owner_supplied_draft` /
`review_needed`, and receives the same advisory score as the Silent fixture
baseline:

- baseline score: `92.78 strong`
- latest score: `92.78 strong`
- aggregate delta: `0.0`
- delta status: `stable_no_material_delta`

The important finding is not that the content improved. The comparison exposes
an exam-visibility gap: the two draft packages are different case ids, while the
underlying package-exam scorecard id is still seed-derived. The comparison now
reports `scorecard_delta_has_no_matched_case_pair` and recommends adding matched
attempt identity before claiming content improvement.

## Boundary

This surface does not:

- call an LLM API;
- generate complete-card draft text at runtime;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

The fresh Codex-supplied draft is unreviewed report-only material. It exists to
exercise the exam loop and reveal the next capability gap.

## Entrypoints

```powershell
python scripts/run_axis_first_rehearsal_scorecard_comparison.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --design-brief tests/fixtures/combat_analysis/mechanism_axis_package_seed_v1/silent_axis_design_brief_snapshot_v1.json --package-seed <card_package_proposal_v1.json> --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --baseline-draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --latest-draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_axis_first_codex_poison_retain_shiv_attempt_v1.json --output-dir tmp/combat_analysis/axis_first_rehearsal_scorecard_comparison_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_axis_first_rehearsal_scorecard_comparison_v1.py tests/scripts/test_run_axis_first_rehearsal_scorecard_comparison.py -q
```

Use `scripts/run_mechanism_axis_package_seed.py` to create the package seed from
the current design brief before running the comparison command.

## Interpretation

A clean comparison means the fresh supplied draft can be replayed through the
axis-first exam loop and compared against the fixture baseline. It does not prove
autonomous card-design quality, balance, reviewed evidence status, or promotion
readiness.

The next capability gap is better comparison identity: scorecard/delta should be
able to compare repeated attempts as matched attempt pairs, not only as distinct
draft package case ids.
