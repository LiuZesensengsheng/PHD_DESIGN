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
  -> facade iterate/provider-comparison follow-up
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

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_exam_iteration_prompt_patch_proposal_v1.py -q
```

The standalone CLI wrapper has been retired. The retained library and toolkit
tests still validate proposal construction from `exam_iteration_run_v1`
snapshots, prompt/handoff patch lanes, boundary assertions, report payloads,
snapshot payloads, and manifest payloads.

## Interpretation

A proposal is useful when repeated generated attempts share the same failure
lanes. It should be used to tighten the next `card_package_draft_handoff_v1` or
LLM prompt before another generated attempt is recorded.

It is not evidence that design quality improved. Improvement still requires new
attempts, validation, package exam feedback, facade-backed comparison or
iteration readout, and human review before promotion.
