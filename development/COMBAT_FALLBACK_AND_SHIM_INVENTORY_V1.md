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

Migration question:
- which remaining effect types are still planner-negative, and which deserve queue-native implementations next

### ActionExecutor Top-Of-Draw Inline Resolution

File:
- [action_executor.py](/D:/PHD_SIMULATER/contexts/combat/application/orchestration/action_executor.py)

Current behavior:
- `_resolve_top_card_effects(...)` plans queued actions when possible
- otherwise it falls back through `execute_effect_once(...)`

Migration question:
- should top-of-draw execution keep this hybrid approach or gain a more explicit queue-native adapter

### PlayTopOfDrawThenExhaust Effect Inline Loop

File:
- [pile.py](/D:/PHD_SIMULATER/contexts/combat/domain/effects/impl/pile.py)

Current behavior:
- `PlayTopOfDrawThenExhaustEffect` still loops effect objects directly and uses `execute_effect_once(...)`

Migration question:
- should this effect be routed fully through orchestration/action queue instead of local inline execution

## Next Default Use

When we plan the next combat runtime cleanup pass, start from this list instead of rediscovering queue-external fallback seams by repo search.
