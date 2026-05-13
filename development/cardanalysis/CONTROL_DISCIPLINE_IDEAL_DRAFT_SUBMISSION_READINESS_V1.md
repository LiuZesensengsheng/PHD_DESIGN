# Control Discipline Ideal Draft Submission Readiness V1

## Purpose

`control_discipline_ideal_draft_submission_readiness_v1` is a report-only
adapter that consumes one
`control_discipline_ideal_complete_card_draft_request_v1` snapshot and records
whether the control-discipline plus ideal loop may prepare for an owner or
external `complete_card_draft_v1` submission.

In the current owner-unavailable state, V1 intentionally stays blocked. It
preserves candidate order, advisory risk context, and empty submission slots so
automation can wait or prepare validation scaffolds, but it does not collect a
draft file or issue a prompt-application intake from an incomplete draft request.

## Scope

The V1 draft-submission readiness scaffold consumes:

- source complete-card draft request snapshot;
- source draft-request readiness and generation status;
- candidate draft request slots;
- source draft request payloads for ready future candidates;
- automation preservation context.

It outputs:

- `ready_for_draft_submission` and `submission_packet_generated` status;
- candidate-level owner/external draft submission slots;
- waiting fields and blocked-until reasons;
- automation-can-prepare and cannot-advance lists;
- explicit report-only boundary assertions.

## Current Owner-Unavailable Behavior

For the current fixture:

- `source_draft_request_ready = false`
- `source_draft_request_generated = false`
- `blocked_by_human_review = true`
- `blocked_by_repair_plan = true`
- `blocked_by_draft_request = true`
- `submission_readiness_status =
  blocked_awaiting_complete_card_draft_request_ready`
- `ready_for_draft_submission = false`
- `submission_packet_generated = false`
- all candidate submission readiness slots keep:
  - `complete_card_draft_submission_slot = null`
  - `submission_metadata_template = null`

Automation may preserve candidate ids, review order, ranked order, risk
summaries, source draft-request refs, and empty submission slots. It may not
collect an owner/external complete-card draft, validate a submitted draft, record
prompt-application intake, call an LLM or external generator, write complete
card text, open runtime card data, or promote cards.

## Ready Draft-Request Behavior

V1 also validates the future ready shape. A ready submission readiness scaffold
requires:

- `source_draft_request_ready = true`
- `source_draft_request_generated = true`
- `blocked_by_draft_request = false`
- source request slots with ready keep/revise candidates or rejected exclusions;
- source ready request payloads for carried candidates;
- `ready_for_draft_submission = true`
- `submission_packet_generated = true`

Ready keep/revise candidates receive report-only owner/external submission
slots and generation-metadata templates. Rejected candidates are explicitly
excluded. Even in the ready shape, V1 does not collect a complete-card draft,
write complete card text, or call any generator.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.ranking_is_authoritative = false`
- `boundary_assertions.repair_plan_is_authoritative = false`
- `boundary_assertions.draft_request_is_authoritative = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.automatic_promotion_created = false`
- `boundary_assertions.runtime_readiness_created = false`
- `boundary_assertions.external_draft_collected = false`
- `boundary_assertions.prompt_application_intake_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.complete_card_draft_generated = false`
- `boundary_assertions.complete_card_draft_generated_by_runtime = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.runtime_card_definition_created = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`
- `boundary_assertions.scorecard_weights_changed = false`

## Entrypoint

Generate the current blocked draft-submission readiness scaffold:

```powershell
python scripts/run_control_discipline_ideal_draft_submission_readiness.py --draft-request tests/fixtures/combat_analysis/control_discipline_ideal_complete_card_draft_request_v1 --output-dir tmp/combat_analysis/control_discipline_ideal_draft_submission_readiness_current
```

Validate the fixture:

```powershell
python scripts/run_control_discipline_ideal_draft_submission_readiness.py --input tests/fixtures/combat_analysis/control_discipline_ideal_draft_submission_readiness_v1 --json
```

Write an empty template:

```powershell
python scripts/run_control_discipline_ideal_draft_submission_readiness.py --write-template tmp/combat_analysis/control_discipline_ideal_draft_submission_readiness_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_draft_submission_readiness_v1.py tests/scripts/test_run_control_discipline_ideal_draft_submission_readiness.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_draft_submission_readiness_v1/`

It consumes the current owner-unavailable complete-card draft request fixture
and keeps all six candidates blocked until human review, repair-plan readiness,
and draft-request readiness supply the needed request payloads.

## Intended Follow-Up

After this slice, the next useful contract is an owner/external complete-card
draft submission manifest or intake adapter that consumes a ready
draft-submission readiness packet and a supplied `complete_card_draft_v1` file.
It should remain blocked while `ready_for_draft_submission = false`.
