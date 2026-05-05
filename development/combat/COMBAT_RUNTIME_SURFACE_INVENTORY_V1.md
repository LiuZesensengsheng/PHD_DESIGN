# Combat Runtime Surface Inventory V1

## Purpose

Record the current combat runtime host surface after `G1` of
`global compat-zero` removed the legacy MVC facade modules.

This document is intentionally about **engineering surface**, not content
semantics. It answers:

- what the active combat runtime host is now
- which `CombatSession` members still form the public engineering surface
- which remaining seams are still planned compat cleanup
- what should stay out of this workstream

## Current Host Shape

- `CombatSession` is the canonical combat runtime host for UI, headless, and
  save/load.
- session-local mutable host data is attached through
  `CombatSessionRuntimeState`.
- render-facing session reads have explicit public accessors:
  - `current_phase`
  - `phase_banner`
  - `enemy_action_banner`
- the old underscore-shaped session compatibility wrappers are now removed:
  - `_phase`
  - `_phase_banner`
  - `_enemy_action_banner`
  - `_enemy_action_steps`
  - `_current_enemy_action`
  - `_enemy_action_timer`
- there is no active `CombatModel` module or `mvc.factory` module anymore:
  - `contexts/combat/mvc/model.py`: deleted
  - `contexts/combat/mvc/factory.py`: deleted
- headed combat composition is session-first end to end:
  - `build_combat_scene_runtime(...)` returns the session-first runtime bundle
  - `CombatController` renders from `CombatSession` through
    `CombatRenderStateAssembler`
  - `CombatState` stores `session` as its only runtime host surface
  - `run_combat.py` enters through the session-first builder
- headless/test helper composition is also session-first:
  - `HeadlessCombatSimulationExecutor` builds `CombatSession` directly
  - `tests/helpers/combat_runtime.py` no longer exposes `model`
  - `tests/helpers/headless_test_base.py` no longer keeps `self.model`
- tooling has been updated to the same baseline:
  - `scripts/debug_imports.py` now imports `CombatSession`

## Quantitative Baseline

As of `2026-04-23`:

- deleted MVC facade modules: `2`
- live runtime/test/script imports or constructions of the removed modules: `0`
- deleted `CombatSession` underscore compat wrappers: `6`
- live `session._...` wrapper reads outside guard coverage: `0`
- remaining textual mentions of removed MVC paths under `tests/combat`: `2`
  files
  - `tests/combat/test_combat_runtime_host_migration_v1.py`
  - `tests/combat/test_combat_runtime_surface_inventory_v1.py`
- those remaining mentions are explicit removal guards, not live usage
- `check_combat_compat_zero.py` is green on this baseline

## Public `CombatSession` Surface

### Stable host/state surface

- `state`
- `event_bus`
- `phase_machine`

### Runtime collaborator surface kept explicit for now

- `effect_executor`
- `card_play_orchestrator`
- `player_turn_orchestrator`

### Presentation/runtime reads

- `busy_reason`
- `presentation_consumer`
- `presentation_log`
- `pending_presentation`
- `current_phase`
- `phase_banner`
- `enemy_action_banner`

### Runtime command and presentation methods

- `start_combat()`
- `end_turn()`
- `play_card(...)`
- `update(...)`
- `enemy_turn()`
- `is_player_turn()`
- `can_accept_commands()`
- `drain_pending_presentation()`
- `set_presentation_consumer(...)`
- `acquire_command_lock(...)`
- `release_command_lock(...)`
- `clear_command_locks()`
- `acknowledge_presentation_event(...)`
- `acknowledge_presentation_lease(...)`
- `create_save_snapshot(...)`
- `to_snapshot_dict(...)`
- `apply_save_snapshot(...)`
- `from_snapshot_dict(...)`

## Mainline Ownership Snapshot

The runtime host is now thin enough that the main ownership points are explicit:

- startup sequencing:
  - `CombatStartOrchestrator`
- enemy-turn timed progression:
  - `EnemyTurnRuntimeDriver`
- presentation shaping and gate-facing event payloads:
  - `CombatPresentationRuntime`
  - `CombatPresentationBridge`
- stress-threshold judgment resolution:
  - `StressThresholdHandler`
- enemy cleanup / pointer / tween follow-up:
  - `EnemyCleanupCoordinator`
  - `EnemyChoreFollowUpPolicy`
  - `EnemyPointerRetargetPolicy`
  - `EnemyTweenMetadataPlanner`
- default collaborator assembly:
  - `build_default_combat_session_services(...)`
  - `CombatSessionServices`

## Remaining Compat Backlog After `G2`

### Active next phases

- `G3`: collapse the `state.xxx -> state.turn_context.xxx` bridge
- `G4`: delete low-value test/import shims
- `G5`: document intentionally retained adapters and stop

### Explicitly retained for now

- save backward-compat migration paths
- adapter-like survivors such as:
  - `ModelEnvironmentArenaEffect`
  - `CardInstance.card_id`
  - `CardInstance.cost_for_player(...)`

### Separate backlog that must stay separate

- red runtime/content failures in `tests/combat/test_json_red_cards.py`
- animation/video blocking semantics
- `combat_view` behavior or visual work
- save schema redesign

## What This Means

- `CombatSession` is no longer sharing host status with a parallel MVC facade.
- the combat engineering surface is smaller and more legible:
  - there is one active runtime host
  - the remaining compat work is now concentrated in named cleanup slices
- the next cleanup no longer needs to debate whether `CombatModel` should stay:
  that question is already resolved by deletion
- the remaining risk is now in field-bridge collapse and later shim cleanup,
  not in host-wrapper ambiguity

## Guardrail

- do not reintroduce `CombatModel` or `mvc.factory`
- new runtime/content tests should use `CombatSession` directly unless the test
  is explicitly asserting removal of the old facade
- if the explicit `CombatSession` surface grows, update:
  - `tests/combat/test_combat_runtime_surface_inventory_v1.py`
  - this inventory document
