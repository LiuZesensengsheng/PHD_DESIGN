# CampaignState Strangler V1

## Problem

`CampaignState` is already thinner than it was during the earlier campaign
cleanup lines, but it is still the place where too many migration-phase seams
meet:

- stable UI-facing request seams
- shell lifecycle and transition hosting
- task-area runtime writes
- thesis checkpoint and submission rollback writes
- trigger-surface snapshot and restore hosting
- one remaining review-next direct alias: `hit_test_service`

The current goal is not to make campaign pure. The goal is to reach an
80-point architecture baseline during the refactor season by moving the next
few explicit write paths and transitional seams out of `CampaignState` without
opening UI, rendering, or broad thesis/task-area redesign.

Level: `L3 Architecture`

Date: `2026-05-12`

## Constraints

- Keep `CampaignState` as the outer shell host.
- Keep stable request seams on `CampaignState` for UI and state-machine callers.
- Stay inside:
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/**`
  - `contexts/campaign/domain/**`
  - `contexts/campaign/lifecycle/**`
  - `tests/campaign/**`
  - campaign docs/logs
- Do not touch:
  - `contexts/campaign/view.py`
  - `contexts/campaign/rendering/**`
  - `contexts/campaign/ui_runtime/**`
  - `cardanalysis` / `combat_analysis`
- Do not reopen:
  - broad thesis/task-area redesign
  - physical service taxonomy migration
  - a generic campaign aggregate or facade layer
- Old pre-alpha saves may be treated aggressively, but save schema changes do
  not belong in this line.

## Complexity

### Essential Complexity

Campaign still needs one shell that coordinates pygame state lifecycle, modal
state, route transitions, turn progression, and UI-facing request seams. Some
methods on `CampaignState` are therefore real host seams, not accidental
compatibility layers.

The essential work is to separate:

1. shell seams that should stay callable from UI/state-machine code
2. write paths that can move behind a narrower service owner
3. review-next aliases that are still direct only because no one has cut the
   local seam yet

### Accidental Complexity

The accidental complexity is that older cleanup lines left several different
kinds of methods sitting next to each other in `state.py`, making all of them
look equally permanent:

- `hit_test_service` is a review-next direct alias, not a stable shell port.
- thesis write/submission checkpoints are business rollback write paths, not
  shell lifecycle methods.
- trigger snapshot/restore methods are lifecycle support seams, but their
  internal storage belongs to the interaction trigger services.
- some private helpers remain only as compatibility call targets for current
  services.

## Options

### Option A. Stop After Boundary Hardening

Keep the current campaign state shape and wait for feature pressure before
touching it again.

Pros:

- lowest immediate risk
- avoids churn while campaign behavior is stable

Cons:

- leaves the only review-next direct alias in place
- keeps rollback/checkpoint write paths hosted in the shell
- makes future agents re-read older cleanup docs to decide what is still live

### Option B. Run A Narrow Strangler Pass

Move one explicit write path or review-next seam per slice while preserving the
shell host surface.

Pros:

- targets the remaining concrete architecture drag
- fits the current content-free refactor window
- keeps UI and product behavior stable
- gives automation a small ordered backlog

Cons:

- does not make the campaign context perfectly pure
- still leaves broad thesis and task-area hotspots until a real trigger appears
- requires discipline not to turn each small seam into a new protocol family

### Option C. Reopen Broad Campaign Purification

Use the refactor window to split `CampaignState`, thesis, task-area, services,
and directory taxonomy in one larger pass.

Pros:

- could reduce more surface area if everything lands cleanly

Cons:

- high churn and weak rollback story
- likely touches UI or rendering by accident
- conflicts with the 80-point target and the user's UI-review constraint
- risks adding abstractions to remove abstractions

## Risks

- If the pass is too timid, the project keeps the current broad shell longer
  than necessary and later agents keep adding to it.
- If the pass is too ambitious, it reopens thesis/task-area redesign or UI
  runtime work without human visual review.
- If every seam becomes a new `Protocol`, the project trades one kind of
  over-abstraction for another.
- If request seams are removed instead of narrowed internally, UI and
  state-machine callers lose the stable surface created by earlier work.

## Recommendation

Choose **Option B**.

Run `CampaignState Strangler V1` as a small-slice execution line inside the
architecture refactor season. The pass should stop at the 80-point baseline,
not at theoretical purity.

### Slice Order

1. **Plan freeze**
   - add this document as the source of truth
   - update task pool, decision log, and daily log
   - no runtime behavior change

2. **Review-next hit-test seam**
   - remove `hit_test_service` as a direct `CampaignState` alias if the local
     mouse-click seam can stay contained
   - prefer an explicit state/service method over a broad host protocol
   - validation: mouse event, interaction sequence, and service-bundle guardrail
     tests
   - status: completed on `2026-05-12`; callers now use
     `find_clicked_campaign_block(...)`

3. **Thesis write checkpoint owner**
   - move capture/restore logic for thesis write rollback out of raw
     `CampaignState` method bodies
   - keep the state-level seam if current callers need it
   - validation: thesis write-path and self-refactor guardrail tests
   - status: completed on `2026-05-12`; `CampaignState` now delegates write
     checkpoint capture/restore to `ThesisWriteCheckpointService`

4. **Thesis submission checkpoint owner**
   - move submission rollback extras out of raw `CampaignState` method bodies
   - keep submission flow behavior unchanged
   - validation: thesis submission, thesis write-path, and campaign guardrail
     tests
   - status: completed on `2026-05-12`; `CampaignState` now delegates
     submission checkpoint capture/restore to `ThesisSubmissionCheckpointService`

5. **Trigger snapshot/read seam review**
   - consolidate trigger snapshot/restore host behavior only if it can reduce
     shell code without bypassing lifecycle host seams
   - do not let lifecycle steps import trigger services directly
   - validation: trigger surface/reaction, turn orchestrator, lifecycle
     guardrail, and contract smoke tests
   - status: completed on `2026-05-12`; `CampaignState` now delegates combined
     trigger/reaction/forced-event clear and checkpoint shape to
     `CampaignTriggerCheckpointService`

6. **80-point stop review**
   - run `py -3.11 -m pytest tests/campaign -q`
   - update docs with what remains intentionally deferred
   - stop before content-pack work unless the pass is clean and committed

### Explicit Non-Targets

- no `CampaignView` work
- no runtime UI extraction
- no reward/meeting/forced-event platform unification
- no `thesis_slice` broad rewrite without a writer/identity trigger
- no `track_block_service` aggregate rewrite without task-area product pressure
- no file-length or touch-count hard gates

## Counter-Review

Why not delete more `CampaignState` seams now?

- several state methods are intentionally stable host seams for UI, lifecycle,
  and transition callers; deleting them would reduce clarity rather than
  abstraction.

Why touch thesis checkpoints if thesis hotspot cleanup is deferred?

- checkpoint capture/restore is a bounded write path with existing tests. It
  can move without redesigning thesis judgment, publication, or task-area rules.

Why not make a generic `CampaignHost` protocol first?

- the project has already seen enough over-abstraction pressure. Add or narrow
  host contracts only when a specific service loses broad state access and the
  replacement surface is smaller than the code it protects.

Why is this worth doing before content-pack work?

- it removes the remaining campaign shell ambiguity while the project is in a
  short content-free refactor window, and it gives future content/runtime work a
  clearer campaign host to build on.

## Decision Summary

1. `CampaignState Strangler V1` is a narrow execution line, not a campaign
   rewrite.
2. `CampaignState` remains the shell host and keeps stable request seams.
3. Each slice moves one write path or review-next seam.
4. `hit_test_service` direct alias removal is complete; thesis checkpoints and
   trigger snapshot/read hosting are the next review targets.
5. UI/runtime rendering stays queued for human visual review.
6. After 3-5 implementation slices, pause and review before continuing toward
   content-pack work.
