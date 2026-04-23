# Campaign Lifecycle Read Surface V1

## Problem

Campaign lifecycle now has explicit runtime result contracts for:

- turn loop
- return resolution

But reading lifecycle state still required callers to inspect several separate
machine fields:

- `current_phase`
- `last_turn_cycle_result`
- `last_return_resolution_result`

That meant the write-side contracts were explicit, but the read-side surface was
still scattered.

## Constraints

- Keep the work inside `contexts/campaign/**`.
- Do not replace the existing result contracts.
- Do not widen into:
  - lifecycle persistence
  - startup-phase migration
  - UI-specific state projection

## Complexity

### Essential Complexity

The lifecycle machine genuinely has:

1. current runtime phase
2. possibly active runtime step
3. the latest turn-loop outcome
4. the latest return-resolution outcome

Those are real read concerns and should be surfaced together.

### Accidental Complexity

The accidental complexity came from making every reader reconstruct one
snapshot-like view by manually touching multiple machine fields.

## Options

### Option A: Keep Reading Machine Fields Directly

What it means:

- callers keep reading `current_phase` and `last_*_result` separately

Pros:

- zero code change

Cons:

- keeps lifecycle reads fragmented
- encourages more ad-hoc reconstruction logic

### Option B: Add One Unified Lifecycle Snapshot Surface

What it means:

- add `CampaignLifecycleSnapshot`
- expose it through `CampaignLifecycleMachine.snapshot()`
- mirror it through `CampaignState.snapshot_campaign_lifecycle_state()`

Pros:

- one explicit read model
- preserves existing result contracts
- cheap and low-risk

Cons:

- adds one more lifecycle contract type
- duplicates a small amount of summary data from the underlying results

## Risks

### Risk If We Stay Scattered

- external readers will keep rebuilding slightly different lifecycle state
  projections
- future UI/runtime code may drift into peeking at machine internals directly

### Risk If We Over-Build

- a richer read model could start duplicating too much domain/runtime state
- lifecycle reads could get mistaken for a persistence schema

## Recommendation

Choose **Option B**.

Current V1 read surface:

- `CampaignLifecycleMachine.snapshot()` now returns
  `CampaignLifecycleSnapshot`
- `CampaignState.snapshot_campaign_lifecycle_state()` mirrors that read surface
  at the shell host

Current snapshot fields:

- `current_phase`
- `active_step`
- `turn_cycle_status`
- `turn_cycle_blocking_step`
- `turn_cycle_turn_advanced`
- `return_resolution_status`
- `return_resolution_opened_reward_id`
- `return_resolution_turn_advanced_count`

Current convenience properties:

- `turn_idle_entered`
- `interrupt_blocked`
- `has_return_transitions`
- `return_reward_opened`

Important boundary:

- the snapshot is a **read surface**
- the detailed lifecycle result contracts still remain the source for richer
  per-run inspection

## Counter-Review

Why not just read the result objects directly everywhere?

- because the most common lifecycle reads are summary reads, not full forensic
  reads
- the snapshot removes repetitive boilerplate without deleting the detailed
  contracts

Why mirror the read surface on `CampaignState` too?

- because campaign shell callers often already work through explicit state-level
  seams
- it avoids forcing every reader to know whether the lifecycle machine itself
  should be touched directly

This recommendation depends on one assumption:

- the project still prefers small explicit contracts over one large generalized
  campaign runtime state object

## Decision Summary

1. Lifecycle write contracts alone are not enough; lifecycle reads should also
   have one explicit surface.
2. The read surface should be a lightweight snapshot, not a new heavy runtime
   aggregate.
3. `CampaignLifecycleMachine.snapshot()` is the canonical lifecycle read owner.
4. `CampaignState.snapshot_campaign_lifecycle_state()` is an acceptable shell
   host seam for callers that already depend on campaign-state entrypoints.
