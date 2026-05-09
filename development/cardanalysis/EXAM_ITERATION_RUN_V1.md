# Exam Iteration Run V1

## Purpose

`exam_iteration_run_v1` is the first report-only record for one self-improving
card-package exam loop.

It answers:

```text
What happened in this attempt, and what should change in the next attempt?
```

## Workflow Position

```text
card_package_draft_handoff_v1
  -> llm_complete_card_draft_attempt_v1
  -> card_draft_failure_taxonomy_v1
  -> card_package_exam_v1
  -> exam_iteration_run_v1
```

## What It Contains

Each iteration run records:

- attempt status;
- failure counts and patch lanes;
- whether package exam was run;
- package-exam outcome, axis alignment, and health labels when available;
- recommended next focus, such as `human_review`, `patch_attempt:<lane>`, or
  `patch_package_exam_findings`.

## Boundary

This surface is advisory context only.

It does not:

- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change default synthesis behavior;
- enable learned or reranker behavior.

## Entrypoints

```powershell
python scripts/run_exam_iteration_run.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --axis-search <mechanism_axis_search_bundle_v1.json> --package-seed <card_package_proposal_v1.json> --output-dir tmp/combat_analysis/exam_iteration_run_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_run_v1.py tests/scripts/test_run_exam_iteration_run.py -q
```

## Negative Controls

The iteration-run tests read
`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_negative_attempt_drafts_v1.json`
to prove that invalid attempts stop before package exam while warning-only
attempts may still run package exam with patch lanes recorded for the next
attempt. These records remain advisory feedback only.

## Interpretation

An iteration run is the unit of learning for the autonomous draft loop. The next
step is to run repeated generated attempts and compare whether recurring failure
types decline.
