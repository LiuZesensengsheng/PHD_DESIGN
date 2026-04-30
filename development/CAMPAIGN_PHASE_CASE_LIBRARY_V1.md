# Campaign Phase Case Library V1

## Purpose

`campaign_phase_case_library_v1` is a normalized case fixture library for
campaign phase experience. It exists to give downstream report-only heads
case-backed starter and pivot context without wiring a new consumer, graph node,
runtime system, hard gate, or synthesis path.

This bootstrap follows the current coverage-guided queue item:

- `queue_campaign_phase_starter_v1`
- target: `starter`
- suggested fixture:
  `tests/fixtures/combat_analysis/campaign_phase_case_library_v1/campaign_phase_cases_v1.json`

## Scope

In scope:

- normalized `cardanalysis_case_input_v1` cases;
- starter phase pressure, recovery, growth, agency, and enemy-pressure context;
- a small pivot contrast set for future expansion;
- focused tests that lock authority and source-review boundaries.

Out of scope:

- consumer wiring;
- capability graph registration;
- report-only surface registry changes;
- evaluator or report-head behavior;
- campaign runtime, encounter runtime, monster stats, hard gates, default
  synthesis, learned, or reranker paths.

## Fixture Layout

The initial fixture pack contains 8 cases:

| Phase | Count | Role |
| --- | ---: | --- |
| `starter` | 6 | Primary queue target; covers opening pressure, first reward comprehension, recovery visibility, basic-axis teaching, enemy-pressure baseline, and route-agency reference. |
| `pivot` | 2 | Adjacent contrast only; covers route disruption and recovery-versus-greed. |

Tier distribution:

| Evidence Tier | Count |
| --- | ---: |
| `reviewed` | 4 |
| `human_curated` | 3 |
| `source_mined` | 1 |

The source-mined route-agency case is intentionally below reviewed authority. It
must preserve `reviewed_evidence_claim` in `authority.forbidden_uses` until a
future human review promotes or rejects it.

## Authority Boundary

Every case keeps:

```text
schema_version = cardanalysis_case_input_v1
authority.authority_boundary = advisory_context_only
```

Recommended allowed consumers:

- `campaign_experience_curve_v1`
- `campaign_power_curve_report_v1`
- `campaign_advisory_bundle_v1`
- `evaluation_autonomous_design_model_v1`
- `cardanalysis_feature_projection_v1`

Forbidden uses include:

- `hard_gate_promotion`
- `legality_decision`
- `default_synthesis_path`
- `runtime_campaign_authority`
- `monster_stat_tuning_authority`
- `reviewed_evidence_claim` for non-reviewed cases

The library is advisory context only. Feature projection may carry labels from
these cases, but those labels are not reviewed evidence or pass/fail authority.

## Why This Is Not Registered In The Graph Yet

This branch only adds a fixture library, documentation, and focused tests. No
implemented consumer reads `campaign_phase_case_library_v1` as a canonical input
surface yet, and no artifact ownership needs to be assigned. Registering it now
would imply an implemented graph relationship that does not exist.

MasterAgent can consider graph registration later after a real consumer starts
reading this fixture pack or an aggregate campaign phase artifact is introduced.

## Schema Pressure / Future Gaps

The current schema can express the phase cases using existing `contexts`,
`feature_hints`, `known_limits`, and `authority` fields. No schema change is
needed for V1.

Future gaps to watch:

- typed phase windows beyond text `round_hint`;
- typed relationship between campaign phase and enemy archetype case packs;
- typed recovery-window cost and payoff vocabulary;
- reviewed promotion workflow for source-mined route-agency references.

These are recorded as future pressure only. They are not requests to edit
`case_input_contract.py` in this branch.

## Validation

```powershell
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/campaign_phase_case_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_phase_case_library_v1.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_case_input_contract_v1.py tests/scripts/test_validate_cardanalysis_case_input.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
python scripts/validate_capability_graph.py
git diff --check
```
