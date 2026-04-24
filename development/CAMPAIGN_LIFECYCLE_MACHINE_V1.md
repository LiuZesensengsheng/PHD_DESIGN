# Campaign Lifecycle Machine V1

## Goal

Define a concrete campaign-side lifecycle architecture for future trait,
event, and forced-interrupt growth without reopening a full `CampaignView`
rewrite, a full node-tree migration, or a whole-campaign aggregate rewrite.

- Level: `L3 Architecture`
- Date: `2026-04-18`

This document is a decision-and-rollout RFC, not an implementation patch.

## Problem

The campaign runtime already has real lifecycle stages, but they are still
spread across several orchestrators and update paths instead of being owned by
one explicit lifecycle model.

Current evidence:

- startup/bootstrap ordering lives in
  `contexts/campaign/services/campaign_startup_orchestrator.py`
- UI-facing end-turn request routing lives in
  `contexts/campaign/services/campaign_end_turn_orchestrator.py`
- actual turn advancement and board refresh live in
  `contexts/campaign/services/campaign_turn_orchestrator.py`
- runtime-time prompt checks and end-turn staged updates still run from
  `contexts/campaign/services/campaign_frame_orchestrator.py`
- campaign fact events exist in
  `contexts/campaign/domain/events.py`, but those events are only a local fact
  log today, not the owner of lifecycle sequencing

That creates a growing risk for future campaign features:

1. traits and events will need clear trigger points such as:
   - after combat return
   - after gantt/time advancement
   - after board stabilization
   - after forced DDL refresh
   - before entering free campaign interaction
2. the current runtime does not expose one explicit owner for those trigger
   points
3. AI or human developers must currently infer the real order by reading
   multiple services and `frame` update behavior together

The project now needs an explicit campaign lifecycle contract, not just more
localized cleanup.

## Constraints

- Keep the current architectural direction:
  - `CampaignState` remains the outer shell host
  - `Task Area` remains a subdomain inside campaign
  - UI/runtime nodes remain presentation-side only
- Do not treat this as a full node-tree migration campaign.
- Do not reopen `contexts/campaign/view.py` as the main work area.
- Do not widen the work into task-area geometry redesign, thesis write-path
  redesign, or save-format cleanup.
- Do not reuse the overloaded generic term `Node` for this new lifecycle layer.

Important naming constraint:

The repository already contains several unrelated `node` concepts:

- old campaign-map nodes in `contexts/campaign/domain/node.py`
- runtime UI nodes in `contexts/campaign/ui_runtime/ui_node.py`
- narrative/quest nodes in `contexts/shared/quest_runtime.py`

So the lifecycle architecture must use a different vocabulary such as:

- `CampaignLifecyclePhase`
- `CampaignLifecycleStep`
- `CampaignTimingWindow`

## Complexity

### Essential Complexity

The campaign runtime genuinely has at least three different kinds of
sequencing complexity:

1. outer lifecycle phase complexity
   - startup
   - return-resolution
   - turn transition
   - forced interrupt handling
   - free interaction / idle
2. intra-phase ordered work
   - advancing `current_turn`
   - stabilizing blocks and tracks
   - recomputing forced DDL state
   - opening reward / meeting / forced prompts in the correct order
3. extension-point complexity
   - future traits
   - future event reactions
   - future campaign passives
   - future deadline/pressure modifiers

### Accidental Complexity

The current accidental complexity mainly comes from owner ambiguity:

- startup checks and turn-interrupt checks are not expressed through the same
  lifecycle vocabulary
- runtime `frame` updates still perform some business-timing checks
- there is no single explicit answer to "when may a campaign trait react?"
- `domain_events` sound lifecycle-like, but they do not currently own
  lifecycle transitions

### What The Project Actually Needs

The project does **not** need:

- a generic graph execution engine
- a new scene graph for campaign business rules
- a full "everything is a node" runtime rewrite

The project **does** need:

- explicit outer lifecycle phases
- explicit ordered steps inside those phases
- explicit timing windows where future reactive content may attach

## Options

### Option A: Keep The Current Orchestrators And Only Add More Docs

What it means:

- keep `startup`, `turn advance`, `interrupt checks`, and runtime prompt checks
  in their current owners
- document the intended order in prose only

Pros:

- lowest short-term cost
- almost no migration risk now

Cons:

- does not give AI a real execution owner
- traits/events will still be added by editing whichever orchestrator "looks
  closest"
- `frame` update remains a soft business-timing owner

### Option B: Add Timing Windows Only, Without A Lifecycle Machine

What it means:

- define windows such as `AFTER_BOARD_STABILIZED`
- let existing orchestrators dispatch those windows opportunistically

Pros:

- cheaper than a lifecycle refactor
- creates some explicit trigger vocabulary

Cons:

- still leaves outer lifecycle ownership split
- does not answer "what phase are we in now?"
- can devolve into many ad-hoc window dispatch call-sites

### Option C: Add A Thin Lifecycle Machine + Ordered Step Pipeline + Timing Windows

What it means:

- outer lifecycle becomes an explicit state machine
- each phase owns an ordered set of internal steps
- step boundaries dispatch stable timing windows
- existing orchestrators are migrated into that structure incrementally

Pros:

- explicit owner for lifecycle sequencing
- explicit insertion points for future traits/events
- AI can add behavior at the right lifecycle seam without guessing
- low enough scope to land serially

Cons:

- requires a new lifecycle layer
- several current orchestrators will need to become delegators or adapters
- naming and migration discipline matter a lot

### Option D: Full Generic Campaign Node Tree

What it means:

- reframe campaign progression as a generic node graph or universal node tree
- move most sequencing into nodes directly

Pros:

- strongest "everything is explicit" story if it succeeds

Cons:

- highest migration risk
- collides with existing `node` terminology already used elsewhere
- likely to blur business lifecycle nodes with runtime/UI nodes
- harder for AI if the graph becomes dynamic or overly abstract

## Risks

### If We Stay With Split Ownership

- future trigger timing will keep drifting across:
  - startup
  - turn advance
  - return resolution
  - runtime frame checks
- new content will accumulate accidental order dependencies
- AI will keep needing broad context scans for simple trigger additions

### If We Over-Build A Generic Node System

- lifecycle logic may become harder to trace than it is now
- naming collisions with existing `node` concepts will confuse both humans and
  AI
- runtime/UI node logic may get mixed with business sequencing

### Specific Technical Risks To Manage

- staged end-turn animation in `EndTurnService` must stay a presentation/timing
  helper, not the source of business truth
- `CampaignFrameOrchestrator.update()` currently performs meeting-prompt timing
  work; migrating that behavior must preserve UX ordering
- reward gates and meeting gates must be explicitly ordered, not left to race
  on first render/update after a transition

## Recommendation

Choose **Option C**.

The recommended architecture is:

### 1. Outer Lifecycle = State Machine

Create a new lifecycle layer under:

- `contexts/campaign/lifecycle/`

Recommended first files:

- `phases.py`
- `windows.py`
- `context.py`
- `hooks.py`
- `machine.py`
- `steps/turn_transition_steps.py`
- `steps/interrupt_gate_steps.py`
- `steps/return_resolution_steps.py`

The outer lifecycle phases should be small and mutually exclusive:

- `STARTUP`
- `RETURN_RESOLUTION`
- `TURN_TRANSITION`
- `TURN_INTERRUPTS`
- `TURN_IDLE`

Meaning:

- `STARTUP`: bootstrapping campaign runtime from persisted/session state
- `RETURN_RESOLUTION`: handling route return, reward/re-entry aftermath, and
  combat/event return payloads
- `TURN_TRANSITION`: the system is actively moving to the next campaign turn
- `TURN_INTERRUPTS`: the system is checking and executing mandatory interrupt
  flows before the player regains free control
- `TURN_IDLE`: the campaign has entered normal free interaction mode

### 2. Phase Internals = Ordered Step Pipeline

Do **not** model phase internals as a generic graph first.

For V1, each phase should own an explicit ordered step list.

For `TURN_TRANSITION`, the initial step sequence should be:

1. `advance_turn_commit`
   - increment `current_turn`
   - establish the new logical campaign day/turn
2. `board_stabilize`
   - resolve fusion/stabilization
   - compact tracks
   - restore the task area to a stable post-advance board shape
3. `forced_ddl_refresh`
   - recompute forced DDL blocks
   - recompute any temporary pressure/debuff side effects
4. `post_turn_reactions`
   - gossip badge increment
   - line-bubble turn hooks
   - top-bar label refresh

For `TURN_INTERRUPTS`, the initial ordered gates should be:

1. `reward_gate`
2. `meeting_gate`
3. `forced_event_gate`

These gates should answer:

- is there a mandatory reward flow to open first?
- is there a mandatory meeting prompt to show next?
- is there another forced event that must preempt free interaction?

`forced_event_gate` may be a minimal placeholder in V1 if the project does not
yet have a stable third forced-interrupt family.

### 3. Extension Points = Timing Windows

Timing windows are where future reactive content should attach.

Recommended initial windows:

- `AFTER_COMBAT_RETURN`
- `BEFORE_TURN_ADVANCE`
- `AFTER_TURN_ADVANCE`
- `AFTER_BOARD_STABILIZED`
- `AFTER_FORCED_DDL_REFRESH`
- `BEFORE_INTERRUPT_GATES`
- `TURN_IDLE_ENTER`

These windows should be dispatched by the lifecycle layer, not by arbitrary UI
or adapter services.

### 4. Naming Rule

Do not use the generic word `Node` for this architecture.

Use:

- `CampaignLifecyclePhase`
- `CampaignLifecycleStep`
- `CampaignTimingWindow`
- `CampaignLifecycleMachine`
- `CampaignLifecycleHookRegistry`

This avoids collision with:

- old campaign-map nodes
- runtime UI nodes
- narrative/quest nodes

### 5. Current Service Mapping

Map the current owners into the new lifecycle incrementally:

- `campaign_startup_orchestrator.py`
  - becomes the source material for `STARTUP`
- `campaign_turn_orchestrator.py`
  - becomes the source material for `TURN_TRANSITION`
- `campaign_end_turn_orchestrator.py`
  - remains the UI-facing request seam, but should delegate actual transition
    ownership into the lifecycle machine
- `campaign_frame_orchestrator.py`
  - should keep runtime view/update concerns
  - should stop owning campaign business-timing checks such as mandatory
    meeting-prompt gating once those gates move into `TURN_INTERRUPTS`

### 6. Recommended Migration Order

#### Phase A: Contract First

Add:

- lifecycle enums
- lifecycle context
- hook registry
- lifecycle machine shell

No major behavior migration yet.

#### Phase B: Move `TURN_TRANSITION`

Split current `CampaignTurnOrchestrator.advance_turn()` into explicit lifecycle
steps.

This is the best first cut because it already has one clear business sequence.

#### Phase C: Rewire End-Turn Completion

Keep `CampaignEndTurnOrchestrator` and `EndTurnService` as request/presentation
helpers, but route final turn advancement through the lifecycle machine.

#### Phase D: Move `TURN_INTERRUPTS`

Lift reward/meeting/forced-interrupt checks out of runtime `frame` timing and
into lifecycle gates.

#### Phase E: Move `RETURN_RESOLUTION`

Unify combat/event return aftermath through a dedicated lifecycle phase and
dispatch `AFTER_COMBAT_RETURN`.

#### Phase F: Enable Real Hook Registration

Only after the lifecycle and windows stabilize, allow future traits/events to
bind to those windows.

### 7. Recommended Test Pack

Add focused tests such as:

- `tests/campaign/test_campaign_lifecycle_machine.py`
- `tests/campaign/test_campaign_turn_transition_steps.py`
- `tests/campaign/test_campaign_interrupt_gates.py`
- `tests/campaign/test_campaign_return_resolution_flow.py`
- `tests/campaign/test_campaign_timing_windows.py`

Keep existing tests as compatibility guards during migration:

- `tests/campaign/test_campaign_turn_orchestrator.py`
- `tests/campaign/test_campaign_end_turn_orchestrator.py`
- `tests/campaign/test_campaign_startup_orchestrator.py`
- `tests/campaign/test_campaign_frame_orchestrator.py`

## Counter-Review

Why not just stay with timing windows only?

- because timing windows alone do not unify outer lifecycle ownership
- they still require developers to know which existing orchestrator should fire
  the window
- they reduce trigger ambiguity, but they do not eliminate sequencing
  ambiguity

Why not adopt a full generic node tree now?

- the project already has too many unrelated `node` meanings
- a dynamic or generic graph would likely make AI work harder, not easier
- the real need is controlled lifecycle sequencing, not a new universal
  abstraction

Why is the recommended path worth doing now?

- campaign is entering a phase where more traits/events/forced interrupts are
  expected
- the current split ownership is still manageable enough to migrate serially
- the payoff for AI-assisted iteration is high because this creates explicit
  insertion points and explicit phase ownership

This recommendation depends on one assumption:

- the team is willing to keep the new lifecycle layer narrow and execution
  focused, instead of turning it into a general "campaign scripting tree"

## Decision Summary

1. The campaign runtime should be modeled primarily as a **lifecycle state
   machine**, not as a generic node tree.
2. Each lifecycle phase should own an explicit **ordered step pipeline**.
3. Future traits/events should attach through **timing windows**, not by adding
   new business timing into arbitrary orchestrators or frame updates.
4. The first migration target should be `TURN_TRANSITION`, followed by
   `TURN_INTERRUPTS`, then `RETURN_RESOLUTION`.
5. The new lifecycle layer should live under `contexts/campaign/lifecycle/`.
6. The lifecycle architecture should avoid the generic term `Node` entirely to
   prevent collision with existing campaign-map, UI-runtime, and narrative node
   models.
7. This is a worthwhile near-term architecture move because it improves future
   feature safety and AI iteration speed without requiring a broad UI or domain
   rewrite.
