# Cardanalysis Coverage Gap Report V1

- Tool: `cardanalysis_coverage_gap_report_v1`
- Status: report-only coverage scanner
- Runtime impact: none
- Graph registration: none by default

## Purpose

The coverage gap scanner answers one planning question:

```text
Where is current cardanalysis case, fixture, projection, and graph coverage thin,
and what should the next case-batch agents collect?
```

It is not an evaluator. It does not score designs, generate content, change
model heads, or decide whether a mechanism is viable.

## Scope

In scope:

- stable `cardanalysis_case_input_v1` normalized case inputs;
- `cardanalysis_feature_projection_v1` projection payloads and snapshots;
- `cardanalysis_case_projection_sample_pack_v1` manifests and snapshots;
- capability graph context for current consumers and dependencies;
- deterministic report-only gap inventory for next case-batch planning.

Out of scope:

- modifying evaluators;
- modifying `case_input_contract.py`;
- modifying `feature_projection.py`;
- modifying `mechanism_axis_discovery.py`;
- modifying `capability_graph_registry.py`;
- modifying `report_only_surface_registry.py`;
- hard gates, default recommendation, synthesis, learned, or reranker behavior;
- promoting source-mined or generated cases to reviewed evidence.

## Inputs

The CLI accepts repeated `--input <path>` values.

Recognized stable inputs:

- one normalized case JSON file;
- a directory containing normalized case JSON files;
- a `{"cases": [...]}` normalized case collection;
- a feature-projection payload or snapshot;
- a case-projection sample-pack input manifest;
- a case-projection sample-pack normalized or projection snapshot;
- a coverage-gap scanner input manifest produced by `--write-template`.

Unrecognized JSON is a soft warning. Missing input paths and invalid JSON are
hard CLI errors.

The first-round template includes existing scan inputs:

- `tests/fixtures/combat_analysis/case_input_contract_v1`
- `tests/fixtures/combat_analysis/feature_projection_v1`
- `tests/fixtures/combat_analysis/existing_asset_case_adapter_v1`
- `tests/fixtures/combat_analysis/case_projection_sample_pack_v1`
- existing optional case-library directories such as
  `bbs_social_case_library_v1`

Optional future families are listed separately when absent:

- `mechanism_case_library_v1`
- `enemy_archetype_model_v1`

## Outputs

The CLI writes:

- `coverage_gap_report.md`
- `snapshot.json`
- `manifest.json`

The snapshot payload keeps:

```text
schema_version = cardanalysis_coverage_gap_report_v1
evaluation_mode = report_only
authority_boundary = advisory_context_only
hard_gate_impact = none
```

Required report sections:

- `scanned_inputs`
- `present_case_families`
- `missing_case_families`
- `mechanism_axis_coverage`
- `basic_axis_coverage`
- `enemy_archetype_coverage`
- `campaign_phase_coverage`
- `source_tier_distribution`
- `review_status_distribution`
- `source_mined_or_generated_followups`
- `undercovered_allowed_consumers`
- `graph_context`
- `recommended_next_case_batches`
- `boundary_assertions`

## Coverage Dimensions

Basic axis coverage tracks:

- draw
- discard
- energy
- block / defense
- status
- search / tutor
- exhaust / removal / transform
- temporary generation

Mechanism axis coverage tracks:

- position / redirect
- charge / delayed payoff
- stance / mode switch
- threshold payoff
- sacrifice / stress cost
- curse / pollution
- summon / temporary object
- chain / combo / loop

Enemy archetype coverage tracks first-round labels such as frontload checks,
multi-enemy pressure, scaling races, status pressure, debuff/control, summons,
elite punishers, and boss phase shifts.

Campaign phase coverage tracks starter, build, pivot, mature, late, and
recovery-pressure coverage.

Statuses are report-only:

- `missing`
- `advisory_only`
- `thin_reviewed`
- `covered`

These are planning labels. They are not pass/fail authority.

## Source Boundary

`source_mined_reference` and `generated_hypothesis` cases remain below reviewed
authority. The scanner may list them in
`source_mined_or_generated_followups`, but the suggested follow-up is review or
human-curation, not automatic promotion.

## Graph Context

The scanner reads `build_cardanalysis_capability_graph()` and impact reports for
`normalized_design_case` and `feature_projection_payload`.

It does not register itself as a canonical capability, task node, report-only
surface, or artifact provider. If this scanner becomes part of repeated
MasterAgent planning, graph registration should be a separate explicit
MasterAgent decision.

## Entrypoints

```bash
python scripts/run_cardanalysis_coverage_gap_report.py --write-template <path>
python scripts/run_cardanalysis_coverage_gap_report.py --input <path> --output-dir <dir>
py -3.11 -m pytest tests/toolkit/combat_analysis/test_coverage_gap_report_v1.py tests/scripts/test_run_cardanalysis_coverage_gap_report.py -q
```
