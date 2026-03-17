# Track Aggregate Re-evaluation V1

## Problem

After the `Campaign vs Task Area Boundary V1`, task-area write-path tightening,
invariant tests, and host narrowing work, we need to decide whether the next
step should be a true `Track` aggregate rewrite or whether the current
`Task Area` model should stay incremental.

The question is no longer theoretical. We now have:

- clearer vocabulary around `Campaign` vs `Task Area`
- explicit task-area write seams on `CampaignState`
- executable invariants around overlap, trailing DDL, and bubble-vs-block
- narrower host contracts for mature task-area services

That makes this the right checkpoint to ask whether a full `Track` aggregate is
worth doing now.

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Constraints

- Keep the current project direction: architecture migration before engine
  migration.
- Do not reopen the safe UI-handoff surface without a concrete new trigger.
- Do not hide `TrackBlockService` behind a fake purity layer.
- Preserve current content iteration speed on the task board.
- Prefer small explicit seams over a long-lived dual model.

## Complexity

### Essential Complexity

- `TrackBlockService` still owns real board geometry behavior:
  - no-overlap normalization
  - DDL snake
  - fusion
  - compaction
  - actionable-today checks
- `CampaignState` still hosts the live task-area runtime list and the runtime
  turn clock.
- thesis remains a specialized policy layer on top of task-area primitives, not
  a replacement data model for them.

### Accidental Complexity

- `track_index` currently carries both lane identity and geometry grouping
- some task-area reads still live on shell-owned storage (`_blocks`)
- the task-area hotspot is still mixed between geometry policy and mutation
  policy
- a premature aggregate cut would likely duplicate the current runtime shape
  before it replaces it

## Options

### Option A: Keep The Current Incremental Task Area Model

What it means:

- keep `CampaignState` as the host of the task-area runtime list
- keep `TrackBlockService` as the main board-rule owner
- continue only with narrow seam cuts when a concrete pain point appears

Pros:

- lowest migration cost
- no dual model pressure right now
- matches the newly landed write-path and host-seam work
- keeps UI-safe boundaries intact

Cons:

- `track_index` remains a weak identity
- task-area rules are still service-centric rather than aggregate-centric
- some future changes may still have to reason about raw hosted blocks

### Option B: Promote A True `Track` Aggregate Now

What it means:

- introduce an explicit `Track` runtime model as the main write owner
- move task-area mutation behind track-owned methods or repositories
- stop treating the hosted block list as the main runtime source

Pros:

- strongest ownership story
- clearer lane-level write rules in the long term
- better fit if task-line identity and cross-lane rules become richer

Cons:

- highest migration cost
- likely creates an awkward dual model while `TrackBlockService` still owns the
  real board math
- would force multiple runtime and test rewrites before there is strong product
  pressure for them

### Option C: Add Only Explicit Track Identity, Not A Full Aggregate

What it means:

- keep the current task-area runtime shape
- add a stronger task-line identity only when `track_index` stops being enough
- continue tightening seams around writers and invariants

Pros:

- solves the most likely future pressure point without a full rewrite
- cheaper than aggregate promotion
- compatible with the current task-area model

Cons:

- still not a full aggregate
- only pays off once a real identity problem appears
- may be unnecessary if current content keeps treating `track_index` as enough

## Risks

### If We Promote A Track Aggregate Too Early

- we may freeze the wrong boundaries around geometry-heavy code
- we may create a new abstraction layer that mostly forwards to old services
- we may slow delivery without actually reducing task-area bugs

### If We Never Revisit It

- `track_index` may become an overloaded pseudo-identity
- more external writers could accumulate before ownership is tightened again
- future task-area specialization could become harder to reason about

### Concrete Trigger Risks To Watch

- more than one new external writer needs track-local invariants
- line identity needs metadata beyond `track_index`
- cross-track rules stop being understandable through the current service seams

## Recommendation

Choose **Option A now**, while explicitly keeping **Option C** as the next
fallback trigger.

Why:

- the recent task-area work removed the biggest immediate ambiguity without
  requiring a new aggregate
- the remaining hotspot is still `TrackBlockService`, and its pain is still
  mostly geometry ownership, not missing aggregate terminology
- the current incremental model now has enough seams and tests to support safe
  iteration

Decision rule:

- do not start a full `Track` aggregate rewrite in the current phase
- revisit only when one of these becomes true:
  - `track_index` is no longer a sufficient identity
  - multiple new writers need shared lane-local invariants
  - `TrackBlockService` can be split cleanly between geometry and business
    mutation

## Counter-Review

Why not promote the aggregate now if we already know the direction?

- because the repo now has a workable middle layer, and the remaining pain is
  not yet "missing aggregate root" pain
- because a premature aggregate would mostly wrap current hosted-block behavior
  instead of replacing it
- because the best next improvement is still selective seam work, not model
  replacement

What assumption does this recommendation depend on?

- that task-area changes in the near term will stay closer to write-path and
  policy tightening than to new lane-identity requirements

If that assumption fails, the next cut should not jump straight to full
aggregate purity. It should first test Option C: add explicit task-line
identity and re-check the remaining hotspot split.

## Decision Summary

1. The current task-area tightening work was enough to make this re-evaluation
   meaningful.
2. A full `Track` aggregate is **not** worth doing now.
3. The best current architecture stance is:
   - `CampaignState` remains the host shell
   - `Task Area` remains a named scheduling subdomain
   - `TrackBlockService` remains the board-rule owner for now
4. The next escalation trigger is explicit track identity pressure, not DDD
   purity by itself.
5. Until that trigger appears, keep investing in:
   - explicit write seams
   - invariant tests
   - narrow host contracts
