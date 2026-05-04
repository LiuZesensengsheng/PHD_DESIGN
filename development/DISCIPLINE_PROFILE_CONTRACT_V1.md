# Discipline Profile Contract V1

## Purpose

`discipline_profile_v1` is a JSON-safe input contract for a discipline or
career combat profile.

It exists to anchor the primary combat layer before later design work expands
ideal reward packages or trait proposals. The profile describes what the
discipline itself owns:

- primary combat identity,
- starting deck tendency,
- mechanism-axis center of gravity,
- and the local complexity budget for ordinary combat cards.

This is an advisory design-input layer only. It does not define runtime decks,
official card pools, hard gates, or legality.

## Why This Contract Comes First

The current layering strategy already states:

- discipline owns the main combat loop, starting deck, and core card pool;
- ideal card packages are shared ecology niches, not second careers;
- traits own long-term growth and should not become recurring combat chores.

Without a stable discipline profile, later `ideal_reward_package_v1` or
`ideal_trait_proposal_v1` work has no upstream anchor for what must remain in
the discipline layer. That makes "shared package" drift and "trait as combat
minigame" drift more likely.

V1 therefore prioritizes the layer that defines the baseline before the
extension layers.

## Authority Boundary

Every profile must set:

- `authority.authority_boundary = advisory_context_only`
- `authority.forbidden_uses` including:
  - `hard_gate_promotion`
  - `legality_decision`
  - `default_synthesis_path`
  - `runtime_starting_deck_definition`
  - `formal_card_pool_definition`

Generated hypotheses must also forbid `reviewed_evidence_claim`.

The contract is not registered in `report_only_surface_registry.py` and should
not be added to `capability_graph_registry.py` until a real implemented
consumer reads it as a live artifact.

## Schema

Required top-level fields:

- `schema_version`: must be `discipline_profile_v1`
- `discipline_id`
- `display_name`
- `design_intent`
- `source`
- `authority`
- `combat_identity`
- `starting_deck_profile`
- `complexity_budget`
- `cross_layer_hooks`
- `layering_guards`
- `evaluation_targets`
- `known_risks`
- `known_limits`

`source` fields:

- `source_type`: `design_note`, `generated_hypothesis`, `reviewed_fixture`, or
  `playtest_observation`
- `evidence_tier`: `human_curated`, `speculative`, or `reviewed`
- `review_status`: `draft`, `review_needed`, `accepted`, or
  `hypothesis_draft`

Reviewed fixture profiles must use `evidence_tier = reviewed` and
`review_status = accepted`. Generated hypotheses must use
`evidence_tier = speculative`, `review_status = hypothesis_draft`, and forbid
`reviewed_evidence_claim`.

`combat_identity` fields:

- `primary_fantasy`
- `core_loop_summary`
- `primary_mechanism_axes`
- `secondary_mechanism_axes`
- `fail_state_play_pattern`

`starting_deck_profile` fields:

- `guaranteed_axes`
- `opening_pattern`
- `resource_posture`
- `defense_posture`
- `card_flow_posture`

`complexity_budget` fields:

- `default_primary_axes_per_card`: must be `1` or `2`
- `default_secondary_axes_per_card`: must be `0` or `1`
- `per_turn_new_decision_budget`: `sts_core_only` or `single_clean_branch`
- `hidden_state_budget`: `none` or `visible_only`
- `tracking_budget`: `none` or `visible_low_memory_only`

`cross_layer_hooks` fields:

- `shared_package_hooks`
- `trait_biases`
- `event_exchange_pressures`

`layering_guards` fields:

- `discipline_owns`
- `must_not_externalize_to_ideal_package`
- `must_not_externalize_to_trait`

`discipline_owns` must include:

- `primary_combat_loop`
- `starting_deck_identity`
- `core_card_pool`

`must_not_externalize_to_ideal_package` must include:

- `replacement_starting_deck`
- `full_resource_economy`

`must_not_externalize_to_trait` must include:

- `recurring_per_turn_operations`
- `turn_by_turn_tracking_tax`

`evaluation_targets` fields:

- `complexity_target`
- `enemy_archetype_tests`
- `reward_path_tests`
- `starting_deck_success_window`
- `failure_state_expectation`

## Entrypoint

Write a template:

```powershell
python scripts/validate_discipline_profile.py --write-template tmp/combat_analysis/discipline_profile_template.json
```

Validate a file or fixture directory:

```powershell
python scripts/validate_discipline_profile.py --input tests/fixtures/combat_analysis/discipline_profile_v1
```

Print a machine-readable report:

```powershell
python scripts/validate_discipline_profile.py --input tests/fixtures/combat_analysis/discipline_profile_v1 --json
```

## V1 Fixture Pack

The first fixture pack contains three valid examples:

- a healthy human-curated discipline foundation,
- a reviewed fixture profile,
- a speculative generated-hypothesis frontier profile that stays below reviewed
  evidence.

Invalid boundary cases are covered in focused tests instead of being placed in
the valid fixture directory.

## Non-Goals

V1 does not:

- generate runtime starting decks or card pools,
- define formal card text,
- define enemy data,
- change UI or save structure,
- change capability graph or report-only registry files,
- enable hard gates, legality, default synthesis, learned, or reranker paths.

## Future Integration Notes

Recommended next contracts after this anchor exists:

1. `ideal_reward_package_v1` for shared enabler/payoff/glue/fail-state ecology
   that stays outside second-career territory.
2. `ideal_trait_proposal_v1` for long-run growth, imprint, and keystone
   innovation without adding recurring combat burden.

Both later contracts should reference the discipline profile rather than
re-describing the primary combat class from scratch.
