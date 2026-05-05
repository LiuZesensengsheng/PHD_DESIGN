# Combat Compat-Zero Plan V1

## Status

- Plan created to drive Phase A-E of the combat compat-zero cleanup
- Main implementation phases landed on `2026-03-29`
- Remaining localized shims were hard-deleted on `2026-03-30`
- Queue-only follow-up for card-play/top-card mainline landed on `2026-04-03`
- This plan is now completed for its original scope

## Original Goal

Push combat runtime from "thin compat shell" to "compat-zero mainline" so future combat content only sees:

- window-native timing reactions
- event-native combat fact reactions
- `windows`-native enemy passives
- neutral fallback APIs

## What Was Completed

### Phase A

- removed Player public compat wrappers from runtime mainline
- locked timing dispatch behind orchestrator + dispatcher ownership

### Phase B

- removed trait/power legacy `on_*` hook API from combat domain types
- added zero-tolerance tests so those hooks cannot be reintroduced silently

### Phase C

- moved enemy passive runtime to `windows` + dispatcher
- removed runtime `hook` ownership and migrated checked-in enemy JSON

### Phase D

- replaced old `EffectExecutor` mainline names with:
  - `execute_card_fallback(...)`
  - `execute_effect_payload(...)`
  - `execute_effect_once(...)`
- later queue-only follow-up work renamed the surviving direct helpers to explicit test/tool-only names:
  - `execute_effect_payload_direct(...)`
  - `execute_effect_once_direct(...)`

### Phase E

- promoted the active gate to [COMBAT_MAINLINE_GATE_V2.md](/D:/PHD_SIMULATER/docs/development/combat/COMBAT_MAINLINE_GATE_V2.md)
- added `scripts/check_combat_compat_zero.py`
- established the runtime fallback inventory document

### Post-Plan Hard Delete

- deleted Player failure stubs
- deleted old-name `EffectExecutor` wrappers
- tightened the precheck and allowlist tests from "isolated" to "zero"

## How We Enforce "Do Not Reintroduce"

The "forbid new compat seam" rule is maintained by tests and precheck, not by convention only:

1. `python scripts/check_combat_compat_zero.py`
2. `python -m pytest tests/combat/test_combat_mainline_allowlist_v1.py -q`
3. `python -m pytest tests/combat -q`
4. `python -m pytest tests/simulation -q`

## Remaining Work After Compat-Zero

The next cleanup work is no longer about compatibility shims. The card-play/top-card fallback seams are already removed from mainline, so future work is about deeper StS-style runtime evolution:

- keep direct execution helpers out of combat mainline unless a new explicit decision says otherwise
- improve preview/runtime/simulation parity on harder content
- keep expanding on top of the timing/event/window mainline only
