# Control Discipline Ideal Candidate Batch Exam Evidence V1

## Purpose

`control_discipline_ideal_candidate_batch_exam_evidence_v1` is a deterministic
report-only evidence/snippet index over one
`control_discipline_ideal_candidate_batch_v1` snapshot and its matching
`control_discipline_ideal_candidate_batch_exam_v1` snapshot.

It improves the exam layer by making the current advisory scores, risk labels,
and diagnostic context easier to audit. It records source field paths, short
snippets, trigger terms, missing/weak evidence flags, and downstream reuse
limits without changing the exam ranking or scorecard.

## Scope

The V1 evidence layer consumes:

- one candidate batch snapshot;
- one matching candidate batch exam snapshot;
- ranked candidates and per-candidate exam results;
- source candidate text fields such as rationale, risk notes, package roles,
  known risks, known limits, review focus, and exam dimension notes.

It outputs:

- per-candidate and per-rubric-dimension evidence snippets;
- risk-label trigger fields for second-career drift, complexity budget, and
  generic-goodstuff drift;
- trigger terms or short phrases found in the source text;
- source field paths for every snippet;
- missing/weak evidence flags;
- evidence strength and readiness summary;
- allowed downstream reuse for diagnostic and human-review packets;
- explicit report-only boundary assertions.

## Output Shape

Required top-level fields:

- `contract_version`: must be
  `control_discipline_ideal_candidate_batch_exam_evidence_v1`
- `evaluation_mode`: must be `report_only`
- `authority_boundary`: must be `advisory_context_only`
- `evidence_scope`
- `evidence_id`
- `source_candidate_batch_ref`
- `source_exam_ref`
- `source_candidate_batch_contract_version`
- `source_exam_contract_version`
- `source_batch_id`
- `source_exam_id`
- `source_pilot_id`
- `discipline_id`
- `candidate_count`
- `rubric_dimensions`
- `evidence_summary`
- `per_candidate_evidence`
- `risk_label_trigger_summary`
- `missing_weak_evidence_flags`
- `evidence_strength_readiness_summary`
- `allowed_downstream_reuse`
- `boundary_assertions`

## Evidence Semantics

V1 assigns an evidence-strength label per candidate and rubric dimension:

- `strong`: multiple source snippets with useful trigger terms;
- `moderate`: usable source snippets but less redundant signal;
- `weak`: source snippets exist but trigger coverage is thin;
- `missing`: no usable source snippet was found.

These labels are audit-readiness labels only. They do not change exam scores,
risk labels, ranked order, human-review order, candidate status, or any later
repair/draft readiness field.

## Boundary

V1 must keep:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.source_candidate_batch_consumed = true`
- `boundary_assertions.source_exam_consumed = true`
- `boundary_assertions.evidence_index_created = true`
- `boundary_assertions.evidence_is_authoritative = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.risk_labels_changed = false`
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
- treat snippets as reviewed or accepted evidence;
- promote or reject candidates;
- create runtime readiness or hard gates;
- generate formal card text;
- write runtime card data;
- call an LLM or external API;
- enable default synthesis, learned behavior, or reranker behavior.

## Entrypoint

Generate the current evidence index:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_evidence.py --batch tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_snapshot.json --exam tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_v1/control_discipline_ideal_pilot_sample_v1_candidate_batch_v1_exam_v1_snapshot.json --output-dir tmp/combat_analysis/control_discipline_ideal_candidate_batch_exam_evidence_current
```

Validate the fixture:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_evidence.py --input tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_evidence_v1 --json
```

Write an empty template:

```powershell
python scripts/run_control_discipline_ideal_candidate_batch_exam_evidence.py --write-template tmp/combat_analysis/control_discipline_ideal_candidate_batch_exam_evidence_template.json
```

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_discipline_ideal_candidate_batch_exam_evidence_v1.py tests/scripts/test_run_control_discipline_ideal_candidate_batch_exam_evidence.py -q
```

## V1 Fixture

The first fixture output lives under:

`tests/fixtures/combat_analysis/control_discipline_ideal_candidate_batch_exam_evidence_v1/`

The current sample indexes all six control-discipline plus ideal candidates.
It preserves the source exam ranking and risk labels, identifies
`green_depth_recovery_candidate_v1` as the highest second-career risk source
label, `blue_truth_delayed_precision_candidate_v1` as the highest complexity
risk source label, and `white_order_audit_control_candidate_v1` as the highest
generic-goodstuff drift source label.

The sample also records one weak evidence flag:

- `white_order_fail_state_candidate_v1` has weak complexity-budget evidence
  because source snippets exist but do not strongly trigger the V1 complexity
  phrase set.

## Intended Follow-Up

This evidence layer is meant to feed:

- sharper exam diagnostics that can cite source paths instead of only summary
  readouts;
- a better human-review packet that shows which fields caused risk labels and
  which dimensions need stronger source evidence.

All reuse remains advisory context. Human review still owns keep, revise,
reject, next-round instruction, formal-card wording, runtime promotion, and
any evidence promotion.
