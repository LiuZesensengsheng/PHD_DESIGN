# Control Discipline Ideal Complete Card Draft Request V1

## Purpose

`control_discipline_ideal_complete_card_draft_request_v1` is a report-only
scaffold that consumes one `control_discipline_ideal_repair_plan_v1` snapshot
and records whether the control-discipline plus ideal loop may ask for
`complete_card_draft_v1` package drafts.

In the current owner-unavailable state, V1 intentionally stays blocked. It
preserves candidate order, advisory risk context, and empty draft request slots
so automation can wait or prepare, but it does not issue a draft request from
an incomplete repair plan.

## Scope

The V1 draft request scaffold consumes:

- source repair-plan snapshot;
- source repair-plan readiness and generation status;
- candidate repair slots;
- candidate repair actions and next-round instructions;
- automation preservation context.

It outputs:

- `draft_request_ready` and `draft_request_generated` status;
- candidate-level complete-card draft request slots;
- waiting fields and blocked-until reasons;
- automation-can-prepare and cannot-advance lists;
- explicit report-only boundary assertions.

## Current Owner-Unavailable Behavior

For the current fixture:

- `source_repair_plan_ready = false`
- `source_repair_plan_generated = false`
- `blocked_by_human_review = true`
- `blocked_by_repair_plan = true`
- `draft_request_status = blocked_awaiting_repair_plan_ready`
- `draft_request_ready = false`
- `draft_request_generated = false`
- all candidate draft request slots keep:
  - `draft_package_id_hint = null`
  - `draft_request_payload = null`

Automation may preserve candidate ids, review order, ranked order, risk
summaries, source repair-plan refs, and empty draft request slots. It may not
call an LLM or external generator, write complete-card draft text, open runtime
card data, or promote cards.

## Ready Repair-Plan Behavior

V1 also validates the future ready shape. A ready draft request scaffold
requires:

- `source_repair_plan_ready = true`
- `source_repair_plan_generated = true`
- `blocked_by_repair_plan = false`
- source repair slots with keep/revise/reject decisions;
- next-round instruction values for carried candidates;
- `draft_request_ready = true`
- `draft_request_generated = true`

Ready keep/revise candidates receive report-only request payloads targeting
`complete_card_draft_v1`. Rejected candidates are explicitly excluded. Even in
the ready shape, V1 does not write complete card text or call any generator.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.ranking_is_authoritative = false`
- `boundary_assertions.repair_plan_is_authoritative = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.automatic_promotion_created = false`
- `boundary_assertions.runtime_readiness_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.complete_card_draft_generated = false`
- `boundary_assertions.complete_card_draft_generated_by_runtime = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`
- `boundary_assertions.scorecard_weights_changed = false`

## Entrypoint

Generate the current blocked draft request scaffold:

```powershell
python scripts/run_control_discipline_ideal_complete_card_draft_request.py --repair-plan tests/fixtures/combat_analysis/control_discipline_ideal_repair_plan_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_exam_v1_human_review_feedback_v1_repair_plan_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_complete_card_draft_request_current
```

Validate the fixture:

```powershell
python scripts/run_control_discipline_ideal_complete_card_draft_request.py --input tests/fixtures/combat_analysis/control_discipline_ideal_complete_card_draft_request_v1 --json
```

Write an empty template:

```powershell
python scripts/run_control_discipline_ideal_complete_card_draft_request.py --write-template tmp/combat_analysis/control_discipline_ideal_complete_card_draft_request_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_complete_card_draft_request_v1.py tests/scripts/test_run_control_discipline_ideal_complete_card_draft_request.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_complete_card_draft_request_v1/`

It consumes the current owner-unavailable repair-plan fixture and keeps all six
candidates blocked until human review and repair-plan readiness supply the
needed decisions and next-round instructions.

## Intended Follow-Up

After this slice, the next useful contract is a draft-submission readiness
adapter for this control-discipline plus ideal request packet. It should remain
blocked when `draft_request_ready = false`.
