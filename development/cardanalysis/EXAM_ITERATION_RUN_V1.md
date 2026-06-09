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
  -> exam_iteration_prompt_patch_proposal_v1
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

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_run_v1.py -q
```

The standalone CLI wrapper has been retired. The retained library and toolkit
tests still validate ready attempts, invalid attempts, four-character negative
controls, report payloads, snapshot payloads, and downstream advisory boundary
assertions.

## Negative Controls

The iteration-run tests read
`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_negative_attempt_drafts_v1.json`
to prove that invalid attempts stop before package exam while warning-only
attempts may still run package exam with patch lanes recorded for the next
attempt. These records remain advisory feedback only.

## Interpretation

An iteration run is the unit of learning for the autonomous draft loop. The next
consumer is `exam_iteration_prompt_patch_proposal_v1`, which compares one or
more runs and recommends prompt or handoff patches for the next generated
attempt. The improvement claim still requires repeated generated attempts and
evidence that recurring failure types decline.

When an iteration run is part of an axis-first package-design rehearsal, wrap it
with `autonomous_card_package_design_run_v1` so the attempt remains tied to the
mechanism-axis search, constrained design brief, package seed, selected variant,
package exam, and scorecard context.
