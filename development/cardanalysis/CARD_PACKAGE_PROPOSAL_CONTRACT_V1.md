# Card Package Proposal Contract V1

## Purpose

`card_package_proposal_v1` is a JSON-safe contract for a card package draft.
It lets later cardanalysis tools discuss a mechanism-centered package skeleton
without creating formal cards, runtime card data, legality decisions, hard
gates, or default synthesis recommendations.

This contract is an input layer only. Human review still owns ideal selection,
mechanism taste, card text, tuning, and whether a draft should become real
content.

## Authority Boundary

Every proposal must set:

- `authority.authority_boundary = advisory_context_only`
- `authority.forbidden_uses` including:
  - `hard_gate_promotion`
  - `legality_decision`
  - `default_synthesis_path`
  - `formal_card_generation`
  - `runtime_card_definition`

Generated hypotheses must also forbid `reviewed_evidence_claim`.

The contract is not a report-only surface registry entry and is not registered
as a capability graph owner in V1.

## Schema

Required top-level fields:

- `schema_version`: must be `card_package_proposal_v1`
- `proposal_id`
- `title`
- `design_intent`
- `ideal_ref`: string or null
- `source`
- `authority`
- `mechanism_core`
- `support_requirements`
- `package_slots`
- `evaluation_targets`
- `known_risks`
- `known_limits`

`source` fields:

- `source_type`: `design_note`, `generated_hypothesis`, `reviewed_fixture`, or
  `playtest_observation`
- `evidence_tier`: `human_curated`, `speculative`, or `reviewed`
- `review_status`: `draft`, `review_needed`, `accepted`, or
  `hypothesis_draft`

Reviewed fixture proposals must use `evidence_tier = reviewed` and
`review_status = accepted`. Generated hypotheses must use
`evidence_tier = speculative`, `review_status = hypothesis_draft`, and forbid
`reviewed_evidence_claim`.

`mechanism_core` fields:

- `primary_axis`
- `secondary_axes`
- `mechanism_promise`
- `failure_state_value`
- `counterplay_or_agency`

`support_requirements` fields:

- `basic_axes`
- `resource_axes`
- `timing_axes`
- `defense_axes`
- `card_flow_axes`
- `campaign_axes`

`package_slots` entries require:

- `slot_id`
- `slot_role`: one of `starter`, `enabler`, `payoff`, `glue`, `defense`,
  `draw`, `resource`, `fail_state`, `bridge`, or `capstone`
- `count_hint`
- `description`
- `required`
- `risk_notes`

A proposal should include `enabler`, `payoff`, and `glue` slots. If one of
those roles is intentionally absent, `known_limits` must explicitly declare the
missing role with `missing_enabler_slot`, `missing_payoff_slot`, or
`missing_glue_slot`.

`evaluation_targets` fields:

- `expected_online_window`
- `expected_campaign_phase`
- `enemy_archetype_tests`
- `deck_compression_expectation`
- `fun_health_expectation`
- `package_health_expectation`

## Entrypoint

Write a template:

```powershell
python scripts/validate_card_package_proposal.py --write-template tmp/combat_analysis/card_package_proposal_template.json
```

Validate a file or fixture directory:

```powershell
python scripts/validate_card_package_proposal.py --input tests/fixtures/combat_analysis/card_package_proposal_v1
```

Print a machine-readable report:

```powershell
python scripts/validate_card_package_proposal.py --input tests/fixtures/combat_analysis/card_package_proposal_v1 --json
```

## V1 Fixture Pack

The first fixture pack contains eight valid examples:

- healthy mechanism package skeleton
- payoff-only package with explicit missing support limits
- strong mechanism with explicit fail-state value
- compression-dependent loop package
- campaign-late package with early dead-card risk
- defense-light fragile package
- generated hypothesis that cannot claim reviewed evidence
- resource bridge package

Invalid boundary cases are covered in focused tests instead of being placed in
the valid fixture directory.

## Non-Goals

V1 does not:

- generate official cards or runtime card definitions
- change existing evaluators
- change `case_input_contract.py`
- change `feature_projection.py`
- change capability graph or report-only registry files
- promote generated or human-curated drafts into reviewed evidence
- enable hard gates, default synthesis, recommendation, learned, or reranker
  paths

## Future Integration Notes

Future owners can evaluate whether this contract should feed mechanism
candidate cards, design iteration briefs, or autonomous design review. Any
registration should be done by MasterAgent after an implemented consumer exists.
