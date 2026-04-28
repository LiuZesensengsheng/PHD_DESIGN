# Gossip/BBS Social Simulation Integration Plan V1

## Purpose

Plan the first safe integration path for
`gossip_bbs_social_simulation_model_v1`.

The V1 sidecar already owns structured event inputs, transition inputs,
simulation state patches, and result payloads. Integration should connect that
sidecar to campaign/combat/narrative facts without turning it into UI,
persistence, card analysis, or prose generation.

The recommended integration shape is a sidecar reaction pipeline:

1. upstream campaign/combat/narrative systems expose reviewed facts;
2. an adapter maps those facts into `GossipEventInput` or
   `GossipTransitionInput`;
3. a runtime application service owns a `GossipSimulationState` instance and
   applies sidecar transitions;
4. presentation reads structured outputs later through a separate read model.

## Non-Goals

- Do not implement campaign integration in this planning pass.
- Do not add UI or replace the current lightweight gossip modal/badge flow.
- Do not write final BBS/forum prose.
- Do not call an LLM.
- Do not add a database.
- Do not mutate campaign save schema or add a persistence migration yet.
- Do not couple to `cardanalysis`.
- Do not make forced-event runtime the Gossip/BBS owner.
- Do not put sidecar transition calls directly into runtime widgets.

## Current Sidecar Surface

The sidecar lives under:

- `contexts/gossip_bbs_social_simulation/contracts.py`
- `contexts/gossip_bbs_social_simulation/transitions.py`

Stable inputs:

- `GossipEventInput`
- `GossipTransitionInput`

Stable state owner:

- `GossipSimulationState`

Stable result envelope:

- `thread_state`
- `additional_thread_states`
- `participant_roles`
- `stance_distribution`
- `rumor_state`
- `heat_delta`
- `relationship_delta`
- `memory_state`
- `path_states`
- `state_patches`
- `next_event_hooks`
- `warnings`

Supported event types:

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

Supported transition types:

- `decay`
- `reply_pressure`

The sidecar must remain domain-only. It may validate structured state and emit
structured patches, but it must not know campaign UI, save format, card-analysis
services, or narrative text rendering.

## Existing Campaign/Social Surfaces

Campaign timing windows currently include:

- `AFTER_COMBAT_RETURN`
- `BEFORE_TURN_ADVANCE`
- `AFTER_TURN_ADVANCE`
- `AFTER_BOARD_STABILIZED`
- `AFTER_FORCED_DDL_REFRESH`
- `BEFORE_INTERRUPT_GATES`
- `TURN_IDLE_ENTER`

Existing binding/reaction services already use some of these windows:

- `CampaignLifecycleBindingService`
  - `AFTER_TURN_ADVANCE` refreshes elapsed time label.
  - `AFTER_FORCED_DDL_REFRESH` increments the existing lightweight gossip badge.
- `CampaignTriggerReactionService`
  - `AFTER_COMBAT_RETURN` applies introvert inspiration.
  - `AFTER_FORCED_DDL_REFRESH` advances line bubbles and extravert gossip badge.
  - domain-event triggers may queue catalog forced events.

Campaign domain events currently include:

- `TurnAdvanced`
- `BlocksFused`
- `DdlAteBlock`
- `BlockStalled`
- `BlocksSpawned`

The current social/gossip UI flow is lightweight flavor presentation, not the
same system as the BBS simulation sidecar. It can become a later consumer of a
small read model, but it should not own the sidecar state or transition rules.

## Recommended Integration Shape

Keep dependencies one-way:

```text
campaign/combat/narrative facts
    -> campaign-owned adapter
    -> GossipEventInput / GossipTransitionInput
    -> GossipBbsRuntimeService
    -> contexts.gossip_bbs_social_simulation
    -> structured read model
    -> optional future presentation
```

Dependency rules:

- `contexts.gossip_bbs_social_simulation` imports no campaign modules.
- A future campaign integration module may import sidecar contracts and
  transition functions.
- Lifecycle hooks may call a campaign-owned service interface, not sidecar
  functions directly.
- Runtime UI widgets must not import sidecar transition functions.
- Forced-event runtime must not become the sidecar queue or state owner.
- Existing gossip badge/modal services may later consume aggregate read-model
  hints, not raw simulation internals.

## Proposed New Integration Units

### `GossipBbsEventAdapter`

Responsibility:

- Translate reviewed upstream facts into zero or more sidecar inputs.
- Reject underspecified facts by returning no inputs plus warnings.
- Keep all mapping deterministic.
- Preserve event IDs and upstream refs for traceability.

Suggested home:

- `contexts/campaign/services/gossip_bbs_event_adapter.py`

Reason:

- The adapter knows campaign fact shapes.
- The sidecar should not import campaign classes.
- A service module keeps it out of runtime widgets and forced-event runtime.

Minimal contract sketch:

```python
@dataclass(frozen=True)
class GossipBbsAdapterOutput:
    events: tuple[GossipEventInput, ...] = ()
    transitions: tuple[GossipTransitionInput, ...] = ()
    warnings: tuple[str, ...] = ()
```

### `GossipBbsRuntimeService`

Responsibility:

- Own an in-memory `GossipSimulationState`.
- Apply adapter outputs in caller-provided order.
- Store the latest structured result envelopes for later read-model projection.
- Expose snapshot/restore only after a persistence decision is made.

Suggested home:

- `contexts/campaign/services/gossip_bbs_runtime_service.py`

Initial boundary:

- In-memory only.
- No `persistent` writes.
- No UI calls.
- No LLM calls.
- No card-analysis calls.

### `GossipBbsReadModel`

Responsibility:

- Project structured result/state into small presentation-safe facts.
- Keep copy-free keys such as thread IDs, heat deltas, unread counts, and stance
  buckets.
- Avoid final forum text or dialogue.

Suggested first shape:

```python
@dataclass(frozen=True)
class GossipBbsReadModel:
    active_thread_ids: tuple[str, ...]
    heated_topic_ids: tuple[str, ...]
    unread_thread_count: int
    pending_hook_types: tuple[str, ...]
```

## Integration Phases

### Phase 0: Current Planning State

Status:

- Sidecar remains isolated.
- Integration plan is documentation only.
- No campaign runtime code changes.

Exit criteria:

- Plan documents dependency boundaries, candidate producers, state ownership,
  stop lines, and first implementation slice.

### Phase 1: Adapter Contract And Fixtures

Goal:

- Add a pure adapter contract with tests against reviewed fixture payloads.

Recommended first input:

- `AFTER_COMBAT_RETURN` fact representing a public combat result.

Recommended first output:

- one `combat_result` `GossipEventInput`;
- optional `boss_defeated` input only when the upstream fact explicitly marks a
  boss/milestone outcome;
- no sidecar state mutation.

Validation:

- Adapter unit tests assert exact sidecar input mappings.
- Existing sidecar tests remain unchanged.

Stop lines:

- Do not call `simulate_event` from the adapter.
- Do not infer deck identity from card-analysis systems.
- Do not generate prose.

### Phase 2: Runtime Service

Goal:

- Add a campaign-owned runtime service that can apply already-created sidecar
  inputs to an in-memory `GossipSimulationState`.

Recommended behavior:

- `apply_adapter_output(output)` applies events and transitions in stable order.
- Each result is stored by `result_id` or source event ID.
- Warnings are collected but do not block campaign flow.

Validation:

- Unit test sequential application of `combat_result`, `reply_pressure`, and
  `decay` using fixture inputs.
- Confirm state patches are applied through `GossipSimulationState.apply_result`.

Stop lines:

- No `persistent` writes.
- No lifecycle hook binding yet unless separately approved.
- No UI presentation.

Implemented Phase 2 surface:

- `contexts/campaign/services/gossip_bbs_runtime_service.py`
- `tests/campaign/test_gossip_bbs_runtime_service.py`

Implemented behavior:

- `GossipBbsRuntimeService` owns runtime-only `GossipSimulationState`.
- `apply_adapter_output(output)` applies events first, then transitions, using
  the sidecar transition functions and `GossipSimulationState.apply_result`.
- Results are indexed by both `result_id` and `source_id`.
- Adapter and transition warnings are accumulated without blocking campaign
  flow.
- `clear_runtime()` clears only in-memory runtime state.

Implemented validation:

- public combat adapter output updates runtime thread and memory state;
- `combat_result -> reply_pressure -> decay` applies in deterministic order;
- adapter warnings with no events create no sidecar results;
- runtime imports stay free of UI, pygame, `persistent`, `gossip_modal`, and
  `cardanalysis`.

### Phase 3: Lifecycle Hook Wiring

Goal:

- Connect runtime service to explicit campaign timing windows.

Preferred windows:

- `AFTER_COMBAT_RETURN`
  - candidate producer for `combat_result`, `boss_defeated`,
    `public_achievement`, and `player_used_unusual_deck` when facts are
    explicit.
- `AFTER_FORCED_DDL_REFRESH`
  - candidate producer for `reply_pressure` or lightweight topic heat refresh
    after campaign pressure changes.
- `TURN_IDLE_ENTER`
  - candidate point for low-risk `decay` after campaign state has stabilized.

Implementation rule:

- Lifecycle hook calls a campaign-owned integration service.
- The hook does not import or call sidecar transition functions directly.

Stop lines:

- Do not add sidecar calls to `CampaignTriggerReactionService` as an inline
  branch. That service is already responsible for trait and forced-event
  reactions; mixing BBS simulation into it would make the integration owner
  ambiguous.
- Do not route through forced-event runtime.

### Phase 4: Read Model Consumer

Goal:

- Let presentation see only small structured hints.

Possible first consumer:

- Existing gossip badge count can eventually read aggregate "active heated
  threads" or "unread structured updates".

Boundary:

- The badge/modal flow should not own thread state.
- Read model must not expose final prose fields.
- Any future modal/feed work is a separate UI task.

### Phase 5: Persistence Decision

Goal:

- Decide whether sidecar state belongs in campaign save data.

Decision inputs:

- Does the BBS state need to survive reload?
- Is it player-visible enough to require consistency across sessions?
- Can it be recomputed from event history, or does it need stored state?
- What migration path handles older saves with no BBS state?

Default until decided:

- Runtime-only state.

Stop lines:

- Do not write `persistent` opportunistically.
- Do not add a migration only to support planning/demo behavior.

### Phase 6: Text And LLM Boundaries

Goal:

- Decide later how structured thread state becomes player-facing copy.

Allowed later path:

- A separate presentation/prose layer maps structured state plus approved copy
  templates into UI output.

Disallowed in V1 integration:

- sidecar-generated forum posts;
- unreviewed narrative text;
- LLM calls from campaign lifecycle hooks;
- storing raw generated dialogue in simulation state.

## Candidate Upstream Producers

### Combat Return

Window:

- `AFTER_COMBAT_RETURN`

Candidate facts:

- combat result ID;
- encounter ID;
- outcome;
- turn;
- player-visible achievement flags;
- explicit boss/milestone flag;
- explicit public package/card refs when already known by campaign.

Candidate sidecar inputs:

- `combat_result`
- `boss_defeated`
- `player_used_unusual_deck`
- `public_achievement`

Risk:

- "Unusual deck" must be an explicit upstream fact or a reviewed heuristic local
  to the adapter. It must not call `cardanalysis`.

### Turn Advancement

Window:

- `AFTER_TURN_ADVANCE` or `TURN_IDLE_ENTER`

Candidate facts:

- old turn;
- new turn;
- pending active thread refs from runtime state.

Candidate sidecar inputs:

- `decay`
- `reply_pressure`

Risk:

- Decay timing must be deterministic and should not run multiple times for the
  same turn.

### Forced DDL Refresh

Window:

- `AFTER_FORCED_DDL_REFRESH`

Candidate facts:

- campaign pressure changed;
- public deadline-related faction pressure if explicitly modeled.

Candidate sidecar inputs:

- `reply_pressure`
- possibly `faction_event` only after a reviewed faction fact exists.

Risk:

- Existing gossip badge updates already run here. The BBS sidecar should not
  duplicate badge presentation logic.

### Narrative / NPC Conflict

Potential future producer:

- reviewed narrative/campaign event facts, not freeform text.

Candidate sidecar inputs:

- `npc_conflict`
- `misunderstanding`
- `scandal`
- `private_leak`
- `rumor_seeded`
- `rumor_debunked`

Risk:

- These events can easily imply private truth or final story copy. Integration
  must require explicit visibility, evidence, and moderation boundary fields.

## State Ownership Options

### Option A: Runtime-Only State

Use initially.

Pros:

- no migration;
- low blast radius;
- easy to test;
- respects current planning boundary.

Cons:

- state resets on reload;
- cannot yet support long-lived BBS continuity.

### Option B: Persisted Snapshot

Use only after a product decision.

Pros:

- survives reload;
- supports long-term memory and thread lifetime.

Cons:

- needs save schema decision;
- needs migration and compatibility tests;
- creates higher regression risk.

### Option C: Recompute From Event History

Consider later only if campaign keeps a compact reviewed event history.

Pros:

- avoids storing derived state;
- easier to inspect causality.

Cons:

- requires stable event retention;
- could become expensive or order-sensitive.

Recommendation:

- Start with Option A.
- Do not choose Option B or C in the first integration slice.

## First Implementation Slice

The first code slice is docs/test-first and narrow:

1. Add `GossipBbsEventAdapter` contract and fixture tests.
2. Map exactly one reviewed `AFTER_COMBAT_RETURN` fixture to a
   `combat_result` `GossipEventInput`.
3. Add one negative fixture where missing public evidence produces no event and
   a warning.
4. Do not instantiate `GossipBbsRuntimeService`.
5. Do not wire lifecycle hooks.

Implemented first-slice surface:

- `contexts/campaign/services/gossip_bbs_event_adapter.py`
- `tests/campaign/test_gossip_bbs_event_adapter.py`

The test target follows the repository's current campaign test layout, where
service tests live directly under `tests/campaign/`.

Validation:

- `py -3.11 -m pytest tests/campaign/test_gossip_bbs_event_adapter.py -q`
- `py -3.11 -m pytest tests/gossip_bbs_social_simulation -q`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`
- `git diff --check`

## Risks And Stop Signals

Stop and re-plan if any first integration slice requires:

- writing `persistent`;
- changing save schema;
- editing runtime UI widgets;
- modifying forced-event runtime ownership;
- importing campaign modules from the sidecar;
- calling card-analysis services;
- calling an LLM;
- adding final forum copy to result payloads;
- inferring private truth from public rumor state;
- broad changes to campaign lifecycle ordering.

## Open Questions

- Which campaign object will own reviewed combat-return facts?
- Should the first adapter live under `contexts/campaign/services/` or a more
  explicit future `contexts/campaign/social/` package?
- Should runtime-only BBS state be reset on every campaign session start, or
  can it persist within a single process-level campaign state?
- Which aggregate read-model field is most useful for the existing gossip badge:
  active thread count, heat delta, unread result count, or pending hook count?

## Decision

Proceed with integration only through a campaign-owned adapter and runtime
service. Keep V1 sidecar pure, copy-free, UI-free, save-free, LLM-free, and
card-analysis-free until a separate integration decision changes one boundary
at a time.
