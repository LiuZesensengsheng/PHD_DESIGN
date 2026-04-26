# Project Memory Rules

## Goal

Keep project continuity in files so AI and human collaborators can resume work without relying on chat history.

## Rules

### 1. Daily Logs Are Short-Term Memory

- One file per day under `docs/logs/daily/`
- File name format: `YYYY-MM-DD.md`
- Daily logs store:
  - current goals
  - completed work
  - blockers
  - next steps
  - promotion candidates for long-term memory
- Daily logs should stay short and operational; do not let them grow into design documents

### 1.5 Weekly Summaries Compress Short-Term Memory

- One file per week under `docs/logs/weekly/`
- File name format: `YYYY-Www.md`
- Weekly summaries compress the last 7 days into:
  - week focus
  - major progress
  - key decisions
  - current blockers
  - next default direction
  - promotion suggestions
- Prefer reading a recent weekly summary before opening many older daily logs

### 2. Long-Term Memory Stays In Stable Docs

- Architecture and process rules belong in `docs/development/`
- Important decisions belong in `docs/pm/DECISION_LOG.md`
- Do not turn daily logs into large design documents
- Default recurring commands should live in `docs/development/DEFAULT_ENTRYPOINTS.md`, not in chat memory

### 2.5 Tool-Local Subsystems Can Own Detailed Living Specs

- When an analysis/design area is expected to gain executable code, its detailed local
  spec may live under `tools/<name>/`
- The tool-local `README.md` is the entrypoint for that subsystem
- `docs/development/` should keep the stable project-wide rule or discovery pointer, not
  a duplicated copy of the subsystem's full internal model
- Register the subsystem entrypoint in `docs/development/PROJECT_MEMORY_INDEX.md`

### 3. Skills Store Methods, Not State

- Skills should define repeatable workflows
- Skills should not become a copy of current project structure or branch progress
- If a skill needs project context, it should read docs instead of embedding them

### 4. Promote Only Stable Facts

Promote a fact from daily logs into long-term memory only when it is:

- repeated across days, or
- a real architectural decision, or
- a working rule that future tasks should follow by default

Promotion targets should stay explicit:

- long-term direction -> `docs/development/CURRENT_DIRECTION.md`
- key tradeoffs -> `docs/pm/DECISION_LOG.md`
- stable workflow or architecture rules -> relevant file in `docs/development/`

### 5. Read Selectively

- Read today's daily log first
- Then read the most recent prior daily log with useful content
- Then read the most recent weekly summary when older context is needed
- Do not load all history unless the task truly requires it
- Treat daily logs older than 7 days as cold memory by default

### 5.5 Hot vs Cold Memory

- Hot memory:
  - `AGENTS.md`
  - `docs/development/CURRENT_DIRECTION.md`
  - relevant `docs/development/*.md`
  - `docs/pm/DECISION_LOG.md`
  - daily logs from the last 7 days
  - the most recent weekly summary
- Cold memory:
  - daily logs older than 7 days
  - older weekly summaries not needed for the current task
- Cold memory remains in the repo; it is not deleted, only deprioritized for default retrieval

### 6. Branch Naming Stays Predictable

- Default Codex branch naming convention is `codex/MM-DD-topic`
- Prefer short topic names that describe the work, for example:
  - `codex/03-10-red-white-fix`
  - `codex/03-10-enemy-balance-v1`
- Use the date without the year unless there is a specific reason to disambiguate

### 7. Memory Health Checks Stay Report-First

- Use `python scripts/check_project_memory_health.py` to inspect the health of the
  file-based memory scaffold.
- Default mode should warn about drift without blocking unrelated product work.
- Use `--strict` only for dedicated memory-maintenance passes.
- Promote a warning into a hard-fail rule only after it is stable, low-noise, and has
  an obvious fix path.
- Keep the source-of-truth policy in `docs/development/PROJECT_MEMORY_HEALTH_V1.md`.

## Default Workflow

### Night Planning

- Record the day's outcome in the current daily log
- Generate or refresh the weekly summary when the week closes
- Promote any stable decisions into the right long-term document
- Leave a concrete next-step note for the next session
- Run the project memory health report when the session had heavy doc, task-pool, or
  decision-log churn

### Daytime Execution

- Read `AGENTS.md`
- Read relevant long-term docs
- Read today's log and the most recent prior useful log
- Execute against the recorded plan
- For recurring tooling tasks, prefer the direct command documented in `docs/development/DEFAULT_ENTRYPOINTS.md`; do not recreate a default umbrella CLI
