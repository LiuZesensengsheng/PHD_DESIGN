# DDD Layer Planning V1

## Problem

After the campaign orchestration closure and the combat queue cutover work, the
repo now has a clearer middle layer, but the "DDD layer" still looks uneven.

The main concern is understandable:

- combat action queue exists, but not every effect path is equally modeled
- some campaign/thesis boundaries now have seams, but not every hotspot is a
  true aggregate
- `SaveRepository` exists, but repository usage is intentionally narrow instead
  of universal

The real question is not "is DDD finished?"

It is:

- what should count as the real DDD roadmap from here
- what is already good enough
- what should stay deliberately incomplete for now

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Constraints

- Keep the current direction: architecture migration before engine migration.
- Do not reopen the campaign UI-safe handoff surface without a concrete trigger.
- Do not turn the repo into a theory-first DDD rewrite.
- Preserve current feature/content iteration speed.
- Prefer explicit seams, tests, and write paths over nominal purity.
- Respect the current shape of the codebase:
  - combat queueing already landed as a bounded orchestration substrate
  - campaign orchestration is closed enough for UI-first work
  - task-area geometry is still a real hotspot
  - save/load already has a real repository boundary

## Complexity

### Essential Complexity

- combat has real sequencing complexity:
  - card play
  - effect order
  - follow-up actions
  - task-host resolution
- campaign has real shell complexity:
  - startup / cleanup / route return
  - modal ownership
  - state transitions
  - thesis and task-area coordination
- task area has real board-rule complexity:
  - no-overlap normalization
  - DDL snake
  - fusion
  - compaction
- thesis has real write/invariant complexity:
  - tier/runtime/meta sync
  - round activation/removal
  - judgment follow-up
  - publication follow-up
- save/load is a real external IO boundary.

### Accidental Complexity

- queue completeness is easy to mistake for "DDD completeness"
- some services still look broad because the repo is in a migration phase, not
  because every broad service should become a repository or aggregate
- `TrackBlockService` mixes geometry policy and mutation policy, which makes it
  look like an aggregate candidate before its boundaries are actually stable
- `CampaignSessionStore` can be mistaken for a missing repository layer, even
  though it is currently a typed helper over shell-owned runtime persistence
- "repository everywhere" would create more abstraction noise than actual
  ownership clarity right now

## Options

### Option A: Push Full DDD Promotion Now

What it means:

- continue shrinking every remaining combat fallback path until the queue is the
  only real execution model
- promote explicit aggregates across campaign/task-area/thesis/combat
- add repository-style abstractions around more runtime/session/content paths
- reduce mixed-mode services aggressively in one broader phase

Pros:

- strongest purity story
- cleaner long-term terminology if it succeeds
- fewer "migration-phase" exceptions left in the architecture

Cons:

- highest cost
- risks reopening the campaign UI handoff phase immediately after it stabilized
- likely forces abstraction ahead of real product pressure
- likely creates forwarding layers around task-area geometry and session helpers
  before the right ownership split is proven

### Option B: Use A Selective DDD Roadmap On Top Of Current Orchestration

What it means:

- treat queueing, aggregates, and repositories as separate architecture axes
- keep combat queue as an application-orchestration substrate, not as the
  definition of DDD completion
- keep repository usage narrow at true IO boundaries
- promote only the aggregate candidates that have real invariant pressure
- use invariant tests and host narrowing before aggregate promotion

Pros:

- matches the repo's current maturity
- avoids turning "DDD planning" into another large rewrite
- keeps UI work unblocked
- gives a real order for future DDD work instead of a vague "make it cleaner"

Cons:

- architecture remains intentionally uneven for a while
- some mixed-responsibility hotspots stay in place longer
- requires discipline to avoid drifting back into ad hoc service growth

### Option C: Freeze DDD Planning Entirely And Stay Orchestration-Only

What it means:

- treat current queue/orchestration seams as enough
- do not define any further DDD roadmap now
- only fix local issues case by case

Pros:

- lowest immediate cost
- zero new architecture pressure

Cons:

- leaves the team without a shared answer when aggregate/repository questions
  come back
- increases the chance of future debates repeating from scratch
- gives no ordering for real follow-up work when hotspots do reappear

## Risks

### If We Push Full DDD Too Early

- we may generalize repositories where typed stores/helpers are actually better
- we may promote a `Track` aggregate before geometry and business mutation are
  separable
- we may spend time on symmetry rather than on the highest-pressure seams
- we may delay UI and content delivery for architecture that has not proven ROI

### If We Do Nothing

- the queue / aggregate / repository story stays mentally blurry
- future contributors may assume missing symmetry implies missing correctness
- the next hotspot may reopen with no agreed migration order

### Trigger Risks To Watch

- combat adds new sequencing-heavy mechanics that no longer fit the current
  planner/fallback split
- thesis gains new cross-round writers that bypass the current write/block seams
- task area needs stronger line identity than `track_index`
- campaign services start duplicating session/persistent write rules again
- save/content boundaries begin leaking concrete IO details into application code

## Recommendation

Choose **Option B**.

The DDD roadmap should be selective and phased, not global.

### Recommended Stance By Axis

#### 1. Action Queue

Current judgment:

- combat queueing is already a successful application-orchestration layer
- it is not the current blocker for DDD planning

Rule:

- treat `ActionQueue`, `CardPlayOrchestrator`, and `EffectPlanner` as the combat
  sequencing substrate
- continue queue work only when a concrete active-path fallback or new mechanic
  creates real sequencing pressure
- do not force campaign or thesis to "also have queues" just for architecture
  symmetry

Practical meaning:

- queue residual work stays in the combat task line
- it should not be used as the headline reason to reopen a broad DDD phase

#### 2. Aggregates

Current judgment:

- `Campaign` should remain a shell/orchestration owner, not a purity-driven
  aggregate root
- `Task Area` is not ready for a full `Track` aggregate
- `Thesis` is the most mature aggregate candidate, but only under explicit new
  pressure

Rule:

- keep the current task-area model incremental
- keep thesis on seam-driven maintenance unless a new hotspot appears
- use candidate review + invariants before promoting new aggregates

Near-term aggregate priority:

1. `Campaign Aggregate Candidate Review`
2. `Aggregate Invariant Tests`
3. selective host narrowing or identity strengthening
4. only then consider explicit promotion of a new aggregate boundary

#### 3. Repository Boundaries

Current judgment:

- `SaveRepository` / `FileSaveRepository` are good repository examples because
  they sit on a real external persistence boundary
- `CampaignSessionStore` should stay a typed store/helper for now
- task-area runtime and thesis runtime should not be pushed behind repositories
  just to look cleaner

Rule:

- keep repositories for true IO or external data boundaries
- do not repository-ize shell-owned runtime/session mutation paths by default
- prefer typed stores, seam methods, and narrow protocols inside live runtime
  contexts

### Recommended Execution Order

If DDD work is reopened after UI-first progress begins, the order should be:

1. `Repository Boundary Cleanup V1`
   - clarify where repositories are truly worth keeping or adding
2. `Campaign Aggregate Candidate Review`
   - decide which campaign-side objects are worth aggregate promotion
3. `Aggregate Invariant Tests V1`
   - lock the chosen boundaries with executable contracts
4. `State Host Facade V1`
   - narrow only the services whose responsibilities are already stable
5. reopen `Thesis Aggregate Boundary Review` or task-area identity work only if
   a fresh trigger appears

This is a roadmap, not a mandate to do all five now.

## Counter-Review

Why not say the DDD layer is already done?

- because the repo still has real aggregate/repository questions that were
  intentionally deferred rather than solved
- because selective follow-up work still has value when new pressure appears

Why not say "do repository cleanup first" and start coding immediately?

- because the campaign orchestration closure just landed, and the next default
  priority is still UI-first validation
- because repository work without a fresh trigger can easily drift into fake
  abstraction

What assumption does the recommendation depend on?

- that near-term project pressure will come more from real UI integration and
  targeted hotspot pain than from a need for immediate architecture symmetry

If that assumption fails, the first thing to reopen should be the smallest
triggered axis:

- queue residuals for combat sequencing pain
- aggregate review for invariant/identity pain
- repository review for IO-boundary pain

not all three at once.

## Decision Summary

1. The current repo does not need a full DDD rewrite phase now.
2. Combat action queueing is already "good enough" as a bounded sequencing
   substrate and should not be confused with unfinished DDD by itself.
3. Repository usage should remain narrow and IO-focused; `CampaignSessionStore`
   is not evidence that a universal repository layer is missing.
4. The most important future DDD work is not "promote everything"; it is:
   - repository boundary review
   - aggregate candidate review
   - invariant locking
   - selective host narrowing
5. The default next project phase should still be UI-first. Reopen DDD work
   only when one specific axis shows real pressure.
