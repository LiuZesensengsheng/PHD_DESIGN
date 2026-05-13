# Project Memory Index

This file is the entry point for project memory.

## Purpose

Use this index to decide where to read and where to write project knowledge.

## Source Of Truth By Layer

### Short-Term Memory

- `docs/logs/daily/YYYY-MM-DD.md`
- Use for current progress, handoff notes, blockers, and next steps
- Keep default retrieval focused on the most recent 7 days

### Long-Term Memory

- `docs/development/**/*.md`
- Use for architecture boundaries, working rules, stable design constraints, and workflow agreements
- Use `docs/development/README.md` as the directory map for long-term memory docs
- Use `docs/development/DEFAULT_ENTRYPOINTS.md` as the default memory source for recurring tooling commands
- Use `docs/development/PROJECT_MEMORY_HEALTH_V1.md` as the source of truth for
  memory-scaffold health checks and escalation rules
- Use `docs/development/PROJECT_MEMORY_DIGEST_V1.md` as the source of truth for the
  read-only hot-memory recovery digest

### Tool-Local Subsystems

- `tools/<name>/README.md`
- Use for serious analysis/design subsystems that are expected to hold both living docs
  and executable code later
- Register only the subsystem entrypoint here; do not duplicate the full internal spec in
  both `docs/` and `tools/`
- Current registered subsystem:
  - `tools/combat_analysis/README.md`
  - source-of-truth entry for the combat-analysis model
  - `tools/delivery_tracker/README.md`
  - source-of-truth entry for the delivery-tracker model and generated current-report flow

### Weekly Memory

- `docs/logs/weekly/YYYY-Www.md`
- Use for compressed weekly summaries, promotion suggestions, and older-context recovery without reopening many daily logs

### Monthly Memory

- `docs/logs/monthly/YYYY-MM.md`
- Use for cross-month recovery, major progress, capability changes, open gaps, and promotion suggestions
- Use monthly summaries before reopening many old weekly summaries or cold daily logs

### Task Pool

- `docs/development/CODEX_TASK_POOL.md`
- Use for work suitable for long, independent Codex execution

### Decision Memory

- `docs/pm/DECISION_LOG.md`
- Use for important decisions, tradeoffs, and rollback notes

### Skill Layer

- External skill definitions under the Codex skills directory
- Use for reusable methods and workflows only

## Recommended Read Order

1. `AGENTS.md`
2. `docs/development/CURRENT_DIRECTION.md`
3. Relevant architecture or workflow documents in `docs/development/` subdirectories
4. `docs/pm/DECISION_LOG.md` if the task changes direction, scope, or architecture
5. `docs/logs/daily/<today>.md`
6. The most recent prior daily log with useful context
7. The most recent weekly summary with useful context
8. The latest monthly summary when recovering context across month boundaries

## Development Directory Map

- `docs/development/architecture/`: cross-cutting architecture, save policy, UI, DDD, EEE, and boundary docs
- `docs/development/campaign/`: campaign runtime, UI, lifecycle, task-area, and campaign-analysis docs
- `docs/development/cardanalysis/`: case-backed design-analysis contracts, evidence libraries, mechanism axes, and advisory model docs
- `docs/development/combat/`: combat runtime contracts, gates, compatibility plans, and automation backlogs
- `docs/development/content/`: formal content-data contracts and balance baselines
- `docs/development/narrative/`: narrative pipeline, source schema, instance model, and task tables
- `docs/development/platform/`: repository tooling, smoke baselines, data pipeline guardrails, and test strategy
- `docs/development/thesis/`: thesis-specific lifecycle, write-path, verdict, and aggregate docs

## Recommended Write Rules

- Write daily progress into the dated daily log
- Write compressed weekly context into `docs/logs/weekly/`
- Write cross-month progress and capability-state context into `docs/logs/monthly/`
- Write stable conclusions into the relevant `docs/development/` subdirectory
- When a subsystem's detailed spec is expected to grow code, keep its local source of
  truth under `tools/<name>/` and register its `README.md` entrypoint here
- Write decision outcomes into `docs/pm/DECISION_LOG.md`
- Write independent AI-executable work into `docs/development/CODEX_TASK_POOL.md`
- Do not store current branch status or recent progress in skill bodies

## Command Recovery

- Use `docs/development/DEFAULT_ENTRYPOINTS.md` for recurring command memory.
- Use `python scripts/show_project_memory_digest.py` for a compact hot-memory recovery
  snapshot after branch switches or merges.
- Use `python scripts/check_project_memory_health.py` when memory scaffolding may have
  drifted after high-velocity work.
- Use the hot-memory read order above for project context recovery.
