# Source-Mined Factual Reference Library V1

- Library: `source_mined_factual_reference_library_v1`
- Contract: `cardanalysis_case_input_v1`
- Status: low-authority external fact reference library
- Runtime impact: none

## Purpose

This library stores factual, source-mined references from public game resources
so future `cardanalysis` reports can reason from concrete examples without
pretending the examples are reviewed project evidence.

The library is intentionally evidence-only. It does not define official project
cards, enemies, campaign pacing, mechanics, package rules, or UI behavior.

## Source Boundary

All V1 cases in this library use:

- `source.source_type = "source_mined_reference"`
- `source.evidence_tier = "source_mined"`
- `source.review_status = "unreviewed_reference"`
- `authority.authority_boundary = "advisory_context_only"`

Every case must include a public `source_url` when available and must forbid
`reviewed_evidence_claim`.

## Batch 1 Coverage

The first batch uses public Slay the Spire Wiki pages as mechanical-fact
references. It covers:

- card-count anti-spam pressure;
- boss passive chip and damage-cap pressure;
- status insertion and deck pollution;
- temporary card generation;
- exhaust package enablers and fail-state risk;
- block retention payoff;
- poison burst payoff;
- draw/cost randomization;
- hand retention and hand-clog pressure;
- card-play limit curses;
- boss split and rebirth phases;
- summoned-minion pressure;
- multi-hit and wound-pressure encounters.

These cases are useful as source-aware examples for future review packets, not
as design authority.

## Validation

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/source_mined_factual_reference_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_source_mined_factual_reference_library_v1.py -q
```

