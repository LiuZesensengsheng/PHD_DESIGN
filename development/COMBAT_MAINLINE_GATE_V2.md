# Combat Mainline Gate V2

## Status

- Active gate as of `2026-03-29`
- Scope remains combat runtime semantics only
- Supersedes `COMBAT_MAINLINE_GATE_V1.md` as the active extension gate
- `COMBAT_TIMING_CONTRACT_V1` and `COMBAT_EVENT_CONTRACT_V1` remain the semantic source of truth

## What V2 Means

- Combat mainline call-sites are now compat-zero for the core seams we targeted in Phase A-D:
  - no public Player timing/event wrapper calls
  - no trait/power legacy `on_*` hook API in combat types
  - no enemy passive `hook`-driven runtime path
  - no old `EffectExecutor` API names in orchestrator/mainline call-sites
- V2 does **not** mean every local compatibility shim has been physically deleted.
- V2 means those remaining shims are isolated, non-mainline, and guarded by zero-tolerance checks on call-sites.

## Allowed Localized Shims

The following compatibility shims may still exist locally, but they are not allowed to regain mainline ownership:

- [player.py](/D:/PHD_SIMULATER/contexts/combat/domain/player.py)
  - `_run_legacy_turn_start_reactions(...)`
  - `_run_legacy_combat_event_reactions(...)`
  - both are failure stubs only
- [executor.py](/D:/PHD_SIMULATER/contexts/combat/domain/effects/executor.py)
  - `execute_legacy_card_fallback(...)`
  - `execute_card_effects(...)`
  - `execute_legacy_effect_data_fallback(...)`
  - `execute_effect_data(...)`
  - `execute_legacy_effect_fallback(...)`
  - `execute_effect(...)`
  - all are compat wrappers only; active mainline uses neutral fallback names

## Mainline Rules

- New trait/power timing reactions must be window-native only.
- New trait/power event reactions must be event-native only.
- New enemy passives must declare `windows`; checked-in enemy JSON must not use `hook`.
- New fallback execution code must use:
  - `execute_card_fallback(...)`
  - `execute_effect_payload(...)`
  - `execute_effect_once(...)`
- Orchestrators, action executors, effect impls, preview/simulation helpers, and content-facing runtime code must not call old `EffectExecutor` names directly.

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
- legacy trait/power `on_*` hook definitions in combat types = `0`
- enemy runtime passive compat seams in mainline = `0`
- checked-in enemy JSON `hook` usage = `0`
- old `EffectExecutor` API call-sites in Python code = `0`
- legacy fallback helper names in card-play/action-executor mainline = `0`

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

The remaining non-queue or queue-external fallback-heavy seams are tracked in:

- [COMBAT_FALLBACK_AND_SHIM_INVENTORY_V1.md](/D:/PHD_SIMULATER/docs/development/COMBAT_FALLBACK_AND_SHIM_INVENTORY_V1.md)

These are not treated as compat ownership regressions as long as they continue to use the neutral fallback API and keep parity tests green.

## Next Promotion Bar

We should only claim a stricter post-V2 gate when all of the following are true:

- Player failure stubs can be hard-deleted without breaking tests or tooling.
- Old `EffectExecutor` wrapper names can be hard-deleted without reintroducing call-site debt.
- Remaining queue-external fallback-heavy seams have an explicit migration decision:
  - queue them
  - keep them intentionally
  - or retire them
- At least one additional expansion pass lands while V2 remains green.
