# Control Discipline Ideal Candidate Batch Exam Diagnostic V1

## Purpose

`control_discipline_ideal_candidate_batch_exam_diagnostic_v1` is a
deterministic report-only diagnostic over one
`control_discipline_ideal_candidate_batch_exam_v1` snapshot.

It improves the exam layer by explaining the existing advisory ranking,
surfacing failure-mode probes, comparing same-ideal and preservation-set
candidates, and preparing concrete human-review questions.

## Scope

The V1 diagnostic consumes:

- one candidate batch exam snapshot;
- ranked candidates;
- recommended human review order;
- per-candidate risk summaries;
- next automation focus.

It outputs:

- ranking explanations for every candidate;
- per-candidate failure-mode probes;
- advisory pairwise comparisons;
- human-review question sets;
- ranking uncertainty notes;
- next exam improvement notes;
- explicit report-only boundary assertions.

## Output Shape

Required top-level fields:

- `contract_version`: must be
  `control_discipline_ideal_candidate_batch_exam_diagnostic_v1`
- `evaluation_mode`: must be `report_only`
- `authority_boundary`: must be `advisory_context_only`
- `diagnostic_scope`
- `diagnostic_id`
- `source_exam_ref`
- `source_exam_contract_version`
- `source_exam_id`
- `source_batch_id`
- `source_pilot_id`
- `discipline_id`
- `candidate_count`
- `diagnostic_summary`
- `ranking_explanations`
- `failure_mode_probes`
- `pairwise_comparisons`
- `human_review_question_sets`
- `ranking_uncertainty`
- `next_exam_improvement_notes`
- `source_exam_readouts`
- `boundary_assertions`

## Diagnostic Dimensions

V1 names these failure-mode probes for each candidate:

- `second_career_drift`
- `generic_goodstuff_drift`
- `complexity_budget`
- `package_completeness`
- `discipline_fit`
- `ideal_temperament_fit`

Human-review questions always include required prompts for discipline fit,
ideal temperament fit, the candidate's primary risk, and next-round
instruction. Package completeness is included as an optional review prompt
when it is not already the primary risk.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.source_exam_consumed = true`
- `boundary_assertions.diagnostic_created = true`
- `boundary_assertions.ranking_is_authoritative = false`
- `boundary_assertions.diagnostic_is_authoritative = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.candidate_promoted = false`
- `boundary_assertions.candidate_rejected = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.runtime_readiness_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

V1 does not:

- change the candidate batch exam ranking;
- change rubric dimensions or scorecard weights;
- treat pairwise comparisons as authority;
- generate formal card text;
- write runtime card data;
- promote or reject candidates;
- create hard gates;
- claim reviewed evidence;
- enable default synthesis;
- enable learned or reranker behavior.

## Entrypoint

Generate the current diagnostic scaffold:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_diagnostic.py --exam tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_exam_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_candidate_batch_exam_diagnostic_current
```

Validate the fixture:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_diagnostic.py --input tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_diagnostic_v1 --json
```

Write an empty template:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_diagnostic.py --write-template tmp/combat_analysis/control_discipline_ideal_candidate_batch_exam_diagnostic_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_candidate_batch_exam_diagnostic_v1.py tests/scripts/test_run_control_discipline_ideal_candidate_batch_exam_diagnostic.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_diagnostic_v1/`

The current sample keeps `white_order_fail_state_candidate_v1` as the top
ranked candidate from the source exam, reports low rank-order confidence because
multiple adjacent candidates have close scores, and provides six advisory
pairwise comparisons:

- three same-ideal comparisons from the source exam focus set;
- three preservation-set comparisons across the next-automation candidates.

## Intended Follow-Up

This diagnostic should feed two later improvements:

- a better human-review packet that asks sharper candidate-specific questions;
- a future exam improvement slice that adds evidence snippet slots without
  changing V1 scorecard weights.

All outputs remain advisory context. Human review still owns keep, revise,
reject, next-round instruction, formal-card wording, runtime promotion, and
evidence promotion.
