# Combat Runtime Surface Inventory V1

## Purpose

Record the current combat runtime host surface after `CombatSession` became the
canonical runtime owner and `CombatModel` was reduced to an explicit
compatibility facade.

This document is intentionally about **surface shape**, not content semantics.
It answers:

- what `CombatModel` still exposes today
- which parts are stable shared entrypoints vs temporary compatibility seams
- where repo usage is still concentrated
- which cuts are safest next

## Current Host Shape

- `CombatSession` is the canonical combat runtime host for UI, headless, and
  save/load.
- `CombatModel` is still present as a compatibility facade because controller,
  some orchestration paths, and many tests still construct or receive
  `CombatModel`.
- `CombatModel` no longer uses broad `__getattr__` / `__setattr__` passthrough.
  Its surface is now explicit.
- New runtime work should prefer `session` directly unless a caller still needs
  the compatibility facade.

## Quantitative Baseline

Repository scan on `2026-04-18` shows `CombatModel` currently exposes `44`
non-constructor surface members plus the plain `session` host reference.

- stable shared surface: `16`
- test/tool surface: `16`
- transitional compatibility surface: `12`

More important than the raw total:

- transitional seams still referenced by non-test runtime code: `3`
- transitional seams currently referenced only by tests: `8`

That means the **actual runtime-mainline seam backlog is small but real**. The
highest-value governance work is not "shrink every exposed member at once". It
is to eliminate the `3` transitional seams that production runtime code still
depends on.

## CombatModel Explicit Surface

### 1. Shared entrypoints that are still reasonable to keep for now

- host/state:
  - `session`
  - `state`
  - `event_bus`
  - `phase_machine`
- runtime commands:
  - `start_combat()`
  - `end_turn()`
  - `play_card(...)`
  - `update(...)`
  - `enemy_turn()`
  - `is_player_turn()`
  - `can_accept_commands()`
- render/save:
  - `get_renderable_state()`
  - `create_save_snapshot(...)`
  - `to_snapshot_dict(...)`
  - `apply_save_snapshot(...)`
  - `from_snapshot_dict(...)`

### 2. Test / tooling seams that are still intentionally exposed

- runtime collaborators:
  - `effect_executor`
  - `card_play_orchestrator`
  - `player_turn_orchestrator`
- runtime toggles:
  - `auto_draw_on_turn_start`
  - `_async_enemy_sequence`
- presentation compatibility:
  - `busy_reason`
  - `presentation_consumer`
  - `presentation_log`
  - `pending_presentation`
  - `drain_pending_presentation()`
  - `set_presentation_consumer(...)`
  - `acquire_command_lock(...)`
  - `release_command_lock(...)`
  - `clear_command_locks()`
  - `acknowledge_presentation_event(...)`
  - `acknowledge_presentation_lease(...)`

### 3. Transitional private compatibility seams

These are the main remaining signs that some orchestration/tests still treat
`CombatModel` like the old runtime host:

- `_handle_after_card_play(...)`
- `_apply_chore_resolution_actions(...)`
- `_prune_defeated_enemies_and_adjust_pointer()`
- `_update_enemy_turn(...)`
- `_inject_turn_start_environment_cards(...)`
- `_check_combat_end()`
- `_handle_card_played(...)`
- `_process_chore_host_enemy_turn_start()`
- `_decay_player_block_at_turn_start(...)`
- `_inject_heart_demons(...)`
- `_phase_banner`
- `_enemy_action_banner`

These are compatibility-owned seams, not the preferred runtime ownership model.

Current count: `12`

Of these `12` seams:

- `3` are still touched by non-test runtime code
- `9` are currently test-only compatibility surface

## Observed Usage Snapshot

Repository scan on `2026-04-18` shows the following patterns:

- high-frequency shared usage:
  - `state`: `235` references across `28` files
  - `play_card(...)`: `125` references across `22` files
  - `end_turn()`: `28` references across `12` files
  - `get_renderable_state()`: `18` references across `8` files
- orchestration still touches a few private compatibility seams:
  - `player_turn_orchestrator.py` uses
    `model._inject_turn_start_environment_cards(...)` and
    `model._decay_player_block_at_turn_start(...)`
  - `ideal_policy.py` uses `model._inject_heart_demons(...)`
- `enemy cleanup` runtime ownership has already moved off the host-private seam:
  - `TurnFlowOrchestrator` now depends on explicit `EnemyCleanupCoordinator`
  - `CombatModel._prune_defeated_enemies_and_adjust_pointer()` remains a
    compatibility wrapper for tests and legacy callers, not a mainline
    orchestration dependency
  - the coordinator has now been split into named collaborators:
    - `EnemyChoreFollowUpPolicy`
    - `EnemyPointerRetargetPolicy`
    - `EnemyTweenMetadataPlanner`
  - that makes pointer/tween behavior separately testable and prepares the path
    toward future `plan -> presentation gate -> commit` cleanup flow
  - chore completion and follow-up resolution are now also explicit runtime
    ownership instead of private coordinator internals
- test-heavy seams:
  - `effect_executor`
  - `card_play_orchestrator`
  - `player_turn_orchestrator`
  - `_update_enemy_turn(...)`
  - `_phase_banner`
  - `_enemy_action_banner`
  - `_handle_after_card_play(...)`
  - `_check_combat_end()`
- session-first usage already exists in a few key places:
  - `contexts/simulation/headless_combat_executor.py`
  - presentation contract tests
  - render-state contract tests
  - headless executor tests

## What This Means

- `CombatModel` is no longer a broad runtime host, but it is still a meaningful
  compatibility facade.
- The largest remaining compatibility pressure is not controller/view code.
  It is a small set of orchestration and test paths that still depend on
  private runtime helpers.
- The current backlog is easier to reason about as `3` runtime-owned seam
  clusters, not as `12` equally urgent members.
- The current surface is already narrow enough that future work should stop
  adding new members and instead either:
  - move new callers to `session`
  - or create one small named seam for the specific collaborator that still
    needs host access

## Recommended Next Cuts

### Safe next cuts

- Keep `CombatModel` stable for shared command/render/save entrypoints during the
  current migration phase.
- Prefer `model.session` or direct `CombatSession` injection for new headless,
  save/load, or presentation-side work.
- Do not add new dynamic passthrough or generic forwarding back into
  `CombatModel`.

### Likely high-ROI follow-up seams

- turn-start host seam:
  - absorb `_inject_turn_start_environment_cards(...)`
  - absorb `_decay_player_block_at_turn_start(...)`
- enemy-turn cleanup seam:
  - first slice landed: explicit `EnemyCleanupCoordinator` now owns mainline
    cleanup
  - second slice landed: pointer retarget and tween metadata are now separate
    policy / planner collaborators
  - third slice landed: chore follow-up is now its own named cleanup policy
  - remaining work is shrinking the compatibility wrapper further, not untangling
    unnamed cleanup internals
- ideal/judgment follow-up seam:
  - absorb `_inject_heart_demons(...)`

Translated into concrete backlog count:

- priority `P1`: `3` runtime-owned transitional seams
  - `_inject_turn_start_environment_cards(...)`
  - `_decay_player_block_at_turn_start(...)`
  - `_inject_heart_demons(...)`
- priority `P2`: `9` test-only transitional seams
  - `_handle_after_card_play(...)`
  - `_apply_chore_resolution_actions(...)`
  - `_prune_defeated_enemies_and_adjust_pointer()`
  - `_update_enemy_turn(...)`
  - `_check_combat_end()`
  - `_handle_card_played(...)`
  - `_process_chore_host_enemy_turn_start()`
  - `_phase_banner`
  - `_enemy_action_banner`

### Guardrail

- `CombatModel` surface growth should be explicit and reviewed.
- If a new member is added to `CombatModel`, update:
  - this inventory
  - the surface allowlist test
