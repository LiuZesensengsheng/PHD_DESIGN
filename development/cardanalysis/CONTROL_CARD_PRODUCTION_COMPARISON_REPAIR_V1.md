# Control Card Production Comparison Repair V1

## Purpose

`control_card_production_comparison_repair_v1` is the report-only comparison and
repair-note layer after `control_card_production_packet_v1`.

It consumes the current owner-blocked control card production packet, compares
the five unreviewed package versions, and prepares deterministic repair notes
for owner review. It does not select a package, draft cards, or promote any
package version.

## Scope

V1 outputs:

- one comparison row per package version;
- fun-promise clarity notes;
- strength-curve risk notes across early, middle, and late phases;
- complexity, generic-goodstuff drift, and second-career risk summaries;
- source evidence/readiness summary;
- repair-priority labels and suggested repair notes;
- lane comparisons such as white-order vs blue-truth, blue-truth vs
  hand-future planning, green-depth vs the front runners, and
  resource-tempo denial as a risk probe;
- recommendation tiers for first owner review, repair candidates, hold-as-probe,
  and owner-boundary review;
- owner decision slots that remain empty;
- allowed preparation and cannot-advance lists;
- explicit report-only boundary assertions.

## Current Readout

The default fixture compares five package versions:

- `white_order_fail_state_packet_v1`
- `blue_truth_forecast_packet_v1`
- `green_depth_compound_stability_packet_v1`
- `resource_tempo_denial_probe_v1`
- `hand_future_planning_probe_v1`

Current advisory tiers are:

- first owner review: `white_order_fail_state_packet_v1`,
  `blue_truth_forecast_packet_v1`
- repair candidates: `green_depth_compound_stability_packet_v1`,
  `hand_future_planning_probe_v1`
- hold as probe: `resource_tempo_denial_probe_v1`

These tiers are not authoritative selections.

## Owner-Unavailable Behavior

The V1 fixture remains blocked:

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- `repair_notes_status = automatic_comparison_repair_notes_ready_owner_review_blocked`
- `next_repair_plan_ready = false`
- `next_repair_plan_status = blocked_awaiting_owner_package_selection`
- owner decision slots stay empty;
- no package version is selected, promoted, rejected, or merged;
- no reviewed or accepted evidence claim is created.

Automation may compare the unreviewed package versions, preserve repair notes,
collect owner questions, and prepare evidence refs for a later review packet.
Automation may not select packages, draft formal cards, create runtime data, or
start playable prototype work.

## Boundary

V1 keeps:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.source_packet_is_authoritative = false`
- `boundary_assertions.comparison_is_authoritative = false`
- `boundary_assertions.owner_selection_recorded = false`
- `boundary_assertions.repair_plan_generated = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.package_version_promoted = false`
- `boundary_assertions.package_version_rejected = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## Entrypoint

Generate the current comparison repair packet:

```powershell
python scripts/run_control_card_production_comparison_repair.py --output-dir tmp/combat_analysis/control_card_production_comparison_repair_current
```

Validate the fixture:

```powershell
python scripts/run_control_card_production_comparison_repair.py --input tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1 --json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_comparison_repair_v1.py tests/scripts/test_run_control_card_production_comparison_repair.py -q
```

## V1 Fixture

The current fixture output lives under:

`tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1/`

It consumes:

`tests/fixtures/combat_analysis/control_card_production_packet_v1/control_card_production_packet_v1_snapshot.json`

## Intended Follow-Up

If the owner becomes available, the next useful step is an owner decision packet
that records keep, revise, reject, or merge choices for one or two package
versions.

If the owner is still unavailable, continue improving comparison/exam evidence
or prepare non-authoritative review questions. Do not proceed to complete-card
draft requests or playable prototype work without owner selection.
