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

### 2. Long-Term Memory Stays In Stable Docs

- Architecture and process rules belong in `docs/development/`
- Important decisions belong in `docs/pm/DECISION_LOG.md`
- Do not turn daily logs into large design documents

### 3. Skills Store Methods, Not State

- Skills should define repeatable workflows
- Skills should not become a copy of current project structure or branch progress
- If a skill needs project context, it should read docs instead of embedding them

### 4. Promote Only Stable Facts

Promote a fact from daily logs into long-term memory only when it is:

- repeated across days, or
- a real architectural decision, or
- a working rule that future tasks should follow by default

### 5. Read Selectively

- Read today's daily log first
- Then read the most recent prior daily log with useful content
- Do not load all history unless the task truly requires it

### 6. Branch Naming Stays Predictable

- Default Codex branch naming convention is `codex/MM-DD-topic`
- Prefer short topic names that describe the work, for example:
  - `codex/03-10-red-white-fix`
  - `codex/03-10-enemy-balance-v1`
- Use the date without the year unless there is a specific reason to disambiguate

## Default Workflow

### Night Planning

- Record the day's outcome in the current daily log
- Promote any stable decisions into the right long-term document
- Leave a concrete next-step note for the next session

### Daytime Execution

- Read `AGENTS.md`
- Read relevant long-term docs
- Read today's log and the most recent prior useful log
- Execute against the recorded plan
