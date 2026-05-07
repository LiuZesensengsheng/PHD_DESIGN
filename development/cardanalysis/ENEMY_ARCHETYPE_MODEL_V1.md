# Enemy Archetype Model V1

## Purpose

Define a case-backed, report-only enemy archetype library for `cardanalysis`.

The goal is not to ship formal enemy stats, runtime encounter scripts, or a
catalog of 200 authored monsters. The goal is to create a reusable normalized
case pack that describes how enemy archetypes validate:

- mechanism promises,
- package resilience,
- campaign pressure pacing,
- stress and recovery expectations,
- player agency under pressure.

## Scope Boundary

In scope:

- normalized `cardanalysis_case_input_v1` cases with
  `design_object.object_type = encounter`,
- archetype-level pressure descriptions,
- advisory relationships to campaign power, stress/resolve, and campaign
  experience models,
- partial-solve expectations and hard-counter risk notes,
- future feature-projection and autonomous-design consumers.

Out of scope:

- monster stats,
- runtime encounter implementation,
- combat runtime changes,
- campaign runtime changes,
- hard gates,
- default synthesis path changes,
- learned or reranker enablement.

## V1 Artifact

V1 stores a normalized case-pack directory at:

`tests/fixtures/combat_analysis/enemy_archetype_model_v1/`

Current shards:

- `enemy_archetype_cases_v1.json`
- `enemy_archetype_gap_round_2_cases_v1.json`
- `enemy_archetype_elite_punisher_longrun_cases_v1.json`
- `enemy_archetype_source_mined_frontload_references_v1.json`

The pack is intentionally report-first and case-library-only.

## Pack-Local Conventions

The library stays inside the existing case-input contract. It does not change
the shared schema. Instead, V1 uses pack-local nested fields inside the existing
`contexts` containers:

- `contexts.combat.player_capability_tests`
- `contexts.combat.hard_counter_risk`
- `contexts.combat.partial_solve_expectation`
- `contexts.combat.identity_notes`
- `contexts.deck_or_package.soft_pressure_mechanisms`
- `contexts.deck_or_package.preferred_partial_answers`
- `contexts.campaign.phase_window`
- `contexts.campaign.campaign_role`
- `contexts.campaign.advisory_relations`
- `contexts.experience.agency_window`
- `contexts.experience.failure_value`
- `contexts.experience.non_numeric_identity`
- `contexts.experience.pressure_texture`

These fields are pack-local vocabulary for encounter modeling. They are not
global schema promotions.

## V1 Coverage

The current pack covers these archetype families:

- early pressure tester
- block tax enemy
- sustain check enemy
- burst clock enemy
- delayed burst enemy
- multi-enemy spread pressure
- status pollution enemy
- draw disruption enemy
- discard pressure enemy
- energy tax enemy
- positioning / redirect validation enemy
- target-priority enemy
- summon / add pressure enemy
- fragile race enemy
- scaling race enemy
- anti-infinite soft pressure enemy
- partial-solve friendly enemy
- failure-state value probe enemy
- stress carryover enemy
- recovery-window validator
- elite punisher
- frontload defense check
- boss phase shift

The newest source-mined frontload-reference shard adds below-reviewed external
references for Jaw Worm and Gremlin Nob. These cases thicken
`frontload_defense_check` coverage while preserving source uncertainty and
forbidding reviewed evidence claims.

Some families now intentionally use more than one normalized case under the
same `primary_axis`. That is a coverage choice, not a schema change: reviewed
and human-curated variants can coexist without promoting the whole family into
runtime or hard-gate authority.

## Advisory Boundary

Every case remains locked to:

- `authority_boundary = advisory_context_only`
- report-only consumers only
- no hard-gate authority
- no legality authority
- no default synthesis authority
- no monster stat tuning authority

Enemy archetype cases may inform future package, campaign, and autonomous design
reports. They must not become a direct runtime or balance owner.

## Intended Consumers

The initial allowed-consumer set is intentionally narrow and advisory:

- `campaign_power_curve_report_v1`
- `campaign_advisory_bundle_v1`
- `evaluation_autonomous_design_model_v1`
- `cardanalysis_feature_projection_v1`

Additional consumers should be registered only after real implementation lands.

## Modeling Notes

V1 treats enemy identity as a pressure question, not a stat line.

Each case tries to answer:

1. what player capability is being tested,
2. which mechanisms or package habits are under soft pressure,
3. when the archetype risks becoming a hard counter,
4. what a good partial solve looks like,
5. what local value remains after imperfect play,
6. how the pressure should relate to campaign pacing and recovery.

The round-two gap fill especially targets three pressure questions that are
easy to under-cover if the pack stays one-case-per-axis only:

- how elite encounters punish exposed greedy turns,
- how early encounter pressure checks immediate defense rather than generic
  opener stability,
- how boss fights ask for answer reorientation across phase shifts.

The long-running case-library lane adds a focused `elite_punisher` shard to
thicken the current thin-reviewed queue target without changing any consumer or
runtime behavior. The extra cases focus on contingency-buffer preservation,
soft counterplay lane diversity, and route-cost accounting.

## Schema Pressure / Future Gaps

The current shared schema is sufficient for V1, but a few pressure points remain:

- encounter composition detail is descriptive only; there is no typed lane,
  spawn-order, or initiative schema,
- pressure intensity bands are prose labels rather than calibrated numeric
  envelopes,
- stress carryover and recovery windows are advisory notes, not typed
  downstream contracts,
- partial-solve outcome tiers are prose, not a shared taxonomy,
- the pack can describe positioning and redirect validation, but it does not
  encode runtime board geometry.

These are documented as pack-local conventions and `known_limits`, not schema
changes.
