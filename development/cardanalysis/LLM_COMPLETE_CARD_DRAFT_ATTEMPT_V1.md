# LLM Complete Card Draft Attempt V1

## Purpose

`llm_complete_card_draft_attempt_v1` records one generated or owner-supplied
answer to a `card_package_draft_handoff_v1` request.

It answers:

```text
Did this draft satisfy the handoff closely enough to enter package exam?
```

## Workflow Position

```text
card_package_draft_handoff_v1
  -> llm_complete_card_draft_attempt_v1
  -> complete_card_draft_v1 validation
  -> card_draft_failure_taxonomy_v1
  -> exam_iteration_run_v1
```

## What It Contains

Each attempt includes:

- handoff and selected-variant source-chain ids;
- draft input path;
- validation summary from `complete_card_draft_v1`;
- failure taxonomy counts and patch lanes;
- advisory next step, such as `run_card_package_exam` or `fix_schema_before_exam`;
- boundary assertions.

## Boundary

This surface does not call an LLM API by itself. It records the result of an
attempt that already exists as JSON.

It does not create:

- formal cards;
- runtime card data;
- hard gates;
- reviewed evidence;
- default synthesis behavior;
- learned or reranker behavior.

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_llm_complete_card_draft_attempt_v1.py -q
```

The standalone CLI wrapper has been retired. The retained library and toolkit
tests still validate handoff matching, `complete_card_draft_v1` validation,
failure taxonomy output, negative controls, boundary attempts, report payloads,
snapshot payloads, and manifest payloads. Current external draft intake should
enter through `llm_draft_prompt_application_v1`, which still records nested
`llm_complete_card_draft_attempt_v1` artifacts.

## Negative Controls

`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_negative_attempt_drafts_v1.json`
contains four generated-attempt negative controls, one per STS1 character. The
attempt test suite uses them to verify schema/slot, axis drift, combo-risk,
generic-goodstuff, exactness, weak fail-state, and STS1-like texture feedback
without promoting any draft.

`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_boundary_attempt_drafts_v1.json`
adds four schema-valid boundary attempts, one per STS1 character. These drafts are
intended to enter report-only iteration feedback and surface plausible design
risks such as secondary-axis swallowing, character-texture mismatch,
numeric-fantasy pressure, and early-weak/late-explosion shape.

## Interpretation

Passing this attempt check means a generated draft can enter package exam. It
does not mean the cards are balanced, reviewed, legal, or ready for runtime data.
