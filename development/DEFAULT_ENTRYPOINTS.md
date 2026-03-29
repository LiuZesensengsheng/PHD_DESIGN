# Default Entrypoints

## Goal

Keep recurring project operations easy to remember for humans and Codex.

Prefer direct tests or single-purpose scripts over umbrella entrypoints.

## Default Rule

- Prefer direct scripts, direct tests, and focused workflow docs for routine work.
- When a task has a stable direct test or script, record that direct command here and in relevant workflow docs.

## Current Default Entrypoints

### Project Memory Maintenance

- Refresh the latest weekly summary:
  - `python -m pytest tests/scripts/test_generate_weekly_summary.py -q`
- Generate a specific weekly summary draft directly:
  - `python scripts/generate_weekly_summary.py --year <year> --week <week>`

### Card Data Pipeline

- Regenerate active card runtime JSON:
  - `python scripts/cards_csv_to_json.py --generate-all-colors`
- Validate card generation contracts:
  - `python -m pytest tests/scripts/test_cards_csv_to_json.py -q`
- Validate active content/data pipeline contracts:
  - `python -m pytest tests/scripts/test_data_pipeline_contracts.py -q`

### Headless / Regression Checks

- Run headless regression helpers:
  - `python scripts/run_headless_tests.py`
- Run targeted pytest coverage:
  - `python -m pytest <path-or-test> -q`

### Combat Mainline Gate

- Run the structural combat compat-zero precheck:
  - `python scripts/check_combat_compat_zero.py`
- Run the combat mainline allowlist gate:
  - `python -m pytest tests/combat/test_combat_mainline_allowlist_v1.py -q`

### Snapshot / Save Debugging

- Compare two machine snapshots:
  - `python scripts/diff_machine_snapshots.py <before.json> <after.json>`
- Compare two machine snapshots with path-level details:
  - `python scripts/diff_machine_snapshots.py <before.json> <after.json> --details`
- Reproduce a seeded headless main path and write snapshots:
  - `python scripts/repro_headless_flow.py <case> --seed <seed>`
- Reproduce a seeded headless main path to a custom output directory:
  - `python scripts/repro_headless_flow.py <case> --seed <seed> --output-dir <dir>`

## Project Recovery

When you need to resume project context before running commands, read:

1. `AGENTS.md`
2. `docs/development/CURRENT_DIRECTION.md`
3. today's daily log
4. the latest weekly summary when recent history matters
