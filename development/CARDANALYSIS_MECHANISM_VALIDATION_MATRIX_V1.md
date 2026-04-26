# Cardanalysis Mechanism Validation Matrix V1

## Purpose

Define the smallest validation package to run when expanding the cardanalysis
mechanism surface, fun/health evaluation surface, deck compression/removal model, or
card package health layer.

This matrix is for future parallel cardanalysis work. It does not add new tests or
change default entrypoints.

## Scope Boundary

In scope:

- `tools/combat_analysis` mechanism-axis family expansion.
- Reviewed mechanism-axis viability fixtures.
- Fun proxy, deck fun, and design scorecard health evaluators.
- Deck compression/removal and turn-budget model changes.
- Card package health, package similarity, and deck skeleton closure checks.
- Merge-time regression for multiple cardanalysis sub-branches.

Out of scope:

- Gameplay runtime validation.
- Changing hard benchmark gate semantics.
- Promoting learned/reranker output into a default path.
- Treating `STS2` evidence as the same trust tier as reviewed `STS1`.

## Baseline Rules

- Always run `git diff --check` before handoff.
- Always run the text encoding guard when adding or editing Markdown, JSON fixtures, or
  generated text contracts:
  - `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`
- Add or update holdout cases only when the change claims catalog-level recovery,
  ranking, or generalization behavior.
- Reviewed viability cases are the first validation layer for a new mechanism family.
  They are not a substitute for holdout evidence once the family affects catalog
  ranking or synthesis recovery claims.
- Report-only/modelization paths may be validated by exports, reranker, and shadow
  tests, but they must not become legality, schema, hard gate, or closure authority.

## Validation Levels

| Level | Use When | Minimum Validation |
| --- | --- | --- |
| `L0 docs spec` | Docs-only planning, no fixtures, no code, no command surface change. | `git diff --check`; text encoding guard. |
| `L1 fixture contract` | Adding or editing reviewed JSON/Markdown fixtures without evaluator logic changes. | The owning fixture/evaluator pytest plus its CLI contract test if artifacts are produced. |
| `L2 evaluator behavior` | Changing scoring, labels, dimensions, report/snapshot payloads, or gates. | Owning evaluator pytest, owning CLI test, and adjacent artifact/snapshot tests. |
| `L3 cross-surface behavior` | A change affects ranking, synthesis, project card assist, deck skeleton, fun/health, or scorecard consumers. | Owning pack plus every named consumer pack in the relevant matrix row. |
| `L4 merge regression` | Main agent merges multiple cardanalysis branches or resolves conflicts across lanes. | Full merge regression package below. |

## Change Matrix

### New Mechanism Family

Use for adding a family such as `strength_scaling`, `block_engine`, `frost_control`,
or `power_focus_scaling`.

Minimum reviewed content:

- Add one family spec below `design_engine` contracts.
- Add at least three reviewed viability contrasts:
  - one clear online shell,
  - one payoff-only, raw-value, or fantasy-exactness failure,
  - one hybrid/goodstuff or adjacent-family confusion case.
- Update the fixture index/readiness notes for the reviewed viability pack.

Minimum tests:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_viability_v1.py tests/scripts/test_run_mechanism_axis_viability_benchmark.py -q
```

Add consumer tests when applicable:

- If the family changes project card recommendation labels or ranking:
  `py -3.11 -m pytest tests/toolkit/combat_analysis/test_project_card_design_cases_v1.py tests/scripts/test_run_fast_card_design_loop.py -q`
- If it changes synthesis candidate ranking or closure diagnostics:
  `py -3.11 -m pytest tests/toolkit/combat_analysis/test_design_engine_constrained_synthesis.py tests/toolkit/combat_analysis/test_design_engine_synthesis_closure.py tests/scripts/test_run_fast_card_synthesis_bridge.py tests/scripts/test_run_fast_card_synthesis_closure.py -q`
- If it changes STS catalog recovery, similarity, or near-neighbor behavior, add a
  holdout case and run the holdout package listed below.

### New Viability Fixture

Use for adding a reviewed pairwise mechanism-axis fixture inside an existing or new
family.

Minimum reviewed content:

- The fixture must keep the stable keys used by
  `mechanism_axis_viability_v1`.
- The positive and negative cases must be different reviewed references.
- `expected_advantage_dimensions` must use existing mechanism-axis dimensions unless
  the dimension vocabulary is intentionally expanded.
- `evidence_refs` and `review_notes` must remain non-empty.

Minimum tests:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_viability_v1.py tests/scripts/test_run_mechanism_axis_viability_benchmark.py -q
```

Escalate to the new-family package if the fixture introduces a family vocabulary item,
new verdict label, new dimension, or changed hard gate behavior.

### New Fun Or Health Evaluator

Use for evaluator changes that judge deck fun, proxy fun, enemy-design fun probes,
scorecard health, or human-facing deck review health.

Minimum tests by touched surface:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_deck_fun_taxonomy_v1.py tests/toolkit/combat_analysis/test_deck_fun_benchmark_v1.py tests/toolkit/combat_analysis/test_deck_fun_benchmark_dataset_governance_v1.py tests/scripts/test_run_deck_fun_benchmark.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_fun_proxy_calibration_v1.py tests/scripts/test_run_fun_proxy_calibration.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_fun_enemy_design_probe_v1.py tests/scripts/test_run_fun_enemy_design_probe.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_scorecard.py tests/toolkit/combat_analysis/test_scorecard_fragile_samples.py tests/toolkit/combat_analysis/test_scorecard_samples.py tests/toolkit/combat_analysis/test_scorecard_ordering_pairs.py -q
```

Also run deck review/portfolio CLIs if the evaluator feeds designer-facing deck
reports:

```powershell
py -3.11 -m pytest tests/scripts/test_run_deck_review_sidecar.py tests/scripts/test_run_deck_portfolio_brief.py -q
```

Holdout is required only if the evaluator changes catalog ranking, synthesis recovery,
or hard pass/fail semantics. Otherwise reviewed deck cases are enough.

### New Deck Compression Or Removal Model

Use for changes to turn-budget compression, removal value, deck-thinning pressure,
cost compression, or any model that says a card/deck is healthier because it removes,
compresses, filters, or skips friction.

Minimum tests:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_analysis.py tests/toolkit/combat_analysis/test_matchup_gap.py tests/toolkit/combat_analysis/test_project_card_design_cases_v1.py tests/toolkit/combat_analysis/test_design_engine_fast_card_loop.py tests/scripts/test_run_fast_card_design_loop.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_scorecard.py tests/toolkit/combat_analysis/test_scorecard_fragile_samples.py -q
```

Add profile tests for any affected character catalog:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_ironclad_profile.py tests/toolkit/combat_analysis/test_silent_profile.py tests/toolkit/combat_analysis/test_defect_profile.py tests/toolkit/combat_analysis/test_watcher_profile.py -q
```

Add holdout when compression/removal changes top-k catalog recovery, near-neighbor
suppression, provenance-drift diagnostics, or synthesis ranking. Use reviewed
viability only when the change is still local to mechanism shell detection.

### New Card Package Health Layer

Use for package density, slot fit, family hit rate, closure fit, motif fit, deck
skeleton evidence, or package-health scorecard changes.

Minimum tests:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_package_similarity_benchmark_v0.py tests/scripts/test_run_package_similarity_benchmark.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_deck_skeleton_sidecar.py tests/toolkit/combat_analysis/test_deck_skeleton_evidence_bridge.py tests/scripts/test_run_combat_analysis_deck_skeleton_sidecar.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_scorecard.py tests/toolkit/combat_analysis/test_scorecard_fragile_samples.py -q
```

Add deck fun benchmark tests if package health is used to claim fun/feel quality:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_deck_fun_benchmark_v1.py tests/toolkit/combat_analysis/test_fun_proxy_calibration_v1.py -q
```

Add STS holdout tests if package health affects catalog recovery or ranking features.

## Holdout Case Rules

### Must Add Holdout

Add at least one reviewed STS holdout case when any of these are true:

- The change claims catalog-level recovery, ranking, or generalization.
- A mechanism family graduates from local viability evidence into synthesis,
  retrieval, project-card ranking, or catalog holdout claims.
- Top-k ordering, neighbor suppression, package similarity, semantic compactness,
  provenance drift, recovery class, or uncertainty-note behavior changes.
- A new evaluator changes candidate ranking or hard benchmark pass/fail decisions.
- A regression was found in an existing external STS lane and the fix needs a permanent
  honesty surface.
- The change adds a new failure family that cannot be represented by pairwise viability
  alone, such as base-family anchoring, hybrid-soup false positives, or provenance
  drift.

Minimum holdout validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_silent_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_defect_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_watcher_v1.py tests/scripts/test_run_sts_catalog_holdout_benchmark.py -q
```

If the holdout feeds ranking exports, rerankers, or shadow reports:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_ranking_export.py tests/scripts/test_run_sts_catalog_holdout_ranking_export.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_pairwise_reranker.py tests/scripts/test_run_sts_catalog_holdout_pairwise_reranker.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_shadow_compare.py tests/toolkit/combat_analysis/test_modelization_shadow_report.py tests/scripts/test_run_modelization_shadow_report.py -q
```

### Reviewed Viability Only

Use reviewed viability without a new holdout when all of these are true:

- The change is local to mechanism-axis family recognition or pairwise contrast
  quality.
- No catalog recovery, top-k ranking, retrieval, synthesis, or project card assist
  output changes are claimed.
- The new case only sharpens online shell versus payoff-only, raw-value,
  almost-loop, or hybrid-soup distinction.
- Existing holdout behavior is intentionally unchanged.

### Docs Spec Only

Do docs-only validation when all of these are true:

- Only files under `docs/development` or other explanatory docs changed.
- No fixture, test, script, default entrypoint, code, generated artifact, or benchmark
  threshold changed.
- The document does not claim a new validated behavior that lacks an existing test
  surface.

Minimum validation:

```powershell
git diff --check
py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q
```

Do not run the large combat-analysis regression package for a pure spec document unless
the spec edits command surfaces, fixture contracts, or benchmark gate language.

## Full Merge Regression Package

Run this when the main agent merges multiple cardanalysis sub-branches, resolves
conflicts across contract/engine/benchmark/modelization/report lanes, or prepares a
large cardanalysis integration handoff.

Architecture and encoding:

```powershell
git diff --check
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
```

Mechanism axis and project assist:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_viability_v1.py tests/scripts/test_run_mechanism_axis_viability_benchmark.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_project_card_design_cases_v1.py tests/toolkit/combat_analysis/test_project_design_assist_regression_matrix_v1.py tests/scripts/test_project_design_assist_sidecar_contracts_v1.py tests/scripts/test_run_fast_card_design_loop.py -q
```

Holdout, ranking, reranker, and shadow:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_silent_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_defect_v1.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_benchmark_watcher_v1.py tests/scripts/test_run_sts_catalog_holdout_benchmark.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts_catalog_holdout_ranking_export.py tests/scripts/test_run_sts_catalog_holdout_ranking_export.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_pairwise_reranker.py tests/scripts/test_run_sts_catalog_holdout_pairwise_reranker.py tests/toolkit/combat_analysis/test_sts_catalog_holdout_shadow_compare.py tests/toolkit/combat_analysis/test_modelization_shadow_report.py tests/scripts/test_run_modelization_shadow_report.py -q
```

Synthesis and closure:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_design_engine_constrained_synthesis.py tests/toolkit/combat_analysis/test_design_engine_synthesis_closure.py tests/toolkit/combat_analysis/test_design_engine_fast_card_loop.py tests/toolkit/combat_analysis/test_design_engine_fast_draft_session.py tests/scripts/test_run_fast_card_synthesis_bridge.py tests/scripts/test_run_fast_card_synthesis_closure.py tests/scripts/test_run_fast_draft_session.py -q
```

Package, deck skeleton, and fun/health:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_package_similarity_benchmark_v0.py tests/scripts/test_run_package_similarity_benchmark.py tests/toolkit/combat_analysis/test_deck_skeleton_sidecar.py tests/toolkit/combat_analysis/test_deck_skeleton_evidence_bridge.py tests/scripts/test_run_combat_analysis_deck_skeleton_sidecar.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_deck_fun_taxonomy_v1.py tests/toolkit/combat_analysis/test_deck_fun_benchmark_v1.py tests/toolkit/combat_analysis/test_deck_fun_benchmark_dataset_governance_v1.py tests/toolkit/combat_analysis/test_fun_proxy_calibration_v1.py tests/toolkit/combat_analysis/test_fun_enemy_design_probe_v1.py tests/scripts/test_run_deck_fun_benchmark.py tests/scripts/test_run_fun_proxy_calibration.py tests/scripts/test_run_fun_enemy_design_probe.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_scorecard.py tests/toolkit/combat_analysis/test_scorecard_fragile_samples.py tests/toolkit/combat_analysis/test_scorecard_samples.py tests/toolkit/combat_analysis/test_scorecard_ordering_pairs.py -q
```

Use the full repo smoke baseline only when the merge also touches shared infrastructure,
default entrypoints, architecture guards outside combat_analysis, or generated
cross-system artifacts.

## DEFAULT_ENTRYPOINTS Policy

Do not edit `docs/development/DEFAULT_ENTRYPOINTS.md` for every new fixture or local
case. Update it only when a stable, reusable command becomes a default project
entrypoint and there is an obvious gap for future agents. If a gap is found while
working on mechanism expansion, call it out separately from the feature change.
