# Weekly Memory Summaries

## Purpose

Use weekly summaries to compress recent daily logs into a short bridge layer for Codex and human collaborators.

## File Format

- Path: `docs/logs/weekly/YYYY-Www.md`
- One file per ISO week
- Keep each file short and decision-oriented

## Required Sections

- `Week Focus`
- `Major Progress`
- `Key Decisions`
- `Current Blockers`
- `Next Default Direction`
- `Promotion Suggestions`

## Retrieval Rules

- Read the most recent weekly summary when older context is needed beyond the current daily log and the most recent useful prior daily log.
- Weekly summaries are preferred over reading many older daily logs.
- Older daily logs remain in the repo, but weekly summaries are the default compressed entry point.

## Maintenance Rules

- Generate a weekly summary from recent daily logs instead of rewriting history from scratch.
- Keep only the last 2-4 weekly summaries in the default hot retrieval set.
- Do not promote everything from a weekly summary into long-term docs; only move repeated or clearly stable facts.

## Automation

- Use `python scripts/generate_weekly_summary.py --year <year> --week <week>` to generate a draft summary for a target ISO week.
- `python -m pytest tests/scripts/test_generate_weekly_summary.py -q` now acts as a lightweight maintenance check:
  - if the latest week's daily logs changed, it rewrites that weekly summary automatically
  - if nothing changed, the maintenance test skips itself
- The script is allowed to suggest promotion candidates, but it should not rewrite long-term docs automatically.
