### 战斗事件与服务化改造方案（草案）

本方案记录当前战斗域的服务化改造现状与后续基于事件总线的扩展路线，面向未来功能：
- 站位系统（我方）
- 场景系统（地图/环境特性）
- 多敌人系统（包含敌人特性与协同）

---

### 目标与原则
- 一致性：能量、费用、牌流、伤害等核心路径有“唯一合法入口”，可测试、可观测。
- 解耦与组合：改用战斗域内事件总线（同步、内存）连接“敌人/玩家/地图/队友/状态/被动”等，降低强耦合回调。
- 顺序可控：使用带优先级的事件分发（PriorityEventBus），确保地图→被动→日志等触发顺序可配置。
- 渐进落地：先服务化，再事件化；保证所有现有用例绿灯，逐步替换回退路径。

---

### 当前已完成（代码已落地）
- 服务化
  - DamageService：玩家与敌人伤害结算（统一格挡/伤害类型），玩家侧事件化闭环已建立。
  - EnergyService：统一能量消耗/增益；支持 X 费用消耗“全部当前能量”。
  - CostService：统一卡牌费用计算，保持现有 Power→Trait 的修改语义。
  - PileService：抽牌/放逐/置顶/弃置统一入口；`CardManager` 增加 `put_on_top`。
- 可靠性
  - Health Guard：受控上下文写入生命值；测试环境非法直写直接抛错，运行时记录 critical。
  - CI 架构检查：禁止在 `contexts/combat/domain/` 内（白名单除外）直接写 `health`；可扩展检查“堆内数组的直接写”。
- 测试
  - 全量 combat 测试绿灯（96 passed）。
  - 新增 DamageService 场景测试：HP_LOSS / NORMAL / PIERCING（含易伤倍率）。
  - 新增 EnergyService 场景测试：加能、负值、X 费、超额消费（抛错不改状态）。
  - 新增状态与事件测试：Vulnerable 叠层/到期、StatusApplied/StatusStacked/StatusEffectExpired。

注：Juggernaut/Combust 敌方伤害当前保留 `enemy.take_damage(...)` 路径以匹配既有测试期望与副作用顺序；后续可再事件化。

---

### 事件总线方案（CombatEventBus）
- 形态：与现有 PriorityEventBus 一致（同步、内存、按优先级分发）。
- 最小事件集（Phase 1）：
  - TurnStarted/TurnEnded（玩家/敌人）
  - CardPlayed / CardExhausted / Shuffled
  - EnergyWasSpent / ConfidenceWasUsed
  - PlayerTookDamage / EnemyTookDamage（玩家已闭环；敌人需要 commit 或总线消费）
  - StatusApplied / StatusStacked / StatusEffectExpired（已在统一状态系统中启用）

- 已接入的敌人事件（Phase 2）：
  - EnemyTurnStarted / EnemyTurnEnded
  - EnemySkillChosen / EnemySkillResolved（选择/结算时发布）
- 订阅优先级（建议从高到低）：
  - 地图/场景特性（全局调控）
  - 敌人/玩家的被动（Power/Trait/状态）
  - 视觉/日志/统计

---

### 与未来功能的对接
- 站位系统（我方）
  - 定义 `AllyPositionChanged`, `AllyEnteredFrontline`, `AllySwappedPosition` 等事件；
  - 牌和技能通过订阅这些事件修正目标选择、范围、伤害修正（例如“前排受伤+X%”）。
  - 在 DamageService 中读取“目标位置标签”（由位置服务产出）以应用额外倍率或豁免规则。

- 场景系统（地图/环境特性）
  - 作为高优先级订阅者，监听 `TurnStarted/Ended`, `DamageApplied`, `StatusApplied` 等事件，
    在分发早期修改上下文（如“本层易伤倍率+0.25”，“本层抽牌上限-1”）。
  - 不直接调用实体；利用事件修正与服务入口（Cost/Energy/Pile/Damage）交互。

- 多敌人系统（协同与被动）
  - 通过 `EnemyTookDamage`, `EnemySkillChosen/Resolved` 实现协同（如“某敌受伤→群体护盾”）。
  - 每个敌人用统一的订阅入口（实体内处理器），不要引入多个总线；事件仍在 CombatEventBus 内流转。

---

### 渐进路线图
- Phase 1（已完成大半）
  - 服务化：Damage/Energy/Cost/Pile ✅
  - 健康守卫与 CI 检查 ✅
  - 玩家伤害事件闭环 ✅
  - 文档与基础测试 ✅

- Phase 2（低风险接入）
  - 敌人事件最小接入：发布 EnemyTurnStarted/EnemyTookDamage；
  - 地图/队友作为订阅者，对上述事件做简单加成/减免；
  - 为关键事件链加顺序断言（CardPlayed → EnergyWasSpent → StatusApplied/Stacked → PlayerTookDamage/EnemyTookDamage）。

- Phase 3（扩展与收敛）
  - 统一状态系统（去重 Vulnerable），发布 StatusApplied/StatusStacked/StatusEffectExpired（已完成）；
  - 敌人技能事件化（SkillChosen/Resolved），
  - 收紧/移除遗留回退路径；CI 扩展“禁止直接堆内写”。

---

## 订阅优先级建议（由高到低）

1) 地图/场景修正（Map/Scene Modifiers）
   - 目标：全局倍率、抽牌上限、特殊回合规则
2) 状态/被动（Status/Powers/Traits）
   - 目标：对事件做按实体的修正/反应
3) 视觉/日志/统计（UI/Logging/Analytics）
   - 目标：记录事件轨迹与展示

说明：优先级通过 `PriorityEventBus.subscribe(event, handler, priority)` 可精细控制；数值越小优先级越高。

---

## 事件契约（核心字段）

- CardPlayed: `player_id, card_id, card_instance_id, target_id, x_cost_value`
- EnergyWasSpent: `amount`
- StatusApplied: `owner_id, effect_name, duration`
- StatusStacked: `owner_id, effect_name, new_duration`
- StatusEffectExpired: `owner_id, effect_name`
- PlayerTookDamage / EnemyTookDamage: `amount, source`
- EnemyTurnStarted / EnemyTurnEnded: `enemy_id, turn_number`
- EnemySkillChosen: `enemy_id, skill_name, cost`
- EnemySkillResolved: `enemy_id, skill_name, result`

---

## 示例：最小地图订阅者

示例实现：`contexts/combat/application/map_subscribers.py: SimpleMapModifier`

- 订阅 `EnemyTurnStarted`，在事件触发时对玩家（或敌人）施加 1 层 Vulnerable：
  - 使用统一状态系统 `StatusEffectManager.add_debuff(..., owner, event_bus)`
  - 不直接修改伤害；由 `DamageService.get_incoming_damage_multiplier` 统一读取生效

测试用例：`tests/combat/test_map_subscriber_minimal.py`

---

## 关键事件顺序断言（当前已覆盖）

- 普通链路：CardPlayed → EnergyWasSpent → StatusApplied/Stacked → PlayerTookDamage（或 EnemyTookDamage）
- X 费链路：CardPlayed → EnergyWasSpent（消耗全部当前能量）→ PlayerTookDamage
- 敌人链路一致性：`apply_damage_to_enemy` 事件之和 == `apply_damage_to_enemy_and_commit` 落地伤害

测试用例：`tests/combat/test_event_order_and_enemy_turn.py`

---

## CI/守卫（现状与建议）

- 现状
  - 禁止 combat/domain 直接写 `health`（仅 `entity.py` 白名单；`player_v2.py` 在 `health_write_context` 受控写入）
  - 禁止直接访问 `CardManager._cards`；禁止对 `hand/draw_pile/discard_pile/exhaust_pile` 直接调用 `append/pop/insert/remove/clear/extend`
  - 能量守卫：禁止直接 `.set_energy`/`.energy.add`/`.energy.spend`/`archetype.add_energy`/`archetype.spend_energy`（服务、原型、协议白名单）

- 建议补充（标准版目标）
  - 事件化路径的检测（可选）：在关键模块禁止绕过总线直接调用，或在审查脚本中提示“请发布 X 事件”
  - 日志结构：为事件添加 trace_id（或上下文堆栈ID）以串联一次动作全链路


---

### 统一入口一览（参考）
- 费用：`CostService.calculate_cost(player, card, active_powers, traits)`
- 能量：`EnergyService.spend_energy(...) / spend_x_cost(...) / add_energy(...)`
- 牌堆：`PileService.draw_cards(...) / exhaust_card_from_hand(...) / move_last_discarded_to_draw_top(...)`
- 伤害：`DamageService.apply_damage_to_player(...) / apply_damage_to_enemy(...)`
  - 注：敌方完全事件化前，可在服务中提供 `..._and_commit` 版本，以内部调用 `enemy.take_damage(...)`。

---

### 风险与对策
- 事件顺序回归风险：为关键序列增加顺序断言测试；使用优先级总线稳定分发顺序。
- 事件风暴：仅在“状态真实变化”处发事件；合并细粒度到阶段性事件（如 TurnStarted 内聚）。
- 性能：目前为同步内存分发，成本极低；如遇热点再优化（批量或采样日志）。

---

### 下一步建议与优先级（决策指引）

- 优先 1：事件总线最小化接入（推荐先做）
  - 做什么：为敌人接入最小事件（EnemyTurnStarted/EnemyTookDamage），补全关键事件链顺序断言测试；地图/场景作为高优先级订阅者先接入 1–2 个简单修正规则（如全局伤害倍率/抽牌上限）。
  - 收益：为“地图特点/站位系统/多敌协同”打通通道；对现有功能影响小、收益大。

- 优先 2：地图特点（在总线基础上展开）
  - 做什么：定义 2–3 个场景特性订阅 TurnStarted/PlayerTookDamage/StatusApplied，输出倍率与限制；提供开关与参数化配置。
  - 收益：可见的玩法增量；技术风险较低。

- 优先 3：站位系统（依赖总线与统一伤害入口）
  - 做什么：抽象“前/后排”标签与换位事件（AllySwappedPosition），在 DamageService 读取位置标签施加倍率；为少量卡/技能添加位置相关效果。
  - 收益：玩法空间大；实现量中等，建议在事件最小化接入后推进。

说明：若开发时长紧张，建议“事件总线最小化接入（含断言）→ 地图特点（1–2 个订阅）→ 站位系统基础骨架”。

---

### 里程碑与工时（粗略）
- 敌人最小事件接入与地图/队友订阅（Phase 2）：0.5–1 天（含测试）。
- 状态系统统一与技能事件化（Phase 3）：1–2 天（依赖内容量）。
- 清理回退路径与 CI 扩展：0.5 天。

如需变更优先级，建议优先“敌人事件最小接入 + 地图/队友订阅”，带来组合能力的核心收益。



### 达到 9/10 的落地计划（1 天内）

- Safe Hook 路由与日志（统一替代 try/except 吞错）
  - 做法：提供 `HookRouter.safe_invoke(hook_name, owner_id, ctx, fn, *args)` 或装饰器 `@safe_hook`，所有 Trait/Power 钩子统一经过路由。
  - 日志：默认 `logger.warning(..., exc_info=True, extra={hook, trait_or_power_id, card_id, enemy_id, turn_no})`；测试/开发环境抛错开关。
  - 验收：全量测试绿灯；搜索代码无 “except: pass” 钩子分发；新增 2 条“钩子异常不影响回合”的单测。

- 敌方伤害统一入口（不引入总线的低风险方案）
  - 做法：在 `DamageService` 增加 `apply_damage_to_enemy_and_commit(enemy, amount, type, source)`，内部委托 `enemy.take_damage(...)`，并返回语义事件以供上层日志/统计。
  - 改造：将调用处（例如效果、部分 Power/Trait）经由该方法；`Juggernaut/Combust` 可先维持 `enemy.take_damage(...)`，逐步替换为 commit 版本以统一入口。
  - 验收：全量测试绿灯；`grep` 无“对敌伤害”的分流逻辑（仅走统一入口或 `take_damage`）。

- 状态系统先期收敛（Vulnerable 单一来源）
  - 做法：保留一套 `Vulnerable`（建议 `buff_system.Vulnerable`），删除/迁移重复实现；在 `DamageService` 明确倍率读取点。
  - 验收：易伤测试通过（玩家/敌人均 x1.5），`grep` 无第二套 Vulnerable 被使用。

- 牌堆服务覆盖与 CI 规则补齐
  - 做法：补充 `PileService` 在个别效果/流程中的使用；为 CI 增加规则：禁止 `CardManager._cards` 直接写（如 `insert/extend` 等），推荐 `put_on_top/move_all_to` 等 API。
  - 验收：全量通过；`validate_architecture.py` 新增检查项通过；`grep` 无直接 `_cards` 写入。

- 事件顺序断言测试（关键序列）
  - 做法：新增 3–4 条断言：`CardPlayed → EnergyWasSpent → StatusApplied → PlayerTookDamage`；X 费卡牌与普通卡各 1 条；带 Vulnerable 的伤害 1 条。
  - 验收：断言通过且稳定（RNG seed 固定）。

完成上述 5 项后，综合健康度预期可从 8.2/10 提升至 9+/10。
