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

- Show the current project memory recovery digest:
  - `python scripts/show_project_memory_digest.py`
- Export the project memory recovery digest as JSON:
  - `python scripts/show_project_memory_digest.py --json`
- Validate the project memory digest contract:
  - `python -m pytest tests/scripts/test_show_project_memory_digest.py -q`
- Run the project memory health report:
  - `python scripts/check_project_memory_health.py`
- Run the project memory health report in strict mode:
  - `python scripts/check_project_memory_health.py --strict`
- Export the project memory health report as JSON:
  - `python scripts/check_project_memory_health.py --json`
- Validate the current project memory health contract:
  - `python -m pytest tests/scripts/test_check_project_memory_health.py -q`
- Validate the weekly summary generator:
  - `python -m pytest tests/scripts/test_generate_weekly_summary.py -q`
- Generate a specific weekly summary draft directly:
  - `python scripts/generate_weekly_summary.py --year <year> --week <week>`

### Delivery Tracker

- Generate the current delivery markdown/json report:
  - `python scripts/generate_delivery_report.py`
- Generate the current delivery report for a specific focus horizon:
  - `python scripts/generate_delivery_report.py --focus-horizon <internal_playtest|closed_test|ea_launch|v1_0|future>`

### Card Data Pipeline

- Regenerate active card runtime JSON:
  - `python scripts/cards_csv_to_json.py --generate-all-colors`
- Validate card generation contracts:
  - `python -m pytest tests/scripts/test_cards_csv_to_json.py -q`
- Validate active content/data pipeline contracts:
  - `python -m pytest tests/scripts/test_data_pipeline_contracts.py -q`

### Narrative Pipeline

- Validate tutorial narrative draft input:
  - `python scripts/validate_narrative_draft.py --draft data/narrative_drafts/tutorial/questline_tutorial.draft.json`
- Import tutorial draft into normalized source:
  - `python scripts/import_narrative_draft_to_src.py --draft data/narrative_drafts/tutorial/questline_tutorial.draft.json --out-dir data/narrative_src/packs/tutorial`
- Check source -> runtime parity for tutorial questline:
  - `python scripts/build_narrative_runtime.py --pack-dir data/narrative_src/packs/tutorial --output data/questlines/questline_tutorial.json --check`
- Check all narrative source packs against runtime outputs (with collision checks):
  - `python scripts/build_narrative_runtime.py --all --pack-root data/narrative_src/packs --check`

### Combat Analysis

- Read the combat-analysis subsystem entrypoint:
  - `tools/combat_analysis/README.md`
- Read the detailed combat-analysis command runbook:
  - `tools/combat_analysis/docs/COMBAT_ANALYSIS_ENTRYPOINTS_V1.md`
- Read cardanalysis north star, case input contract, report-only registry, and validation matrix:
  - `docs/development/cardanalysis/CARDANALYSIS_NORTH_STAR_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_REPORT_ONLY_SURFACE_REGISTRY_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`
- Run the profile-aware combat-analysis reference report:
  - `python scripts/generate_combat_analysis_reference_report.py --profile-id <profile-id>`
- Run the cross-profile combat-analysis portfolio report:
  - `python scripts/generate_combat_analysis_portfolio_report.py`
- Run the report-only cardanalysis evidence quality audit:
  - `python scripts/run_cardanalysis_evidence_quality_audit.py --input tests/fixtures/combat_analysis/source_followup_case_library_v1 --input tests/fixtures/combat_analysis/mechanism_case_library_v1 --output-dir tmp/combat_analysis/evidence_quality_audit_current`
- Run the report-only mechanism axis search bundle:
  - `python scripts/run_mechanism_axis_search.py --input tests/fixtures/combat_analysis/mechanism_axis_search_v1/silent_high_agency_visible_clock_v1.json --output-dir tmp/combat_analysis/mechanism_axis_search_current`
- Write the constrained design brief from the current mechanism axis search snapshot:
  - `python scripts/run_mechanism_axis_design_brief.py --input tmp/combat_analysis/mechanism_axis_search_current/silent_sts1_reviewed_axes_328508221e_mechanism_axis_search_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_design_brief_current`
- Write a role-level card package proposal seed from the current mechanism axis design brief:
  - `python scripts/run_mechanism_axis_package_seed.py --input tmp/combat_analysis/mechanism_axis_design_brief_current/silent_sts1_reviewed_axes_328508221e_design_brief_mechanism_axis_design_brief_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_package_seed_current`
- Validate the generated package seed against `card_package_proposal_v1`:
  - `python scripts/validate_card_package_proposal.py --input tmp/combat_analysis/mechanism_axis_package_seed_current --json`
- Run the mechanism axis report-only chain exam:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_report_only_chain_v1.py -q`
- Write an evaluation-autonomous-design handoff input from the current package seed:
  - `python scripts/run_mechanism_axis_evaluation_handoff.py --input tmp/combat_analysis/mechanism_axis_package_seed_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1.json --output-dir tmp/combat_analysis/mechanism_axis_evaluation_handoff_current`
- Run the evaluation autonomous design model from that handoff:
  - `python scripts/run_evaluation_autonomous_design_model.py --input tmp/combat_analysis/mechanism_axis_evaluation_handoff_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff.json --output-dir tmp/combat_analysis/evaluation_autonomous_design_from_axis_handoff_current`
- Write a report-only owner-report request packet from the current evaluation handoff:
  - `python scripts/run_mechanism_axis_owner_report_requests.py --input tmp/combat_analysis/mechanism_axis_evaluation_handoff_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff.json --output-dir tmp/combat_analysis/mechanism_axis_owner_report_requests_current`
- Write a report-only owner-report input readiness plan from the current request packet:
  - `python scripts/run_mechanism_axis_owner_report_input_plan.py --input tmp/combat_analysis/mechanism_axis_owner_report_requests_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_report_requests_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_report_input_plan_current`
- Validate and query the cardanalysis capability dependency/conflict graph:
  - `python scripts/validate_capability_graph.py`

### Headless / Regression Checks

- Run headless regression helpers:
  - `python scripts/run_headless_tests.py`
- Run targeted pytest coverage:
  - `python -m pytest <path-or-test> -q`

### Architecture / Encoding Guardrails

- Validate architecture boundaries:
  - `python scripts/validate_architecture.py`
- Validate resource contract boundaries:
  - `python scripts/check_resource_contracts.py`
- Check asset manifest/enums consistency:
  - `python scripts/check_asset_manifest_consistency.py`
  - strict mode (fail on drift): `python scripts/check_asset_manifest_consistency.py --strict`
- Run campaign simplification guardrails:
  - `python -m pytest tests/campaign/test_campaign_simplification_guardrails_v1.py -q`
- Run static contract and naming guards:
  - `python -m pytest tests/test_contract_police.py tests/shared/test_naming_and_contract_guards.py -q`
- Run text encoding and line-ending guards:
  - `python scripts/check_text_encoding.py`
- Validate text encoding and line-ending guard contracts:
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
