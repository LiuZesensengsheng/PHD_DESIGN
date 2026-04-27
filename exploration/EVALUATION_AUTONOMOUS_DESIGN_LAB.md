# Evaluation Autonomous Design Model Lab

- Lab direction: `Evaluation & Autonomous Design Model Lab`
- Current model id: `evaluation_autonomous_design_model_v1`
- Current posture: docs-only, report-only, human-review-required
- First slice date: `2026-04-27`

## Purpose

This lab defines a report-only model for judging whether a candidate mechanism and its
package skeleton are likely to become fun, healthy, coherent design material.

The model is intended to answer these questions before any formal card generation:

- Is the mechanism likely to create good player-facing play?
- Is the card package taking shape as a package instead of goodstuff or payoff-only?
- Does the plan depend on deck removal, compression, or starter cleanup before it can
  honestly be called reachable?
- Which parameter should be searched first when turning a mechanism axis into a package
  skeleton and design brief?

## Strict Boundary

This lab must not:

- create a duplicate V1 evaluator for an already registered report-only surface
- upgrade report-only output into a hard gate
- change the default recommendation path
- enable learned ranking, reranking, or autonomous promotion
- generate formal cards directly
- treat `promote` as anything stronger than "send to human-reviewed next-step queue"

Current canonical report-only owners remain the source of truth:

| Surface | Canonical owner |
| --- | --- |
| `deck_compression_report_v1` | `tools/combat_analysis/design_engine/deck_compression_report.py` |
| `mechanism_fun_health_v1` | `tools/combat_analysis/design_studio/mechanism_fun_health_benchmark.py` |
| `card_package_health_v1` | `tools/combat_analysis/design_studio/card_package_health.py` |
| `design_iteration_brief_v1` | `tools/combat_analysis/design_engine/design_iteration_brief.py` |
| `mechanism_axis_discovery_v1` | `tools/combat_analysis/design_engine/mechanism_axis_discovery.py` |
| `cardanalysis_evidence_bundle_v1` | `tools/combat_analysis/design_engine/cardanalysis_evidence_bundle.py` |

This lab can define an orchestration vocabulary around those surfaces, but it should
not own their scoring, gate semantics, fixture schema, or CLI behavior.

## Current Minimal Question

How can a mechanism-axis candidate become a report-only `package_skeleton` and
`design_candidate_brief` without becoming a card generator or hard gate?

The first useful answer is a small entity graph, a shared dimension vocabulary, one
parameter-search example, and explicit rejection reasons.

## Model Envelope

`evaluation_autonomous_design_model_v1` is a report-only aggregation contract:

```yaml
evaluation_autonomous_design_model_v1:
  evaluation_mode: report_only
  authority: advisory
  promotion_authority: human_review_required
  inputs:
    - mechanism_candidate
    - evidence_bundle
    - parameter_search_space
  intermediate_outputs:
    - package_skeleton
    - design_candidate_brief
  review_outputs:
    - fun_health_report
    - deck_compression_report
    - package_health_report
    - design_iteration_brief
    - rejection_reason
  forbidden_outputs:
    - formal_card
    - hard_gate
    - default_rank_override
    - learned_promotion
```

## Entity Vocabulary

| Entity | Role in this lab | Notes |
| --- | --- | --- |
| `mechanism_candidate` | A proposed mechanism axis before card generation. | Usually comes from mechanism-axis discovery, source mining, or human design intent. |
| `fun_health_report` | Report-only read on agency, payoff texture, setup tax, fail states, variance, combo aspiration, degeneracy, and matchup elasticity. | Consolidates into the existing `mechanism_fun_health_v1` surface. |
| `deck_compression_report` | Report-only read on removal, compression, starter pollution, and route dependency. | Consolidates into `deck_compression_report_v1`. |
| `package_health_report` | Report-only read on package density, slots, anchors, glue, payoff timing, and anti-soup behavior. | Consolidates into `card_package_health_v1`. |
| `design_iteration_brief` | Report-only summary of what to reject, revise, or inspect next. | Uses existing `design_iteration_brief_v1` vocabulary. |
| `evidence_bundle` | Portable evidence container that keeps source reports inspectable. | Uses `cardanalysis_evidence_bundle_v1` as the canonical bundle surface. |
| `parameter_search_space` | Bounded set of parameters worth probing before designing a package skeleton. | Must stay parameter-level, not formal-card-level. |
| `package_skeleton` | Role-level package outline: anchor, support, glue, payoff, safety valve. | This is not a card list and not a generated card set. |
| `design_candidate_brief` | Human-readable design brief for review, including target parameter and known risks. | May describe card jobs, never final card text. |
| `rejection_reason` | Normalized reason to reject or revise a candidate before further design. | Advisory only; no hard pass/fail authority. |

## Evaluation Dimensions

The lab normalizes dimensions from the existing report-only specs. These names are the
shared vocabulary for briefs and working logs.

| Dimension | Primary question |
| --- | --- |
| `agency` | Does the mechanism create meaningful play choices rather than an automatic line? |
| `payoff_texture` | Does the payoff create varied, legible, earned outcomes instead of one flat number? |
| `setup_tax` | How much must the player pay before the mechanism starts contributing? |
| `fail_state_value` | When the line misses, does the package still produce block, draw, scaling, partial progress, or readable recovery? |
| `variance_pressure` | Does the plan need lucky draw/order/enemy behavior, or can the player shape the variance? |
| `combo_aspiration` | Is the dream state legible, exciting, and worth chasing? |
| `degeneracy_pressure` | Does the plan risk becoming low-cost, low-choice, low-constraint, and environment-flattening? |
| `matchup_elasticity` | Can the mechanism adapt across fast, scaling, multi-enemy, action-punisher, and defensive pressure? |
| `deck_compression_requirement` | How much thinning or effective thinning is needed before the online claim is credible? |
| `removal_access_dependency` | Does the plan depend on route-specific out-of-combat removal? |
| `starter_pollution_tolerance` | How many starter/basic or off-axis cards can remain before the plan breaks down? |
| `package_density` | Is there enough on-axis density for the package to show up through ordinary draws? |
| `support_payoff_balance` | Are support, bridge, and stabilizer jobs present before payoff greed? |
| `glue_quality` | Do bridge/glue pieces connect setup to payoff instead of merely sharing broad tags? |
| `anchor_clarity` | Is the primary anchor readable, and is secondary-anchor uncertainty preserved? |
| `goodstuff_risk` | Is generic value doing the real work instead of the named mechanism? |
| `payoff_only_risk` | Is an exciting payoff present without enough setup, bridge, density, or fail-state support? |

## Autonomous Design Flow

The lab uses this report-only flow:

1. `choose mechanism axis`
   - Select one `mechanism_candidate` from discovery, source mining, or human intent.
   - Record why this is the smallest current question.
2. `identify foundation dependencies`
   - Name dependencies such as draw, energy, discard, removal, compression, retain,
     filter, defense, damage, scaling, or exhaust.
   - Mark whether any foundation axis may swallow the candidate identity.
3. `choose parameter target`
   - Pick one parameter from `parameter_search_space`.
   - Avoid searching many knobs in one iteration.
4. `build anchor/support/glue/payoff/safety valve`
   - Produce a `package_skeleton` with roles only.
   - Do not write final card names, costs, numbers, or text.
5. `design brief`
   - Write a `design_candidate_brief` that states the axis, target parameter, role
     skeleton, expected texture, and known rejection risks.
6. `report-only evaluation`
   - Attach or request `fun_health_report`, `deck_compression_report`,
     `package_health_report`, `design_iteration_brief`, and `evidence_bundle` reads.
   - These reports explain, not decide.
7. `reject/revise/promote`
   - `reject`: stop the candidate for a named `rejection_reason`.
   - `revise`: keep the axis but adjust one parameter or skeleton role.
   - `promote`: send the brief to human review or a future reviewed fixture task.

## Parameter Search Space

The first model version recognizes these parameter examples as useful knobs:

| Parameter | First question | Common failure signal |
| --- | --- | --- |
| `charge_turns` | How many turns should delayed setup take before release is satisfying but not dead? | `setup_tax_too_high`, `fail_state_missing` |
| `trigger_density` | How many triggers are needed before the axis appears through normal draw? | `payoff_only`, `variance_pressure` |
| `star_gain_rate` | How fast should a threshold resource grow before the release becomes automatic? | `low_agency_loop`, `generic_goodstuff` |
| `discard_outlet_count` | How many outlets are needed before discard becomes identity rather than hand cleanup? | `swallowed_by_discard`, `payoff_only` |
| `removal_dependency` | How much external removal is being assumed for the package to function? | `removal_dependency_too_high` |
| `payoff_cost_ceiling` | How expensive can the payoff be before it competes with assembly? | `setup_tax_too_high`, `payoff_only` |
| `setup_turns` | What is the first functional turn under realistic draw pressure? | `setup_tax_too_high` |
| `fail_state_floor` | What useful output remains when the payoff misses? | `fail_state_missing` |
| `compression_requirement` | How thin must the deck be before the mechanism is reliable? | `removal_dependency_too_high`, `swallowed_by_draw` |
| `enemy_pressure_tolerance` | Which common pressure can the package absorb without collapsing? | `matchup_too_narrow` |

## Example Mechanism: Delayed Charge Release

This is a role-level example only. It is not a formal card set.

```yaml
mechanism_candidate:
  axis_id: delayed_charge_release
  fantasy: build visible charge, choose when to release, keep partial value if delayed
  foundation_dependencies:
    required:
      - defense
      - payoff_conversion
    optional:
      - draw
      - retain
      - energy
  foundation_identity_risks:
    - swallowed_by_draw
    - swallowed_by_energy
  first_parameter_target:
    parameter: charge_turns
    initial_probe: 2_to_3_turns
package_skeleton:
  anchor: charge state source that is visible before payoff
  support: charge progress or protection while charging
  glue: timing, filter, or retain bridge that makes release a choice
  payoff: release converter with at least two useful release modes
  safety_valve: partial release or defensive conversion when the full release misses
expected_report_questions:
  agency: is release timing matchup-dependent?
  payoff_texture: can release be burst, defense, or conversion rather than one number?
  setup_tax: does charging contribute before payoff?
  fail_state_value: does partial charge still matter?
  deck_compression_requirement: does the plan need a thin deck to see anchor plus payoff?
  support_payoff_balance: does support arrive before payoff greed?
```

### Initial Judgment

`delayed_charge_release` is a plausible `revise` candidate if the first package skeleton
keeps charge timing as the main decision. It should be rejected if draw, energy, or raw
payoff numbers become the real identity.

## Rejection Reasons

These are advisory reasons for report-only review. They do not create hard gates.

| `rejection_reason` | Meaning | First revision question |
| --- | --- | --- |
| `swallowed_by_draw` | Draw throughput is the real engine, and the named mechanism adds little agency. | Can the axis add a timing, targeting, or state choice that draw alone cannot provide? |
| `swallowed_by_energy` | Energy acceleration makes the package generic resource goodstuff. | Can the payoff require a non-energy decision or visible setup state? |
| `swallowed_by_discard` | Discard outlets become generic filtering rather than mechanism identity. | Is discard a cost, trigger, resource, or release condition? |
| `removal_dependency_too_high` | The plan only works after unrealistic starter cleanup or route-specific removal. | Can in-combat compression, broader density, or lower exactness reduce the burden? |
| `payoff_only` | The package has a payoff fantasy but insufficient setup, bridge, or support. | Which support or glue role must be built before payoff? |
| `generic_goodstuff` | Strong cards or broad value hide a weak mechanism. | Which card job proves the named axis instead of ordinary value? |
| `low_agency_loop` | The online pattern becomes repetitive, automatic, and low-choice. | What constraint, timing fork, matchup response, or safety tradeoff restores agency? |
| `matchup_too_narrow` | One common encounter pressure invalidates the mechanism or the mechanism ignores all pressure. | Which safety valve or alternate line improves elasticity? |
| `setup_tax_too_high` | The setup asks for too many turns, slots, energy, upgrades, or exact pieces before function. | Can setup pieces do useful work before payoff? |
| `fail_state_missing` | Missing the release leaves dead cards, wasted turns, or generic survival only. | What partial progress, fallback output, or recoverable miss should exist? |

## Working Log

### 2026-04-27 Slice 1

Evaluation/design problem:

- Define how a mechanism-axis candidate becomes a package skeleton and design brief
  without creating a new evaluator or autonomous card generator.

Model increment:

- Added the report-only `evaluation_autonomous_design_model_v1` envelope.
- Defined the minimum entity vocabulary for candidate, reports, evidence, skeleton,
  brief, and rejection reasons.
- Normalized evaluation dimensions across fun/health, deck compression, package health,
  and design-iteration language.

Example mechanism/package:

- Used `delayed_charge_release` as a role-only example.
- First parameter target is `charge_turns`.
- Skeleton roles are anchor, support, glue, payoff, and safety valve.

Judgment rules:

- A candidate may only advance when the named mechanism keeps agency after foundation
  support is added.
- Package skeletons must show support and glue before payoff.
- Compression/removal assumptions must be visible before any loop, exactness, or
  compact-shell claim is treated as reachable.
- `promote` means human-review queue only.

Failure case:

- If `delayed_charge_release` becomes "draw enough cards, gain enough energy, then play
  one large payoff," record `swallowed_by_draw`, `swallowed_by_energy`, or
  `generic_goodstuff` before expanding the skeleton.

Next round entry:

- Pick one parameter, likely `charge_turns` or `fail_state_floor`, and write a tighter
  report-only brief template that maps expected evidence from the canonical surfaces.
  Do not add code, fixtures, or generated cards unless a later task explicitly asks for
  that implementation slice.
