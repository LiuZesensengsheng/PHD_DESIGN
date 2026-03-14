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

- `docs/development/*.md`
- Use for architecture boundaries, working rules, stable design constraints, and workflow agreements
- Use `docs/development/DEFAULT_ENTRYPOINTS.md` as the default memory source for recurring tooling commands

### Weekly Memory

- `docs/logs/weekly/YYYY-Www.md`
- Use for compressed weekly summaries, promotion suggestions, and older-context recovery without reopening many daily logs

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
3. Relevant architecture or workflow documents in `docs/development/`
4. `docs/pm/DECISION_LOG.md` if the task changes direction, scope, or architecture
5. `docs/logs/daily/<today>.md`
6. The most recent prior daily log with useful context
7. The most recent weekly summary with useful context

## Recommended Write Rules

- Write daily progress into the dated daily log
- Write compressed weekly context into `docs/logs/weekly/`
- Write stable conclusions into `docs/development/`
- Write decision outcomes into `docs/pm/DECISION_LOG.md`
- Write independent AI-executable work into `docs/development/CODEX_TASK_POOL.md`
- Do not store current branch status or recent progress in skill bodies

## Command Recovery

- Use `docs/development/DEFAULT_ENTRYPOINTS.md` for recurring command memory.
- Use the hot-memory read order above for project context recovery.
