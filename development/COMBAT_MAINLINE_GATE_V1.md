# Combat Mainline Gate V1

## 目标

在 `COMBAT_TIMING_CONTRACT_V1` 和 `COMBAT_EVENT_CONTRACT_V1` 已落地之后，
把 legacy 接口压缩成受控兼容壳，避免后续扩卡时重新长出隐式主线。

## Compat-only seams

以下入口允许继续存在，但视为兼容层，不再是主线语义锚点：

- `Player.start_turn()`
- `Player.dispatch_turn_start_reactions(...)`
- `Player.dispatch_combat_event_reactions(...)`
- `Player._dispatch_combat_event_reactions(...)`
- `Player._run_legacy_turn_start_reactions(...)`
- `Player._run_legacy_combat_event_reactions(...)`

## 新内容接入规则

- 新 trait / power 的 timing 反应默认只能走 window-native 接口
- 新 trait / power 的事件反应默认只能走 event-native 接口
- 不允许为新内容新增自定义：
  - `on_card_drawn`
  - `on_card_exhausted`
  - `on_confidence_changed`
  - `on_player_took_damage`
  - `on_shuffled`
- 上述 legacy event hook 只允许留在：
  - protocol
  - base compat type
  - `EventMappedTrait` / `EventMappedPower`

## 门禁测试

V1 默认门禁至少包括：

- direct `player.start_turn(...)` usage allowlist
- direct `dispatch_turn_start_reactions(...)` usage allowlist
- direct `dispatch_combat_event_reactions(...)` usage allowlist
- legacy timing hook definition allowlist
- legacy event hook definition allowlist

## 默认推进方向

- 能迁到 window-native / event-native 的内容，优先迁
- compat seam 允许保留，但只作为迁移期壳
- 之后的 preview / simulation parity 工作，必须建立在这些门禁持续为绿的前提上
