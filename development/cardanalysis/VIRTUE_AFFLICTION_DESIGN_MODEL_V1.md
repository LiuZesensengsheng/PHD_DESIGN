# Virtue Affliction Design Model V1

## Purpose

`virtue_affliction_design_model_v1` is a minimal report-only contract draft for
evaluating stress-threshold designs inspired by Darkest Dungeon 1's virtue and
affliction structure.

It is not a runtime system, not a card generator, not a campaign curve, and not
a hard gate. It only defines how a future advisory report could judge whether a
proposal has the structural properties of a psychological state loop.

This document is intentionally DD1-only. Darkest Dungeon 2 relationship and
affinity systems are useful future contrast material, but they are out of
scope for this model.

## Authority Boundary

- `evaluation_mode`: `report_only`
- `authority_boundary`: `advisory_context_only`
- `hard_gate_impact`: `none`

The model must not:

- design or promote formal cards,
- write runtime data,
- mutate campaign or combat behavior,
- create hard gates,
- alter default generation, learning, synthesis, or reranker paths,
- claim Darkest Dungeon 1 material as reviewed project evidence,
- enter the core exam contract without a separate approved integration task.

## Relationship To `stress_resolve_model_v1`

`stress_resolve_model_v1` is the broader planning head for HP, stress, resolve,
threshold events, recovery, and campaign relation.

`virtue_affliction_design_model_v1` is narrower. It focuses on the branch
structure around a stress threshold:

```text
stress buildup -> threshold drama -> positive break or negative break ->
team contagion/recovery -> long-term consequence
```

This model is implemented as a report-only surface. The live capability graph
contains only the minimal registry-derived capability and report artifact needed
to keep canonical surface coverage valid. It does not register consumers,
feature-projection inputs, default generation, runtime integration, or hard-gate
authority. A future integration may either fold it into `stress_resolve_model_v1`
or add explicit review-gated consumers after review.

The implementation architecture lives in
`VIRTUE_AFFLICTION_ARCHITECTURE_BLUEPRINT_V1.md`. This model document defines
what the evaluator means; the architecture blueprint defines how it should be
layered, validated, and eventually registered if implementation is approved.

## Architecture Decision

### Problem

The DD1 research note explains the stress, virtue, and affliction loop in
design language, but design language alone is too soft for future evaluation.
The project needs a report-only model that can say which parts of a proposed
stress-threshold loop are structurally present, which parts are risky, and how
the model would fit into the existing cardanalysis dependency/conflict graph.

### Constraints

- Learn from DD1 only in this document.
- Keep DD1 material at `source_mined` or `design_reference` status.
- Stay report-only and advisory.
- Do not design formal cards.
- Do not write runtime data.
- Do not create hard gates.
- Do not modify campaign curve, default generation, learning, synthesis, or
  reranker behavior.
- Do not claim reviewed evidence.
- Reuse cardanalysis graph vocabulary instead of inventing a parallel planning
  system.

### Complexity

Essential complexity:

- Stress is a time-evolving state, not a one-shot debuff.
- Threshold drama depends on visible buildup, branch uncertainty, and outcome
  contrast.
- Affliction-like outcomes must represent agency loss and team contagion.
- Virtue-like outcomes must represent reversal value without removing risk.
- Long-term cost must be visible separately from local combat value.

Accidental complexity to avoid:

- copying DD1's exact numbers, names, or gothic framing;
- turning the model into a hard pass/fail gate;
- mixing this branch into card package generation or core exam contracts;
- creating a second governance graph outside the existing cardanalysis graph
  vocabulary.

### Options

| Option | Description | Upside | Downside |
| --- | --- | --- | --- |
| Fold into `stress_resolve_model_v1` immediately | Treat virtue/affliction as a subsection of the existing broader model. | Lowest surface count. | Hides threshold-branch structure and makes the math harder to review independently. |
| Keep a narrow `virtue_affliction_design_model_v1` draft with graph projection | Define the math and graph edges here, then decide later whether implementation folds into stress/resolve or becomes its own node. | Best match for DD1-specific learning and parallel review safety. | Adds one more draft document to maintain. |
| Jump to runtime/card system design | Start mapping the loop into gameplay content. | Fastest path to visible design. | Violates current boundaries and skips model validation. |

### Risks

- The model could become too abstract to guide real design.
- The graph projection could be mistaken for an implemented capability graph
  registration.
- Future agents could copy DD1 values or names as if they were accepted
  project tuning.
- A report could be misread as proof that a stress system is fun, balanced, or
  ready for runtime work.

### Recommendation

Use the second option. Keep the system design and math inside this
`virtue_affliction_design_model_v1` contract, and express future integration in
the cardanalysis graph vocabulary. Keep code, fixtures, and graph coverage
report-only; do not add default entrypoints, consumers, runtime wiring, or
hard-gate authority yet.

The model should become useful before it becomes authoritative: first it should
produce advisory metrics and graph placement, then later it can be folded into
or connected with `stress_resolve_model_v1` after review.

### Counter-Review

The main objection is that a separate draft model may duplicate
`stress_resolve_model_v1`. That is real. The reason to keep it separate for now
is that DD1's most valuable lesson is the threshold branch, not general stress
accounting. If the branch model later collapses into ordinary stress accounting,
it should be merged back into `stress_resolve_model_v1` instead of promoted as a
separate capability.

### Decision Summary

`virtue_affliction_design_model_v1` should be a DD1-only, report-only,
math-backed threshold-branch evaluator. It uses the live cardanalysis graph only
for canonical report-only surface coverage. It should not add consumer edges,
default paths, runtime paths, or hard-gate authority without a later integration
task.

## DD1-Derived System Model

The model treats a party as a set of characters observed over discrete decision
steps.

```text
H = set of characters
i = one character in H
t = decision step
s_i(t) = stress for character i at step t
q_i(t) = resolve state for character i at step t
q_i(t) in {normal, virtue_like, affliction_like, endpoint_risk}
```

DD1 teaches the shape of the loop, not the project's final numbers. Parameters
such as `T_resolve`, `S_max`, and `p_virtue_base` are placeholders. The model
must not copy DD1's exact values by default.

### Stress Transition

```text
s_i(t + 1) =
  clamp(
    s_i(t)
    + enemy_pressure_i(t)
    + environment_pressure_i(t)
    + expedition_pressure_i(t)
    + ally_contagion_i(t)
    - recovery_i(t),
    0,
    S_max
  )
```

Where:

- `enemy_pressure_i(t)` covers direct stress attacks, critical events, and
  combat tempo pressure.
- `environment_pressure_i(t)` covers darkness, traps, hunger, supplies, and
  route friction.
- `expedition_pressure_i(t)` covers retreat, ally death, prolonged fights, and
  accumulated risk.
- `ally_contagion_i(t)` covers stress emitted by allies in an
  affliction-like state.
- `recovery_i(t)` covers skills, camping, town recovery, positive events, and
  virtue-like relief.

The key DD1 lesson is that stress buildup should be multi-source and partially
answerable. A single hidden random spike is a bad fit for this model.

### Threshold Event

```text
if q_i(t) == normal and s_i(t) >= T_resolve:
  q_i(t + 1) = virtue_like with probability p_virtue_i(t)
  q_i(t + 1) = affliction_like with probability 1 - p_virtue_i(t)
```

The branch probability is modeled as:

```text
p_virtue_i(t) =
  clamp_probability(
    p_virtue_base
    + trait_modifier_i
    + item_modifier_i
    + context_modifier_i(t)
    + history_modifier_i(t)
  )
```

This is not an implementation requirement. It is a design-analysis shape: the
report should identify which inputs would plausibly affect the branch and which
ones would make the branch feel arbitrary.

### Affliction-Like State

Affliction-like outcomes change behavior reliability and produce team stress.

```text
command_reliability_i(t) =
  base_reliability_i - agency_loss_i(q_i, context_t)

ally_contagion_k(t) +=
  contagion_weight_i_to_k * affliction_emission_i(t)
```

The report should separate three costs:

- `local_cost`: reduced stats, bad moves, refusal, self-damage, or missed
  opportunities.
- `team_cost`: stress emitted to allies, formation disruption, healing refusal,
  or shared resource disruption.
- `future_cost`: recovery time, roster downtime, identity memory, or endpoint
  risk.

### Virtue-Like State

Virtue-like outcomes convert threshold pressure into reversal value.

```text
s_i(t + 1) -= virtue_self_relief_i
s_k(t + 1) -= virtue_party_relief_i_to_k
reversal_value_i(t) =
  local_buff_value_i
  + team_stabilization_value_i
  + continuation_option_value_i
```

The report should not treat positive break as a generic buff. It should ask
whether the state:

- arrives at a visible crisis point,
- stabilizes the party,
- creates a credible continue-or-retreat decision,
- preserves future risk.

### Endpoint Risk

DD1 has a second stress endpoint after the 100 stress resolve check. This model
keeps the concept but does not copy the exact death/heart-attack behavior.

```text
endpoint_risk_i(t) =
  probability(s_i reaches S_max within horizon H | q_i, current party state)
```

The project-facing design question is not "should we copy heart attacks?" The
question is whether an unresolved negative state has a visible escalation path
and a recovery window before that escalation becomes severe.

## Metric Layer

The model should report qualitative labels, but the labels should be backed by
explicit metric definitions. These metrics are advisory and must not become
hard gates.

| Metric | Sketch | Reads As |
| --- | --- | --- |
| `stress_growth_rate` | `E[max(0, s_i(t + 1) - s_i(t))]` | How quickly pressure builds. |
| `time_to_threshold` | `min t where s_i(t) >= T_resolve` | Whether players can see crisis coming. |
| `branch_entropy` | uncertainty of virtue-like vs affliction-like split | Whether the threshold is suspenseful. |
| `outcome_contrast` | distance between positive and negative branch consequences | Whether the branch matters. |
| `threshold_drama_score` | visibility * branch_entropy * outcome_contrast * lead_time | Whether the threshold creates drama. |
| `positive_break_value` | expected value of virtue-like branch over baseline | Whether reversal is meaningful. |
| `negative_break_cost` | expected value lost under affliction-like branch | Whether failure has teeth. |
| `stress_contagion_rate` | expected stress emitted to allies per afflicted step | Whether one break can pressure the team. |
| `cascade_reproduction` | expected extra threshold crossings caused by one negative break over horizon H | Whether the system can spiral. |
| `agency_preservation` | prevention + mitigation + triage + recovery choices, adjusted by command reliability loss | Whether decisions still matter. |
| `long_term_cost` | recovery resource cost + downtime + persistent identity or risk debt | Whether consequences survive one fight. |

The most important anti-spike metric is `agency_preservation`. A stressful
system can be punishing, but it should not make the player feel the optimal
choice disappeared before the threshold.

## Decision EV Layer

The model can compare high-level player options without designing final cards.

```text
EV_continue =
  quest_reward
  + p_virtue * positive_break_value
  - p_affliction * negative_break_cost
  - cascade_risk
  - long_term_cost

EV_retreat =
  saved_roster_value
  - retreat_penalty
  - abandoned_reward
  - residual_recovery_cost

EV_recover_now =
  preserved_future_value
  - action_tempo_cost
  - resource_cost
  - enemy_pressure_from_delay
```

The threshold is healthy when multiple options can be rational in different
contexts. If one option always dominates, the loop becomes either a tax or a
trap rather than a dramatic decision.

## Graph Projection

The live cardanalysis capability graph is a multi-relation graph, not a single
DAG. This model should use the same planning semantics.

### Partial Order View

This is the preferred conceptual order:

```text
dd1_source_reference
-> dd1_stress_virtue_affliction_research_v1
-> normalized_design_case
-> virtue_affliction_feature_projection
-> virtue_affliction_design_model_v1
-> virtue_affliction_design_report
-> human_design_review
```

This order is not authority promotion. It only describes how source material
can become advisory review context while preserving provenance.

### Proposed Future Nodes

| Node Id | Kind | Status | Trust Tier | Notes |
| --- | --- | --- | --- | --- |
| `dd1_stress_virtue_affliction_research_v1` | artifact | draft | source_mined | The DD1-only research report. |
| `virtue_affliction_design_model_v1` | capability | draft | report_only | Live only as canonical report-only surface coverage. |
| `virtue_affliction_feature_projection` | artifact | draft | report_only | Optional future projection from normalized cases into metrics. |
| `virtue_affliction_design_report` | artifact | draft | report_only | Live human-readable advisory output artifact. |
| `decision_dd1_values_not_project_tuning` | decision | draft | decision_frozen after review | Prevents copying DD1 numbers or labels as defaults. |

### Proposed Future Edges

| Source | Relation | Target | Reason |
| --- | --- | --- | --- |
| `virtue_affliction_design_model_v1` | `depends_on` | `decision_report_only_surfaces_not_authoritative` | Live edge that keeps report-only output advisory. |
| `virtue_affliction_design_model_v1` | `depends_on` | `dd1_stress_virtue_affliction_research_v1` | Uses DD1-only structure as source-mined/design-reference input. |
| `virtue_affliction_design_model_v1` | `depends_on` | `decision_dd1_values_not_project_tuning` | Prevents copying DD1 thresholds, probabilities, and labels. |
| `virtue_affliction_design_model_v1` | `optional_depends_on` | `stress_resolve_summary` | Useful context if the model is folded into stress/resolve. |
| `virtue_affliction_design_model_v1` | `consumes` | `normalized_design_case` | Future only, if normalized cases are wired. |
| `virtue_affliction_design_model_v1` | `consumes` | `virtue_affliction_feature_projection` | Future only, if metric projection is wired. |
| `virtue_affliction_design_model_v1` | `provides` | `virtue_affliction_design_report` | Live advisory report output. |
| `virtue_affliction_design_model_v1` | `review_gated_with` | `stress_resolve_model_v1` | Future edge if consumer or ownership overlap is added. |
| `virtue_affliction_design_model_v1` | `review_gated_with` | `campaign_power_curve_report_v1` | Required only if future reports discuss campaign pacing. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `default_synthesis_path` | Hard conflict if anyone uses the report to drive default generation. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `runtime_data_generation` | Hard conflict if anyone turns the report into runtime payloads. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `hard_gate_promotion` | Hard conflict if anyone treats the report as pass/fail authority. |

The future consumer, review-gated, and conflict targets above are conceptual
guardrail targets unless later registered as graph edges or nodes. The current
live graph only records canonical report-only surface coverage and advisory
authority dependencies.

## Minimal Evaluator Algorithm

If implemented later, the evaluator should:

1. Load a case or report-only model input.
2. Reject DD1-derived inputs that claim `reviewed` status.
3. Check the authority boundary is `advisory_context_only`.
4. Extract stress sources, recovery sources, threshold branch, positive break,
   negative break, contagion, and long-term consequence.
5. Compute or estimate the metric layer.
6. Emit qualitative findings for required dimensions.
7. Emit transferability notes: `transferable`, `adapt_with_caution`,
   `do_not_copy`.
8. Emit forbidden downstream uses.
9. Avoid `overall_pass`, `hard_gates`, formal card text, runtime payloads, and
   default generation hints.

## Source Status Rules

Inputs that reference Darkest Dungeon 1 must use one of:

- `source_mined`
- `design_reference`

They must not use `reviewed` unless a later project review explicitly promotes
that material.

Recommended forbidden uses for DD1-derived input:

- `hard_gate_promotion`
- `runtime_data_generation`
- `formal_card_design`
- `default_synthesis_path`
- `learned_or_reranker_default`
- `reviewed_evidence_claim`

## Draft Input Shape

The contract is JSON-safe plain data if later implemented. The shape below is a
documentation draft, not runtime data.

```json
{
  "schema_version": "virtue_affliction_design_model_v1",
  "case_id": "short_unique_id",
  "title": "Readable case title",
  "source": {
    "source_type": "design_reference",
    "source_name": "human-readable source",
    "evidence_tier": "source_mined",
    "review_status": "not_reviewed",
    "reference_family": "darkest_dungeon_1",
    "source_url": null
  },
  "design_scope": {
    "object_type": "stress_threshold_loop",
    "project_area": "report_only_cardanalysis",
    "intended_use": "advisory_design_review"
  },
  "stress_track": {
    "buildup_sources": [],
    "visibility": "visible_meter",
    "mitigation_choices": [],
    "persistence": "encounter_and_roster_context"
  },
  "threshold_event": {
    "trigger": "stress_threshold",
    "presentation": [],
    "branching_model": "positive_negative_split",
    "known_probabilities": null
  },
  "model_parameters": {
    "stress_cap": null,
    "resolve_threshold": null,
    "time_horizon": null,
    "virtue_base_probability": null,
    "affliction_base_probability": null,
    "contagion_weights": {},
    "agency_loss_weight": null,
    "long_term_cost_weight": null
  },
  "positive_break": {
    "state_name": null,
    "agency_change": null,
    "party_effects": [],
    "recovery_or_reversal_effects": [],
    "risk_reward_role": null
  },
  "negative_break": {
    "state_name": null,
    "agency_change": null,
    "team_contagion_effects": [],
    "failure_escalation": [],
    "recovery_requirements": []
  },
  "long_term_consequence": {
    "roster_costs": [],
    "memory_or_identity": [],
    "future_run_pressure": []
  },
  "authority": {
    "authority_boundary": "advisory_context_only",
    "forbidden_uses": []
  }
}
```

## Draft Output Shape

```json
{
  "schema_version": "virtue_affliction_design_model_v1_report",
  "evaluation_mode": "report_only",
  "authority_boundary": "advisory_context_only",
  "case_id": "short_unique_id",
  "metric_findings": [],
  "dimension_findings": [],
  "transferability": {
    "transferable": [],
    "adapt_with_caution": [],
    "do_not_copy": []
  },
  "decision_notes": [],
  "open_questions": [],
  "forbidden_downstream_uses": []
}
```

## Required Dimensions

Each report should evaluate these dimensions independently. V1 should prefer
qualitative labels such as `strong`, `mixed`, `weak`, `unsafe`, and `unknown`
over numeric authority.

| Dimension | Minimum Finding |
| --- | --- |
| `stress_buildup` | Identify pressure sources, visibility, mitigation, and whether buildup is earned. |
| `threshold_drama` | Judge whether the threshold creates anticipation and a meaningful branch event. |
| `positive_break` | Judge whether virtue-like outcomes create reversal, relief, identity, and risk reward. |
| `negative_break` | Judge whether affliction-like outcomes create real disruption without pure helplessness. |
| `team_contagion` | Identify how one state can affect allies or shared resources. |
| `long_term_consequence` | Identify carryover, recovery cost, memory, or roster-planning impact. |
| `agency_preservation` | Judge whether players have prevention, mitigation, triage, and recovery choices. |

Recommended optional dimensions:

- `recovery_window`
- `state_identity`
- `risk_reward_tuning`
- `anti_debuff_depth`
- `presentation_readability`
- `authority_safety`

## Positive Pattern Labels

- `visible_pressure_clock`
- `earned_threshold_event`
- `asymmetric_branch_with_real_upside`
- `affliction_as_behavior_mode`
- `virtue_as_reversal_moment`
- `recoverable_team_contagion`
- `long_tail_roster_cost`
- `state_memory_identity`

## Counterexample Labels

- `hidden_random_debuff`
- `stat_only_break`
- `no_counterplay_spiral`
- `overfarmable_positive_break`
- `agency_erasure`
- `grind_only_recovery_tax`
- `direct_dd1_label_copy`
- `authority_boundary_violation`

## Minimum Review Checklist

Before using this model in any future report, verify:

1. Does the input label source status and avoid reviewed-evidence claims?
2. Does the report stay advisory and report-only?
3. Does it avoid formal card text, runtime data, and hard gates?
4. Does it separate DD1 learning from project-specific design decisions?
5. Does it evaluate both positive and negative break branches?
6. Does it preserve player agency as a first-class dimension?
7. Does it identify what should not be copied?

## Validation Policy

Current focused validation:

```powershell
git diff --check
py -3.11 -m pytest tests/toolkit/combat_analysis/test_virtue_affliction_design_model_v1.py tests/scripts/test_run_virtue_affliction_design_model.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
```

If future work adds capability graph entries or default entrypoints, run the
corresponding graph/entrypoint validation from
`CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`.
