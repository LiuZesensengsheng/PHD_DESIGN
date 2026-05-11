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

Initial coverage plus the first four increments, the targeted round-2 gap
patch, package completion/conflict shards, the foundation-axis boundary shard,
and the exam-sensitivity shard is 222 normalized cases:

- 68 reviewed mechanism cases;
- 130 human-curated mechanism, package, or route-shape cases;
- 12 source-mined reference cases;
- 12 generated hypotheses.

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

The fourth increment adds 100 more cases in nine shards: three reviewed
mechanism packs, four human-curated package packs, one source-mined reference
pack, and one generated hypothesis pack. The goal is broad near-closeout
coverage without regressing into oversized files.

The targeted round-2 gap patch adds four human-curated direct mechanism cases
for the queue targets `curse_pollution` and `stance_mode_switch`. These cases
stay below reviewed authority and exist only to close the current mechanism-axis
coverage gap.

The foundation-axis boundary shard adds four human-curated advisory mechanism
cases that illustrate how draw, discard, energy, exhaust, defense/block, damage,
status, search/tutor, retain, filter, compression/removal, temporary generation,
and scaling can support or swallow higher-level mechanism identity. These cases
are shared-language examples, not reviewed evidence or hard-gate inputs.

The exam-sensitivity shard adds 16 human-curated advisory card-package cases for
current report-only exam blind spots: axis drift, same-lane content changes,
secondary-axis swallowing, character texture mismatch, early-weak/late-explosive
shape, package synergy collapse, and failure-state quality. The second slice
adds Defect orb/focus/power tempo, lightning/frost support-lane takeover, and
orb-slot/focus synergy-collapse probes plus Watcher wrath/calm, retain/scry,
mantra early-floor, and wrong-stance failure-state probes. These cases provide
future mechanism-axis, package-health, and feature-projection inputs only; they
do not change scorecard weights, exam implementation, runtime card data, or
promotion authority.

## Pack Layout

The fixture directory is intentionally sharded:

- `mechanism_cases_v1.json`
- `mechanism_failure_counterplay_cases_v1.json`
- `mechanism_package_density_cases_v1.json`
- `mechanism_reviewed_constraint_cases_v1.json`
- `mechanism_package_ratio_cases_v1.json`
- `mechanism_frontier_reference_and_hypothesis_cases_v1.json`
- `mechanism_reviewed_access_and_tempo_cases_v1.json`
- `mechanism_reviewed_board_and_timing_cases_v1.json`
- `mechanism_reviewed_pressure_and_scaling_cases_v1.json`
- `mechanism_package_access_support_cases_v1.json`
- `mechanism_package_tempo_pressure_cases_v1.json`
- `mechanism_package_board_structure_cases_v1.json`
- `mechanism_package_cost_recovery_cases_v1.json`
- `mechanism_frontier_reference_cases_v1.json`
- `mechanism_frontier_hypothesis_cases_v1.json`
- `mechanism_axis_gap_round_2_cases_v1.json`
- `mechanism_package_completion_cases_v1.json`
- `mechanism_package_conflict_cases_v1.json`
- `mechanism_exam_sensitivity_cases_v1.json`
- `mechanism_foundation_axis_boundary_cases_v1.json`

The goal is not many tiny files for their own sake. The goal is to keep each
pack reviewable and semantically legible.

## Pack Management Rules

Preferred maintenance rules:

- add new cases as a new semantic shard, not by endlessly growing one legacy
  file;
- keep a shard around `8-16` cases when possible;
- avoid shards larger than `20` cases unless there is a strong review reason;
- isolate source-mined and generated material from reviewed and human-curated
  packs when practical;
- keep focused tests pack-aware, using per-pack counts and tier checks instead
  of a giant single expected-id list.

Future re-sharding is acceptable as long as:

- case content stays semantically identical,
- `case_id` values stay stable,
- source/review boundaries stay unchanged,
- the contract remains `cardanalysis_case_input_v1`.

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
