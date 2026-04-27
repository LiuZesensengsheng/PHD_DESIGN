# Gossip BBS Social Simulation Model Lab

- Model: `gossip_bbs_social_simulation_model_v1`
- Status: exploration draft
- First slice: `2026-04-27`
- Current owner branch: `codex/04-27-gossip-bbs-model-lab`

## Boundary

This lab only models domain state, state transitions, and structured payloads for
future in-game BBS / gossip / public-opinion simulation.

It does not:

- build UI
- call an LLM for final prose
- write large story text
- couple directly to `cardanalysis`
- add a database or persistence migration

The intended output is structured state that later systems may render,
summarize, or transform into narrative content.

## Project Context Read

- Narrative pipeline docs favor explicit structured consequences and runtime-safe
  transition requests, not arbitrary callback scripts.
- Narrative instance docs separate template from instance state; this model should
  likewise keep topic/thread memory as explicit state, not generated text.
- Campaign lifecycle docs expose future timing windows such as combat return,
  turn advance, forced DDL refresh, and turn idle. This lab should remain a
  sidecar to those facts until an integration point is explicitly chosen.
- Existing gossip runtime is a lightweight flavor modal and badge flow. It is a
  useful reference for current UI boundaries, but not the target model.

## V1 Entity Vocabulary

| Entity | Minimal role in the model |
| --- | --- |
| `actor` | Player, NPC, mentor, rival, spectator, or named account that can remember, post, reply, or change stance. |
| `faction` | Lab, school, discipline, deck archetype fan group, or social clique that biases interpretation. |
| `relationship_edge` | Directed relation between two actors with affinity, trust, rivalry, obligation, and recent delta. |
| `event` | Structured upstream fact such as combat result, scandal, leak, achievement, or rumor correction. |
| `topic` | Public discussion subject derived from one or more events. Owns heat and memory entry points. |
| `rumor` | Unverified claim attached to a topic; owns credibility, spread, source clarity, and debunk status. |
| `post` | First public statement in a thread; structured role and stance, not final prose. |
| `reply` | Actor response to a post or reply; can amplify, challenge, ask for proof, joke, or moderate. |
| `thread` | BBS conversation container with lifetime, participants, heat, moderation state, and output hooks. |
| `stance` | Actor/topic position such as support, doubt, mockery, concern, factional defense, or moderator-neutral. |
| `credibility` | Numeric or bucketed belief score for rumor/event interpretation. |
| `heat` | Public attention level for topic, rumor, post, or thread. |
| `memory` | Persistent public or actor-local recollection of notable events and resolved claims. |
| `decay` | Time-based reduction in heat, credibility salience, reply pressure, and memory accessibility. |
| `moderation_boundary` | Safety and tone boundary for thread actions: no doxxing, no private detail reveal beyond payload, no hate/personal harassment escalation. |

## Event Input Catalog

Each input should be accepted as a structured event with `event_id`,
`event_type`, `turn`, `visibility`, `source_actor`, `target_refs`, `evidence`,
and optional `faction_refs`.

| Event type | Default topic pressure |
| --- | --- |
| `combat_result` | Converts combat outcome into public performance memory. |
| `boss_defeated` | Creates high-heat achievement topic and faction prestige pressure. |
| `player_used_unusual_deck` | Creates novelty topic, proof requests, and deck-identity stance split. |
| `new_card_package_seen` | Creates theorycraft topic with lower credibility requirements. |
| `npc_conflict` | Creates relationship topic and faction alignment pressure. |
| `faction_event` | Creates faction reputation topic and alignment drift. |
| `scandal` | Creates high-heat, high-moderation-risk rumor/topic pair. |
| `misunderstanding` | Creates medium-heat rumor with high debunk sensitivity. |
| `rumor_seeded` | Creates rumor-first topic with low initial credibility and high spread variance. |
| `rumor_debunked` | Lowers credibility, shifts stances, and creates reputation repair or backlash hooks. |
| `public_achievement` | Raises public sentiment and long-memory chance. |
| `private_leak` | Creates boundary-sensitive rumor with strict moderation and source-risk metadata. |

## State Variables

| Variable | Meaning |
| --- | --- |
| `topic_heat` | Attention currently attached to a topic. |
| `rumor_credibility` | Belief score for an unverified claim. |
| `actor_interest` | Actor willingness to notice or enter the thread. |
| `actor_bias` | Actor prior leaning from faction, relationship, and memory. |
| `relationship_delta` | Relationship change caused by public stance, proof, or mockery. |
| `faction_alignment` | Direction and strength of factional support or opposition. |
| `public_sentiment` | Aggregate public evaluation of the actor/topic. |
| `memory_decay_rate` | Rate at which the event leaves easy recall. |
| `reply_pressure` | Likelihood that actors feel pushed to respond. |
| `thread_lifetime` | Remaining active turns before thread archives or decays. |

## Transition Rules

1. `event -> topic`
   - Create or update a topic when event visibility is not private-only.
   - Initial `topic_heat` comes from event salience, public visibility, novelty,
     faction involvement, and current public fatigue.

2. `topic -> thread`
   - Spawn a thread when `topic_heat >= thread_open_threshold`.
   - Thread inherits topic tags, source event refs, moderation boundary, and
     initial public sentiment.

3. `actor -> reply decision`
   - Actor replies when
     `actor_interest + reply_pressure + faction_alignment + relationship_bias`
     beats silence threshold.
   - Actor may lurk if interest is high but credibility or moderation risk is
     unclear.

4. `faction -> stance`
   - Faction membership shifts actor stance toward defense, attack, skepticism,
     or prestige-claiming.
   - Rival factions increase skeptical and mocking replies.

5. `rumor heat / cooling`
   - Rumor heat rises with novelty, ambiguity, source status, and faction echo.
   - Rumor heat cools with proof clarity, moderator intervention, time, and
     competing topics.

6. `debunk -> credibility`
   - `rumor_debunked` lowers `rumor_credibility`.
   - If the debunk source is mistrusted, heat may rise while credibility falls.

7. `time -> decay`
   - Each turn reduces `topic_heat`, `reply_pressure`, and active thread lifetime
     by `memory_decay_rate`, modified by public achievement or scandal severity.

8. `thread activity -> relationship`
   - Supportive replies can raise affinity/trust.
   - Mocking, accusation, or factional pile-on can lower affinity and raise
     rivalry.

9. `player behavior -> public memory`
   - Events above salience threshold create memory entries.
   - Memory entries later bias actor interest, faction alignment, and credibility
     priors for related topics.

## Output Payload Shape

The model emits state, not final copy:

```json
{
  "thread_state": {},
  "participant_roles": {},
  "stance_distribution": {},
  "rumor_state": {},
  "heat_delta": {},
  "relationship_delta": {},
  "next_event_hooks": []
}
```

## Working Log: 2026-04-27

### Round Event

`player_used_unusual_deck`

Minimal input:

```json
{
  "event_id": "evt_20260427_unusual_deck_001",
  "event_type": "player_used_unusual_deck",
  "turn": 18,
  "visibility": "public_after_combat",
  "source_actor": "player",
  "target_refs": ["rival_grad_a", "mentor_a", "deck_theory_faction"],
  "evidence": {
    "combat_outcome": "elite_win",
    "deck_signal": "unusual_low_cost_recursion",
    "proof_density": 0.62,
    "spectator_overlap": 0.48
  },
  "faction_refs": ["lab_a", "deck_theory_faction", "rival_lab_b"]
}
```

### Model Increment

This first slice adds the shared V1 vocabulary and concretizes only one event
path:

`player_used_unusual_deck -> novelty topic -> proof-request thread -> stance split`

Newly named derived signals:

- `deck_novelty_score`: how far the seen deck behavior is from expected public
  memory.
- `proof_density`: how much observable evidence exists before the thread starts.
- `spectator_overlap`: how many potential posters plausibly saw enough to care.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "source_event_ids": ["evt_20260427_unusual_deck_001"],
    "status": "active",
    "opened_turn": 18,
    "thread_lifetime": 4,
    "topic_heat": 0.71,
    "reply_pressure": 0.58,
    "public_sentiment": 0.18,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "claim_requires_evidence_above": 0.55
    }
  },
  "participant_roles": {
    "player": "silent_subject",
    "rival_grad_a": "skeptic",
    "mentor_a": "authority_lurker",
    "deck_theory_faction": "explainer",
    "lab_a": "supportive_witness",
    "moderator": "boundary_keeper"
  },
  "stance_distribution": {
    "support": 0.34,
    "skepticism": 0.28,
    "theorycraft": 0.22,
    "mockery": 0.10,
    "moderator_neutral": 0.06
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "claim_type": "mechanism_misread",
    "rumor_credibility": 0.32,
    "heat": 0.44,
    "debunk_status": "not_debunked",
    "evidence_gap": 0.38
  },
  "heat_delta": {
    "topic_heat": 0.31,
    "rumor_heat": 0.18,
    "reply_pressure": 0.22
  },
  "relationship_delta": {
    "player->deck_theory_faction": 0.08,
    "rival_grad_a->player": -0.04,
    "mentor_a->player": 0.03
  },
  "next_event_hooks": [
    {
      "hook_type": "rumor_debunked",
      "condition": "proof_density rises above 0.78 or moderator pins evidence"
    },
    {
      "hook_type": "new_card_package_seen",
      "condition": "same package appears in another public combat"
    },
    {
      "hook_type": "public_achievement",
      "condition": "player repeats elite_win with similar deck signal"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `deck_novelty_score` as an event-to-topic salience modifier.
- Added `proof_density` as a rumor credibility brake.
- Added `spectator_overlap` as a participant/reply-pressure modifier.
- Added the first concrete transition:
  - if `deck_novelty_score` is high and `visibility` is public, create a novelty
    topic;
  - if `topic_heat >= 0.50`, open a BBS thread;
  - if `proof_density < 0.70`, create a low-credibility mechanism-misread rumor;
  - if faction alignment is positive, assign explainer/support roles before
    mockery roles.

### Risks

- The model can drift into final forum writing if example payloads become prose.
- `player_used_unusual_deck` is tempting to connect to `cardanalysis`; this lab
  should only accept a reviewed structured signal for now.
- Moderation boundaries need stronger rules before handling `private_leak` or
  high-severity `scandal`.
- Memory persistence shape is intentionally not chosen yet; do not add save
  schema from this first slice.

### Next Round Entry

Use `rumor_debunked` next. It is the smallest useful follow-up because it tests
credibility reduction, heat backlash, stance migration, relationship repair, and
memory correction without needing UI or final prose.

## Working Log: 2026-04-27 Round 2

### Round Event

`rumor_debunked`

This round continues from `rumor_deck_is_bugged_001` created by the previous
`player_used_unusual_deck` slice.

Minimal input:

```json
{
  "event_id": "evt_20260427_debunk_001",
  "event_type": "rumor_debunked",
  "turn": 19,
  "visibility": "public_thread_update",
  "source_actor": "moderator",
  "target_refs": [
    "rumor_deck_is_bugged_001",
    "bbs_thread_unusual_deck_018_001",
    "player",
    "rival_grad_a"
  ],
  "evidence": {
    "debunk_source_type": "moderator_pinned_evidence",
    "evidence_visibility": 0.86,
    "debunk_authority": 0.74,
    "proof_density_after": 0.84,
    "contradiction_strength": 0.69
  },
  "faction_refs": ["deck_theory_faction", "lab_a", "rival_lab_b"]
}
```

### Model Increment

This slice adds the first correction path:

`rumor_debunked -> credibility drop -> stance migration -> memory correction`

Newly named derived signals:

- `debunk_authority`: trust granted to the actor or system presenting the
  correction.
- `evidence_visibility`: how many participants can inspect the correction
  without relying on hearsay.
- `belief_inertia`: resistance from actors who already posted or aligned around
  the rumor.
- `backfire_risk`: chance that heat rises while credibility falls.
- `memory_correction_strength`: likelihood that future recalls remember the
  corrected state instead of the original rumor.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "source_event_ids": [
      "evt_20260427_unusual_deck_001",
      "evt_20260427_debunk_001"
    ],
    "status": "cooling_after_correction",
    "opened_turn": 18,
    "updated_turn": 19,
    "thread_lifetime": 2,
    "topic_heat": 0.57,
    "reply_pressure": 0.34,
    "public_sentiment": 0.27,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "repeat_debunked_claim_requires_new_evidence": true,
      "correction_pin_active": true
    }
  },
  "participant_roles": {
    "player": "silent_subject_rehabilitated",
    "rival_grad_a": "skeptic_under_correction",
    "mentor_a": "authority_lurker_positive",
    "deck_theory_faction": "evidence_explainer",
    "lab_a": "supportive_witness",
    "moderator": "correction_anchor"
  },
  "stance_distribution": {
    "support": 0.42,
    "skepticism": 0.16,
    "theorycraft": 0.24,
    "mockery": 0.06,
    "correction_acceptance": 0.09,
    "moderator_neutral": 0.03
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "claim_type": "mechanism_misread",
    "rumor_credibility": 0.11,
    "heat": 0.25,
    "debunk_status": "debunked_with_visible_evidence",
    "evidence_gap": 0.16,
    "memory_correction_strength": 0.72,
    "backfire_risk": 0.18
  },
  "heat_delta": {
    "topic_heat": -0.14,
    "rumor_heat": -0.19,
    "reply_pressure": -0.24
  },
  "relationship_delta": {
    "player->deck_theory_faction": 0.04,
    "deck_theory_faction->player": 0.06,
    "rival_grad_a->player": -0.01,
    "mentor_a->player": 0.05,
    "moderator->rival_grad_a": -0.02
  },
  "next_event_hooks": [
    {
      "hook_type": "public_achievement",
      "condition": "corrected unusual-deck win remains in public memory for 2 turns"
    },
    {
      "hook_type": "misunderstanding",
      "condition": "low-belief-inertia actor repeats the old claim without malice"
    },
    {
      "hook_type": "faction_event",
      "condition": "rival_lab_b contests the correction source instead of the evidence"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `debunk_authority` as a credibility-delta multiplier.
- Added `evidence_visibility` as a stance-migration multiplier.
- Added `belief_inertia` as resistance to correction for prior posters and
  faction-aligned skeptics.
- Added `backfire_risk` so a correction can reduce `rumor_credibility` while
  briefly keeping `topic_heat` alive.
- Added `memory_correction_strength` so later topics can recall "debunked
  unusual-deck claim" instead of only "unusual-deck rumor."

Concrete transition:

1. Find the target rumor by `target_refs`.
2. Compute `credibility_drop` from `debunk_authority`, `evidence_visibility`,
   `contradiction_strength`, and current `rumor_credibility`.
3. Lower `rumor_credibility`; clamp at `0.0`.
4. Move stances from `skepticism` and `mockery` toward
   `correction_acceptance`, `support`, or `silent_lurking` based on
   `belief_inertia`.
5. Reduce `reply_pressure` unless `backfire_risk` crosses a local threshold.
6. Write a memory correction entry when `memory_correction_strength >= 0.60`.
7. Apply small relationship repair toward actors who provided or accepted
   visible evidence.

### Risks

- A debunk path can become too moralizing if the model assumes every correction
  is fully trusted. `debunk_authority` and `belief_inertia` should stay separate.
- A low-trust correction can create heat backlash; the model must allow heat and
  credibility to move in opposite directions.
- Memory correction should not erase the old rumor completely. Future recall
  needs both the original claim and the corrected status.
- This still does not define persistence ownership. Keep memory as a payload
  concept until a save boundary is chosen.

### Next Round Entry

Use `misunderstanding` next. It is the smallest next case because it can reuse
the corrected rumor memory and test whether actors repeat old claims with low
malice, medium heat, and repairable relationship damage.

## Working Log: 2026-04-27 Round 3

### Round Event

`misunderstanding`

This round continues from the corrected memory for `rumor_deck_is_bugged_001`.
The goal is to model a low-malice actor repeating the old claim because they
missed the pinned correction, not because they are intentionally reseeding a
rumor.

Minimal input:

```json
{
  "event_id": "evt_20260427_misunderstanding_001",
  "event_type": "misunderstanding",
  "turn": 20,
  "visibility": "public_thread_reply",
  "source_actor": "peer_observer_b",
  "target_refs": [
    "rumor_deck_is_bugged_001",
    "bbs_thread_unusual_deck_018_001",
    "player",
    "moderator"
  ],
  "evidence": {
    "repeated_claim_ref": "rumor_deck_is_bugged_001",
    "source_memory_access": 0.31,
    "correction_salience": 0.72,
    "intent_malice_score": 0.12,
    "public_repeat_visibility": 0.46,
    "clarification_latency": 1
  },
  "faction_refs": ["lab_a", "deck_theory_faction"]
}
```

### Model Increment

This slice adds the first mistaken-repeat path:

`misunderstanding -> brief topic reactivation -> clarification -> repairable relationship damage`

Newly named derived signals:

- `source_memory_access`: how likely the actor was to have seen or recalled the
  corrected status.
- `intent_malice_score`: whether the repeat is a misunderstanding or should be
  escalated into `rumor_seeded`.
- `correction_salience`: how visible the existing correction is at the moment of
  repetition.
- `clarification_latency`: how many turns pass before a correction reply or
  moderator reminder appears.
- `repair_window_turns`: how long the model treats the relationship damage as
  easy to repair.
- `apology_probability`: chance that the source actor accepts correction and
  reduces relationship damage.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "source_event_ids": [
      "evt_20260427_unusual_deck_001",
      "evt_20260427_debunk_001",
      "evt_20260427_misunderstanding_001"
    ],
    "status": "briefly_reactivated_by_misunderstanding",
    "opened_turn": 18,
    "updated_turn": 20,
    "thread_lifetime": 2,
    "topic_heat": 0.63,
    "reply_pressure": 0.42,
    "public_sentiment": 0.23,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "repeat_debunked_claim_requires_new_evidence": true,
      "correction_pin_active": true,
      "misunderstanding_grace_turns": 1
    }
  },
  "participant_roles": {
    "player": "silent_subject_slightly_harmed",
    "peer_observer_b": "mistaken_repeater",
    "moderator": "correction_reminder",
    "deck_theory_faction": "patient_explainer",
    "lab_a": "supportive_witness",
    "rival_grad_a": "low_activity_skeptic"
  },
  "stance_distribution": {
    "support": 0.39,
    "skepticism": 0.18,
    "theorycraft": 0.21,
    "mockery": 0.05,
    "correction_acceptance": 0.13,
    "moderator_neutral": 0.04
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "claim_type": "mechanism_misread",
    "rumor_credibility": 0.15,
    "heat": 0.31,
    "debunk_status": "debunked_but_repeated_by_mistake",
    "evidence_gap": 0.16,
    "memory_correction_strength": 0.68,
    "misunderstanding_episode_id": "misunderstanding_001",
    "apology_probability": 0.64
  },
  "heat_delta": {
    "topic_heat": 0.06,
    "rumor_heat": 0.06,
    "reply_pressure": 0.08
  },
  "relationship_delta": {
    "peer_observer_b->player": -0.03,
    "player->peer_observer_b": -0.02,
    "deck_theory_faction->peer_observer_b": 0.01,
    "moderator->peer_observer_b": -0.01
  },
  "next_event_hooks": [
    {
      "hook_type": "relationship_repair",
      "condition": "peer_observer_b accepts correction within repair_window_turns"
    },
    {
      "hook_type": "rumor_seeded",
      "condition": "same actor repeats debunked claim again after clarification"
    },
    {
      "hook_type": "new_card_package_seen",
      "condition": "fresh public evidence shifts thread from accusation to theorycraft"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `source_memory_access` as a check against whether the actor had a fair
  chance to know the correction.
- Added `intent_malice_score` to separate accidental repetition from hostile
  rumor seeding.
- Added `correction_salience` to dampen credibility growth when the correction
  is still visible.
- Added `clarification_latency` as a heat and relationship-damage multiplier.
- Added `repair_window_turns` and `apology_probability` for reversible social
  damage.

Concrete transition:

1. Find the corrected rumor memory by `repeated_claim_ref`.
2. If `intent_malice_score < 0.30` and `source_memory_access < 0.45`, classify
   the event as `misunderstanding`.
3. Keep the original rumor in `debunked` state; attach a
   `misunderstanding_episode_id` instead of reopening the rumor as new truth.
4. Increase `topic_heat` and `reply_pressure` by public visibility, but cap
   `rumor_credibility` when `correction_salience >= 0.60`.
5. Apply small, repairable relationship damage to the repeated-claim source and
   target.
6. If clarification arrives within `repair_window_turns`, move stance toward
   `correction_acceptance` and reduce long-term relationship damage.
7. If the same actor repeats after clarification, escalate the next event hook
   to `rumor_seeded`.

### Risks

- The model must not treat every repeated false claim as harmless. High
  `intent_malice_score` or repeated behavior should leave the
  `misunderstanding` path.
- The model must not erase the harm just because intent is low; relationship
  damage should still exist, but remain more repairable.
- If `correction_salience` is too strong, the thread may become sterile and
  never reactivate. Low source memory access should still create small heat.
- This still stays outside persistence and UI; `repair_window_turns` is a
  proposed state variable, not a saved-schema decision.

### Next Round Entry

Use `new_card_package_seen` next. It can test whether fresh public evidence
turns a corrected accusation thread into a lower-risk theorycraft topic without
coupling to `cardanalysis` internals.

## Working Log: 2026-04-27 Round 4

### Round Event

`new_card_package_seen`

This round continues from the corrected and briefly reactivated unusual-deck
thread. The purpose is to model fresh public evidence that lets participants
move from accusation and correction into lower-risk theorycraft.

Minimal input:

```json
{
  "event_id": "evt_20260427_card_package_seen_001",
  "event_type": "new_card_package_seen",
  "turn": 21,
  "visibility": "public_after_combat",
  "source_actor": "spectator_feed",
  "target_refs": [
    "bbs_thread_unusual_deck_018_001",
    "topic_unusual_low_cost_recursion_001",
    "player",
    "deck_theory_faction"
  ],
  "evidence": {
    "package_signal": "low_cost_recursion_package_public_v0",
    "observed_anchor_count": 3,
    "observation_confidence": 0.67,
    "repeat_visibility": 0.58,
    "package_identity_uncertainty": 0.41,
    "evidence_provenance": "spectator_visible_combat_log"
  },
  "faction_refs": ["deck_theory_faction", "lab_a", "rival_lab_b"]
}
```

### Model Increment

This slice adds the first evidence-to-theorycraft path:

`new_card_package_seen -> theorycraft topic update -> accusation cooling -> package-memory seed`

Newly named derived signals:

- `package_signal`: public, non-authoritative identity hint for the observed card
  package.
- `observed_anchor_count`: count of visible package anchors seen by spectators.
- `observation_confidence`: how confident public participants are that a coherent
  package exists.
- `package_identity_uncertainty`: remaining uncertainty about what the package
  actually is.
- `theorycraft_pressure`: likelihood that actors reply with explanation,
  speculation, or build comparison instead of accusation.
- `accusation_to_analysis_shift`: amount of stance mass moved from rumor or
  mockery toward theorycraft.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "source_event_ids": [
      "evt_20260427_unusual_deck_001",
      "evt_20260427_debunk_001",
      "evt_20260427_misunderstanding_001",
      "evt_20260427_card_package_seen_001"
    ],
    "status": "converted_to_theorycraft",
    "opened_turn": 18,
    "updated_turn": 21,
    "thread_lifetime": 3,
    "topic_heat": 0.69,
    "reply_pressure": 0.46,
    "public_sentiment": 0.31,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "repeat_debunked_claim_requires_new_evidence": true,
      "correction_pin_active": true,
      "theorycraft_label_required": true
    }
  },
  "participant_roles": {
    "player": "observed_package_subject",
    "spectator_feed": "evidence_source",
    "deck_theory_faction": "theorycraft_lead",
    "lab_a": "supportive_witness",
    "rival_lab_b": "competitive_analyst",
    "moderator": "boundary_keeper"
  },
  "stance_distribution": {
    "support": 0.34,
    "skepticism": 0.10,
    "theorycraft": 0.39,
    "mockery": 0.03,
    "correction_acceptance": 0.10,
    "moderator_neutral": 0.04
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "claim_type": "mechanism_misread",
    "rumor_credibility": 0.08,
    "heat": 0.18,
    "debunk_status": "superseded_by_public_package_evidence",
    "evidence_gap": 0.09,
    "memory_correction_strength": 0.75,
    "accusation_to_analysis_shift": 0.21
  },
  "package_state": {
    "package_topic_id": "package_low_cost_recursion_public_v0",
    "package_signal": "low_cost_recursion_package_public_v0",
    "observation_confidence": 0.67,
    "package_identity_uncertainty": 0.41,
    "theorycraft_pressure": 0.52,
    "public_memory_status": "seeded_unconfirmed_package_memory"
  },
  "heat_delta": {
    "topic_heat": 0.06,
    "rumor_heat": -0.13,
    "theorycraft_heat": 0.28,
    "reply_pressure": 0.04
  },
  "relationship_delta": {
    "deck_theory_faction->player": 0.05,
    "rival_lab_b->player": 0.01,
    "player->deck_theory_faction": 0.02,
    "moderator->thread_participants": 0.01
  },
  "next_event_hooks": [
    {
      "hook_type": "public_achievement",
      "condition": "player wins again while package memory remains active"
    },
    {
      "hook_type": "faction_event",
      "condition": "deck_theory_faction claims the package as a school identity"
    },
    {
      "hook_type": "player_used_unusual_deck",
      "condition": "same package signal appears with a different combat outcome"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `package_signal` as a public, non-authoritative package identity hint.
- Added `observed_anchor_count` as a lightweight evidence-density input.
- Added `observation_confidence` to keep theorycraft stronger than rumor but
  weaker than confirmed fact.
- Added `package_identity_uncertainty` so the model can keep speculation labeled
  as speculation.
- Added `theorycraft_pressure` as a reply-pressure subtype.
- Added `accusation_to_analysis_shift` to explicitly move stance mass away from
  the old debunked claim.

Concrete transition:

1. Accept `new_card_package_seen` only as a structured public signal; do not call
   `cardanalysis` or infer package legality.
2. Match `package_signal` against current topic memory and corrected rumor memory.
3. If `observation_confidence >= 0.55`, create or update `package_state`.
4. Reduce old rumor heat when package evidence explains the original ambiguity.
5. Increase `theorycraft_pressure` and stance mass for `theorycraft`, capped by
   `package_identity_uncertainty`.
6. Require a theorycraft label while uncertainty remains above `0.25`.
7. Seed unconfirmed package memory that future `public_achievement` or repeated
   combat outcomes can strengthen.

### Risks

- This path can accidentally become a card-analysis evaluator. Keep the input as
  reviewed public signals only.
- Theorycraft can become disguised accusation if the moderation boundary does not
  require uncertainty labels.
- The package memory is unconfirmed. Future events should be able to strengthen,
  split, or discard it.
- Fresh evidence should not delete the debunk record; it supersedes the old
  accusation with a better explanation.

### Next Round Entry

Use `public_achievement` next. It can test whether repeated success with an
active package memory converts short-lived theorycraft into public prestige and
longer-term actor/faction memory.

## Working Log: 2026-04-27 Round 5

### Round Event

`public_achievement`

This round continues from the theorycraft conversion path. The purpose is to
model how repeated public success strengthens social memory without treating the
success as proof of exact package identity or card-analysis correctness.

Minimal input:

```json
{
  "event_id": "evt_20260427_public_achievement_001",
  "event_type": "public_achievement",
  "turn": 23,
  "visibility": "public_after_combat",
  "source_actor": "combat_result_feed",
  "target_refs": [
    "bbs_thread_unusual_deck_018_001",
    "topic_unusual_low_cost_recursion_001",
    "package_low_cost_recursion_public_v0",
    "player",
    "deck_theory_faction"
  ],
  "evidence": {
    "achievement_kind": "elite_streak_win",
    "combat_outcome": "elite_win",
    "repeat_success_count": 2,
    "active_package_memory_ref": "package_low_cost_recursion_public_v0",
    "achievement_visibility": 0.74,
    "attribution_confidence": 0.63,
    "performance_margin": 0.58,
    "audience_overlap": 0.49,
    "counterevidence_pressure": 0.18
  },
  "faction_refs": ["deck_theory_faction", "lab_a", "rival_lab_b"]
}
```

### Model Increment

This slice adds the first prestige-to-memory path:

`public_achievement -> prestige topic update -> package memory reinforcement -> slower decay`

Newly named derived signals:

- `achievement_visibility`: how easy the public can observe the achievement
  without private detail.
- `repeat_success_count`: number of related public successes still reachable in
  topic memory.
- `attribution_confidence`: confidence that the active package memory is related
  to the achievement, not proof that the package identity is exact.
- `prestige_memory_strength`: long-memory weight attached to the actor's public
  success.
- `decay_resistance`: how much the achievement slows normal topic and memory
  decay.
- `faction_claim_pressure`: likelihood that a faction starts treating the
  achievement as evidence for its own identity or doctrine.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "source_event_ids": [
      "evt_20260427_unusual_deck_001",
      "evt_20260427_debunk_001",
      "evt_20260427_misunderstanding_001",
      "evt_20260427_card_package_seen_001",
      "evt_20260427_public_achievement_001"
    ],
    "status": "prestige_reactivation",
    "opened_turn": 18,
    "updated_turn": 23,
    "thread_lifetime": 5,
    "topic_heat": 0.78,
    "reply_pressure": 0.41,
    "public_sentiment": 0.52,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "repeat_debunked_claim_requires_new_evidence": true,
      "correction_pin_active": true,
      "theorycraft_label_required": true,
      "achievement_claim_must_reference_public_event": true
    }
  },
  "participant_roles": {
    "player": "observed_achiever",
    "combat_result_feed": "achievement_evidence_source",
    "deck_theory_faction": "prestige_amplifier",
    "lab_a": "local_supporter",
    "rival_lab_b": "skeptical_counterweight",
    "moderator": "boundary_keeper"
  },
  "stance_distribution": {
    "support": 0.42,
    "skepticism": 0.09,
    "theorycraft": 0.25,
    "mockery": 0.02,
    "prestige_claim": 0.16,
    "moderator_neutral": 0.06
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "claim_type": "mechanism_misread",
    "rumor_credibility": 0.05,
    "heat": 0.12,
    "debunk_status": "suppressed_by_public_success_memory",
    "evidence_gap": 0.06,
    "memory_correction_strength": 0.79,
    "accusation_to_analysis_shift": 0.25
  },
  "package_state": {
    "package_topic_id": "package_low_cost_recursion_public_v0",
    "package_signal": "low_cost_recursion_package_public_v0",
    "observation_confidence": 0.73,
    "package_identity_uncertainty": 0.34,
    "theorycraft_pressure": 0.47,
    "linked_success_count": 2,
    "public_memory_status": "reinforced_unconfirmed_package_memory"
  },
  "prestige_state": {
    "achievement_memory_id": "memory_player_elite_streak_023_001",
    "actor_id": "player",
    "achievement_kind": "elite_streak_win",
    "prestige_memory_strength": 0.64,
    "memory_decay_rate": 0.09,
    "decay_resistance": 0.31,
    "attribution_confidence": 0.63,
    "faction_claim_pressure": 0.44,
    "public_sentiment": 0.52
  },
  "heat_delta": {
    "topic_heat": 0.09,
    "rumor_heat": -0.06,
    "theorycraft_heat": 0.10,
    "prestige_heat": 0.31,
    "reply_pressure": -0.05
  },
  "relationship_delta": {
    "deck_theory_faction->player": 0.08,
    "lab_a->player": 0.06,
    "rival_lab_b->player": 0.02,
    "player->deck_theory_faction": 0.03
  },
  "next_event_hooks": [
    {
      "hook_type": "faction_event",
      "condition": "deck_theory_faction claims the achievement as school identity"
    },
    {
      "hook_type": "boss_defeated",
      "condition": "next achievement crosses a higher public salience threshold"
    },
    {
      "hook_type": "rumor_seeded",
      "condition": "rival faction reframes the achievement as staged or carried"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `achievement_visibility` as public observability for achievement facts.
- Added `repeat_success_count` as a compact memory-reinforcement input.
- Added `attribution_confidence` to separate achievement credit from exact
  package proof.
- Added `prestige_memory_strength` as long-memory weight for an actor's public
  success.
- Added `decay_resistance` so strong achievements slow but do not remove normal
  decay.
- Added `faction_claim_pressure` as the bridge from actor prestige into faction
  alignment drift.

Concrete transition:

1. Accept `public_achievement` only as a structured public fact; do not grant
   rewards, write final BBS prose, or evaluate card strength.
2. Match `active_package_memory_ref` to current topic memory if present.
3. If `repeat_success_count >= 2` and `achievement_visibility >= 0.60`,
   increase `prestige_memory_strength`.
4. If `attribution_confidence >= 0.55`, reinforce package memory but keep it
   unconfirmed while `package_identity_uncertainty > 0.25`.
5. Reduce old rumor heat when public success makes the old accusation less
   useful as an explanation.
6. Apply `decay_resistance` to topic memory and actor prestige memory, while
   leaving `memory_decay_rate` nonzero.
7. Increase `faction_claim_pressure` when a faction has already participated in
   the theorycraft thread.

### Risks

- Achievement must not become proof of exact package identity. It can strengthen
  public memory, not certify the mechanism.
- Prestige can snowball too quickly if `decay_resistance` stacks without a cap.
- Faction claim pressure can steal agency from the player if every achievement
  is immediately owned by a faction.
- The old debunked rumor should stay in corrected memory; the achievement
  suppresses it rather than deleting it.

### Next Round Entry

Use `faction_event` next. It can test whether a faction claim over the player's
achievement creates alignment drift, rivalry pressure, and new hooks without
turning the BBS model into final narrative text.

## Working Log: 2026-04-27 Round 6

### Round Event

`faction_event`

This round tests a faction trying to claim the player's public achievement as
evidence for its own school identity. The model should create alignment drift
and rivalry pressure, not authored faction dialogue.

Minimal input:

```json
{
  "event_id": "evt_20260427_faction_claim_001",
  "event_type": "faction_event",
  "turn": 24,
  "visibility": "public_bbs",
  "source_actor": "deck_theory_faction",
  "target_refs": [
    "player",
    "memory_player_elite_streak_023_001",
    "package_low_cost_recursion_public_v0"
  ],
  "evidence": {
    "faction_event_kind": "achievement_claimed_as_school_identity",
    "claim_strength": 0.61,
    "claim_legitimacy": 0.48,
    "player_consent_signal": "unknown",
    "prior_participation": 0.72,
    "rival_attention": 0.57
  },
  "faction_refs": ["deck_theory_faction", "lab_a", "rival_lab_b"]
}
```

### Model Increment

This slice adds the first faction-claim path:

`faction_event -> faction claim topic -> alignment drift -> rivalry pressure`

Newly named derived signals:

- `claim_strength`: how forcefully a faction ties the achievement to itself.
- `claim_legitimacy`: public confidence that the faction has a fair basis for
  the claim.
- `identity_capture_risk`: risk that the player's achievement is socially
  overwritten by faction ownership.
- `alignment_delta`: faction-level movement toward support, rivalry, or
  skepticism.
- `rivalry_pressure`: likelihood that rival factions answer the claim.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "topic_id": "topic_unusual_low_cost_recursion_001",
    "status": "faction_claim_contested",
    "updated_turn": 24,
    "topic_heat": 0.82,
    "reply_pressure": 0.54,
    "public_sentiment": 0.49,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "player_consent_unknown_label_required": true,
      "faction_claim_must_reference_public_event": true
    }
  },
  "participant_roles": {
    "player": "achievement_subject",
    "deck_theory_faction": "claiming_faction",
    "lab_a": "soft_affiliation_support",
    "rival_lab_b": "rival_counterclaim",
    "moderator": "boundary_keeper"
  },
  "stance_distribution": {
    "support": 0.31,
    "skepticism": 0.14,
    "theorycraft": 0.18,
    "prestige_claim": 0.22,
    "factional_rivalry": 0.10,
    "moderator_neutral": 0.05
  },
  "rumor_state": {
    "rumor_id": "rumor_deck_is_bugged_001",
    "rumor_credibility": 0.05,
    "heat": 0.10,
    "debunk_status": "background_corrected_memory"
  },
  "faction_state": {
    "claiming_faction": "deck_theory_faction",
    "claim_strength": 0.61,
    "claim_legitimacy": 0.48,
    "identity_capture_risk": 0.42,
    "rivalry_pressure": 0.46,
    "alignment_delta": {
      "deck_theory_faction": 0.08,
      "lab_a": 0.03,
      "rival_lab_b": -0.05
    }
  },
  "heat_delta": {
    "topic_heat": 0.04,
    "prestige_heat": 0.06,
    "faction_heat": 0.24,
    "reply_pressure": 0.13
  },
  "relationship_delta": {
    "deck_theory_faction->player": 0.04,
    "player->deck_theory_faction": -0.01,
    "rival_lab_b->deck_theory_faction": -0.07,
    "lab_a->deck_theory_faction": 0.02
  },
  "next_event_hooks": [
    {
      "hook_type": "npc_conflict",
      "condition": "rival_lab_b challenges the legitimacy of the faction claim"
    },
    {
      "hook_type": "rumor_seeded",
      "condition": "rival response reframes the claim as opportunistic"
    },
    {
      "hook_type": "faction_event",
      "condition": "player later accepts or rejects the faction label"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `claim_strength`, `claim_legitimacy`, `identity_capture_risk`,
  `alignment_delta`, and `rivalry_pressure`.
- If `player_consent_signal` is unknown, faction claims must stay labeled as
  claims rather than accepted identity.
- If `claim_strength > claim_legitimacy`, increase `identity_capture_risk`.
- Rival factions gain reply pressure when `rival_attention >= 0.50`.
- Alignment can drift toward the claiming faction without increasing the
  player's own affinity.

### Risks

- Faction claims can erase player agency if consent is assumed.
- A faction event can look like final lore if the model emits prose instead of
  state.
- Rivalry pressure should not revive the old bug rumor unless a new
  `rumor_seeded` event explicitly does that.

### Next Round Entry

Use `npc_conflict` next. It can test whether the rival challenge becomes a
relationship conflict rather than immediately becoming a rumor.

## Working Log: 2026-04-27 Round 7

### Round Event

`npc_conflict`

This round models a rival analyst challenging the faction claim around the
player's achievement. The conflict is public, but the model keeps it as a
relationship and stance dispute unless someone adds an unverified factual claim.

Minimal input:

```json
{
  "event_id": "evt_20260427_npc_conflict_001",
  "event_type": "npc_conflict",
  "turn": 25,
  "visibility": "public_bbs",
  "source_actor": "rival_lab_b_analyst",
  "target_refs": [
    "deck_theory_faction",
    "player",
    "evt_20260427_faction_claim_001"
  ],
  "evidence": {
    "conflict_kind": "claim_legitimacy_challenge",
    "grievance_strength": 0.56,
    "conflict_visibility": 0.68,
    "evidence_quality": 0.46,
    "tone_pressure": 0.52,
    "mediation_capacity": 0.39,
    "repair_offer_strength": 0.18
  },
  "faction_refs": ["rival_lab_b", "deck_theory_faction", "lab_a"]
}
```

### Model Increment

This slice adds a conflict-before-rumor path:

`npc_conflict -> relationship dispute -> stance polarization -> escalation hook`

Newly named derived signals:

- `grievance_strength`: how strongly the source actor objects to the target.
- `conflict_visibility`: public reach of the dispute.
- `tone_pressure`: likelihood that replies shift from analysis to personal
  attack or faction pile-on.
- `mediation_capacity`: ability of moderators or respected actors to keep the
  dispute bounded.
- `repair_offer_strength`: visible attempt to cool or clarify the conflict.
- `escalation_risk`: chance that conflict becomes `rumor_seeded` or `scandal`.

### Example `thread_state`

```json
{
  "thread_state": {
    "thread_id": "bbs_thread_unusual_deck_018_001",
    "status": "relationship_conflict_active",
    "updated_turn": 25,
    "topic_heat": 0.86,
    "reply_pressure": 0.62,
    "public_sentiment": 0.43,
    "moderation_boundary": {
      "private_detail_allowed": false,
      "personal_attack_allowed": false,
      "claim_requires_evidence_above": 0.55,
      "faction_label_attack_blocked": true
    }
  },
  "participant_roles": {
    "rival_lab_b_analyst": "conflict_source",
    "deck_theory_faction": "conflict_target",
    "player": "disputed_subject",
    "lab_a": "possible_mediator",
    "moderator": "tone_boundary_keeper"
  },
  "stance_distribution": {
    "support": 0.24,
    "skepticism": 0.19,
    "theorycraft": 0.12,
    "prestige_claim": 0.16,
    "factional_rivalry": 0.22,
    "moderator_neutral": 0.07
  },
  "conflict_state": {
    "conflict_id": "conflict_claim_legitimacy_025_001",
    "source_actor": "rival_lab_b_analyst",
    "target_actor": "deck_theory_faction",
    "grievance_strength": 0.56,
    "conflict_visibility": 0.68,
    "tone_pressure": 0.52,
    "mediation_capacity": 0.39,
    "repair_offer_strength": 0.18,
    "escalation_risk": 0.47,
    "rumor_boundary_crossed": false
  },
  "heat_delta": {
    "topic_heat": 0.04,
    "faction_heat": 0.10,
    "conflict_heat": 0.33,
    "rumor_heat": 0.00,
    "reply_pressure": 0.08
  },
  "relationship_delta": {
    "rival_lab_b_analyst->deck_theory_faction": -0.09,
    "deck_theory_faction->rival_lab_b_analyst": -0.07,
    "player->rival_lab_b_analyst": -0.02,
    "lab_a->player": 0.01
  },
  "next_event_hooks": [
    {
      "hook_type": "relationship_repair",
      "condition": "repair_offer_strength increases before escalation_risk exceeds 0.60"
    },
    {
      "hook_type": "rumor_seeded",
      "condition": "conflict source adds an unverified factual accusation"
    },
    {
      "hook_type": "moderation_boundary",
      "condition": "tone_pressure exceeds mediation_capacity"
    }
  ]
}
```

### New State Variables / Transition Rules

- Added `conflict_state` as separate from `rumor_state`.
- Added `grievance_strength`, `conflict_visibility`, `tone_pressure`,
  `mediation_capacity`, `repair_offer_strength`, and `escalation_risk`.
- If no unverified factual claim is present, keep `rumor_boundary_crossed` false.
- If `tone_pressure > mediation_capacity`, increase reply pressure and
  relationship damage.
- If `repair_offer_strength` rises before escalation, reduce conflict heat
  without changing topic memory.

### Risks

- Public conflict can be mistaken for rumor just because it is heated.
- Over-strong moderation can erase useful rivalry and make the BBS too flat.
- Relationship damage should be directed, not applied as global dislike.

### Next Round Entry

Use `rumor_seeded` next. It can test the boundary where a conflict actor adds an
unverified factual claim and crosses from rivalry into rumor spread.
