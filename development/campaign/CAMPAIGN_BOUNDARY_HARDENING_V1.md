# Campaign Boundary Hardening V1

## Goal

Turn the current campaign architecture direction into an automation-safe
execution line.

This plan is not another broad cleanup pass.

It exists to harden the already-chosen campaign boundaries around:

- lifecycle ownership
- trigger / forced-event ownership
- direct seam policy
- runtime-UI vs business-orchestration separation
- executable campaign-side guardrails

- Level: `L3 Architecture`
- Date: `2026-04-24`

## Problem

The repo already completed the earlier campaign simplification and self-refactor
lines closely enough that the next problem is no longer "how do we make
campaign less messy in general?"

The real problem is:

- how to turn the current campaign direction into one stable automation line
- how to keep future campaign work on lifecycle/trigger seams instead of
  drifting back into frame/update timing
- how to hard-fail the stable campaign boundary rules instead of relying on
  prose plus recent memory

Current evidence:

- `CampaignState` already has a stable grouped-service surface and preserved
  `request_*` host seams
- lifecycle result and snapshot contracts are now explicit
- forced-event ownership has already moved onto runtime/presenter/catalog seams
- runtime UI boundaries are documented and intentionally narrow

What is still missing is a single plan that says:

- what the next active campaign line is
- what must not be reopened
- which boundaries are now hard-fail vs report-only
- which hotspots stay deferred until real product pressure appears

## Constraints

- Keep the scope inside:
  - `contexts/campaign/**`
  - `tests/campaign/**`
  - campaign-related docs/logs under `docs/**`
- Keep the current direction:
  - architecture migration before engine migration
  - no broad `CampaignView` rewrite
  - no whole-campaign aggregate rewrite
- Preserve the direct seam whitelist from
  `docs/development/campaign/CAMPAIGN_DIRECT_SEAM_POLICY_V1.md`.
- Preserve the runtime UI boundary from
  `docs/development/campaign/CAMPAIGN_RUNTIME_UI_BOUNDARY_V1.md`.
- Do not widen into:
  - `contexts/campaign/view.py`
  - `contexts/campaign/rendering/**`
  - `contexts/campaign/ui_runtime/**`
  - `contexts/shared/**`
- Do not use this line to do physical `services -> application/ui` directory
  migration.
- Use `py -3.11` for validation; the default `python` executable is not the
  project baseline on the current workstation.

## Complexity

### Essential Complexity

The next campaign work really does need to coordinate four architecture axes:

1. lifecycle timing ownership
2. trigger / reaction / forced-event ownership
3. shell/runtime seam policy
4. hard-fail boundary enforcement

Those are real architecture concerns, not cleanup taste.

### Accidental Complexity

The accidental complexity comes from treating all remaining campaign follow-up
as if it were the same kind of work.

It is not.

There are at least three different categories now:

1. mainline boundary hardening
   - lifecycle contracts
   - trigger ownership
   - forced-event seams
   - guardrails
2. optional narrow review-next cleanup
   - `hit_test_service`
3. triggered backlog only
   - `thesis_slice`
   - future `track_block_service` follow-up
   - directory purity or large service taxonomy cleanup

If those categories are mixed together, automation will either:

- reopen broad cleanup by accident
- or keep skipping the highest-value boundary work because it looks "already
  mostly done"

## Options

### Option A: Freeze Campaign Follow-Up And Stay Feature-Driven Only

What it means:

- keep the current docs as reference memory
- only touch campaign boundaries when a specific feature breaks them

Pros:

- lowest immediate cost
- avoids new planning overhead

Cons:

- stable campaign rules remain partly social rather than mechanical
- lifecycle/trigger growth can drift back into frame/update ownership
- automation has no single source-of-truth next line

### Option B: Run A Narrow Campaign Boundary Hardening Line

What it means:

- keep prior cleanup lines closed
- start a new serial plan focused on hardening the campaign boundaries that are
  now stable enough to enforce
- keep hotspots and directory purity out of the mainline unless triggered

Pros:

- matches the repo's current maturity
- makes the next automation line decision-frozen instead of open-ended
- raises AI safety without reopening broad structural churn

Cons:

- does not produce perfect directory symmetry
- leaves some large files and hotspots in place longer
- requires explicit hard-fail vs report-only discipline

### Option C: Reopen Broad Campaign Purification

What it means:

- use this phase to physically reorganize more of `services/`
- push toward `application/ui` directory purity
- revisit multiple deferred hotspots in one line

Pros:

- strongest theoretical surface symmetry if it succeeds

Cons:

- highest churn
- reopens areas that are intentionally out of scope
- likely blends lifecycle hardening with taxonomy cleanup and hotspot rewrites

## Risks

### If We Do Too Little

- campaign boundary rules stay split across several docs without a new
  automation-safe mainline
- stable seams may drift because they are not all encoded as hard-fail guardrails
- later AI work will keep rescanning multiple campaign docs just to decide where
  a change should land

### If We Do Too Much

- this line can silently reopen:
  - `CampaignView`
  - visual-runtime extraction
  - `services` physical taxonomy migration
  - thesis/task-area hotspot rewrites
- the line stops being automation-friendly and turns back into a broad refactor

### Specific Risks To Manage

- `hit_test_service` may look like a trivial cleanup but still touch hot event
  ingress if widened carelessly
- `thesis_slice` can attract cleanliness-driven refactor pressure despite
  lacking a fresh writer/identity trigger
- hard-failing noisy metrics such as touch counts or file length would create
  unstable guardrails and reduce trust in the checks

## Recommendation

Choose **Option B**.

Treat the next active campaign architecture line as:

`boundary hardening, not broad cleanup`

### Decision Freeze

The following decisions are accepted for this line:

1. scope stays inside campaign/tests/docs
2. target is boundary hardening, not directory purity or broad reorganization
3. no physical `services -> application/ui` migration in this round
4. `hit_test_service` is an optional late-phase seam review, not a mandatory
   mainline blocker
5. `thesis_slice` remains triggered backlog only until real writer/identity
   pressure appears
6. only stable boundary rules become hard-fail; hotspot touch counts and file
   length stay report-only
7. every slice must update repo memory:
   - task pool
   - relevant development docs
   - daily log
8. validation rhythm stays:
   - targeted tests per slice
   - `tests/campaign -q` at phase close
   - smoke baseline only at closure or when a slice explicitly requires it

## Execution Plan

### Phase 0. Scope Freeze And Baseline Lock

Goal:

- freeze the active line before automation starts making changes

Deliverables:

1. this plan document
2. task-pool active entry updated to point here
3. decision-log entry for the accepted hardening line
4. daily-log entry for the decision freeze
5. explicit validation pack for later phases

Done definition:

- the next active campaign line is no longer ambiguous
- no-touch zones are explicit
- hard-fail vs report-only policy is explicit

### Phase 1. Lifecycle Contract Closure

Goal:

- keep `contexts/campaign/lifecycle/` as the canonical timing owner
- continue removing any residual business-timing ambiguity around startup,
  turn-cycle, return-resolution, and interrupt entry/exit reporting

Primary areas:

- `contexts/campaign/lifecycle/**`
- `contexts/campaign/services/campaign_startup_orchestrator.py`
- `contexts/campaign/services/campaign_turn_orchestrator.py`
- `contexts/campaign/services/campaign_end_turn_orchestrator.py`
- `contexts/campaign/state.py`
- `tests/campaign/test_campaign_lifecycle_machine.py`
- related lifecycle contract tests

Allowed cuts:

- explicit result/read-surface tightening
- host seam tightening
- lifecycle-owned timing reads replacing implicit reconstruction

Do not do:

- broad task-area redesign
- `CampaignView` work
- generic interrupt-platform expansion

Validation:

- targeted lifecycle pack for the active slice
- `py -3.11 -m pytest tests/campaign/test_campaign_lifecycle_machine.py tests/campaign/test_campaign_turn_orchestrator.py tests/campaign/test_campaign_startup_orchestrator.py -q`
- phase close:
  - `py -3.11 -m pytest tests/campaign -q`

### Phase 2. Trigger And Forced-Event Boundary Closure

Goal:

- keep trigger collection, trigger consumption, and forced-event ownership on
  one explicit campaign path

Primary areas:

- `contexts/campaign/services/campaign_trigger_surface_service.py`
- `contexts/campaign/services/campaign_trigger_reaction_service.py`
- `contexts/campaign/services/campaign_forced_event_runtime_service.py`
- `contexts/campaign/services/campaign_forced_event_presentation_service.py`
- `contexts/campaign/domain/campaign_forced_event_catalog.py`
- related tests/docs

Allowed cuts:

- trigger consumer tightening
- forced-event gate/resolution contract tightening
- boundary guardrails that forbid direct presentation or modal dependency from
  the wrong owner

Do not do:

- new product-scale interrupt platform
- save compatibility redesign
- new forced-event UI shape discussions inside this line

Validation:

- targeted trigger/forced-event pack for the active slice
- phase close:
  - `py -3.11 -m pytest tests/campaign -q`

### Phase 3. Campaign Boundary Gates

Goal:

- add or tighten hard-fail campaign guardrails for the stable rules that now
  define the architecture

Current status on `2026-04-24`:

- a hard-fail guardrail now locks the explicit lifecycle result seams so
  startup and end-turn host paths do not regress back to raw-context-only
  handoffs
- a second hard-fail guardrail now locks `CampaignState` direct service alias
  installation to:
  - the stable shell/runtime whitelist
  - grouped-only reward/thesis/social ownership
  - the optional review-next `hit_test_service` survivor only
- a third hard-fail guardrail now keeps turn timing ownership out of frame and
  event-ingress paths so keyboard/mouse/ui-button routing stays on
  `CampaignState.request_end_turn*()` host seams
- a fourth hard-fail guardrail now keeps forced-event ownership split between
  the runtime owner and presenter seam so:
  - stable non-presentation forced-event owners stay UI-framework free
  - pending/active queue state does not drift back into the presenter
- a fifth hard-fail guardrail now keeps forced-event gate wiring on the
  `CampaignState` host seam instead of letting lifecycle-step code couple
  directly to runtime/presenter owners
- a sixth hard-fail guardrail now keeps lifecycle-side trigger dispatch on
  `CampaignState` host seams instead of letting lifecycle context/steps couple
  directly to trigger/forced-event owners
- a seventh hard-fail guardrail now keeps the lifecycle package itself free of
  direct UI-framework and campaign-service imports
- `Phase 3` close validation passed on `2026-04-24`:
  - `py -3.11 -m pytest tests/campaign -q`
- `Phase 3` is now complete; the only remaining in-line follow-up is the
  optional `Phase 4` review-next seam slice for `hit_test_service`

Primary targets:

- `tests/campaign/test_campaign_simplification_guardrails_v1.py`
- `scripts/validate_architecture.py` if and only if the added checks can remain
  stable and campaign-specific
- campaign development docs that define the allowed boundary

Good hard-fail rules for this phase:

- grouped leaf-service families must not regain direct state aliases
- removed compatibility seams must not reappear
- runtime UI must not import campaign business-service ownership
- campaign timing logic must not quietly drift back into frame/update paths
- direct shell/runtime seams must stay whitelist-based rather than open-ended

Good report-only signals for this phase:

- hotspot touch counts
- file lengths
- internal module responsibility counts

Validation:

- `py -3.11 -m pytest tests/campaign/test_campaign_simplification_guardrails_v1.py -q`
- any new focused guardrail tests for this phase
- phase close:
  - `py -3.11 -m pytest tests/campaign -q`

### Phase 4. Optional Review-Next Seam Slice

Goal:

- evaluate the remaining review-next seam:
  - `hit_test_service`

Current stance:

- optional
- only execute if the change stays local and does not destabilize event ingress

Do not do:

- reopen the direct seam whitelist broadly
- use this phase to start a new cleanup wave

Validation:

- the smallest targeted event-ingress pack that covers the touched seam
- phase close:
  - `py -3.11 -m pytest tests/campaign -q`

### Phase 5. Triggered Backlog Only

These are explicitly **not** automatic next steps for this line:

- `thesis_slice` dependency narrowing
- another `track_block_service` architecture pass
- physical `services -> application/ui` reorganization
- `CampaignView` or visual-runtime refactor

Only reopen them when one of these triggers appears:

- thesis writer collision or stronger identity/invariant pressure
- task-area DDL/fusion/compaction becomes a near-term product blocker
- retained `services` taxonomy confusion starts blocking active automation work

## Automation Contract

Every automation slice under this plan should have:

1. one declared phase
2. one declared write scope
3. one explicit validation pack
4. one explicit no-touch list
5. the required memory updates:
   - daily log
   - task pool when phase status changes
   - any long-term doc that became the new source of truth

### Default Validation Rhythm

Per slice:

- run only the targeted tests needed for the touched seam

Per phase close:

- `py -3.11 -m pytest tests/campaign -q`

At line closure or explicitly high-risk phase closure:

- `py -3.11 scripts/run_repo_smoke_baseline.py`

## Stop Conditions

Pause this line and split a new task if:

- progress requires broad edits under:
  - `contexts/campaign/view.py`
  - `contexts/campaign/rendering/**`
  - `contexts/campaign/ui_runtime/**`
  - `contexts/shared/**`
- a slice needs physical service taxonomy migration to make progress
- `thesis_slice` or task-area hotspots become the actual critical path
- the work starts discussing save/schema redesign rather than campaign boundary
  hardening

## Counter-Review

Why not just keep A1 lifecycle/forced-event narrowing as-is and skip a new
planning line?

- because the repo now needs one active source-of-truth that also defines
  guardrails, hard-fail policy, optional seams, and backlog triggers
- the old line is a good technical base, but too narrow as the next automation
  entrypoint by itself

Why not reopen `thesis_slice` now if it is still the hottest remaining service?

- because the current evidence still says it is a convenience hotspot without a
  fresh identity/writer trigger
- cleanliness alone is not enough reason to reopen a broad thesis cut

Why not push physical `services` taxonomy cleanup now?

- because that would mix naming/placement work with the higher-value boundary
  hardening work
- the next risk is not "the directories look imperfect"; it is "stable campaign
  rules are not all mechanically enforced yet"

## Decision Summary

1. The next active campaign architecture line is `Campaign Boundary Hardening
   V1`.
2. This line hardens boundaries; it does not reopen broad cleanup.
3. The mainline order is:
   - lifecycle contracts
   - trigger / forced-event closure
   - campaign-side guardrails
   - optional `hit_test_service` review
4. `thesis_slice`, task-area hotspot follow-up, and physical service taxonomy
   cleanup stay in triggered backlog.
5. Only stable boundary rules become hard-fail; noisy structural metrics remain
   report-only.
