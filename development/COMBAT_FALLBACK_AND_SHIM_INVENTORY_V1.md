# Combat Fallback And Shim Inventory V1

## Purpose

Track combat fallback ownership after the compat-zero cleanup.

This document is no longer a list of allowed compatibility shims. The localized Player and `EffectExecutor` shims were physically deleted on `2026-03-30`, and the remaining card-play/top-card runtime fallback seams were removed from mainline on `2026-04-03`.

## Cleared Local Compatibility Shims

- `Player._run_legacy_turn_start_reactions(...)`: deleted
- `Player._run_legacy_combat_event_reactions(...)`: deleted
- `EffectExecutor.execute_legacy_card_fallback(...)`: deleted
- `EffectExecutor.execute_card_effects(...)`: deleted
- `EffectExecutor.execute_legacy_effect_data_fallback(...)`: deleted
- `EffectExecutor.execute_effect_data(...)`: deleted
- `EffectExecutor.execute_legacy_effect_fallback(...)`: deleted
- `EffectExecutor.execute_effect(...)`: deleted

## Recently Resolved Runtime Seams

- `PlayTopOfDrawThenExhaustEffect.execute(...)`:
  - as of `2026-03-31`, it no longer loops top-card effects locally through the direct-exec helper that is now named `execute_effect_once_direct(...)`
  - top-card resolution now reuses `ActionExecutor` ownership instead of effect-local sequencing
- `swap_with_paper`:
  - as of `2026-03-31`, the active white thesis card no longer depends on per-effect fallback
  - planner now maps it into a queue action and `ActionExecutor` toggles `paper_ally.is_front` directly
- Shared per-effect resolution spine:
  - as of `2026-03-31`, card play and top-of-draw started sharing `effect_resolution_runner.py`
  - as of `2026-04-03`, that shared runner became queue-only
  - unplanned effects now raise `QueueOnlyPlanningError` instead of silently falling back through direct execution
  - effects whose conditions are intentionally not met now plan as `[]`, so "no-op" is explicit and stable
- Card-play / top-of-draw mainline fallback removal:
  - as of `2026-04-03`, `CardPlayOrchestrator` no longer keeps full-card fallback or per-effect fallback branches
  - as of `2026-04-03`, `ActionExecutor._resolve_top_card_effects(...)` no longer keeps a hybrid fallback path
  - `fallback_action_policy.py` was deleted
- Reposition target fallback removal:
  - as of `2026-04-03`, `reposition` no longer infers the pointer target when card play does not provide an explicit enemy target
  - queue planning for `reposition` now requires an explicit `target_id`
- `JuggernautPower` damage commit fallback removal:
  - as of `2026-04-03`, `JuggernautPower` no longer falls back to `enemy.take_damage(...)` when `DamageService.apply_damage_to_enemy_and_commit(...)` fails
  - commit failures now stay visible as an explicit runtime error path instead of silently switching damage semantics
- `DamageService` commit fallback removal:
  - as of `2026-04-03`, `DamageService.apply_damage_to_enemy_and_commit(...)` no longer assumes a hit committed successfully when `enemy.commit_damage(...)` raises
  - it also no longer retries through an aggregated commit path when per-event commit handling breaks
- Demo trait damage fallback removal:
  - as of `2026-04-03`, `ExtravertTrait` and `FeelingTrait` no longer fall back to direct `enemy.take_damage(...)` when unified enemy damage application fails
  - their damage semantics now stay aligned with the shared damage service instead of switching onto a direct-write side path
- Enemy-turn step fallback removal:
  - as of `2026-04-03`, `CombatModel.enemy_turn()` no longer keeps a local log-and-continue loop for enemy action steps
  - enemy-turn aliases now reuse the phase-machine mainline, and step callback failures stop the sequence instead of continuing to later steps
- `DefaultIntentSelector` filtered-pool fallback removal:
  - as of `2026-04-03`, it returns `None` when cooldown/condition filtering leaves no weighted candidate
  - it no longer chooses from filtered-out candidates in that case
- Design-v2 storage effect families:
  - as of `2026-03-31`, `add_steadfast_token` and `add_paradigm` are no longer unknown content-only effect types
  - factory, effect registry, planner, action executor, and `CombatState` now all recognize them through minimal state-carrier semantics

## Active Pack Boundary

- As of `2026-03-31`, the active `red/white` runtime card scan in
  [test_active_queue_boundaries.py](/D:/PHD_SIMULATER/tests/combat/test_active_queue_boundaries.py)
  expects the explicit fallback allowlist to stay at `0`.
- As of `2026-04-03`, the queue-only follow-up kept that boundary green together with:
  - `scripts/check_combat_compat_zero.py`
  - `tests/combat/test_combat_mainline_allowlist_v1.py`
  - `tests/combat`
  - `tests/simulation`
- This still does **not** mean the runtime has no direct-effect helpers anywhere.
- It means the checked-in combat mainline and active `red/white` packs no longer rely on queue-external fallback branches during card play or top-card resolution.

## Mainline Status

- `CardPlayOrchestrator` is queue-only for effect resolution.
- `ActionExecutor._resolve_top_card_effects(...)` is queue-only for effect resolution.
- Planner-negative effects in combat mainline are now explicit errors, not silent alternate execution paths.
- `reposition` is now an explicit-target mechanic, not a pointer-target fallback mechanic.
- Shared enemy damage commit now uses explicit per-event commit semantics instead of silent assume-success or aggregate fallback semantics.
- Demo trait retaliation/ping damage no longer switches to direct `enemy.take_damage(...)` when unified damage application fails.
- Enemy-turn aliases now reuse the phase-machine mainline, and enemy action step failures are explicit instead of log-and-continue.
- `DefaultIntentSelector` now surfaces an empty filtered pool as `None` instead of choosing from filtered-out candidates.
- New combat effect families must either:
  - gain planner/action support
  - intentionally plan as `[]` when their condition does nothing
  - or stay outside mainline in tests/tools until they are modeled properly

## Remaining Direct Execution Helpers Outside Mainline

These helpers still exist, but they are no longer mainline fallback seams:

- [executor.py](/D:/PHD_SIMULATER/contexts/combat/domain/effects/executor.py)
  - `execute_effect_payload_direct(...)`
  - `execute_effect_once_direct(...)`

Current intended use:

- targeted tests
- low-level effect implementation coverage
- tooling or debug flows that explicitly opt into direct execution

Not intended use:

- card-play orchestrator mainline
- top-of-draw inline mainline
- new hybrid "plan if possible, otherwise direct execute" branches

## Next Default Use

When combat runtime work resumes, start from planner coverage or effect modeling questions instead of reintroducing fallback seams into orchestrators.

## Phase 2B Note

- A repository scan over `data/cards` reports zero effect types that are unknown to the planner/mainline by type.
- The next non-visual runtime step is no longer parser/planner recognition; it is deciding whether to:
  - activate the design-v2 pack in the runtime load path
  - or implement the first real trigger semantics for `paradigm` / `steadfast`
