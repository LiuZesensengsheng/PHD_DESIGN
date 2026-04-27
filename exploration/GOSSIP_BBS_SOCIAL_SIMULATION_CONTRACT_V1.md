# Gossip BBS Social Simulation Contract V1

- Model: `gossip_bbs_social_simulation_model_v1`
- Status: schema-pass draft extracted from exploration rounds
- Source lab: `docs/exploration/GOSSIP_BBS_SOCIAL_SIMULATION_LAB.md`
- Date: `2026-04-27`

## Purpose

This contract compresses the current Gossip/BBS Social Simulation Lab into a
stable implementation target.

It defines the structured inputs, state records, transition results, and
guardrails for a future domain-only simulation layer.

It does not define:

- UI
- generated BBS prose
- LLM calls
- database persistence
- `cardanalysis` evaluation
- campaign save schema migration

## Type Conventions

- IDs are stable strings.
- `turn` is an integer campaign/combat timeline tick supplied by the caller.
- Scores are floats in `[0.0, 1.0]`.
- Deltas are floats in `[-1.0, 1.0]`.
- Enum-like strings use lower snake case.
- `schema_version` belongs on stored state and future fixtures; upstream event
  envelopes may omit it until code-level fixture loading exists.
- Unknown optional references should be omitted or represented by explicit
  `"unknown"` values, not inferred.
- Text fields in this contract are labels, statuses, or refs. They are not final
  forum copy.

## Event Input Envelope

All upstream events should normalize into this shape before simulation:

```json
{
  "event_id": "evt_unique_id",
  "event_type": "public_achievement",
  "turn": 23,
  "visibility": "public_after_combat",
  "source_actor": "combat_result_feed",
  "target_refs": ["player"],
  "evidence": {},
  "faction_refs": []
}
```

Required fields:

| Field | Type | Rule |
| --- | --- | --- |
| `event_id` | string | Unique upstream fact id. |
| `event_type` | enum | One of the event types below. |
| `turn` | int | Logical turn when the fact becomes visible. |
| `visibility` | enum | Controls topic creation and privacy rules. |
| `source_actor` | string | Actor, system feed, moderator feed, or anonymous source id. |
| `target_refs` | list[string] | Referenced actors, factions, topics, rumors, threads, memories, packages, or prior events. |
| `evidence` | object | Event-specific structured evidence. |
| `faction_refs` | list[string] | Optional factions relevant to stance or alignment drift. |

Supported `event_type` values:

- `combat_result`
- `boss_defeated`
- `player_used_unusual_deck`
- `new_card_package_seen`
- `npc_conflict`
- `faction_event`
- `scandal`
- `misunderstanding`
- `rumor_seeded`
- `rumor_debunked`
- `public_achievement`
- `private_leak`

Supported `visibility` values:

- `private_only`
- `partial_public_claim`
- `public_bbs`
- `public_after_combat`
- `public_thread_update`
- `public_thread_reply`
- `moderator_visible`

`private_only` events must not spawn a public thread directly.
`public_thread_update` and `public_thread_reply` are public visibility values
that should attach to an existing thread when possible before spawning a new
one.

## Transition Input Envelope

Internal model transitions that are not upstream events use this shape:

```json
{
  "transition_id": "tick_unique_id",
  "transition_type": "decay",
  "turn": 40,
  "turn_start": 35,
  "turn_end": 39,
  "target_refs": ["bbs_thread_id"],
  "actors": ["actor_id"],
  "inputs": {}
}
```

Supported `transition_type` values:

- `decay`
- `reply_pressure`

## State Store Draft

The first implementation should use an in-memory, serializable state object.
Do not add a database in V1.

```json
{
  "schema_version": "gossip_bbs_social_simulation_model_v1",
  "events": {},
  "topics": {},
  "threads": {},
  "posts": {},
  "replies": {},
  "rumors": {},
  "actors": {},
  "factions": {},
  "relationships": {},
  "memories": {},
  "moderation_boundaries": {},
  "packages": {},
  "conflicts": {},
  "leaks": {},
  "scandals": {},
  "milestones": {}
}
```

Only the fields required by a tested transition need to exist in code. Unknown
specialized records should not be invented until a fixture requires them.
This state store is a domain-side cache, not a campaign save schema.

## Schema Coverage Checklist

| Required entity | Contract owner |
| --- | --- |
| `actor` | `ActorState` |
| `faction` | `FactionState` |
| `relationship_edge` | `RelationshipEdge` |
| `event` | `Event Input Envelope` |
| `topic` | `TopicState` |
| `rumor` | `RumorState` |
| `post` | `PostState` |
| `reply` | `ReplyState` |
| `thread` | `ThreadState` |
| `stance` | `stance_distribution` and per-post/per-reply `stance` |
| `credibility` | `rumor_credibility`, `credibility_signal`, and evidence fields |
| `heat` | `topic_heat`, `heat`, `heat_contribution`, and `heat_delta` |
| `memory` | `MemoryState` |
| `decay` | `decay` transition contract |
| `moderation_boundary` | `ModerationBoundary` |

## Core Records

### `TopicState`

```json
{
  "topic_id": "topic_id",
  "topic_kind": "performance|rumor|theorycraft|prestige|faction|scandal|conflict|leak|milestone|package",
  "source_event_ids": [],
  "thread_ids": [],
  "topic_heat": 0.0,
  "public_sentiment": 0.0,
  "memory_refs": [],
  "status": "active"
}
```

Stable `topic_kind` values:

- `performance`
- `rumor`
- `theorycraft`
- `prestige`
- `faction`
- `scandal`
- `conflict`
- `leak`
- `milestone`
- `package`

### `ActorState`

```json
{
  "actor_id": "actor_id",
  "actor_kind": "player|npc|faction_account|system_feed|moderator|anonymous",
  "faction_refs": [],
  "memory_refs": [],
  "actor_interest": 0.0,
  "actor_bias": 0.0,
  "reply_threshold": 0.0,
  "social_risk": 0.0
}
```

Actor fields are priors for reply and stance decisions. They must not generate
posts without an event or transition.

### `ThreadState`

```json
{
  "thread_id": "thread_id",
  "parent_thread_id": null,
  "topic_id": "topic_id",
  "source_event_ids": [],
  "status": "active",
  "opened_turn": 0,
  "updated_turn": 0,
  "thread_lifetime": 0,
  "topic_heat": 0.0,
  "reply_pressure": 0.0,
  "public_sentiment": 0.0,
  "moderation_boundary": {}
}
```

Stable `ThreadState.status` values from exploration:

- `active`
- `cooling_after_correction`
- `briefly_reactivated_by_misunderstanding`
- `converted_to_theorycraft`
- `prestige_reactivation`
- `faction_claim_contested`
- `relationship_conflict_active`
- `rumor_containment_needed`
- `leak_quarantined`
- `scandal_lockdown`
- `limited_performance_reopen`
- `new_milestone_thread`
- `debunk_backfire_discussion`
- `archived_with_correction_pin`
- `slow_decay_active`
- `low_activity_observed`

### `PostState`

```json
{
  "post_id": "post_id",
  "thread_id": "thread_id",
  "author_ref": "actor_id",
  "source_event_ids": [],
  "turn": 0,
  "role": "thread_opener",
  "stance": "skepticism",
  "credibility_signal": 0.0,
  "heat_contribution": 0.0,
  "moderation_boundary": {}
}
```

`PostState` stores structured role and stance only. It must not store final BBS
copy.

### `ReplyState`

```json
{
  "reply_id": "reply_id",
  "thread_id": "thread_id",
  "parent_post_id": "post_id",
  "parent_reply_id": null,
  "author_ref": "actor_id",
  "turn": 0,
  "role": "supportive_witness",
  "stance": "support",
  "reply_pressure_delta": 0.0,
  "relationship_delta_refs": [],
  "moderation_boundary": {}
}
```

`ReplyState` may point at either a post or a reply. It is still structured
state, not prose.

### `RumorState`

```json
{
  "rumor_id": "rumor_id",
  "topic_id": "topic_id",
  "claim_type": "mechanism_misread",
  "source_actor": "actor_id",
  "target_refs": [],
  "rumor_credibility": 0.0,
  "heat": 0.0,
  "source_clarity": 0.0,
  "claim_specificity": 0.0,
  "evidence_gap": 0.0,
  "spread_velocity": 0.0,
  "debunk_status": "unresolved",
  "rumor_truth_status": "unresolved"
}
```

Stable `debunk_status` values:

- `unresolved`
- `not_debunked`
- `debunked`
- `debunked_with_visible_evidence`
- `debunked_but_repeated_by_mistake`
- `debunked_with_backfire`
- `superseded_by_public_package_evidence`
- `suppressed_by_public_success_memory`
- `background_corrected_memory`

New fixtures should prefer `unresolved` over `not_debunked`; `not_debunked`
exists to keep the first exploration example readable.

`rumor_truth_status` must remain separate from heat and credibility. Allowed
values:

- `unresolved`
- `false`
- `partially_supported`
- `true`
- `not_applicable`

### `MemoryState`

```json
{
  "memory_id": "memory_id",
  "memory_kind": "rumor|correction|scandal|performance|prestige|milestone|package",
  "owner_ref": "public",
  "source_refs": [],
  "memory_accessibility": 0.0,
  "memory_decay_rate": 0.0,
  "created_turn": 0,
  "updated_turn": 0,
  "status": "active"
}
```

Special retention fields may be attached when relevant:

- `corrected_claim_retention`
- `privacy_boundary_retention`
- `long_memory_anchor`
- `decay_resistance`
- `prestige_memory_strength`

### `RelationshipEdge`

```json
{
  "source_actor": "actor_a",
  "target_actor": "actor_b",
  "affinity": 0.0,
  "trust": 0.0,
  "rivalry": 0.0,
  "obligation": 0.0,
  "recent_delta": 0.0
}
```

Relationship deltas are directed. Do not apply global dislike unless the event
explicitly targets the public.

### `FactionState`

```json
{
  "faction_id": "faction_id",
  "alignment": 0.0,
  "claim_strength": 0.0,
  "claim_legitimacy": 0.0,
  "identity_capture_risk": 0.0,
  "rivalry_pressure": 0.0
}
```

Unknown player consent must stay explicit. Faction alignment may drift without
increasing the player's affinity toward that faction.

### `ModerationBoundary`

```json
{
  "private_detail_allowed": false,
  "personal_attack_allowed": false,
  "claim_requires_evidence_above": 0.55,
  "repeat_debunked_claim_requires_new_evidence": true,
  "correction_pin_active": false,
  "theorycraft_label_required": false,
  "unverified_claim_label_required": false,
  "leak_content_hidden": false,
  "redaction_required": false,
  "summary_only_mode": false,
  "new_replies_limited": false,
  "institution_attention_flag": false,
  "summary_only_scandal_refs": false,
  "performance_discussion_allowed": false,
  "scandal_summary_link_only": false,
  "achievement_thread_split": false
}
```

Boundary fields are constraints on downstream presentation and future state
transitions. They are not UI instructions.

## Specialized Optional Records

Transition outputs may include these records when the corresponding path is
active:

| Record | Owner path | Stable fields |
| --- | --- | --- |
| `package_state` | `new_card_package_seen`, package-linked success | `package_topic_id`, `package_signal`, `observation_confidence`, `package_identity_uncertainty`, `theorycraft_pressure`, `public_memory_status` |
| `prestige_state` | `public_achievement` | `achievement_memory_id`, `actor_id`, `achievement_kind`, `prestige_memory_strength`, `decay_resistance`, `attribution_confidence`, `faction_claim_pressure` |
| `conflict_state` | `npc_conflict` | `conflict_id`, `source_actor`, `target_actor`, `grievance_strength`, `conflict_visibility`, `tone_pressure`, `mediation_capacity`, `repair_offer_strength`, `escalation_risk` |
| `leak_state` | `private_leak` | `leak_id`, `privacy_risk`, `leak_authenticity`, `redaction_level`, `source_exposure_risk`, `public_relevance`, `evidence_quarantine` |
| `scandal_state` | `scandal` | `scandal_id`, `scandal_severity`, `boundary_breach_score`, `institution_attention`, `containment_failure`, `trust_collapse`, `scandal_competition`, `status` |
| `performance_state` | `combat_result` | `combat_memory_id`, `combat_outcome`, `outcome_salience`, `performance_margin`, `performance_consistency`, `ordinary_discussion_pull`, `memory_rebalance` |
| `milestone_state` | `boss_defeated` | `achievement_memory_id`, `boss_salience`, `milestone_status`, `thread_split_pressure`, `scandal_drag`, `long_memory_anchor` |
| `actor_reply_state` | `reply_pressure` | `actor_interest`, `lurker_interest`, `reply_threshold`, `social_risk`, `future_hook_readiness`, `decision` |

Stable specialized record statuses:

- `active_lockdown`
- `active_but_competed`

## Output Envelope

Every event or transition should return a structured result:

```json
{
  "result_id": "result_unique_id",
  "source_id": "evt_or_tick_id",
  "turn": 0,
  "thread_state": {},
  "additional_thread_states": {},
  "participant_roles": {},
  "stance_distribution": {},
  "rumor_state": {},
  "memory_state": {},
  "path_states": {},
  "heat_delta": {},
  "relationship_delta": {},
  "state_patches": {},
  "next_event_hooks": [],
  "warnings": []
}
```

Required top-level fields for V1 implementation:

- `result_id`
- `source_id`
- `turn`
- `thread_state`
- `participant_roles`
- `stance_distribution`
- `heat_delta`
- `relationship_delta`
- `next_event_hooks`

`rumor_state` may be absent when the event has no rumor involvement.

`additional_thread_states` is a map keyed by thread id for transitions such as
`decay` that touch more than one thread. New fixtures should use it instead of
one-off names such as `active_thread_state`.

Path-specific optional records may appear either under `path_states` or as
their stable record name during early fixtures, for example `package_state`,
`scandal_state`, `milestone_state`, or `actor_reply_state`.

`state_patches` may remain report-only at first; it is the intended bridge from
pure transition result to an in-memory store update.

## Stance Distribution

`stance_distribution` is a map of stance id to score. Scores should sum to
approximately `1.0` after normalization.

Stable stance ids:

- `support`
- `skepticism`
- `theorycraft`
- `mockery`
- `correction_acceptance`
- `moderator_neutral`
- `prestige_claim`
- `factional_rivalry`
- `rumor_amplification`
- `privacy_concern`
- `silent_memory`

## Next Event Hooks

```json
{
  "hook_type": "rumor_debunked",
  "condition": "public evidence directly addresses the rumor",
  "target_refs": [],
  "priority": 0.0
}
```

Required fields:

- `hook_type`
- `condition`

Optional fields:

- `target_refs`
- `priority`
- `expires_after_turns`

Hooks are suggestions for future systems. They must not execute campaign,
narrative, UI, or reward behavior by themselves.

Stable hook types from the exploration rounds:

- `combat_result`
- `boss_defeated`
- `player_used_unusual_deck`
- `new_card_package_seen`
- `npc_conflict`
- `faction_event`
- `scandal`
- `misunderstanding`
- `rumor_seeded`
- `rumor_debunked`
- `public_achievement`
- `private_leak`
- `decay`
- `reply_pressure`
- `relationship_repair`
- `moderation_boundary`

`relationship_repair` and `moderation_boundary` are internal hook classes. They
must not dispatch campaign behavior directly.

## Event Evidence Contracts

### `player_used_unusual_deck`

Stable evidence fields:

- `combat_outcome`
- `deck_signal`
- `proof_density`
- `spectator_overlap`
- `deck_novelty_score`

Boundary: creates novelty and proof-request pressure, not card legality.

### `new_card_package_seen`

Stable evidence fields:

- `package_signal`
- `observed_anchor_count`
- `observation_confidence`
- `repeat_visibility`
- `package_identity_uncertainty`
- `evidence_provenance`

Boundary: accepts public package signals only; does not call `cardanalysis`.

### `public_achievement`

Stable evidence fields:

- `achievement_kind`
- `combat_outcome`
- `repeat_success_count`
- `active_package_memory_ref`
- `achievement_visibility`
- `attribution_confidence`
- `performance_margin`
- `audience_overlap`
- `counterevidence_pressure`

Boundary: strengthens public memory; does not prove exact package identity or
grant rewards.

### `faction_event`

Stable evidence fields:

- `faction_event_kind`
- `claim_strength`
- `claim_legitimacy`
- `player_consent_signal`
- `prior_participation`
- `rival_attention`

Boundary: unknown player consent remains explicit.

### `npc_conflict`

Stable evidence fields:

- `conflict_kind`
- `grievance_strength`
- `conflict_visibility`
- `evidence_quality`
- `tone_pressure`
- `mediation_capacity`
- `repair_offer_strength`

Boundary: conflict is not rumor until an unverified factual claim appears.

### `rumor_seeded`

Stable evidence fields:

- `claim_text_ref`
- `source_clarity`
- `claim_specificity`
- `evidence_gap`
- `spread_velocity`
- `containment_pressure`
- `old_debunked_claim_ref`

Boundary: heat and credibility are separate; new rumors do not silently merge
with corrected old rumors.

### `private_leak`

Stable evidence fields:

- `leak_kind`
- `privacy_risk`
- `leak_authenticity`
- `redaction_level`
- `source_exposure_risk`
- `public_relevance`
- `moderator_intervention`

Boundary: private material is quarantined before credibility transfer; do not
store raw private content.

### `scandal`

Stable evidence fields:

- `scandal_kind`
- `scandal_severity`
- `boundary_breach_score`
- `institution_attention`
- `containment_failure`
- `trust_collapse`
- `rumor_truth_status`

Boundary: scandal heat does not imply rumor truth.

### `combat_result`

Stable evidence fields:

- `combat_outcome`
- `outcome_salience`
- `performance_margin`
- `performance_consistency`
- `audience_overlap`
- `scandal_competition`
- `package_signal_visible`

Boundary: ordinary combat results create performance memory, not milestone
prestige by default.

### `boss_defeated`

Stable evidence fields:

- `boss_id`
- `boss_salience`
- `performance_margin`
- `repeat_success_count`
- `audience_overlap`
- `thread_split_pressure`
- `scandal_drag`

Boundary: can split a new milestone thread, but should keep parent memory links.

### `rumor_debunked`

Stable evidence fields:

- `debunk_source_type`
- `debunk_authority`
- `source_trust`
- `evidence_visibility`
- `proof_density_after`
- `contradiction_strength`
- `correction_proof_clarity`
- `faction_defensiveness`
- `belief_inertia`
- `correction_acceptance_lag`
- `backfire_risk`
- `memory_correction_strength`

Boundary: backfire heat can rise while credibility falls; heat is not evidence.

### `misunderstanding`

Stable evidence fields:

- `repeated_claim_ref`
- `source_memory_access`
- `intent_malice_score`
- `correction_salience`
- `public_repeat_visibility`
- `clarification_latency`
- `repair_window_turns`
- `apology_probability`

Boundary: low malice can be repairable, but repeated behavior after clarification
should escalate.

## Transition Contracts

### `decay`

Stable input fields:

- `quiet_turns`
- `new_evidence_count`
- `active_reply_count`
- `correction_pin_active`
- `milestone_anchor_active`

Stable output fields:

- `heat_decay_curve`
- `memory_accessibility`
- `archive_threshold`
- `resurfacing_cost`
- `corrected_claim_retention`

Boundary: decay never deletes corrected rumor records, privacy boundaries, or
milestone memory anchors.

### `reply_pressure`

Stable input fields:

- `thread_status`
- `base_reply_pressure`
- `memory_trigger_match`
- `social_risk`
- `notification_pressure`
- `moderation_friction`

Stable output fields:

- `actor_reply_state`
- `lurker_interest`
- `reply_threshold`
- `future_hook_readiness`

Boundary: interested actors may lurk; silent memory should not create
relationship delta until later public action.

## Hard Invariants

1. Domain outputs are structured state, not final BBS prose.
2. No transition may call LLM text generation.
3. No transition may call or depend on `cardanalysis`.
4. Rumor heat and rumor credibility must remain separate.
5. Scandal heat must not imply rumor truth.
6. Debunked rumor memory keeps original claim ref and corrected status.
7. Private leak content is never stored as raw public text.
8. Unknown player consent remains explicit in faction claims.
9. Decay archives and lowers accessibility; it does not delete history.
10. Hooks do not execute side effects outside the gossip model.
11. New enum/status values must update this contract and the lab log in the
    same slice.

## First Implementation Target

The first code slice should implement only:

1. typed input envelopes
2. typed output envelope
3. typed core records for actor, topic, thread, post, reply, rumor, memory,
   faction, relationship edge, and moderation boundary
4. in-memory state container
5. pure transition stubs for:
   - `player_used_unusual_deck`
   - `rumor_seeded`
   - `rumor_debunked`
   - `public_achievement`
   - `decay`
   - `reply_pressure`
6. fixture-based tests copied from the exploration examples

Do not implement UI, persistence migration, or campaign integration in the first
code slice.
