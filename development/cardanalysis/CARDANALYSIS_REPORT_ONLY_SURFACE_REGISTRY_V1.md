# Cardanalysis Report-Only Surface Registry V1

## Purpose

Prevent semantic drift after the fast report-only expansion wave.

This registry names the canonical owner for each current cardanalysis report-only
surface. New work should extend or consolidate into these surfaces instead of creating
parallel V1 modules with overlapping meaning.

## Canonical Surfaces

| Surface | Route Class | Owner | CLI | Evidence Bundle Section |
| --- | --- | --- | --- | --- |
| `mechanism_fun_health_v1` | `calibration_support` | `tools/combat_analysis/design_studio/mechanism_fun_health_benchmark.py` | none | `mechanism_fun_health_summary` |
| `card_package_health_v1` | `calibration_support` | `tools/combat_analysis/design_studio/card_package_health.py` | none | `card_package_health_summary` |
| `evaluation_autonomous_design_model_v1` | `non_facade_design_support` | `tools/combat_analysis/design_engine/evaluation_autonomous_design_model.py` | none | evidence bundle root |
| `cardanalysis_evidence_bundle_v1` | `evidence_support` | `tools/combat_analysis/design_engine/cardanalysis_evidence_bundle.py` | none | evidence bundle root |
| `campaign_power_curve_report_v1` | `non_facade_design_support` | `tools/combat_analysis/design_engine/campaign_power_curve_model.py` | none | `campaign_power_curve_summary` |

The machine-readable mirror lives in
`tools/combat_analysis/report_only_surface_registry.py`.

Route classes are inventory labels, not new workflow authority:

- `calibration_support` surfaces keep reviewed benchmark or health calibration
  behavior for retained consumers.
- `evidence_support` surfaces normalize advisory evidence for retained
  consumers.
- `non_facade_design_support` surfaces are retained design-support libraries
  for broader design, campaign, or enemy work, but they are not the current
  Codex-facing card package workflow.

New card-package design work should start from
`scripts/run_cardanalysis_tool_facade.py`, not from these retained surfaces,
unless a route-map update explicitly promotes a new facade action.

`evaluation_autonomous_design_model_v1` is retained as a library/fixture
surface. Its former standalone CLI wrapper is retired so it does not look like a
current card package entrypoint.

`mechanism_fun_health_v1` is retained as a calibration library/fixture surface.
Its former standalone CLI wrapper is retired; use the focused toolkit test when
changing mechanism fun/health calibration behavior.

`card_package_health_v1` is retained as a calibration library/fixture surface.
Its former standalone CLI wrapper is retired; current draft-package validation
should use `card_package_exam_v1`, which embeds `card_package_health_v1`
advisory labels.

## Consolidation Rules

- Do not add a second V1 module for the same semantic surface.
- Treat overlapping branches as consolidation inputs, not direct merge candidates.
- Keep report-only output explicitly marked with `evaluation_mode=report_only`.
- Report-only manifests and snapshots must not expose `overall_pass` or `hard_gates`
  unless the underlying evaluator already owns explicit hard gates.
- Evidence bundle output may flag review conflicts, but it must not become pass/fail
  authority.
- `evaluation_autonomous_design_model_v1` may orchestrate existing summaries and
  package-skeleton wording, but it must not replace canonical scoring owners or create
  formal cards.
- `campaign_power_curve_report_v1` may provide campaign pacing and encounter
  validation context, but it must not define monster stats, hard counters, or runtime
  encounter implementation.
- `campaign_power_curve_report_v1` is retained as a report-only
  library/fixture surface. Its standalone CLI wrapper is retired; current
  Codex-facing package work should use facade-backed exam/review routes or
  `campaign_curve_profile_v1` where a current package exam needs advisory
  campaign fit context.
- The former `virtue_affliction_design_model_v1` surface is retired from active
  registry ownership. DD1-inspired stress-threshold, branch-outcome, contagion,
  agency, and long-term-cost research may inform a future generic
  `stress_threshold_branch_model_v1`, but it must re-enter through the facade
  route map and preserve report-only boundaries.
- The former `position_redirect_code_preflight_v1` control-direction handoff is
  retired from active registry ownership. Historical position-redirect evidence
  may remain in mechanism-discovery fixtures, but no dedicated report-only
  preflight surface should be rebuilt without updating the facade route map.
- The former `deck_compression_report_v1` and `design_iteration_brief_v1`
  owner surfaces are retired from active registry ownership. Evidence bundles
  and autonomous-design inputs may still read historical
  `deck_compression_summary` and `design_iteration_summary` sections as
  optional compatibility fields, but new Codex-facing work should enter through
  facade-backed routes instead of rebuilding these direct report owners.
- The former `mechanism_axis_discovery_v1` surface is retired from active
  registry ownership. Retained evidence bundles may still carry historical
  `mechanism_axis_discovery_summary` sections, but new axis preparation should
  use facade-backed mechanism-axis search, design-brief, and package-seed
  routes.
- `design_engine` must not import `design_studio`; shared registry data should stay as
  strings or move below both layers.

## Known Consolidation Inputs

- Historical `deck_compression_report_v1` inputs may inform future facade-backed
  package or route-readiness exams, especially persistent thinning visibility,
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

For a mainline merge that touches report-only surfaces, also run the owning
toolkit evaluator tests listed in `CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`;
only run CLI tests for surfaces whose standalone wrappers remain active.
