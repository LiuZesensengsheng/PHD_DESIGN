# Cardanalysis Case Projection Sample Pack V1

## Purpose

`cardanalysis_case_projection_sample_pack_v1` is a thin engineering entrypoint
that proves one closed loop:

`legacy fixture -> existing_asset_case_adapter_v1 -> normalized_design_case -> cardanalysis_feature_projection_v1`

It is a deterministic sample-pack tool, not a new evaluator, not a new
canonical report-only surface, and not a hard-gate authority.

## Scope Boundary

In scope:

- composing existing adapter and feature-projection steps,
- producing deterministic sample artifacts for regression,
- proving multiple legacy source families can share the same normalized-case
  bridge.

Out of scope:

- new scoring logic,
- new canonical summaries,
- graph or registry ownership changes,
- hard gates, default recommendation changes, or learned/reranker enablement.

## Input Surface

V1 accepts:

- one or more legacy fixture file or directory paths, or
- a small JSON manifest that lists those paths.

Manifest entries are resolved relative to the manifest file first, then relative
to the repository root. This keeps generated templates runnable from temporary
output directories while preserving fixture-local manifests.

The template manifest covers four legacy sources:

- `mechanism_axis_viability_v1`
- `campaign_power_curve_report_v1`
- `stress_resolve_model_v1`
- `campaign_experience_curve_v1`

## Output Artifacts

V1 writes:

- `normalized_cases_snapshot.json`
- `feature_projection_snapshot.json`
- `manifest.json`
- `case_projection_sample_pack_report.md`

All outputs remain JSON-safe and deterministic.

## Authority Boundary

- normalized cases must keep
  `schema_version = cardanalysis_case_input_v1`
- normalized cases must keep
  `authority.authority_boundary = advisory_context_only`
- feature projections must keep
  `schema_version = cardanalysis_feature_projection_v1`
- feature projections must keep
  `projection_mode = report_only`
- feature projections must keep
  `authority_boundary = advisory_context_only`

Unreviewed/source-mined/generated cases must not be promoted to reviewed just
because they pass through the sample pack.

## Graph Note

This branch intentionally does not register a new capability or task node.

Reason:

- the graph already models the two real owners:
  `existing_asset_case_adapter_v1` and `cardanalysis_feature_projection_v1`
- this sample pack only composes those existing owners into a regression
  entrypoint
- it provides no new canonical payload, summary, or review surface

If the entrypoint becomes a repeated merge-planning surface later, MasterAgent
can decide whether a task node is worthwhile.
