# Campaign Modal Lock Contract V1

## Goal

Define the current blocking-modal and input-lock contract for `campaign` so UI
work can safely rely on one explicit rule set instead of implicit owner
behavior.

This is a migration-phase contract. It documents the stable V1 rules we are
using now, not the final end-state architecture.

## Why This Exists

Before this cut, campaign modal behavior was partially correct but still too
implicit:

- multiple blocking surfaces could try to open in the same frame
- lock owner handoff was not always explicit
- some services still treated `_input_locked` as a writable detail instead of a
  coordinated boundary

That made parallel UI work risky because a collaborator could not easily answer:

- which modal owns blocking input right now
- whether a second blocking modal is allowed to open
- who is allowed to release the lock

## Current Blocking Owners

The active blocking owners in V1 are:

- `choice_modal`
- `judgment_modal`
- `gossip`
- `meeting_prompt`

These owners share one campaign-wide blocking lock.

## Contract Rules

### Single Blocking Owner Rule

Only one blocking owner may hold campaign input lock at a time.

If a different owner already holds the lock, a new blocking modal must not open
on top of it.

Practical meaning:

- blocking modal show attempts must fail fast instead of silently overlapping
- the existing owner remains authoritative until it releases the lock

### Lock Acquisition Rule

`ModalCoordinator.lock(owner)` is the stable lock-acquisition seam.

Its V1 behavior is:

- returns `True` when lock ownership is acquired or re-acquired by the same
  owner
- returns `False` when a foreign owner already holds the lock
- writes `_input_locked` and `_input_lock_owner` only when acquisition succeeds

UI-facing code should not guess or recreate this logic locally.

### Lock Release Rule

`ModalCoordinator.unlock(owner)` may only release the matching owner.

V1 behavior:

- matching owner: releases the lock
- non-matching owner: no-op
- `unlock()` with no owner is cleanup-only force release

This prevents one modal flow from accidentally clearing another modal's lock.

### Blocking Show Rule

The following blocking entrypoints now obey the owner contract:

- `ModalCoordinator.show_choices(...)`
- `ModalCoordinator.show_choice_options(...)`
- `ModalCoordinator.show_judgment(..., blocking=True, ...)`
- `MeetingPromptUiService.show()`
- `GossipFlowApplicationService.lock_inputs()`

If a foreign owner already holds the lock, these entrypoints do not open a new
blocking surface.

## Event Routing Rule

Campaign input ingress still follows this order:

1. `CampaignModalDispatchService.dispatch(event)`
2. `CampaignInputLockService.handle_locked_event(event)`
3. keyboard/mouse/button adapters
4. orchestration seams

Meaning:

- visible modals get first shot at consuming input
- if a blocking owner is still active, underlying campaign actions must not run
- meeting prompt remains special: it is rendered as campaign-owned UI but routed
  through the input-lock service under owner `meeting_prompt`

## Deferred Modal Rule

When a blocking modal is already open, later blocking prompts must defer rather
than overlap.

Current important example:

- if reward choice modal opens during startup
- and meeting prompt is also due that turn
- meeting prompt waits until reward modal releases `choice_modal`
- then the next update cycle may open `meeting_prompt`

This is the current safe behavior for parallel UI development.

## Service Ownership Rule

These services may coordinate lock behavior:

- `ModalCoordinator`
- `CampaignInputLockService`
- `CampaignModalDispatchService`
- `MeetingPromptUiService`
- `GossipFlowApplicationService`

These services should not bypass owner-aware release semantics.

In this cut, `LineBubbleService` and thesis judgment unlock flow were also
aligned to reuse the coordinated owner behavior instead of blindly clearing the
lock.

`GossipFlowApplicationService` now also routes lock acquire/release only
through `ModalCoordinator` instead of keeping a direct raw-field fallback.

## Non-Goals

This contract does not:

- introduce modal stacking
- convert all campaign UI into one modal framework
- redesign modal visuals
- remove legacy `_input_locked` storage from `CampaignState`

Current nuance:

- raw storage still exists on `CampaignState`
- direct service-side fallback writes should stay deleted
- owner-aware lock mutation should stay centralized in `ModalCoordinator`

## Safe UI Collaboration Rule

For campaign UI work, assume:

- blocking state is owned by the modal/input-lock seams, not by widgets
- UI code may trigger modal show/hide through stable host seams
- UI code should not directly assign `_input_locked` or `_input_lock_owner`

If a new UI flow needs special lock behavior, add a seam or owner rule instead
of teaching widget code to mutate lock state directly.

## Verification

V1 is currently protected by focused tests covering:

- owner-aware choice modal lock/unlock
- foreign-owner rejection for new blocking modals
- meeting prompt deferral while reward choice modal is active
- gossip lock refusal under foreign owner
- judgment unlock releasing only `judgment_modal`

## Next Cut

With this modal contract in place, the next highest-value campaign handoff task
is:

- `Campaign Block Click Orchestrator V1`
