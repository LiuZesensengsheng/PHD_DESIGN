# Campaign Forced Event Narrow Plan V1

## Goal

Define a narrow long-term architecture for campaign forced events that keeps
the current lifecycle/trigger-surface direction, without reopening a broad
campaign interrupt-platform rewrite.

- Level: `L3 Architecture`
- Date: `2026-04-23`

## Problem

Campaign now has a real forced-event path, but it is still intentionally
minimal and partly transitional.

Current production path:

- trigger detection lives in
  `contexts/campaign/services/campaign_trigger_reaction_service.py`
- interrupt ownership lives in
  `contexts/campaign/lifecycle/steps/interrupt_gate_steps.py`
- state-level host seam lives in
  `contexts/campaign/state.py`

What works today:

- `DdlAteBlock` can enqueue one pending forced-event payload
- `TURN_INTERRUPTS -> FORCED_EVENT_GATE` can block idle entry
- the gate can open a modal and release back to normal flow
- runtime snapshot/restore already covers trigger-reaction state

What is still too temporary for the long term:

- pending forced-event state is still a raw `dict`
- the trigger reaction service currently owns both:
  - forced-event detection
  - forced-event presentation opening
- presentation currently reuses `gossip_modal` directly
- there is no explicit forced-event runtime owner with a stable queue contract

If more forced events are added on top of the current shape, the project risks
growing a second ad-hoc reaction/prompt path next to the lifecycle machine.

## Constraints

- Keep the work inside `contexts/campaign/**`.
- Preserve the existing lifecycle machine and trigger surface as the timing
  baseline.
- Do not reopen `contexts/campaign/view.py` or a broad runtime UI rewrite.
- Do not widen the task into a unified reward/meeting/forced-event platform.
- Preserve rollback/checkpoint behavior for turn advancement.
- Keep the result AI-friendly:
  - explicit owner
  - explicit queue semantics
  - explicit stop line

## Complexity

### Essential Complexity

Forced events genuinely need four things:

1. explicit detection
2. explicit pending/runtime ownership
3. explicit interrupt-gate integration
4. explicit presentation/resolution flow

Those needs are real and will not disappear if the code is rearranged.

### Accidental Complexity

The current accidental complexity comes from the temporary owner shape:

- `_pending_forced_event` is still embedded inside
  `CampaignTriggerReactionService`
- presentation opening still happens from the reaction service itself
- forced-event payloads are still untyped dictionaries
- the current path reuses `gossip_modal`, which is practical now but hides the
  fact that forced events are their own interrupt family

### What The Project Actually Needs

The project does **not** need right now:

- a generic campaign scripting engine
- a unified interrupt framework for reward/meeting/forced-event together
- a dedicated new modal UI system

The project **does** need:

- one explicit forced-event runtime owner
- one explicit forced-event model
- one explicit gate-to-presenter path
- one explicit small-slice rollout plan

## Options

### Option A: Keep The Current Minimal Forced-Event Path

What it means:

- keep `_pending_forced_event` inside `CampaignTriggerReactionService`
- keep modal opening in the same service
- add future forced events by extending the existing `if/elif` branches

Pros:

- cheapest short-term path
- no new service split immediately

Cons:

- reaction ownership and presentation ownership stay mixed
- future forced events will expand a temporary service instead of a stable seam
- AI will still need to edit the same service for unrelated concerns

### Option B: Build A Narrow Long-Term Forced-Event Path

What it means:

- keep trigger detection on the trigger surface path
- add a dedicated forced-event runtime owner
- keep `FORCED_EVENT_GATE` as the lifecycle insertion point
- split presentation opening behind a small dedicated seam
- do **not** unify reward/meeting/forced-event into one platform yet

Pros:

- gives forced events an explicit stable owner
- keeps scope small enough for serial landing
- preserves the campaign lifecycle direction already chosen
- AI can extend forced events without reopening unrelated systems

Cons:

- adds 1-2 focused services
- leaves the broader interrupt family intentionally not-yet-unified

### Option C: Build A Broad Unified Interrupt Platform Now

What it means:

- redesign reward, meeting, and forced-event handling under one generalized
  interrupt runtime and presenter stack

Pros:

- strongest long-term symmetry story if completed well

Cons:

- highest scope and migration risk
- likely to drag UI/runtime concerns into the same slice
- not required to stabilize forced events themselves

## Risks

### Risk If We Stay Temporary

- `CampaignTriggerReactionService` will keep accumulating unrelated logic
- forced-event payloads will drift as ad-hoc dictionaries
- future contributors may bypass the lifecycle gate and open prompts directly

### Risk If We Over-Build Too Early

- reward/meeting/forced-event concerns may get entangled
- work may spill into `CampaignView`, modal UI, or broad interrupt redesign
- automation slices become too large and too decision-heavy

### Specific Technical Risks To Manage

- modal owner ordering must remain correct relative to:
  - reward gate
  - meeting gate
  - forced-event gate
- checkpoint restore must not replay already-consumed trigger reactions
- a failed modal open must not incorrectly enter `TURN_IDLE`
- coalescing multiple same-turn forced events must stay deterministic

## Recommendation

Choose **Option B**.

Adopt a narrow long-term forced-event plan with the following target shape.

### 1. Keep Trigger Detection On The Trigger Surface Path

`CampaignTriggerReactionService` should continue to decide when a trigger
produces a forced event.

But its role should narrow to:

- detect trigger
- build a forced-event model
- enqueue it into a dedicated runtime owner

It should stop directly opening UI.

### 2. Add An Explicit Forced-Event Runtime Owner

Recommended new owner:

- `CampaignForcedEventRuntimeService`

Recommended first responsibility set:

- hold pending forced events
- hold the currently active forced event when needed
- coalesce or append incoming events by explicit rules
- expose snapshot/restore
- expose one gate-facing operation such as:
  - `open_next_if_possible()`
  - or `handle_gate()`

This service should remain grouped under campaign interaction/runtime ownership
and should not become a new direct `CampaignState` leaf alias.

### 3. Use A Small Explicit Forced-Event Model

Recommended first model shape:

- `event_id`
- `title`
- `text`
- `source_trigger_sequence`
- `priority`
- `coalescing_key`
- `payload`

Important decision:

- this model is runtime-first for now
- do **not** widen this slice into a persistent save-schema redesign

### 4. Keep `FORCED_EVENT_GATE` As The Only Mandatory Entry Point

The lifecycle insertion point is already correct:

- `TURN_INTERRUPTS -> FORCED_EVENT_GATE`

That should remain the only mandatory forced-interrupt opening seam.

This avoids reintroducing:

- frame-time prompt checks
- direct modal opens from arbitrary business services

### 5. Split Presentation Behind A Dedicated Seam

Recommended seam:

- `CampaignForcedEventPresentationService`

Short-term implementation rule:

- this presenter may internally reuse current modal capabilities
- it may even still render through the current visual style initially
- but the runtime owner and reaction service should stop depending on
  `gossip_modal` directly

### 6. Stop Line

This plan explicitly does **not** include:

- reward gate redesign
- meeting prompt redesign
- generalized interrupt family unification
- new forced-event content design beyond the minimum event needed to validate
  the seam

## Execution Slices

These slices are intended to be automation-friendly and serially landable.

### Slice 1: Explicit Model + Runtime Owner

Scope:

- add `CampaignForcedEventRecord` or equivalent explicit runtime model
- add `CampaignForcedEventRuntimeService`
- move `_pending_forced_event` ownership out of
  `CampaignTriggerReactionService`
- preserve current gate behavior and current visible UX

Deliverables:

- explicit model file
- runtime owner with snapshot/restore
- reaction service enqueues model objects instead of raw modal payload dicts

Validation:

- focused forced-event runtime tests
- existing campaign trigger-reaction tests stay green
- `tests/campaign -q`

Stop and ask if:

- runtime model seems to require save-schema persistence
- more than one active forced event is needed immediately

### Slice 2: Presenter Seam Extraction

Scope:

- add `CampaignForcedEventPresentationService`
- move modal-open logic out of `CampaignTriggerReactionService`
- gate/runtime owner now call presenter instead of `gossip_modal` directly

Deliverables:

- explicit presenter service
- gate/runtime tests for open failure and retry behavior
- no direct `gossip_modal` dependency from trigger reaction service

Validation:

- focused presenter/gate tests
- `tests/campaign -q`

Stop and ask if:

- this requires a new visual component instead of a seam extraction

### Slice 3: Resolution Flow And Gate Contract Tightening

Scope:

- make active/pending forced-event states explicit
- define what happens when:
  - a modal is already open
  - multiple events are queued
  - a present attempt fails
- ensure gate semantics remain deterministic

Deliverables:

- explicit runtime state transitions
- tests for:
  - blocked owner
  - retry path
  - multi-event coalescing/order

Validation:

- focused forced-event gate flow tests
- `tests/campaign/test_campaign_lifecycle_machine.py -q`
- `tests/campaign -q`

Stop and ask if:

- product behavior for queue order or coalescing becomes ambiguous

### Slice 4: First Extension Guardrail

Scope:

- add one additional reaction-friendly forced-event path or explicit catalog hook
- add guardrails so future forced events follow the same enqueue/runtime/gate
  path instead of opening prompts directly

Deliverables:

- one more concrete forced-event producer or catalog registration path
- guardrail tests or architecture assertions against direct forced-event modal
  opens from unrelated services

Current V1 landing choice:

- prefer an explicit catalog hook before adding a second product-heavy
  forced-event family
- the first landed hook lives in:
  - `contexts/campaign/domain/campaign_forced_event_catalog.py`
- `CampaignTriggerReactionService` now routes mapped triggers through that
  catalog and then enqueues the runtime owner

Validation:

- focused new forced-event tests
- `tests/campaign -q`

Stop and ask if:

- the second forced-event family implies a broader product/system redesign

## Counter-Review

Why not keep the current path until more forced events exist?

- because forced events have already entered the production lifecycle path
- the next forced-event addition would otherwise deepen a temporary owner shape

Why not unify reward, meeting, and forced events now?

- because the current need is to stabilize forced events themselves
- broad interrupt unification is a separate architecture decision with higher
  scope and more UI/runtime coupling

Why is reusing current visual style still acceptable in the recommendation?

- because the critical architecture problem is owner clarity, not immediate UI
  differentiation
- separating the presenter seam first reduces risk without forcing a new visual
  implementation in the same slice

This recommendation depends on one assumption:

- the team is willing to keep the forced-event long-term path narrow and not
  automatically widen it into a generalized interrupt framework

## Decision Summary

1. Campaign forced events should move to a narrow long-term architecture now.
2. The chosen path is **not** a broad interrupt-platform rewrite.
3. Trigger detection stays on the trigger-surface path.
4. Pending/active forced-event ownership should move into a dedicated runtime
   service.
5. Presentation should move behind a dedicated presenter seam.
6. `FORCED_EVENT_GATE` remains the only mandatory forced-interrupt entry point.
7. The work should land as four small automation-friendly slices rather than
   one large rewrite.
