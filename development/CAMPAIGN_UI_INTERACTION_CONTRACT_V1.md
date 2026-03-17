# Campaign UI Interaction Contract V1

## Goal

Define the minimum stable interaction surface that a UI-focused collaborator can
depend on while `campaign` remains in mixed-mode transition.

This document is intentionally practical. It does not describe the final
architecture. It defines:

- which campaign entrypoints are stable enough for UI work now
- which state and service internals are not safe UI dependencies
- which seams should be treated as application/orchestration ownership

## Why This Exists

`CampaignState` is already acting as a UI host, but some campaign flows still
mix:

- pygame event adaptation
- view/runtime widget handling
- transition orchestration
- thesis-specific state mutation

That is acceptable during migration, but it is not a safe implicit contract for
parallel UI work.

The rule for UI collaboration is:

- UI may depend on stable host entrypoints
- UI may own presentation/runtime-node behavior
- UI must not reach into campaign business internals directly

## Non-Goals

This contract does not:

- fully redesign campaign into final DDD layers
- make every current `services/*` module a stable public API
- require full node-tree migration before UI work starts
- bless private underscore-prefixed state fields as long-term contract

## Current Stable UI Host Surface

These are the state-level entrypoints that UI work may rely on now.

### Lifecycle Host

Owned by `CampaignState`:

- `startup(persistent)`
- `cleanup()`
- `handle_event(event)`
- `update(dt)`
- `draw()`

Meaning:

- external callers should treat `CampaignState` as the lifecycle host
- UI should not bypass this host and independently drive campaign services

### User-Intent Entry Seams

Stable enough for current UI work:

- `CampaignState.handle_clicked_block(block)`
- `CampaignState.request_end_turn(staged=False)`
- `CampaignState.request_ending(trigger_reason, extra=...)`

Meaning:

- UI may forward a resolved block click into the host seam
- UI may request end-turn through one explicit request seam
- UI may request ending transition
- UI should not manually reproduce the downstream business sequence

Compatibility note:

- `CampaignState.end_turn()` still exists in V1 as a compatibility wrapper for
  actual turn advancement
- new UI-facing code should prefer `request_end_turn(...)`

### Transition Request Surface

Stable state-level transition seams now exposed by `CampaignState`:

- `request_deck_view()`
- `request_event_block(block_id)`
- `request_combat_block(block_id, encounter_id)`
- `request_dev_combat(encounter_id)`
- `request_meeting()`
- `request_ending(trigger_reason, extra=...)`

Meaning:

- UI may trigger state transitions only through explicit state request seams
- transition payload construction remains owned by `TransitionHelper` and shared
  contract helpers
- UI must not call `state.tx.*` directly
- UI must not write transition payloads directly into `persistent`

### View / Runtime Presentation Surface

Presentation-facing helpers currently exposed by `CampaignView`:

- `handle_runtime_ui_event(event)`
- `update_runtime_ui(dt)`
- `render_runtime_ui(surface)`
- `draw_layers(...)`
- `show_choice_toggle(visible)`
- `screen_to_canvas(screen_pos)`
- `get_content_transform_params()`
- `get_block_rect(block, current_turn=...)`

Meaning:

- these are presentation/runtime helpers, not business APIs
- UI collaborators may extend them for rendering and runtime widget behavior
- business branching must not be added here

## UI-Owned Areas

The following areas are appropriate for UI-focused work:

- `contexts/campaign/view.py`
- `contexts/campaign/rendering/**`
- `contexts/campaign/ui/**`
- `contexts/campaign/ui_runtime/**`

Allowed responsibilities:

- rendering
- node/widget composition
- local hit areas
- local animation
- local visibility/lifecycle
- coordinate conversion and layout
- event-to-intent translation that forwards into state/application seams

## Application / Orchestration-Owned Areas

The following areas should own campaign process logic:

- `TransitionHelper`
- startup hydration/effects services
- modal dispatch and input lock coordination
- turn advancement sequencing
- block click routing
- thesis submission / publication orchestration

UI may call into these seams.

UI must not re-implement their sequencing locally.

## Explicit Non-Contract Internals

UI should not directly depend on any of the following campaign internals.

### State Internals

Do not read or write these directly from new UI code:

- `CampaignState._blocks`
- `CampaignState._forced_ddl_blocks`
- `CampaignState._active_temp_debuffs`
- `CampaignState.pending_block_id`
- `CampaignState.active_reward_context`
- `CampaignState._meeting_prompt_window`
- `CampaignState._meeting_enter_btn`
- `CampaignState._meeting_skip_btn`
- `CampaignState._input_locked`
- `CampaignState._input_lock_owner`
- `CampaignState._gossip_last_open_ms`
- `CampaignState._endturn_three_stage`
- `CampaignState._stage1_pinned_ids`

Rule:

- underscore-prefixed fields are migration internals, not UI contract

### Service Internals

The following services are not stable UI dependency points:

- `ThesisMetaService`
- `TrackBlockService`
- `CampaignMouseEventService`
- `ThesisSlice`

Reason:

- they still hold too much mixed responsibility
- they are valid refactor targets, not safe external contract

UI should not import these modules as if they were stable presentation APIs.

## Current Input Routing Rule

Until dedicated orchestration cutovers land, UI event ingress should follow this
path:

1. modal-first dispatch
2. input-lock guard
3. runtime UI event handling
4. keyboard/mouse/button/hover adapters
5. orchestration or transition seam

Practical rule:

- new UI work should plug into the existing event ingress through
  `CampaignState.handle_event(...)`
- new UI work should not call business services directly from random widget code

## Current Runtime Widget Rule

Runtime nodes/widgets are allowed to own:

- local presentation state
- local hover/open/close state
- local animation timing
- local hit-testing

Runtime nodes/widgets are not allowed to own:

- route resolution policy
- thesis submission rules
- reward sequencing
- transition payload wiring
- campaign save/load mutation

If a runtime widget needs to trigger business behavior, it should forward a
request into a host seam rather than mutate campaign internals directly.

## Contract For Parallel UI Work

When another developer works on campaign UI, the safe collaboration model is:

- treat `CampaignState` as the lifecycle host
- treat `CampaignView` and `ui_runtime` as presentation/runtime territory
- treat transition and turn advancement as orchestration territory
- avoid direct dependencies on underscore state fields
- avoid direct writes to `persistent` for state transitions
- avoid treating current hotspot services as stable UI APIs

## Immediate Follow-Up Cuts

This contract is the precondition for the next campaign handoff tasks.

The next highest-value cuts are:

1. `Campaign Event Input Split V1`
2. `Campaign Thesis Submission Flow Cut V1`
3. `Campaign Runtime UI Boundary V1`
4. `Campaign UI Handoff Tests V1`

These cuts should turn today's implicit boundaries into explicit ones.

## Decision Rule

When adding campaign-side code, ask:

1. Is this mainly drawing, local widget state, attachment, or interaction shell?
   - put it in `view`, `rendering`, `ui`, or `ui_runtime`
2. Is this mainly sequencing, transition policy, modal ownership, or business
   consequence?
   - keep it in orchestration/service/state seam territory
3. Does this require reading or writing underscore state fields from UI code?
   - stop and add a seam instead

## Current Status

This is a migration-phase contract, not a final architecture freeze.

It is good enough to support:

- parallel UI work
- campaign orchestration cutovers
- incremental runtime-node adoption

It is not a reason to stop refining the campaign interaction seams.
