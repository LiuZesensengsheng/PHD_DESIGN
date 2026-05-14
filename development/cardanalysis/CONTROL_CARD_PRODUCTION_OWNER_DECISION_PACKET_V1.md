# Control Card Production Owner Decision Packet V1

## Purpose

`control_card_production_owner_decision_packet_v1` is the report-only owner
decision layer after `control_card_production_comparison_repair_v1`.

It consumes the current owner-blocked comparison/repair snapshot and turns it
into a low-effort review packet: if the owner only has ten minutes, answer the
small set of keep, revise, reject, merge, and next-round instruction fields.

The packet does not select a package, draft cards, promote or reject any package
version, or create a repair plan.

## Scope

V1 outputs:

- suggested owner review order;
- a ten-minute review question panel;
- one package decision card per package version;
- one-line play promise, mechanism axis, ideal id, advisory tier, top risks,
  and top repair notes per package;
- empty owner decision slots for `keep`, `revise`, `reject`, or `merge`;
- empty owner-selected, rejected, merge-pair, taste, strength, complexity,
  forbidden-pattern, and next-round instruction fields;
- decision readiness summary;
- allowed preparation and cannot-advance lists;
- explicit report-only boundary assertions.

## Current Readout

The default fixture preserves this suggested review order:

1. `white_order_fail_state_packet_v1`
2. `blue_truth_forecast_packet_v1`
3. `green_depth_compound_stability_packet_v1`
4. `hand_future_planning_probe_v1`
5. `resource_tempo_denial_probe_v1`

The first two remain the fastest owner-review candidates. Green-depth and
hand-future remain repair candidates. Resource-tempo denial remains a held risk
probe. These are advisory review-order hints, not authoritative selections.

## Owner-Unavailable Behavior

The V1 fixture remains blocked:

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- `decision_packet_status = owner_decision_packet_ready_owner_review_blocked`
- `decision_packet_ready_for_owner_review = true`
- `owner_decision_ready = false`
- `owner_selection_recorded = false`
- `next_repair_plan_ready = false`
- `next_repair_plan_status = blocked_awaiting_owner_package_selection`
- owner decision slots stay empty;
- no package version is selected, promoted, rejected, or merged;
- no reviewed or accepted evidence claim is created.

Automation may format this packet, preserve comparison/repair notes, prepare
empty owner decision templates, and prepare later repair-plan inputs after owner
selection. Automation may not record owner decisions, select packages, generate a
repair plan, draft formal cards, or write runtime card data.

## Boundary

V1 keeps:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.comparison_is_authoritative = false`
- `boundary_assertions.owner_decision_recorded = false`
- `boundary_assertions.owner_selection_recorded = false`
- `boundary_assertions.package_version_selected = false`
- `boundary_assertions.package_version_promoted = false`
- `boundary_assertions.package_version_rejected = false`
- `boundary_assertions.repair_plan_generated = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## Entrypoint

Generate the current owner decision packet:

```powershell
python scripts/run_control_card_production_owner_decision_packet.py --output-dir tmp/combat_analysis/control_card_production_owner_decision_packet_current
```

Validate the fixture:

```powershell
python scripts/run_control_card_production_owner_decision_packet.py --input tests/fixtures/combat_analysis/control_card_production_owner_decision_packet_v1 --json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_owner_decision_packet_v1.py tests/scripts/test_run_control_card_production_owner_decision_packet.py -q
```

## V1 Fixture

The current fixture output lives under:

`tests/fixtures/combat_analysis/control_card_production_owner_decision_packet_v1/`

It consumes:

`tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1/control_card_production_comparison_repair_v1_snapshot.json`

## Intended Follow-Up

If the owner fills the packet, the next useful slice is a repair-plan generator
for the selected one or two packages.

If the owner is still unavailable, keep improving evidence, comparison, and
review-question quality. Do not proceed to complete-card draft requests or
playable prototype work without owner selection.
