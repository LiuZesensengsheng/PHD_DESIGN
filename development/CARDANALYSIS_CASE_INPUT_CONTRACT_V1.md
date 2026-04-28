# Cardanalysis Case Input Contract V1

## Purpose

Define the minimum shared input contract for future `cardanalysis` case-backed
work.

This contract is an anti-corruption layer. It lets the project collect cases
from reviewed fixtures, playtest observations, design notes, source-mined game
references, and speculative hypotheses without forcing every downstream
evaluator to understand every source format.

## Scope

In scope:

- new case-like evidence for mechanism, package, campaign, encounter, stress,
  resolve, BBS/social, and experience modeling;
- low-cost normalization before feature projection;
- provenance, uncertainty, and allowed-consumer metadata;
- gradual migration from existing fixtures where useful.

Out of scope:

- replacing focused evaluator fixture schemas;
- replacing hard-gate benchmark contracts;
- making source-mined references equivalent to reviewed evidence;
- defining every possible future metric in V1;
- training a learned model directly from raw source text.

## Contract Shape

The canonical V1 shape is JSON-safe plain data.

```json
{
  "schema_version": "cardanalysis_case_input_v1",
  "case_id": "unique_case_id",
  "title": "Short readable title",
  "summary": "One or two sentences describing the observed design pattern.",
  "source": {
    "source_type": "reviewed_fixture",
    "source_name": "human-readable source or fixture pack",
    "game_reference": "optional source game or project area",
    "evidence_tier": "reviewed",
    "review_status": "accepted",
    "source_url": null
  },
  "design_object": {
    "object_type": "mechanism",
    "primary_axis": "optional primary axis id",
    "secondary_axes": [],
    "object_refs": []
  },
  "contexts": {
    "combat": {},
    "deck_or_package": {},
    "campaign": {},
    "experience": {}
  },
  "observed_behavior": {
    "setup": [],
    "payoff": [],
    "failure_modes": [],
    "counterplay_or_constraints": []
  },
  "labels": {
    "positive": [],
    "negative": [],
    "uncertain": []
  },
  "feature_hints": {
    "mechanism": [],
    "resource": [],
    "timing": [],
    "agency": [],
    "variance": [],
    "compression": [],
    "campaign": [],
    "flavor_or_social": []
  },
  "known_limits": [],
  "authority": {
    "authority_boundary": "advisory_context_only",
    "allowed_consumers": [],
    "forbidden_uses": []
  }
}
```

## Required Fields

Required for all V1 normalized cases:

- `schema_version`
- `case_id`
- `title`
- `summary`
- `source.source_type`
- `source.evidence_tier`
- `source.review_status`
- `design_object.object_type`
- `observed_behavior`
- `labels`
- `authority.authority_boundary`

Optional fields should stay present as empty containers when a case family does
not need them yet. This keeps downstream normalization deterministic.

## Source Types

Allowed V1 source types:

- `reviewed_fixture`
- `playtest_observation`
- `design_note`
- `source_mined_reference`
- `generated_hypothesis`

`source_mined_reference` and `generated_hypothesis` are not reviewed evidence.
They can be used for exploration and candidate discovery, but they must not be
used as hard-gate proof.

## Evidence Tiers

Allowed V1 evidence tiers:

- `reviewed`
- `human_curated`
- `source_mined`
- `speculative`

Promotion rule:

```text
source_mined/speculative -> human_curated -> reviewed
```

Promotion requires explicit review. It must not happen just because a case is
used by a downstream model.

## Design Object Types

Allowed V1 object types:

- `mechanism`
- `card`
- `card_package`
- `deck_archetype`
- `encounter`
- `campaign_phase`
- `campaign_event`
- `stress_resolve_model`
- `bbs_social_event`
- `experience_pattern`

New object types should be added only when repeated cases cannot be expressed
with these values without losing important meaning.

## Feature Hints

`feature_hints` are not final model features. They are lightweight labels that
help feature-projection code and later model heads bootstrap without requiring
large rule stacks.

Prefer adding a label first. Promote a label to a typed field only when:

1. multiple consumers need it,
2. it has stable semantics,
3. tests can lock the interpretation.

## Authority And Consumers

`authority.authority_boundary` must default to:

```text
advisory_context_only
```

`allowed_consumers` should name the capability heads or applications that may
read the case. Examples:

- `mechanism_axis_discovery_v1`
- `mechanism_fun_health_v1`
- `card_package_health_v1`
- `campaign_power_curve_report_v1`
- `evaluation_autonomous_design_model_v1`

`forbidden_uses` should name unsafe uses. Examples:

- `hard_gate_promotion`
- `legality_decision`
- `default_synthesis_path`
- `reviewed_evidence_claim`

## Existing Asset Compatibility

Existing evaluator fixtures do not need immediate migration.

Recommended compatibility path:

1. keep current focused fixture schemas where they already work,
2. add adapters only when a downstream shared capability needs normalized cases,
3. export normalized cases next to existing fixtures rather than rewriting the
   original pack,
4. preserve reviewed fixture ownership and expected verdict semantics.

## Feature Projection Payload

Feature projection is the next layer after normalized cases.

V1 only defines the artifact boundary:

```json
{
  "schema_version": "cardanalysis_feature_projection_v1",
  "case_id": "unique_case_id",
  "projection_mode": "report_only",
  "features": {},
  "source_trace": {},
  "authority_boundary": "advisory_context_only"
}
```

The payload is intentionally open. Each future feature projector may own a
narrow subset, but the authority boundary and source trace must remain visible.

## Conflict Boundaries

The case input contract conflicts with work that:

- changes normalized case meaning from a single downstream evaluator,
- treats source-mined evidence as reviewed,
- removes provenance or uncertainty fields,
- changes `authority_boundary` away from `advisory_context_only`,
- lets generated hypotheses become default synthesis or hard-gate input.

## Minimum Review Checklist

Before a new case family uses this contract, check:

1. Does it preserve source provenance?
2. Does it state reviewed vs source-mined vs speculative status?
3. Does it avoid claiming hard authority?
4. Does it name allowed consumers?
5. Does it keep source-specific weirdness behind the case-normalization layer?
6. Does it add labels before adding new typed fields?

## Suggested First Consumers

Good first consumers are:

- mechanism-axis discovery,
- campaign pressure/stress exploration,
- mechanism fun/health fixture expansion,
- card package health fixture expansion,
- BBS/social read-model exploration.

These consumers can benefit from normalized cases without forcing existing
reviewed benchmark packs to migrate immediately.
