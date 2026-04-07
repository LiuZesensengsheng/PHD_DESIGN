# Default Entrypoints

## Goal

Keep recurring project operations easy to remember for humans and Codex.

Prefer direct tests or single-purpose scripts over umbrella entrypoints.

## Default Rule

- Prefer direct scripts, direct tests, and focused workflow docs for routine work.
- When a task has a stable direct test or script, record that direct command here and in relevant workflow docs.

## Current Default Entrypoints

### Environment Setup

- Install runtime dependencies:
  - `py -3.11 -m pip install -r requirements.txt`
- Install development dependencies:
  - `py -3.11 -m pip install -r requirements-dev.txt`
- Install build-only dependencies:
  - `py -3.11 -m pip install -r requirements-build.txt`

### Repository Smoke Baseline

- Run the default repo-wide smoke baseline:
  - `python scripts/run_repo_smoke_baseline.py`
- List the included smoke groups:
  - `python scripts/run_repo_smoke_baseline.py --list`
- Run one smoke group only:
  - `python scripts/run_repo_smoke_baseline.py --group <group>`

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

### Combat Analysis

- Generate the profile-aware combat-analysis reference report:
  - `python scripts/generate_combat_analysis_reference_report.py --profile-id <profile-id>`
- Generate the cross-profile combat-analysis portfolio understanding report:
  - `python scripts/generate_combat_analysis_portfolio_report.py`
- Write a reviewed Design Loop v1 input template:
  - `python scripts/run_combat_analysis_design_loop.py --write-template <path>`
- Run a local Design Loop v1 review from a reviewed JSON input:
  - `python scripts/run_combat_analysis_design_loop.py --input <path> --output-dir <dir>`
- Scaffold a new character profile file without registering it:
  - `python scripts/scaffold_combat_analysis_profile.py --family sts1 --character-id <id> --display-name <中文名>`
- Validate the profile scaffold script:
  - `python -m pytest tests/scripts/test_scaffold_combat_analysis_profile.py -q`
- Validate Design Loop v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_loop.py tests/scripts/test_run_combat_analysis_design_loop.py -q`

### Headless / Regression Checks

- Run headless regression helpers:
  - `python scripts/run_headless_tests.py`
- Run targeted pytest coverage:
  - `python -m pytest <path-or-test> -q`

### Architecture / Encoding Guardrails

- Validate architecture boundaries:
  - `python scripts/validate_architecture.py`
- Run campaign simplification guardrails:
  - `python -m pytest tests/campaign/test_campaign_simplification_guardrails_v1.py -q`
- Run static contract and naming guards:
  - `python -m pytest tests/test_contract_police.py tests/shared/test_naming_and_contract_guards.py -q`
- Run text encoding and line-ending guards:
  - `python -m pytest tests/shared/test_text_encoding_guards.py -q`

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
