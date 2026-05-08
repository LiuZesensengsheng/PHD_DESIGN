# Cardanalysis Case Progress Report V1

- Tool: `cardanalysis_case_progress_report_v1`
- Status: report-only case inventory and maturity dashboard
- Runtime impact: none
- Graph registration: `cardanalysis_case_progress_report_v1`

## Purpose

The case progress report answers a different planning question than the coverage
gap scanner:

```text
How mature is the current cardanalysis case inventory by family, evidence tier,
consumer, and tracked metric group?
```

It is a dashboard and ledger, not an evaluator. It does not score designs,
generate content, change model heads, decide mechanism viability, or promote
evidence.

## Relationship To Coverage Gap

`cardanalysis_coverage_gap_report_v1` answers "what should we collect next?"

`cardanalysis_case_progress_report_v1` answers "how complete does the current
case base look, and which consumers still lack reviewed evidence?"

The progress report intentionally reuses the coverage-gap scanner's stable input
loader and target coverage sections so the two tools stay comparable.

## Inputs

The CLI accepts repeated `--input <path>` values.

Recognized inputs match the coverage-gap scanner:

- one normalized case JSON file;
- a directory containing normalized case JSON files;
- a `{"cases": [...]}` normalized case collection;
- a feature-projection payload or snapshot;
- a case-projection sample-pack input manifest;
- a case-projection sample-pack normalized or projection snapshot;
- a coverage-gap scanner input manifest;
- a case-progress scanner input manifest produced by `--write-template`.

## Outputs

The CLI writes:

- `case_progress_report.md`
- `snapshot.json`
- `manifest.json`

The snapshot payload keeps:

```text
schema_version = cardanalysis_case_progress_report_v1
evaluation_mode = report_only
authority_boundary = advisory_context_only
hard_gate_impact = none
```

Required snapshot sections:

- `progress_summary`
- `case_family_progress`
- `metric_progress_groups`
- `consumer_attention`
- `source_tier_distribution`
- `review_status_distribution`
- `recommended_next_case_batches`
- `graph_context`
- `boundary_assertions`

## Maturity Labels

Case-family labels:

- `missing`
- `advisory_seed`
- `advisory_inventory`
- `reviewed_seed`
- `reviewed_covered`

Metric target statuses are inherited from the coverage-gap scanner:

- `missing`
- `advisory_only`
- `thin_reviewed`
- `covered`

Overall labels:

- `bootstrap_inventory`
- `broad_inventory_review_limited`
- `metric_coverage_still_thin`
- `case_backed_planning_ready`

These labels are planning metadata. They are not pass/fail authority and should
not be used to approve card packages, tune enemies, or enable generation.

## Graph Semantics

The tool is registered in the capability graph as a read-only planning
capability:

- consumes `normalized_design_case`;
- consumes `feature_projection_payload`;
- provides `cardanalysis_case_progress_snapshot`;
- depends on `authority_boundary_contract`;
- depends on `decision_report_only_surfaces_not_authoritative`.

It is not a canonical report-only registry surface and does not replace any
evaluator owner.

## Current Snapshot Reading

Running the default template on 2026-05-08 produced:

- `278` stable scanned cases;
- `84` reviewed cases;
- `22` projection payloads;
- reviewed ratio `0.302`;
- metric maturity average `0.962`;
- overall maturity `broad_inventory_review_limited`.

The strongest inventories are:

- `mechanism_case_library_v1`: `206` cases, `68` reviewed;
- `enemy_archetype_model_v1`: `39` cases, `12` reviewed.

The most visible reviewed-evidence gaps are:

- `campaign_experience_curve_v1`: `7` allowed cases, `0` reviewed;
- `card_package_health_v1`: `106` allowed cases, `0` reviewed.

This means the system has broad advisory coverage, but some downstream consumers
still need explicit human review before their evidence should be treated as
reviewed.

## Entrypoints

```bash
python scripts/run_cardanalysis_case_progress_report.py --write-template <path>
python scripts/run_cardanalysis_case_progress_report.py --input <path> --output-dir <dir>
py -3.11 -m pytest tests/toolkit/combat_analysis/test_case_progress_report_v1.py tests/scripts/test_run_cardanalysis_case_progress_report.py -q
```

