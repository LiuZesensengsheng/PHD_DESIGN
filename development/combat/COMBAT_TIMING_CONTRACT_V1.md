# Combat Timing Contract V1

## 目标

定义一份明确的战斗时序契约，使其同时满足：

- 在心智模型上接近《杀戮尖塔》式卡牌战斗
- 足以支撑 `300+` 卡牌、`100+` 特质、以及大量敌方被动
- 足够清晰，让卡牌设计者不必记忆隐藏的代码顺序

这份文档是：

- 一份时序契约
- 一份后续实现迁移的目标

它不是一份完整的引擎重写计划。

## 为什么需要这份文档

当前战斗代码已经有一条可用主链路：

- 出牌经过 transaction
- `CardPlayed` 进入统一的 orchestrator 结算主线
- 许多主动效果已经走 planner / queue
- 回合开始与回合结束已经有较稳定的执行顺序

但现在的时序仍然有相当一部分是隐性的：

- 一些 hook 在 `Player`
- 一些 hook 在 `CombatModel`
- 一些是 event bus 回调
- 一些是 queue follow-up
- 一些敌方被动仍然是 bespoke 特例

这会让三件事越来越困难：

1. 添加新的 trait / power / enemy passive 反应
2. 判断特殊效果是否真正能组合
3. 保持 preview、真实执行、simulation 三者一致

V1 的目标，就是为这些行为定义一套统一的时序词汇。

## 范围

V1 覆盖：

- 战斗开始
- 玩家回合
- 出牌
- 回合结束
- 敌方回合
- 战斗结束
- 以下反应源的统一顺序：
  - 玩家 traits
  - 玩家 powers
  - 敌方 passives
  - arena / encounter effects

V1 不要求：

- 先实现药水系统
- 先把术语全部改成 relic 风格
- 先重写外层 UI phase machine
- 立刻删除所有 legacy effect 实现

## 外层阶段模型

外层阶段模型保持有意的简洁：

- `PLAYER_TURN`
- `ENEMY_TURN`
- `COMBAT_END`

现有 `CombatPhaseMachine` 仍然可以大体保持这种粗颗粒度。

真正的改进重点在每个外层阶段的内部：

- 明确内部 timing windows
- 明确每个窗口允许什么修改
- 明确 reaction order

## 时序词汇

### 1. 战斗开始

- `COMBAT_SETUP`
  - 构建 player、enemies、encounter payload
  - 固定 RNG seed
  - 挂载持久化传入的战斗启动数据
- `COMBAT_START_PRE`
  - 初始化战斗开始时就存在的系统
  - 注册 arena / encounter effects
  - 注册带入战斗的玩家构筑状态
- `COMBAT_START_REACTIONS`
  - 触发“战斗开始时”反应
- `OPENING_HAND_SETUP`
  - 洗牌
  - 处理 innate
  - 抽起手牌
- `FIRST_PLAYER_TURN_ENTER`
  - 进入首个玩家回合

### 2. 玩家回合

- `TURN_START_RESET`
  - 增加 turn number
  - 重置本回合计数器与本回合上下文
  - 清理上一回合残留的一次性标记
- `TURN_START_BLOCK_DECAY`
  - 处理玩家侧临时防御值衰减
  - V1 目标是更接近 StS：
    - 玩家 block 穿过敌方回合
    - 在玩家自己的下个回合开始时再衰减
- `TURN_START_PRE_DRAW`
  - 执行必须发生在抽牌前的回合开始反应
  - 典型用途：
    - 补充能量
    - 重置 pointer / queue 限制
    - 重置 once-per-turn 计数
    - 注入“默认属于本回合开始配置”的临时环境牌
- `TURN_START_DRAW`
  - 执行正常的回合开始抽牌 / 补牌
- `TURN_START_POST_DRAW`
  - 执行依赖“新手牌状态”的反应
  - 仅当某些机制明确要作为“不占正常抽牌数的额外赠牌”时，才默认在这里注入临时牌
- `ACTION_WINDOW`
  - 玩家可以出牌、结束回合，或未来使用战斗侧工具能力

### 3. 出牌

- `PLAY_ATTEMPT`
  - 校验是否可出
  - 锁定当前 source card / target / x-cost 上下文
- `PLAY_COST_FINALIZE`
  - 在所有 cost modifier 作用后，确定真实费用
- `PLAY_COMMIT`
  - 支付能量并提交这次出牌
  - 从这里开始，这张牌被视为“已打出”
- `ON_CARD_PLAYED`
  - 触发“当你打出一张牌时”反应
  - 这是一个 reaction window，不等于牌本身已经结算完
- `BEFORE_CARD_RESOLUTION`
  - 固定本次卡牌结算的瞬时修正
- `BEFORE_EFFECT`
  - 每个单独 effect 执行前的窗口
- `EFFECT_RESOLUTION`
  - 通过 planner/queue 或 legacy fallback 执行一个 effect
- `AFTER_EFFECT`
  - 处理由这个 effect 触发的 follow-up reactions
- 对卡上的每个 effect 重复：
  - `BEFORE_EFFECT -> EFFECT_RESOLUTION -> AFTER_EFFECT`
- `AFTER_CARD_RESOLVED`
  - 当整张牌的所有 effects 执行完成后，触发卡级别的后处理反应
- `POWER_ATTACH`
  - 如果这是一张 Power 牌，在这里附着其持久被动
- `CARD_ROUTE`
  - 弃牌 / 消耗 / 移入 power area
- `AFTER_CARD_ROUTED`
  - 卡牌离开手牌归属后的最终清理窗口

### 4. 玩家回合结束

- `TURN_END_PRE`
  - 不再允许开启新的 action
  - 清空 / 收尾任何待处理 reaction queue
- `HAND_CLEANUP`
  - 按规则弃掉或消耗手牌中剩余卡牌
- `TURN_END_REACTIONS`
  - 执行回合结束时反应
- `TURN_END_POST`
  - 清理临时费用覆盖与回合结束瞬时状态
- 转入敌方回合

### 5. 敌方回合

- `ENEMY_TURN_START`
  - 执行全局敌方回合开始反应
  - 处理敌方侧临时防御值衰减
  - 处理 chore / countdown tick
  - V1 目标是更接近 StS：
    - 敌方 block 穿过玩家回合
    - 在敌方自己的回合开始时再衰减
- 对每个敌人：
  - `ENEMY_START`
  - `ENEMY_ACTION`
  - `ENEMY_END`
- `ENEMY_TURN_END`
  - 执行全局敌方回合结束反应
  - prune defeated enemies
  - 执行 combat end check
- 转回玩家回合

### 6. 战斗结束

- `COMBAT_END_CHECK`
  - 每次可能结束战斗的重要状态变化之后执行
- `COMBAT_END_RESOLVE`
  - 标记胜负
  - 冻结后续战斗 action
- `COMBAT_END_CLEANUP`
  - 仅执行 battle-scoped cleanup

## 反应顺序

V1 不再采用“enemy passives 永远先于玩家侧”的全局规则。

V1 改为更接近 StS 心智模型的窗口归属规则：

- 谁拥有这个窗口，谁优先反应
- 对方反应在拥有方之后
- arena / encounter effects 只在明确绑定该窗口时抢在双方之前

### 先判断窗口归属

#### 玩家拥有的窗口

- `TURN_START_*`
- `ACTION_WINDOW`
- `PLAY_*`
- `ON_CARD_PLAYED`
- `BEFORE_CARD_RESOLUTION`
- `BEFORE_EFFECT`
- `AFTER_EFFECT`
- `AFTER_CARD_RESOLVED`
- `POWER_ATTACH`
- `CARD_ROUTE`
- `AFTER_CARD_ROUTED`
- `TURN_END_*`

#### 敌方拥有的窗口

- `ENEMY_TURN_START`
- `ENEMY_START`
- `ENEMY_ACTION`
- `ENEMY_END`
- `ENEMY_TURN_END`

#### 全局窗口

- `COMBAT_START_*`
- `COMBAT_END_*`

### 默认组顺序

在同一个 timing window 内，先按以下大组顺序运行：

1. arena / encounter effects
2. 拥有方 reactions
3. 对方 reactions
4. 该窗口产出的 deferred follow-up actions

### 各类窗口的默认展开顺序

#### 玩家拥有窗口

1. arena / encounter effects
2. player traits
3. player powers
4. enemy passives
5. deferred follow-up actions

#### 敌方拥有窗口

1. arena / encounter effects
2. enemy passives
3. player traits
4. player powers
5. deferred follow-up actions

#### 全局窗口

默认使用：

1. arena / encounter effects
2. player traits
3. player powers
4. enemy passives
5. deferred follow-up actions

若某个全局窗口需要特殊优先级，应由该窗口单独声明，而不是靠订阅顺序隐式决定。

### 重要规则

插入顺序不是契约的一部分。

这条契约必须由显式 priority 驱动，而不能依赖：

- subscribe 先后顺序
- list append 顺序
- 谁先被构造出来

### 组内优先级

每个 group 内部，后续实现应支持：

- `priority`
  - 数字越小越先执行
- `stable_tiebreak`
  - 稳定的二级排序，例如 source id

V1 期望每个 reaction source 最终都能暴露：

- source id
- source group
- priority
- supported windows

## 各窗口的修改规则

这一节是整份契约里最重要的部分。

### `TURN_START_RESET`

允许：

- 重置计数器
- 清理上一回合临时标记

不允许：

- 抽牌
- 直接造成伤害
- 永久修改牌组内容

### `TURN_START_BLOCK_DECAY`

允许：

- 清空或衰减玩家本轮不应继续保留的临时防御值

契约规则：

- 这一窗口是玩家 block 的默认衰减点
- 不再把玩家 block 设计为“在玩家按 End Turn 时立即清空”
- 玩家 block 必须穿过整个敌方回合
- `TURN_END_PRE`、`HAND_CLEANUP`、`TURN_END_REACTIONS`、`TURN_END_POST` 默认都不得清空玩家 block
- 只有明确声明“保留 block”或“跳过本次 block decay”的效果，才能例外覆盖这次衰减

这条规则是 V1 向 StS 靠拢的核心之一。

### `TURN_START_PRE_DRAW`

允许：

- 补充能量
- 刷新 once-per-turn 上限
- 执行回合开始时 buff / passive 更新
- 注入默认属于“回合开始配置”的临时环境牌

不允许：

- 处理打出卡牌后的 route
- 反向修改上一回合结算结果

### `TURN_START_DRAW`

允许：

- 执行正常抽牌
- 触发 on-draw reactions

不允许：

- 手动做 combat-end routing

### `TURN_START_POST_DRAW`

允许：

- 执行依赖新手牌状态的 reactions
- 注入明确标注为“额外赠牌、且不占正常抽牌数”的临时卡

契约规则：

- 如果某张环境牌本质上是“系统每回合发给你的标准配置牌”，默认应在 `TURN_START_PRE_DRAW`
- 如果某张环境牌本质上是“额外奖励牌”，默认应在 `TURN_START_POST_DRAW`

### `ON_CARD_PLAYED`

语义：

- 这张牌已经提交并支付
- 但它自己的 active effects 还没有全部执行完成

允许：

- 增加计数器
- 为当前卡打标记 / 追加本次结算修正
- 产生 follow-up actions

不允许：

- route 这张已打出的牌
- 假设它所有效果都已经执行完成

### `BEFORE_EFFECT`

允许：

- 固定 effect-local modifiers
- 如有需要，锁定 target snapshot

不允许：

- 消耗未来 effect 的状态

### `AFTER_EFFECT`

允许：

- 处理这个 effect 触发出的 reactions
- enqueue follow-up actions
- 如果这个 effect 可能击杀，则做 combat end check

### `AFTER_CARD_RESOLVED`

语义：

- 卡牌上的所有 active effects 都已执行完成
- 但卡牌本身还可能没有完成 route

允许：

- 一次性的“这张牌结算后”反应
- 卡级别计数器的最终落账

### `POWER_ATTACH`

语义：

- 这张刚打出的 Power 牌，从这里开始成为持久被动来源

契约规则：

- 新附着的 power 不参与它自己这张牌的：
  - `PLAY_COST_FINALIZE`
  - `ON_CARD_PLAYED`
  - `BEFORE_EFFECT`
  - 当前卡结算过程

这样可以消除一大类“自己 retroactively 影响自己”的歧义。

### `CARD_ROUTE`

允许：

- 将卡移入 discard / exhaust / power area
- 发布 routed-card 事件

契约规则：

- route decision 必须读取一套共享的 force-exhaust contract
- traits 与 powers 不能在“谁能强制改 route”这个问题上各走各的

### `TURN_END_REACTIONS`

允许：

- end-of-turn traits / powers
- 计划好的清理型 reaction

契约规则：

- `TURN_END_REACTIONS` 不负责 block decay
- block decay 已经移动到拥有者自己的下个回合开始窗口

### `ENEMY_TURN_START`

允许：

- 执行敌方回合开始 reactions
- 清空或衰减敌方不应继续保留的临时防御值
- 处理 chore / countdown

契约规则：

- 这一窗口是敌方 block 的默认衰减点
- 不再默认让敌方 block 在玩家回合结束时直接消失
- 敌方 block 必须穿过整个玩家回合
- 玩家侧回合结束相关窗口默认不得清空敌方 block
- 只有明确声明“保留 block”或“跳过本次 block decay”的效果，才能例外覆盖这次衰减

## Traits、Powers、Enemy Passives 的统一契约

### Traits

Traits 是更像 relic 的玩家持久构筑层。

Traits 可以反应在任意支持的 timing window 上，但应优先用于：

- combat start
- turn start
- card played
- effect resolution modifiers
- turn end

Traits 不应依赖裸 insertion order。

### Powers

Powers 是 battle-local 的持久效果层。

Powers 可以反应在与 traits 相同的窗口上，但在 V1 中默认排在 traits 之后。

由刚打出的 Power 牌产生的新 power，会在 `POWER_ATTACH` 才正式生效。

### Enemy Passives

Enemy passives 在 V1 中应被视为 first-class reaction source，而不是特例。

它们应能接入相同的 timing vocabulary，例如：

- combat start
- enemy turn start / end
- player card played
- player damage taken
- enemy damaged

V1 不要求它们立刻拥有完全相同的类层级。

但 V1 要求它们进入同一套 timing windows。

## Queue / Planner / Legacy Effects 的契约

V1 继续保留 action queue 作为主动效果的优先 sequencing substrate。

规则：

- planner 已支持的 effect，以 planned actions 为准
- legacy direct effect execution 在迁移期仍允许存在
- planned path 和 legacy path 都必须遵守同一套 timing windows

这意味着：

- legacy effect 不允许悄悄跳过 `BEFORE_EFFECT` / `AFTER_EFFECT`
- planner path 也不允许发明一套与 legacy 完全不同的时序语义

## Preview 契约

Preview 与 execution 应共享同一套卡级别时序假设：

- cost preview 参考 `PLAY_COST_FINALIZE`
- effect preview 参考 `BEFORE_EFFECT` modifiers
- preview 不默认包含 `AFTER_EFFECT` side effect，除非该效果被明确标记

V1 不要求所有特殊效果都做到完美 preview。

但 V1 要求：

- “简单 planned effect”
- “简单 executed effect”

这两类至少要共享同一套 modifier order。

## 与当前运行时的对应关系

这一节用于把当前运行时映射到目标契约。

### 已经比较接近的部分

- 外层 phase 已存在：
  - `PLAYER_TURN`
  - `ENEMY_TURN`
- 出牌已经有 transaction 边界
- 卡牌效果已经进入统一 orchestrated mainline
- 敌方回合已经有稳定 step sequence

### 仍未正式化的部分

- `on_turn_start` / `on_turn_end` 顺序仍分散在 model 与 player
- `on_card_played` 的语义尚未正式文档化
- power attach timing 目前仍是隐式规则
- enemy passives 还没进入同一 reaction substrate
- event-bus priority 还不是当前真实权威
- block decay 时机仍未按“拥有者下个回合开始”正式收口

## V1 非目标

V1 不尝试：

- 先加药水
- 先重做战斗外层 UI
- 一次性删光所有 legacy effect classes
- 一次性定义完所有未来 keyword mechanics
- 强行把项目改成完全照搬 StS

## 推荐迁移顺序

1. 先补测试，把以下窗口锁住：
   - turn start
   - card play
   - power attach
   - turn end
   - block decay ownership
2. 引入一套内部 timing enum / window vocabulary
3. 让 trait / power / enemy-passive reactions 经过同一个 shared dispatcher
4. 让 queue path 与 legacy path 发出相同的 timing hooks
5. 修正 route-card 语义，使 traits 与 powers 共享同一套 routing contract
6. 把 block decay 从“当前回合结束”正式迁移到“拥有者下个回合开始”

## 待评审问题

在进入实现前，最值得评审的是这 5 个点：

1. 临时环境牌默认应放在 `TURN_START_PRE_DRAW`，还是保留 `TURN_START_POST_DRAW` 作为“不占正常抽牌数”的赠牌窗口？
2. `BLOCK_DECAY` 是否确认改为“在拥有者的下个回合开始时衰减”，而不是“在当前回合结束时衰减”？
3. 玩家侧默认顺序用 `traits -> powers` 是否合适？
4. reaction ordering 是否确认采用“谁拥有窗口谁优先”的规则，而不是“enemy passives 永远先于玩家侧”？
5. `POWER_ATTACH` 放在 `AFTER_CARD_RESOLVED` 之后，是否符合本项目想要的手感？

## V1 默认答案

如果评审没有否决，V1 默认采用：

- 环境牌注入：
  - 默认 `TURN_START_PRE_DRAW`
  - 若设计目标明确是“额外赠牌且不占正常抽牌”，则例外放在 `TURN_START_POST_DRAW`
- block decay：
  - 改为“在拥有者的下个回合开始时衰减”
  - 玩家 block 在 `TURN_START_BLOCK_DECAY`
  - 敌方 block 在 `ENEMY_TURN_START`
  - 默认不存在“回合结束自动清 block”
  - 只有显式保留类效果可以覆盖这次衰减
- 玩家侧顺序：`traits -> powers`
- reaction ordering：
  - 默认采用“谁拥有窗口谁优先”
  - 玩家窗口中玩家侧优先
  - 敌方窗口中敌方侧优先
- power attach：在 card resolution 完成后、route finalization 前生效
