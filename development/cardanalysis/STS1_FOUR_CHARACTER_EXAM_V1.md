# STS1 Four Character Exam V1

## Purpose

`sts1_four_character_exam_v1` is a report-only application loop that runs the
current STS1 card-package design exam across Ironclad, Silent, Defect, and
Watcher.

It connects:

```text
sts1_exam_target_v1
-> card_package_variant_set_v1
-> card_package_draft_handoff_v1
-> complete_card_draft_v1
-> card_package_exam_v1
```

## Boundary

This surface is advisory context only.

It does not:

- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change default synthesis behavior;
- enable learned or reranker behavior.

The current fixture drafts are owner-supplied draft material for loop testing.
They require human review before any design promotion.

## Default Command

```powershell
python scripts/run_sts1_four_character_exam.py
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_four_character_exam_v1.py tests/scripts/test_run_sts1_four_character_exam.py -q
```

## Current Coverage

The first four-character exam uses these target lanes:

| Character | Primary Axis | Secondary Axes |
| --- | --- | --- |
| Silent | `poison` | `retain`, `shiv` |
| Ironclad | `strength_scaling` | `exhaust`, `block_engine` |
| Defect | `orb_control` | `frost_control`, `power_focus_scaling` |
| Watcher | `stance_mantra` | `scry_control`, `retain` |

The report-only enrichment inventory for current papers, blind spots, and proposed
negative/boundary samples lives in
`docs/development/cardanalysis/STS1_CARD_EXAM_ENRICHMENT_V1.md` and
`tests/fixtures/combat_analysis/sts1_card_exam_enrichment_v1/sts1_card_exam_enrichment_proposals_v1.json`.
The first concrete boundary-attempt batch lives in
`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_boundary_attempt_drafts_v1.json`
and is validated without changing this four-character exam contract.

## Interpretation

Passing this exam means the report-only loop can carry all four STS1 characters
from target constraints through variant selection, handoff, complete owner draft,
package-health feedback, and package exam summary.

It does not mean the model can autonomously publish balanced, legal STS1 cards.
The next capability gap is replacing owner-filled complete drafts with a bounded
LLM generation attempt and comparing failure patterns across repeated exam runs.
