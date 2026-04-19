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
- session-local mutable runtime data is now hosted behind
  `CombatSessionRuntimeState`; `CombatSession` keeps compatibility properties for
  current render/tests while local host data is being tightened.
- `CombatModel` is still present as a compatibility facade because controller,
  some orchestration paths, and many tests still construct or receive
  `CombatModel`.
- `CombatModel` no longer uses broad `__getattr__` / `__setattr__` passthrough.
  Its surface is now explicit.
- New runtime work should prefer `session` directly unless a caller still needs
  the compatibility facade.

## Quantitative Baseline

Repository scan on `2026-04-19` shows `CombatModel` currently exposes `32`
non-constructor surface members plus the plain `session` host reference.

- stable shared surface: `16`
- test/tool surface: `16`
- transitional compatibility surface: `0`

More important than the raw total:

- transitional seams still referenced by non-test runtime code: `0`
- transitional seams currently referenced only by tests: `0`

That means the **runtime-mainline backlog for host-private combat seams is
closed for this migration slice**. The remaining work is no longer "get
orchestrators off old helpers". It is to decide how much of the remaining
compatibility facade should:

- stay as intentional test/tool surface
- move to direct `session` / collaborator usage in tests
- or be hard-deleted once compatibility pressure is actually gone

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

The current `CombatModel` surface no longer exposes any remaining private
combat-runtime compatibility seam methods or properties.

Current count: `0`

Of these `0` seams:

- `0` are still touched by non-test runtime code
- `0` are currently test-only compatibility surface

## Observed Usage Snapshot

Repository scan on `2026-04-18` shows the following patterns:

- high-frequency shared usage:
  - `state`: `235` references across `28` files
  - `play_card(...)`: `125` references across `22` files
  - `end_turn()`: `28` references across `12` files
  - `get_renderable_state()`: `18` references across `8` files
- runtime mainline no longer touches the last turn-start / heart-demon
  compatibility helpers:
  - `PlayerTurnOrchestrator` now depends on:
    - `PlayerBlockDecayPolicy`
    - `DefaultTurnStartEnvironmentInjector`
  - `IdealPolicy` and `CombatPostResolutionPolicy` now depend on:
    - `HeartDemonService`
- enemy-turn ownership is also more explicit than the earlier inventory pass:
  - `TurnFlowOrchestrator` now delegates start/end housekeeping to:
    - `EnemyTurnStartPolicy`
    - `EnemyTurnEndPolicy`
  - enemy-side block decay moved into:
    - `EnemyBlockDecayPolicy`
- combat startup ownership is now explicit too:
  - `CombatSession.start_combat()` delegates to `CombatStartOrchestrator`
  - startup sequencing no longer lives inline on the session host:
    - starter deck bootstrap
    - combat-start reaction dispatch
    - opening shuffle / innate move / opening draw
    - first-player-turn handoff
- stress-threshold judgment handling is now explicit:
  - `CombatSession` wires the `StressThresholdReached` subscription only
  - `StressThresholdHandler` owns:
    - target ideal selection
    - verdict application
    - `JudgmentResolved` publish
    - combat-loss marking on judgment-flow failure
- enemy-turn sequence driving is now explicit:
  - `CombatSession` delegates enemy-turn timed progression to `EnemyTurnRuntimeDriver`
  - the runtime driver now owns:
    - enemy-turn entry sequencing
    - step progression / drain-to-completion
    - enemy action banner updates during execution
- presentation shaping is now explicit:
  - `CombatPresentationBridge` remains the lower-level lease/log/consumer owner
  - `CombatPresentationRuntime` now owns:
    - phase/enemy banner event shaping
    - card-play / enemy-step presentation payload shaping
    - command-gate delegation facade used by the session
- runtime collaborator assembly is now explicit:
  - `CombatSession.__init__` no longer constructs the full collaborator graph inline
  - `build_default_combat_session_services(...)` now acts as the default composition root
  - `CombatSessionServices` is the explicit bundle attached by the session host
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
  - the enemy-cleanup mainline now reaches chore resolution through the explicit
    `ChoreResolutionOrchestrator`, not through a generic callback seam
- test-heavy shared/testing surface:
  - `effect_executor`
  - `card_play_orchestrator`
  - `player_turn_orchestrator`
- session-first usage already exists in a few key places:
  - `contexts/simulation/headless_combat_executor.py`
  - presentation contract tests
  - render-state contract tests
  - headless executor tests

## What This Means

- `CombatModel` is no longer a broad runtime host, but it is still a meaningful
  compatibility facade.
- The runtime-mainline migration goal for this slice is met:
  production combat orchestration no longer depends on the last three
  host-private helper seams.
- The remaining pressure is mostly test/compat cleanup, not gameplay runtime
  ownership confusion.
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

### Completed in this slice

- turn-start host seam absorbed:
  - `_inject_turn_start_environment_cards(...)`
  - `_decay_player_block_at_turn_start(...)`
- ideal/judgment follow-up seam absorbed:
  - `_inject_heart_demons(...)`
- enemy-turn start/end housekeeping split into explicit policies:
  - `EnemyTurnStartPolicy`
  - `EnemyTurnEndPolicy`
  - `EnemyBlockDecayPolicy`
- combat-start host body absorbed:
  - startup sequencing now lives in `CombatStartOrchestrator`
  - `CombatSession.start_combat()` stays as the stable runtime entrypoint only
- stress-threshold host body absorbed:
  - judgment event flow now lives in `StressThresholdHandler`
  - the session keeps only event subscription wiring
- enemy-turn driver host body absorbed:
  - timed enemy-turn progression now lives in `EnemyTurnRuntimeDriver`
  - the session keeps phase-machine entrypoints only
- presentation shaping host body absorbed:
  - banner/event payload shaping now lives in `CombatPresentationRuntime`
  - the bridge remains the lower-level presentation lease/log owner
- composition-root body absorbed:
  - default runtime collaborator assembly now lives in `build_default_combat_session_services(...)`
  - the session host now attaches a bundle instead of constructing each collaborator inline

Translated into current backlog count:

- priority `P1`: `0` runtime-owned transitional seams
- priority `P2`: `0` test-only transitional seams

### Likely next cuts

- no private `CombatModel` compatibility seams remain in the active runtime
  inventory for this migration line
- the remaining `CombatSession` cleanup is now optional shape work rather than
  urgent ownership repair:
  - save/load facade extraction if we want an even thinner host
  - trimming how many collaborators remain explicitly attached on the session
    surface
- move test-only callers toward `session` or explicit collaborators where that
  improves clarity instead of preserving broad `CombatModel` ownership
- decide which remaining helper methods are still worth keeping as explicit
  compatibility wrappers and which can be deleted after the next migration pass

### Guardrail

- `CombatModel` surface growth should be explicit and reviewed.
- If a new member is added to `CombatModel`, update:
  - this inventory
  - the surface allowlist test
