# Project Documentation Layers V1

## Goal

Keep project continuity in files with a simple four-layer model that works for part-time development and AI collaboration.

## Layer 1. Daily Logs

- Path: `docs/logs/daily/`
- Purpose: short-term working memory
- Use for:
  - today's goals
  - completed work
  - blockers
  - next steps
- Do not use for:
  - stable architecture rules
  - long-term project principles

## Layer 2. Development Docs

- Path: `docs/development/`
- Purpose: long-term architecture and workflow memory
- Use for:
  - architecture boundaries
  - data workflows
  - UI rules
  - balance baselines
  - task pool
- Do not use for:
  - daily progress notes

## Layer 3. Decision Log

- Path: `docs/pm/DECISION_LOG.md`
- Purpose: durable decision history
- Use for:
  - major tradeoffs
  - accepted directions
  - rollback notes
- Do not use for:
  - routine implementation notes

## Layer 4. Task Pool

- Path: `docs/development/CODEX_TASK_POOL.md`
- Purpose: queue of work suitable for long independent Codex execution
- Use for:
  - tasks with clear inputs and outputs
  - work that benefits from uninterrupted execution
- Do not use for:
  - today's exact status
  - unresolved high-subjectivity design debates

## Read Order

For a non-trivial task, read in this order:

1. `AGENTS.md`
2. relevant docs in `docs/development/`
3. `docs/pm/DECISION_LOG.md` if the task changes direction or architecture
4. today's daily log
5. the most recent useful prior daily log
6. code

## Write Rules

- write current progress to the daily log
- write stable rules to `docs/development/`
- write major decisions to the decision log
- write candidate independent work to the task pool
