# Campaign Transition Request Contract V1

## Goal

Define one stable transition-request surface for campaign so UI-facing code can
ask for deck/event/combat/meeting/ending transitions without assembling payload
dicts or mutating `persistent` directly.

## Why This Exists

Before this cut, campaign transition requests were partly centralized but still
inconsistent:

- some UI adapters called `state.tx.*` directly
- meeting prompt entered `MEETING` by passing the whole `persistent` object
- some services set `pending_block_id` themselves before requesting transition
- some combat transitions built raw payload dicts instead of reusing one seam

That made the transition boundary harder to explain and riskier for parallel UI
work.

## Stable UI-Facing Seams

The V1 state-level transition request seams are:

- `CampaignState.request_deck_view()`
- `CampaignState.request_event_block(block_id)`
- `CampaignState.request_combat_block(block_id, encounter_id)`
- `CampaignState.request_dev_combat(encounter_id)`
- `CampaignState.request_meeting()`
- `CampaignState.request_ending(trigger_reason, extra=...)`

Rule:

- UI-facing code should call these state seams
- UI-facing code should not call `state.tx.*` directly
- UI-facing code should not pass raw transition payloads into
  `request_state_change(...)`

## Payload Ownership

`TransitionHelper` remains the payload-shape owner.

It now centralizes:

- `to_deck()`
- `to_event(block_id)`
- `to_combat(block_id=None, encounter_id=..., final_combat_reason=..., ...)`
- `to_combat_dev(encounter_id)`
- `to_meeting()`
- `to_ending(trigger_reason, extra=...)`

Shared contract helpers in `contexts/shared/domain/contracts.py` still define
the persistent payload format for:

- `pending_block_id`
- `start_combat_encounter_id`
- `final_combat_reason`
- `ending_payload`

## Current Payload Rules

### Deck

- request seam: `request_deck_view()`
- payload rule: no extra payload required

### Event

- request seam: `request_event_block(block_id)`
- payload rule: `pending_block_id` must be set through the helper contract

### Combat

- request seams:
  - `request_combat_block(block_id, encounter_id)`
  - `request_dev_combat(encounter_id)`
  - internal `request_combat_transition(...)`
- payload rule:
  - `start_combat_encounter_id` is required
  - `pending_block_id` is optional
  - `final_combat_reason` is optional but contract-owned

### Meeting

- request seam: `request_meeting()`
- payload rule: no raw `persistent` pass-through

### Ending

- request seam: `request_ending(trigger_reason, extra=...)`
- payload rule:
  - ending payload is built by the ending service
  - campaign stores the same payload under `ENDING_PAYLOAD`
  - request data must stay contract-shaped rather than ad-hoc

## Startup Return Path

Route-return handling remains owned by `CampaignRouteResolutionService`.

Its V1 rule is:

- consume route-resolved transitions from the shared queue
- resolve returned campaign blocks through `CampaignState.resolve_returned_route_block(...)`
- keep reward-open follow-up data separate from the transition request surface

That means startup return flow is still contract-backed rather than relying on
legacy one-off runtime keys.

## Internal Producer Rule

Not every campaign-internal service needs to call the public state seams, but
every transition producer should still use contract-owned request builders.

Current examples:

- thesis judgment combat entry now goes through state combat request seam
- graduation-defense combat entry now goes through the same combat transition
  contract instead of raw payload assembly
- meeting prompt now requests `MEETING` through a dedicated seam instead of
  passing all of `persistent`

## Non-Goals

This cut does not:

- redesign the whole game state machine
- remove `TransitionHelper`
- force every internal service into one generic transition API
- replace the route-resolved transition queue

## Verification

V1 is currently protected by focused tests covering:

- helper payload shape for event/combat/meeting/ending
- state request seams for event/combat/meeting
- UI deck/dev-combat adapters delegating through state request seams
- meeting prompt using the meeting request seam
- thesis event/judgment flows delegating through transition request seams
- startup route-resolution contract remaining intact

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign Startup Seam Cleanup V1`
