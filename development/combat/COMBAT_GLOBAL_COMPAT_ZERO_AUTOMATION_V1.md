# Combat Global Compat-Zero Automation V1

## Purpose

This document defines the next combat cleanup line after the original
runtime-mainline compat-zero work completed.

The previous compat-zero plan already removed the dangerous **mainline fallback
and shim paths** from active combat orchestration. What remains now is a wider
"global compat" tail spread across:

- MVC facade surface
- session-private compatibility wrappers
- state field bridges
- test/import-path helper bridges
- save/schema backward-compat bridges
- a few internal runtime adapters

This document exists so future automation can:

- distinguish **safe delete work** from **decision-gated retention**
- avoid mixing compat cleanup with unrelated runtime/content bugs
- stop at the right boundary instead of silently crossing into save/schema or
  visual behavior work

## Scope Definition

### Already complete

- combat runtime-mainline fallback/shim cleanup
- session-first runtime host migration
- headed/headless/save-load shared runtime entry through `CombatSession`

### Covered by this document

- remaining combat compatibility surfaces outside the completed mainline pass
- the order in which those surfaces should be removed or explicitly retained
- the decision gates that must be locked before long-running automation starts

### Explicit non-goals

- no `combat_view` behavior rewrite
- no combat content semantics rebalance
- no red-card runtime bug fixing mixed into this line
- no animation/video gating implementation in this line
- no save schema redesign in this line

## Current Baseline

As of `2026-04-23`, after `G4` completion and the `G5` retained-adapter review:

- runtime-mainline fallback seams: effectively `0`
- `contexts/combat/mvc/model.py`: deleted
- `contexts/combat/mvc/factory.py`: deleted
- live runtime/test/script imports or constructions of the removed MVC facade:
  `0`
- remaining textual removal guards under `tests/combat`: `2` files
  - `tests/combat/test_combat_runtime_host_migration_v1.py`
  - `tests/combat/test_combat_runtime_surface_inventory_v1.py`
- combat mainline is already session-first for UI, headless, and save/load
- `G3` batch 1 is landed:
  - `action_executor.py`, `pointer_queue_white.py`, `misc.py`, and
    `pile_service.py` now route the touched runtime reads/writes through
    `state.turn_context`
  - the touched tests now seed/assert the migrated counters and tween metadata
    through `turn_context`
  - `scripts/check_combat_compat_zero.py` now guards this batch against
    reintroducing `state.xxx` runtime writes in the migrated files
- `G3` batch 2 is landed:
  - `enemy_tween_planner.py` now commits tween metadata through
    `state.turn_context`
  - the `enemy_tween_*` bridge properties were deleted from `CombatState`
  - enemy cleanup / tween planner tests now seed/assert tween metadata through
    `turn_context`
  - `scripts/check_combat_compat_zero.py` now guards the removed
    `enemy_tween_*` bridge surface against re-entry
- `G3` batch 3 is landed:
  - `player.py`, `powers.py`, `effects/base.py`, `effects/impl/red.py`,
    `effects/impl/pile.py`, and `traits_demo_impl.py` now create/use
    `state.turn_context` directly for the touched runtime counters/flags
    instead of falling back to legacy `state.xxx` scalar writes
  - the following non-tween bridge properties were deleted from `CombatState`:
    - `draw_locked`
    - `reposition_count_this_turn`
    - `reposition_limit_per_turn`
    - `frontier_batch_counter`
    - `red_extra_draw_context`
    - `red_frontier_damage_bonus_current_play`
    - `red_offcolor_damage_bonus_current_play`
    - `force_frontier_next_cards`
    - `traits_double_current_effects`
    - `scribble_played_this_turn`
  - the core-state contract test now asserts explicit `turn_context` ownership
    instead of the removed bridge write path
  - `scripts/check_combat_compat_zero.py` now guards this removed bridge subset
    against direct `state.xxx` re-entry
- `G3` batch 4 is landed:
  - `render_state_assembler.py` now reads `lock_queue_active` from
    `state.turn_context` instead of the legacy bridge field
  - the `lock_queue_active` bridge property was deleted from `CombatState`
  - render-state contract coverage now includes an explicit `lock_queue`
    projection assertion
  - `scripts/check_combat_compat_zero.py` now guards the removed
    `lock_queue_active` bridge against direct `state.xxx` re-entry
- `G3` batch 5 is landed:
  - `action_executor.py` now reserves frontier batch ids through
    `state.turn_context`
  - `render_state_assembler.py` now reads `frontier_used_batches` from
    `state.turn_context`
  - the final `CombatState -> turn_context` bridge properties were deleted:
    - `frontier_used_batches`
    - `non_red_played_this_turn`
  - the touched render/red tests now seed/assert through `turn_context`
  - `scripts/check_combat_compat_zero.py` now guards the removed final bridge
    subset against direct `state.xxx` re-entry
- `G4` batch 1 is landed:
  - `tests/combat/test_damage_service.py` now imports `DamageEffect` directly
    from `contexts.combat.domain.effects.impl.core`
  - the import-path compatibility re-export
    `contexts/combat/domain/effects/implementations.py` was deleted
  - `scripts/check_combat_compat_zero.py` now guards the removed shim file and
    import path against re-entry
- `G4` batch 2 is landed:
  - `tests/combat/test_action_queue.py` now maps chore-resolution actions
    directly through `ChoreResolutionPlanner`
  - the test-only compatibility shim
    `ChoreResolutionOrchestrator._map_actions(...)` was deleted
  - `scripts/check_combat_compat_zero.py` now guards the removed shim method
    and call shape against re-entry
- `G4` batch 3 is landed:
  - the no-op enemy legacy methods were deleted from
    `contexts/combat/domain/enemies/entity.py`:
    - `select_skill_for_turn()`
    - `use_selected_skill()`
  - `scripts/check_combat_compat_zero.py` now guards the removed enemy legacy
    method definitions and call sites against re-entry
- `G5` retained-adapter review is accepted:
  - save backward-compat was an intentional retained boundary at the time of
    this review, but `Save Reset Policy V1` later superseded that stance for
    current pre-content saves.
  - current retained combat save/read surfaces are:
    - `save_snapshot_mapper.py`
    - session save/apply host entrypoints
    - player-side scalar energy projection snapshot/restore for rollback
  - `ModelEnvironmentArenaEffect` and
    `DefaultTurnStartEnvironmentInjector` are retained as intentional runtime
    adapters
  - `CardInstance.card_id` and `CardInstance.cost_for_player(...)` are
    retained as stable convenience contracts
  - `EffectContext` is not treated as a retained adapter; it is a dead
    scaffold candidate for a later tiny cleanup slice
  - player scalar-energy / colored-pool convergence is explicitly split out as
    a separate future decision line, not part of compat-zero closure
- the combat global compat-zero line is now closed at `Engineering Zero`
  after `G5`; future work should split into dedicated follow-up lines instead
  of continuing the same delete wave

## Remaining Compat Surface Inventory

### C1. MVC facade / legacy entrypoint layer

Status:

- completed on `2026-04-23`

Primary verification files:

- `tests/combat/test_combat_runtime_host_migration_v1.py`
- `tests/combat/test_combat_render_state_contracts.py`
- `tests/combat/test_combat_presentation_contract_v1.py`
- `tests/combat/test_combat_runtime_surface_inventory_v1.py`
- `tests/combat/test_combat_mainline_allowlist_v1.py`
- `scripts/debug_imports.py`

Current role:

- the facade modules themselves are gone
- surviving references are guard-only assertions and removal checks
- `CombatSession` is now the only active runtime host at this layer

Default classification:

- closed

### C2. Session-private compatibility wrappers

Primary files:

- `contexts/combat/runtime/session.py`

Current examples:

- `_phase`
- `_phase_banner`
- `_enemy_action_banner`
- `_enemy_action_steps`
- `_current_enemy_action`
- `_enemy_action_timer`

Current role:

- older underscore-shaped compatibility reads/writes kept on the runtime host

Default classification:

- tighten, then delete

### C3. `CombatState -> turn_context` field bridge

Primary files:

- `contexts/combat/domain/state.py`
- `contexts/combat/application/orchestration/action_executor.py`
- `contexts/combat/domain/effects/impl/pointer_queue_white.py`
- `contexts/combat/domain/effects/impl/misc.py`
- `contexts/combat/domain/services/pile_service.py`

Current role:

- keeps old `state.xxx` reads/writes alive while runtime data now really lives
  under `state.turn_context.xxx`
- `G3` batches 1-5 migrated the remaining runtime callers and touched tests
  onto direct `turn_context` ownership
- the final bridge properties were deleted in `G3` batch 5:
  - `frontier_used_batches`
  - `non_red_played_this_turn`
- remaining live bridge surface: `0`

Default classification:

- closed on `2026-04-23`

### C4. Low-value test/import compatibility helpers

Primary files:

- `contexts/combat/domain/enemies/entity.py`

Current examples:

- after `G4` batch 1, the import-path compatibility re-export is already gone
  and after `G4` batch 2, the planner test shim is also gone
- after `G4` batch 3, the no-op enemy legacy methods are also gone
- remaining live shim surface in this bucket: `0`

Default classification:

- closed on `2026-04-23`

### C5. Save/schema backward-compat bridges

Primary files:

- `contexts/combat/application/save/combat_save_service.py`
- `contexts/combat/application/save/save_snapshot_mapper.py`
- `contexts/combat/domain/player.py`

Current examples:

- player-side scalar energy projection snapshot handling for rollback
- fallback RNG restoration path

Default classification:

- superseded by `Save Reset Policy V1` and `Combat Contract Convergence V1`
- not part of the original compat-zero delete work; future edits should follow
  the newer save and energy-contract documents

### C6. Potential long-lived adapters that look like compat

Primary files:

- `contexts/combat/domain/arena_effects.py`
- `contexts/combat/domain/models/card_models.py`
- `contexts/combat/domain/effects/context.py`

Current examples:

- `ModelEnvironmentArenaEffect`
- `CardInstance.card_id`
- `CardInstance.cost_for_player(...)`
- `EffectContext` keeping older call-shape expectations in mind

Default classification:

- reviewed on `2026-04-23`
- retained:
  - `ModelEnvironmentArenaEffect`
  - `CardInstance.card_id`
  - `CardInstance.cost_for_player(...)`
- not retained:
  - `EffectContext`
    - treat as dead scaffold
    - if touched later, clean it in a separate tiny slice rather than under
      compat-zero

## Decision Gates

Automation should not start full cleanup until these are explicitly accepted.

### D0. What does "global compat-zero" mean for this repo?

Options:

- `Strict full zero`
  - delete MVC/test/import/save backward-compat together
- `Engineering zero`
  - delete runtime/test/MVC compatibility shells
  - keep save backward-compat and explicit retained adapters for now

Recommended:

- choose `Engineering zero`

Reason:

- it matches the user's current "safe incremental" preference
- it avoids mixing gameplay engineering cleanup with historical-save risk
- it is much more automation-friendly

### D1. Final fate of `CombatModel`

Options:

- `Delete in this program`
- `Freeze until visual/animation phase`

Recommended:

- delete in this program

Reason:

- the user explicitly wants to continue toward full MVC removal
- the remaining footprint is now small enough to remove deliberately
- keeping it longer has more architectural downside than technical necessity

### D2. How should the `state.xxx -> turn_context.xxx` bridge be removed?

Options:

- `Big bang`
  - delete bridge properties and dual reads/writes in one batch
- `Staged collapse`
  - migrate callers first
  - then delete bridge properties

Recommended:

- use `Staged collapse`

Reason:

- this bridge still has real call-site usage
- it is more coupled to runtime correctness than the MVC facade itself
- staged removal is safer for automation and easier to validate

### D3. Policy for low-value test/import shims

Options:

- `Allow test-only shims to remain`
- `Delete low-value shims once direct tests/imports are migrated`

Recommended:

- delete low-value shims once direct tests/imports are migrated

Reason:

- these shims mostly preserve old call shapes rather than valuable boundaries
- they are ideal automation targets once coverage is explicit

### D4. Save backward-compat policy

Options:

- `Delete legacy payload migration in this line`
- `Keep save backward-compat for now and revisit later`

Recommended:

- keep save backward-compat for now

Reason:

- this is high-risk and low-ROI compared with the other remaining compat layers
- it should be a dedicated save-lifecycle decision, not a side effect of MVC
  cleanup

### D5. Policy for "adapter-like" compatibility survivors

Examples:

- `ModelEnvironmentArenaEffect`
- `CardInstance.card_id`
- `CardInstance.cost_for_player(...)`

Options:

- `Treat as compat-zero blockers`
- `Treat as explicit retained adapters unless later proven harmful`

Recommended:

- treat them as explicit retained adapters for now

Reason:

- not every old-looking API is still accidental complexity
- deleting these without a stronger boundary decision would create churn with
  unclear payoff

## Automation Execution Plan

### G0. Decision freeze

Goal:

- lock `D0-D5`

Automation-safe:

- no

Stop condition:

- all accepted decisions are recorded

### G1. MVC facade plane removal

Goal:

- remove the remaining explicit MVC facade layer

Status:

- completed on `2026-04-23`

Completed work:

- replaced the remaining facade-oriented contract coverage with direct
  `CombatSession` / presentation-runtime / removal-guard assertions
- deleted:
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/mvc/factory.py`
- updated:
  - `scripts/debug_imports.py`
  - `scripts/check_combat_compat_zero.py`
  - `tests/combat/test_combat_mainline_allowlist_v1.py`

Automation-safe:

- yes, after `D0` and `D1`

Validation pack:

- `py -3.11 -m pytest tests/combat/test_combat_runtime_host_migration_v1.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_render_state_contracts.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_presentation_contract_v1.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_mainline_allowlist_v1.py -q`
- `py -3.11 scripts/check_combat_compat_zero.py`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`

Stop condition:

- met:
  - no live runtime/test/script imports of
    `contexts.combat.mvc.model.CombatModel`
  - no remaining runtime file for `contexts/combat/mvc/factory.py`
  - only guard-only textual references remain in two removal-assertion tests

### G2. Session wrapper tightening

Goal:

- remove remaining underscore-shaped session compatibility wrappers

Status:

- completed on `2026-04-23`

Completed work:

- confirmed the underscore compatibility wrappers had no remaining live reads
  outside guard coverage
- deleted the following wrapper properties from `CombatSession`:
  - `_phase`
  - `_phase_banner`
  - `_enemy_action_banner`
  - `_enemy_action_steps`
  - `_current_enemy_action`
  - `_enemy_action_timer`
- tightened structural guards so the removed wrapper names cannot silently
  re-enter live code

Automation-safe:

- yes, after `G1`

Validation pack:

- `py -3.11 -m pytest tests/combat/test_combat_phase_machine.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- `py -3.11 -m pytest tests/combat/test_enemy_turn_runtime_driver.py tests/combat/test_presentation_runtime.py -q`

Stop condition:

- met:
  - no underscore compatibility wrapper definitions remain on `CombatSession`
  - no live `session._...` wrapper reads remain outside the guard test

### G3. `turn_context` bridge collapse

Goal:

- make `state.turn_context` the only runtime home for these fields

Status:

- completed on `2026-04-23`

Primary work:

- migrate dual reads/writes in:
  - `action_executor.py`
  - `pointer_queue_white.py`
  - `misc.py`
  - `pile_service.py`
- migrate tests to assert through `state.turn_context`
- delete bridge properties from `CombatState`

Completed work so far:

- batch 1 collapsed the touched runtime writes/reads in:
  - `action_executor.py`
  - `pointer_queue_white.py`
  - `misc.py`
  - `pile_service.py`
- moved the touched test setup/assertions onto `state.turn_context` in:
  - `tests/combat/test_action_queue.py`
  - `tests/combat/test_white_endpoint_and_summary.py`
  - `tests/combat/test_json_white_cards.py`
- tightened `scripts/check_combat_compat_zero.py` so these files cannot silently
  drift back to `state.xxx` writes for the migrated fields
- batch 2 collapsed the enemy tween metadata path in:
  - `enemy_tween_planner.py`
- moved the tween-metadata planner/cleanup tests onto `state.turn_context` in:
  - `tests/combat/test_enemy_tween_metadata_planner.py`
  - `tests/combat/test_enemy_cleanup_coordinator.py`
- deleted the `CombatState` bridge properties for:
  - `enemy_tween_start_time`
  - `enemy_tween_duration`
  - `enemy_tween_from_idx`
  - `enemy_tween_to_idx`
- tightened `scripts/check_combat_compat_zero.py` so the deleted tween bridge
  surface cannot silently return
- batch 3 tightened the touched runtime helper branches in:
  - `player.py`
  - `powers.py`
  - `effects/base.py`
  - `effects/impl/red.py`
  - `effects/impl/pile.py`
  - `traits_demo_impl.py`
- batch 3 deleted the following `CombatState` bridge properties:
  - `draw_locked`
  - `reposition_count_this_turn`
  - `reposition_limit_per_turn`
  - `frontier_batch_counter`
  - `red_extra_draw_context`
  - `red_frontier_damage_bonus_current_play`
  - `red_offcolor_damage_bonus_current_play`
  - `force_frontier_next_cards`
  - `traits_double_current_effects`
  - `scribble_played_this_turn`
- batch 3 replaced the remaining bridge-oriented core-state contract test with
  explicit `turn_context` ownership coverage
- tightened `scripts/check_combat_compat_zero.py` so this removed bridge subset
  cannot silently return through direct `state.xxx` access
- batch 4 moved `render_state_assembler.py` off the `lock_queue_active` bridge
  onto direct `turn_context` reads
- batch 4 deleted the `CombatState.lock_queue_active` bridge property
- batch 4 added an explicit render-state contract for `lock_queue` projection
- tightened `scripts/check_combat_compat_zero.py` so the removed
  `lock_queue_active` bridge cannot silently return through direct
  `state.xxx` access
- batch 5 tightened `action_executor.py` so frontier batch reservation now goes
  through `state.turn_context`
- batch 5 moved `render_state_assembler.py` off the
  `frontier_used_batches` bridge onto direct `turn_context` reads
- moved the final render/red-test touched setup/assertions onto
  `state.turn_context` in:
  - `tests/combat/test_json_red_cards.py`
  - `tests/combat/test_combat_render_state_contracts.py`
- batch 5 deleted the final `CombatState` bridge properties:
  - `frontier_used_batches`
  - `non_red_played_this_turn`
- tightened `scripts/check_combat_compat_zero.py` so this removed final bridge
  subset cannot silently return through direct `state.xxx` access

Phase boundary:

- the `CombatState -> turn_context` bridge surface is now fully removed from
  live runtime callers and the touched contract coverage
- any remaining red-content/runtime failures stay out of this phase by
  accepted scope and decision gates

Automation-safe:

- yes, after `D2`

Validation pack:

- `py -3.11 -m pytest tests/combat/test_reposition_and_lockqueue.py -q`
- `py -3.11 -m pytest tests/combat/test_white_endpoint_and_summary.py -q`
- `py -3.11 -m pytest tests/combat/test_pointer_engine.py -q`
- `py -3.11 -m pytest tests/combat/test_content_window_native_batch1.py tests/combat/test_content_window_native_batch2.py -q`

Stop condition:

- met:
  - runtime no longer writes or reads the bridged fields through `state.xxx`

### G4. Low-value test/import shim cleanup

Status:

- completed on `2026-04-23`

Goal:

- delete remaining narrow test/import compatibility helpers

Primary work:

- migrate imports off `contexts.combat.domain.effects.implementations`
- migrate tests off `ChoreResolutionOrchestrator._map_actions(...)`
- remove `Enemy.select_skill_for_turn()` / `Enemy.use_selected_skill()`
- delete the shim bodies once direct usage is gone

Completed work so far:

- batch 1 migrated `tests/combat/test_damage_service.py` off the legacy
  `contexts.combat.domain.effects.implementations` import path
- batch 1 deleted:
  - `contexts/combat/domain/effects/implementations.py`
- tightened `scripts/check_combat_compat_zero.py` so the removed shim file and
  import path cannot silently return
- batch 2 migrated `tests/combat/test_action_queue.py` off the
  `ChoreResolutionOrchestrator._map_actions(...)` compatibility shim onto
  direct `ChoreResolutionPlanner` coverage
- batch 2 deleted:
  - `ChoreResolutionOrchestrator._map_actions(...)`
- tightened `scripts/check_combat_compat_zero.py` so the removed shim method
  and call shape cannot silently return
- batch 3 deleted the no-op enemy legacy methods from
  `contexts/combat/domain/enemies/entity.py`:
  - `select_skill_for_turn()`
  - `use_selected_skill()`
- tightened `scripts/check_combat_compat_zero.py` so the removed enemy legacy
  method definitions and call sites cannot silently return

Phase boundary:

- the low-value test/import shim surface covered by `G4` is now fully removed
- any remaining work after `G4` is decision-gated retained-adapter review, not
  more automation-safe shim deletion

Automation-safe:

- yes, after `D3`

Validation pack:

- `py -3.11 -m pytest tests/combat/test_damage_service.py -q`
- `py -3.11 -m pytest tests/combat/test_action_queue.py -q`
- `py -3.11 -m pytest tests/combat/test_enemy_execution_flow.py tests/combat/test_tutor_intent_text.py -q`

Stop condition:

- met:
  - the shim files or shim methods are physically removed

### G5. Retained adapter review

Status:

- completed as a decision-gated review on `2026-04-23`

Goal:

- explicitly document what is intentionally retained after engineering zero

Candidates:

- save backward-compat migration
- `ModelEnvironmentArenaEffect`
- `CardInstance.card_id`
- `CardInstance.cost_for_player(...)`
- `EffectContext`

Resolution:

- retained backward-compat boundary:
  - combat save/load migration and session save/apply entrypoints
- retained intentional runtime adapter:
  - `ModelEnvironmentArenaEffect`
  - `DefaultTurnStartEnvironmentInjector`
- retained stable convenience contract:
  - `CardInstance.card_id`
  - `CardInstance.cost_for_player(...)`
- not retained under this bucket:
  - `EffectContext`
    - dead scaffold candidate
    - move to a later tiny cleanup slice if needed
- explicitly out of scope for this closure:
  - player scalar-energy / colored-pool convergence
    - treat as a separate future decision line
- phase result:
  - combat global compat-zero is closed at `Engineering Zero`
  - no further automatic delete wave should continue under this same plan

Automation-safe:

- no

Stop condition:

- met:
  - retained adapters were promoted to explicit contracts
  - non-retained survivors were split into later dedicated follow-up lines

## Separate Backlog That Must Not Be Blended In

These are not compat-zero tasks:

- red runtime/content failures in `tests/combat/test_json_red_cards.py`
- animation/video blocking semantics
- combat visual/content iteration
- save-schema redesign

If automation hits those areas while executing `G1-G4`, it should stop and
report instead of silently expanding scope.

## Recommended Decision Package

If we want to start automation with the least ambiguity, accept this package:

1. `D0 = Engineering zero`
2. `D1 = Delete CombatModel in this program`
3. `D2 = Staged collapse for turn_context bridge`
4. `D3 = Delete low-value test/import shims after migration`
5. `D4 = Keep save backward-compat for now`
6. `D5 = Treat adapter-like survivors as retained unless later re-decided`

This yields a clean automation order:

1. `G1` remove MVC facade plane
2. `G2` remove session wrapper compat
3. `G3` collapse `turn_context` bridge
4. `G4` delete low-value test/import shims
5. `G5` document retained adapters and stop

## Default Validation Discipline

After each small step:

- `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`

After each bridge cleanup step:

- rerun the focused pack for the touched slice
- do not jump directly to unrelated combat content failures

After each completed phase:

- run the smallest green smoke set that still proves the phase boundary
- commit before starting the next phase
