# Exam Iteration Multi-Character Batch Summary V1

## Purpose

`exam_iteration_multi_character_batch_summary_v1` is a report-only artifact for
comparing generated-attempt batch snapshots across multiple STS1 character
targets.

It answers:

```text
Across character-target generated-attempt batches, which failure families are
resolved, persistent, or newly observed, and did every batch preserve
prompt-application intake boundaries?
```

## Workflow Position

```text
exam_iteration_generated_attempt_batch_run_v1 snapshots
  -> exam_iteration_multi_character_batch_summary_v1
```

This surface does not run drafts through exams itself. It reads already-written
batch-run snapshots and summarizes cross-character movement.

## What It Writes

The CLI writes:

- `exam_iteration_multi_character_batch_summary_v1_report.md`;
- `exam_iteration_multi_character_batch_summary_v1_snapshot.json`;
- `exam_iteration_multi_character_batch_summary_v1_manifest.json`.

## Boundary

This surface is cross-character feedback only.

It does not:

- call an LLM API;
- generate complete card drafts;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change default synthesis behavior;
- enable learned or reranker behavior.

It rejects source batch snapshots that claim any of those boundary-crossing
actions or that report prompt-application intake boundary violations.

## Entrypoints

```powershell
python scripts/run_exam_iteration_multi_character_batch_summary.py --input <silent_exam_iteration_generated_attempt_batch_run_v1_snapshot.json> --input <ironclad_exam_iteration_generated_attempt_batch_run_v1_snapshot.json> --output-dir tmp/combat_analysis/exam_iteration_multi_character_batch_summary_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_multi_character_batch_summary_v1.py tests/scripts/test_run_exam_iteration_multi_character_batch_summary.py -q
```

## Interpretation

A clean multi-character summary means the current feedback loop can compare
failure movement across supplied/generated attempt batches. It does not mean
the underlying draft cards are balanced, reviewed, or ready for runtime
promotion.
