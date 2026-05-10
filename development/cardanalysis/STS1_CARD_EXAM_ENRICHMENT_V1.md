# STS1 Card Exam Enrichment V1

## Purpose

This document is a report-only enrichment pass for the current STS1 card and
card-package exam content.

It focuses on:

- exam paper inventory;
- negative controls and boundary sample proposals;
- current blind spots;
- `card_design_scorecard_v1` dimension suggestions.

It does not call an LLM, generate formal cards, write runtime card data, change
hard gates, enable learned or reranker behavior, or change `exam_iteration_*` core
contracts.

## Current Exam Papers

| Paper | Fixture | Current use |
| --- | --- | --- |
| Four-character happy path | `tests/fixtures/combat_analysis/sts1_four_character_exam_v1/four_character_exam_sources_v1.json` | Runs Silent, Ironclad, Defect, and Watcher through the report-only package exam loop. |
| Four-character generated-attempt negatives | `tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_negative_attempt_drafts_v1.json` | Provides one intentionally flawed generated-attempt draft per character. |
| Four-character boundary generated attempts | `tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_boundary_attempt_drafts_v1.json` | Provides one schema-valid but suspicious generated-attempt draft per character for report-only attempt and iteration feedback. |
| Enrichment proposal pack | `tests/fixtures/combat_analysis/sts1_card_exam_enrichment_v1/sts1_card_exam_enrichment_proposals_v1.json` | Lists proposed negative and boundary cases, blind spots, and scorecard dimensions. |

## Current Coverage

| Character | Positive lane | Existing negative focus |
| --- | --- | --- |
| Silent | poison with retain and shiv support | missing required slot |
| Ironclad | strength scaling with exhaust and block support | axis drift and generic goodstuff |
| Defect | orb control with frost and focus support | combo explosion and generic goodstuff |
| Watcher | stance/mantra with scry and retain support | exactness, weak fail state, and non-STS1-like text |

The current set is useful, but each character mostly tests a different failure
family. The next exam-content batch should rotate failure families across characters
so the exam can catch plausible bad drafts, not only obvious broken drafts.

The first concrete boundary batch now does this without changing the core exam
contracts: it uses valid `complete_card_draft_v1` payloads that can enter
`llm_complete_card_draft_attempt_v1` and `exam_iteration_run_v1`, then checks that
existing report-only feedback names the expected revision risks.

## Blind Spots

- Family coverage is uneven across characters.
- Plausible boundary samples are thin: off-character but tag-correct drafts can still
  look acceptable.
- Numeric fantasy is not directly classified when the draft remains schema-valid.
- Secondary axes can swallow the primary axis without always becoming a blocking
  axis drift.
- Early-weak but late-explosive packages need named samples.

## Proposed Samples

The proposal fixture covers at least one new negative or boundary case for each
character:

- Silent: shiv tempo swallowing poison, retained bookkeeping that feels off-character,
  and shiv/draw/refund combo risk.
- Ironclad: block engine swallowing strength, missing fail-state floor, and overlarge
  strength numbers.
- Defect: frost/focus swallowing orb control, free focus numeric fantasy, and delayed
  dark-release early/late imbalance.
- Watcher: generic stance goodstuff, retain/scry setup tunnel, and early blank turns
  into late Divinity explosion.

These are proposals, not runtime cards. They should become concrete fixtures only
after the main exam owner decides which cases should be blocking failures and which
should remain warning-only.

## Concrete Boundary Attempt Batch

The first promoted report-only batch keeps one new generated-attempt boundary case
per character:

| Character | Case | Main pressure |
| --- | --- | --- |
| Silent | `silent_shiv_tempo_goodstuff_boundary_attempt_v1` | Shiv tempo and refunds explain the package better than poison. |
| Ironclad | `ironclad_block_engine_swallows_strength_boundary_attempt_v1` | A block engine swallows the intended strength-scaling identity. |
| Defect | `defect_free_focus_numeric_fantasy_boundary_attempt_v1` | Free focus and refund language create numeric-fantasy combo pressure. |
| Watcher | `watcher_early_blank_late_divinity_explosion_boundary_attempt_v1` | Early turns are too blank while late Divinity payoff spikes too hard. |

This batch is deliberately warning-oriented: the drafts remain schema-valid and
can enter package-exam feedback so reviewers can inspect the failure readout
instead of only proving that invalid JSON is rejected.

## Scorecard Suggestions

Suggested `card_design_scorecard_v1` dimensions:

- `primary_axis_dominance`
- `secondary_axis_containment`
- `character_texture_fit`
- `numeric_band_grounding`
- `fail_state_floor_specificity`
- `early_floor_late_ceiling_balance`
- `sts1_text_compactness`

These dimensions should remain advisory until reviewed examples and stable numeric
evidence exist. In particular, `numeric_band_grounding` should not become a gate
without per-character reviewed bands.

## Waiting For Mainline

- Turn selected proposals into a second concrete negative-control fixture batch.
- Decide which boundary samples should stay warning-only and which should become
  blocking expectations in a future mainline exam pass.
- Add scorecard implementation only after the scorecard owner accepts the dimension
  definitions and evidence sources.
- Keep `exam_iteration_run_v1` and `exam_iteration_generated_attempt_batch_run_v1`
  core contracts unchanged for this enrichment pass.

## Validation

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_card_exam_enrichment_v1.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_card_exam_boundary_attempts_v1.py -q
```
