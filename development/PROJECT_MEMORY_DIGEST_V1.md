# Project Memory Digest V1

## Goal

Provide a read-only recovery snapshot for humans and Codex before starting a
non-trivial task.

The digest does not replace the canonical memory files. It collects the current hot
memory into one compact view so a new session can quickly decide what to read next.

## Default Entrypoint

```bash
python scripts/show_project_memory_digest.py
```

Use JSON mode when another tool needs to consume the same recovery view:

```bash
python scripts/show_project_memory_digest.py --json
```

Validate the digest contract with:

```bash
python -m pytest tests/scripts/test_show_project_memory_digest.py -q
```

## What It Includes

- project memory health summary
- current north star and priorities
- active task-pool titles
- latest daily log path, blockers, and next steps
- latest weekly summary path, key decisions, and next direction
- latest monthly summary path, capability changes, current state, and next direction
- latest decision-log entries

## What It Does Not Do

- It does not modify files.
- It does not replace `AGENTS.md` read-order rules.
- It does not decide which facts should be promoted.
- It does not read cold daily logs by default.
- It does not validate commands or run tests.

## Recommended Use

Run the digest:

- before starting a long Codex task
- after switching branches
- after merging a memory-heavy branch
- when deciding which source-of-truth docs to open next

If the digest reports memory-health warnings, run:

```bash
python scripts/check_project_memory_health.py
```

and handle the concrete actions there before trusting the hot-memory view.
