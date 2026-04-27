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
