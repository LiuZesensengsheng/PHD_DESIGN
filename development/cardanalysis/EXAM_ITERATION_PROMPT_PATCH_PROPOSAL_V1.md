# Exam Iteration Prompt Patch Proposal V1

## Purpose

`exam_iteration_prompt_patch_proposal_v1` is a report-only feedback artifact for
the STS1 autonomous draft loop.

It answers:

```text
Across one or more iteration runs, which prompt or handoff instructions should
change before the next generated complete-card draft attempt?
```

## Workflow Position

```text
card_package_draft_handoff_v1
  -> llm_complete_card_draft_attempt_v1
  -> card_draft_failure_taxonomy_v1
  -> card_package_exam_v1
  -> exam_iteration_run_v1
  -> exam_iteration_prompt_patch_proposal_v1
  -> exam_iteration_batch_comparison_v1
```

## What It Contains

Each proposal records:

- source `exam_iteration_run_v1` ids;
- iteration status counts;
- observed failure counts by taxonomy type;
- patch lane counts;
- whether package exam feedback was available;
- recommended prompt patch text per lane;
- recommended handoff patch text per lane;
- evidence back to source iteration ids;
- next attempt focus.

## Boundary

This surface is advisory prompt and handoff patch advice only.

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
python scripts/run_exam_iteration_prompt_patch_proposal.py --input tmp/combat_analysis/exam_iteration_run_current/exam_iteration_run_v1_snapshot.json --output-dir tmp/combat_analysis/exam_iteration_prompt_patch_proposal_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_prompt_patch_proposal_v1.py tests/scripts/test_run_exam_iteration_prompt_patch_proposal.py -q
```

The CLI accepts repeated `--input` paths or `--input-dir` directories containing
`*_snapshot.json` files. It only consumes `exam_iteration_run_v1` snapshots.

## Interpretation

A proposal is useful when repeated generated attempts share the same failure
lanes. It should be used to tighten the next `card_package_draft_handoff_v1` or
LLM prompt before another generated attempt is recorded.

It is not evidence that design quality improved. Improvement still requires new
attempts, validation, package exam feedback, batch comparison, and human review
before promotion.
