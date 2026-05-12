# Control Discipline Ideal Candidate Batch V1

## Purpose

`control_discipline_ideal_candidate_batch_v1` is a deterministic report-only
candidate-generation surface.

It consumes one validated `control_discipline_ideal_pilot_v1` input and writes
multiple unreviewed candidate package proposal skeletons for each ideal
temperament profile in the pilot. The output exists for later batch exam,
automatic filtering, and human review. It does not create formal cards.

## Scope

The V1 batch:

- consumes exactly one ready pilot;
- keeps the discipline as the combat-loop owner;
- generates at least two candidates for each current ideal:
  - `white_order`
  - `blue_truth`
  - `green_depth`
- emits report-only candidate skeletons plus embedded
  `card_package_proposal_v1` package skeletons;
- stays deterministic and does not call an LLM or external API.

## Output Shape

Required top-level fields:

- `contract_version`: must be `control_discipline_ideal_candidate_batch_v1`
- `evaluation_mode`: must be `report_only`
- `authority_boundary`: must be `advisory_context_only`
- `batch_scope`
- `batch_id`
- `source_input_ref`
- `pilot_ref`
- `source_pilot_id`
- `source_pilot_title`
- `discipline_id`
- `candidate_count`
- `discipline_profile_summary`
- `ideal_profile_refs`
- `manifest_candidates`
- `per_ideal_summary`
- `generated_candidates`
- `boundary_assertions`

Every generated candidate must include:

- `candidate_id`
- `ideal_id`
- `candidate_status = generated_unreviewed_report_only`
- `intended_difference`
- `discipline_fit_rationale`
- `ideal_temperament_rationale`
- `second_career_risk_notes`
- `complexity_budget_notes`
- `package_roles`
- `package_proposal_ref`
- embedded `package_proposal`

The embedded `package_proposal` must stay inside
`card_package_proposal_v1` boundaries:

- `source_type = generated_hypothesis`
- `evidence_tier = speculative`
- `review_status = hypothesis_draft`
- no formal card text
- no runtime card data
- no reviewed-evidence claim

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

V1 does not:

- write runtime card data;
- generate formal card text;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable synthesis by default;
- enable learned or reranker behavior;
- change scorecard weights.

## Design Rule

The batch is allowed to widen package hypotheses, but it must not widen the
combat owner.

That means:

- discipline still owns moment-to-moment control play;
- ideal still owns temperament, reward bias, and review texture;
- ideal must not become a second career, hidden score, or recurring per-turn
  obligation.

## Entrypoint

```powershell
python scripts/run_control_discipline_ideal_candidate_batch.py --input tests/fixtures/combat_analysis/control_discipline_ideal_pilot_v1/control_discipline_ideal_pilot_sample_v1.json --output-dir tmp/combat_analysis/control_discipline_ideal_candidate_batch_current
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_candidate_batch_v1.py tests/scripts/test_run_control_discipline_ideal_candidate_batch.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_v1/`

It contains:

- 6 generated unreviewed candidate skeletons;
- 2 candidates each for `white_order`, `blue_truth`, and `green_depth`;
- embedded `card_package_proposal_v1` skeletons with no formal card fields;
- second-career and complexity-budget review notes for each candidate.

## Intended Follow-Up

The batch is meant to answer:

- what directions exist for each ideal?
- how does each direction still belong to control discipline?
- where might the ideal become a second career?
- which candidates look strongest for later exam or human review?

Those are advisory answers only. Final review still belongs to later automated
checks and humans.
