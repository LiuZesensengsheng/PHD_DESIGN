# Default Entrypoints

## Goal

Keep recurring project operations easy to remember for humans and Codex.

Prefer direct tests or single-purpose scripts over umbrella entrypoints.

## Default Rule

- Prefer direct scripts, direct tests, and focused workflow docs for routine work.
- When a task has a stable direct test or script, record that direct command here and in relevant workflow docs.

## Current Default Entrypoints

Default commands use `python` and the project Python 3.11 contract; use
`py -3.11` only when `python` is not 3.11.

### Environment Setup

- Install runtime dependencies:
  - `python -m pip install -r requirements.txt`
- Install development dependencies:
  - `python -m pip install -r requirements-dev.txt`
- Install build-only dependencies:
  - `python -m pip install -r requirements-build.txt`

### Repository Smoke Baseline

- Run the quick local test smoke profile:
  - `python scripts/run_test_smoke.py --profile quick`
- Run the contract-oriented test smoke profile:
  - `python scripts/run_test_smoke.py --profile contract`
- List test smoke profiles:
  - `python scripts/run_test_smoke.py --list`
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
- Check implementation-branch daily-log policy:
  - `python scripts/check_daily_log_branch_policy.py --base-ref origin/master`
- Validate the weekly summary generator:
  - `python -m pytest tests/scripts/test_generate_weekly_summary.py -q`
- Generate a specific weekly summary draft directly:
  - `python scripts/generate_weekly_summary.py --year <year> --week <week>`

### Delivery Tracker

- Generate the current delivery markdown/json report:
  - `python scripts/generate_delivery_report.py`
- Generate the current delivery report for a specific focus horizon:
  - `python scripts/generate_delivery_report.py --focus-horizon <internal_playtest|closed_test|ea_launch|v1_0|future>`
- Generate delivery planning metrics from slice inventory plus recent git activity:
  - `python scripts/generate_planning_metrics.py --focus-horizon <internal_playtest|closed_test|ea_launch|v1_0|future> --since <git-date>`

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
  - `docs/development/cardanalysis/CARDANALYSIS_CANONICAL_ROUTE_MAP_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_TOOL_FACADE_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`
- Query the Codex-facing cardanalysis tool facade:
  - `python scripts/run_cardanalysis_tool_facade.py --list-actions`
  - `python scripts/run_cardanalysis_tool_facade.py --action review_pack --json`
  - `python scripts/run_cardanalysis_tool_facade.py --action review_pack --commands`
  - `python scripts/run_cardanalysis_tool_facade.py --action exam --commands`
  - `python scripts/run_cardanalysis_tool_facade.py --action generate_or_ingest --commands`
  - `python scripts/run_cardanalysis_tool_facade.py --check`
- Run the report-only Engineering cardpool review packet through the facade-listed route:
  - `python scripts/run_engineering_cardpool_review_pack.py --output-dir tmp/combat_analysis/engineering_cardpool_review_pack_current`
- Run the report-only Engineering data-method probe through the facade-listed route:
  - `python scripts/run_engineering_data_method_cardanalysis_probe.py --output-dir tmp/combat_analysis/engineering_data_method_cardanalysis_probe_current`
- Run the profile-aware combat-analysis reference report:
  - `python scripts/generate_combat_analysis_reference_report.py --profile-id <profile-id>`
- Run the cross-profile combat-analysis portfolio report:
  - `python scripts/generate_combat_analysis_portfolio_report.py`
- Run the report-only cardanalysis evidence quality audit:
  - `python scripts/run_cardanalysis_report.py --report evidence-quality --input tests/fixtures/combat_analysis/source_followup_case_library_v1 --input tests/fixtures/combat_analysis/mechanism_case_library_v1 --output-dir tmp/combat_analysis/evidence_quality_audit_current`
- Write the report-only cardanalysis case progress dashboard:
  - `python scripts/run_cardanalysis_report.py --report case-progress --write-template tmp/combat_analysis/case_progress_current_template.json`
  - `python scripts/run_cardanalysis_report.py --report case-progress --input tmp/combat_analysis/case_progress_current_template.json --output-dir tmp/combat_analysis/case_progress_current`
- Write and validate STS1 exam targets:
  - `python scripts/validate_sts1_exam_target.py --write-template tmp/combat_analysis/sts1_exam_target_template.json`
  - `python scripts/validate_sts1_exam_target.py --input tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json`
- Write and validate report-only card package variant sets:
  - `python scripts/validate_card_package_variant_set.py --write-template tmp/combat_analysis/card_package_variant_set_template.json`
  - `python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json`
  - `python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --write-report tmp/combat_analysis/card_package_variant_set_report.md`
- Card package draft handoff is retained as a report-only library/fixture
  surface only; its standalone CLI wrapper is retired.
- LLM complete-card draft attempt is retained as a report-only library/fixture
  surface only; its standalone CLI wrapper is retired.
- Exam iteration run and exam iteration prompt patch proposal are retained only
  as report-only supporting libraries for external draft intake and legacy
  single-attempt feedback records; their standalone CLI wrappers are retired.
- Record prompt-patch application and external complete-card draft intake without calling an LLM.
  This is a supporting `generate_or_ingest` command also listed by the
  cardanalysis facade:
  - `python scripts/run_llm_draft_prompt_application.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --prompt-patch <exam_iteration_prompt_patch_proposal_v1_snapshot.json> --generation-metadata <external_generation_metadata.json> --output-dir tmp/combat_analysis/llm_draft_prompt_application_current`
- External draft intake packet and submission readiness are retained as
  report-only library/fixture surfaces only; their standalone CLI wrappers are
  retired from default entrypoints.
- External draft intake rehearsal is retained as a report-only library/fixture
  surface only; its standalone CLI wrapper is retired from default entrypoints.
- Exam iteration batch comparison is fully retired from active code, tests,
  graph nodes, and default entrypoints. Use retained single-attempt iteration
  feedback plus facade-backed iterate/provider-comparison routes instead.
- Exam iteration generated-attempt batch run is fully retired from active code,
  tests, graph nodes, and default entrypoints. Use retained single-attempt
  iteration feedback plus facade-backed iterate/provider-comparison routes
  instead.
- Exam iteration multi-character batch summary is fully retired from active
  code, tests, graph nodes, and default entrypoints. Use retained single-target
  iteration feedback plus facade-backed iterate routes instead.
- STS1 four-character generated-attempt intake, external draft intake
  rehearsal, and owner-approved external draft batch manifest are fully retired
  from active code, tests, graph nodes, and default entrypoints. Use retained
  single-draft intake routes plus the facade-backed complete-card generation,
  exam, review-pack, feedback, and iterate actions instead.
- Write and validate complete card draft packages:
  - `python scripts/validate_complete_card_draft.py --write-template tmp/combat_analysis/complete_card_draft_template.json`
  - `python scripts/validate_complete_card_draft.py --input tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json`
- `card_package_health_v1` conversion for complete drafts is embedded in
  `scripts/run_card_package_exam.py`; the validator no longer exposes a
  standalone export route.
- Run a report-only card package exam from axis search, package seed, and complete drafts:
  - `python scripts/run_card_package_exam.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --package-seed <generated-card-package-proposal-v1.json> --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/card_package_exam_current`
- Run the report-only STS1 four-character card package exam loop: `python scripts/run_sts1_four_character_exam.py`
- Control card production packet, comparison-repair, and owner-decision packet
  are fully retired from active code, tests, graph nodes, and default
  entrypoints. Use the facade-backed complete-card review-pack/feedback routes
  instead.
- STS1 exam capability calibration, negative case pack, and negative case
  projection are fully retired from active code, tests, graph nodes, and
  default entrypoints. Use retained complete-card validation, canonical exams,
  scorecards, advisory exams, Chinese review packs, feedback input, and facade
  routes for current negative or boundary work.
- Axis-first integrated exam summary and axis-first repair iteration run are
  fully retired from active code, tests, graph nodes, and default entrypoints.
  Use retained canonical exam, scorecard, advisory exam, Chinese review-pack,
  and facade routes instead.
- Mechanism-axis search, design brief, package seed, and package-proposal
  validation are now supporting input-preparation commands under:
  - `python scripts/run_cardanalysis_tool_facade.py --action generate_or_ingest --commands`
- Control-discipline plus ideal work now stops at the pilot input contract; the
  old candidate-batch, exam, human-review feedback, and repair-plan sidechain
  is retired. Reviewed candidates should continue through the facade-backed
  `generate_or_ingest` / `complete_card_draft_v1` route:
  - `python scripts/run_cardanalysis_tool_facade.py --action generate_or_ingest --commands`
- Mechanism-axis evaluation handoff, owner, and card-package-health preparation
  stages are fully retired from active code, tests, graph nodes, and default
  entrypoints. Use facade-backed mechanism-axis search/design-brief/package-seed
  for input preparation, then the cardanalysis facade actions for package work.
- Validate and query the cardanalysis capability dependency/conflict graph:
  - `python scripts/validate_capability_graph.py`

### Headless / Regression Checks

- Run headless regression helpers:
  - `python scripts/run_headless_tests.py`
- Run targeted pytest coverage:
  - `python -m pytest <path-or-test> -q`

### Architecture / Encoding Guardrails

- Run the report-only Radon code complexity audit:
  - `python scripts/run_code_complexity_report.py`
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

For resume context, read `AGENTS.md`, `docs/development/CURRENT_DIRECTION.md`, today's daily log, then the latest weekly summary when recent history matters.
