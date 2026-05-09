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

## Entrypoints

```powershell
python scripts/run_llm_complete_card_draft_attempt.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/llm_complete_card_draft_attempt_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_llm_complete_card_draft_attempt_v1.py tests/scripts/test_run_llm_complete_card_draft_attempt.py -q
```

## Interpretation

Passing this attempt check means a generated draft can enter package exam. It
does not mean the cards are balanced, reviewed, legal, or ready for runtime data.
