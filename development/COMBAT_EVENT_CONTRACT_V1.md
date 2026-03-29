# Combat Event Contract V1

## Goal

Move combat fact reactions out of Player-owned raw loops and into a combat-side dispatcher so events have the same explicit owner and stable ordering model as timing windows.

This contract covers combat fact events only. It does not cover:

- outer `CombatPhaseMachine`
- potions, map flow, or reward flow
- out-of-combat UI sequencing

## Event Scope

V1 treats these as combat fact events:

- `CardDrawn`
- `CardExhausted`
- `Shuffled`
- `PlayerTookDamage`
- `EnemyTookDamage`
- `ConfidenceChanged`
- `ConfidenceWasUsed`
- `EnergyWasSpent`
- `StatusApplied`
- `StatusStacked`
- `StatusEffectExpired`
- `StressThresholdReached`
- `StressIncreased`
- `OffColorCardPlayed`
- `JudgmentResolved`

## Runtime Ownership

- The runtime owner is `CombatEventDispatcher`.
- `Player` still subscribes to the event bus, but only to:
  - apply required local state updates
  - forward combat facts into `CombatEventDispatcher`
- There is no remaining legacy event-loop fallback in runtime mainline.

This means:

- event ordering is no longer decided by `Player` raw loops
- `Player._run_legacy_combat_event_reactions(...)` has been deleted

## Default Ordering

Combat fact events use the same owner-first rules as timing windows.

### Player-Owned Events

1. arena / encounter effects
2. player traits
3. player powers
4. enemy passives

### Enemy-Owned Events

1. arena / encounter effects
2. enemy passives
3. player traits
4. player powers

### Default Owner Heuristics

- `EnemyTookDamage` belongs to enemy side
- most player resource, draw, and damage events belong to player side
- `Status*` ownership is determined by `owner_id`
- unknown ownership defaults to player side

## Runtime Content Interface

V1 mainline uses event-native interfaces:

- `supported_event_types`
- `supports_combat_event(...)`
- `react_to_combat_event(...)`

Legacy `on_*` event hooks are not part of the supported combat runtime interface anymore.

## Test Anchors

V1 must keep these true:

- player-owned events resolve in `traits -> powers`
- enemy-owned events resolve in `enemy passives -> player traits -> player powers`
- runtime-published events such as `Shuffled`, `CardExhausted`, and `StatusApplied` enter the dispatcher mainline
- runtime mainline does not depend on `Player._run_legacy_combat_event_reactions(...)`

## Relation To Timing Contract

- timing windows answer "which phase window are we in"
- combat events answer "which fact just happened"
- both use the same owner-first mental model
- neither relies on shared event bus priority as the combat source of truth
