# Codex Task Pool

## Purpose

This file is the hot task index for Codex collaboration.

It answers only a few questions:

- which tasks are currently worth active Codex time
- which source-of-truth docs define the rollout
- what the expected output looks like
- what is blocked, queued, or already closed

Detailed implementation history belongs in:

- `docs/logs/daily/`
- `docs/logs/weekly/`
- `docs/development/task_pool_archive/`

This file is not:

- a daily log
- a decision log
- a full architecture spec

## How To Use

Before starting a non-trivial task, confirm:

1. The task still matches current priorities.
2. The source-of-truth doc exists and is stable enough to execute from.
3. The validation target is clear.
4. The task can progress without constant product/visual judgment calls.

## Selection Rules

Prefer handing work to Codex when:

- inputs are explicit
- expected outputs are explicit
- validation is automatable
- the task does not depend on high-frequency subjective visual review

Do not treat a task as a long-running Codex lane when it is mainly:

- pure visual polish
- final narrative tone tuning
- high-subjectivity UX balancing
- exploratory work with no stable acceptance criteria

## Active Tasks

### A1. Campaign Lifecycle And Forced-Event Narrowing

- Goal:
  - continue campaign lifecycle tightening through explicit runtime contracts,
    trigger ownership, and forced-event seams
  - keep campaign shell behavior stable while reducing hidden timing paths
- Source of truth:
  - `docs/development/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md`
  - `docs/development/CAMPAIGN_LIFECYCLE_MACHINE_V1.md`
  - `docs/development/CAMPAIGN_LIFECYCLE_READ_SURFACE_V1.md`
  - `docs/development/CAMPAIGN_TURN_LOOP_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_RETURN_RESOLUTION_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_STARTUP_CONTRACT_V1.md`
- Current status:
  - forced-event narrow plan V1 reached its intended stop line on `2026-04-23`
  - lifecycle result and snapshot surfaces are now explicit
  - further work should stay narrow and contract-driven
- Boundaries:
  - do not widen into a full interrupt platform rewrite
  - do not reopen `CampaignView` or visual-runtime work
  - do not redesign save compatibility in the same slice

### A2. Narrative Pipeline V1

- Goal:
  - build a stable `draft -> normalized source -> build -> runtime -> acceptance`
    pipeline for narrative content
- Source of truth:
  - `docs/development/NARRATIVE_PIPELINE_V1.md`
  - `docs/development/NARRATIVE_PIPELINE_TASK_TABLE_V1.md`
  - `docs/development/DATA_PIPELINE_GUARDRAILS_V1.md`
- Current rules:
  - keep `data/questlines/*.json` as the active runtime path during migration
  - do not grow new content in legacy campaign-event JSON paths
  - prefer serial rollout over competing architecture branches
- Expected output:
  - normalized narrative source schema
  - source/build tooling
  - tutorial-path parity proof
  - acceptance tests for the active narrative route

## Queued Tasks

### Q1. Combat Post-Compat Follow-Ups

- Status:
  - `Combat Global Compat-Zero` is complete at `Engineering Zero`
  - follow-up work must start as separate, decision-gated lines
- Likely next topics:
  - energy contract convergence
  - save lifecycle or schema redesign
  - dead scaffold cleanup
- Source of truth:
  - `docs/development/COMBAT_AUTOMATION_BACKLOG_V1.md`
  - `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
  - `docs/pm/DECISION_LOG.md`
- Do not mix into these follow-ups:
  - red content/runtime bug fixes
  - animation or video blocking semantics
  - `combat_view` behavior changes

### Q2. Resource Guardrail Convergence V1

- Goal:
  - continue narrowing asset/resource entrypoints behind stable guardrails
- Source of truth:
  - `scripts/check_resource_contracts.py`
  - `scripts/check_asset_manifest_consistency.py`
  - `scripts/run_repo_smoke_baseline.py`
- Reason it is queued:
  - the guardrail base exists
  - remaining work is mostly engineering debt reduction, not current P0 product risk

### Q3. Combat Analysis Next Cycle

- Status:
  - the prior V1 iteration is closed
  - the next cycle should be reopened only after a clearer benchmark gap or
    reviewed sample set appears
- Default rule:
  - keep using `source facts -> reviewed annotation -> projection`
  - avoid premature shared semantics until repeated patterns justify them

## Closed Reference Tasks

These are intentionally not the default next move. Keep them as reference memory.

### C1. Combat Global Compat-Zero

- Source of truth:
  - `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
  - `docs/development/COMBAT_RUNTIME_SURFACE_INVENTORY_V1.md`
  - `docs/pm/DECISION_LOG.md`
- Closure status:
  - `G1 -> G5` completed on `2026-04-23`
  - the mainline is closed at `Engineering Zero`

### C2. Campaign Simplification V1

- Source of truth:
  - `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md`
- Closure status:
  - mainline complete through `Phase 4`
  - `Phase 5` is triggered backlog only

### C3. Campaign Self Refactor V1

- Source of truth:
  - `docs/development/CAMPAIGN_SELF_REFACTOR_PLAN_V1.md`
- Closure status:
  - mainline complete through `Phase 4`
  - treat as closed reference memory, not a default next action

## Archive Rule

Move a task out of the active or queued hot zone when:

- it is complete
- it is blocked by a new decision
- it no longer matches the current production stage
- it requires ongoing high-frequency human taste judgment

For older completed task detail, use:

- `docs/development/task_pool_archive/2026-03_2026-04_completed.md`
