# State Host Facade V1

## Problem

After repository cleanup, aggregate candidate review, and invariant locking, the
remaining DDD follow-up was to narrow one more high-ROI campaign service away
from broad `state: Any` access.

The key question was not "can we facade the whole campaign state?"

It was:

- which service is now stable enough for a narrower host
- which hotspot should still stay deferred
- what cut reduces risk without reopening another broad architecture pass

- Level: `L2 Module`
- Date: `2026-03-17`

## Constraints

- Do not open a whole-campaign facade.
- Do not force `TrackBlockService` behind a fake abstraction while it is still
  geometry-heavy.
- Keep the campaign UI-safe surface unchanged.
- Prefer business-intent seam methods over protocols that mirror internal state.
- Build on the recent conclusion that the closest mature aggregate candidate is
  track-local thesis progression.

## Complexity

### Essential Complexity

- `ThesisMetaService` still coordinates:
  - tier prompt UI
  - thesis submission delegation
  - idea-selection modal flow
  - publication compatibility flow
  - track-local tier reads
- these behaviors are already more stable than earlier in the refactor because:
  - thesis write-path responsibility is now split out
  - thesis block mutation is now split out
  - thesis judgment/publication follow-up already have dedicated services

### Accidental Complexity

- the service still depended on a broad `state: Any`
- submission/publication compatibility calls still reached through nested
  service objects on state
- track-local tier reads still had a fallback path that could drift back toward
  raw `_blocks` access

## Options

### Option A: Add A Broad CampaignState Facade

What it means:

- define one large host/facade for multiple remaining services
- migrate `ThesisMetaService`, `ThesisSlice`, and others together

Pros:

- strongest short-term symmetry
- fewer future `state: Any` constructors if it succeeded

Cons:

- too much surface for one cut
- high risk of inventing a forwarding layer that mostly mirrors internals
- not aligned with the "smallest mature seam" rule

### Option B: Narrow `ThesisMetaService` With A Focused Host

What it means:

- add one `ThesisMetaHost` protocol
- route submission/publication compatibility through explicit `CampaignState`
  seam methods
- keep `ThesisWritePathService` as the owner of persistence writes

Pros:

- targets the most mature remaining thesis hotspot
- matches the current aggregate-candidate review
- improves AI and human safety by making dependencies explicit
- avoids reopening geometry-heavy code

Cons:

- only one service gets narrowed in this pass
- compatibility wrappers still exist inside `ThesisMetaService`

### Option C: Narrow `TrackBlockService` Instead

What it means:

- introduce a task-area host/facade around board rules now

Pros:

- addresses a large visible hotspot

Cons:

- still the wrong timing
- geometry and mutation policy are still too mixed
- higher risk of fake abstraction than real clarity

## Risks

### If We Facade Too Broadly

- protocols will start mirroring internal state fields
- the codebase gains abstraction noise without reducing churn

### If We Pick The Wrong Hotspot

- we spend effort where responsibilities are still moving
- follow-up refactors may immediately invalidate the new facade

### Residual Risk After This Cut

- `ThesisMetaService` still contains compatibility wrappers
- `ThesisSlice` and `TrackBlockService` remain intentionally deferred

## Recommendation

Choose **Option B**.

### Cut Landed

This pass narrowed `ThesisMetaService` around a focused `ThesisMetaHost`.

Code-side result:

- added `ThesisMetaHost` to `contexts/campaign/services/campaign_service_protocols.py`
- `ThesisMetaService` no longer takes `state: Any`
- `CampaignState` now exposes thin thesis facade seam methods for:
  - `submit_thesis_round_from_writing(...)`
  - `show_thesis_publication_modal(...)`
  - `open_thesis_innovation_draw_placeholder_modal(...)`
  - `record_thesis_innovation_placeholder_choice(...)`
  - `pick_thesis_innovation_placeholder_candidates(...)`
- `ThesisMetaService` now delegates through those seam methods instead of
  reaching into nested state-owned service objects directly
- track-local tier reads now rely on
  `get_campaign_blocks_for_track(track_index)` instead of raw `_blocks`
  fallback scanning

### Why This Service

This is the best current host-facade target because:

- its responsibilities are substantially more stable than earlier
- it sits directly on the leading thesis aggregate-candidate boundary
- it benefits from business-intent seam methods more than from raw state access

## Counter-Review

Why not narrow `ThesisSlice` instead?

- because it is still mostly a facade over other thesis services
- narrowing it now would give less ownership clarity than narrowing
  `ThesisMetaService`

Why not wait longer?

- because this service had already crossed the maturity line after the write
  path, block mutation, aggregate review, and invariant work
- leaving it on `state: Any` would keep the most mature remaining thesis seam
  fuzzier than it needs to be

What assumption does this depend on?

- that the next useful DDD work should stay trigger-driven rather than opening a
  second large facade campaign

## Decision Summary

1. `State Host Facade V1` should be a targeted cut, not a global facade pass.
2. `ThesisMetaService` is now mature enough for host narrowing.
3. `TrackBlockService` remains deferred.
4. `ThesisMetaService` now depends on a focused host plus explicit
   business-intent seam methods.
5. The DDD follow-up sequence is effectively closed for this phase unless a new
   hotspot trigger appears.
