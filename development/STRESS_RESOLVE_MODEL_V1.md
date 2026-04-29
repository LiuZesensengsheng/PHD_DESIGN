# Stress Resolve Model V1

## Purpose

`stress_resolve_model_v1` is a report-only planning head for HP, stress,
resolve, affliction-like threshold events, and virtue-like positive threshold
events.

It is inspired by external dark-fantasy dungeon design patterns, but external
source-mined material is not project reviewed evidence. The model only produces
advisory context for human design review.

## Authority Boundary

- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `hard_gate_impact`: `none`

The model must not:

- wire campaign or combat runtime behavior,
- create hard gates,
- change default recommendation or synthesis paths,
- enable learned or reranker defaults,
- claim Darkest Dungeon material as reviewed project evidence.

## Source Tiers

The input surface distinguishes three source statuses:

- `source_mined`: source-mined external observations; useful for exploration,
  never reviewed evidence by itself.
- `design_reference`: human-readable design-reference framing; useful for model
  vocabulary, not proof.
- `reviewed`: project-reviewed context such as accepted authority-boundary docs
  or reviewed internal reports.

Any reference with `reference_family = "darkest_dungeon"` must remain
`source_mined` or `design_reference`. The implementation rejects it if marked
`reviewed`.

## Model Dimensions

V1 reports these dimensions:

- HP and stress as distinct but coupled pressure tracks.
- Combat stress accumulation versus campaign-long stress carryover.
- Recovery windows and their route/resource tradeoffs.
- Affliction-like collapse thresholds and virtue-like positive threshold events.
- Player agency versus uncontrollable punishment.
- Whether failed resolve outcomes still preserve local value.
- Relationship to campaign power-curve phase context.

## Relationship To Cardanalysis Graph

This branch does not register the model in
`tools/combat_analysis/capability_graph_registry.py` and does not connect it to
`normalized_design_case` or `feature_projection_payload`.

Future graph work can add a `stress_resolve_model_v1` task or capability node
after integration review. Suggested future edges:

- optional consume `normalized_design_case`,
- optional consume `feature_projection_payload`,
- optional review-gate with `campaign_power_curve_report_v1`,
- provide a report-only `stress_resolve_summary` artifact.

## CLI

Write a template:

```powershell
python scripts/run_stress_resolve_model.py --write-template tmp/stress_resolve_template.json
```

Run fixtures:

```powershell
python scripts/run_stress_resolve_model.py --input tests/fixtures/combat_analysis/stress_resolve_model_v1/stress_resolve_cases_v1.json --output-dir tmp/combat_analysis/stress_resolve_model_v1
```

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_stress_resolve_model_v1.py tests/scripts/test_run_stress_resolve_model.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```
