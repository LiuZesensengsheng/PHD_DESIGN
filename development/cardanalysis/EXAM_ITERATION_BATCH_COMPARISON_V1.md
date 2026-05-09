# Exam Iteration Batch Comparison V1

## Purpose

`exam_iteration_batch_comparison_v1` is a report-only artifact for comparing a
small ordered batch of generated draft attempts.

It answers:

```text
Across repeated exam iteration runs, which failure families look resolved,
persistent, or newly observed?
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

Each comparison records:

- ordered source `exam_iteration_run_v1` ids;
- optional prompt-patch proposal summary;
- first and final observed failure families;
- resolved, persistent, and newly observed failure families;
- resolved, persistent, and newly observed patch lanes;
- per-failure and per-lane timelines by attempt index;
- package-exam feedback availability;
- an advisory readout for the next iteration.

## Boundary

This surface is comparison feedback only.

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
python scripts/run_exam_iteration_batch_comparison.py --input <attempt_001_exam_iteration_run_snapshot.json> --input <attempt_002_exam_iteration_run_snapshot.json> --prompt-patch <exam_iteration_prompt_patch_proposal_v1_snapshot.json> --output-dir tmp/combat_analysis/exam_iteration_batch_comparison_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_batch_comparison_v1.py tests/scripts/test_run_exam_iteration_batch_comparison.py -q
```

Inputs are ordered. The first `--input` is treated as the baseline attempt and
the final `--input` is treated as the current attempt.

## Interpretation

Resolved failure families are useful evidence for the next prompt or handoff
edit, but they are not proof that the design loop is good. Newly observed
failures and missing package-exam feedback must be reviewed before claiming
improvement.
