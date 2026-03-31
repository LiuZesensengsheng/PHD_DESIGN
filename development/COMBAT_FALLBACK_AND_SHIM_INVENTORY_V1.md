# Combat Fallback And Shim Inventory V1

## Purpose

Track the remaining queue-external fallback surfaces after the compat-zero cleanup.

This document is no longer a list of allowed compatibility shims. The localized Player and `EffectExecutor` shims were physically deleted on `2026-03-30`.

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
  - as of `2026-03-31`, it no longer loops top-card effects locally through `execute_effect_once(...)`
  - direct fallback execution now delegates into `ActionExecutor` so top-of-draw resolution reuses the queue-native top-card path
- `swap_with_paper`:
  - as of `2026-03-31`, the active white thesis card no longer depends on per-effect fallback
  - planner now maps it into a queue action and `ActionExecutor` toggles `paper_ally.is_front` directly
  - `tests/combat/test_active_queue_boundaries.py` active fallback scan is now expected to stay at zero
- Shared per-effect resolution spine:
  - as of `2026-03-31`, `CardPlayOrchestrator._resolve_effects_one_by_one(...)` and `ActionExecutor._resolve_top_card_effects(...)` now share `effect_resolution_runner.py`
  - planner dispatch, `execute_effect_once(...)` fallback, fallback follow-up collection, and nested action draining now run through one implementation
  - card-play timing windows remain owned by `CardPlayOrchestrator`, so the timing contract stays local while the runtime skeleton is deduplicated
- Design-v2 storage effect families:
  - as of `2026-03-31`, `add_steadfast_token` and `add_paradigm` are no longer unknown content-only effect types
  - factory, effect registry, planner, action executor, and `CombatState` now all recognize them through minimal state-carrier semantics
  - current scope is intentionally narrow: these effects can now resolve through the mainline and persist state, but their richer trigger semantics are still future work

## Queue-External Fallback Surfaces

These are still real runtime seams, but they are no longer compatibility-owned. They use the neutral fallback API and remain valid until we explicitly queue them or decide to keep them.

### CardPlayOrchestrator Full-Card Fallback

File:
- [card_play_orchestrator.py](/D:/PHD_SIMULATER/contexts/combat/application/orchestration/card_play_orchestrator.py)

Current behavior:
- when effect planning is unavailable, runtime falls back through `execute_card_fallback(...)`

Migration question:
- should more effect families be planned/queued so this path becomes rarer

### CardPlayOrchestrator Per-Effect Fallback

File:
- [card_play_orchestrator.py](/D:/PHD_SIMULATER/contexts/combat/application/orchestration/card_play_orchestrator.py)

Current behavior:
- when `EffectPlanner.plan(...)` returns `None`, runtime falls back through `execute_effect_once(...)`
- the per-effect planning and fallback skeleton is now shared with top-of-draw through `effect_resolution_runner.py`

Migration question:
- which remaining effect types are still planner-negative, and which deserve queue-native implementations next

### ActionExecutor Top-Of-Draw Inline Resolution

File:
- [action_executor.py](/D:/PHD_SIMULATER/contexts/combat/application/orchestration/action_executor.py)

Current behavior:
- `_resolve_top_card_effects(...)` plans queued actions when possible
- otherwise it falls back through `execute_effect_once(...)`
- its planner/fallback/follow-up ordering now reuses the same shared runner as card play

Migration question:
- should we keep the hybrid path or continue by shrinking planner-negative effect coverage until this fallback becomes rare enough to treat as intentional

## Next Default Use

When we plan the next combat runtime cleanup pass, start from this list instead of rediscovering queue-external fallback seams by repo search.

## Phase 2B Note

- A repository scan over `data/cards` now reports zero effect types that are unknown to the planner/mainline by type.
- The next non-visual runtime step is no longer parser/planner recognition; it is deciding whether to:
  - activate the design-v2 pack in the runtime load path
  - or implement the first real trigger semantics for `paradigm` / `steadfast`
