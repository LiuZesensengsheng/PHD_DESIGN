# Project Wiki

- Status: Active
- Owner: Team
- Scope: human-facing-project-index
- Canonical: No
- Supersedes: none
- Superseded By: none
- Implemented In: none
- Last Reviewed: 2026-05-17

## Purpose

This wiki is a friendly navigation layer. It points to source-of-truth docs, but it does not replace them.

Use it when you want to answer:

- What should I read first?
- Which docs are current enough to trust?
- Where do design, architecture, data, and validation live?

## Start Here

| Need | Read |
| --- | --- |
| Current project direction | [CURRENT_DIRECTION.md](../development/CURRENT_DIRECTION.md) |
| Design overview | [Design Wiki](design.md) |
| Development docs map | [development/README.md](../development/README.md) |
| Default commands | [DEFAULT_ENTRYPOINTS.md](../development/DEFAULT_ENTRYPOINTS.md) |
| Active Codex task queue | [CODEX_TASK_POOL.md](../development/CODEX_TASK_POOL.md) |
| Project memory rules | [PROJECT_MEMORY_INDEX.md](../development/PROJECT_MEMORY_INDEX.md) |

## Source Of Truth Rules

- Wiki pages are indexes and summaries.
- Stable architecture and workflow rules live under `docs/development/`.
- Durable decisions live in `docs/pm/DECISION_LOG.md`.
- Design intent and design status live under `docs/design/`.
- Runtime behavior lives in code, data, and tests.

When the wiki and a source-of-truth doc disagree, trust the source-of-truth doc and update the wiki.
