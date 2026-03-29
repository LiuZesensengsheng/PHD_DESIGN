# Combat Mainline Gate V1

> Superseded by [COMBAT_MAINLINE_GATE_V2.md](/D:/PHD_SIMULATER/docs/development/COMBAT_MAINLINE_GATE_V2.md) for active extension gating.

## 目标

在 `COMBAT_TIMING_CONTRACT_V1` 和 `COMBAT_EVENT_CONTRACT_V1` 已落地之后，
把 legacy 接口压缩成受控兼容壳，避免后续扩卡时重新长出隐式主线。

## Compat-only seams

当前只允许以下私有 legacy helper 继续存在，且仅作为迁移期占位：

- `Player._run_legacy_turn_start_reactions(...)`
- `Player._run_legacy_combat_event_reactions(...)`

以下 public compat 入口已从主线移除，不允许恢复：

- `Player.start_turn()`
- `Player.dispatch_turn_start_reactions(...)`
- `Player.dispatch_combat_event_reactions(...)`

Enemy passive runtime 已收口为 dispatcher-owned 主线，不允许恢复以下 compat seam：

- `Enemy.on_spawn()`
- `Enemy.start_turn(..., run_passives=...)`
- `Enemy.end_turn(..., run_passives=...)`
- `Enemy._run_compat_passives_for_window(...)`
- `Enemy._execute_passives(...)`

EffectExecutor 主线入口已收口为 neutral fallback API，不允许主线重新依赖以下旧名：

- `EffectExecutor.execute_legacy_card_fallback(...)`
- `EffectExecutor.execute_card_effects(...)`
- `EffectExecutor.execute_legacy_effect_data_fallback(...)`
- `EffectExecutor.execute_effect_data(...)`
- `EffectExecutor.execute_legacy_effect_fallback(...)`
- `EffectExecutor.execute_effect(...)`

当前主线 fallback 入口固定为：

- `EffectExecutor.execute_card_fallback(...)`
- `EffectExecutor.execute_effect_payload(...)`
- `EffectExecutor.execute_effect_once(...)`

## 新内容接入规则

- 新 trait / power 的 timing 反应默认只能走 window-native 接口
- 新 trait / power 的事件反应默认只能走 event-native 接口
- 新 enemy passive 的 runtime 反应默认只能走 `windows` 声明 + dispatcher 排序
- 新 enemy JSON 不允许再写 `hook`；checked-in 数据必须显式声明 `windows`
- 新的 effect fallback 主线只允许接入 neutral API，不允许再从 orchestrator / action executor / effect impl 直接调用旧名
- `contexts/combat/domain/traits.py` 与 `contexts/combat/domain/powers.py` 中的 legacy `on_*` hook 已移除，不允许恢复：
  - `on_turn_start`
  - `on_turn_end`
  - `on_card_played`
  - `on_card_drawn`
  - `on_card_exhausted`
  - `on_confidence_changed`
  - `on_player_took_damage`
  - `on_shuffled`

## 门禁测试

V1 默认门禁至少包括：

- direct `player.start_turn(...)` usage allowlist
- direct `dispatch_turn_start_reactions(...)` usage allowlist
- direct `dispatch_combat_event_reactions(...)` usage allowlist
- legacy timing hook definition zero-check for trait/power types
- legacy event hook definition zero-check for trait/power types
- enemy passive compat seam zero-check
- checked-in enemy JSON `hook` zero-check
- old EffectExecutor API call-site zero-check
- orchestrator legacy fallback helper-name zero-check

当前目标值：

- direct `player.start_turn(...)` usage = `0`
- direct `dispatch_turn_start_reactions(...)` usage = `0`
- direct `dispatch_combat_event_reactions(...)` usage = `0`
- enemy runtime passive compat seams = `0`
- checked-in enemy JSON `hook` usage = `0`
- old EffectExecutor API calls in Python code = `0`
- card-play / action-executor legacy fallback helper names = `0`

## 默认推进方向

- 能迁到 window-native / event-native 的内容，优先迁
- 剩余 compat seam 只允许留在明确的迁移计划里，不能重新长回 runtime 主线
- 之后的 preview / simulation parity 工作，必须建立在这些门禁持续为绿的前提上
