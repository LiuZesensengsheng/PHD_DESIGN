# Position Redirect Code Preflight V1

## Purpose

`position_redirect_code_preflight_v1` is a report-only handoff surface between
Mechanism Axis Discovery Model Lab and later gameplay/content implementation.

It answers one narrow question:

- Can `position_redirect_threat_control` start a bounded code slice, and under which
  parameter/readability constraints?

It does not answer:

- whether `position_redirect_threat_control` is a formal mechanism family
- whether the project should change mechanism-axis hard gates
- whether synthesis/default recommendation should prefer the axis
- whether learned/reranker paths should be enabled

## Scope Boundary

In scope:

- go/no-go for a later bounded report-only or feature-flagged code slice
- displacement-vector bounds
- telegraph/readability bounds
- fail-state partial-solve evidence
- foundation-axis override sanity
- evidence-bundle visibility

Out of scope:

- gameplay runtime implementation
- card/content generation
- mechanism-axis contract edits
- viability hard-gate edits
- synthesis/default recommendation edits
- learned or reranker default changes
- treating source-mining or STS2 observations as reviewed evidence

## Required Scenarios

The preflight fixture must cover:

- `healthy_middle_band`
- `auto_solve_risk`
- `unreadable_telegraph`
- `foundation_override_sanity`
- `fail_state_partial_solve`

The current reviewed fixture is:

`tests/fixtures/combat_analysis/position_redirect_code_preflight_v1/position_redirect_code_preflight_reviewed_v1.json`

Current result:

- final decision: `code_handoff_ready_with_bounds`
- go/no-go: `go_with_bounds`

## Required Code Bounds

The next code-development agent should carry these bounds forward:

- cap the first implementation band at one or two displacement vectors
- reject full-solution telegraph overlays
- keep the preview compact and readable
- log fail-state partial-solve value
- keep damage and defense as comparison axes, not the mechanism identity

## Default Command

```powershell
python scripts/run_position_redirect_code_preflight.py --input tests/fixtures/combat_analysis/position_redirect_code_preflight_v1/position_redirect_code_preflight_reviewed_v1.json --output-dir <dir>
```

Write a template:

```powershell
python scripts/run_position_redirect_code_preflight.py --write-template <path>
```

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_position_redirect_code_preflight_v1.py tests/scripts/test_run_position_redirect_code_preflight.py -q
```

Registry and bundle checks:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_cardanalysis_evidence_bundle_v1.py tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py -q
```
