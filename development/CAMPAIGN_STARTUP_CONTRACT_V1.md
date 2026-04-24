# Campaign Startup Contract V1

## Problem

Campaign lifecycle already had:

- explicit turn-loop result
- explicit return-resolution result
- explicit lifecycle read surface

But startup still remained more implicit than the rest of the lifecycle timing
line.

Current pre-slice behavior:

- `CampaignStartupOrchestrator.startup(...)` owned the startup order
- it delegated into lifecycle-owned `run_return_resolution(...)`
- it later delegated into `recheck_turn_interrupts()`
- but the overall startup outcome still had to be inferred from:
  - mutable machine phase
  - nested return-resolution state
  - whether interrupt gates blocked at the end

That meant startup was still the one major lifecycle entrypoint without one
explicit result contract.

## Constraints

- Keep the slice inside `contexts/campaign/**`.
- Preserve current startup ordering:
  - startup presentation bootstrap
  - hydration
  - lifecycle hook refresh
  - startup return-resolution handoff
  - startup-only effects
  - startup status/inspiration/forced-DDL refresh
  - interrupt recheck
- Do not widen into:
  - startup hydration redesign
  - startup step-graph execution
  - save-schema work
  - broader UI rewrite

## Complexity

### Essential Complexity

Startup genuinely has one composite lifecycle outcome:

1. startup completes and free interaction is entered
2. startup completes but an interrupt gate still blocks free interaction

It also contains one nested lifecycle result that should stay explicit:

- startup return-resolution

### Accidental Complexity

The accidental complexity came from leaving the top-level startup answer split
across:

- orchestrator sequencing
- nested lifecycle calls
- machine mutable phase

## Options

### Option A: Keep Startup Implicit

What it means:

- keep startup as orchestration-only
- let callers inspect nested lifecycle state manually

Pros:

- cheapest immediate path

Cons:

- leaves startup as the odd lifecycle path without an explicit result
- keeps AI readers reconstructing the outcome instead of reading it

### Option B: Add A Narrow Startup Result Contract

What it means:

- keep `CampaignStartupOrchestrator` as the order owner for now
- let `CampaignLifecycleMachine.run_startup(...)` own the explicit startup
  result
- keep nested return-resolution explicit instead of flattening it away

Pros:

- matches the turn / return tightening direction
- stays narrow and runtime-only
- preserves current startup order

Cons:

- adds one more lifecycle result type
- leaves full startup step tracing for a later slice

## Recommendation

Choose **Option B**.

Current V1 contract:

- `CampaignLifecycleMachine.run_startup(...)` now returns
  `CampaignStartupResult`
- `CampaignStartupResult.status` is one of:
  - `COMPLETED_TO_IDLE`
  - `COMPLETED_WITH_INTERRUPT_BLOCK`
- the result also keeps these nested/runtime details explicit:
  - `return_resolution_result`
  - `interrupt_context`
  - `blocking_step`
  - `final_phase`
- `CampaignLifecycleMachine.last_startup_result` keeps the latest startup
  result available for inspection

Supporting seam tightening:

- `CampaignStartupOrchestrator.startup(...)` now delegates the startup mainline
  through `lifecycle_machine.run_startup(...)`
- `CampaignState.recheck_turn_interrupts()` now returns the interrupt context
  instead of discarding it
- lifecycle snapshot now also exposes startup summary fields:
  - `startup_status`
  - `startup_blocking_step`

## Counter-Review

Why not move full startup execution into lifecycle step files now?

- because this slice only needs explicit result ownership
- the current startup order is already stable enough to preserve as-is
- broader startup step extraction would widen risk for little immediate payoff

Why keep nested return-resolution explicit inside startup?

- because startup can still resume route-return aftermath
- flattening that nested result away would recreate another implicit timing gap

This recommendation depends on one assumption:

- the team still prefers serial, narrow lifecycle contracts over one-shot
  startup rewrites

## Decision Summary

1. Startup outcome should be explicit, not reconstructed from nested state.
2. `CampaignLifecycleMachine` should own the startup result contract even while
   `CampaignStartupOrchestrator` still owns the concrete step order.
3. Startup should expose both:
   - whether idle was entered or an interrupt blocked
   - the nested return-resolution result that happened during startup
4. The lifecycle read surface should include startup summary fields so
   shell/UI-side readers do not need to inspect machine internals directly.
