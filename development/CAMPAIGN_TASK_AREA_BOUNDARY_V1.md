# Campaign vs Task Area Boundary V1

## Goal

Clarify the architectural split between:

- `Campaign` as the outer shell
- `Task Area` (also called the Gantt area) as the campaign's scheduling subdomain

This is a decision-prep design document, not a full rewrite plan.

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Problem

The repository already implies two different concepts, but the current runtime
still blends them together:

- the whole campaign shell
- the task board / task lines / blocks / event bubbles

Current evidence:

- `contexts/campaign/state.py` owns lifecycle, transitions, modal/input state,
  startup, and also the `_blocks` list
- `contexts/campaign/domain/block_dto.py` is the real runtime shape for
  schedulable blocks
- `contexts/campaign/services/track_block_service.py` owns most board mutation
  rules such as normalization, fusion, DDL snake, compaction, and actionable
  block detection
- design docs already distinguish `Task Block` from `Event Bubble`, and
  distinguish task lines from the full campaign shell

That mismatch creates three problems:

1. UI and future orchestration work do not have a stable vocabulary.
2. `CampaignState` risks becoming the dumping ground for both shell logic and
   task-board rules.
3. It is hard to tell whether a change belongs to campaign lifecycle, task
   scheduling, thesis-specific rules, or pure presentation.

## Constraints

- Keep the current direction: `Godot-ization inside pygame`, not a one-shot
  engine rewrite.
- Preserve the newly finished `Campaign UI Handoff` contract; do not reopen the
  UI safety surface without a concrete trigger.
- Do not force a full DDD aggregate rewrite just because the naming is messy.
- Respect the current hotspot guidance:
  - `TrackBlockService` is still geometry-heavy and should not be hidden behind
    a wide fake facade yet.
  - UI should not depend on `TrackBlockService` directly.
- Incremental evolution is preferred over deep structural churn.

## Complexity

### Essential Complexity

- `Campaign` shell complexity:
  - state-machine transitions
  - startup / restore / return flow
  - modal ownership and input lock
  - cross-context requests such as combat, event, deck, meeting, ending

- `Task Area` complexity:
  - tracks / task lines
  - blocks and their board geometry
  - DDL snake, fusion, normalization, compaction
  - actionable-today detection
  - line-bubble anchoring and task-area overlays

- specialization complexity:
  - thesis is not the whole task area
  - thesis is a specialized rule layer that happens to use task-area tracks and
    blocks

### Accidental Complexity

- naming drift between `campaign`, `gantt`, `track`, `task line`, `line bubble`,
  `event`, and `block`
- `CampaignState._blocks` acting as both shell-owned storage and task-area data
- old design language and current runtime names not being mapped explicitly
- some services mixing task-board geometry with rule mutation

## Options

### Option A: Keep The Current Runtime And Only Add Informal Vocabulary

What it means:

- do not define a formal `Task Area` boundary
- keep talking about campaign, gantt, track, and task interchangeably
- postpone the distinction until a later refactor

Pros:

- lowest short-term effort
- no migration work now

Cons:

- keeps ownership blurry for new UI and orchestration work
- makes future task-board seams harder to cut cleanly
- increases the chance that task rules leak back into shell or UI code

### Option B: Define `Task Area` As An Explicit Campaign Subdomain Now

What it means:

- `Campaign` remains the outer shell and host
- `Task Area` becomes the named scheduling subdomain inside campaign
- current runtime shape can stay mostly as:
  - `CampaignState` as host
  - `BlockDTO` / `Block`
  - `_blocks`
  - `TrackBlockService`
  - visible-block and line-bubble services
- we clarify ownership now, then evolve the write paths in small cuts later

Pros:

- gives the team a stable vocabulary immediately
- matches both the existing docs and the real runtime shape
- helps future UI work stop at the right seam
- avoids a premature full aggregate rewrite

Cons:

- still relies on migration-phase shapes such as `_blocks`
- does not by itself solve the `TrackBlockService` hotspot
- requires follow-up cuts or the boundary stays "doc only"

### Option C: Do A Full Track Aggregate Rewrite Now

What it means:

- promote `Track` / `Lane` / `Block` into explicit aggregates immediately
- move all task-area writes behind one track service or repository surface
- aggressively narrow or replace current state-level block mutation paths

Pros:

- strongest DDD purity
- most explicit write-path ownership
- best long-term engine-like model if it succeeds

Cons:

- highest cost and migration risk
- not necessary for safe UI collaboration right now
- likely to create a long-lived dual model while current services are still
  mixed between geometry and business logic
- premature before the task-area writers and invariants are narrower

## Risks

### If We Stay Too Loose

- `CampaignState` keeps absorbing both shell work and task-board rules
- UI developers may treat block storage or board services as the contract
- thesis-specific logic may keep masquerading as generic task-area behavior

### If We Over-Correct Too Early

- we may build a fake aggregate layer over still-unclear board mutation rules
- a large rewrite could slow content and UI iteration without improving safety
- we may accidentally duplicate the same logic across old and new task-board
  paths

### Specific Risk To Watch

- `track_index` is currently both geometry identity and a proxy for business
  grouping
- if later features need stronger identity than `track_index`, the next cut
  should introduce an explicit task-line identity instead of widening
  `CampaignState`

## Recommendation

Choose **Option B**.

Define the architecture like this:

### 1. `Campaign` = Outer Shell

`Campaign` should own:

- lifecycle and startup
- modal/input lock ownership
- cross-state transition requests
- persistent/session integration
- top-level progression and return handling

Current modules that fit the shell:

- `contexts/campaign/state.py`
- `contexts/campaign/services/transition_helper.py`
- campaign startup, modal, input, and end-turn orchestrators

### 2. `Task Area` = Campaign Scheduling Subdomain

`Task Area` should own:

- task lines / tracks
- schedulable blocks
- board stabilization rules
- DDL snake and fusion
- visible-board projection inputs
- line-bubble placement and task-area overlays

Current modules that fit the task area:

- `contexts/campaign/domain/block_dto.py`
- `contexts/campaign/services/track_block_service.py`
- `contexts/campaign/services/campaign_visible_blocks_service.py`
- `contexts/campaign/services/line_bubble_service.py`

Important point:

- `Task Area` is **inside** campaign
- it is **not** a sibling state machine
- it is **not** the same thing as the whole campaign

### 3. `Track` / `Task Line` = A Lane Inside Task Area

Use this vocabulary:

- `Task Area` = the full central scheduling board
- `Task Line` or `Track` = one lane inside that board

For now, `track_index` remains the runtime identity for those lanes.

### 4. `Block` = Schedulable Unit

`Block` means the board unit that participates in:

- timing
- geometry
- fusion
- DDL pressure
- actionable-today checks

That maps directly to `BlockDTO` / `Block`.

### 5. `Event Bubble` = Overlay, Not Block

`Event Bubble` should be treated as:

- a task-area overlay anchored to a task line
- not part of block geometry
- not part of fusion
- not a replacement for task blocks

This matches the existing design docs and keeps line-bubble behavior from being
mis-modeled as block mutation.

### 6. `Thesis` = Specialized Policy Layer On Top Of Task Area

`Thesis` is not the same thing as `Task Area`.

Instead:

- thesis rules use task-area tracks and blocks
- thesis services add specialized progression, meta, verdict, and publication
  semantics
- that specialization should not force the entire task board to be modeled as a
  thesis-specific aggregate

### Working Ownership Rule

When a new change is mainly about:

- transitions, startup, modal/input ownership, return flow:
  - it belongs to `Campaign` shell
- tracks, blocks, DDL/fusion, line-bubble anchoring, board invariants:
  - it belongs to `Task Area`
- local animation, widget trees, presentation-only hit-testing:
  - it belongs to UI / runtime presentation

## Counter-Review

Why not jump directly to the full aggregate rewrite now?

- the current task-board hotspot is still dominated by geometry and mutation
  rules, not by a missing repository abstraction
- the new UI handoff work no longer needs that big rewrite to proceed safely
- the current write paths are not narrow enough yet to make a full aggregate cut
  cheap or obvious

Why is this recommendation still worth doing now?

- it removes naming ambiguity immediately
- it gives follow-up refactors a cleaner target
- it reduces the chance of another "campaign means everything" architecture pass

This recommendation depends on one assumption:

- the team is willing to follow this document with a few small task-area seam
  cuts, rather than treating it as a final abstraction by itself

## Decision Summary

1. `Campaign` should be treated as the outer shell and lifecycle host.
2. `Task Area` should be treated as a named scheduling subdomain inside
   campaign.
3. `Track` / `Task Line` is one lane inside `Task Area`.
4. `Block` is the schedulable unit in that subdomain.
5. `Event Bubble` is a task-area overlay, not a block.
6. `Thesis` is a specialized rule layer on top of task-area primitives, not the
   definition of the whole board.
7. We should **not** do a full track aggregate rewrite now.
8. The next practical step is small task-area boundary tightening, not a
   campaign-wide rewrite.

## Suggested Follow-Up Cuts

1. `Task Area Terminology Alignment V1`
   - add a small terminology note near the current runtime files and docs
   - stop using `campaign` and `task area` interchangeably

2. `Task Area Write-Path Contract V1`
   - identify which block mutations are task-area writes
   - make those writes explicit at the state seam before deeper refactors

3. `Task Area Invariant Tests V1`
   - protect no-overlap, trailing DDL, fusion safety, and bubble-vs-block
     separation with focused tests

4. `Task Area Host Narrowing V1`
   - narrow the mature task-area services away from broad `CampaignState`
     access where ROI is clear

5. `Track Aggregate Re-evaluation V1`
   - only after the previous cuts land, decide whether a full `Track` aggregate
     is now worth the cost
