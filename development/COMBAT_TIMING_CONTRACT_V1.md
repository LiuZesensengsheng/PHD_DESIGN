# Combat Timing Contract V1

## Goal

Define one explicit combat timing contract that is:

- close to the mental model used by Slay the Spire-style card combat
- stable enough for `300+` cards, `100+` traits, and many enemy passives
- clear enough that card authors do not need to memorize hidden code order

This document is a timing contract and migration target.

It is not a full engine rewrite plan.

## Why This Exists

The current combat code already has a workable mainline:

- card play goes through a transaction
- `CardPlayed` enters one orchestrated resolution path
- many active effects already use planner/queue execution
- turn start and turn end already have recognizable sequencing

But timing is still partly implicit:

- some hooks are in `Player`
- some are in `CombatModel`
- some are event-bus callbacks
- some are queue follow-ups
- some enemy passives are bespoke

That makes three things harder than they should be:

1. adding new trait / power / enemy-passive reactions
2. predicting whether a special effect composes correctly
3. keeping preview, execution, and simulation aligned

V1 fixes that by defining one shared timing vocabulary.

## Scope

V1 covers:

- combat start
- player turn
- card play
- turn end
- enemy turn
- combat end
- reaction ordering for:
  - player traits
  - player powers
  - enemy passives
  - arena / encounter effects

V1 does not require:

- a potion system
- a full relic rename or feature rename
- a new outer UI phase machine
- immediate removal of all legacy effect implementations

## Outer Phase Model

The outer phase model remains intentionally small:

- `PLAYER_TURN`
- `ENEMY_TURN`
- `COMBAT_END`

The existing `CombatPhaseMachine` can stay roughly this simple.

The main improvement is inside each outer phase:

- explicit internal timing windows
- explicit mutation rules
- explicit reaction order

## Timing Vocabulary

### 1. Combat Start

- `COMBAT_SETUP`
  - build player, enemies, encounter payload
  - seed RNG
  - attach persistent combat-start data
- `COMBAT_START_PRE`
  - instantiate combat-start systems
  - register arena / encounter effects
  - register carried-in player build state
- `COMBAT_START_REACTIONS`
  - fire "at combat start" reactions
- `OPENING_HAND_SETUP`
  - shuffle draw pile
  - move innate cards
  - draw opening hand
- `FIRST_PLAYER_TURN_ENTER`
  - enter first player turn

### 2. Player Turn

- `TURN_START_RESET`
  - increment turn number
  - reset per-turn counters and per-turn context
  - clear one-turn flags from the previous turn
- `TURN_START_PRE_DRAW`
  - run start-of-turn reactions that must happen before draw
  - example use:
    - refresh energy
    - reset pointer / queue limits
    - reset once-per-turn counters
- `TURN_START_DRAW`
  - draw the normal start-of-turn hand fill
- `TURN_START_POST_DRAW`
  - run reactions that depend on the fresh hand
  - inject temporary environment cards only if contract says they belong here
- `ACTION_WINDOW`
  - player may play cards, end turn, or use future combat-side utilities

### 3. Card Play

- `PLAY_ATTEMPT`
  - validate playability
  - lock current source card / target / x-cost context
- `PLAY_COST_FINALIZE`
  - finalize actual cost after all cost modifiers
- `PLAY_COMMIT`
  - spend energy and commit the play
  - from this point the card is considered "played"
- `ON_CARD_PLAYED`
  - fire "when you play a card" reactions
  - this is a reaction window, not the card's own effect body
- `BEFORE_CARD_RESOLUTION`
  - finalize transient modifiers for this card resolution
- `BEFORE_EFFECT`
  - window before each individual effect
- `EFFECT_RESOLUTION`
  - execute one effect through planner/queue or legacy fallback
- `AFTER_EFFECT`
  - resolve follow-up reactions caused by that effect
- repeat `BEFORE_EFFECT -> EFFECT_RESOLUTION -> AFTER_EFFECT` for each effect
- `AFTER_CARD_RESOLVED`
  - run post-card reactions after all effects complete
- `POWER_ATTACH`
  - if the card is a power, attach its persistent passive now
- `CARD_ROUTE`
  - discard / exhaust / move to power area
- `AFTER_CARD_ROUTED`
  - final cleanup after the card leaves hand ownership

### 4. Player Turn End

- `TURN_END_PRE`
  - no new actions may be started
  - finalize any pending reaction queue
- `HAND_CLEANUP`
  - discard or exhaust remaining hand cards by card rules
- `TURN_END_REACTIONS`
  - run end-of-turn reactions
- `BLOCK_DECAY`
  - decay temporary defense values for the player
- `TURN_END_POST`
  - clear temporary cost overrides and end-of-turn transient state
- transition to enemy turn

### 5. Enemy Turn

- `ENEMY_TURN_START`
  - global enemy-turn start reactions
  - chore / countdown ticks
- for each enemy:
  - `ENEMY_START`
  - `ENEMY_ACTION`
  - `ENEMY_END`
- `ENEMY_TURN_END`
  - global enemy-turn end reactions
  - prune defeated enemies
  - perform combat-end check
- transition back to player turn

### 6. Combat End

- `COMBAT_END_CHECK`
  - after any meaningful state mutation that can end combat
- `COMBAT_END_RESOLVE`
  - mark win / loss
  - freeze further combat actions
- `COMBAT_END_CLEANUP`
  - battle-scoped cleanup only

## Reaction Ordering

V1 defines one default ordering rule.

Within one timing window, reactions run in this group order:

1. arena / encounter effects
2. active enemy passives relevant to the window
3. player traits
4. player powers
5. deferred follow-up actions emitted by the window

This order is intentionally simple:

- global before local
- enemy-side before player-side
- relic-like build modifiers before power-like combat modifiers
- queued follow-up work after direct reactions

### Important Rule

Insertion order is not part of the contract.

The contract must be driven by explicit priority inside each group, not by:

- subscription order
- list append order
- whichever object happened to be constructed first

### Per-Group Priority

Within each group, the implementation should support:

- `priority`
  - lower number runs earlier
- `stable_tiebreak`
  - deterministic fallback, such as source id

For V1, every reaction source should eventually expose:

- source id
- source group
- priority
- supported windows

## Mutation Rules By Window

These rules are the most important part of the contract.

### `TURN_START_RESET`

Allowed:

- reset counters
- clear previous-turn temporary flags

Not allowed:

- draw cards
- deal damage
- permanently mutate deck contents

### `TURN_START_PRE_DRAW`

Allowed:

- refill energy
- refresh once-per-turn caps
- start-of-turn buff / passive updates

Not allowed:

- route played cards
- retroactively modify previous turn outcomes

### `TURN_START_DRAW`

Allowed:

- draw the normal hand fill
- trigger on-draw reactions

Not allowed:

- manual combat-end routing

### `ON_CARD_PLAYED`

Meaning:

- the card has been committed and paid for
- the card's own active effects have not finished yet

Allowed:

- increment counters
- mark pending modifiers for this card
- create follow-up actions

Not allowed:

- route the played card
- assume all of the card's effects are already complete

### `BEFORE_EFFECT`

Allowed:

- finalize effect-local modifiers
- lock target snapshot if needed

Not allowed:

- consume unrelated future effect state

### `AFTER_EFFECT`

Allowed:

- resolve reactions caused by the finished effect
- enqueue follow-up actions
- check combat end if the effect can kill

### `AFTER_CARD_RESOLVED`

Meaning:

- all active effects on the card have completed
- the card may still not be routed yet

Allowed:

- one-shot "after this card resolves" reactions
- finalize card-level counters

### `POWER_ATTACH`

Meaning:

- persistent power effects from the just-played power card become active here

Contract rule:

- the newly attached power does not participate in its own:
  - `PLAY_COST_FINALIZE`
  - `ON_CARD_PLAYED`
  - `BEFORE_EFFECT`
  - current card resolution

This removes a large class of self-retroactive ambiguity.

### `CARD_ROUTE`

Allowed:

- move the card to discard / exhaust / power area
- publish routed-card events

Contract rule:

- route decisions must read one shared force-exhaust contract
- traits and powers must not diverge on whether they can force routing

### `TURN_END_REACTIONS`

Allowed:

- end-of-turn traits / powers
- scheduled cleanup reactions

Contract rule:

- `TURN_END_REACTIONS` happens before `BLOCK_DECAY`

This keeps "end of turn" reactions separate from "lose temporary defense now".

## Contract For Traits, Powers, And Enemy Passives

### Traits

Traits are the relic-like persistent player build layer.

Traits may react in any supported timing window, but should prefer:

- combat start
- turn start
- card played
- effect resolution modifiers
- turn end

Traits should not rely on raw insertion order.

### Powers

Powers are battle-local persistent effects.

Powers may react in the same windows as traits, but their reactions occur after
traits in V1.

Powers created by a just-played power card become active at `POWER_ATTACH`.

### Enemy Passives

Enemy passives are first-class reaction sources, not bespoke special cases.

Enemy passives should be able to react through the same timing vocabulary:

- combat start
- enemy turn start / end
- player card played
- player damage taken
- enemy damaged

V1 does not require the same class hierarchy for all of them, but it does
require the same timing windows.

## Contract For Queue / Planner / Legacy Effects

V1 keeps the action queue as the preferred active-effect sequencing substrate.

Rules:

- planned actions are authoritative when a card effect is supported by planner
- legacy direct effect execution is still allowed during migration
- both planned and legacy paths must honor the same timing windows

That means:

- legacy effects may not silently skip `BEFORE_EFFECT` / `AFTER_EFFECT`
- planner support is not allowed to invent different timing semantics

## Preview Contract

Preview and execution should share the same card-level timing assumptions:

- cost preview uses `PLAY_COST_FINALIZE`
- effect preview assumes `BEFORE_EFFECT` modifiers
- preview must not include `AFTER_EFFECT` side effects unless explicitly marked

V1 does not require perfect preview of every special effect.

It does require that "simple" planned effects and "simple" executed effects use
the same modifier order.

## Current Mapping To Existing Runtime

This section maps the current runtime to the target contract.

### Already Close

- outer phases already exist:
  - `PLAYER_TURN`
  - `ENEMY_TURN`
- card play already has a transaction boundary
- card effects already enter one orchestrated mainline
- enemy turns already use a stable step sequence

### Not Yet Formalized

- `on_turn_start` and `on_turn_end` ordering is still spread across model and player
- `on_card_played` semantics are not formally documented
- power attachment timing is implicit
- enemy passives are not on the same reaction substrate
- event-bus priority is not yet the real authority

## V1 Non-Goals

V1 does not attempt to:

- add potions
- redesign the outer combat UI
- remove all legacy effect classes in one pass
- decide every future keyword mechanic
- force a full Slay the Spire clone

## Recommended Migration Order

1. Write tests that lock the timing windows around:
   - turn start
   - card play
   - power attach
   - turn end
2. Introduce one internal timing enum / window vocabulary
3. Route trait / power / enemy-passive reactions through one shared dispatcher
4. Align queue path and legacy path to emit the same timing hooks
5. Fix route-card semantics so traits and powers share the same routing contract

## Open Review Questions

These are the main questions to review before implementation:

1. Should temporary environment cards be injected in `TURN_START_PRE_DRAW` or `TURN_START_POST_DRAW`?
2. Should `BLOCK_DECAY` happen before or after `TURN_END_REACTIONS`?
3. Is `traits -> powers` the right player-side default order for V1?
4. Should enemy passives always react before player traits, or only in enemy-owned windows?
5. Does `POWER_ATTACH` after `AFTER_CARD_RESOLVED` match the desired feel for this game?

## Proposed Default Answer For V1

Unless review says otherwise, V1 should use:

- environment card injection: `TURN_START_POST_DRAW`
- block decay: after `TURN_END_REACTIONS`
- player-side order: `traits -> powers`
- enemy passives: before player-side reactions
- power attach: after card resolution, before route finalization

