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
- Write the report-only cardanalysis case progress dashboard:
  - `python scripts/run_cardanalysis_case_progress_report.py --write-template tmp/combat_analysis/case_progress_current_template.json`
  - `python scripts/run_cardanalysis_case_progress_report.py --input tmp/combat_analysis/case_progress_current_template.json --output-dir tmp/combat_analysis/case_progress_current`
- Write and validate STS1 exam targets:
  - `python scripts/validate_sts1_exam_target.py --write-template tmp/combat_analysis/sts1_exam_target_template.json`
  - `python scripts/validate_sts1_exam_target.py --input tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json`
- Write and validate report-only card package variant sets:
  - `python scripts/validate_card_package_variant_set.py --write-template tmp/combat_analysis/card_package_variant_set_template.json`
  - `python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json`
  - `python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --write-report tmp/combat_analysis/card_package_variant_set_report.md`
- Write a report-only complete-card draft handoff from the recommended package variant:
  - `python scripts/run_card_package_draft_handoff.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --output-dir tmp/combat_analysis/card_package_draft_handoff_current`
- Record one generated or owner-supplied `complete_card_draft_v1` attempt against a draft handoff:
  - `python scripts/run_llm_complete_card_draft_attempt.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/llm_complete_card_draft_attempt_current`
- Validate four-character generated-attempt negative controls:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_llm_complete_card_draft_attempt_v1.py tests/toolkit/combat_analysis/test_exam_iteration_run_v1.py -q`
- Record one report-only attempt-to-exam iteration run:
  - `python scripts/run_exam_iteration_run.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --axis-search <mechanism_axis_search_bundle_v1.json> --package-seed <card_package_proposal_v1.json> --output-dir tmp/combat_analysis/exam_iteration_run_current`
- Summarize iteration runs into report-only prompt and handoff patch advice:
  - `python scripts/run_exam_iteration_prompt_patch_proposal.py --input tmp/combat_analysis/exam_iteration_run_current/exam_iteration_run_v1_snapshot.json --output-dir tmp/combat_analysis/exam_iteration_prompt_patch_proposal_current`
- Compare an ordered batch of generated-attempt iteration runs:
  - `python scripts/run_exam_iteration_batch_comparison.py --input <attempt_001_exam_iteration_run_snapshot.json> --input <attempt_002_exam_iteration_run_snapshot.json> --prompt-patch <exam_iteration_prompt_patch_proposal_v1_snapshot.json> --output-dir tmp/combat_analysis/exam_iteration_batch_comparison_current`
- Write and validate complete card draft packages:
  - `python scripts/validate_complete_card_draft.py --write-template tmp/combat_analysis/complete_card_draft_template.json`
  - `python scripts/validate_complete_card_draft.py --input tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json`
- Export a complete card draft as temporary `card_package_health_v1` owner input:
  - `python scripts/validate_complete_card_draft.py --input tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --export-card-package-health-input tmp/combat_analysis/complete_card_draft_card_package_health_input.json`
- Run a report-only card package exam from axis search, package seed, and complete drafts:
  - `python scripts/run_card_package_exam.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --package-seed <generated-card-package-proposal-v1.json> --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/card_package_exam_current`
- Run the report-only STS1 four-character card package exam loop:
  - `python scripts/run_sts1_four_character_exam.py`
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
- Check whether the current package seed may enter the card-package generation exam:
  - `python scripts/run_mechanism_axis_generation_exam_readiness.py --input tmp/combat_analysis/mechanism_axis_owner_report_input_plan_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_report_requests_input_plan_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_generation_exam_readiness_current`
- Write a report-only owner evidence queue from the generation-exam readiness blockers:
  - `python scripts/run_mechanism_axis_owner_evidence_queue.py --input tmp/combat_analysis/mechanism_axis_generation_exam_readiness_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_generation_exam_readiness_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_evidence_queue_current`
- Write empty owner evidence intake templates from the current owner evidence queue:
  - `python scripts/run_mechanism_axis_owner_evidence_intake_packet.py --input tmp/combat_analysis/mechanism_axis_owner_evidence_queue_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_evidence_queue_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_evidence_intake_packet_current`
- Write a report-only card package health owner input scaffold from the current package seed and intake packet:
  - `python scripts/run_mechanism_axis_card_package_health_scaffold.py --package-seed tmp/combat_analysis/mechanism_axis_package_seed_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1.json --intake-packet tmp/combat_analysis/mechanism_axis_owner_evidence_intake_packet_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_evidence_intake_packet_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current`
- Check whether the card package health scaffold has enough owner-filled material for a later input-writing step:
  - `python scripts/run_mechanism_axis_card_package_health_readiness.py --input tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_card_package_health_owner_input_scaffold_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_readiness_current`
- Write a temporary `card_package_health_v1` input from a fully owner-filled scaffold:
  - `python scripts/run_mechanism_axis_card_package_health_input_writer.py --input tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current/<filled_scaffold_snapshot>.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_input_writer_current`
- Explicitly run the canonical `card_package_health_v1` evaluator on that temporary input:
  - `python scripts/run_mechanism_axis_card_package_health_owner_run.py --input tmp/combat_analysis/mechanism_axis_card_package_health_input_writer_current/card_package_health_input.json --input-writer-manifest tmp/combat_analysis/mechanism_axis_card_package_health_input_writer_current/card_package_health_input_writer_manifest.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_owner_run_current`
- Adapt that owner-run snapshot into a report-only `cardanalysis_evidence_bundle_v1`:
  - `python scripts/run_mechanism_axis_card_package_health_evidence_bundle.py --input tmp/combat_analysis/mechanism_axis_card_package_health_owner_run_current/card_package_health_owner_run_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_evidence_bundle_current`
- Merge the report-only evidence bundle back into the evaluation handoff input:
  - `python scripts/run_mechanism_axis_evaluation_evidence_merge.py --handoff-input tmp/combat_analysis/mechanism_axis_evaluation_handoff_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff.json --evidence-bundle tmp/combat_analysis/mechanism_axis_card_package_health_evidence_bundle_current/cardanalysis_evidence_bundle.json --output-dir tmp/combat_analysis/mechanism_axis_evaluation_evidence_merge_current`
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
