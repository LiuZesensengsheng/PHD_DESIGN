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

- Generate the profile-aware combat-analysis reference report:
  - `python scripts/generate_combat_analysis_reference_report.py --profile-id <profile-id>`
- Generate the cross-profile combat-analysis portfolio understanding report:
  - `python scripts/generate_combat_analysis_portfolio_report.py`
- Write a reviewed Design Loop v1 input template:
  - `python scripts/run_combat_analysis_design_loop.py --write-template <path>`
- Run a local Design Loop v1 review from a reviewed JSON input:
  - `python scripts/run_combat_analysis_design_loop.py --input <path> --output-dir <dir>`
- Run a local Deck Skeleton Assist sidecar review from a reviewed JSON input:
  - `python scripts/run_combat_analysis_deck_skeleton_sidecar.py --input <path> --output-dir <dir>`
- Run the STS package similarity benchmark from reviewed shell fixtures:
  - `python scripts/run_package_similarity_benchmark.py --input tests/fixtures/combat_analysis/s34_sts_package_similarity_benchmark_v0 --output-dir <dir>`
- Run the STS catalog holdout benchmark from reviewed Ironclad fixtures:
  - `python scripts/run_sts_catalog_holdout_benchmark.py --input tests/fixtures/combat_analysis/s35_sts_catalog_holdout_benchmark_v1 --output-dir <dir>`
- Export deterministic ranking rows from reviewed STS holdout benchmark fixtures:
  - `python scripts/run_sts_catalog_holdout_ranking_export.py --input tests/fixtures/combat_analysis/s35_sts_catalog_holdout_benchmark_v1 --output-dir <dir>`
- Export one aggregate deterministic ranking dataset across the current reviewed `STS1` holdout surface:
  - `python scripts/run_sts_catalog_holdout_ranking_export.py --input tests/fixtures/combat_analysis/sts_catalog_holdout_ranking_export_v1/sts1_external_holdout_reviewed_manifest_v1.json --output-dir <dir>`
- Export deterministic ranking rows from reviewed retrieval fixtures:
  - `python scripts/run_reviewed_retrieval_ranking_export.py --input tests/fixtures/combat_analysis/retrieval --output-dir <dir>`
- Export deterministic ranking rows from the reviewed closed-set pick-ranking benchmark:
  - `python scripts/run_pick_ranking_export.py --input tests/fixtures/combat_analysis/pick_ranking/pick_ranking_cases_v1.json --output-dir <dir>`
- Train and evaluate the offline pick-ranking pairwise reranker from an export snapshot:
  - `python scripts/run_pick_ranking_pairwise_reranker.py --input <pick-ranking-export-snapshot.json> --output-dir <dir>`
- Train and evaluate the offline reviewed retrieval pairwise reranker from an export snapshot:
  - `python scripts/run_reviewed_retrieval_pairwise_reranker.py --input <retrieval-ranking-export-snapshot.json> --output-dir <dir>`
- Train and evaluate the offline STS holdout pairwise reranker from an export snapshot:
  - `python scripts/run_sts_catalog_holdout_pairwise_reranker.py --input <ranking-export-snapshot.json> --output-dir <dir>`
- Run the fun-proxy calibration sidecar from reviewed deck benchmark inputs:
  - `python scripts/run_fun_proxy_calibration.py --input tests/fixtures/combat_analysis/deck_fun_benchmark_v1 --output-dir <dir>`
- Run the fun enemy-design probe sidecar from reviewed deck + forum inputs:
  - `python scripts/run_fun_enemy_design_probe.py --reviewed-pack tests/fixtures/combat_analysis/deck_fun_benchmark_v1 --forum-input tests/fixtures/combat_analysis/forum_weak_labels_v1 --review-input tests/fixtures/combat_analysis/forum_deck_case_bridge_v1/review_annotations_v1.json --session-focus enemy_design --output-dir <dir>`
- Write a fast card-design loop input template:
  - `python scripts/run_fast_card_design_loop.py --write-template <path>`
- Run a fast card-design loop review from a reviewed JSON input:
  - `python scripts/run_fast_card_design_loop.py --input <path> --output-dir <dir>`
- Write a fast card synthesis bridge input template:
  - `python scripts/run_fast_card_synthesis_bridge.py --write-template <path>`
- Run the constrained fast card synthesis bridge from a reviewed JSON input:
  - `python scripts/run_fast_card_synthesis_bridge.py --input <path> --output-dir <dir>`
- Write a fast card synthesis closure input template:
  - `python scripts/run_fast_card_synthesis_closure.py --write-template <path>`
- Run the fast card synthesis closure sidecar from a reviewed JSON input:
  - `python scripts/run_fast_card_synthesis_closure.py --input <path> --output-dir <dir>`
- Read the autonomy design-assist runbook:
  - `tools/combat_analysis/docs/AUTONOMY_DESIGN_ASSIST_RUNBOOK_V1.md`
- Write a Design Candidate Scout single-session input template:
  - `python scripts/run_design_candidate_scout.py --write-template <path>`
- Run a report-only Design Candidate Scout single-session review:
  - `python scripts/run_design_candidate_scout.py --input <path> --output-dir <dir>`
- Write a Design Candidate Scout batch manifest template:
  - `python scripts/run_design_candidate_scout.py --write-batch-template <path>`
- Run a report-only Design Candidate Scout batch review:
  - `python scripts/run_design_candidate_scout.py --batch-input <path> --output-dir <dir>`
- Write a bounded candidate shadow manifest template:
  - `python scripts/run_bounded_candidate_shadow.py --write-template <path>`
- Run a report-only bounded candidate shadow review:
  - `python scripts/run_bounded_candidate_shadow.py --input <path> --output-dir <dir>`
- Write an Evaluation Autonomous Design Model input template:
  - `python scripts/run_evaluation_autonomous_design_model.py --write-template <path>`
- Run a report-only Evaluation Autonomous Design Model review:
  - `python scripts/run_evaluation_autonomous_design_model.py --input <path> --output-dir <dir>`
- Write a Campaign Power Curve report input template:
  - `python scripts/run_campaign_power_curve_report.py --write-template <path>`
- Run a report-only Campaign Power Curve review:
  - `python scripts/run_campaign_power_curve_report.py --input <path> --output-dir <dir>`
- Write a position redirect code preflight input template:
  - `python scripts/run_position_redirect_code_preflight.py --write-template <path>`
- Run a report-only position redirect code preflight from a reviewed JSON input:
  - `python scripts/run_position_redirect_code_preflight.py --input tests/fixtures/combat_analysis/position_redirect_code_preflight_v1/position_redirect_code_preflight_reviewed_v1.json --output-dir <dir>`
- Run the reviewed mechanism-axis viability benchmark:
  - `python scripts/run_mechanism_axis_viability_benchmark.py --input tests/fixtures/combat_analysis/mechanism_axis_viability_v1 --output-dir <dir>`
- Run a unified project design-assist session in one mode:
  - `python scripts/run_project_design_assist_session.py --mode <card|enemy|synthesis> --input <path> --output-dir <dir>`
- Run a unified project design-assist batch session:
  - `python scripts/run_project_design_assist_session.py --batch-input <path>`
- Write a fast draft-session input template (3-pick-1 with optional discard):
  - `python scripts/run_fast_draft_session.py --write-template <path>`
- Run a fast draft session from a reviewed JSON input:
  - `python scripts/run_fast_draft_session.py --input <path> --output-dir <dir>`
- Scaffold a new character profile file without registering it:
  - `python scripts/scaffold_combat_analysis_profile.py --family sts1 --character-id <id> --display-name <婵炴垶鎼╅崢浠嬪几閸愵喖瑙?`
- Validate the profile scaffold script:
  - `python -m pytest tests/scripts/test_scaffold_combat_analysis_profile.py -q`
- Validate Design Loop v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_loop.py tests/scripts/test_run_combat_analysis_design_loop.py -q`
- Validate Deck Skeleton Sidecar v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_deck_skeleton_sidecar.py tests/scripts/test_run_combat_analysis_deck_skeleton_sidecar.py -q`
- Validate the STS package similarity benchmark v0:
  - `python -m pytest tests/toolkit/combat_analysis/test_package_similarity_benchmark_v0.py tests/scripts/test_run_package_similarity_benchmark.py -q`
- Validate the STS catalog holdout benchmark v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_v1.py tests/scripts/test_run_sts_catalog_holdout_benchmark.py -q`
- Validate the STS catalog holdout ranking export v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_ranking_export.py tests/scripts/test_run_sts_catalog_holdout_ranking_export.py -q`
- Validate the reviewed retrieval ranking export v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_reviewed_retrieval_ranking_export.py tests/scripts/test_run_reviewed_retrieval_ranking_export.py -q`
- Validate the pick-ranking export v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_pick_ranking_export.py tests/scripts/test_run_pick_ranking_export.py -q`
- Validate the pick-ranking pairwise reranker v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_pick_ranking_pairwise_reranker.py tests/scripts/test_run_pick_ranking_pairwise_reranker.py -q`
- Validate the reviewed retrieval pairwise reranker v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_reviewed_retrieval_pairwise_reranker.py tests/scripts/test_run_reviewed_retrieval_pairwise_reranker.py -q`
- Validate the STS catalog holdout pairwise reranker v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_pairwise_reranker.py tests/scripts/test_run_sts_catalog_holdout_pairwise_reranker.py -q`
- Validate fast card-design loop v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_fast_card_loop.py tests/scripts/test_run_fast_card_design_loop.py -q`
- Validate fast card synthesis bridge v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_constrained_synthesis.py tests/scripts/test_run_fast_card_synthesis_bridge.py -q`
- Validate fast card synthesis closure v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_synthesis_closure.py tests/scripts/test_run_fast_card_synthesis_closure.py -q`
- Validate Design Candidate Scout v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_design_candidate_scout.py tests/scripts/test_run_design_candidate_scout.py -q`
- Validate bounded candidate shadow v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_bounded_candidate_shadow.py tests/scripts/test_run_bounded_candidate_shadow.py -q`
- Validate Evaluation Autonomous Design Model v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_evaluation_autonomous_design_model_v1.py tests/scripts/test_run_evaluation_autonomous_design_model.py -q`
- Validate Campaign Power Curve report v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_campaign_power_curve_model_v1.py tests/scripts/test_run_campaign_power_curve_report.py -q`
- Validate position redirect code preflight v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_position_redirect_code_preflight_v1.py tests/scripts/test_run_position_redirect_code_preflight.py -q`
- Validate the reviewed mechanism-axis viability benchmark:
  - `python -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_viability_v1.py tests/scripts/test_run_mechanism_axis_viability_benchmark.py -q`
- Validate retrieval persistent-miss lane-local probes:
  - `python -m pytest tests/toolkit/combat_analysis/test_reviewed_retrieval_persistent_miss_probe_pack.py -q`
- Validate fast draft-session v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_design_engine_fast_draft_session.py tests/scripts/test_run_fast_draft_session.py -q`
- Validate enemy-design isolation guardrails:
  - `python -m pytest tests/toolkit/combat_analysis/test_enemy_design_guardrails.py -q`
- Validate project card-design assist reviewed cases v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_project_card_design_cases_v1.py -q`
- Validate project enemy-design assist reviewed cases v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_project_enemy_design_cases_v1.py -q`
- Validate fun-proxy calibration sidecar v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_fun_proxy_calibration_v1.py tests/scripts/test_run_fun_proxy_calibration.py -q`
- Validate fun enemy-design probe sidecar v1:
  - `python -m pytest tests/toolkit/combat_analysis/test_fun_enemy_design_probe_v1.py tests/scripts/test_run_fun_enemy_design_probe.py -q`
- Validate project design-assist sidecar CLI contracts v1:
  - `python -m pytest tests/scripts/test_project_design_assist_sidecar_contracts_v1.py -q`
- Read cardanalysis north star, case input contract, report-only registry, and validation matrix:
  - `docs/development/CARDANALYSIS_NORTH_STAR_V1.md`
  - `docs/development/CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`
  - `docs/development/CARDANALYSIS_REPORT_ONLY_SURFACE_REGISTRY_V1.md`
  - `docs/development/CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`
- Write a cardanalysis normalized case input template:
  - `python scripts/validate_cardanalysis_case_input.py --write-template <path>`
- Validate a cardanalysis normalized case input file or directory:
  - `python scripts/validate_cardanalysis_case_input.py --input <path>`
- Validate the cardanalysis case input validator:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_case_input_contract_v1.py tests/scripts/test_validate_cardanalysis_case_input.py -q`
- Run the existing asset case adapter export:
  - `python scripts/run_existing_asset_case_adapter.py --input <legacy-json-or-dir> --output-dir <dir>`
- Validate the existing asset case adapter:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_existing_asset_case_adapter_v1.py tests/scripts/test_run_existing_asset_case_adapter.py -q`
- Write a case-projection sample pack input template:
  - `python scripts/run_case_projection_sample_pack.py --write-template <path>`
- Run the case-projection sample pack closure over one or more legacy inputs:
  - `python scripts/run_case_projection_sample_pack.py --input <legacy-json-or-dir-or-manifest> --output-dir <dir>`
- Validate the case-projection sample pack v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_case_projection_sample_pack_v1.py tests/scripts/test_run_case_projection_sample_pack.py -q`
- Write a cardanalysis coverage-gap scanner input template:
  - `python scripts/run_cardanalysis_coverage_gap_report.py --write-template <path>`
- Run a report-only cardanalysis coverage-gap scan:
  - `python scripts/run_cardanalysis_coverage_gap_report.py --input <case-or-projection-json-or-dir-or-manifest> --output-dir <dir>`
- Validate Cardanalysis Coverage Gap Report v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_coverage_gap_report_v1.py tests/scripts/test_run_cardanalysis_coverage_gap_report.py -q`
- Write a cardanalysis feature projection input template:
  - `python scripts/run_cardanalysis_feature_projection.py --write-template <path>`
- Run a report-only cardanalysis feature projection review:
  - `python scripts/run_cardanalysis_feature_projection.py --input tests/fixtures/combat_analysis/feature_projection_v1/feature_projection_cases_v1.json --output-dir <dir>`
- Validate Cardanalysis Feature Projection v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_feature_projection_v1.py tests/scripts/test_run_cardanalysis_feature_projection.py -q`
- Write a Stress Resolve Model input template:
  - `python scripts/run_stress_resolve_model.py --write-template <path>`
- Run a report-only Stress Resolve Model review:
  - `python scripts/run_stress_resolve_model.py --input tests/fixtures/combat_analysis/stress_resolve_model_v1/stress_resolve_cases_v1.json --output-dir <dir>`
- Validate Stress Resolve Model v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_stress_resolve_model_v1.py tests/scripts/test_run_stress_resolve_model.py -q`
- Write a Campaign Experience Curve input template:
  - `python scripts/run_campaign_experience_curve.py --write-template <path>`
- Run a report-only Campaign Experience Curve review:
  - `python scripts/run_campaign_experience_curve.py --input tests/fixtures/combat_analysis/campaign_experience_curve_v1/campaign_experience_curve_cases_v1.json --output-dir <dir>`
- Validate Campaign Experience Curve v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_experience_curve_v1.py tests/scripts/test_run_campaign_experience_curve.py -q`
- Write a Campaign Advisory Bundle input template:
  - `python scripts/run_campaign_advisory_bundle.py --write-template <path>`
- Run a report-only Campaign Advisory Bundle review:
  - `python scripts/run_campaign_advisory_bundle.py --input tests/fixtures/combat_analysis/campaign_advisory_bundle_v1/campaign_advisory_bundle_cases_v1.json --output-dir <dir>`
- Validate Campaign Advisory Bundle v1:
  - `py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_advisory_bundle_v1.py tests/scripts/test_run_campaign_advisory_bundle.py -q`
- Validate and query the cardanalysis capability dependency/conflict graph:
  - `python scripts/validate_capability_graph.py`
  - `python scripts/validate_capability_graph.py --impact <node-id>`
  - `python scripts/validate_capability_graph.py --batch <node-id> <node-id>`

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
