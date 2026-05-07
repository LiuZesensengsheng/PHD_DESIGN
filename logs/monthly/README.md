# Monthly Memory Summaries

## Purpose

Use monthly summaries as the cross-month recovery layer between weekly summaries and long-term development docs.

Monthly summaries should answer:

- what materially changed this month?
- which capabilities grew or became usable?
- which decisions, PRs, or docs matter later?
- what still blocks the long-term goals?
- which facts should be promoted into `docs/development/` or `docs/pm/DECISION_LOG.md`?

## File Format

- Path: `docs/logs/monthly/YYYY-MM.md`
- One file per calendar month
- Keep each file compact, outcome-oriented, and readable without opening many daily logs

## Required Sections

- `Month Focus`
- `Major Progress`
- `Capability Changes`
- `Key Decisions`
- `Current State`
- `Open Gaps`
- `Next Default Direction`
- `Promotion Suggestions`

## Retrieval Rules

- Read the latest monthly summary when weekly summaries are not enough or when recovering context across month boundaries.
- Monthly summaries are preferred over reading many old weekly summaries or old daily logs.
- Daily logs older than 7 days and older weekly summaries remain in the repo, but monthly summaries are the default cold-memory bridge.

## Maintenance Rules

- Update the current month summary after major integration, evidence, architecture, or planning milestones.
- Do not move old daily logs into monthly directories unless a later explicit archive policy is accepted.
- Do not promote everything from a monthly summary into long-term docs; promote only stable facts, decisions, or workflow rules.
- Keep implementation details and command transcripts out of monthly summaries unless they change recovery behavior.
