# Control Discipline Ideal Human Review Feedback V1

## Purpose

`control_discipline_ideal_human_review_feedback_v1` is a report-only feedback
capture scaffold for one
`control_discipline_ideal_candidate_batch_exam_v1` snapshot.

It preserves the exam's ranked candidates, recommended human review order, and
per-candidate risk summaries while creating empty keep/revise/reject and review
dimension slots for a later owner review pass. When the owner is unavailable,
V1 explicitly records that the pipeline is awaiting human review and blocks
repair-plan generation, formal card text, runtime readiness, and promotion.

## Scope

The V1 scaffold consumes:

- a candidate batch exam snapshot;
- ranked candidates;
- recommended human review order;
- per-candidate risk summaries for second-career, complexity, package
  completeness, and generic-goodstuff drift.

It outputs:

- a human review feedback template;
- candidate-level keep/revise/reject decision slots;
- empty required review dimensions;
- owner-unavailable placeholder mode;
- review completeness status;
- next repair-plan readiness;
- automation preservation context for waiting or preparation.

## Required Review Dimensions

Every candidate slot includes:

- `discipline_fit`
- `ideal_temperament_fit`
- `second_career_risk`
- `complexity_budget`
- `package_completeness`
- `generic_goodstuff_drift`
- `next_round_instruction`

The decision slot must allow `keep`, `revise`, or `reject`, but the
owner-unavailable fixture keeps the decision value null.

## Owner-Unavailable Mode

The default V1 output supports the current no-human-available state:

- `review_status = awaiting_human_review`
- `owner_unavailable_placeholder_mode = true`
- `blocked_by_human_review = true`
- all decision slots are null;
- all reviewer values are null;
- `review_complete = false`
- `repair_plan_ready = false`
- `automation_wait_scaffold_ready = true`

This lets automation preserve context and prepare empty downstream input shapes
without claiming that a candidate has been accepted, rejected, reviewed, or
promoted.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.human_review_completed = false`
- `boundary_assertions.blocked_by_human_review = true`
- `boundary_assertions.ranking_is_authoritative = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.automatic_promotion_created = false`
- `boundary_assertions.runtime_readiness_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`
- `boundary_assertions.scorecard_weights_changed = false`

V1 does not:

- generate formal card text;
- write runtime card data;
- promote candidates;
- claim reviewed or accepted evidence;
- treat the exam ranking as authoritative;
- create hard gates;
- enable synthesis, learned behavior, or reranker behavior;
- change scorecard weights.

## Entrypoint

Generate the owner-unavailable feedback scaffold from the current exam fixture:

```powershell
python scripts/validate_control_discipline_ideal_human_review_feedback.py --exam tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_exam_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_human_review_feedback_current
```

Validate the fixture:

```powershell
python scripts/validate_control_discipline_ideal_human_review_feedback.py --input tests/fixtures/combat_analysis/control_discipline_ideal_human_review_feedback_v1 --json
```

Write an empty template:

```powershell
python scripts/validate_control_discipline_ideal_human_review_feedback.py --write-template tmp/combat_analysis/control_discipline_ideal_human_review_feedback_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_human_review_feedback_v1.py tests/scripts/test_validate_control_discipline_ideal_human_review_feedback.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_human_review_feedback_v1/`

It consumes the current candidate batch exam fixture and records all six
candidates as awaiting human review. The current waiting scaffold preserves the
exam's next automation preservation set:

- `white_order_fail_state_candidate_v1`
- `blue_truth_forecast_candidate_v1`
- `green_depth_compound_stability_candidate_v1`

## Intended Follow-Up

The next slice should either:

- build a repair-plan generator that consumes completed human decisions and
  next-round instructions; or
- build a complete-card draft request packet that only activates after a human
  decision selects a candidate for drafting.

Given the current owner-unavailable state, the repair-plan generator is the
more natural next contract: it can validate that it stays blocked until this
feedback scaffold is filled.
