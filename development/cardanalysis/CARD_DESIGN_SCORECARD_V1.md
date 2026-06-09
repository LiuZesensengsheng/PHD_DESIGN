# Card Design Scorecard V1

## Purpose

`card_design_scorecard_v1` is a report-only scoring surface for current
card-package exam outputs.

It answers:

```text
Can an existing card-package exam, exam-iteration run, or STS1 four-character
exam be converted into comparable advisory design scores without becoming a
hard gate or promotion authority?
```

## Workflow Position

```text
card_package_exam_v1
  or exam_iteration_run_v1
  or sts1_four_character_exam_v1
  -> card_design_scorecard_v1
```

`scripts/run_sts1_four_character_exam.py` also writes scorecard artifacts in
the same output directory so the all-role STS1 exam has comparable scores by
default.

## Dimensions

V1 scores each case on a 0-100 advisory scale across:

- `schema_completeness`
- `axis_alignment`
- `character_identity`
- `sts1_like_fit`
- `strength_risk_control`
- `combo_risk_control`
- `fun_tension`
- `package_synergy`
- `failure_state_quality`

The scorecard uses direct signals when available and named proxy notes when a
dimension is not yet backed by a dedicated model head.

The snapshot now also includes report-only `dimension_explanations`. These name
the current proxy inputs for each dimension and the visibility lane reviewers
should inspect before treating a stable score as equivalent content:

- `axis_alignment` -> axis alignment
- `character_identity` -> character texture
- `sts1_like_fit` -> STS1-like fit
- `strength_risk_control` -> strength risk
- `combo_risk_control` -> combo risk
- `fun_tension` -> fun tension
- `package_synergy` -> package synergy
- `failure_state_quality` -> failure-state quality

Optional `scorecard_dimension_visibility_notes` payloads can be shown in the
Markdown report with `--visibility-notes`. The overlay can surface same-score
content movement, but it does not change `card_design_scorecard_v1` scores,
weights, hard-gate behavior, or authority.

Reusable same-score visibility-note fixtures live under:

```text
tests/fixtures/combat_analysis/card_design_scorecard_visibility_notes_v1/
```

## Future Extension Points

The V1 payload reserves explicit extension points for:

- `stress_threshold_branch_model_v1`
- `campaign_curve_card_package_bridge_v1`

Those future heads may add richer context, but this scorecard must not silently
turn their report-only readouts into hard gates.

## Boundary

This surface does not:

- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

Scores are advisory comparison aids only. Human review is still required before
any design promotion.

## Entrypoints

```powershell
python scripts/run_card_design_scorecard.py --input tmp/combat_analysis/sts1_four_character_exam_current/sts1_four_character_exam_v1_snapshot.json --output-dir tmp/combat_analysis/card_design_scorecard_current
python scripts/run_card_design_scorecard.py --input <supported_exam_or_iteration_snapshot.json> --visibility-notes <scorecard_dimension_visibility_notes.json> --output-dir tmp/combat_analysis/card_design_scorecard_with_visibility_notes_current
python scripts/run_sts1_four_character_exam.py --output-dir tmp/combat_analysis/sts1_four_character_exam_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_design_scorecard_v1.py tests/toolkit/combat_analysis/test_report_only_cli_artifact_runner_v1.py -q
```

## Interpretation

A clean scorecard run means a supported report-only source can be transformed
into comparable scores and dimension averages. It does not prove autonomous LLM
card-design quality, card balance, reviewed evidence status, or promotion
readiness.

The former scorecard calibration and delta-report side readers are retired.
Current progress comparison should use retained canonical exam/readout payloads
and the facade-backed advisory exam or review-pack routes rather than rebuilding
a separate scorecard side chain.

Use `autonomous_card_package_design_run_v1` when the scorecard belongs to a
supplied complete-card draft that should be audited as axis-first. That run
records the chain from mechanism-axis search through package seed, variant
handoff, exam iteration, package exam, and scorecard without generating card
text or promoting cards.
