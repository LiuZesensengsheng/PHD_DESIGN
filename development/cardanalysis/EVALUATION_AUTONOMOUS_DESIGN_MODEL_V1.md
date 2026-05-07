# Evaluation Autonomous Design Model V1

## Purpose

`evaluation_autonomous_design_model_v1` is a report-only orchestration surface for
turning a mechanism candidate, parameter target, package skeleton, and existing
cardanalysis evidence summaries into a human-review design brief.

It answers:

- whether the role-level package skeleton is ready for report-only review
- which evidence sections are present or missing
- which rejection or revision reason should be named first
- how strongly the brief is allowed to speak without false confidence
- which canonical report should be requested next

It does not decide whether a card is legal, balanced, fun, healthy, or recommended by
default.

## Scope Boundary

In scope:

- report-only orchestration over existing summary payloads
- `mechanism_candidate`, `parameter_search_space`, `package_skeleton`, and
  `design_candidate_brief` input contracts
- package-skeleton readiness wording for anchor, support, glue, payoff, and safety
  valve roles
- evidence gap and conflict notes across canonical report-only summaries
- advisory `reject`, `revise`, or `promote_to_human_review_queue` wording

Out of scope:

- generating formal cards
- changing legality, schema, hard gates, or default recommendation paths
- replacing canonical report-only owners for fun/health, compression, package health,
  design iteration, mechanism-axis discovery, or evidence bundles
- importing `design_studio` from `design_engine`
- enabling learned ranking, reranking, or autonomous promotion
- claiming project temperament fit

## Canonical Owners

This module consumes summary-shaped evidence from registered surfaces:

| Evidence | Canonical owner |
| --- | --- |
| `mechanism_axis_discovery_summary` | `mechanism_axis_discovery_v1` |
| `mechanism_fun_health_summary` | `mechanism_fun_health_v1` |
| `card_package_health_summary` | `card_package_health_v1` |
| `deck_compression_summary` | `deck_compression_report_v1` |
| `design_iteration_summary` | `design_iteration_brief_v1` |
| evidence bundle root | `cardanalysis_evidence_bundle_v1` |

The autonomous design model may explain how those summaries interact, but it must not
re-score or override them.

## Input Contract

Required input sections:

- `mechanism_candidate`: mechanism axis, fantasy, and known foundation dependencies
- `parameter_search_space`: one current target parameter and optional companion
  parameter
- `package_skeleton`: role-level anchor, support, glue, payoff, and safety valve

Optional input sections:

- `design_candidate_brief`: existing human-readable intent or forbidden claims
- `evidence_bundle`: report-only summaries and supplied evidence conflicts
- top-level canonical summary sections, which are folded into the evidence bundle

The module accepts only role-level design material. Final card names, costs, exact
numbers, and rules text belong outside this surface.

## Output Contract

The snapshot contains:

- `generated_design_candidate_brief`
- `package_skeleton_review`
- `evidence_review`
- `parameter_review`
- `advisory_review`
- `boundary_assertions`

Required flags:

- `contract_version=evaluation_autonomous_design_model_v1`
- `evaluation_mode=report_only`
- `review_required=true`

Forbidden output keys and claims:

- `formal_card`
- `hard_gate`
- `default_rank_override`
- `learned_promotion`

## Package Skeleton Readiness

Role checklist:

| Role | Requirement |
| --- | --- |
| `anchor` | visible mechanism state before payoff |
| `support` | setup-window output or survival tied to the mechanism |
| `glue` | timing, hold, bridge, filter, or state-management decision |
| `payoff` | downstream conversion, not the only identity proof |
| `safety_valve` | recoverable miss tied to the mechanism |

Readiness labels are advisory:

- `skeleton_ready_for_review`
- `skeleton_partial`
- `skeleton_payoff_only`
- `skeleton_goodstuff_blur`
- `skeleton_fail_state_gap`
- `skeleton_reachability_unknown`

These are wording labels, not hard gates.

## Evidence Wording

Expected report sections:

- `mechanism_axis_discovery_summary`
- `mechanism_fun_health_summary`
- `card_package_health_summary`
- `deck_compression_summary`
- `design_iteration_summary`

Allowed wording ladder:

| Evidence state | Strongest wording |
| --- | --- |
| No report sections | `review_only_candidate` |
| Partial or broken skeleton | `revise_package_skeleton` |
| Skeleton ready, fun/health missing | `package_ready_for_fun_health_review` |
| Skeleton ready, compression missing | `package_ready_but_reachability_unknown` |
| Reports present and one primary risk remains | `revise_one_parameter_or_role` |
| Reports present, risks named, no false confidence | `promote_to_human_review_queue` |

`promote_to_human_review_queue` does not mean default recommendation, card generation,
learned promotion, or hard-gate pass.

## Rejection Reasons

The V1 advisory reasons are:

- `swallowed_by_draw`
- `swallowed_by_energy`
- `swallowed_by_discard`
- `removal_dependency_too_high`
- `payoff_only`
- `generic_goodstuff`
- `low_agency_loop`
- `matchup_too_narrow`
- `setup_tax_too_high`
- `fail_state_missing`

Each reason maps to one first revision action in the implementation. A future change
may expand the vocabulary only with reviewed fixtures and tests.

## Initial Parameter Coverage

The implementation includes reviewed-style fixture coverage for:

- `charge_turns`
- `discard_outlet_count`

The first `charge_turns` comparison is band-based: `short_to_medium` with
`fail_state_floor` as the companion parameter.

The first `discard_outlet_count` transfer checks whether discard is an identity,
cost, trigger, resource, or release choice rather than generic hand cleanup.

## Validation

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_evaluation_autonomous_design_model_v1.py tests/scripts/test_run_evaluation_autonomous_design_model.py -q
```

Registry and boundary validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
```

Mechanism-axis discovery remains an upstream evidence owner and should still be run
when this surface consumes discovery summaries.
