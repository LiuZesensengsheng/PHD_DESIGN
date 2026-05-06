# Cardanalysis Evidence Quality Audit V1

- Tool: `cardanalysis_evidence_quality_audit_v1`
- Status: report-only evidence asset audit
- Runtime impact: none
- Graph registration: none by default
- Report-only registry registration: none by default

## Purpose

This audit turns the existing normalized advisory evidence library into a more
manageable planning asset.

It does not decide whether a case is correct, balanced, viable, or ready for
promotion. Human review is temporarily unavailable, so the audit only inventories
machine-detectable quality risks and prepares later review-packet queues.

## Scope

In scope:

- normalized `cardanalysis_case_input_v1` fixture directories;
- duplicate and near-duplicate case-id/title/primary-axis risks;
- source tier and review-status distributions;
- authority-boundary and forbidden-use completeness;
- allowed-consumer scope risks;
- foundation-axis and mechanism-family coverage weakness;
- review-packet candidate queues for later human review.

Out of scope:

- runtime, UI/save, formal card data, or formal enemy data changes;
- capability graph registry or report-only registry changes;
- hard gates, default synthesis, learned behavior, or reranker behavior;
- automatic promotion from `human_curated`, `source_mined`, or `speculative`
  evidence into `reviewed`;
- asking a human to judge case correctness during this audit lane.

## Entrypoint

```bash
python scripts/run_cardanalysis_evidence_quality_audit.py \
  --input tests/fixtures/combat_analysis/source_followup_case_library_v1 \
  --input tests/fixtures/combat_analysis/mechanism_case_library_v1 \
  --output-dir tmp/combat_analysis/evidence_quality_audit_current
```

The CLI writes:

- `evidence_quality_audit.md`
- `snapshot.json`
- `manifest.json`

## Output Contract

The snapshot keeps:

```text
schema_version = cardanalysis_evidence_quality_audit_v1
evaluation_mode = report_only
authority_boundary = advisory_context_only
hard_gate_impact = none
```

Required sections:

- `scanned_inputs`
- `source_type_distribution`
- `source_tier_distribution`
- `review_status_distribution`
- `duplicate_and_near_duplicate_risks`
- `authority_boundary_audit`
- `allowed_consumers_audit`
- `foundation_axis_coverage`
- `foundation_axis_weak_coverage`
- `mechanism_family_coverage`
- `mechanism_family_weak_coverage`
- `review_packet_candidate_queue`
- `advisory_only_stopline`
- `boundary_assertions`

## Current Machine-Detectable Findings

The first scan over:

- `tests/fixtures/combat_analysis/source_followup_case_library_v1`
- `tests/fixtures/combat_analysis/mechanism_case_library_v1`

reported:

- `686` normalized cases total.
- Source tiers:
  - `reviewed`: `68`
  - `human_curated`: `594`
  - `source_mined`: `12`
  - `speculative`: `12`
- Review statuses:
  - `accepted`: `68`
  - `review_needed`: `550`
  - `source_aligned`: `44`
  - `draft`: `12`
  - `needs_review`: `12`
- Exact duplicate case IDs: `0`.
- Near-duplicate case-id stems: present, mostly paired followup lanes that should
  stay packet-reviewable instead of being silently merged.
- Primary-axis reuse risks:
  - `curse_pollution`
  - `stance_mode_switch`
- Authority-boundary drift: `0` cases outside `advisory_context_only`.
- Core forbidden-use drift: `0` cases missing the core stop lines
  `hard_gate_promotion` and `default_synthesis_path`.
- Non-reviewed reviewed-claim drift: `0` below-reviewed cases missing
  `reviewed_evidence_claim`.
- Allowed-consumer unknowns: `0` after including existing report-only consumers.
- Broad consumer-scope risks: present; these are planning risks, not failures.
- Foundation-axis weak coverage:
  - `retain`: `thin_reviewed`
  - `filter`: `thin_reviewed`
  - `scaling`: `advisory_only`
- Mechanism-family weak coverage includes several source-followup-heavy families
  that are still mostly below-reviewed, such as `chain_fatigue`,
  `energy_instability`, `search_public_target`, `status_decay_transfer`, and
  `temporary_generation_memory`.

## Review-Packet Queue Meaning

The audit queue lists cases that look structurally ready for future packet review.
It prioritizes below-reviewed cases that:

1. already carry review-packet or witness-set readiness markers;
2. have setup, payoff, failure-mode, and counterplay fields filled;
3. touch weak foundation axes or mechanism families;
4. preserve the `reviewed_evidence_claim` stopline.

Queue membership is not promotion. It means only:

```text
requires_explicit_human_review_decision_before_any_reviewed_claim
```

## Advisory-Only Stopline

This audit may:

- prioritize future review packets;
- identify evidence-quality cleanup slices;
- help planners decide which existing evidence needs better packaging.

This audit must not:

- auto-promote evidence tiers;
- decide legality, viability, hard-gate results, or synthesis defaults;
- change runtime, formal data, UI/save, capability graph registry, or
  report-only registry;
- enable learned or reranker behavior;
- ask a human to judge case correctness as part of the audit run itself.

## Validation

Focused validation:

```bash
py -3.11 -m pytest tests/toolkit/combat_analysis/test_evidence_quality_audit_v1.py tests/scripts/test_run_cardanalysis_evidence_quality_audit.py -q
```

Full lane validation should also run both normalized case validators plus the
standard architecture, encoding, capability-graph, and diff checks.
