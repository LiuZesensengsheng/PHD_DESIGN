# Control Discipline Ideal Candidate Batch Exam V1

## Purpose

`control_discipline_ideal_candidate_batch_exam_v1` is a deterministic
report-only advisory ranking over one
`control_discipline_ideal_candidate_batch_v1` snapshot.

It helps decide which generated control-discipline plus ideal-temperament
candidates deserve later human review, which candidates are useful risk probes,
and which candidate sets should be preserved for the next automated comparison
when humans are not immediately available.

## Scope

The V1 exam:

- consumes exactly one generated candidate batch snapshot;
- preserves the batch as source material and does not modify the producer;
- ranks candidates with a deterministic rubric;
- reports per-ideal winners, second-career risk, complexity risk, package role
  completeness, generic-goodstuff drift, and next automation focus;
- stays report-only and advisory.

## Output Shape

Required top-level fields:

- `contract_version`: must be `control_discipline_ideal_candidate_batch_exam_v1`
- `evaluation_mode`: must be `report_only`
- `authority_boundary`: must be `advisory_context_only`
- `exam_scope`
- `exam_id`
- `source_candidate_batch_ref`
- `source_candidate_batch_contract_version`
- `source_batch_id`
- `source_pilot_id`
- `discipline_id`
- `candidate_count`
- `rubric_summary`
- `per_candidate_results`
- `ranked_candidates`
- `per_ideal_winners`
- `second_career_risk_summary`
- `complexity_risk_summary`
- `package_completeness_summary`
- `generic_goodstuff_drift_summary`
- `failure_families`
- `recommended_human_review_order`
- `next_automation_focus`
- `boundary_assertions`

## Rubric

The V1 rubric is deterministic and uses higher-is-better scores:

- `discipline_loop_fit`
- `ideal_temperament_fit`
- `second_career_risk_inverse`
- `complexity_budget_fit`
- `package_role_completeness`
- `review_readiness`
- `generic_goodstuff_drift_inverse`

Risk inverse dimensions lower a candidate's advisory score when source notes
suggest ideal-as-second-career drift, complexity-budget pressure, or generic
goodstuff/value drift. These are advisory signals only.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.ranking_is_authoritative = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`
- `boundary_assertions.scorecard_weights_changed = false`

V1 does not:

- generate formal card text;
- write runtime card data;
- promote candidates;
- create hard gates;
- claim reviewed evidence;
- enable default synthesis;
- enable learned or reranker behavior;
- change existing scorecard weights.

## Entrypoint

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam.py --input tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_candidate_batch_exam_current
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_candidate_batch_exam_v1.py tests/scripts/test_run_control_discipline_ideal_candidate_batch_exam.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_v1/`

The current sample ranks the six generated candidates from Agent 1's sample
batch, reports per-ideal winners for `white_order`, `blue_truth`, and
`green_depth`, and identifies:

- highest second-career risk: `green_depth_recovery_candidate_v1`;
- highest complexity risk: `blue_truth_delayed_precision_candidate_v1`;
- highest generic-goodstuff drift: `white_order_audit_control_candidate_v1`;
- next automation preservation set:
  `white_order_fail_state_candidate_v1`,
  `blue_truth_forecast_candidate_v1`, and
  `green_depth_compound_stability_candidate_v1`.

## Intended Follow-Up

The exam is meant to answer:

- which candidates are most worth human review;
- which candidates most risk turning ideal into a second career;
- which candidates need complexity-budget review first;
- whether package role coverage is complete enough for later comparison;
- which candidates may be generic goodstuff rather than control-owned ideal
  texture;
- which candidates automation should preserve or compare while waiting for
  humans.

All answers are advisory context. Human review still owns keep, revise, reject,
formal-card wording, runtime promotion, and any evidence promotion.
