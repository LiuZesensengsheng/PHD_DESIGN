# Exam Iteration Generated Attempt Batch Run V1

## Purpose

`exam_iteration_generated_attempt_batch_run_v1` is a report-only orchestration
artifact for running a small ordered batch of already-generated or owner-supplied
`complete_card_draft_v1` attempts.

It answers:

```text
Given a draft handoff and multiple draft attempts, what changed across the
iteration loop, and what should the next prompt or handoff patch focus on?
```

## Workflow Position

```text
card_package_draft_handoff_v1
  + ordered complete_card_draft_v1 files
  -> exam_iteration_run_v1 per attempt
  -> exam_iteration_prompt_patch_proposal_v1 from the first attempt
  -> exam_iteration_batch_comparison_v1 across the ordered attempts
  -> exam_iteration_generated_attempt_batch_run_v1
```

## What It Writes

The CLI writes a top-level report, snapshot, and manifest plus nested artifacts:

- `handoff/` with `card_package_draft_handoff_v1`;
- `iterations/attempt_###/` with one `exam_iteration_run_v1` per draft;
- `prompt_patch/` with first-round `exam_iteration_prompt_patch_proposal_v1`;
- `batch_comparison/` with `exam_iteration_batch_comparison_v1`.

## Boundary

This surface is orchestration feedback only.

It does not:

- call an LLM API;
- generate complete card drafts;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change default synthesis behavior;
- enable learned or reranker behavior.

## Entrypoints

```powershell
python scripts/run_exam_iteration_generated_attempt_batch.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft <attempt_001_complete_card_draft_v1.json> --draft <attempt_002_complete_card_draft_v1.json> --axis-search <mechanism_axis_search_bundle_v1.json> --package-seed <card_package_proposal_v1.json> --output-dir tmp/combat_analysis/exam_iteration_generated_attempt_batch_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_generated_attempt_batch_run_v1.py tests/scripts/test_run_exam_iteration_generated_attempt_batch.py -q
```

Draft inputs are ordered. The first draft is treated as the baseline attempt for
the first-round prompt patch proposal; all drafts are compared by the batch
comparison layer.

## Interpretation

A final attempt that reaches `ready_for_human_review` is still only an advisory
exam signal. It shows the current loop can classify and compare attempts, not
that the design is balanced, reviewed, or ready for runtime promotion.
