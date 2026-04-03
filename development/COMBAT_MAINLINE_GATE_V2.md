# Combat Mainline Gate V2

## Status

- Active gate as of `2026-03-29`
- Hard-delete cleanup completed on `2026-03-30`
- Scope remains combat runtime semantics only
- Supersedes `COMBAT_MAINLINE_GATE_V1.md` as the active extension gate
- `COMBAT_TIMING_CONTRACT_V1` and `COMBAT_EVENT_CONTRACT_V1` remain the semantic source of truth

## What V2 Means

- Combat mainline call-sites are compat-zero for the core seams we targeted in Phase A-E.
- The remaining localized compat shims that V2 originally tolerated are now physically deleted.
- Card-play and top-of-draw effect resolution are queue-only as of `2026-04-03`.
- V2 now means both of these are true:
  - mainline call-sites are zero
  - old shim definitions are also zero

## Zero-Tolerance Rules

- No public Player timing or combat-event wrapper calls.
- No Player legacy timing/event helper definitions.
- No trait/power legacy `on_*` hook API in combat types.
- No enemy passive `hook`-driven runtime path.
- No old `EffectExecutor` API names in Python code.
- No old `EffectExecutor` API definitions in `EffectExecutor`.

## Mainline Rules

- New trait/power timing reactions must be window-native only.
- New trait/power event reactions must be event-native only.
- New enemy passives must declare `windows`; checked-in enemy JSON must not use `hook`.
- Card-play and top-of-draw mainline must stay queue-only.
- `reposition` must use an explicit enemy target in mainline; do not silently infer the pointer target when input is missing.
- New combat effect families must either:
  - plan into queue actions
  - return `[]` when they are intentionally a no-op under current conditions
  - or remain outside mainline until their queue contract is modeled
- Direct helper execution such as `execute_effect_payload_direct(...)` / `execute_effect_once_direct(...)` is test/tool-only unless we explicitly open a new runtime decision.
- Orchestrators, action executors, effect impls, preview/simulation helpers, and content-facing runtime code must not call removed old `EffectExecutor` names directly.

## Required Pre-Expansion Checks

Run these before merging a package that adds combat content or changes combat runtime ordering:

1. `python scripts/check_combat_compat_zero.py`
2. `python -m pytest tests/combat/test_combat_mainline_allowlist_v1.py -q`
3. `python -m pytest tests/combat -q`
4. `python -m pytest tests/simulation -q`

## Required Zero Values

- direct `player.start_turn(...)` usage = `0`
- direct `dispatch_turn_start_reactions(...)` usage = `0`
- direct `dispatch_combat_event_reactions(...)` usage = `0`
- Player legacy timing helper definitions/usages = `0`
- Player legacy event helper definitions/usages = `0`
- legacy trait/power `on_*` hook definitions in combat types = `0`
- enemy runtime passive compat seams in mainline = `0`
- checked-in enemy JSON `hook` usage = `0`
- old `EffectExecutor` API definitions in Python code = `0`
- old `EffectExecutor` API call-sites in Python code = `0`
- legacy fallback helper names in card-play/action-executor mainline = `0`
- queue-external fallback seams in card-play/action-executor mainline = `0`

## Regression Suite

The minimum gate suite for V2 is:

- [test_combat_mainline_allowlist_v1.py](/D:/PHD_SIMULATER/tests/combat/test_combat_mainline_allowlist_v1.py)
- [test_combat_timing_contract_v1.py](/D:/PHD_SIMULATER/tests/combat/test_combat_timing_contract_v1.py)
- [test_combat_event_contract_v1.py](/D:/PHD_SIMULATER/tests/combat/test_combat_event_contract_v1.py)
- [test_combat_reaction_dispatcher_v1.py](/D:/PHD_SIMULATER/tests/combat/test_combat_reaction_dispatcher_v1.py)
- [test_card_play_timing_contract_v1.py](/D:/PHD_SIMULATER/tests/combat/test_card_play_timing_contract_v1.py)
- [test_combat_mainline_smoke_pack_v1.py](/D:/PHD_SIMULATER/tests/combat/test_combat_mainline_smoke_pack_v1.py)
- `tests/combat`
- `tests/simulation`

## Remaining Runtime Inventory

Current queue-only ownership and any remaining direct-execution helpers outside mainline are tracked in:

- [COMBAT_FALLBACK_AND_SHIM_INVENTORY_V1.md](/D:/PHD_SIMULATER/docs/development/COMBAT_FALLBACK_AND_SHIM_INVENTORY_V1.md)

These are runtime migration items, not compatibility-owned seams.

## Next Promotion Bar

We should only claim a stricter post-V2 gate when all of the following are true:

- queue-external fallback-heavy seams have an explicit migration decision:
  - queue them
  - keep them intentionally outside mainline
  - or retire them
- preview/runtime/simulation parity remains stable through an expansion pass
- at least one additional expansion pass lands while the current zero-tolerance gate stays green
