# Source Followup Case Library V1

- Library: `source_followup_case_library_v1`
- Contract: `cardanalysis_case_input_v1`
- Status: bootstrap case library for blocked source followups
- Runtime impact: none

## Purpose

This library gives source-mined and generated followup items a safe review
exit. It turns queue targets into human-curated review notes without promoting
the source material to reviewed evidence.

The library is intentionally narrow. It records what a reviewer should inspect
next, which assumptions remain unresolved, and which consumers may use the case
as advisory context. It does not decide whether the original hypothesis is true,
balanced, viable, or ready for family promotion.

## Source Targets

The V1 bootstrap handles the current `source_followup` items emitted by
`coverage_guided_case_queue_v1`:

- `generated_chain_fatigue_hypothesis_case_v1`
- `generated_hypothesis_private_leak_case_v1`
- `generated_loop_safety_break_hypothesis_case_v1`
- `generated_pollution_market_hypothesis_case_v1`

The long-running case-library lane also adds followup review notes for:

- `generated_defense_reflect_hypothesis_case_v1`
- `generated_draw_heat_budget_hypothesis_case_v1`
- `generated_energy_instability_hypothesis_case_v1`
- `generated_recovery_window_validator_enemy_case_v1`
- `generated_redirect_collision_hypothesis_case_v1`
- `generated_search_public_target_hypothesis_case_v1`
- `generated_summon_expiry_hypothesis_case_v1`
- `source_mined_anti_infinite_soft_pressure_enemy_case_v1`
- `source_mined_draw_disruption_enemy_case_v1`
- `source_mined_charge_decay_reference_case_v1`

Each followup case stores the original target id and queue id under
`contexts.campaign` and `contexts.experience.source_followup`.

## Contract Use

The fixture pack continues to use the shared normalized case contract:

- `source.source_type = "design_note"`
- `source.evidence_tier = "human_curated"`
- `source.review_status = "review_needed"`
- `authority.authority_boundary = "advisory_context_only"`

The followup cases use existing fields only:

| Followup meaning | Existing field convention |
| --- | --- |
| Original queue item | `contexts.campaign.queue_id` |
| Original source case | `contexts.campaign.target_case_id` and `contexts.experience.source_followup.target_case_id` |
| Review plan | `contexts.experience.source_followup.review_questions` |
| Evidence still needed | `contexts.experience.source_followup.human_curated_evidence_needed` |
| Review risk | `observed_behavior.failure_modes`, `labels.negative`, and `labels.uncertain` |
| Candidate hints | `feature_hints` |
| Authority limits | `known_limits` and `authority.forbidden_uses` |

These are review-note conventions inside the shared contract, not a second
schema.

## Authority Boundary

All V1 cases remain below reviewed authority.

They must not be used for:

- reviewed evidence claims;
- hard-gate promotion;
- reviewed mechanism-family promotion;
- default synthesis or recommendation;
- evaluator logic changes;
- capability graph or report-only registry changes;
- runtime, persistence, UI, or learned/reranker paths.

The fixture pack therefore includes `reviewed_evidence_claim` in
`authority.forbidden_uses` even though its immediate source type is
`design_note`. This preserves the boundary that the underlying target cases are
generated hypotheses.

## Fixture Pack

The V1 fixture pack lives at:

```text
tests/fixtures/combat_analysis/source_followup_case_library_v1/
```

Coverage:

- chain fatigue followup review note;
- private leak followup review note;
- loop safety break followup review note;
- pollution market followup review note.
- defense reflect followup review note;
- draw heat budget followup review note;
- energy instability followup review note;
- recovery window validator followup review note;
- redirect collision followup review note;
- search public target followup review note;
- summon expiry followup review note;
- anti-infinite soft pressure followup review note;
- draw disruption enemy followup review note;
- charge decay reference followup review note.

The cases may help report-only scanners, feature projection, and advisory
discovery surfaces ask better next-review questions. They do not create
reviewed evidence.

## Validation

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/source_followup_case_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_source_followup_case_library_v1.py -q
```
