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
