# Project Memory Health V1

## Goal

Keep the lightweight file-based project memory system observable without turning it into
a heavy platform or a noisy merge gate.

This health check answers:

- are the core memory files still present?
- are hot-memory entrypoints still cross-linked?
- is the daily/weekly memory cadence drifting?
- are active task-pool items still tied to sources of truth and validation?
- is command memory starting to grow beyond a useful index?

## Default Entrypoint

```bash
python scripts/check_project_memory_health.py
```

Use strict mode only when intentionally tightening process discipline:

```bash
python scripts/check_project_memory_health.py --strict
```

Use JSON mode when another script or automation needs to consume the report:

```bash
python scripts/check_project_memory_health.py --json
```

## Current Posture

The health check is **report-first** by default.

- `FAIL` means a required source-of-truth file is missing or the memory system is
  structurally broken.
- `WARN` means the system is drifting but the warning should not automatically block
  unrelated product or architecture work.
- `--strict` can treat warnings as failures for dedicated maintenance passes.
- each issue should include a concrete suggested action so warnings are actionable
  instead of vague process noise.

## What It Checks

- core memory files:
  - `AGENTS.md`
  - `docs/development/CURRENT_DIRECTION.md`
  - `docs/development/DEFAULT_ENTRYPOINTS.md`
  - `docs/development/PROJECT_MEMORY_INDEX.md`
  - `docs/development/PROJECT_MEMORY_RULES.md`
  - `docs/development/CODEX_TASK_POOL.md`
  - `docs/pm/DECISION_LOG.md`
- hot-memory cross-links in `AGENTS.md` and `PROJECT_MEMORY_INDEX.md`
- today's daily log presence
- today's daily log handoff-section shape:
  - `Today Goals`
  - `Completed`
  - `Current Blockers`
  - `Next Step`
  - `Candidate Long-Term Memory`
- latest daily log age
- oversized hot daily logs from the last 7 days
- latest weekly summary age
- whether `DEFAULT_ENTRYPOINTS.md` registers the health check
- active task-pool source-of-truth and validation expectations

## Output Modes

- Text mode is the human default.
- JSON mode exposes:
  - `root`
  - `today`
  - `fail_count`
  - `warn_count`
  - `issues[]`
- Each issue includes:
  - `severity`
  - `code`
  - `message`
  - `path`
  - `action`

## What It Does Not Do

- It does not replace human judgment about which facts deserve promotion.
- It does not read old cold logs by default.
- It does not validate every command in `DEFAULT_ENTRYPOINTS.md`.
- It does not make weekly summary generation automatic.
- It does not introduce a database, vector store, or separate memory platform.

## Recommended Use

Run this check:

- before ending a high-velocity session
- before starting a memory-system maintenance branch
- after changing `AGENTS.md`, `PROJECT_MEMORY_INDEX.md`, `PROJECT_MEMORY_RULES.md`,
  `DEFAULT_ENTRYPOINTS.md`, `CODEX_TASK_POOL.md`, or weekly/daily log rules
- before deciding whether a memory warning should be promoted into a hard guardrail

## Escalation Rule

Keep new checks report-only until they satisfy all of these:

- the rule is stable across at least a few sessions
- false positives are rare
- the fix is obvious from the report
- the failure would materially hurt project resumption or scope control

Only then consider adding the check to a hard-fail validation pack.
