# Project Memory Health V1

## Goal

Keep the lightweight file-based project memory system observable without turning it into
a heavy platform or a noisy merge gate.

This health check answers:

- are the core memory files still present?
- are hot-memory entrypoints still cross-linked?
- is the daily/weekly memory cadence drifting?
- is the current monthly recovery summary present?
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

## Test-Backed Contract

The script owns reusable analysis logic and the human/automation CLI. Pytest owns the
current-repository health contract.

- `tests/scripts/test_check_project_memory_health.py` calls `analyze_project_memory(...)`
  against the real checkout and expects `0 fail / 0 warning`.
- fixture-style tests in the same file cover missing logs, missing core files, strict
  mode, JSON output, and handoff-section drift.
- repo-state tests derive `today` from the latest dated daily log so the contract is
  not flaky when an old branch is checked out later.

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
  - `docs/development/PROJECT_MEMORY_DIGEST_V1.md`
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
- current monthly summary presence
- whether `DEFAULT_ENTRYPOINTS.md` registers the health check
- whether `DEFAULT_ENTRYPOINTS.md` registers the memory digest
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
- It does not make weekly or monthly summary generation automatic.
- It does not introduce a database, vector store, or separate memory platform.

## Recommended Use

Run this check:

- before ending a high-velocity session
- before starting or closing a dedicated memory-summary or memory-system
  maintenance branch
- after changing `AGENTS.md`, `PROJECT_MEMORY_INDEX.md`, `PROJECT_MEMORY_RULES.md`,
  `DEFAULT_ENTRYPOINTS.md`, `CODEX_TASK_POOL.md`, or monthly/weekly/daily log rules
- before deciding whether a memory warning should be promoted into a hard guardrail

## Daily Log Branch Guard

Use the separate daily-log branch policy guard to keep normal implementation PRs
from touching high-conflict daily logs:

```bash
python scripts/check_daily_log_branch_policy.py --base-ref origin/master
```

Dedicated memory-summary branches should make their exception explicit:

```bash
python scripts/check_daily_log_branch_policy.py --base-ref origin/master --allow-daily-log
```

This guard is intentionally separate from the health check. Health checks answer
whether the memory scaffold is recoverable; the branch policy guard answers
whether the current PR is changing the right class of files.

## Oversized Daily Log Response

When a hot daily log is oversized:

1. Confirm a weekly bridge exists for that week.
2. Replace the daily log with a concise handoff summary.
3. Move stable facts into the relevant long-term docs, decision log, task pool, or
   weekly summary.
4. Keep a `Compression Notes` section that says the original detailed log remains
   recoverable from git history.
5. Do not create a new long-term document merely to preserve transient execution detail.

## Escalation Rule

Keep new checks report-only until they satisfy all of these:

- the rule is stable across at least a few sessions
- false positives are rare
- the fix is obvious from the report
- the failure would materially hurt project resumption or scope control

Only then consider adding the check to a hard-fail validation pack.
