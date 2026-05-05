# Campaign Self Refactor Plan V1

## Goal

Run the next campaign architecture pass as a **campaign-only refactor**.

This plan is about improving stability, DDD readiness, and AI safety inside
`contexts/campaign/` without reopening a broad UI rewrite, visual-runtime
migration, or shared-architecture cleanup.

## Why Now

The project already completed the earlier campaign simplification and
orchestration-closure passes closely enough to support UI work:

- `CampaignState` has stable `request_*` seams
- thesis already has a real write-path boundary
- aggregate-candidate invariants already exist
- task-area rules are a known hotspot, but they are still explicitly deferred

That means the highest-value next step is not another broad architecture pass.

It is a narrower one:

- keep the scope inside `campaign`
- tighten the campaign shell
- converge thesis writes
- make task-area rules easier to reason about

## Core Rule

Prefer:

`campaign-only scope -> stable seam preservation -> hotspot-local refactor -> guardrail update`

Do not prefer:

`campaign refactor -> accidental view rewrite -> visual runtime extraction -> shared cleanup`

## Scope

### In Scope

- `contexts/campaign/state.py`
- `contexts/campaign/domain/**`
- `contexts/campaign/services/**`
- `tests/campaign/**`
- campaign-specific development docs and daily logs

### Out of Scope By Default

- `contexts/campaign/view.py`
- `contexts/campaign/rendering/**`
- `contexts/campaign/ui/**`
- `contexts/campaign/ui_runtime/**`
- `contexts/shared/**`
- combat architecture
- visual-runtime extraction
- shared utility consolidation

## Non-Goals

- No full `CampaignView` rewrite
- No visual-runtime package extraction in this pass
- No whole-campaign aggregate promotion
- No repository-everywhere cleanup
- No node-tree migration campaign
- No shared architecture cleanup unless a real blocker appears

## Target Outcomes

By the end of this plan, campaign should feel like:

1. a thinner shell host
2. a clearer thesis subdomain with a more explicit main write path
3. a task-area hotspot whose rules are easier to inspect and test
4. a codebase where AI can safely change one campaign slice without guessing
   across multiple hidden ownership layers

## Phase 0. Scope Freeze And Baseline Lock

### Goal

Freeze the scope before implementation work starts.

### Deliverables

1. this plan document
2. an active task entry in `docs/development/CODEX_TASK_POOL.md`
3. a daily-log handoff note for the current date
4. a baseline validation pack for later phases

### Done Definition

Phase 0 is complete when:

- the campaign-only scope is explicitly written down
- the no-touch zones are written down
- the default next phase is `Phase 1`, not an open-ended debate
- the baseline validation pack is recorded for future phases

### Status

- `2026-04-18`: Phase 0 landed

## Phase 1. Shell Closure

### Goal

Keep `CampaignState` as the shell host, but reduce the chance that new
business logic keeps flowing back into it.

### Main Targets

- `contexts/campaign/state.py`
- `contexts/campaign/services/campaign_state_service_bundle.py`
- `contexts/campaign/services/campaign_service_protocols.py`

### Intended Cut

- preserve the existing stable `request_*` surface
- make service ownership/grouping easier to follow
- keep new business branches out of `CampaignState`
- prefer explicit host seams over raw broad host access

### Do Not Do

- rewrite `CampaignView`
- rename public seams just for taste
- move runtime-visual concerns into this phase

### Validation

- `python -m pytest tests/campaign/test_campaign_state_service_bundle_groups.py tests/campaign/test_campaign_simplification_guardrails_v1.py -q`
- `python -m pytest tests/campaign/test_campaign_simplification_guardrails_v1.py -q`
- `python -m pytest tests/campaign/test_campaign_ui_handoff_contracts.py tests/campaign/test_campaign_runtime_ui_boundary_contract.py -q`

### Status

- `2026-04-18`: Phase 1 landed

## Phase 2. Thesis Convergence

### Goal

Make the thesis track-local boundary more coherent without forcing a brand-new
formal aggregate type.

### Main Targets

- `contexts/campaign/services/thesis_write_path_service.py`
- `contexts/campaign/services/thesis_meta_service.py`
- `contexts/campaign/services/thesis_submission_flow_service.py`
- `contexts/campaign/services/thesis_round_service.py`
- `contexts/campaign/services/thesis_slice.py`
- `contexts/campaign/domain/thesis_runtime_state.py`
- `contexts/campaign/domain/session_store.py`

### Intended Cut

- reduce split-brain thesis state
- converge tier/meta/paper-tag/submission/publication writes around clearer main
  paths
- keep track-local isolation explicit

### Do Not Do

- invent a second parallel thesis model
- promote a whole new aggregate root just for terminology
- widen the scope into generic persistence cleanup

### Validation

- `python -m pytest tests/campaign/test_thesis_write_path_service.py tests/campaign/test_thesis_submission_flow_service.py -q`
- `python -m pytest tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_aggregate_invariants.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py -q`

### Status

- `2026-04-18`: Phase 2 landed

## Phase 3. Task Area Internal Rule Split

### Goal

Keep `TrackBlockService` as the stable external task-area entry point while
splitting its internal rule responsibilities into smaller units.

### Main Targets

- `contexts/campaign/services/track_block_service.py`
- `contexts/campaign/domain/track_service.py`

### Intended Cut

- separate overlap normalization
- separate DDL snake logic
- separate fusion logic
- separate compaction / stabilization helpers

### Do Not Do

- no `Track` aggregate promotion
- no new identity model in this phase
- no broad facade over all task-area behavior

### Validation

- `python -m pytest tests/campaign/test_track_block_service_overlap_guard.py tests/campaign/test_track_block_service_ddl.py tests/campaign/test_track_block_service_fusion_thesis_nodes.py -q`
- `python -m pytest tests/campaign/test_task_area_invariants.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py -q`

### Status

- `2026-04-18`: Phase 3 landed

## Phase 4. Guardrails, Docs, And Closure

### Goal

Turn the new boundaries into durable repo memory and executable checks.

### Main Targets

- `tests/campaign/**`
- `docs/development/architecture/AGGREGATE_INVARIANT_TESTS_V1.md`
- `docs/development/campaign/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
- `docs/development/campaign/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md`
- current daily log / weekly-summary follow-up when needed

### Intended Cut

- refresh hotspot status
- refresh invariant docs
- lock the newly stable assumptions in tests
- archive or downgrade the task once the main cuts are complete

### Validation

- `python -m pytest tests/campaign -q`
- `python -m pytest tests/shared/test_text_encoding_guards.py -q`

### Status

- `2026-04-18`: Phase 4 landed

## Execution Rules

- Run the plan serially, not as a broad parallel architecture rewrite
- Preserve stable shell seams unless a concrete trigger requires change
- Prefer local refactors over global symmetry
- Stop and re-scope if progress requires broad edits under:
  - `contexts/campaign/view.py`
  - `contexts/campaign/rendering/**`
  - `contexts/campaign/ui_runtime/**`
  - `contexts/shared/**`
- Update the task pool when the active phase changes
- Update the daily log when a phase lands or a stop condition appears

## Stop Conditions

Pause this plan and split a separate task if:

- the work starts requiring a `CampaignView` rewrite
- visual-runtime extraction becomes the real blocker
- task-area changes need a new track identity model
- shared infrastructure becomes necessary beyond a narrow campaign blocker

## Current Recommendation

Treat this plan as the active campaign refactor entry point.

Current status:

1. Phase 0 is complete
2. Phase 1 shell closure is complete
3. Phase 2 thesis convergence is complete
4. Phase 3 task-area internal rule split is complete
5. Phase 4 guardrails, docs, and closure is complete
6. the mainline campaign self-refactor plan is complete and should now be treated as closed reference memory
7. visual-runtime and shared cleanup remain explicitly out of scope for now
