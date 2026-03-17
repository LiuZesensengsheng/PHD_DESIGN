# Campaign Aggregate Candidate Review V1

## Problem

After the campaign orchestration closure, task-area boundary tightening, and
repository cleanup work, the next DDD question is narrower:

- which campaign-side objects are real aggregate candidates
- which ones should stay shell hosts, DTOs, or service-owned rule clusters
- whether any promotion is worth doing now

This review is not asking "can we invent a cleaner model?"

It is asking:

- which boundary already carries real invariant pressure
- which boundary is still too mixed or too geometry-heavy
- what the safest next step should be

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Constraints

- Keep the current direction: architecture migration before engine migration.
- Keep the finished campaign UI handoff closed unless a concrete trigger
  appears.
- Do not force a full `Track` aggregate rewrite; that was already rejected in
  `TRACK_AGGREGATE_REEVALUATION_V1.md`.
- Preserve current feature/content iteration speed on the campaign board.
- Prefer seam-driven tightening over a second broad campaign rewrite.
- Tie the judgment to the current codebase, especially:
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/track_block_service.py`
  - `contexts/campaign/services/thesis_*`
  - `contexts/campaign/domain/thesis_runtime_state.py`
  - `contexts/campaign/domain/session_store.py`

## Complexity

### Essential Complexity

- `CampaignState` owns real shell complexity:
  - startup / cleanup
  - route return
  - modal/input ownership
  - cross-state transition requests
- `Task Area` owns real board complexity:
  - block geometry
  - no-overlap normalization
  - DDL snake
  - fusion
  - compaction
- thesis owns real track-local consistency:
  - tier tags on thesis blocks
  - per-track thesis meta
  - per-track paper tags
  - submitted-round history
  - publication history

### Accidental Complexity

- `CampaignState` still hosts both shell behavior and task-area storage
- `track_index` is still the practical track-local identity
- thesis state is split across:
  - block tags in `_blocks`
  - `ThesisRuntimeState.track_meta`
  - `ThesisRuntimeState.paper_tags_by_track`
  - `CampaignSessionStore` snapshots and tier/publication persistence
- some broad services can look like aggregate roots when they are really
  migration-phase coordinators

## Options

### Option A: Promote `Campaign` As The Formal Aggregate Root Now

What it means:

- treat `CampaignState` as the main aggregate root
- keep task-area and thesis behavior as internal methods or child policies
- continue shrinking services back into a more central runtime model

Pros:

- strongest single-owner story
- easiest answer if someone asks "what is the top-level root?"

Cons:

- too broad to be useful
- collapses shell lifecycle, task-area geometry, and thesis progression into
  one oversized boundary
- would push more logic back toward the host class right after recent seam work

### Option B: Keep `Campaign` As Shell, Treat Aggregate Candidates Selectively

What it means:

- keep `Campaign` as shell/orchestration owner
- keep `Task Area` as a named campaign subdomain, not a promoted aggregate yet
- treat thesis as the closest aggregate candidate, but keep it seam-driven
  until identity pressure or new writers justify promotion

Pros:

- matches the current runtime shape
- preserves the UI-safe surface
- avoids turning geometry-heavy code into a fake aggregate
- keeps the best candidate visible without forcing premature model replacement

Cons:

- architecture stays intentionally uneven
- some candidate boundaries remain partially split across runtime stores and
  services

### Option C: Promote A Track-Local `Thesis` Aggregate Now

What it means:

- formalize one per-track thesis boundary as the main owner of:
  - thesis block tags
  - thesis meta
  - paper tags
  - submission/publication history
- move more of the current `thesis_*` services behind that explicit object

Pros:

- best fit for the most mature invariant cluster in the current campaign code
- could reduce thesis-specific writer drift
- more realistic than promoting the whole campaign or the whole task area

Cons:

- still depends on `track_index` as the effective identity
- current runtime state is still split across `_blocks`, runtime meta, and
  session persistence
- risks creating a parallel thesis model before task-line identity becomes more
  explicit

## Risks

### If We Promote The Wrong Aggregate Too Early

- `Campaign` becomes a giant aggregate in name only
- `Track` or `Task Area` may get wrapped before geometry and business mutation
  are separable
- thesis may gain a second model instead of a clearer single boundary

### If We Stay Too Loose

- track-local thesis consistency may keep relying on memory and service order
- future contributors may treat raw `_blocks` scanning as the default contract
- candidate boundaries may stay blurred until a bigger refactor becomes harder

### Trigger Risks To Watch

- thesis gains more writers that must update tags, meta, and session data
  together
- `track_index` stops being enough as thesis/task-area identity
- non-thesis writers need shared block-removal or track-local write rules

## Recommendation

Choose **Option B** now.

### Candidate Review Outcome

#### 1. `Campaign` Is Not The Aggregate Candidate

`CampaignState` should stay the shell owner for:

- lifecycle
- transitions
- modal/input ownership
- startup / cleanup
- persistent/session coordination

This is a host/orchestration boundary, not a good DDD aggregate promotion
target.

#### 2. `Task Area` Is A Real Subdomain, But Not A Promoted Aggregate Yet

Current task-area rules live mainly in:

- `BlockDTO`
- hosted `_blocks`
- `TrackBlockService`
- task-area write seams on `CampaignState`

This is a meaningful subdomain, but not a good aggregate promotion target yet
because:

- geometry rules still dominate the hotspot
- `track_index` is still a thin identity
- `TrackBlockService` still mixes normalization and mutation policy

#### 3. The Closest Aggregate Candidate Is Track-Local `Thesis`

The strongest invariant cluster today is the thesis progression boundary around
one track:

- thesis tier tags on track-local blocks
- track-local thesis meta in `ThesisRuntimeState`
- track-local paper tags
- submitted-round history
- publication history

Current evidence:

- `ThesisWritePathService`
- `ThesisBlockMutationService`
- `ThesisRoundService`
- `ThesisJudgmentFlowService`
- `tests/campaign/test_thesis_aggregate_invariants.py`

This is the most credible future aggregate candidate, but it is still not worth
full promotion now.

### Small Cut Landed With This Review

To make the thesis track-local boundary a little more explicit without opening a
full facade rewrite:

- `CampaignState` now exposes `get_campaign_blocks_for_track(track_index)`
- `ThesisWritePathService` uses that seam for track-local tier-tag writes
- `ThesisMetaService` uses that seam for track-local tier reads

This does not create a new aggregate, but it starts expressing the real
track-local thesis boundary more directly than raw `_blocks` scanning.

### Practical Next Step

If we continue the DDD path now, the next task should be
`Aggregate Invariant Tests V1`, focused on:

- campaign shell invariants that cross startup / cleanup / route return
- task-area invariants that remain board-critical
- thesis track-local consistency as the leading aggregate candidate

## Counter-Review

Why not promote the thesis aggregate now if it is clearly the best candidate?

- because the current shape is still split across runtime block tags, runtime
  meta, and session persistence
- because `track_index` is still a pragmatic identity, not a richer explicit
  object
- because the repo benefits more right now from stronger invariant coverage
  than from another model rewrite

Why not say no aggregate candidate exists yet?

- because thesis track-local consistency is already real and already protected
  by focused tests
- because pretending there is no candidate would hide the most mature DDD
  boundary in the current campaign code

What assumption does this recommendation depend on?

- that near-term campaign change pressure will still be better served by seam
  tightening and invariants than by an immediate new aggregate type

If that assumption fails, the first promotion target should be the
track-local thesis boundary, not the whole campaign shell and not the full
task area.

## Decision Summary

1. `Campaign` should remain a shell/orchestration owner, not a promoted
   aggregate root.
2. `Task Area` is a real campaign subdomain, but not a good aggregate
   promotion target yet.
3. The closest current aggregate candidate is track-local `Thesis`
   progression.
4. Even that thesis boundary is not worth full promotion in the current phase.
5. The best next step is stronger aggregate-focused invariant coverage, not a
   new broad model rewrite.
