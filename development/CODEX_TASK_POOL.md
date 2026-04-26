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

### A1. Campaign Boundary Hardening V1

- Goal:
  - harden the current campaign architecture around lifecycle ownership,
    trigger/forced-event ownership, direct seam policy, and executable
    guardrails
  - keep campaign shell behavior stable without reopening broad cleanup or
    directory-purity work
- Source of truth:
  - `docs/development/CAMPAIGN_BOUNDARY_HARDENING_V1.md`
  - `docs/development/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md`
  - `docs/development/CAMPAIGN_INTERRUPT_GATE_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_LIFECYCLE_MACHINE_V1.md`
  - `docs/development/CAMPAIGN_LIFECYCLE_READ_SURFACE_V1.md`
  - `docs/development/CAMPAIGN_TURN_LOOP_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_RETURN_RESOLUTION_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_STARTUP_CONTRACT_V1.md`
  - `docs/development/CAMPAIGN_DIRECT_SEAM_POLICY_V1.md`
  - `docs/development/CAMPAIGN_RUNTIME_UI_BOUNDARY_V1.md`
- Current status:
  - decision-frozen on `2026-04-24`
  - `Phase 1` lifecycle contract closure completed on `2026-04-24`
  - turn-loop, return-resolution, standalone interrupt-gate, and startup
    nested interrupt-gate result surfaces are now explicit
  - the UI-facing end-turn host seam now also preserves the explicit
    turn-cycle result through `request_end_turn_result()`
  - `py -3.11 -m pytest tests/campaign -q` passed for the `Phase 1` close
  - `Phase 2` trigger and forced-event boundary closure completed on
    `2026-04-24`
  - forced-event owner closure now includes:
    - a curated import/reference guardrail that keeps stable non-presentation
      forced-event owners free of direct `gossip_modal` references and
      presenter imports
    - fail-closed runtime gate semantics that preserve explicit `active`
      ownership during presenter-probe failure and no-presenter retry paths
  - `py -3.11 -m pytest tests/campaign -q` passed for the `Phase 2` close
  - `Phase 3` campaign boundary gates completed on `2026-04-24`
  - the phase-close validation pack passed:
    - `py -3.11 -m pytest tests/campaign -q`
  - the first `Phase 3` hard-fail guardrail locked explicit lifecycle result
    seams on the startup/end-turn/state host path
  - a second `Phase 3` hard-fail guardrail now keeps `CampaignState` direct
    service alias installation whitelist-based:
    - stable shell/runtime ports remain direct
    - reward/thesis/social families stay grouped-only
    - optional `hit_test_service` review-next status is preserved without
      freezing it as a permanent seam
  - a third `Phase 3` hard-fail guardrail now keeps turn timing ownership out
    of frame/event-ingress paths:
    - keyboard/mouse/ui-button ingress stays on
      `CampaignState.request_end_turn*()`
    - frame/event services may not reach directly into lifecycle-machine turn
      advancement
  - a fourth `Phase 3` hard-fail guardrail now keeps forced-event ownership
    split on the accepted runtime/presenter line:
    - stable non-presentation forced-event owners stay UI-framework free
    - pending/active queue state stays in runtime ownership, not presenter
  - a fifth `Phase 3` hard-fail guardrail now keeps forced-event gate wiring
    on the `CampaignState` host seam:
    - lifecycle-step gate code may not couple directly to runtime/presenter
    - `CampaignState.handle_pending_forced_campaign_event()` remains the
      stable handoff point
  - a sixth `Phase 3` hard-fail guardrail now keeps lifecycle-side trigger
    dispatch on `CampaignState` host seams:
    - lifecycle context/step files may not couple directly to
      `trigger_surface` / `trigger_reactions`
    - trigger windows and reactions continue to route through the state host
      seam
  - a seventh `Phase 3` hard-fail guardrail now keeps
    `contexts/campaign/lifecycle/**` free of direct UI-framework and
    campaign-service imports
  - forced-event narrow plan V1 already reached its intended stop line on
    `2026-04-23`
  - the mainline hard-fail guardrail baseline is now sufficient to close
    `Phase 3` without reopening broad cleanup
  - the active next move is no longer another mandatory guardrail slice; only
    the optional `Phase 4` `hit_test_service` review remains in-line
- Current rules:
  - keep the scope inside `campaign/tests/docs`
  - do not reopen `CampaignView`, visual-runtime extraction, or shared cleanup
  - do not start physical `services -> application/ui` migration in this line
  - treat `hit_test_service` as optional late-phase review only
  - keep `thesis_slice` and task-area hotspot follow-up as triggered backlog
  - hard-fail only stable boundary rules; keep touch counts/file lengths
    report-only
  - per slice:
    - run targeted validation only
    - update daily log
    - update task pool / long-term docs when phase status changes
- Validation rhythm:
  - slice level:
    - focused tests only
  - phase close:
    - `py -3.11 -m pytest tests/campaign -q`
  - line closure or explicitly high-risk phase:
    - `py -3.11 scripts/run_repo_smoke_baseline.py`

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
- Validation rhythm:
  - schema/tooling slices:
    - focused script and unit tests for the touched importer, builder, or validator
  - parity close:
    - `python scripts/build_narrative_runtime.py --all --pack-root data/narrative_src/packs --check`
    - focused acceptance tests for the active tutorial route
  - cross-context risk:
    - run the relevant campaign/cross-context smoke tests before closing the line

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
