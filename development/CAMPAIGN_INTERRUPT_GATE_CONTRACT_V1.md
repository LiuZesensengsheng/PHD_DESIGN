# Campaign Interrupt Gate Contract V1

## Goal

Make `TURN_INTERRUPTS` executions readable as an explicit contract instead of
leaving recheck callers with only a raw lifecycle context or no readable result
at all.

## Why This Exists

The lifecycle machine already had explicit result objects for:

- turn-cycle execution
- return-resolution execution
- startup execution

But the interrupt-gate path still had one asymmetry:

- `run_turn_interrupts()` returned only `CampaignLifecycleContext`
- later recheck paths such as startup completion, reward resolution, or meeting
  prompt dismiss could trigger the gates again
- those rechecks had no dedicated result contract or snapshot surface

That was still workable, but it kept interrupt rechecks less explicit than the
other lifecycle entrypoints.

## Contract

`TURN_INTERRUPTS` now has an explicit result contract:

- `CampaignInterruptGateResult`
- `CampaignInterruptGateStatus`

The result answers:

- did the gates reach `TURN_IDLE`
- or did some interrupt gate remain blocking
- which gate blocked
- what the final lifecycle phase became

## Current Ownership

- `CampaignLifecycleMachine.run_turn_interrupts()` remains the canonical gate
  executor
- `CampaignLifecycleMachine.run_turn_interrupts_result()` is the explicit
  result-returning seam
- `CampaignState.recheck_turn_interrupts()` keeps the legacy context-returning
  host seam for compatibility
- `CampaignState.recheck_turn_interrupts_result()` is the explicit state-level
  result seam

## Read Surface

`CampaignLifecycleSnapshot` now also exposes the latest interrupt-gate summary:

- `interrupt_gate_status`
- `interrupt_gate_blocking_step`

This lets later readers inspect the last gate outcome without reconstructing it
from:

- `current_phase`
- startup result
- turn-cycle result
- ad-hoc caller memory

## Current Intended Use

Use the explicit interrupt-gate result when the caller needs to reason about
what happened during a standalone gate recheck.

Examples:

- startup orchestration after startup-only effects
- later reward / prompt close flows when a follow-up read surface is useful

Use the older context-returning seam only where compatibility still matters.

## Non-Goals

This cut does not:

- create a broader interrupt platform
- replace `CampaignTurnCycleResult` or `CampaignStartupResult`
- reopen `CampaignView` or runtime UI ownership
- redesign reward / meeting / forced-event gating order

## Verification

V1 is protected by focused tests covering:

- explicit interrupt-gate result creation
- machine-side latest interrupt-gate result tracking
- lifecycle snapshot exposure of interrupt-gate summary fields
- state-level interrupt result seam handoff
- startup orchestrator delegation through the new explicit result seam

## Next Cut

The next lifecycle-side hardening work should stay narrow:

- continue tightening explicit lifecycle result and read surfaces
- do not widen back into broad campaign cleanup
