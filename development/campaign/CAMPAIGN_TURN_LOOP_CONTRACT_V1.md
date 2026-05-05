# Campaign Turn Loop Contract V1

## Problem

Campaign lifecycle already has explicit phases, steps, and timing windows, but
the top-level **turn loop result** was still implicit.

Current pre-slice behavior:

- `CampaignLifecycleMachine.run_turn_transition()` returned a
  `CampaignLifecycleContext`
- `CampaignLifecycleMachine.run_turn_interrupts()` returned a second
  `CampaignLifecycleContext`
- `CampaignLifecycleMachine.run_turn_cycle()` only returned the interrupt
  context
- whether the turn had fully advanced, whether idle had been entered, and which
  gate blocked the loop still had to be reconstructed from:
  - `machine.current_phase`
  - `context.interrupt_blocked`
  - `context.interrupt_blocking_step`
  - the fact that turn transition had already run elsewhere

That shape was still AI-unfriendly:

- callers could not read one explicit answer to "what did this turn-cycle do?"
- the transition half of the loop was hidden behind side effects
- future turn-loop logic would need to keep inferring state from multiple
  objects

## Constraints

- Keep the work inside `contexts/campaign/**`.
- Do not change gameplay ordering for:
  - turn advance
  - board stabilization
  - forced DDL refresh
  - interrupt gate order
- Keep rollback ownership in `CampaignTurnOrchestrator`.
- Do not widen this into:
  - save-schema work
  - interrupt-family unification
  - generic node-tree execution

## Complexity

### Essential Complexity

One campaign turn-cycle genuinely has two business stages:

1. turn transition
2. interrupt gating

And it also has two stable outcomes:

1. idle entered
2. interrupt blocked

That is real complexity and should be made explicit.

### Accidental Complexity

The accidental complexity came from splitting the readable outcome across:

- multiple return values
- machine mutable state
- implicit knowledge that turn transition had already happened

## Options

### Option A: Keep `run_turn_cycle()` Implicit

What it means:

- keep returning only the interrupt context
- let callers inspect `current_phase` and interrupt flags manually

Pros:

- zero migration cost

Cons:

- keeps the most important turn-loop answer implicit
- forces future AI edits to keep reconstructing the same result

### Option B: Return A Tuple Of Contexts

What it means:

- return `(transition_context, interrupt_context)`

Pros:

- cheap
- exposes both halves of the loop

Cons:

- still leaves the outcome vocabulary implicit
- still requires every caller to re-derive "blocked vs idle entered"

### Option C: Add An Explicit Turn-Cycle Result Contract

What it means:

- add `CampaignTurnCycleResult`
- add `CampaignTurnCycleStatus`
- let `run_turn_cycle()` return one explicit result object
- keep the latest result readable on the lifecycle machine

Pros:

- one explicit read model for the turn loop
- no gameplay-order change
- easy to extend later if turn-loop policy grows

Cons:

- adds one more lifecycle contract type
- requires small seam propagation through orchestrator/state helpers

## Risks

### Risk If We Stay Implicit

- turn-loop state keeps being inferred instead of read
- future reward/meeting/forced-event work keeps growing hidden dependencies on
  machine internals

### Risk If We Over-Build

- a larger "turn loop runtime" object could duplicate existing lifecycle
  context/state
- persistence concerns could get mixed into what should stay a runtime-only
  contract

## Recommendation

Choose **Option C**.

Current V1 contract:

- `CampaignLifecycleMachine.run_turn_cycle()` returns
  `CampaignTurnCycleResult`
- `CampaignTurnCycleResult.transition_context` exposes the transition half
- `CampaignTurnCycleResult.interrupt_context` exposes the interrupt half
- `CampaignTurnCycleResult.status` is one of:
  - `TURN_IDLE_ENTERED`
  - `INTERRUPT_BLOCKED`
- `CampaignTurnCycleResult.blocking_step` exposes the gate owner when blocked
- `CampaignLifecycleMachine.last_turn_cycle_result` keeps the latest explicit
  loop result available for inspection

Supporting seam tightening:

- `CampaignTurnOrchestrator.advance_turn()` now returns the transition context
- `CampaignState.advance_campaign_turn()` now forwards that explicit context
  instead of discarding it
- `CampaignEndTurnOrchestrator.request_end_turn_result()` now preserves the
  explicit turn-cycle result for callers that need the lifecycle outcome
- `CampaignState.request_end_turn_result()` mirrors that explicit end-turn
  result seam at the campaign shell host
- keyboard/mouse/ui-button ingress should keep calling
  `CampaignState.request_end_turn*()` host seams rather than reaching directly
  into lifecycle-machine timing APIs

Current status on `2026-04-24`:

- a hard-fail campaign guardrail now keeps:
  - `campaign_frame_orchestrator.py`
  - keyboard/mouse/ui-button ingress services
  free of direct turn-timing calls such as:
  - `run_turn_cycle()`
  - `run_turn_transition()`
  - `run_turn_interrupts()`
  - `advance_campaign_turn()`

## Counter-Review

Why not stop at returning both contexts?

- because the real problem was not only missing data
- it was missing vocabulary for the actual loop outcome

Why is this worth doing before more content work?

- because reward/meeting/forced-event growth will keep leaning on turn-loop
  outcomes
- making that result explicit now is cheaper than retrofitting it after more
  branches depend on implicit behavior

This recommendation depends on one assumption:

- the team wants turn-loop state to stay as a narrow runtime contract, not as a
  new persistent gameplay model

## Decision Summary

1. Campaign turn-loop outcome should be explicit, not reconstructed.
2. `run_turn_cycle()` should return a dedicated result object rather than only
   an interrupt context.
3. The result should name the two current stable outcomes:
   - idle entered
   - interrupt blocked
4. Transition context should still flow through the atomic turn-orchestrator
   seam so rollback ownership stays unchanged.
