# Card Draft Failure Taxonomy V1

## Purpose

`card_draft_failure_taxonomy_v1` is the report-only label set for generated or
owner-supplied `complete_card_draft_v1` attempts.

It answers:

```text
Why did this draft fail before or during the card-package exam?
```

## Failure Families

V1 names failures across these lanes:

- schema and authority boundary;
- required slot coverage;
- card-count and target constraints;
- mechanism axis identity;
- package role structure;
- payoff-before-bridge sequencing;
- exactness fantasy and setup tax;
- generic goodstuff drift;
- weak fail-state floor;
- combo explosion risk;
- STS1-like card feel;
- unclear fun texture.

## Boundary

Failure labels are revision guidance only.

They do not create:

- formal cards;
- runtime card data;
- hard gates;
- reviewed evidence;
- default synthesis behavior;
- learned or reranker behavior.

## Validation

The retained taxonomy library is validated by:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_draft_failure_taxonomy_v1.py tests/toolkit/combat_analysis/test_llm_complete_card_draft_attempt_v1.py -q
```

The standalone `llm_complete_card_draft_attempt_v1` CLI wrapper has been
retired. Current external draft intake should enter through
`llm_draft_prompt_application_v1`, which still records nested attempt artifacts
and applies this taxonomy before downstream report-only exams.

## Negative Controls

The generated-attempt fixture
`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_negative_attempt_drafts_v1.json`
keeps one intentionally flawed draft per STS1 character. It is used by the
attempt and iteration tests to check that schema/slot, axis identity,
package-structure, STS1-like, strength, combo, and fun-texture failures are
visible before future prompt patches are trusted.

The companion boundary fixture
`tests/fixtures/combat_analysis/llm_complete_card_draft_attempt_v1/sts1_four_character_boundary_attempt_drafts_v1.json`
keeps one schema-valid but suspicious draft per STS1 character. It is used to
check that the existing taxonomy and iteration readout still expose warning
families for secondary-axis swallowing, generic goodstuff, numeric fantasy,
weak fail states, and STS1-like texture drift without adding a hard gate.
