# BBS Social Case Model V1

- Model: `bbs_social_case_model_v1`
- Status: case-backed modeling entrypoint
- Contract: `cardanalysis_case_input_v1`
- Runtime impact: none

## Purpose

This document defines how BBS, social, and gossip cases enter the
`cardanalysis` case library without creating a new runtime, UI, persistence
layer, or prose generator.

The entrypoint exists so future social read-model work can inspect case-backed
signals while preserving source provenance and review boundaries. It is a
modeling surface, not a gossip simulation state contract.

## Scope

In scope:

- normalized BBS/social cases using `cardanalysis_case_input_v1`;
- fixture coverage for reviewed, human-curated, source-mined, and speculative
  social patterns;
- shared semantics for actor, audience, rumor target, relationship edges,
  trigger windows, ambiguity, escalation, payoff horizon, and social texture;
- advisory feature hints for future report-only consumers.

Out of scope:

- runtime wiring;
- `gossip_bbs_social_simulation_model_v1` state mutation;
- campaign lifecycle hook changes;
- UI, persistence, database, or save-schema changes;
- LLM prose or final BBS post text;
- reviewed combat evidence promotion;
- default synthesis or hard-gate decisions.

## Contract Reuse

Use `design_object.object_type = "bbs_social_event"` for concrete gossip,
forum, social, rumor, reveal, meme, or backlash cases.

Use `campaign_event` only when the case is primarily about campaign scheduling
and the social surface is secondary. Use `experience_pattern` only when there is
no concrete social event. The V1 fixture pack uses `bbs_social_event` for every
case so the social modeling intent remains explicit without extending the enum.

## Field Semantics

The shared case contract already has enough room for the social read model
entrypoint. Do not add a parallel schema unless multiple live consumers need
typed fields and the semantics have stabilized.

| Social meaning | Existing field convention |
| --- | --- |
| Actor | `contexts.experience.social_frame.actor_ref` |
| Audience | `contexts.experience.social_frame.audience_refs` |
| Rumor target | `contexts.experience.social_frame.rumor_target_refs` |
| Relationship edges | `contexts.experience.social_frame.relationship_edges` |
| Trigger window | `contexts.campaign.trigger_window` and `feature_hints.timing` |
| Secrecy | `contexts.experience.social_frame.secrecy_level`, `labels.uncertain`, and `feature_hints.agency` |
| Ambiguity | `contexts.experience.social_frame.ambiguity_level`, `labels.uncertain`, and `feature_hints.variance` |
| Escalation | `observed_behavior.setup`, `observed_behavior.failure_modes`, and `feature_hints.flavor_or_social` |
| Short-term payoff | `observed_behavior.payoff` entries prefixed with `short_term:` |
| Long-tail payoff | `observed_behavior.payoff` entries prefixed with `long_tail:` |
| Trust and suspicion | `labels`, `feature_hints.flavor_or_social`, and relationship edge labels |
| Irony and meme spread | `feature_hints.flavor_or_social`, `labels.positive`, and `labels.uncertain` |
| Reveal and backlash | `observed_behavior.failure_modes`, `labels.negative`, and `feature_hints.flavor_or_social` |

These conventions are deliberately text-label based. They are hints for future
case-backed modeling, not final social-state fields.

## Authority Boundary

All cases keep:

```text
authority.authority_boundary = advisory_context_only
```

Reviewed BBS/social cases are reviewed as case-library fixtures. They do not
become reviewed combat evidence, family promotion proof, legality decisions, or
default synthesis input.

Cases below reviewed tier must not claim reviewed authority:

- `human_curated` cases include `reviewed_evidence_claim` in
  `authority.forbidden_uses`;
- `source_mined_reference` cases stay `source_mined` and unreviewed;
- `generated_hypothesis` cases stay `speculative` and hypothesis-only.

Source-mined and generated cases can suggest candidate review questions. They
cannot prove that a social mechanism is real, balanced, fun, or canon-ready.

## Fixture Pack

The V1 fixture pack lives at:

```text
tests/fixtures/combat_analysis/bbs_social_case_library_v1/
```

Coverage:

- reviewed gossip escalation;
- human-curated after-combat return rumor propagation;
- human-curated role linkage and faction reaction;
- human-curated meme or joke spread with low trust;
- human-curated reveal and backlash;
- source-mined public-thread reference;
- generated private-leak hypothesis.

The pack is intentionally small. Its job is to lock the contract mapping and
source boundary before any runtime or read-model work consumes it.

## Consumer Rules

Future consumers may read these cases for:

- social wording context in reports;
- candidate axis surfacing;
- review-question generation;
- uncertainty and source-boundary notes.

Future consumers must not:

- mutate `gossip_bbs_social_simulation_model_v1` state from these cases;
- spawn public threads or posts;
- promote source-mined or generated material to reviewed evidence;
- treat `feature_hints` as final social-state facts;
- change viability hard gates, default synthesis, or recommendation behavior.

## Validation

Validate the fixture pack with:

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/bbs_social_case_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_bbs_social_case_library_v1.py -q
```
