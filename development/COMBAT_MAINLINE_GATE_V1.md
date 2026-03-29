# Combat Mainline Gate V1

> Superseded by [COMBAT_MAINLINE_GATE_V2.md](/D:/PHD_SIMULATER/docs/development/COMBAT_MAINLINE_GATE_V2.md).

## Historical Meaning

V1 was the first combat mainline gate after `COMBAT_TIMING_CONTRACT_V1` and `COMBAT_EVENT_CONTRACT_V1` landed.

It established these baseline rules:

- public Player compat wrappers must not regain mainline ownership
- trait/power legacy `on_*` hooks are not allowed in combat domain types
- enemy passive runtime must move to `windows` + dispatcher
- mainline fallback code must stop using old `EffectExecutor` names

## Historical Limits

V1 still tolerated a few localized shim definitions while forcing their call-sites to zero.

Those tolerated shims were fully deleted on `2026-03-30`, which is why V2 is now the only active gate.

## Use

- Read this file only as historical context.
- Use [COMBAT_MAINLINE_GATE_V2.md](/D:/PHD_SIMULATER/docs/development/COMBAT_MAINLINE_GATE_V2.md) for any active combat extension or cleanup work.
