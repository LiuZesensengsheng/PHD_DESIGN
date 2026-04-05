# Campaign Simplification Plan V1

## Goal

Improve campaign-side architectural simplicity without reopening a broad UI
rewrite, a full DDD promotion pass, or a node-tree migration campaign.

This plan is about making the current mixed-mode architecture easier to read,
safer to extend, and cheaper to maintain.

## Why Now

Recent combat cleanup improved simplicity by deleting compat shims and fallback
paths instead of layering more abstraction on top of them.

Campaign should follow the same pattern:

- delete residual compatibility paths
- tighten stable host seams
- split mixed-responsibility hotspots only where ROI is clear
- keep runtime UI growth local

## North-Star Rule

Prefer:

`delete old path -> guard the seam -> split by responsibility -> grow locally`

Do not prefer:

`add a broad abstraction first and hope the code feels simpler later`

## Non-Goals

- No whole-campaign facade
- No full `CampaignView` rewrite
- No full runtime-node migration
- No repository-everywhere cleanup
- No purity-driven `Track` aggregate promotion

## What "Simplicity" Means Here

This plan treats simplicity as a combination of:

1. fewer parallel execution paths
2. narrower host responsibilities
3. fewer mixed-responsibility service modules
4. clearer UI/runtime vs business/orchestration ownership
5. executable guardrails that stop drift early

## Current Problem Types

### 1. Parallel Path Residue

The highest-cost complexity is not file length by itself.

The highest-cost complexity is when one business outcome can still happen through:

- a mainline path
- a compatibility wrapper
- a fallback branch
- a silent fabricate-success path

### 2. Host Composition Noise

`CampaignState` should remain the shell host, but the current composition surface
is still heavy enough to raise entry cost for both humans and Codex.

### 3. Mixed-Responsibility Hotspots

Some service modules still mix multiple reasons to change.

Current known hotspots:

- `MeetingService`
- `TrackBlockService`
- `CampaignMouseEventService`
- `ThesisMetaService`
- `ThesisSlice`

### 4. Runtime/UI Boundary Drift Risk

`ui_runtime` is allowed to grow local widget/runtime structure.
It must not become a new business-rule dumping ground.

## Phase 0 Deliverables

Phase 0 is the setup phase.

It is complete when all of the following exist:

1. this plan document
2. an active task entry in `docs/development/CODEX_TASK_POOL.md`
3. at least one executable simplification guardrail test
4. default smoke coverage for that guardrail

Current status:

- `2026-04-05`: Phase 0 landed
- `2026-04-05`: Phase 1 landed
- `2026-04-05`: Phase 2 landed
- `2026-04-05`: Phase 3 landed
- `2026-04-05`: Phase 4 landed
- `2026-04-05`: the mainline simplification pass is effectively complete through Phase 4
- `2026-04-05`: Phase 5 moved to triggered backlog; do not auto-start it without near-term board-rule pressure

## Baseline Snapshot

The current simplification baseline is:

- `CampaignState`: shell host with stable `request_*` seams retained
- `CampaignView`: still large, but not the primary simplification target now
- `ThesisMetaService`: narrowed once already, but still a hotspot
- `TrackBlockService`: real hotspot, intentionally deferred for broad abstraction
- `CampaignMouseEventService`: short file, but still a mixed adapter/orchestration seam

Hotspot touch counts recorded in `CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`:

- `ThesisMetaService`: `56`
- `TrackBlockService`: `38`
- `CampaignMouseEventService`: `39`
- `ThesisSlice`: `38`

These are observability metrics, not hard-fail test budgets.

## Scorecard

Track simplification progress with these five metrics:

1. residual compatibility wrapper count
2. residual fabricated-success / warn-and-continue path count
3. hotspot `self.state.*` touch counts
4. number of campaign seams protected by focused tests
5. number of new runtime/UI behaviors that stop at `CampaignState` seams instead of
   reaching into internals

Do not use raw line counts as the primary success metric.
Line counts may be tracked for context, but they are too brittle to be the main
gate.

## Phases

### Phase 1. Delete Residual Old Paths

Goal:

- hard-delete remaining compatibility wrappers
- remove stale fallback or fabricate-success paths
- keep only one real path for each active behavior

Primary areas:

- `contexts/campaign/state.py`
- `contexts/campaign/services/thesis_meta_service.py`
- `contexts/campaign/services/thesis_slice.py`
- `contexts/campaign/services/meeting_service.py`

Validation:

- `py -3.11 -m pytest tests/campaign/test_thesis_judgment_flow_service.py tests/campaign/test_meeting_events_branching.py tests/campaign/test_campaign_turn_orchestrator.py -q`
- `py -3.11 scripts/run_repo_smoke_baseline.py`

### Phase 2. Reduce CampaignState Composition Noise

Goal:

- keep `CampaignState` as the shell host
- extract service wiring/composition clutter into a helper or bundle
- preserve stable `request_*` seam methods

Validation:

- `py -3.11 -m pytest tests/campaign/test_campaign_dependency_narrowing_services.py tests/campaign/test_campaign_ui_handoff_contracts.py tests/campaign/test_campaign_transition_request_contract.py -q`
- `py -3.11 scripts/validate_architecture.py`
- `py -3.11 scripts/run_repo_smoke_baseline.py`

### Phase 3. Split MeetingService By Reason To Change

Goal:

- keep `MeetingService` as a thin orchestrator
- split selection / shop / event-flow responsibilities into focused helpers

Recommended internal targets:

- `MeetingEventSelector`
- `MeetingShopService`
- `MeetingEventFlowService`

Validation:

- `py -3.11 -m pytest tests/campaign/test_meeting_service_core.py tests/campaign/test_meeting_events_branching.py tests/campaign/test_meeting_trigger.py -q`
- `py -3.11 -m pytest tests/campaign -q`
- `py -3.11 scripts/run_repo_smoke_baseline.py`

### Phase 4. Split Mouse Input Into Intent Resolution + Dispatch

Goal:

- keep campaign click handling on the state surface
- replace one large mixed method with:
  - click intent resolution
  - click intent dispatch

Validation:

- `py -3.11 -m pytest tests/campaign/test_campaign_ui_handoff_contracts.py tests/campaign/test_campaign_runtime_ui_boundary_contract.py tests/campaign/test_campaign_block_click_orchestrator.py tests/campaign/test_campaign_end_turn_orchestrator.py -q`
- `py -3.11 scripts/run_repo_smoke_baseline.py`

### Phase 5. Split TrackBlockService Internally Only When Triggered

Trigger signals:

- board rules start blocking content iteration
- multiple services need the same board invariants
- DDL / fusion / compaction edits frequently collide

Current stance:

- keep this slice prepared, but deferred by default
- only start when one of the trigger signals becomes part of the near-term roadmap, not just a cleanliness concern

Allowed cut:

- internal policy split only

Do not do:

- broad facade campaign
- purity-driven aggregate promotion
- repository-ization of task-area runtime state

Validation:

- `py -3.11 -m pytest tests/campaign/test_track_block_service_ddl.py tests/campaign/test_track_block_service_fusion_thesis_nodes.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py -q`
- `py -3.11 scripts/run_repo_smoke_baseline.py`

### Phase 6. Grow Runtime UI Locally, Not Globally

Goal:

- let runtime widgets grow retained local structure
- stop business consequences at `CampaignState` seams

Validation:

- `py -3.11 -m pytest tests/campaign/test_campaign_runtime_ui_boundary_contract.py tests/campaign/test_campaign_ui_handoff_contracts.py -q`

## How Tests Maintain Simplicity

Tests can maintain simplicity, but only through executable proxies.

Tests are good at protecting:

- single-path ownership
- forbidden imports
- forbidden direct writes
- stable seam surfaces
- runtime/UI boundary rules
- smoke-level regression against accidental architecture drift

Tests are not good at directly scoring:

- elegance
- naming taste
- whether a split is the "best possible" split
- whether a large file is still conceptually simple

So the maintenance model should be:

1. document the simplification rule
2. encode the highest-value part as a guardrail test
3. keep a small scorecard for the parts that should be observed, not hard-failed

## Recommended Guardrail Types

### Good Hard-Fail Guardrails

- `ui_runtime` must not import campaign business services
- input adapters should stop at `CampaignState` request seams
- hotspot services should remain UI-framework-free where that boundary is stable
- deleted compatibility seams must not reappear

### Good Report-Only Metrics

- hotspot touch counts
- file lengths
- number of responsibilities inside a module

These are useful review signals, but too brittle for immediate hard-fail tests.

## Execution Rules

- Run this plan serially, not as a broad parallel architecture rewrite
- Prefer deleting code over wrapping code
- Preserve stable external seams while simplifying internals
- Update `CODEX_TASK_POOL.md` when the active phase changes
- Update the hotspot/defer docs when a phase materially changes what is safe to touch

## Current Recommendation

The project should currently treat this plan as:

1. Phase 0 through Phase 4 complete
2. Keep Phase 5 prepared but deferred until upcoming work directly touches DDL / fusion / compaction or shared board invariants
3. Let near-term campaign follow-up stay focused on active roadmap work instead of starting a cleanliness-only `TrackBlockService` refactor

That keeps the simplicity gains already landed, without reopening a real
task-area hotspot before it becomes the critical path.
