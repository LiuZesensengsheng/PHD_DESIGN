# Card Design Scorecard Calibration V1

## Purpose

`card_design_scorecard_calibration_v1` is a report-only control suite for
`card_design_scorecard_v1`.

It answers:

```text
Does the scorecard separate healthy card-package controls from known negative
controls, and do weak dimensions line up with the intended failure family?
```

## Workflow Position

```text
card_design_scorecard_v1 snapshot
  -> card_design_scorecard_calibration_v1
```

The default CLI path builds simulated STS1 four-character controls without
calling an LLM or generating card text:

- 4 characters: Silent, Ironclad, Defect, Watcher
- 9 scenario families per character
- 36 total control cases

## Scenario Families

- `healthy_baseline`
- `schema_gap`
- `axis_drift`
- `identity_drift`
- `sts1_like_gap`
- `strength_combo_risk`
- `fun_tension_gap`
- `package_synergy_gap`
- `failure_state_gap`

Each control declares an expected score range, expected rating, and expected
weak dimensions. Calibration succeeds only when the observed scorecard output
falls inside that expectation and the healthy baseline is separated from the
negative controls.

## Boundary

This surface does not:

- change scorecard weights;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- call an LLM API;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

The calibration status is an advisory tuning signal only. It is not a pass/fail
authority for cards, packages, generation, or promotion.

## Entrypoints

```powershell
python scripts/run_card_design_scorecard_calibration.py --output-dir tmp/combat_analysis/card_design_scorecard_calibration_current
python scripts/run_card_design_scorecard_calibration.py --input <card_design_scorecard_calibration_input_v1.json> --output-dir <dir>
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_design_scorecard_calibration_v1.py tests/scripts/test_run_card_design_scorecard_calibration.py -q
```

## Interpretation

A clean calibration run means the current scorecard can distinguish the built-in
control scenarios. It does not prove balance, reviewed evidence, autonomous LLM
quality, or promotion readiness.
