# Control Discipline Ideal Repair Plan V1

## Purpose

`control_discipline_ideal_repair_plan_v1` is a report-only scaffold that
consumes one `control_discipline_ideal_human_review_feedback_v1` snapshot and
records whether the control-discipline plus ideal candidate loop may produce a
next-round repair plan.

In the current owner-unavailable state, V1 intentionally stays blocked. It
preserves candidate order, advisory risk context, and empty candidate repair
slots so automation can wait or prepare, but it does not infer human decisions
or generate repairs from empty review fields.

## Scope

The V1 repair-plan scaffold consumes:

- source human-review feedback snapshot;
- source review status and completeness;
- candidate keep/revise/reject decision slots;
- required review dimensions;
- next-round instructions;
- automation preservation context.

It outputs:

- `repair_plan_ready` and `repair_plan_generated` status;
- candidate-level repair slots;
- waiting fields and blocked-until reasons;
- automation-can-prepare and cannot-advance lists;
- explicit report-only boundary assertions.

## Current Owner-Unavailable Behavior

For the current fixture:

- `source_review_status = awaiting_human_review`
- `source_review_complete = false`
- `blocked_by_human_review = true`
- `plan_generation_status = blocked_awaiting_human_review`
- `repair_plan_ready = false`
- `repair_plan_generated = false`
- all candidate repair slots keep:
  - `source_human_decision = null`
  - `repair_action = null`
  - `next_round_instruction = null`
  - `repair_objectives = []`

Automation may preserve candidate ids, review order, ranked order, risk
summaries, and empty repair slots. It may not choose keep/revise/reject, create
repair objectives, open a complete-card draft request, or promote runtime
readiness.

## Completed-Review Behavior

V1 also validates the future ready shape. A ready repair-plan scaffold requires:

- `source_review_status = human_review_recorded`
- source review completeness true;
- every candidate has a keep/revise/reject decision;
- every required review dimension has a reviewer value;
- `next_round_instruction` is supplied;
- `repair_plan_ready = true`
- `repair_plan_generated = true`

Even in the ready shape, the artifact remains report-only. It still does not
generate formal card text, write runtime card data, create hard gates, claim
reviewed evidence, or change scorecard weights.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
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

## Entrypoint

Generate the current blocked repair-plan scaffold:

```powershell
python scripts/run_control_discipline_ideal_repair_plan.py --feedback tests/fixtures/combat_analysis/control_discipline_ideal_human_review_feedback_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_exam_v1_human_review_feedback_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_repair_plan_current
```

Validate the fixture:

```powershell
python scripts/run_control_discipline_ideal_repair_plan.py --input tests/fixtures/combat_analysis/control_discipline_ideal_repair_plan_v1 --json
```

Write an empty template:

```powershell
python scripts/run_control_discipline_ideal_repair_plan.py --write-template tmp/combat_analysis/control_discipline_ideal_repair_plan_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_repair_plan_v1.py tests/scripts/test_run_control_discipline_ideal_repair_plan.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_repair_plan_v1/`

It consumes the current owner-unavailable human-review feedback fixture and
keeps all six candidates blocked until human review supplies decisions and
next-round instructions.

## Intended Follow-Up

After this slice, the next useful contract is a complete-card draft request
packet for reviewed candidates. It should consume a ready repair-plan scaffold
and remain blocked when `repair_plan_ready = false`.
