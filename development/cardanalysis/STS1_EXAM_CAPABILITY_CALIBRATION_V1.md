# STS1 Exam Capability Calibration V1

## Purpose

`sts1_exam_capability_calibration_v1` is a deterministic report-only sidecar for
the current STS1 card-package exam loop.

It answers:

```text
Which missing explanation dimensions should reviewers inspect before trusting
that a package is actually STS1-like and ready for the next human design pass?
```

## Current Gap Dimensions

V1 names two high-value gaps without adding score weights:

- `primary_axis_dominance`
- `early_floor_late_ceiling_balance`

`primary_axis_dominance` checks whether the stated primary axis actually appears
across the package roles, or whether a secondary axis / generic-goodstuff value
is explaining the package instead.

`early_floor_late_ceiling_balance` checks whether the package does useful work
before payoff assembly, or whether early turns are blank while late ceiling,
refund, setup-tax, or exactness pressure carries the experience.

## Inputs

V1 consumes existing report-only fixtures:

- happy-path `complete_card_draft_v1` STS1 packages;
- generated-attempt boundary controls from
  `llm_complete_card_draft_attempt_boundary_controls_v1`.

It reads card ids, roles, tags, numeric profile, setup tax, exactness dependency,
and evidence trace fields. It does not echo formal card rules text into its
snapshot.

## Output Shape

Required top-level fields:

- `contract_version`: `sts1_exam_capability_calibration_v1`
- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `calibration_scope`
- `hard_gate_impact`: `none`
- `score_weight_impact`: `none`
- `sample_summary`
- `calibrated_gap_dimensions`
- `per_package_readouts`
- `calibration_summary`
- `boundary_assertions`

The readout separates current happy-path packages from boundary controls so
reviewers can see which dimensions distinguish plausible risk samples without
changing the canonical exam or scorecard.

## Boundary

V1 does not:

- generate formal card text;
- write runtime card data;
- modify official card data;
- create hard gates;
- change card-package exam outcomes;
- change scorecard dimensions or weights;
- claim reviewed evidence;
- enable default synthesis;
- call an LLM/API;
- enable learned or reranker behavior.

The output is advisory context only. Human review still owns fun judgment,
archetype identity, numeric bands, formal wording, reviewed evidence promotion,
and runtime promotion or rejection.

## Control Package Help

This sidecar helps later control card-package production by making two failure
modes visible before human review:

- a control support or ideal texture becoming the real plan instead of the
  stated discipline axis;
- a package having no interactive floor before payoff, which can make control
  loops feel inert rather than deliberate.

It does not select, promote, reject, or repair control candidates by itself.

## Entrypoint

```powershell
python scripts/run_sts1_exam_capability_calibration.py --output-dir tmp/combat_analysis/sts1_exam_capability_calibration_current
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_exam_capability_calibration_v1.py tests/scripts/test_run_sts1_exam_capability_calibration.py -q
```

## V1 Fixture

The first fixture output lives under:

```text
tests/fixtures/combat_analysis/sts1_exam_capability_calibration_v1/
```

It reads the four STS1 happy-path owner drafts and the four STS1 boundary
controls. The current fixture identifies:

- Silent, Ironclad, and Defect boundary controls as
  `risk_secondary_axis_or_goodstuff_swallowing_primary`;
- Watcher boundary control as `risk_early_blank_late_explosion`;
- all happy-path owner drafts as clear/balanced on these two readouts.

These labels are explanation probes, not pass/fail authority.
