### 场景玩法模板对齐（单一规则引擎的两个示例）

本文件将内容设计与当前技术实现对齐，形成可落地的“流程蓝本”。注意：这不是“两套战斗系统”，而是“同一套规则引擎”下的两种场景玩法示例，用于验证与对齐需求。

---

## 共同基础（已在代码中具备）

- 统一入口与服务：
  - 能量：`EnergyService.spend_energy / spend_x_cost / add_energy`
  - 费用：`CostService.calculate_cost`
  - 牌堆：`PileService.draw_cards_with_shuffle / ...`
  - 伤害：`DamageService.apply_damage_to_player / apply_damage_to_enemy_and_commit`
- 状态系统：`StatusEffectManager` + `StatusApplied/StatusStacked/StatusEffectExpired`
- 事件总线（最小接入）：
  - 玩家：`CardPlayed / EnergyWasSpent / PlayerTookDamage / CardExhausted / Shuffled`
  - 敌人：`EnemyTurnStarted / EnemyTurnEnded / EnemySkillChosen / EnemySkillResolved`
  - 地图订阅者示例：`SimpleMapModifier`（可扩展为多规则版）

---

## 示例A：临时工的合同（盟友 + 位置交换）

要点：引入一个“友方召唤单位（代码佣兵）”，其生命值=预算；支持前/后排位置交换；敌人优先攻击前排；提供每回合加入的“位置交换”卡。

1) 规则与数据
- Ally（盟友）：`Entity` 子类（或轻量对象）
  - 字段：`id, name, health(=budget), is_frontline: bool`
  - 事件：`AllyJoinedBattle, AllyPositionChanged, BudgetChanged(=health changed), AllyLeftBattle`
- 位置：
  - 最小实现：玩家与盟友各带 `position_tag`（`"FRONT" | "BACK"`）。
  - 敌人攻击目标选择：若有盟友且其为 FRONT，则优先盟友；否则玩家。
- 位置交换卡：
  - 效果：交换双方 `position_tag`；发布 `AllyPositionChanged` 事件。
- 预算耗尽：
  - 触发 `AllyLeftBattle`，移除盟友；后续敌人默认攻击玩家。

2) 事件链（示例回合）
- TurnStarted(player) → Map/状态生效（`StatusApplied/Stacked`）
- CardPlayed(位置交换) → EnergyWasSpent → AllyPositionChanged
- 敌人回合：EnemyTurnStarted → EnemySkillChosen → 按目标选择（前排） → DamageService.apply_damage_to_player(...)/commit → EnemySkillResolved → EnemyTurnEnded

3) 技术落地建议
- 位置系统（最小骨架）：
  - 在 `CombatState` 增加 `ally: Optional[Entity]` 与 `position_tag`（玩家/盟友）；
  - 在 `DamageService.get_incoming_damage_multiplier` 预留读取位置标签（未来可加“前排受伤+X%”的地图规则）。
- 目标选择：在 `Enemy._apply_skill_effect` 前根据位置标签选择目标；本轮不改敌人体系可由 `QuickCombatModel` 提供一个简化策略（不更改敌人复杂逻辑）。
- 位置交换卡：实现一个 `SwapPositionEffect` 调整标签并发布事件。

4) 测试基线
- 位置交换有效：交换后，敌人优先攻击盟友；预算扣减；预算清零触发离场。
- 与服务/事件一致：
  - 交换 → `AllyPositionChanged`
  - 敌人攻击 → `EnemyTurnStarted/EnemySkillChosen/EnemySkillResolved`
  - 伤害通过 `DamageService`，并由状态系统正确放大/减免。

---

## 示例B：决战·PPT时间线（场景时间轴 + 光环）

要点：每2回合切换一次“PPT背景”，背景为地图光环（Aura），对战场施加增益/减益；玩家完全可预知顺序。

1) 规则与数据
- 时间线：固定长度序列（例如5项），元素为 `AuraRule`：
  - `{ name, duration_turns, on_apply(statuses...), on_remove(statuses...), modifiers(energy_cost_delta, draw_bonus, global_damage_mult, ... ) }`
- 触发：每2个玩家回合切换到下一项（`TurnStarted` 时检查并切换）。
- 典型光环：
  - 酷炫PPT → `[胸有成竹]`：每回合 +1 抽牌，卡牌费 -1（通过 `MapModifier` 改写 `CostService` 的修正或每回合发 `AddEnergy` 等策略）。
  - 简笔画PPT → `[支支吾吾]`：手牌上限 -1，卡牌费 +1；敌人获得 `[乘胜追击]`（对玩家伤害有穿透/倍率）。

2) 事件链（示例两回合切换）
- TurnStarted → 检查是否到达切换点 → 移除旧光环（`StatusEffectExpired`）→ 应用新光环（`StatusApplied/Stacked`）→ 写入可读日志（用于可视化时间线）。
- CardPlayed → EnergyWasSpent →（效果执行）→ Player/EnemyTookDamage。

3) 技术落地建议
- 使用 `MapModifier` 的“规则版”（例如 `RuleBasedMapModifier`）：
  - 订阅 `TurnStarted`，维护 `timeline_index` 与 `turn_counter`；达到阈值切换；
  - 执行 `StatusEffectManager.add_buff/add_debuff` 与成本/抽牌修正（通过现有服务。
- 可视化：UI 层读取“当前光环名称/剩余回合/下一项预告”。

4) 测试基线
- 时间线切换：每2回合切换一次；状态正确移除/应用；
- 数值修正：费用/抽牌/伤害倍率按规则生效；
- 与现有事件顺序一致：`TurnStarted` →（光环切换）→ 后续链路不受破坏。

---

## 与 Node2/Node3 其他战斗的映射建议

- 祖传代码第一课（小型战斗）
  - 以“洗牌污染/抽到诅咒”作为核心节奏：通过 `PileService` 在 `Shuffled` 或特定事件时注入负面卡。
- 实验室书堆考古（专注度规则）
  - 卡牌费用阈值/回合内第一张牌类型惩罚：实现 `MapModifier` 对 `CostService` 的动态门槛规则与 `StatusEffect` 惩罚注入。
- 在翻车边缘吹牛（外行的矜持）
  - 敌人永久 Debuff（减伤/对特定类别减伤），通过状态系统实现；达成条件（打出3张技能牌）时临时移除并转入易伤状态。

---

## 统一规则引擎与配置格式（草案）

两类玩法可共享一份场景配置，并由同一 MapModifier/状态系统/服务层承载。示意配置（最终字段以策划对齐为准）：

```json
{
  "scene_id": "node3_finale",
  "ally": {
    "enabled": true,
    "name": "代码佣兵",
    "resource": { "type": "budget", "current": 100, "max": 100 },
    "position": "FRONT",
    "leave_condition": { "type": "resource_zero" }
  },
  "position_rules": {
    "enemy_targeting": "frontline_first",
    "swap_card_id": "swap_position"
  },
  "timeline": {
    "enabled": true,
    "switch_every_turns": 2,
    "auras": [
      {
        "name": "酷炫PPT",
        "duration_turns": 2,
        "apply_status": [{ "type": "buff", "name": "胸有成竹", "value": 1 }],
        "modifiers": { "draw_bonus": 1, "cost_delta": -1 }
      },
      {
        "name": "简笔画PPT",
        "duration_turns": 2,
        "apply_status": [
          { "type": "debuff", "name": "支支吾吾", "value": 1 }
        ],
        "modifiers": { "hand_limit_delta": -1, "cost_delta": +1, "enemy_damage_piercing": true }
      }
    ]
  }
}
```

实现要点：
- 读取 JSON → 注册 `RuleBasedMapModifier` → 在 `TurnStarted/EnemyTurnStarted` 等事件点应用/移除状态、修改费用/抽牌等；
- 盟友“资源条”作为 Entity/轻量对象附着到 `CombatState`，目标选择遵循 `enemy_targeting`；
- 不改敌人系统的前提下，目标选择可先在 `QuickCombatModel` 层实现，后续再内聚到敌人侧。

---

## 版本化落地路径（不改敌人系统的前提下）

1) V1（1–2 天）
- 位置标签最小骨架 + 位置交换效果（仅标签，不改敌人核心AI，目标选择在模型层处理）
- RuleBasedMapModifier（时间线 + 2 种光环规则）
- 4–6 条单测：位置交换目标选择、预算HP扣减、时间线切换、光环生效与事件顺序

2) V2（1–2 天）
- 盟友实体化（可显示血量/受击动画），预算归零离场事件
- 地图规则配置化（JSON/类配置）
- 可视化时间线与当前光环 UI 钩子（占位）

---

## 日志与可观测性

- 使用 `stack_logger.context` 包裹关键流程（出牌、回合、光环切换、位置交换）；
- 短期可用“日志级 trace”（在入口生成 `trace_id` 并作为上下文输出）；
- 长期可将 `trace_id` 写入 `DomainEvent` 字段（兼容演进）。

---

## 风险与回退

- 位置系统：先仅标签+目标选择在模型层，避免大改敌人AI；
- 地图光环：通过状态系统/服务修正，不引入绕路写；
- 一切数值修改走统一服务（Cost/Energy/Damage/Pile），CI 已有守卫。


