# Campaign End Turn Orchestrator V1

## Goal

Give campaign UI one explicit end-turn request seam instead of letting
keyboard/button/mouse adapters choose their own turn-advance behavior.

## Why This Exists

Before this cut, campaign end-turn handling was split across multiple places:

- keyboard input could directly advance the turn
- the end-turn button could directly advance the turn
- the fish click path could start the staged sequence itself
- forced-DDL blocking lived in UI-facing adapters instead of one request owner

That worked, but it was not a safe handoff surface for a separate UI developer.

## Stable Seams

The V1 state-level seams are:

- `CampaignState.request_end_turn(staged=False)`
- `CampaignState.advance_campaign_turn()`

Rule:

- UI and event adapters should only request end-turn
- orchestration and staged-sequence internals may explicitly advance the turn

## Current Ownership

`CampaignEndTurnOrchestrator` now owns UI-facing end-turn request routing.

Its V1 behavior is:

- direct request:
  - block when forced DDL is active
  - otherwise advance immediately through `CampaignTurnOrchestrator`
- staged request:
  - delegate to `EndTurnService.start_single_click_staged_endturn()`

This keeps the request semantics in one place while preserving the existing
three-stage fish flow.

## Request Vs Advance

The important V1 distinction is:

- `request_end_turn(...)` means "the UI wants to end the turn"
- `advance_campaign_turn()` means "the orchestration layer is now actually
  moving the campaign turn forward"

That distinction matters because the staged fish flow is a request first, but
the real turn advance happens later after the animation/fusion sequence
stabilizes.

## UI Adapter Boundary

The current UI-facing adapters now behave like translators only:

- `CampaignKeyboardEventService`
- `CampaignUiButtonEventService`
- `CampaignMouseEventService`

They may decide whether the request is staged or direct.

They should not:

- re-check forced-DDL policy locally
- call `turn_orchestrator.advance_turn()` directly
- start mixed end-turn sequences on their own

## Internal Advancement Boundary

These internal flows may still perform actual advancement:

- `CampaignTurnOrchestrator`
- `EndTurnService`
- internal state-owned route resolution that is already past the UI request step

In V1, `CampaignState.end_turn()` remains as a compatibility wrapper, but it is
no longer the preferred UI-facing seam.

## Non-Goals

This cut does not:

- redesign the three-stage fish sequence
- rewrite DDL/fusion behavior
- remove all legacy turn helpers in one pass
- convert all campaign update timing into a new state machine

## Verification

V1 is currently protected by focused tests covering:

- direct request advancing when not forced
- direct request blocking under forced DDL
- staged request delegating to the staged end-turn service
- keyboard/button adapters forwarding into the request seam
- fish click forwarding staged request intent
- end-turn service using explicit internal advancement instead of UI request

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign Transition Request Contract V1`
