# Campaign Return Resolution Contract V1

## Problem

Campaign lifecycle already had an explicit `RETURN_RESOLUTION` phase, but the
runtime still exposed it mainly as a mutable `CampaignLifecycleContext`.

Current pre-slice behavior:

- `CampaignLifecycleMachine.run_return_resolution(...)` returned only the
  lifecycle context
- callers had to inspect:
  - `context.return_resolved_block_ids`
  - `context.return_reward_ids`
  - `context.opened_reward_id`
  - `machine.current_phase`
- there was no single explicit answer to:
  - were there any return transitions at all?
  - did return resolution advance turns?
  - did it open a reward?

That left the return path more implicit than the newly tightened turn-loop
contract.

## Constraints

- Keep the work inside `contexts/campaign/**`.
- Preserve the current return-resolution order:
  - route cleanup
  - turn advance
  - `AFTER_COMBAT_RETURN`
  - reward open
- Do not widen into:
  - startup-phase unification
  - reward-platform redesign
  - save-schema work

## Complexity

### Essential Complexity

Return resolution genuinely has three meaningful outcomes:

1. no return transitions
2. return transitions resolved but no reward opened
3. reward opened

It also may advance one or more campaign turns while staying inside the return
phase.

### Accidental Complexity

The accidental complexity came from making callers reconstruct those outcomes
from context mutation rather than reading one explicit result object.

## Options

### Option A: Keep Context-Only Return Resolution

What it means:

- continue returning only `CampaignLifecycleContext`

Pros:

- cheapest possible path

Cons:

- keeps return outcome implicit
- forces future callers to keep decoding context state manually

### Option B: Add A Narrow Return-Resolution Result Contract

What it means:

- add `CampaignReturnResolutionResult`
- add `CampaignReturnResolutionStatus`
- return one explicit outcome object from
  `run_return_resolution(...)`

Pros:

- mirrors the turn-loop tightening direction
- keeps the slice runtime-only and narrow
- makes startup/return readers simpler and safer

Cons:

- adds one more lifecycle result type
- requires a small amount of seam propagation

## Risks

### Risk If We Stay Implicit

- return-resolution behavior keeps being decoded instead of read
- future combat/event return work may add more hidden dependencies on context
  mutation order

### Risk If We Over-Build

- a broader "return runtime aggregate" would be heavier than what the current
  path needs
- reward/startup concerns could get dragged into the same slice

## Recommendation

Choose **Option B**.

Current V1 contract:

- `CampaignLifecycleMachine.run_return_resolution(...)` now returns
  `CampaignReturnResolutionResult`
- `CampaignReturnResolutionResult.status` is one of:
  - `NO_TRANSITIONS`
  - `RESOLVED_WITHOUT_REWARD`
  - `REWARD_OPENED`
- the result also makes these fields explicit:
  - `resolved_block_ids`
  - `reward_ids`
  - `opened_reward_id`
  - `turn_advanced_count`
  - `turn_transition_contexts`
- `CampaignLifecycleMachine.last_return_resolution_result` keeps the latest
  explicit return-resolution outcome available for inspection

Supporting runtime tightening:

- return-resolution now captures any nested turn-transition contexts produced by
  `advance_campaign_turn()`
- startup/orchestration callers can ignore the returned object for now, but the
  contract is now available instead of hidden

## Counter-Review

Why not leave return resolution alone and move straight to startup?

- because return resolution was still one of the most implicit timing paths
- and it is much cheaper to tighten than a broader startup-phase migration

Why include nested turn-transition contexts?

- because return resolution may advance one or more turns
- keeping those contexts explicit avoids another round of hidden lifecycle
  state

This recommendation depends on one assumption:

- the team still wants lifecycle execution to stay readable through explicit
  runtime contracts rather than through one large generalized state object

## Decision Summary

1. Return-resolution outcome should be explicit, not context-decoded.
2. `run_return_resolution(...)` should return a dedicated result contract.
3. The result should name the three current stable outcomes:
   - no transitions
   - resolved without reward
   - reward opened
4. Nested turn-transition execution during return resolution should also be
   exposed explicitly rather than staying hidden inside side effects.
