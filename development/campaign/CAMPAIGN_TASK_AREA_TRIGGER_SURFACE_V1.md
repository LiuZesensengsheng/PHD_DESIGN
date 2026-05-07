# Campaign Task Area Trigger Surface V1

## Goal

Add one stable, explicit trigger-consumption surface for future campaign
traits, forced events, and task-area reactions, without reopening another
whole-campaign rewrite.

This is a focused execution contract layered on top of the existing lifecycle
machine and task-area seams.

- Level: `L3 Architecture`
- Date: `2026-04-22`

## Problem

The campaign runtime already had two useful but incomplete sources of timing
information:

- lifecycle timing windows
- task-area domain events in `state.domain_events`

Neither one was a good final consumer surface on its own.

Why not windows alone:

- windows tell us *when* the shell is in a stable timing edge
- they do not tell us which concrete task-area fact happened inside the turn

Why not raw `domain_events` alone:

- they tell us *what happened*
- they are still a low-level fact log and rollback detail
- consumers would still need to guess phase/step timing by reading lifecycle
  internals

That would make future trait/event work AI-unfriendly again:

- some reactions would bind to windows
- some reactions would peek directly at `state.domain_events`
- phase/step context would remain implicit

## Decision

Keep the existing lifecycle windows as the canonical shell timing edges, but
collect them together with task-area domain events into one explicit trigger
surface.

Current trigger kinds:

- `window`
- `domain_event`

Current stable record shape:

- `sequence`
- `trigger_kind`
- `current_turn`
- `phase`
- `step`
- `window`
- `domain_event_type`
- `payload`

This shape is defined by:

- `contexts/campaign/domain/campaign_trigger.py`

## Canonical Inputs

### 1. Lifecycle Window Triggers

These are emitted by the lifecycle layer itself, not by arbitrary UI/runtime
callers.

Current windows:

- `AFTER_COMBAT_RETURN`
- `BEFORE_TURN_ADVANCE`
- `AFTER_TURN_ADVANCE`
- `AFTER_BOARD_STABILIZED`
- `AFTER_FORCED_DDL_REFRESH`
- `BEFORE_INTERRUPT_GATES`
- `TURN_IDLE_ENTER`

Each window trigger records:

- the current lifecycle `phase`
- the most relevant lifecycle `step`
- the current campaign turn at the time of emission

### 2. Task-Area Domain-Event Triggers

These are emitted through the shell seam:

- `CampaignState.record_campaign_domain_event(...)`

Current domain-event producers routed into the trigger surface:

- turn advancement:
  - `TurnAdvanced`
- task-area fusion:
  - `BlocksFused`
- DDL snake consumption:
  - `DdlAteBlock`

Each domain-event trigger records:

- the current lifecycle `phase` when available
- the currently active lifecycle `step` when available
- a stable `domain_event_type`
- a copied event `payload`

## Consumer Surface

Future trait/event consumers should prefer these state seams:

- `peek_campaign_triggers()`
- `consume_campaign_triggers()`
- `clear_campaign_triggers()`

Lifecycle/runtime ownership still uses the write-side seams:

- `set_active_campaign_trigger_step(...)`
- `record_campaign_window_trigger(...)`
- `record_campaign_domain_event(...)`

Rollback/checkpoint ownership uses:

- `snapshot_campaign_trigger_state()`
- `restore_campaign_trigger_state(...)`

Important ownership rule:

- the concrete trigger collector lives at
  `state.interaction_services.trigger_surface`
- it is intentionally **grouped-only**
- it should not regain a direct `state.trigger_surface` alias

## Relationship To `domain_events`

`state.domain_events` still exists for now.

Current stance:

- keep it for rollback/internal continuity
- keep existing tests that verify important task-area facts are appended there
- do **not** treat it as the preferred future consumer surface

New campaign reaction logic should stop reading raw `domain_events` directly
unless it is specifically working on low-level recovery/rollback behavior.

## Current Consumer Baseline

The first production trigger consumers now live in:

- `contexts/campaign/services/campaign_trigger_reaction_service.py`

Important runtime rule:

- production consumers should **not** drain the trigger queue during normal
  gameplay
- instead, the reaction service tracks `last_processed_sequence` and replays
  only new trigger records

Current production reactions:

- `AFTER_COMBAT_RETURN`
  - if the player owns `trait_introvert`, grant `+1 inspiration`
- `AFTER_FORCED_DDL_REFRESH`
  - advance `line_bubbles`
  - if the player owns `trait_extravert`, increment the gossip badge once more
- `DdlAteBlock`
  - queue one pending forced-event payload
  - surface it through `TURN_INTERRUPTS -> FORCED_EVENT_GATE`

Current ownership split after this cut:

- lifecycle hook binding still owns stable shell/system window hooks such as:
  - elapsed-time label refresh
  - baseline gossip badge increment
- built-in line-bubble / introvert / extravert reactions are no longer owned by
  lifecycle hook registration
- those reactions now run through the trigger surface so future trait/event work
  has one explicit campaign reaction path

## Rollback Contract

Trigger collection must stay atomic with turn advancement.

So `CampaignTurnOrchestrator` now checkpoints and restores:

- pending trigger records
- next trigger sequence id

This prevents half-written trigger buffers from surviving when turn
advancement, board stabilization, or compaction fails partway through.

## Non-Goals

This V1 trigger surface does **not** mean:

- a generic scripting engine
- a new universal campaign node tree
- a replacement for lifecycle phase ownership
- a replacement for task-area domain events themselves

The lifecycle machine still owns *when* campaign phases advance.
The task area still owns *what* board/domain facts occur.
The trigger surface is the stable bridge that future reactive content should
consume.

## Current Bottom Line

After this cut, campaign timing is more explicit for AI and human developers:

- lifecycle windows remain the canonical timing edges
- task-area facts remain explicit domain events
- future traits/events now have one stable trigger queue instead of two
  unrelated low-level surfaces
