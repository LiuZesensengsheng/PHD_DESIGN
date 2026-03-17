# Campaign Task Area Write-Path Contract V1

## Goal

Make the current `Task Area` write paths explicit so callers stop open-coding
board mutation from multiple places.

This is a migration-step contract, not a full aggregate rewrite.

## Problem

After the `Campaign vs Task Area Boundary V1` clarification, the next risk is
not vocabulary drift but write-path drift.

Before this cut, some task-area writers were still open-coding patterns like:

- compute next track index from `_blocks`
- call `TrackService.apply_blueprint(...)`
- assign back into `_blocks`
- manually call stabilization helpers

That pattern existed in more than one place, which made future tightening
harder.

## Contract

### Preferred Task-Area Write Seams On `CampaignState`

Use these state seams for external task-area writes:

- `build_campaign_block(...)`
  - construct a task-area block from explicit fields
- `allocate_campaign_block_id()`
  - allocate ids for new task-area blocks
- `restore_campaign_runtime(current_turn, blocks)`
  - restore a full task-area snapshot during hydration
- `replace_campaign_blocks(blocks)`
  - replace the full task-area block list when the caller already owns the full
    replacement result
- `stabilize_campaign_board()`
  - run normalization, trailing-DDL enforcement, and encounter-id backfill
- `get_next_task_area_track_index()`
  - compute the next task-line index without open-coding `_blocks` scanning
- `apply_task_area_blueprint_plans(plans)`
  - preferred seam for appending generated blueprint plans onto the current
    task-area board

### Thesis-Specific Mutation Seams

Do not route thesis-local block removal through generic list mutation.

Use:

- `state.thesis_blocks.activate_review_chain_for_round(...)`
- `state.thesis_blocks.activate_next_dormant_round(...)`
- `state.thesis_blocks.remove_round_blocks(...)`
- `state.thesis_blocks.remove_blocks_by_id(...)`

These are specialized write seams on top of task-area primitives.

## What Changed In This Cut

The following writers now use explicit task-area seams instead of mutating
`_blocks` directly:

- `contexts/campaign/services/thesis_blueprint_app_service.py`
  - now uses `get_next_task_area_track_index()`
  - now uses `apply_task_area_blueprint_plans(plans)`
- `contexts/campaign/services/campaign_keyboard_event_service.py`
  - the `F7` dev blueprint path now uses the same seams

## Internal Writers That Stay Internal For Now

These mutations remain internal implementation details for now:

- `TrackBlockService`
  - owns task-area board algorithms such as fusion and DDL snake
- `EndTurnService`
  - still performs staged in-sequence fusion writes as part of its runtime flow
- `ThesisBlockMutationService`
  - owns thesis-local block removal and dormant-round activation

The rule is:

- external app-service writers should prefer state seams
- internal board algorithms may still mutate the hosted list directly until
  their own seam extraction becomes worth it

## Stop Signs

Do not add new external writers that:

- assign `state._blocks = ...` after `TrackService.apply_blueprint(...)`
- compute next track indices by open-coding `_blocks` scans
- call `_normalize_no_overlap()` and `_ensure_last_block_is_ddl_per_track()`
  directly from outer app services when `stabilize_campaign_board()` or
  `apply_task_area_blueprint_plans(...)` already covers the intent

## Current Bottom Line

The current V1 contract is:

- task-area writes may still be hosted by `CampaignState`
- but repeated external write patterns should be funneled through explicit
  state seams
- full aggregate promotion can wait until the remaining internal writers are
  narrower and more stable
