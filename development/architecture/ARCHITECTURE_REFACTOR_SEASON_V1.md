# Architecture Refactor Season V1

## Goal

Use the short content-free window to reduce architecture drag before the next
content push.

This is a planning and coordination document. It does not authorize a broad
rewrite. Each execution line below must still land as a separate branch with its
own focused scope, validation pack, and rollback story.

## Current Context

- The long-term direction remains `Godot-ization inside pygame`, not an engine
  migration.
- The project now has layered test feedback:
  - `py -3.11 scripts/run_test_smoke.py --profile quick`
  - `py -3.11 scripts/run_test_smoke.py --profile contract`
  - `py -3.11 -m pytest -q` remains the commit gate until explicitly changed.
- The user is willing to accept more refactor time in the short term.
- Old saves can be treated aggressively during this pre-content stage.
- UI refactor needs human visual review and should wait for a review window.
- `cardanalysis` / `combat_analysis` remains out of scope for this refactor
  season unless explicitly reopened.

## Non-Goals

- No one-shot engine rewrite.
- No whole-project directory-purity migration.
- No broad `CampaignView` rewrite without human review.
- No content-design work mixed into architecture cleanup.
- No deleting tests only to reduce runtime.
- No save-compatibility churn hidden inside combat/campaign/content changes.

## Execution Lines

### Line 0. Test Strategy Follow-Up

Status:

- foundation landed in `Test Strategy V1`

Purpose:

- keep refactor feedback fast enough for AI agents
- avoid turning every tiny slice into a four-minute validation wait

Allowed work:

- tag smoke-owned tests with existing marker vocabulary
- add focused smoke profiles only when they have a clear owner
- profile repeated campaign/combat fixture setup before changing helpers

Do not do:

- change the full-suite commit gate without a decision-log update
- optimize `cardanalysis` tests in this line
- enable xdist by default

Default validation:

- `py -3.11 scripts/run_test_smoke.py --profile quick`
- `py -3.11 scripts/run_test_smoke.py --profile contract`
- `py -3.11 -m pytest -q` before commits

### Line 1. Save Reset Policy V1

Source of truth:

- `docs/development/architecture/SAVE_RESET_POLICY_V1.md`

Purpose:

- remove old-save ambiguity while the project has no meaningful external save
  compatibility obligation
- make future save behavior explicit instead of accidentally tolerant

Allowed work:

- document that pre-alpha saves may be invalidated
- add a current save schema policy with clear unsupported-version errors
- delete low-value legacy migration paths after tests prove current saves still
  round-trip
- simplify save-slot and machine-snapshot compatibility code where the old
  format is only kept for historical local saves

Do not do:

- mix save reset with combat energy semantics
- mix save reset with content-pack/DLC schema design beyond a placeholder field
- silently delete current save/load round-trip coverage

Default validation:

- `py -3.11 scripts/run_test_smoke.py --profile quick`
- focused save tests under `tests/save/` and `tests/shared/*snapshot*`
- `py -3.11 -m pytest -q` before commits

Stop conditions:

- a change requires supporting real user saves
- a migration decision affects future content-pack identity
- save failures require gameplay-rule changes to fix

### Line 2. Combat Contract Convergence V1

Source of truth:

- `docs/development/combat/COMBAT_CONTRACT_CONVERGENCE_V1.md`

Purpose:

- reduce long-lived combat dual tracks and implicit contracts after compat-zero
  closure

Primary targets:

- player energy scalar vs colored energy pool convergence
- event bus priority semantics and protocol alignment
- effect/card contract clarity where convenience aliases are retained
- combat save payload fields only after `Save Reset Policy V1` freezes its
  stance

Allowed work:

- write a decision doc before implementation
- converge one contract at a time
- prefer typed/current runtime ownership over compatibility fallbacks
- keep combat session as the runtime host

Do not do:

- reopen combat global compat-zero as a general cleanup wave
- rebalance combat content
- change animation/video blocking semantics
- refactor `combat_view` behavior as part of contract cleanup

Default validation:

- `py -3.11 scripts/run_test_smoke.py --profile quick`
- `py -3.11 scripts/run_test_smoke.py --profile contract`
- relevant combat focused tests
- `py -3.11 -m pytest -q` before commits

Stop conditions:

- content semantics or balance become the real blocker
- contract convergence requires save-policy decisions that have not landed
- a slice touches UI behavior more than runtime/domain contracts

### Line 3. CampaignState Strangler V1

Source of truth:

- `docs/development/campaign/CAMPAIGN_STATE_STRANGLER_V1.md`

Purpose:

- continue shrinking `CampaignState` by moving explicit write paths and
  lifecycle/trigger/reward boundaries behind stable services

Current baseline:

- `Campaign Boundary Hardening V1` is already closed through Phase 3.
- The remaining in-line campaign boundary item is optional `hit_test_service`
  review.

Allowed work:

- follow the new strangler plan before implementation
- pick one write path or host seam per slice
- keep `CampaignState` as the shell while moving responsibilities out
- add guardrails only for stable rules, not file size or touch counts

Do not do:

- reopen broad campaign cleanup
- move physical directories for taxonomy alone
- touch `contexts/campaign/view.py`, `rendering/**`, or `ui_runtime/**`
  without a UI review window
- reopen thesis/task-area hotspots without a fresh writer or board-rule trigger

Default validation:

- `py -3.11 scripts/run_test_smoke.py --profile quick`
- focused campaign tests for the touched seam
- `py -3.11 -m pytest tests/campaign -q` at phase close
- `py -3.11 -m pytest -q` before commits

Stop conditions:

- progress requires visual UI changes
- progress requires broad thesis/task-area redesign
- a slice starts changing product rules rather than architecture ownership

### Line 4. Content Pack Minimal V1

Source of truth:

- `docs/development/content/CONTENT_PACK_MINIMAL_V1.md`

Purpose:

- prepare future content/DLC work without building a heavy plugin platform

Allowed work:

- define pack manifest shape
- define pack id, version, dependencies, and deprecation policy
- validate active content packs
- record enabled pack identity in current save schema after save reset policy
  is clear

Do not do:

- build a full mod/plugin system
- add hot reload
- implement complex dependency solving
- migrate all content directories in one pass

Default validation:

- `py -3.11 scripts/run_test_smoke.py --profile quick`
- data-pipeline focused tests
- content discovery and save-pinning focused tests
- `py -3.11 -m pytest -q` before commits

Stop conditions:

- pack identity decisions need product naming or store/DLC policy
- content authoring begins to dominate architecture work
- save schema assumptions are still unresolved

### Line 5. UI Runtime Refactor Window

Purpose:

- continue pygame-internal Godot-like runtime UI work when human visual review
  is available

Allowed work:

- retained/runtime widget extraction for one interaction at a time
- modal/input ownership cleanup with screenshots or manual review
- preserve current user-visible behavior unless the user is actively reviewing
  the change

Do not do:

- broad visual rewrite while the user is unavailable
- replace whole screens in one PR
- mix subjective UI polish into combat/campaign contract convergence

Default validation:

- focused UI/controller tests
- `py -3.11 scripts/run_test_smoke.py --profile quick`
- screenshots or manual review notes when rendering changes
- `py -3.11 -m pytest -q` before commits

Stop conditions:

- visual behavior cannot be judged automatically
- the change needs design taste decisions
- a UI refactor starts changing business rules

## Recommended Order

1. Close this planning line.
2. Run `Save Reset Policy V1`.
3. Start `Combat Contract Convergence V1`, with energy convergence as the first
   likely decision.
4. Start `CampaignState Strangler V1` after the first combat/save slice lands or
   when campaign work becomes the critical path.
5. Start `Content Pack Minimal V1` after save identity policy is clear.
6. Schedule `UI Runtime Refactor Window` when human visual review is available.

## Validation Rhythm

For implementation slices:

1. run focused tests while editing
2. run quick smoke before broader validation
3. run contract smoke when touching boundaries
4. run the subsystem phase-close pack when closing a phase
5. run full pytest before each commit until the commit policy changes

## PR Discipline

Each PR should state:

- which execution line it belongs to
- what it intentionally does not touch
- focused validation
- smoke validation
- full-suite validation or explicit blocker

If a PR starts spanning more than one execution line, split it.

## Decision Summary

This refactor season is worthwhile because there is a short content-free window
and the test feedback loop is now fast enough to support smaller AI slices.

The most valuable first move is not broad cleanup. It is to remove save-policy
ambiguity, then converge combat contracts, then continue campaign strangling
under established boundaries.
