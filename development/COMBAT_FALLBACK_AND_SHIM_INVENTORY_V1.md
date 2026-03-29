# Combat Fallback And Shim Inventory V1

## Purpose

Track the remaining localized fallback and compatibility surfaces after the Phase A-D mainline cleanup.

This document is not a list of approved regressions. It is a migration inventory for seams that still exist, but no longer own combat ordering semantics.

## Local Compatibility Shims

### Player Failure Stubs

File:
- [player.py](/D:/PHD_SIMULATER/contexts/combat/domain/player.py)

Items:
- `_run_legacy_turn_start_reactions(...)`
- `_run_legacy_combat_event_reactions(...)`

Current status:
- allowed to exist locally
- zero call-sites required
- both raise immediately if reached

Exit condition:
- delete both methods after confirming no tooling/tests still rely on their presence

### EffectExecutor Old-Name Wrappers

File:
- [executor.py](/D:/PHD_SIMULATER/contexts/combat/domain/effects/executor.py)

Items:
- `execute_legacy_card_fallback(...)`
- `execute_card_effects(...)`
- `execute_legacy_effect_data_fallback(...)`
- `execute_effect_data(...)`
- `execute_legacy_effect_fallback(...)`
- `execute_effect(...)`

Current status:
- allowed to exist only inside `EffectExecutor`
- zero Python call-sites required outside the wrapper class itself
- active mainline must use `execute_card_fallback(...)`, `execute_effect_payload(...)`, `execute_effect_once(...)`

Exit condition:
- delete wrappers after one full expansion cycle stays green with zero reintroduction pressure

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

When we plan the next combat runtime cleanup pass, use this document as the starting migration list instead of rediscovering seams by repo search.
