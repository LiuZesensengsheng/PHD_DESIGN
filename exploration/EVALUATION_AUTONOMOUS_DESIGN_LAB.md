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

## Parameter Brief Template: `charge_turns`

This template is the first reusable brief format for a single parameter probe. It keeps
the work at role and evidence level. It must not become card text, final numbers, a
hard gate, or a learned promotion feature.

Use this when the smallest current question is:

- How many turns should a delayed setup ask for before the release feels earned but not
  dead?

### Brief Shape

```yaml
design_candidate_brief:
  brief_id: charge_turns_delayed_release_probe_v1
  evaluation_mode: report_only
  mechanism_candidate:
    axis_id: delayed_charge_release
    axis_question: can charge timing stay meaningful after foundation support is added?
  parameter_target:
    name: charge_turns
    probe_band: short_to_medium
    companion_parameter: fail_state_floor
    forbidden_claims:
      - exact_balance_number
      - final_card_text
      - hard_gate_pass
      - autonomous_promotion
  foundation_dependencies:
    required:
      - defense_or_tempo_buffer
      - visible_progress_state
      - release_conversion
    optional:
      - draw_selection
      - retain_or_timing_hold
      - limited_energy_smoothing
    identity_risks:
      - swallowed_by_draw
      - swallowed_by_energy
      - generic_goodstuff
  package_skeleton:
    anchor: creates or tracks delayed charge progress
    support: keeps the player alive or productive while charge builds
    glue: lets the player adjust release timing without solving the whole line
    payoff: converts charge into at least two distinct release modes
    safety_valve: turns partial charge into useful output when full release misses
  report_requests:
    mechanism_axis_discovery_summary:
      - foundation_dependency_vector
      - axis_agency_preservation
      - first_parameter_probe
    mechanism_fun_health_summary:
      - agency
      - payoff_texture
      - setup_tax
      - fail_state_value
      - variance_pressure
      - matchup_elasticity
    card_package_health_summary:
      - package_density
      - support_payoff_balance
      - glue_quality
      - anchor_clarity
      - goodstuff_risk
      - payoff_only_risk
    deck_compression_summary:
      - deck_compression_requirement
      - starter_pollution_tolerance
      - removal_access_dependency
    design_iteration_summary:
      - reject_revise_promote_recommendation
      - primary_rejection_reason
      - next_parameter_to_probe
```

### Evidence Mapping

| Canonical surface | Evidence needed for `charge_turns` | Red flag |
| --- | --- | --- |
| `mechanism_axis_discovery_v1` | Shows that charge/release is the named axis and draw, energy, or defense are support axes. | Foundation support becomes the real axis. |
| `mechanism_fun_health_v1` | Shows release timing has matchup-dependent choices and setup turns are not dead turns. | The player waits for a fixed countdown with no meaningful choices. |
| `card_package_health_v1` | Shows anchor, support, glue, payoff, and safety valve roles are all visible. | Payoff appears before support/glue, or broad value hides weak package identity. |
| `deck_compression_report_v1` | Shows whether seeing anchor plus payoff requires a compact deck or route-specific removal. | The brief assumes repeated contact without naming compression or starter pollution. |
| `design_iteration_brief_v1` | States whether to reject, revise one parameter, or send the role brief to human review. | The brief sounds certain while report evidence is thin or conflicting. |
| `cardanalysis_evidence_bundle_v1` | Keeps all report summaries inspectable and separated by owner. | Aggregation hides disagreement or turns report-only evidence into pass/fail authority. |

### Probe Bands

The lab should describe `charge_turns` with bands rather than exact balance numbers.

| Band | Interpretation | Main review pressure |
| --- | --- | --- |
| `immediate` | The release can happen before delayed play is really established. | Risk of `generic_goodstuff` or low combo aspiration. |
| `short` | The player can usually release after a small, readable setup window. | Check whether the setup has enough agency to avoid automatic play. |
| `medium` | The charge asks for a visible commitment and should create a real release moment. | Check `setup_tax`, `fail_state_value`, and matchup elasticity. |
| `long` | The charge becomes a high-commitment plan that must defend itself while building. | Risk of `setup_tax_too_high` and `fail_state_missing`. |
| `exact_or_variable` | The release asks for exact timing or variable timing control. | Risk of `variance_pressure`, payoff-only exactness, or draw/retain swallowing the axis. |

For the first report-only pass, prefer probing `short` versus `medium`. Do not search
`long` until the safety valve is explicit. Do not search `exact_or_variable` until the
brief can show why exactness improves agency instead of only increasing brittleness.

### Companion Safety Valve: `fail_state_floor`

`charge_turns` should never be reviewed alone. Every delayed setup brief must name a
`fail_state_floor`:

- `partial_progress`: partial charge still converts into a smaller useful result
- `defensive_buffer`: charge setup also protects the player during the setup window
- `selection_recovery`: missed release improves later timing or card access
- `state_conversion`: unused charge changes mode instead of becoming blank
- `none_visible`: no recoverable miss is present

If the safety valve is `none_visible`, the default recommendation is `revise`, not
`promote`, even when the dream payoff is exciting.

### Decision Wording

The template uses three advisory outcomes:

| Outcome | Meaning |
| --- | --- |
| `reject` | Stop this candidate for a named `rejection_reason`; do not expand the package skeleton. |
| `revise` | Keep the mechanism axis, but change one parameter or one missing role. |
| `promote` | Send the role-level brief to human review or a future reviewed fixture task. |

`promote` requires all of the following report-only signals:

- charge timing remains the primary agency source
- setup turns have useful output before full payoff
- package skeleton includes visible support and glue before payoff
- safety valve is not `none_visible`
- compression and removal assumptions are named, even if unknown
- goodstuff and payoff-only risks are explicitly addressed

These are not hard gates. They are the minimum wording discipline for avoiding false
confidence in an autonomous-design brief.

## Evidence Bundle Handoff Checklist

This checklist is the third slice for the `charge_turns` template. It describes what a
complete report-only handoff should contain without changing
`cardanalysis_evidence_bundle_v1` or adding a new surface.

The existing bundle already allows missing sections. This checklist only explains how
the lab should interpret those missing sections in a design brief.

### Bundle Envelope

```yaml
cardanalysis_evidence_bundle_handoff:
  contract_version: cardanalysis_evidence_bundle_v1
  evaluation_mode: report_only
  bundle_id: charge_turns_delayed_release_probe_v1
  designer_intent:
    mechanism_target: delayed_charge_release
    parameter_target: charge_turns
    companion_parameter: fail_state_floor
    package_skeleton_level: role_only
    forbidden_claims:
      - formal_card
      - exact_balance_number
      - hard_gate
      - default_recommendation_change
      - learned_or_reranker_promotion
  expected_sections:
    mechanism_axis_discovery_summary: required_for_axis_choice
    mechanism_axis_summary: optional_viability_read_if_available
    mechanism_fun_health_summary: required_before_promote_wording
    card_package_health_summary: required_before_promote_wording
    deck_compression_summary: required_before_reachability_wording
    design_iteration_summary: required_for_reject_revise_promote_wording
  allowed_missing_sections: true
  review_required: true
```

`mechanism_axis_summary` is included because the current evidence bundle supports it.
It is not a new lab-owned surface. Treat it as an optional existing viability read that
can reveal "final shell online" versus "not online" context before the brief asks fun,
package, or reachability questions.

### Section Checklist

| Bundle section | Handoff question | If missing |
| --- | --- | --- |
| `designer_intent` | Does the bundle state `delayed_charge_release`, `charge_turns`, `fail_state_floor`, and role-only scope? | Mark the handoff incomplete; do not infer intent from report text. |
| `mechanism_axis_discovery_summary` | Was this axis chosen because charge timing preserves agency after foundation support? | Use `needs_parameter_probe`; do not claim the axis was selected. |
| `mechanism_axis_summary` | Is there an existing viability read for whether the final shell can come online? | Keep online/offline wording unknown; do not block docs-only brief work. |
| `mechanism_fun_health_summary` | Are agency, payoff texture, setup tax, fail-state value, variance, and matchup elasticity visible? | Use `not_evaluated` for fun/health and avoid `promote` wording. |
| `card_package_health_summary` | Are anchor, support, glue, payoff, safety valve, density, and anti-goodstuff risks visible? | Use `revise` if payoff/support sequencing is being claimed. |
| `deck_compression_summary` | Are compression, starter pollution, and removal assumptions named before reachability claims? | Use `reachability_unknown`; do not claim the package is generally reachable. |
| `design_iteration_summary` | Is there a report-only recommendation and primary reason? | The lab may summarize risks, but should not write `reject`, `revise`, or `promote`. |
| `evidence_conflicts` | Does the bundle surface conflicts such as positive fun/health with route-dependent compression? | If absent because sections are missing, state `conflicts_not_evaluated`. |

### Completeness Labels

The lab can use these labels in prose. They are not new payload fields and not gates.

| Label | Meaning |
| --- | --- |
| `handoff_complete` | All expected sections are present and no required role-level intent is missing. |
| `handoff_partial` | Enough sections are present to discuss the next revision, but not enough for `promote` wording. |
| `axis_choice_missing` | `mechanism_axis_discovery_summary` is missing, so axis selection remains unreviewed. |
| `fun_health_missing` | Fun/health cannot be claimed; use `not_evaluated`. |
| `package_health_missing` | Package coherence cannot be claimed; avoid package-ready language. |
| `reachability_missing` | Compression/removal assumptions are absent; avoid reachable-from-run language. |
| `iteration_recommendation_missing` | The lab can list risks but should not choose reject/revise/promote wording. |
| `conflicts_not_evaluated` | Missing sections prevent bundle conflict checks from being meaningful. |

### Conflict Review

For `charge_turns`, reviewers should inspect conflicts before reading the final
recommendation:

- If fun/health is positive but compression is route-dependent, keep the play-pattern
  praise but downgrade reachability language.
- If a mechanism-axis summary says the final shell is online but compression is
  route-dependent, state that online final-shell evidence does not prove normal-run
  assembly.
- If package health is positive but fun/health is missing, the package can be coherent
  while play texture remains unevaluated.
- If fun/health is positive but package health is missing, the mechanism may be fun in
  theory while the package skeleton is not yet review-ready.

These conflicts should produce review notes, not automatic rejection.

### Handoff Decision Discipline

Use the most conservative wording supported by present sections:

| Present evidence | Allowed wording |
| --- | --- |
| designer intent only | `review_only_candidate` |
| discovery only | `needs_parameter_probe` |
| discovery plus package health | `revise_package_skeleton` |
| discovery plus fun/health | `revise_play_pattern_or_parameter` |
| discovery plus compression | `reachability_known_or_unknown`, depending on compression report |
| all expected sections except design iteration | risk summary only, no reject/revise/promote |
| all expected sections present | `reject`, `revise`, or `promote_to_human_review_queue` |

Do not collapse this table into pass/fail. The purpose is to keep missing evidence
visible so the next agent can run or request the owning report rather than inventing an
answer.

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

## Revision Action Map For `charge_turns`

This table turns a `rejection_reason` into one next revision action for the
`charge_turns` brief. It is deliberately narrow:

- one reason maps to one first action
- action wording stays at parameter or role-skeleton level
- actions do not create scores, thresholds, gates, generated cards, or automatic
  promotion

| `rejection_reason` | First `revision_action` | What to change first | What not to do |
| --- | --- | --- | --- |
| `swallowed_by_draw` | `restore_timing_choice` | Add a timing, hold, or release fork that draw alone cannot solve. | Do not add more draw as the fix. |
| `swallowed_by_energy` | `remove_energy_as_identity` | Make release depend on visible charge state, matchup timing, or conversion choice. | Do not make the payoff merely more expensive or more refunded. |
| `swallowed_by_discard` | `separate_filter_from_charge` | State whether discard is a trigger, cost, or smoothing support. | Do not treat generic hand cleanup as proof of the charge axis. |
| `removal_dependency_too_high` | `widen_non_removal_reachability` | Reduce exactness, add in-combat compression, or increase role redundancy. | Do not assume shop/event removal as free reachability. |
| `payoff_only` | `build_support_before_payoff` | Add support or glue before increasing payoff ambition. | Do not write a bigger release fantasy first. |
| `generic_goodstuff` | `sharpen_axis_proof` | Name the job that only delayed charge/release can do. | Do not count strong defense, damage, draw, or energy as package proof by itself. |
| `low_agency_loop` | `add_release_fork` | Add a matchup, timing, target, or safety tradeoff after charge is online. | Do not rely on repeated automatic charge-release cycles. |
| `matchup_too_narrow` | `add_safety_valve_mode` | Add one alternate line for fast, multi-enemy, action-punisher, or scaling pressure. | Do not average the weakness away with generic value. |
| `setup_tax_too_high` | `shorten_or_pay_back_setup` | Move from `medium` toward `short`, or make setup turns produce useful output. | Do not compensate only by making the final payoff larger. |
| `fail_state_missing` | `raise_fail_state_floor` | Choose `partial_progress`, `defensive_buffer`, `selection_recovery`, or `state_conversion`. | Do not keep `fail_state_floor=none_visible` while using `promote` wording. |

### Action Sequencing

When multiple rejection reasons appear, revise in this order:

1. Fix identity swallowing first:
   `swallowed_by_draw`, `swallowed_by_energy`, `swallowed_by_discard`,
   `generic_goodstuff`.
2. Fix skeleton order second:
   `payoff_only`, `setup_tax_too_high`, `fail_state_missing`.
3. Fix reachability third:
   `removal_dependency_too_high`.
4. Fix matchup and loop texture fourth:
   `low_agency_loop`, `matchup_too_narrow`.

The sequencing is advisory. Its purpose is to prevent the brief from polishing a payoff
while the axis identity, setup burden, or fail state is still unresolved.

### Revision Output Shape

Use a compact report-only note:

```yaml
revision_note:
  evaluation_mode: report_only
  source_template: charge_turns_delayed_release_probe_v1
  rejection_reason: setup_tax_too_high
  revision_action: shorten_or_pay_back_setup
  parameter_to_adjust: charge_turns
  role_to_adjust: support
  forbidden_changes:
    - final_card_text
    - exact_balance_number
    - hard_gate_threshold
    - learned_or_reranker_promotion
  next_review_request:
    - mechanism_fun_health_summary
    - card_package_health_summary
```

If the next revision cannot name exactly one parameter or one package role to adjust,
the brief is still too broad and should return to `review_only_candidate`.

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

### 2026-04-27 Slice 2

Evaluation/design problem:

- Turn the vague `charge_turns` next step into a reusable report-only brief template
  that still cannot generate formal cards or claim hard-gate authority.

Model increment:

- Added `Parameter Brief Template: charge_turns`.
- Made `fail_state_floor` a required companion parameter for delayed setup probes.
- Mapped the brief to the canonical evidence bundle sections for mechanism discovery,
  fun/health, package health, deck compression, design iteration, and evidence bundle
  ownership.

Example mechanism/package:

- Continued using `delayed_charge_release`.
- Kept the package at role level: anchor, support, glue, payoff, safety valve.
- Introduced `short` versus `medium` as the first useful probe band, avoiding exact
  numeric balance claims.

Judgment rules:

- `charge_turns` should be described as a probe band, not a final number.
- `fail_state_floor=none_visible` forces a `revise` recommendation by wording
  discipline, not by hard gate.
- `promote` requires visible support/glue before payoff and explicit compression
  assumptions, but still only means human-review queue.

Failure case:

- If longer charge only makes the payoff larger while setup turns do not create agency,
  partial value, or matchup adaptation, record `setup_tax_too_high` plus
  `fail_state_missing` and revise the safety valve before touching payoff ambition.

Next round entry:

- Define a compact `evidence_bundle` handoff checklist for this template so future
  runs can tell which canonical report is missing without merging report ownership.

### 2026-04-27 Slice 3

Evaluation/design problem:

- Make the `charge_turns` brief resumable by listing exactly which evidence bundle
  sections are expected and what wording is allowed when each section is missing.

Model increment:

- Added `Evidence Bundle Handoff Checklist`.
- Included `mechanism_axis_summary` as an optional existing viability read supported by
  the bundle, while keeping canonical report-only ownership unchanged.
- Added prose-only completeness labels such as `handoff_partial`,
  `reachability_missing`, and `iteration_recommendation_missing`.

Example mechanism/package:

- Continued using `delayed_charge_release` with `charge_turns` plus
  `fail_state_floor`.
- Kept the bundle handoff at role/summary level; no generated card text, exact balance
  numbers, or fixture schema changes were introduced.

Judgment rules:

- Missing fun/health means play texture is `not_evaluated`, not bad.
- Missing deck compression means reachability is unknown, not free.
- Missing design iteration means the lab may list risks but should not write
  `reject`, `revise`, or `promote`.
- Evidence conflicts should produce review notes, not automatic rejection.

Failure case:

- If a future brief claims `promote` while `deck_compression_summary` or
  `design_iteration_summary` is missing, treat that as false confidence and downgrade
  the wording to a partial handoff.

Next round entry:

- Add one compact `rejection_reason` to `revision_action` mapping for the
  `charge_turns` template, still as docs-only guidance and not as evaluator logic.

### 2026-04-27 Slice 4

Evaluation/design problem:

- Convert `charge_turns` rejection reasons into first revision actions without turning
  the lab into a scoring or generation system.

Model increment:

- Added `Revision Action Map For charge_turns`.
- Added advisory action sequencing so identity swallowing is addressed before payoff
  polishing, reachability claims, or matchup texture.
- Added a compact `revision_note` shape that keeps the next step at parameter or role
  level.

Example mechanism/package:

- Continued using `delayed_charge_release`.
- The example revision note uses `setup_tax_too_high -> shorten_or_pay_back_setup`
  and adjusts `charge_turns` plus the `support` role.

Judgment rules:

- A revision action must name one first action, one parameter or role to adjust, and
  the owning report summaries to re-check.
- If a revision cannot name one parameter or one package role, it is still too broad
  and should return to `review_only_candidate`.
- Identity-swallowing failures should be fixed before larger payoff work.

Failure case:

- If the brief responds to `setup_tax_too_high` by only increasing payoff size, keep
  the rejection reason and require either shorter setup or useful setup output.

Next round entry:

- Add one minimal package-skeleton readiness checklist for `charge_turns`, focused on
  anchor/support/glue/payoff/safety-valve completeness and still docs-only.
