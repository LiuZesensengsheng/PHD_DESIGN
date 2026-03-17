# Campaign Orchestration Closure V1

## Goal

Mark the current campaign orchestration phase as closed enough for parallel UI
work, without pretending the whole campaign context has become a pure engine or
a fully modeled aggregate system.

- Level: `L3 Architecture`
- Date: `2026-03-17`

## What Is Closed

The following campaign-shell seams are now considered the stable orchestration
surface for this phase:

- startup and startup return flow
- block click routing
- end-turn request routing
- state transition requests for event / combat / meeting / ending
- modal lock ownership for blocking campaign modals
- thesis writing submission and publication follow-up entrypoints
- runtime-widget to shell boundary
- task-area write seams and task-area invariants

This means the default next step is no longer "continue cleaning orchestration".
The default next step is "build UI against the seams that now exist".

## Stable Seams

UI-safe shell entrypoints:

- `CampaignState.handle_clicked_block(block)`
- `CampaignState.request_end_turn(staged=False)`
- `CampaignState.request_event_block(block_id)`
- `CampaignState.request_combat_transition(...)`
- `CampaignState.request_meeting()`
- `CampaignState.request_ending(...)`
- `CampaignState.request_thesis_submission_for_writing_block(block)`
- `CampaignState.check_and_prompt_thesis_submission()`

Startup / return-flow owners:

- `CampaignStartupOrchestrator`
- `CampaignRouteResolutionService`
- `CampaignState.cleanup()` + startup snapshot hydration

Session-intent seams tightened in this closure pass:

- meeting handled-turn persistence now stops at a shell seam
- innovation placeholder choice persistence now stops at a typed session-store seam
- thesis combat-sync payload is now consumed through a one-shot seam instead of
  open-coded read + clear logic in a facade

## Current Invariants

The current closure assumes these executable invariants hold:

- startup plus cleanup preserve shell-owned runtime snapshot and handled meeting turns
- route-resolved transitions are consumed once, not replayed again after cleanup
- thesis combat-sync payload is applied once and then cleared
- combat transition requests do not mutate shell state when `encounter_id` is blank

These are now protected by focused tests rather than memory only.

## Deferred Hotspots

Still intentionally deferred in this phase:

- `contexts/campaign/services/thesis_meta_service.py`
- `contexts/campaign/services/track_block_service.py`
- `contexts/campaign/services/campaign_mouse_event_service.py`
- `contexts/campaign/services/thesis_slice.py` beyond the small session-access cleanup

Why defer:

- these files still carry mixed responsibilities or geometry-heavy rules
- the current product need is safer UI collaboration, not maximum purity
- reopening them broadly now would likely increase churn more than confidence

See also:

- `docs/development/CAMPAIGN_HOTSPOT_DEFER_LIST_V1.md`
- `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
- `docs/development/TRACK_AGGREGATE_REEVALUATION_V1.md`

## Reopen Triggers

Reopen campaign orchestration only when one of these becomes true:

- a new UI path cannot be expressed through the existing state-level seams
- a service starts duplicating session/persistent write rules again
- a new combat-entry path needs encounter validation beyond the current request contract
- task-area writers start needing stronger lane identity or shared local invariants
- a deferred hotspot gains new business branches, not just presentation edits

If none of those triggers appears, prefer UI work or content work over another
architecture pass.

## UI Boundary

The intended collaboration split after this document:

- UI work should stay in `ui/`, `ui_runtime/`, `rendering/`, `view`, and thin
  event adapters
- UI work should stop at state-level intent seams and runtime-widget local logic
- UI should not directly mutate shell internals, raw transition payloads, or
  session-store details

## Bottom Line

Campaign orchestration is not "perfectly engineized".

It is now stable enough that further broad orchestration work is lower priority
than building UI on top of the seams already cut. Future architecture changes
should be trigger-driven and local, not another open-ended cleanup phase.
