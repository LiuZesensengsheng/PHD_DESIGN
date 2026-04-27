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

## Package Skeleton Readiness For `charge_turns`

This checklist decides whether a role-level `package_skeleton` is ready to be handed to
the canonical report-only surfaces. It does not decide whether the package is good, fun,
balanced, legal, or ready for card generation.

### Readiness Labels

Use these labels only in prose:

| Label | Meaning |
| --- | --- |
| `skeleton_ready_for_review` | All five roles are named, the safety valve is non-empty, and the brief states what evidence to request next. |
| `skeleton_partial` | At least three roles are named, but one required role or evidence request is still vague. |
| `skeleton_payoff_only` | Payoff is clearer than anchor, support, or glue. |
| `skeleton_goodstuff_blur` | Support roles are generic value and do not prove delayed charge/release identity. |
| `skeleton_fail_state_gap` | Safety valve is missing, `none_visible`, or not tied to charge state. |
| `skeleton_reachability_unknown` | Roles are clear, but compression/removal assumptions are not named. |

These labels should not appear as evaluator outputs unless a later implementation task
explicitly adds reviewed fixtures and tests.

### Role Checklist

| Role | Required for `charge_turns` review | Common weak version | First revision action |
| --- | --- | --- | --- |
| `anchor` | Names the visible charge state or delayed progress source. | Any strong card that happens to wait. | `sharpen_axis_proof` |
| `support` | Helps the player survive or stay productive while charge builds. | Generic block, damage, draw, or energy that would fit any package. | `build_support_before_payoff` |
| `glue` | Lets the player adjust timing, hold state, filter, or bridge setup to release. | More throughput without a timing decision. | `restore_timing_choice` |
| `payoff` | Converts charge into at least two release modes or one release plus a meaningful tradeoff. | One large delayed number. | `add_release_fork` |
| `safety_valve` | Gives partial progress, defense, selection recovery, or state conversion when full release misses. | `none_visible`, blank miss, or generic survival. | `raise_fail_state_floor` |

### Minimum Skeleton Shape

```yaml
package_skeleton_readiness:
  evaluation_mode: report_only
  source_template: charge_turns_delayed_release_probe_v1
  readiness_label: skeleton_partial
  roles:
    anchor:
      present: true
      review_note: visible_charge_state_named
    support:
      present: true
      review_note: setup_turns_have_output
    glue:
      present: false
      review_note: timing_bridge_missing
    payoff:
      present: true
      review_note: release_conversion_named
    safety_valve:
      present: true
      fail_state_floor: partial_progress
  missing_role_actions:
    glue: restore_timing_choice
  next_report_requests:
    - card_package_health_summary
    - mechanism_fun_health_summary
```

If `anchor`, `support`, or `glue` is missing, the skeleton should not use `promote`
wording. If `payoff` is the only clear role, use `skeleton_payoff_only`. If
`safety_valve` is missing or `none_visible`, use `skeleton_fail_state_gap` even when
the other roles are clear.

### Role Completeness Rules

- `anchor` cannot be "the payoff card." The anchor must make progress visible before
  release.
- `support` cannot be counted as package proof unless it helps the setup window or the
  charge state specifically.
- `glue` must create a timing, hold, bridge, filter, or state-management decision.
- `payoff` must be staged after anchor/support/glue in the brief wording.
- `safety_valve` must explain what happens when full release misses.
- Any role can be `unknown`, but unknown roles force `skeleton_partial` or a narrower
  failure label.

### Handoff Rule

A `charge_turns` package skeleton is ready for report-only review when it can answer:

1. What is charging?
2. What keeps the player from paying dead setup turns?
3. What lets release timing become a choice?
4. What does the release convert into?
5. What happens if the full release misses?
6. Which canonical report should review the next uncertainty?

If any answer would require final card text, exact numbers, or a new evaluator, the
skeleton is not ready; return to role-level revision.

## Parameter Search Note: `short` Versus `medium` Charge Turns

This note answers the first parameter-search question for `charge_turns`: when should
the delayed setup read as `short`, and when should it read as `medium`?

It is a band comparison only. It does not choose exact turn counts, costs, card text,
thresholds, or balance numbers.

### Search Intent

Use `short` versus `medium` when all of these are true:

- The candidate already names `delayed_charge_release` as the primary axis.
- `fail_state_floor` is present and is not silently assumed.
- The package skeleton can name at least anchor, support, and payoff.
- The main uncertainty is setup commitment, not whether the mechanism exists.

If the brief cannot name those facts, return to `review_only_candidate` instead of
searching a band.

### Band Contrast

| Band | What it should test | Main risk | First report request |
| --- | --- | --- | --- |
| `short` | Can a compact charge window create a visible timing choice without becoming immediate value? | `generic_goodstuff`, `low_agency_loop` | `mechanism_fun_health_summary` |
| `medium` | Can a larger visible commitment create a better release moment without dead setup turns? | `setup_tax_too_high`, `fail_state_missing` | `mechanism_fun_health_summary` plus `card_package_health_summary` |

The first comparison should ask which band preserves agency with the least false
confidence. `short` is preferable when `medium` only increases payoff ambition.
`medium` is preferable only when it adds a real timing or matchup choice and the setup
turns still produce useful output.

### Minimal Parameter Note

```yaml
parameter_search_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  parameter_target: charge_turns
  candidate_bands:
    - short
    - medium
  companion_parameter: fail_state_floor
  search_question: preserve_release_agency_without_dead_setup
  forbidden_claims:
    - exact_turn_count
    - final_card_text
    - hard_gate_threshold
    - default_recommendation_change
    - learned_or_reranker_promotion
  first_review_focus:
    - agency
    - setup_tax
    - fail_state_value
    - support_payoff_balance
```

Do not compare `long` until a non-empty safety valve exists. Do not compare
`exact_or_variable` until the brief explains why exact timing improves agency instead
of only raising variance pressure.

## Foundation Dependency Budget For `charge_turns`

This note keeps foundation axes from swallowing `delayed_charge_release`.

The candidate is allowed to use draw, energy, retain, filter, defense, damage,
scaling, compression, discard, or exhaust as support. It should not let those axes
become the real reason the package works unless the mechanism candidate is renamed.

### Dependency Classes

| Dependency class | Meaning | Review wording |
| --- | --- | --- |
| `required_foundation` | The charge axis cannot be reviewed without this support. | Name it before the parameter probe. |
| `bounded_support` | The foundation helps the charge axis while leaving charge decisions visible. | Keep it as support evidence. |
| `identity_swallowing_risk` | The foundation axis now creates more agency than charge/release. | Revise identity before payoff work. |
| `unpriced_dependency` | The brief assumes support but does not name its cost or timing. | Request the owning report before reachability wording. |

### Budget Rules

- Defense can be required, but generic block does not prove the charge package.
- Draw can smooth setup, but more draw is not a fix for missing release decisions.
- Energy can enable release, but refund or acceleration cannot be the identity.
- Retain or filter can preserve agency when it creates a timing or hold decision.
- Compression can make repeated contact plausible, but deck compression owns the
  reachability language.
- Discard can support filtering only if the brief states whether discard is a cost,
  trigger, or smoothing tool.

### Minimal Dependency Note

```yaml
foundation_dependency_budget:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  required_foundation:
    - defense_or_tempo_buffer
    - visible_progress_state
  bounded_support:
    - retain_or_filter_for_release_timing
  identity_swallowing_risks:
    - swallowed_by_draw
    - swallowed_by_energy
  unpriced_dependencies:
    - compression_context_unknown
  first_revision_if_swallowed: restore_timing_choice
```

If the first proposed fix for a weak `charge_turns` brief is only "add more draw" or
"add more energy," record `swallowed_by_draw` or `swallowed_by_energy` before tuning
the payoff.

## Fail-State Floor Probe For `charge_turns`

This note answers the companion-parameter question: what useful output remains when
the full release misses?

`fail_state_floor` is not a reward for failure. It is the minimum recoverable output
that prevents delayed setup from becoming dead turns.

### Floor Options

| `fail_state_floor` | Useful when | Weak version |
| --- | --- | --- |
| `partial_progress` | Partial charge can become smaller output or later state. | Partial charge is only a worse payoff number. |
| `defensive_buffer` | Setup turns protect the player while charge builds. | Generic block that would be good in any package. |
| `selection_recovery` | Missing release improves later timing, access, or hold decisions. | More draw that hides the missed release. |
| `state_conversion` | Unused charge changes mode or role instead of going blank. | Conversion ignores charge state and becomes value soup. |
| `none_visible` | No recoverable miss is present yet. | Any `promote` wording is false confidence. |

### Pairing Rules

- `short` can tolerate a lighter floor if setup turns already produce useful output.
- `medium` needs a named non-empty floor before review-ready wording.
- `none_visible` should map to `raise_fail_state_floor`, not a larger payoff.
- The floor must mention charge state, setup timing, or release control to count as
  mechanism-specific.
- A floor that is only generic survival should be reviewed as `generic_goodstuff` risk.

### Minimal Floor Note

```yaml
fail_state_floor_probe:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  parameter_target: charge_turns
  candidate_band: medium
  fail_state_floor: partial_progress
  floor_question: does_partial_charge_still_change_the_next_decision
  first_revision_if_missing: raise_fail_state_floor
  next_report_requests:
    - mechanism_fun_health_summary
    - card_package_health_summary
```

If the floor cannot be described without writing final card text, keep the brief at
role level and mark the next action as `raise_fail_state_floor`.

## Compression Assumption Note For `charge_turns`

This note keeps `charge_turns` from accidentally assuming repeated anchor/payoff
contact in a compact deck.

The lab does not price removal routes itself. It only records whether compression and
starter-pollution assumptions are visible enough to request or read the canonical
`deck_compression_summary`.

### Compression Assumption Labels

Use these labels only in prose:

| Label | Meaning |
| --- | --- |
| `compression_named_low` | The brief names why normal deck growth should not erase charge contact. |
| `compression_named_medium` | The brief expects some thinning, selection, retain, or redundancy but does not require exact compactness. |
| `compression_route_dependent` | The brief depends on removal, transform quality, or early in-combat compression before the online claim is credible. |
| `compression_unknown` | The brief does not yet know whether starter pollution breaks contact. |
| `compression_false_confidence` | The brief claims repeated charge/release contact without naming deck size, redundancy, or route assumptions. |

These labels are not evaluator outputs and should not replace
`deck_compression_report_v1` wording such as `online_if_compressed` or
`route_dependent_online`.

### Assumption Rules

- A `short` band can still have high compression pressure if it needs repeated exact
  contact.
- A `medium` band can be acceptable with thicker decks only if support and glue provide
  real redundancy.
- Retain, filtering, and draw selection can lower variance, but they are not the same
  as persistent removal.
- Transform should not be treated as clean removal unless replacement risk is named.
- In-combat compression only helps if it arrives before charge/release contact matters.

### Minimal Compression Note

```yaml
compression_assumption_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  parameter_target: charge_turns
  assumption_label: compression_unknown
  known_context:
    deck_size: unknown
    starter_pollution: unknown
    removal_route: unknown
  forbidden_wording:
    - generally_reachable
    - reliable_loop
    - hard_gate_pass
  next_report_request: deck_compression_summary
```

If the package skeleton is otherwise clear but compression is unknown, use
`skeleton_reachability_unknown` rather than `promote`.

## Goodstuff And Payoff-Only Triage For `charge_turns`

This note distinguishes a real delayed charge/release package from generic value or a
single exciting payoff.

### Triage Questions

| Risk | Diagnostic question | First revision action |
| --- | --- | --- |
| `generic_goodstuff` | Would the same support be desirable if charge did not exist? | `sharpen_axis_proof` |
| `payoff_only` | Is the payoff clearer than the anchor, support, or glue? | `build_support_before_payoff` |
| `skeleton_goodstuff_blur` | Does broad defense, draw, or damage hide weak package identity? | `sharpen_axis_proof` |
| `skeleton_payoff_only` | Is the role skeleton mostly a release fantasy? | `build_support_before_payoff` |

### Role Proof Rules

- Anchor proof must show visible progress before release.
- Support proof must help the setup window or charge state specifically.
- Glue proof must create a timing, hold, bridge, filter, or state-management choice.
- Payoff proof must be downstream of anchor/support/glue in the brief wording.
- Safety-valve proof must explain the miss, not only the dream.

### Minimal Triage Note

```yaml
goodstuff_payoff_triage:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  package_skeleton_readiness: skeleton_payoff_only
  primary_risk: payoff_only
  role_to_fix_first: support
  revision_action: build_support_before_payoff
  forbidden_fix:
    - larger_payoff
    - generic_draw_patch
    - generic_energy_patch
```

If a role cannot name why it belongs to delayed charge/release, mark that role as
unknown instead of counting it as package density.

## Evidence Conflict Triage For `charge_turns`

This note keeps report-only evidence from being collapsed into a single confident
verdict.

Conflicts should be written as review notes. They should not become hard gates,
default recommendation changes, or autonomous promotion rules.

### Conflict Notes

| Evidence conflict | Conservative wording |
| --- | --- |
| Fun/health positive, compression route-dependent | The play pattern may be attractive, but normal-run reachability remains route-dependent. |
| Package health positive, fun/health missing | The package may be coherent, but play texture is `not_evaluated`. |
| Fun/health positive, package health missing | The mechanism may be promising, but the role skeleton is not package-ready. |
| Discovery positive, package payoff-only | The axis exists, but package assembly must revise support or glue first. |
| Discovery positive, foundation swallowing risk high | The axis needs identity revision before parameter tuning. |
| Compression positive, fail state missing | Reachability alone does not make delayed setup healthy. |

### Minimal Conflict Note

```yaml
evidence_conflict_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  conflict:
    positive_evidence: mechanism_fun_health_summary
    limiting_evidence: deck_compression_summary
  conservative_wording: attractive_but_route_dependent
  allowed_next_action: revise
  forbidden_next_action: autonomous_promote
```

When conflicts are unresolved, the design brief should name the next owning report to
read instead of inventing a combined score.

## Iteration Wording Ladder For `charge_turns`

This note limits how strongly a `charge_turns` brief may speak at each evidence level.

It is wording discipline only. It does not add pass/fail gates or evaluator labels.

### Wording Ladder

| Evidence state | Strongest allowed wording |
| --- | --- |
| Axis intent only | `review_only_candidate` |
| Axis plus parameter note | `needs_report_only_probe` |
| Axis plus partial skeleton | `revise_package_skeleton` |
| Skeleton ready, fun/health missing | `package_ready_for_fun_health_review` |
| Skeleton ready, compression missing | `package_ready_but_reachability_unknown` |
| All expected reports present, one primary risk remains | `revise_one_parameter_or_role` |
| All expected reports present, risks named, no false confidence | `promote_to_human_review_queue` |

`promote_to_human_review_queue` is the maximum wording. It does not mean formal card
generation, default recommendation, learned promotion, or hard-gate pass.

### Minimal Iteration Note

```yaml
iteration_wording_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  evidence_state: skeleton_ready_compression_missing
  allowed_wording: package_ready_but_reachability_unknown
  forbidden_wording:
    - validated_package
    - generally_reachable
    - hard_gate_pass
    - generate_cards
```

If a brief wants stronger wording than this ladder allows, the next action is to
request missing evidence, not to smooth the text.

## Enemy Pressure Tolerance Panel For `charge_turns`

This note gives `enemy_pressure_tolerance` a first report-only shape for delayed
charge/release.

The panel does not simulate encounters or create matchup gates. It names which common
pressure should be reviewed before a charge package sounds broadly healthy.

### Pressure Panel

| Pressure | Question for `charge_turns` | Failure reason |
| --- | --- | --- |
| `fast_pressure` | Can setup turns produce enough output before the release? | `setup_tax_too_high` |
| `multi_enemy_pressure` | Can release or safety-valve output avoid single-target tunnel vision? | `matchup_too_narrow` |
| `action_punisher_pressure` | Does the package avoid repeated low-impact charge actions? | `low_agency_loop` |
| `scaling_pressure` | Can delayed release matter before enemy scaling outpaces it? | `fantasy_only` |
| `defensive_race_pressure` | Can the package defend while keeping charge state relevant? | `fail_state_missing` |

`fantasy_only` is allowed as a prose diagnosis here because it appears in the
fun/health review vocabulary. It should not be added to the lab's normalized
`rejection_reason` list unless a later reviewed implementation task asks for that
expansion.

### Minimal Pressure Note

```yaml
enemy_pressure_tolerance_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  parameter_target: charge_turns
  pressure_to_review_first: fast_pressure
  tolerance_question: do_setup_turns_have_output_before_release
  likely_revision_action: shorten_or_pay_back_setup
  next_report_request: mechanism_fun_health_summary
```

If the package only works in slow fights, use `matchup_too_narrow` or
`setup_tax_too_high` before increasing payoff ambition.

## Package Density Balance For `charge_turns`

This note keeps `package_density` and `support_payoff_balance` separate.

A package can have many on-theme roles and still be unhealthy if payoff dominates the
sequence. It can also have low density but a clear next revision if the missing role is
named.

### Balance Reads

| Read | Healthy sign | Risk sign |
| --- | --- | --- |
| `role_density` | Anchor, support, glue, payoff, and safety valve are all represented at role level. | Payoff is the only detailed role. |
| `support_before_payoff` | Support and glue are described before release ambition. | The brief starts with a finisher. |
| `redundancy_without_soup` | More than one role can support charge state without becoming generic value. | Extra roles are just draw, block, damage, or energy. |
| `payoff_texture_balance` | Release can branch or convert state without replacing setup decisions. | Release is one large number. |

### Balance Rules

- More density is not automatically better if it blurs the axis into goodstuff.
- One clear missing role is better than five vague roles.
- Support density should be reviewed before payoff upgrades.
- Glue quality should be reviewed before any exact or variable timing probe.
- Safety-valve density matters only when it is tied to charge state or setup timing.

### Minimal Balance Note

```yaml
package_density_balance_note:
  evaluation_mode: report_only
  mechanism_candidate: delayed_charge_release
  package_density_read: partial
  support_payoff_balance_read: support_before_payoff_missing
  role_to_fix_first: glue
  revision_action: restore_timing_choice
  next_report_request: card_package_health_summary
```

If density improves by adding generic value, mark `generic_goodstuff` instead of
calling the skeleton healthier.

## Transfer Note: `discard_outlet_count`

This note checks whether the lab vocabulary can transfer from `charge_turns` to another
parameter without becoming a card generator.

The second parameter is `discard_outlet_count`. The goal is not to design formal discard
cards. The goal is to ask when discard remains a mechanism identity rather than generic
hand cleanup.

### Minimal Transfer Shape

```yaml
design_candidate_brief:
  brief_id: discard_outlet_count_identity_probe_v1
  evaluation_mode: report_only
  mechanism_candidate:
    axis_id: discard_velocity_release
    axis_question: does_discard_create_identity_or_only_filtering
  parameter_target:
    name: discard_outlet_count
    probe_band: low_to_medium
    companion_parameter: payoff_contact_reliability
  foundation_dependencies:
    required:
      - discard_outlet
      - discard_payoff_or_resource
    optional:
      - draw_selection
      - hand_size_buffer
      - energy_smoothing
    identity_risks:
      - swallowed_by_discard
      - swallowed_by_draw
      - generic_goodstuff
  package_skeleton:
    anchor: visible reason discard matters beyond cleanup
    support: keeps outlet/payoff contact from becoming draw-order fantasy
    glue: chooses what to discard, hold, or convert
    payoff: rewards discard timing or accumulated discard state
    safety_valve: missed outlet still leaves selection, block, or partial resource value
  report_requests:
    mechanism_axis_discovery_summary:
      - foundation_dependency_vector
      - axis_agency_preservation
      - first_parameter_probe
    mechanism_fun_health_summary:
      - agency
      - variance_pressure
      - fail_state_value
      - payoff_texture
    card_package_health_summary:
      - package_density
      - glue_quality
      - goodstuff_risk
      - payoff_only_risk
    deck_compression_summary:
      - starter_pollution_tolerance
      - deck_compression_requirement
```

### Transfer Rules

- If discard is only a way to see more cards, record `swallowed_by_draw`.
- If discard is only hand cleanup with no cost, trigger, resource, or release choice,
  record `swallowed_by_discard`.
- If the payoff is clear but outlet density is vague, record `payoff_only`.
- If outlet density is high but every decision is automatic, record `low_agency_loop`.
- If starter or off-axis cards are assumed to disappear, request
  `deck_compression_summary`.

This transfer keeps the model parameter-level and role-level. It should not produce
card text, exact outlet counts, formal discard cards, or default ranking changes.

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

### 2026-04-27 Slice 5

Evaluation/design problem:

- Decide when a `charge_turns` role-level package skeleton is ready to be handed to
  canonical report-only review without becoming card generation or a gate.

Model increment:

- Added `Package Skeleton Readiness For charge_turns`.
- Defined prose-only readiness labels such as `skeleton_ready_for_review`,
  `skeleton_payoff_only`, `skeleton_goodstuff_blur`, and
  `skeleton_fail_state_gap`.
- Added a five-role checklist for anchor, support, glue, payoff, and safety valve.

Example mechanism/package:

- Continued using `delayed_charge_release`.
- The example readiness payload marks glue missing and maps that missing role to
  `restore_timing_choice`.

Judgment rules:

- The anchor cannot be the payoff card.
- Support only counts when it helps the setup window or charge state specifically.
- Glue must create a timing, hold, bridge, filter, or state-management decision.
- Safety valve must explain what happens when full release misses.
- Missing roles keep the skeleton at `skeleton_partial` or a narrower failure label.

Failure case:

- If payoff is the only clear role, label the skeleton `skeleton_payoff_only` and
  revise support/glue before writing a larger release fantasy.

Next round entry:

- Add one minimal parameter-search note for the first `short` versus `medium`
  `charge_turns` probe, still using bands and no exact balance numbers.

### 2026-04-27 Slice 6

Evaluation/design problem:

- Decide how to compare `short` versus `medium` `charge_turns` without choosing exact
  balance numbers.

Model increment:

- Added `Parameter Search Note: short Versus medium Charge Turns`.
- Defined the first band comparison as a search for release agency without dead setup.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example note compares only `short` and `medium` with `fail_state_floor` as a
  companion parameter.

Judgment rules:

- Use `short` when `medium` only increases payoff ambition.
- Use `medium` only when it creates a real timing or matchup decision and setup turns
  still produce useful output.

Failure case:

- If the brief cannot name axis, companion floor, and basic roles, it returns to
  `review_only_candidate` instead of searching a band.

Next round entry:

- Add one minimal foundation dependency budget so draw, energy, and other support axes
  do not swallow the charge identity.

### 2026-04-27 Slice 7

Evaluation/design problem:

- Decide when foundation support helps `charge_turns` and when it becomes the real
  identity.

Model increment:

- Added `Foundation Dependency Budget For charge_turns`.
- Split dependencies into `required_foundation`, `bounded_support`,
  `identity_swallowing_risk`, and `unpriced_dependency`.

Example mechanism/package:

- Continued `delayed_charge_release` with defense and visible progress as required
  foundations, retain/filter as bounded support, and draw/energy as swallowing risks.

Judgment rules:

- Generic block does not prove the package.
- More draw or more energy is not a fix for missing release decisions.
- Compression remains owned by the canonical deck compression surface.

Failure case:

- If the first proposed fix is only "add more draw" or "add more energy," record
  `swallowed_by_draw` or `swallowed_by_energy` before tuning payoff.

Next round entry:

- Add one minimal `fail_state_floor` probe so the companion parameter has its own
  review discipline.

### 2026-04-27 Slice 8

Evaluation/design problem:

- Decide what useful output remains when the full `charge_turns` release misses.

Model increment:

- Added `Fail-State Floor Probe For charge_turns`.
- Compared `partial_progress`, `defensive_buffer`, `selection_recovery`,
  `state_conversion`, and `none_visible`.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example uses `medium` plus `partial_progress` and asks whether partial charge
  changes the next decision.

Judgment rules:

- `medium` needs a named non-empty floor before review-ready wording.
- A floor must reference charge state, setup timing, or release control to count as
  mechanism-specific.

Failure case:

- If the floor is `none_visible`, revise with `raise_fail_state_floor` rather than
  making the final payoff larger.

Next round entry:

- Add one compression assumption note so repeated anchor/payoff contact is not
  silently assumed.

### 2026-04-27 Slice 9

Evaluation/design problem:

- Decide how much compression and starter-pollution context must be visible before a
  `charge_turns` brief discusses reachability.

Model increment:

- Added `Compression Assumption Note For charge_turns`.
- Defined prose-only assumption labels such as `compression_unknown`,
  `compression_route_dependent`, and `compression_false_confidence`.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example note sets deck size, starter pollution, and removal route to unknown and
  requests `deck_compression_summary`.

Judgment rules:

- Retain, filtering, and draw selection are not persistent removal.
- In-combat compression helps only if it arrives before charge/release contact matters.

Failure case:

- If the skeleton is otherwise clear but compression is unknown, use
  `skeleton_reachability_unknown` instead of `promote`.

Next round entry:

- Add one goodstuff/payoff-only triage so role density does not hide generic support.

### 2026-04-27 Slice 10

Evaluation/design problem:

- Distinguish a real delayed charge/release package from generic value or a single
  exciting payoff.

Model increment:

- Added `Goodstuff And Payoff-Only Triage For charge_turns`.
- Mapped generic-goodstuff and payoff-only risks to the first role-level revision.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example triage marks the skeleton as `skeleton_payoff_only` and fixes support
  before payoff.

Judgment rules:

- Anchor, support, glue, payoff, and safety valve each need role-specific proof.
- A role that cannot explain why it belongs to delayed charge/release stays unknown.

Failure case:

- If a brief adds generic draw, block, damage, or energy as package proof, record
  `generic_goodstuff` rather than counting healthier density.

Next round entry:

- Add one evidence-conflict triage so report-only summaries stay separated.

### 2026-04-27 Slice 11

Evaluation/design problem:

- Decide how to handle conflicting report-only evidence without collapsing it into a
  hidden score.

Model increment:

- Added `Evidence Conflict Triage For charge_turns`.
- Listed conservative wording for common conflicts between discovery, fun/health,
  package health, and compression summaries.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example conflict keeps a positive fun/health read but limits wording because
  deck compression is route-dependent.

Judgment rules:

- Conflicts produce review notes, not automatic rejection.
- The brief should name the next owning report instead of inventing a combined score.

Failure case:

- If fun/health is positive but compression is route-dependent, do not call the package
  generally reachable.

Next round entry:

- Add one iteration wording ladder so the brief cannot overstate thin evidence.

### 2026-04-27 Slice 12

Evaluation/design problem:

- Limit how strongly a `charge_turns` brief may speak at each evidence level.

Model increment:

- Added `Iteration Wording Ladder For charge_turns`.
- Defined the strongest allowed wording from axis intent through
  `promote_to_human_review_queue`.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example marks a skeleton-ready but compression-missing case as
  `package_ready_but_reachability_unknown`.

Judgment rules:

- `promote_to_human_review_queue` is the maximum wording.
- Stronger wording requires missing evidence, not smoother prose.

Failure case:

- If a brief says `validated_package`, `generally_reachable`, `hard_gate_pass`, or
  `generate_cards`, it has crossed the lab boundary.

Next round entry:

- Add one enemy-pressure tolerance panel so matchup elasticity has a first review
  shape for `charge_turns`.

### 2026-04-27 Slice 13

Evaluation/design problem:

- Decide which common enemy pressure should be reviewed before a charge package sounds
  broadly healthy.

Model increment:

- Added `Enemy Pressure Tolerance Panel For charge_turns`.
- Listed fast, multi-enemy, action-punisher, scaling, and defensive-race pressure.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example reviews `fast_pressure` first and maps it to
  `shorten_or_pay_back_setup`.

Judgment rules:

- The panel names review pressure only; it does not simulate encounters or add gates.
- Slow-fight-only success should be recorded as setup or matchup risk before payoff
  ambition increases.

Failure case:

- If the package only works after slow uninterrupted setup, use `matchup_too_narrow`
  or `setup_tax_too_high`.

Next round entry:

- Add one package density balance note so support/payoff order stays visible.

### 2026-04-27 Slice 14

Evaluation/design problem:

- Separate `package_density` from `support_payoff_balance` for `charge_turns`.

Model increment:

- Added `Package Density Balance For charge_turns`.
- Named `role_density`, `support_before_payoff`, `redundancy_without_soup`, and
  `payoff_texture_balance` as balance reads.

Example mechanism/package:

- Continued `delayed_charge_release`.
- The example marks density as partial and fixes the `glue` role first.

Judgment rules:

- More density is not better if it blurs the axis into goodstuff.
- One clear missing role is better than five vague roles.

Failure case:

- If density improves only through generic value, mark `generic_goodstuff`.

Next round entry:

- Add one transfer note for `discard_outlet_count` to verify the lab vocabulary can
  move beyond `charge_turns` without generating formal cards.

### 2026-04-27 Slice 15

Evaluation/design problem:

- Test whether the lab vocabulary transfers from `charge_turns` to another parameter
  while staying report-only and role-level.

Model increment:

- Added `Transfer Note: discard_outlet_count`.
- Defined a minimal `discard_velocity_release` brief with outlet density, payoff
  contact reliability, and discard identity risks.

Example mechanism/package:

- Used `discard_velocity_release` as a role-level transfer example.
- The skeleton names anchor, support, glue, payoff, and safety valve without card text
  or exact outlet counts.

Judgment rules:

- If discard only sees more cards, record `swallowed_by_draw`.
- If discard is only hand cleanup, record `swallowed_by_discard`.
- If outlet density is high but decisions are automatic, record `low_agency_loop`.

Failure case:

- If starter or off-axis cards are assumed away, request `deck_compression_summary`
  before reachability wording.

Next round entry:

- Either choose the first `discard_outlet_count` band comparison or promote stable lab
  rules into a long-term development spec after human review.
