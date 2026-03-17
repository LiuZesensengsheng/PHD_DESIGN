# Campaign Startup Seam Cleanup V1

## Goal

Move campaign startup order behind one explicit orchestration seam so UI work
does not need to understand startup hydration, route-return consumption, reward
opening, and startup-only side effects as scattered `CampaignState.startup()`
details.

## Why This Exists

Before this cut, campaign already had good startup sub-services, but the actual
startup order still lived inline inside `CampaignState.startup()`:

- view/bootstrap setup
- session hydration
- route-return transition consumption
- startup-only effects
- reward modal auto-open
- startup status/inspiration refresh
- forced-DDL refresh
- startup meeting prompt

That made the startup path correct but too implicit for safe UI handoff work.

## Stable Seam

`CampaignStartupOrchestrator` now owns the startup mainline order.

`CampaignState.startup(...)` now behaves as:

1. `super().startup(...)`
2. build `CampaignSessionStore`
3. delegate the rest of startup ordering to the orchestrator

This makes `startup()` the lifecycle entrypoint while moving the process order
behind one explicit orchestration seam.

## Current Startup Order

V1 startup order is now:

1. configure runtime-seeded services
2. assert transition protocol guardrails
3. start campaign BGM
4. restore consumed meeting-turn memory
5. mark startup mode active
6. bootstrap startup presentation shell
7. hydrate campaign/session runtime data
8. consume route-return startup transitions
9. apply startup-only effects
10. open startup reward modal if requested
11. refresh startup status UI
12. initialize inspiration UI state
13. refresh forced-DDL state
14. show startup meeting prompt if due
15. clear startup mode flag

## Ownership Split

### Startup Orchestrator Owns

- startup step ordering
- coordination between hydration, route resolution, and startup effects
- the boundary between startup-only effects and UI-visible startup consequences

### Startup Hydration Service Owns

- restoring campaign snapshot/runtime blocks
- loading thesis meta and paper-tag snapshots
- backfilling combat encounter ids
- applying thesis-combat sync payload
- default deck initialization

### Startup Effects Service Owns

- initial board seed when campaign is empty
- pending meeting add-line effect
- reward-id-to-open result for startup follow-up UI

### CampaignState Owns

- lifecycle host entrypoint
- concrete runtime/view/bootstrap methods
- startup presentation shell creation
- startup UI refresh helpers

## UI Collaboration Rule

UI work should treat startup as orchestration-owned.

UI code should not:

- replicate startup ordering locally
- assume reward/meeting prompt opening is driven directly by widgets
- depend on startup-only side effects being scattered across `CampaignState`

UI code may rely on:

- `CampaignState.startup(...)` as the lifecycle entrypoint
- startup-visible consequences happening in the documented order above

## Safety Rule

`CampaignStartupOrchestrator` now guarantees that the startup flag is cleared in
`finally` even if a mid-startup step fails unexpectedly.

That gives later cleanup/refactor work a firmer contract than the old inline
method body.

## Non-Goals

This cut does not:

- redesign startup hydration data shapes
- replace route-return transition queueing
- remove startup side effects such as reward auto-open
- make startup fully pure or side-effect free

## Verification

V1 is currently protected by focused tests covering:

- orchestrator step order
- startup-flag reset on failure
- hydration and startup-effects host seams
- startup reward-open protocol
- startup route-return block resolution
- startup meeting prompt lifecycle
- startup thesis combat tag sync

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign Event Input Split V1`
