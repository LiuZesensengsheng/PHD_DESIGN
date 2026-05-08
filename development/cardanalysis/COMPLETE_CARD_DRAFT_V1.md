# Complete Card Draft V1

## Purpose

`complete_card_draft_v1` is the first contract that allows an owner or LLM-assisted
workflow to write full card draft text while keeping the result outside runtime card
data and reviewed evidence.

It answers:

```text
Can this proposed package be expressed as complete, reviewable card drafts?
```

It does not answer whether the cards should enter the game.

## Boundary

All V1 drafts use:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`

Required forbidden uses include:

- `hard_gate_promotion`
- `legality_decision`
- `default_synthesis_path`
- `formal_card_promotion`
- `runtime_card_definition`
- `reviewed_evidence_claim`

## Draft Shape

Each package includes:

- source and authority metadata;
- target game, character, primary axis, and secondary axes;
- source package seed and required package slots;
- one or more complete card drafts.

Each card draft includes:

- card id, name, color, type, rarity, and cost;
- rules text, upgraded rules text, and upgrade summary;
- package slot, package role, role tags, package tags, and slot tags;
- numeric profile;
- setup tax and exactness dependency;
- evidence trace and review notes.

## Package Health Bridge

The validator can export a temporary `card_package_health_v1` owner-input case.
That bridge lets complete card drafts satisfy the previously missing
`card_like_candidate_slots` lane without claiming reviewed evidence.

## Entrypoints

```powershell
python scripts/validate_complete_card_draft.py --write-template tmp/combat_analysis/complete_card_draft_template.json
python scripts/validate_complete_card_draft.py --input tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json
python scripts/validate_complete_card_draft.py --input tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --export-card-package-health-input tmp/combat_analysis/complete_card_draft_package_health_input.json
py -3.11 -m pytest tests/toolkit/combat_analysis/test_complete_card_draft_v1.py tests/scripts/test_validate_complete_card_draft.py -q
```

## Stop Lines

Pause for human review before any follow-up:

- writes runtime card data;
- changes formal card schemas;
- promotes a draft as reviewed evidence;
- changes hard gates, default synthesis, learned behavior, or reranker behavior.

