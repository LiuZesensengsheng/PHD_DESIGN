# Cardanalysis Report-Only Surface Registry V1

## Purpose

Prevent semantic drift after the fast report-only expansion wave.

This registry names the canonical owner for each current cardanalysis report-only
surface. New work should extend or consolidate into these surfaces instead of creating
parallel V1 modules with overlapping meaning.

## Canonical Surfaces

| Surface | Owner | CLI | Evidence Bundle Section |
| --- | --- | --- | --- |
| `deck_compression_report_v1` | `tools/combat_analysis/design_engine/deck_compression_report.py` | `scripts/run_deck_compression_report.py` | `deck_compression_summary` |
| `mechanism_fun_health_v1` | `tools/combat_analysis/design_studio/mechanism_fun_health_benchmark.py` | `scripts/run_mechanism_fun_health_benchmark.py` | `mechanism_fun_health_summary` |
| `card_package_health_v1` | `tools/combat_analysis/design_studio/card_package_health.py` | `scripts/run_card_package_health_benchmark.py` | `card_package_health_summary` |
| `design_iteration_brief_v1` | `tools/combat_analysis/design_engine/design_iteration_brief.py` | `scripts/run_design_iteration_brief.py` | `design_iteration_summary` |
| `mechanism_axis_discovery_v1` | `tools/combat_analysis/design_engine/mechanism_axis_discovery.py` | `scripts/run_mechanism_axis_discovery.py` | `mechanism_axis_discovery_summary` |
| `cardanalysis_evidence_bundle_v1` | `tools/combat_analysis/design_engine/cardanalysis_evidence_bundle.py` | none | evidence bundle root |

The machine-readable mirror lives in
`tools/combat_analysis/report_only_surface_registry.py`.

## Consolidation Rules

- Do not add a second V1 module for the same semantic surface.
- Treat overlapping branches as consolidation inputs, not direct merge candidates.
- Keep report-only output explicitly marked with `evaluation_mode=report_only`.
- Report-only manifests and snapshots must not expose `overall_pass` or `hard_gates`
  unless the underlying evaluator already owns explicit hard gates.
- Evidence bundle output may flag review conflicts, but it must not become pass/fail
  authority.
- `design_engine` must not import `design_studio`; shared registry data should stay as
  strings or move below both layers.

## Known Consolidation Inputs

- `deck_compression_model_v1` should consolidate into
  `deck_compression_report_v1`; useful pieces are persistent thinning visibility,
  deck-size sensitivity reason codes, and removal/transform/exhaust distinctions.
- `mechanism_fun_health_evaluator_v1` should consolidate into
  `mechanism_fun_health_v1`; useful pieces are explicit degeneracy signal visibility,
  review-pack completeness indicators, and reviewer-readiness documentation.

## Validation

Run the registry guard when changing any report-only surface, CLI, evidence bundle
section, or default entrypoint:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py -q
```

For a mainline merge that touches report-only surfaces, also run the owning evaluator
and CLI tests listed in `CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`.
