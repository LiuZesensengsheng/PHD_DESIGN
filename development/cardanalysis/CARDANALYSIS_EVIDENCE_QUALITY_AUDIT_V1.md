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
- `duplicate_axis_risk_clusters`
- `authority_boundary_audit`
- `allowed_consumers_audit`
- `allowed_consumer_scope_notes`
- `foundation_axis_coverage`
- `foundation_axis_weak_coverage`
- `foundation_axis_review_packet_backlog`
- `mechanism_family_coverage`
- `mechanism_family_weak_coverage`
- `mechanism_family_review_packet_backlog`
- `review_packet_candidate_queue`
- `planning_summary`
- `risk_severity_summary`
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

## Planning Summary

The audit also emits `planning_summary` so a later agent can choose the next
slice without rereading every risk list. It groups machine-detectable risks into
plain planning actions such as:

- cluster near-duplicate case-id stems before packaging a later review backlog;
- separate intentional primary-axis density from possible axis drift;
- prioritize weak foundation-axis coverage such as `retain`, `filter`, or
  `scaling`;
- summarize broad allowed-consumer scope before reusing cases across report-only
  heads.

The summary is still advisory only. Its recommended slices may update audit
output, documentation, or focused tests, but they carry the same forbidden-change
list as the main audit stopline.

## Duplicate And Axis Risk Clusters

`duplicate_axis_risk_clusters` is a compact view over the duplicate and axis-reuse
details. It exists so later agents can plan review-packet backlogs from groups
instead of rereading every case row.

Cluster types:

- `exact_duplicate_case_id`: high-priority identifier collision; fix metadata
  before packaging.
- `near_duplicate_case_id_stem`: related followup or possible duplication that
  should be clustered before review-packet planning.
- `primary_axis_reuse`: repeated `primary_axis` values that may be intentional
  coverage density or possible axis drift.

Every cluster keeps:

```text
authority_boundary = advisory_context_only
promotion_action = no_reviewed_promotion
```

Cluster membership is not a correctness claim and does not request immediate
human review.

## Foundation Axis Review-Packet Backlog

`foundation_axis_review_packet_backlog` groups weak foundation axes into later
packet-planning rows. The current intent is to make thin or advisory-only axes
easier to plan without opening a human-review request during the audit itself.

Each item records:

- axis id and coverage status;
- reviewed, human-curated, and lower-tier case counts;
- candidate case IDs from the review-packet queue or coverage matches;
- a suggested packet-planning action;
- `promotion_action = no_reviewed_promotion`;
- `human_review_request = not_requested_by_this_audit`.

For the current fixture scan, the backlog focuses on `retain`, `filter`, and
`scaling`. This list is a planning inventory, not a claim that those cases are
correct or ready for reviewed promotion.

## Mechanism Family Review-Packet Backlog

`mechanism_family_review_packet_backlog` applies the same planning shape to weak
mechanism-family coverage. It groups below-reviewed or thin-reviewed family
targets into later packet-planning rows, with candidate case IDs drawn from the
review-packet queue where possible.

The current scan reports weak-family backlog rows for families such as
`chain_fatigue`, `energy_instability`, `search_public_target`,
`status_decay_transfer`, `draw_heat`, `pollution_market`, and
`redirect_collision`.

Every row keeps:

```text
authority_boundary = advisory_context_only
promotion_action = no_reviewed_promotion
human_review_request = not_requested_by_this_audit
```

## Allowed Consumer Scope Notes

`allowed_consumer_scope_notes` summarizes broad consumer scope by consumer/head.
It is meant to prevent accidental authority broadening when a case is allowed
for many report-only consumers.

The current scan reports `64` broad-scope cases and `9` consumer notes. Broad
scope is not automatically wrong: heads such as
`cardanalysis_feature_projection_v1` and
`evaluation_autonomous_design_model_v1` are expected to read many cases. The
audit records this as planning context so future agents do not mistake broad
read access for promotion authority.

## Severity Summary

`risk_severity_summary` rolls the planning risks into a compact merge-readiness
view. It is still report-only and explicitly not a gate.

The current scan has:

- high: `0`
- medium: `5`
- low: `1`
- merge readiness:
  `mergeable_report_only_no_high_severity_drift_detected`

This means the audit lane is mergeable as report-only tooling, while the medium
risks remain useful follow-up planning items.

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
