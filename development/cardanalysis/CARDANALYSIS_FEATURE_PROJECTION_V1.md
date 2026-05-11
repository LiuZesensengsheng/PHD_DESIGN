# Cardanalysis Feature Projection V1

## Purpose

Define the minimal deterministic layer that projects a
`cardanalysis_case_input_v1` normalized design case into a
`cardanalysis_feature_projection_v1` payload.

This layer is an anti-corruption boundary between normalized case evidence and
future capability/model heads. It is intentionally report-only and does not own
hard gates, recommendation defaults, synthesis, or learned/reranker behavior.

## Input

The input is a JSON-safe plain mapping that follows
`CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`:

- `schema_version = cardanalysis_case_input_v1`
- case identity fields: `case_id`, `title`, `summary`
- source provenance under `source`
- object identity under `design_object`
- context, observed behavior, labels, feature hints, known limits
- `authority.authority_boundary = advisory_context_only`

The projector rejects non-advisory authority boundaries instead of silently
normalizing them.

The implementation reuses `tools/combat_analysis/case_input_contract.py` for
input normalization. Feature projection should not carry a second copy of the
case schema.

## Output

The output payload shape is:

```json
{
  "schema_version": "cardanalysis_feature_projection_v1",
  "case_id": "case_id",
  "projection_mode": "report_only",
  "authority_boundary": "advisory_context_only",
  "features": {},
  "source_trace": {},
  "scope_notes": [],
  "boundary_assertions": {}
}
```

`source_trace` preserves the case source, design object, contexts, observed
behavior, labels, feature hints, known limits, and authority metadata so
downstream consumers can see provenance and uncertainty.

## Feature Buckets

V1 always emits these feature buckets:

- `mechanism`
- `resource`
- `timing`
- `agency`
- `variance`
- `compression`
- `campaign`
- `flavor_or_social`

Each bucket includes:

- `projection_basis = feature_hints_and_case_context_report_only`
- `projection_status = hint_present | no_hint_supplied`
- `hint_labels`
- `input_fields_read`
- `present_source_fields`
- `interpretation_boundary = hint_not_authority`
- `authority_boundary = advisory_context_only`

The projector does not score, rank, or interpret feature hints as final truth.
Hints remain labels from the normalized case contract.

## Explicit Non-Goals

- No complex scoring.
- No model training.
- No learned/reranker default path.
- No default synthesis recommendation.
- No hard-gate, legality, or promotion authority.
- No capability graph registry edits in this slice.

## CLI

Write a template:

```text
python scripts/run_cardanalysis_feature_projection.py --write-template <path>
```

Run projection:

```text
python scripts/run_cardanalysis_feature_projection.py --input <case-json> --output-dir <dir>
```

`--input` may be a single case JSON file, a JSON array or `cases` manifest, or a
fixture directory containing JSON case files.

The CLI writes:

- `cardanalysis_feature_projection.md`
- `cardanalysis_feature_projection_snapshot.json`
- `cardanalysis_feature_projection_manifest.json`

## Downstream Impact

This V1 keeps the payload semantics aligned with the existing graph artifact:
`feature_projection_payload`.

Because it does not change the artifact meaning beyond implementing the
documented report-only boundary, this slice should not invalidate downstream
consumers by itself. MasterAgent should still review registration with:

- provider capability node: `cardanalysis_feature_projection_v1`
- consumes: `normalized_design_case`
- provides: `feature_projection_payload`
- depends on: `cardanalysis_case_input_contract_v1`
- consumes: `authority_boundary_contract`
- review-gated with: `evaluation_autonomous_design_model_v1`
- review-gated with: `mechanism_axis_discovery_v1`

## Fixture Notes

`tests/fixtures/combat_analysis/feature_projection_v1/` includes direct
normalized projection samples for exam-sensitivity blind spots that are already
represented in the mechanism case library. These samples make Defect
orb/focus/power same-lane drift, Defect package synergy collapse, Watcher
wrong-stance failure states, Watcher retain/scry same-lane role swaps, and
Watcher wrath/calm character texture readable as feature buckets.

The same fixture family also includes four axis-first lane-review sensitivity
samples for Silent, Ironclad, Defect, and Watcher. These r4 samples keep the
same STS1 mechanism lanes visible while surfacing content-quality deltas such
as axis drift, character texture mismatch, STS1-like wording drift,
failure-state floor, combo/setup tax, package synergy collapse, and fun-tension
drift.

They are not additional reviewed evidence. They keep `evidence_tier =
human_curated`, `review_status = review_needed`, and
`authority_boundary = advisory_context_only`.

## Validation

Focused validation:

```text
py -3.11 -m pytest tests/toolkit/combat_analysis/test_feature_projection_v1.py tests/scripts/test_run_cardanalysis_feature_projection.py -q
```

Shared guardrails:

```text
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```
