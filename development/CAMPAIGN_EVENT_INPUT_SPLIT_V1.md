# Campaign Event Input Split V1

## Goal

Further separate campaign event adapters from campaign input orchestration so
mouse/button/keyboard services mainly translate pygame events into intent
requests instead of continuing to own small business/UI-flow rules.

## Why This Exists

After block-click, end-turn, transition, and startup cleanup, event adapters
were still carrying several input-side behaviors directly:

- gossip debounce/open rules
- idea modal open requests
- meeting prompt enter requests
- choice-toggle modal opening
- line-bubble press forwarding

These are smaller than block-click routing, but they still blur the adapter
boundary if they stay embedded in raw pygame-event services.

## Stable Input Seams

The current state-level input seams are now:

- `CampaignState.request_gossip_entry()`
- `CampaignState.request_gossip_entry_debounced(now_ms=...)`
- `CampaignState.request_idea_selection()`
- `CampaignState.request_meeting_entry()`
- `CampaignState.request_choice_toggle()`
- `CampaignState.request_line_bubble_press(ui_element)`

Rule:

- event adapters may call these seams
- event adapters should not re-implement the associated mini-flows locally

## Current Ownership

`CampaignEventInputOrchestrator` now owns these non-block-click,
non-turn-advance input intents.

Its V1 responsibilities are:

- gossip open debounce
- gossip entry request forwarding
- idea-selection request forwarding
- meeting-enter request forwarding
- persistent choice-toggle modal request
- line-bubble press forwarding

## Adapter Boundary

The event adapters still own:

- raw pygame event type filtering
- hit testing against concrete UI elements
- local event-to-intent translation
- click sound / low-latency interaction shell behavior

They no longer need to own the associated input mini-flows themselves.

## Examples

### Mouse

`CampaignMouseEventService` now:

- detects gossip button hit
- translates it into `request_gossip_entry_debounced(...)`

It no longer owns the debounce rule itself.

### UI Button

`CampaignUiButtonEventService` now:

- translates meeting-enter button into `request_meeting_entry()`
- translates gossip button into `request_gossip_entry_debounced(...)`
- translates idea button into `request_idea_selection()`
- translates choice-toggle button into `request_choice_toggle()`
- translates line-bubble press into `request_line_bubble_press(...)`

### Keyboard

`CampaignKeyboardEventService` now:

- translates `F8` / `I` into `request_idea_selection()`
- translates `G` into `request_gossip_entry()`

## Non-Goals

This cut does not:

- remove all `self.state.*` usage from event services
- rewrite hit-test math
- redesign line-bubble UI behavior
- fold every event path into one giant input state machine

## Verification

V1 is currently protected by focused tests covering:

- event-input orchestrator debounce and delegation behavior
- mouse gossip/deck/block-click delegation
- UI button gossip/deck/end-turn/meeting delegation
- keyboard idea/gossip/dev-combat delegation

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign Thesis Submission Flow Cut V1`
