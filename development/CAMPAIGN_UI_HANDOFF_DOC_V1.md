# Campaign UI Handoff Doc V1

## Goal

Give the incoming campaign UI developer a short, executable handoff note:

- where UI work is safe
- which host seams to call
- which internals to avoid
- which tests protect the current contract

## Safe Work Areas

The safest places for new campaign UI work are:

- `contexts/campaign/ui_runtime/**`
- `contexts/campaign/ui/**`
- `contexts/campaign/rendering/**`
- `contexts/campaign/view.py`

Allowed work in those areas:

- retained widget/node composition
- rendering and local layout
- local animation
- local hit-testing
- event-to-intent translation

## Stable Host Seams

New UI work should prefer these `CampaignState` entrypoints instead of reaching
into internals.

Core interaction seams:

- `handle_clicked_block(block)`
- `request_end_turn(staged=False)`
- `request_gossip_entry()`
- `request_gossip_entry_debounced(now_ms=...)`
- `request_idea_selection()`
- `request_meeting_entry()`
- `request_choice_toggle()`
- `request_line_bubble_press(ui_element)`

Transition seams:

- `request_deck_view()`
- `request_event_block(block_id)`
- `request_combat_block(block_id, encounter_id)`
- `request_dev_combat(encounter_id)`
- `request_meeting()`
- `request_ending(trigger_reason, extra=...)`

Thesis submission seams:

- `check_and_prompt_thesis_submission()`
- `request_thesis_submission_for_writing_block(block)`

## Do Not Depend On These

Do not treat the following as stable UI contract:

- underscore-prefixed `CampaignState` fields
- direct `state.tx.*` calls
- direct transition payload writes into `persistent`
- direct `persistent` writes from runtime widgets
- `ThesisMetaService` as a presentation API
- `TrackBlockService` as a UI extension surface
- `CampaignMouseEventService` as the place to add more business rules

## Runtime UI Rule

`ui_runtime` owns only local runtime concerns:

- local node trees
- local widget state
- local animation
- local hit-testing

If a widget needs a business consequence, stop at a `CampaignState` seam.

Do not put campaign routing, thesis rules, or transition wiring inside
`ui_runtime`.

## Recommended Test Checks

When changing campaign UI, the fastest high-value checks are:

- `python -m pytest tests/campaign/test_campaign_ui_handoff_contracts.py -q`
- `python -m pytest tests/campaign/test_campaign_runtime_ui_boundary_contract.py -q`

If the change touches a specific seam, also run the focused seam suite:

- block click: `tests/campaign/test_campaign_block_click_orchestrator.py`
- end turn: `tests/campaign/test_campaign_end_turn_orchestrator.py`
- transition requests: `tests/campaign/test_campaign_transition_request_contract.py`
- thesis submission: `tests/campaign/test_thesis_submission_flow_service.py`

## When To Ask For A New Seam

Stop and ask for a new orchestration seam if the UI change would require:

- reading `_blocks` or other underscore state directly
- building transition payloads manually
- mutating thesis meta or submission history directly
- bypassing modal/input-lock ownership
- importing campaign business services into `ui_runtime`

## Current Bottom Line

The current handoff model is:

- UI owns presentation and local runtime behavior
- `CampaignState` owns lifecycle and stable entrypoints
- services own sequencing and business consequences

That is enough for parallel UI work without waiting for a full DDD rewrite or a
full node-tree migration.
