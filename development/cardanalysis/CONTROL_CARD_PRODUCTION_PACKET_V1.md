# Control Card Production Packet V1

## Purpose

`control_card_production_packet_v1` is the first human-facing report-only
packet for the control-only card production trial.

It consumes the current control discipline plus ideal candidate batch, candidate
batch exam, and candidate batch exam evidence snapshots. It turns those advisory
inputs into several concrete package versions that the owner can review before
any complete-card draft request or playable prototype work begins.

## Scope

The V1 packet outputs three to five control package versions. Each version
includes:

- a play promise;
- mechanism and ideal source;
- intended loop;
- role slots;
- eight semi-formal concept slots;
- combo and anti-combo notes;
- fun and strength evaluation;
- expected early, middle, and late strength curve;
- complexity-budget notes;
- generic-goodstuff drift and second-career risk;
- evidence and owner review questions;
- allowed preparation, blocked fields, and recommended next action.

Semi-formal concept slots may use card-like labels, cost bands, roles, and
mechanical intent. They are not official card text and are not runtime card
data.

## Current Packet Versions

The default fixture produces five unreviewed package versions:

- `white_order_fail_state_packet_v1`
- `blue_truth_forecast_packet_v1`
- `green_depth_compound_stability_packet_v1`
- `resource_tempo_denial_probe_v1`
- `hand_future_planning_probe_v1`

The first three come from the preserved candidate-batch exam focus set. The last
two are optional comparison probes from the production trial plan.

## Owner-Unavailable Behavior

The current fixture remains blocked:

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- owner decision slots stay empty;
- no reviewed or accepted evidence claim is created;
- no package version is promoted or rejected;
- no playable prototype, complete-card draft, official card text, or runtime card
  data is produced.

Automation may still format the packet, preserve evidence refs, prepare review
questions, and prepare for a later complete-card draft request after the owner
selects one or two package versions.

## Boundary

V1 keeps:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.blocked_by_owner_review = true`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.candidate_promoted = false`
- `boundary_assertions.candidate_rejected = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## Entrypoint

Generate the current packet:

```powershell
python scripts/run_control_card_production_packet.py --output-dir tmp/combat_analysis/control_card_production_packet_current
```

Validate the fixture:

```powershell
python scripts/run_control_card_production_packet.py --input tests/fixtures/combat_analysis/control_card_production_packet_v1 --json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_packet_v1.py tests/scripts/test_run_control_card_production_packet.py -q
```

## V1 Fixture

The current fixture output lives under:

`tests/fixtures/combat_analysis/control_card_production_packet_v1/`

It uses the existing control discipline plus ideal pilot fixtures as provisional
context while the owner is unavailable.

## Intended Follow-Up

If the owner selects one or two package versions, the next useful slice is a
complete-card draft request packet for those selected versions. If the owner is
still unavailable, the next useful slice is a comparison or repair-planning
packet that improves review questions without drafting formal cards.
