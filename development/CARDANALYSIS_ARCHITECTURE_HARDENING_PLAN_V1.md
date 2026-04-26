# Cardanalysis Architecture Hardening Plan V1

## Purpose

Make `tools/combat_analysis` safe for fast parallel development by separating stable
contracts, engine logic, benchmark/studio work, modelization experiments, and report
presentation.

The goal is not a rewrite. The goal is a sequence of behavior-preserving cuts that
reduce merge pressure and make ownership boundaries explicit.

## Current Decision

Use an incremental hardening path:

1. Add architecture boundary guards before large moves.
2. Move shared contracts out of high-level benchmark/studio modules.
3. Split artifact readers and schema contracts out of orchestrators.
4. Keep scout, bounded shadow, and learned ranking report-only/default-off unless a
   later human decision explicitly promotes them.
5. Preserve existing snapshots and reports while moving code.

## Non-Negotiable Boundaries

- `combat_analysis` is not gameplay runtime.
- `combat_analysis` is not the card data source of truth.
- `design_engine` must not grow new direct imports from `design_studio`.
- Scout and bounded candidate shadow remain report-only, default-off, and
  human-review-required.
- Learned/modelized work starts with ranking/reranking only.
- Legality, schema, hard benchmark gates, and closure diagnostics stay explicit.

## Target Layers

```text
adapters / profiles / source facts
        -> analysis / projections / recommendation
        -> design_engine
           - shared contracts
           - bounded candidate envelopes
           - scout/shadow orchestration
           - explicit constraints and diagnostics
        -> design_studio
           - reviewed benchmarks
           - ranking exports
           - offline reranker experiments
           - shadow comparison reports
        -> reports / scripts
           - presentation
           - CLI wiring
           - artifact writing
```

## Parallel Lanes

These lanes should be safe to develop in parallel once their contracts are stable:

- `contract-lane`: dataclasses, payload parsers, versioned artifact contracts.
- `engine-lane`: scout, bounded shadow, synthesis envelope, closure diagnostics.
- `benchmark-lane`: holdout, mechanism-axis, retrieval/pick/export fixtures.
- `modelization-lane`: feature export, offline reranker, shadow comparison.
- `report-lane`: markdown, HTML, snapshot presentation.
- `docs-ops-lane`: capability map, readiness scorecard, entrypoints, logs.

Avoid assigning two workers to the same large orchestrator file in the same batch.

## Automation-Safe Work

The following can be executed without mid-run human decisions as long as tests remain
green and public output contracts stay stable:

- Moving shared constants/specs from `design_studio` into lower-level contract modules.
- Extracting artifact readers/indexers from orchestrators.
- Adding architecture guard tests with explicit allowlists.
- Splitting report renderers without changing rendered content.
- Adding deterministic fixture tests for artifact contracts.
- Removing allowlisted import edges after the dependent code has moved.

## Human Decision Gates

Stop and ask before doing any of the following:

- Enabling learned ranking in a default path.
- Introducing a new external ML dependency.
- Starting a default-on bounded generator.
- Letting learned/modelized code own legality, schema, benchmark gates, or closure
  diagnostics.
- Moving `STS2` into the same trust tier as reviewed `STS1`.
- Changing threshold semantics or benchmark pass/fail gates.

## Current Migration Debt

- Large orchestrator modules still need responsibility splits:
  - `design_engine/design_candidate_scout.py`
  - `reports/html/sts_profile_template.py` still owns a large single-page static
    template and can later split CSS/JS sections if report-lane conflicts continue.

## First Milestone Exit Criteria

- No `design_engine -> design_studio` imports.
- Shared mechanism-axis contracts live below `design_studio`.
- Bounded shadow artifact parsing is outside the bounded shadow orchestrator.
- Design-candidate scout mechanism evidence matching/summary logic is outside the
  scout orchestration module.
- Design-candidate scout report/snapshot rendering is outside the scout orchestration
  module.
- Bounded candidate shadow report/snapshot rendering is outside the bounded shadow
  orchestration module.
- Constrained synthesis report/snapshot rendering is outside the synthesis orchestration
  module.
- Constrained synthesis mutation delta/role/state helpers are outside the synthesis
  orchestration module.
- Constrained synthesis ranked-candidate selection and diversity guardrails are outside
  the synthesis orchestration module.
- Constrained synthesis tuning-goal derivation and tuned variant construction are
  outside the synthesis orchestration module.
- Fast-card synthesis closure report/snapshot/plain-data rendering is outside closure
  orchestration.
- Fast-card synthesis closure projection helpers, fixture loading, and cluster
  diagnostics are outside closure orchestration.
- Fast-card synthesis closure reviewed fixture replay mainline is outside closure
  orchestration.
- STS catalog holdout loading and artifact/report/delta/manifest helpers are outside
  the benchmark evaluation module.
- STS catalog holdout similarity metrics and diagnostic bucket aggregation are outside
  the benchmark evaluation module.
- STS catalog holdout case replay, variant evaluation, projection lookup, and
  uncertainty-note helpers are outside the benchmark contract module.
- STS HTML public package entrypoint is thin; the large profile renderer lives in its
  own report-lane module.
- STS profile HTML template text is separated from the renderer injection logic.
- Focused regression packs pass for touched surfaces.
- Reviewed benchmark/calibration loading lives outside `design_engine`.

## Second Milestone Exit Criteria

- `synthesis_closure` continues to accept benchmark/calibration inputs through an
  explicit adapter boundary instead of default-importing `design_studio`.
- Artifact readers/writers exist for the major scout/shadow/export snapshots.
- Report rendering consumes stable payloads and does not recompute engine decisions.
- Workers can operate on contract, engine, benchmark, modelization, report, and docs
  lanes without editing the same files.
