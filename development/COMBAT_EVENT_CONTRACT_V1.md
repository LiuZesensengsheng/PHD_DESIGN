# Combat Event Contract V1

## 目标

把战斗中的事实事件从 `Player` 内部 raw loops 收口到 combat-side dispatcher，
让事件反应和 timing windows 一样，拥有显式的主线 owner 与稳定顺序。

这份契约只覆盖战斗事实事件，不覆盖：

- 外层 `CombatPhaseMachine`
- 药水、地图、奖励
- 战斗外 UI 流程

## 当前事件范围

V1 主线把以下事件视为 combat fact events：

- `CardDrawn`
- `CardExhausted`
- `Shuffled`
- `PlayerTookDamage`
- `EnemyTookDamage`
- `ConfidenceChanged`
- `ConfidenceWasUsed`
- `EnergyWasSpent`
- `StatusApplied`
- `StatusStacked`
- `StatusEffectExpired`
- `StressThresholdReached`
- `StressIncreased`
- `OffColorCardPlayed`
- `JudgmentResolved`

## 运行时归属

- 新主线 owner 是 `CombatEventDispatcher`
- `Player` 仍保留 event bus 订阅，但只负责：
  - 必要的本地状态更新
  - 向 `CombatEventDispatcher` 转发
  - 在没有 dispatcher 的窄兼容场景下回退到 legacy loop

这意味着：

- `Player._run_legacy_combat_event_reactions(...)` 不再是主线路径
- 事件排序权不再由 `Player` 内部列表循环决定

## 默认顺序

事件反应顺序沿用与 timing windows 一致的 owner-first 规则：

### 玩家拥有事件

1. arena / encounter effects
2. player traits
3. player powers
4. enemy passives

### 敌方拥有事件

1. arena / encounter effects
2. enemy passives
3. player traits
4. player powers

### 默认 owner 判断

- `EnemyTookDamage` 归敌方
- 大多数玩家侧资源/抽牌/受伤事件归玩家
- `Status*` 事件按 `owner_id` 判定归属
- 无法识别时默认归玩家

## 接入面

V1 主线默认使用 event-native 接口：

- `supported_event_types`
- `supports_combat_event(...)`
- `react_to_combat_event(...)`

legacy 事件钩子仍可在无 dispatcher 的兼容路径下工作，但不再作为新增内容的主接口。

## 测试锚点

V1 至少锁住以下事实：

- 玩家拥有事件顺序为 `traits -> powers`
- 敌方拥有事件顺序为 `enemy passives -> player traits -> player powers`
- runtime publish 出来的 `Shuffled / CardExhausted / StatusApplied` 等事件会进入 dispatcher 主线
- 主线运行时不依赖 `Player._run_legacy_combat_event_reactions(...)`

## 与 COMBAT_TIMING_CONTRACT_V1 的关系

- timing windows 负责“阶段窗口”
- combat events 负责“事实广播”
- 两者共享相同的 owner-first 心智模型
- 两者都不依赖 shared event bus priority 作为战斗真相
