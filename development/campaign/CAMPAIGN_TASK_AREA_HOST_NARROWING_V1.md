# Campaign Task Area Host Narrowing V1

## Goal

Narrow the mature `Task Area` services that no longer need broad
`CampaignState` access, without building a fake universal facade over the whole
campaign shell.

This is a focused dependency cut, not a full aggregate rewrite.

## Problem

After the task-area boundary, write-path, and invariant passes, two services
were still depending on a wide `CampaignState` shape even though their real
needs were already small and stable:

- `contexts/campaign/services/line_bubble_service.py`
- `contexts/campaign/services/thesis_blueprint_app_service.py`

That made the boundary look looser than it really is and kept new task-area
logic coupled to shell internals by default.

## What Changed

### 1. `LineBubbleService` now depends on `LineBubbleHost`

The service now uses a narrow host that exposes:

- `manager`
- `view`
- `gossip_modal`
- `persistent`
- `current_turn`
- `get_campaign_blocks()`
- `lock_gossip_inputs()`
- `unlock_gossip_inputs()`

This cut removes the remaining direct dependency on:

- `state._blocks`
- `state.gossip_flow`
- `state._unlock_gossip_inputs`
- raw input-lock fields

### 2. `ThesisBlueprintAppService` now depends on `TaskAreaBlueprintHost`

The service now uses explicit task-area seams for:

- next task-line allocation
- blueprint write application
- thesis tier runtime reset
- thesis meta preparation
- saved-tier cleanup
- thesis meta snapshot persistence

This cut removes the remaining direct dependency on:

- `_ensure_thesis_meta(...)`
- ad hoc `_thesis_tier_map` cleanup via `CampaignSessionStore`

### 3. `CampaignState` grew only thin seam methods

Added seam methods:

- `lock_gossip_inputs()`
- `unlock_gossip_inputs()`
- `ensure_task_area_thesis_meta(...)`
- `clear_saved_thesis_tier_for_track(...)`

These are intent-level seams, not a new facade layer.

## Why These Cuts Were Worth It

- they already had stable behavior and stable vocabulary
- they reduced broad host coupling without hiding `TrackBlockService`
- they improved testability with small stub hosts
- they help the task-area boundary become executable instead of doc-only

## What We Explicitly Did Not Do

- no fake universal `CampaignStateHost`
- no protocol for `TrackBlockService`
- no full `Track` aggregate promotion
- no repository abstraction for task-area blocks

## Remaining Defer

Still not worth narrowing in this pass:

- `contexts/campaign/services/track_block_service.py`
  - still dominated by board geometry and mutation rules
- `contexts/campaign/services/thesis_meta_service.py`
  - still carries mixed migration-phase responsibilities

## Verification

Focused protection now includes:

- `tests/campaign/test_campaign_dependency_narrowing_services.py`
- `tests/campaign/test_task_area_invariants.py`
- `tests/campaign/test_task_area_write_path_contract.py`

## Current Bottom Line

`Task Area Host Narrowing V1` is complete when:

- mature task-area services no longer assume broad `CampaignState`
- the new host contracts stay smaller than the services they protect
- `TrackBlockService` remains intentionally broad until its own hotspot is
  smaller
