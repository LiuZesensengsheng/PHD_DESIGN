# Card Package Draft Handoff V1

## Purpose

`card_package_draft_handoff_v1` is the report-only request packet between a selected
package variant and a future `complete_card_draft_v1` JSON draft.

It answers:

```text
What exactly should an LLM or owner write next, and how will that output be checked?
```

It does not write complete card text by itself.

## Workflow Position

```text
sts1_exam_target_v1
  -> card_package_variant_set_v1
  -> card_package_draft_handoff_v1
  -> complete_card_draft_v1
  -> card_package_exam_v1
```

## What It Contains

Each handoff includes:

- target and variant source-chain ids;
- the selected variant and score context;
- `complete_card_draft_v1` root/card field requirements;
- required slots copied from the variant;
- target card constraints from the STS1 exam target;
- a prompt packet for LLM/owner drafting;
- a validation plan for complete draft, package health, and package exam checks.

## Boundary

All V1 handoffs use:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `handoff_scope = llm_complete_card_draft_request_only`

The handoff does not create:

- complete card drafts;
- formal/promoted cards;
- runtime card data;
- hard gates;
- reviewed evidence;
- default synthesis or learned/reranker behavior.

## Current Smoke Fixture

The first reusable smoke fixture selects `poison_clock_retain_bridge` by
default and requests a `complete_card_draft_v1` package with five required
slots. The standalone CLI wrapper has been retired; the retained library and
toolkit tests validate this fixture shape directly.

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_package_draft_handoff_v1.py -q
```

Current external draft intake should enter through
`llm_draft_prompt_application_v1`, which still records nested
`card_package_draft_handoff_v1` artifacts alongside draft attempt metadata.

## Stop Lines

Pause for human review before any follow-up:

- writes runtime card data;
- treats handoff output as a valid complete draft before validation;
- promotes generated cards as reviewed evidence;
- changes hard gates, default synthesis, learned behavior, or reranker behavior.
