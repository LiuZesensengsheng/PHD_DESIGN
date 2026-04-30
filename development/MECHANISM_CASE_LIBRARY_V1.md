# Mechanism Case Library V1

- Library: `mechanism_case_library_v1`
- Status: case-only fixture pack
- Contract: `cardanalysis_case_input_v1`
- Runtime impact: none

## Purpose

This document defines a case-only expansion pack for normalized mechanism and
card-package evidence.

The pack exists to grow coverage for mechanism selection and package design
without changing evaluator behavior, case schema, hard gates, default
recommendation paths, or the capability graph registry.

## Scope

In scope:

- reviewed and below-reviewed normalized cases for mechanism and card-package
  patterns;
- mechanism-heavy coverage for draw, discard, energy, defense, status, search,
  exhaust, temporary generation, position, charge, stance, threshold,
  sacrifice, curse, summon, and chain families;
- authority, provenance, and review-boundary preservation;
- schema-pressure notes captured in `known_limits` instead of schema edits.

Out of scope:

- evaluator logic changes;
- `case_input_contract.py` enum or field changes;
- capability-graph registry changes;
- default synthesis or recommendation routing;
- hard-gate promotion;
- learned or reranker default-path wiring.

## Contract Reuse

Every case in this pack stays on:

```text
schema_version = cardanalysis_case_input_v1
```

The pack does not introduce a parallel schema.

It uses:

- `design_object.object_type = "mechanism"` for direct mechanism cases;
- `design_object.object_type = "card_package"` for package-shape cases.

## Fixture Pack

The V1 fixture pack lives under:

```text
tests/fixtures/combat_analysis/mechanism_case_library_v1/
```

Initial coverage plus the first three increments is 78 normalized cases:

- 32 reviewed mechanism cases;
- 38 human-curated package or route-shape cases;
- 4 source-mined reference cases;
- 4 generated hypotheses.

Coverage buckets:

- draw
- discard
- energy
- block and defense
- status
- search and tutor
- exhaust, removal, and transform
- temporary card generation
- position and redirect
- charge and delayed payoff
- stance and mode switch
- threshold payoff
- sacrifice, self-damage, and stress cost
- curse or pollution as resource
- summon or temporary object
- chain, combo, and loop

The first increment adds failure and counterplay probes for draw clutter,
discard empty-hand collapse, energy hoarding, defense stall, status cleanup
tax, tutor overfit, temporary-generation execution load, and loop-breaker
density.

The second increment adds package density and brittleness probes for energy
refunds, status cleanup narrowness, summon payoff/body ratios, mode entry/exit
ratios, threshold accelerator overbuild, curse payoff density, position anchor
density, and temporary-generation core-plan drift.

The third increment adds 30 extended constraint cases: reviewed timing,
visibility, cap, interrupt, lockout, and overflow constraints; human-curated
package-ratio probes across draw, discard, energy, defense, status, search,
exhaust, transform, redirect, charge, stance, threshold, stress, and curse;
plus source-mined and generated cases that stay below reviewed authority.

## Authority Boundary

Every case keeps:

```text
authority.authority_boundary = advisory_context_only
```

Every case also keeps at least these consumer and non-consumer boundaries:

- `allowed_consumers`
  - `mechanism_axis_discovery_v1`
  - `cardanalysis_feature_projection_v1`
- `forbidden_uses`
  - `hard_gate_promotion`
  - `legality_decision`
  - `default_synthesis_path`

Below-reviewed cases also carry `reviewed_evidence_claim` inside
`authority.forbidden_uses`.

Source-mined references and generated hypotheses remain advisory exploration
material. They are not reviewed evidence and they are not canonical promotion
proof.

## Consumer Rules

This pack may inform:

- mechanism-axis discovery context;
- report-only feature projection;
- mechanism and package review prompts;
- future case-backed retrieval or clustering work.

This pack must not:

- change evaluator verdict semantics by itself;
- override existing reviewed fixture owners;
- become a hard gate or legality authority;
- feed default synthesis or recommendation paths;
- wash source-mined or speculative material into reviewed evidence.

## Schema Pressure / Future Gaps

The existing case contract was intentionally reused unchanged. A few mechanism
families still need text-label conventions rather than typed fields. Current
pressure markers include:

- `schema_pressure:status_lineage_and_owner_changes_are_text_only`
- `schema_pressure:search_reveal_and_target_zone_are_text_only`
- `schema_pressure:generated_card_origin_and_duration_are_text_only`
- `schema_pressure:position_geometry_needs_typed_slots`
- `schema_pressure:lane_adjacency_rules_are_text_only`
- `schema_pressure:charge_meter_state_is_text_only`
- `schema_pressure:charge_decay_budget_is_text_only`
- `schema_pressure:mode_transition_graph_is_text_only`
- `schema_pressure:threshold_track_and_overflow_are_text_only`
- `schema_pressure:self_damage_vs_stress_cost_requires_shared_cost_vocabulary`
- `schema_pressure:pollution_lineage_and_subtype_value_are_text_only`
- `schema_pressure:temporary_object_lifecycle_is_text_only`
- `schema_pressure:loop_budget_and_repeat_count_are_text_only`

These markers are documentation and review prompts. They are not schema-change
approval.

## Validation

Validate the pack with:

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/mechanism_case_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_case_library_v1.py -q
```
