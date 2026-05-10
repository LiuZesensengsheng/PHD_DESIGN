# Virtue Affliction Design Model V1

## Purpose

`virtue_affliction_design_model_v1` is a minimal report-only contract draft for
evaluating stress-threshold designs inspired by Darkest Dungeon 1's virtue and
affliction structure.

It is not a runtime system, not a card generator, not a campaign curve, and not
a hard gate. It only defines how a future advisory report could judge whether a
proposal has the structural properties of a psychological state loop.

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

This draft does not register a new capability graph node. A future integration
may either fold it into `stress_resolve_model_v1` or register it as a separate
report-only capability after review.

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

For this docs-only draft:

```powershell
git diff --check
py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q
```

If future work adds scripts, fixtures, capability graph entries, or default
entrypoints, run the corresponding owning tests and graph/entrypoint validation
from `CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`.

