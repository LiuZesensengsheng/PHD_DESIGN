# Card Design Scorecard Delta Report V1

## Purpose

`card_design_scorecard_delta_report_v1` is a report-only progress reader for
ordered `card_design_scorecard_v1` snapshots.

It answers:

```text
Did the latest card-design exam scorecard actually improve, regress, or stay
flat relative to a prior scorecard, and which dimensions should the next
iteration focus on?
```

## Workflow Position

```text
card_design_scorecard_v1 snapshot
  + card_design_scorecard_v1 snapshot
  -> card_design_scorecard_delta_report_v1
```

Use it after scorecard calibration has shown the scorecard can separate healthy
controls from known failure-family controls. Delta reports are comparison aids;
they do not recalibrate score weights.

## Readouts

V1 compares the first input as the baseline and the last input as the latest
snapshot.

It reports:

- aggregate score delta and movement;
- per-dimension average movement;
- weak dimensions that resolved, persisted, or appeared;
- matched case movement by `case_id`;
- resolved, persistent, and new scorecard issue flags;
- next iteration focus hints for prompt, handoff, axis-search, or exam-coverage
  follow-up.

## Boundary

This surface does not:

- change scorecard weights;
- write runtime card data;
- generate complete card drafts;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- call an LLM API;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

`delta_status` is an advisory progress label only. It is not a pass/fail
authority for cards, card packages, generation, or promotion.

## Entrypoints

```powershell
python scripts/run_card_design_scorecard_delta_report.py --input <baseline_card_design_scorecard_v1_snapshot.json> --input <latest_card_design_scorecard_v1_snapshot.json> --output-dir tmp/combat_analysis/card_design_scorecard_delta_report_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_design_scorecard_delta_report_v1.py tests/scripts/test_run_card_design_scorecard_delta_report.py -q
```

## Interpretation

A clean delta report means the system can compare existing scorecards and name
likely next-focus dimensions. It does not prove autonomous card-design quality,
card balance, reviewed evidence status, or promotion readiness.

When comparing fresh axis-first draft rehearsals, use
`axis_first_rehearsal_scorecard_comparison_v1` as the wrapper. It preserves this
delta report's non-authoritative boundary while adding attempt-level audit
warnings for distinct draft packages that do not form a matched case pair.
