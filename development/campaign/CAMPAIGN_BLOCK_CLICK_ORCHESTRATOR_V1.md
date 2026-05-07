# Campaign Block Click Orchestrator V1

## Goal

Move campaign block-click business routing out of the raw mouse event adapter
and into one explicit orchestration seam.

## Why This Exists

Before this cut, `CampaignMouseEventService` still mixed:

- click adaptation
- canvas/hit-test/view math
- block branch ordering
- transition requests
- thesis and DDL click consequences

That made the mouse event service both UI-facing and business-facing at the
same time.

## Stable Seam

The current host seam is:

- `CampaignState.handle_clicked_block(block)`

UI/event adapters may forward a resolved block click into this seam.

They should not re-implement block-type branch ordering locally.

## Current Ordering

`CampaignBlockClickOrchestrator.handle_clicked_block(...)` now owns this order:

1. DDL block
2. thesis DDL vs main DDL split
3. non-combat helper path
4. combat transition path
5. event transition path
6. no-transition fallback

Important behavior preserved in V1:

- thesis DDL still activates temporary DDL pressure before judgment flow
- combat click still requires a resolved `encounter_id`
- event click still delegates through the existing thesis/event seam
- non-combat helper still gets first refusal before combat/event branch logic

## UI Adapter Boundary

`CampaignMouseEventService` still owns:

- raw mouse-event adaptation
- gossip button click
- deck/inspiration click shortcuts
- end-turn fish click
- screen-to-canvas conversion
- click effects
- block hit-testing

It no longer owns the main block-click business branch tree.

## Non-Goals

This cut does not:

- rewrite hit-test math
- redesign block DTOs
- fully refactor thesis flow internals
- remove all `CampaignState` compatibility helpers in one pass

## Verification

V1 is protected by focused tests covering:

- thesis DDL routing
- main DDL routing
- non-combat-before-combat ordering
- combat transition request wiring
- missing encounter guard
- event-path delegation
- mouse-event layer delegation into the block-click seam

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign End Turn Orchestrator V1`
