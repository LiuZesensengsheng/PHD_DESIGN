# Control Discipline Ideal Pilot V1

## Purpose

`control_discipline_ideal_pilot_v1` is a report-only input contract for the
first control-discipline plus ideal-temperament design pilot.

It prepares the next automation layer without generating card text. The
contract describes one discipline-owned combat loop, several ideal temperament
profiles, planned candidate package slots, and the human review form that must
be filled before any runtime or formal-card promotion work can happen.

## Layering Rule

The pilot keeps the current design layering explicit:

- discipline/career owns the primary combat loop;
- ideal owns temperament, reward bias, event pressure, and review texture;
- ideal must not become a second career, hidden moral score, or recurring
  per-turn combat burden.

This is the main guardrail for the control pilot. It lets later tools generate
multiple package hypotheses while preserving a single readable combat owner.

## Schema

Required top-level fields:

- `schema_version`: must be `control_discipline_ideal_pilot_v1`
- `pilot_id`
- `title`
- `source`
- `authority`
- `discipline_profile`
- `ideal_temperament_profiles`
- `candidate_package_manifest`
- `human_review_form`
- `pilot_guardrails`
- `next_stage_readiness`

`source` values are intentionally narrow:

- `source_type`: `design_note`, `human_curated`, or `generated_hypothesis`
- `evidence_tier`: `human_curated` or `speculative`
- `review_status`: `draft`, `review_needed`, or `hypothesis_draft`

Generated hypotheses must remain speculative and must use
`review_status = hypothesis_draft`.

`authority.authority_boundary` must be `advisory_context_only`. The
`forbidden_uses` list must include hard-gate promotion, legality decisions,
runtime card definitions, runtime card data writes, formal card generation,
reviewed-evidence claims, default synthesis paths, ideal-as-second-career use,
and hidden moral punishment.

`candidate_package_manifest.candidate_slots` are planned or generated
unreviewed report-only slots. A generated slot must name a
`package_proposal_ref`; a planned slot may leave that reference null. The
manifest must cover every ideal profile in the pilot.

`human_review_form.review_dimensions` must include:

- `discipline_fit`
- `ideal_temperament_fit`
- `second_career_risk`
- `complexity_budget`
- `keep_revise_reject`

## Guardrails

Every valid pilot must keep:

- `pilot_guardrails.report_only = true`
- `pilot_guardrails.discipline_owns_combat_loop = true`
- `pilot_guardrails.ideal_must_not_be_second_career = true`
- `pilot_guardrails.human_review_required_before_runtime = true`
- `pilot_guardrails.llm_api_called = false`
- `pilot_guardrails.runtime_card_data_written = false`
- `pilot_guardrails.formal_cards_promoted = false`
- `pilot_guardrails.hard_gate_created = false`
- `pilot_guardrails.default_synthesis_enabled = false`
- `pilot_guardrails.learned_or_reranker_enabled = false`
- `next_stage_readiness.runtime_promotion_ready = false`

These are validation rules, not prose-only conventions.

## Entrypoint

Write a template:

```powershell
python scripts/validate_control_discipline_ideal_pilot.py --write-template tmp/combat_analysis/control_discipline_ideal_pilot_template.json
```

Validate the fixture directory:

```powershell
python scripts/validate_control_discipline_ideal_pilot.py --input tests/fixtures/combat_analysis/control_discipline_ideal_pilot_v1
```

Print a machine-readable validation report:

```powershell
python scripts/validate_control_discipline_ideal_pilot.py --input tests/fixtures/combat_analysis/control_discipline_ideal_pilot_v1 --json
```

## V1 Fixture

The first fixture is
`tests/fixtures/combat_analysis/control_discipline_ideal_pilot_v1/control_discipline_ideal_pilot_sample_v1.json`.

It defines a control discipline profile, three ideal temperament profiles
(`white_order`, `blue_truth`, and `green_depth`), six planned unreviewed
candidate package slots, and a human review form that includes
`second_career_risk`.

## Non-Goals

V1 does not:

- generate cards, packages, prompts, or candidate text;
- call an external LLM or API;
- write runtime card data;
- promote formal cards or reviewed evidence;
- create hard gates, legality decisions, default synthesis paths, learned
  behavior, or reranker behavior;
- replace human review.

## Next Stages

The intended next slices are:

- report-only candidate package batch generation from this pilot input;
- batch exam and ranking for unreviewed package candidates;
- human review capture with keep/revise/reject decisions;
- repair-plan generation from human notes and exam deltas.
