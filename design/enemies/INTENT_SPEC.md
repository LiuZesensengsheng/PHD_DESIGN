# 敌人意图系统（草案）

> 目的：以“强类型 + 自解释 + 数据驱动”为准绳，定义敌人在战斗中的【选择-解析-影响】闭环，支撑可迭代的AI行为与可复盘的调参流程。本文为独立草案，稳定后并入总设计文档。

## 1. 核心目标
- 强类型：以 `EnemyIntent` 数据结构表达意图而非纯字符串。
- 自解释：意图从“如何被选中、为何被选中、实际造成什么效果”三个阶段具备结构化日志与事件。
- 数据驱动：技能/意图的权重、冷却、条件、目标策略从数据（JSON）中获取，默认选择器可替换。

## 2. 数据模型
### 2.1 EnemyIntent
- intent_id: string（`intent::<skill_id>` 或策略生成）
- name: string（用于UI展示）
- intent_type: Enum ['Attack','Buff','Debuff','Utility']
- targeting: Enum ['Player','Self','Random']
- params: Dict（携带效果原始参数与选择上下文）
- source_skill_id: string|null（溯源技能）

示例：
```json
{
  "intent_id": "intent::attack1",
  "name": "准备使用 基础攻击",
  "intent_type": "Attack",
  "targeting": "Player",
  "params": {"effect": {"type": "damage", "min_value": 6, "max_value": 10}},
  "source_skill_id": "attack1"
}
```

### 2.2 EnemySkill（补充字段，向下兼容）
- effect.weight: int ≥1（权重，默认1）
- effect.cooldown: int ≥0（冷却回合，默认0）
- effect.conditions: Dict（选择条件，key见下文）

条件约定（最小集，可扩展）：
- player_confidence_leq: int（玩家当前格挡≤X）
- enemy_hp_geq: int（敌人当前生命≥X）

## 3. 选择器（Selector）
默认实现 DefaultIntentSelector：
1) 冷却衰减：每回合选择开始时对该敌人所有技能冷却减1。
2) 候选集：从手牌中过滤能量可负担的技能；若无则退回到全部手牌。
3) 条件过滤：按 `effect.conditions` 过滤不可用技能。
4) 冷却过滤：剔除仍在冷却中的技能。
5) 权重抽样：按 `effect.weight` 做加权随机，若集合为空退回候选集随机。
6) 冷却设置：命中技能若有 `cooldown>0`，记录冷却。
7) 意图映射：将技能 effect 的 type 映射到 `intent_type/targeting`，封装为 `EnemyIntent`。

可替换：通过策略接口 `IntentSelector` 注入自定义选择器（如基于状态机/脚本/蒙特卡洛等高级AI）。

## 4. 事件与日志
- 事件增强（建议）
  - EnemySkillChosen: {enemy_id, skill_id, skill_name, intent_type, targeting, weight, cooldown_remaining}
  - EnemySkillResolved: {enemy_id, skill_id, result, actual_values}
- 结构化日志（stack_logger，建议）
  - SELECT: 候选→过滤→加权池（列表与权重快照）
  - RESOLVE: 命中技能与意图映射、目标
  - APPLY: 真实数值（如施压=7）、发布的领域事件ID

## 5. JSON 约定（草案）
```json
{
  "skills": [
    {
      "skill_id": "attack1",
      "name": "基础攻击",
      "description": "造成8点压力",
      "cost": 1,
      "type": "Attack",
      "effect": {
        "type": "damage",
        "min_value": 6,
        "max_value": 10,
        "weight": 2,
        "cooldown": 1,
        "conditions": {"player_confidence_leq": 12}
      }
    }
  ]
}
```

## 6. 与领域对象的接口
- Enemy
  - `set_intent(intent: EnemyIntent)`：设置意图（UI展示用 `intent.name`）。
  - `select_skill_for_turn()`：优先使用选择器返回的意图→同步 `selected_skill`；若失败退回“能量最高”旧逻辑。
  - `get_current_stats()`：返回 `intent` 为结构化字典。

## 7. 测试建议（最小集）
1) 权重有效性：高权重技能在多次选择中出现频率更高（统计容忍区间）。
2) 冷却生效：被选中后 N 回合内不再被选中。
3) 条件过滤：当玩家格挡>阈值时，某些技能不可被选中。
4) 事件一致性：Resolved 的实际数值与 `DamageService` 汇总一致。

## 8. 迁移策略
- 阶段A：仅新增字段与结构化返回，保持旧逻辑兼容（已完成）。
- 阶段B：逐步把技能 JSON 增补 `weight/cooldown/conditions` 并观察选择结果；接入结构化日志，形成可复盘流水线。
- 阶段C：按需要替换选择器为更高级策略；完善事件载荷与可视化工具。

## 9. 开放问题
- 更复杂的目标策略（多目标、按标签选择）需要何种规则描述？
- 条件表达式是否需要表达式语言（避免逻辑爆炸）？
- 是否需要在 Campaign 层对敌人AI参数做全局难度曲线修正？

（本文件为草案，随实现演进更新）



