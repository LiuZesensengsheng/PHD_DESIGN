# 论文线「写作×导师」多阵营对战规格（导演式）V0.1

> 定位：投稿前固定触发的一场关键战斗。  
> 目标：在不拆成三套系统的前提下，通过“阵营组合变化 + 标签联动 + 导演式抽取”提供反复游玩新鲜感。

---

## 1. 为什么值得投入

- 这是论文线重复出现的高频节点，体验质量直接决定“会不会腻”。
- 这块可以作为论文线最具辨识度的亮点：学术冲突被具象成可玩战斗。
- 用统一骨架做多组合，后续扩内容成本低，适合持续迭代。

结论：值得投入，但应投入在“框架和配置化能力”，而不是一次性堆大量特效和脚本。

---

## 2. 设计原则

- 单一战斗骨架：所有模式共享同一套核心机制。
- 阵营只改镜头：ABC 只改变“谁和谁打、目标偏置、事件口味”，不改底层规则。
- 标签强联动：论文标签必须能影响战斗过程和结果反馈。
- 导演式随机：不做纯 1/3 随机，避免连刷同模式。

---

## 3. 统一战斗骨架（所有模式共用）

### 3.1 核心对象

- `DDL倒计时`：剩余回合数。
- `异议槽`：`method/language/scope/baseline/novelty/impact` 六个槽位。
- `返工债`：本回合未处理异议累积为债务，回合末触发惩罚。

### 3.2 通用胜负

- 胜利：在倒计时内压下关键异议（例如清空高优先异议或总异议值低于阈值）。
- 失败：倒计时结束仍超阈值，视为“写作未过审”，不能投稿。

### 3.3 主流程联动

- 胜利：解锁投稿弹窗（选择 T0~T4）。
- 失败：保持在写作阶段，下回合可重打同节点。

---

## 4. 阵营组合池（先做 3 核心 + 3 扩展）

> 说明：仅改变阵营、目标偏置和事件包；不新增底层系统。

### 4.1 核心组合（首发）

1. `A` 我 + 导师 vs 论文  
语义：共同打磨稿件。  
偏置：`language/scope` 异议更高频。  
戏剧点：导师“帮你改，但嘴很毒”。

2. `B` 我 + 论文 vs 导师  
语义：投稿前答辩压力测试。  
偏置：`method/baseline/novelty` 异议更高频。  
戏剧点：导师作为审查者连续追问。

3. `C` 我 vs 导师 + 论文  
语义：崩溃夜战（内耗具象化）。  
偏置：异议混合，返工债增长更快。  
戏剧点：一边被导师催，一边被稿件问题反噬。

### 4.2 扩展组合（后续）

1. `D` 我 vs 我的论文  
2. `E` 我 vs 师兄 + 论文  
3. `F` 我 + 导师 vs Reviewer2幻影

---

## 5. 导演式抽取（避免纯随机）

每次触发写作战时，为每个模式计算分数并加权抽取：

`mode_score = base + novelty_bonus + tag_fit_bonus + narrative_bonus - repeat_penalty`

### 5.1 建议参数

- `repeat_penalty`：上次模式再次出现时 `-0.45`。
- `novelty_bonus`：近期未出现模式 `+0.25`。
- `tag_fit_bonus`：与当前标签问题匹配的模式 `+0.20~0.35`。
- `narrative_bonus`：上轮 `reject` 时提高冲突模式（B/C）`+0.20`。

### 5.2 护栏

- 同一模式最多连续 2 次。
- 任意 4 次写作战内，至少出现 2 种不同模式。

---

## 6. 标签联动（必须落地）

### 6.1 标签到异议的映射

- `method` 负向：方法异议初始层数 +1。
- `baseline` 负向：对比实验异议触发率上升。
- `language` 负向：措辞/结构异议触发率上升。
- `novelty` 正向：创新槽初始抗性 +1。
- `impact` 正向：终局阈值略放宽。
- `scope` 负向：回合末返工债额外 +1。

### 6.2 战后标签变化（占位规则）

- 胜利：移除 1 个主轴负向标签或降权 1 层。
- 失败：新增 1 个对应轴负向标签（可堆叠）。
- 模式差异：A 偏语言轴、B 偏方法轴、C 偏综合轴。

---

## 7. 数据结构建议（配置化）

```json
{
  "mode_id": "B_player_paper_vs_mentor",
  "enabled": true,
  "base_weight": 1.0,
  "left_units": ["player", "paper"],
  "right_units": ["mentor"],
  "axis_bias": {"method": 0.3, "baseline": 0.25, "novelty": 0.2},
  "debt_growth_mult": 1.0,
  "win_tag_rewards": [{"axis": "method", "action": "downgrade_negative"}],
  "lose_tag_penalties": [{"axis": "method", "action": "add_negative"}]
}
```

### 7.1 接口边界（先约定，后实现）

- 输入：`WritingBattleDirectorContextDTO`
- 输出：`WritingBattleSceneRecipeDTO`
- 约束：导演器只负责“选模式 + 生成配方”；战斗系统只消费配方，不反向改导演规则。

```json
{
  "WritingBattleDirectorContextDTO": {
    "track_index": 0,
    "round": 2,
    "paper_tags_snapshot": [
      {"id": "baseline_thin", "axis": "baseline", "polarity": "negative", "weight": 1}
    ],
    "last_mode_id": "A_player_mentor_vs_paper",
    "recent_mode_ids": ["A_player_mentor_vs_paper", "B_player_paper_vs_mentor"],
    "last_verdict": "reject",
    "pressure": 72,
    "seed": 12345
  },
  "WritingBattleSceneRecipeDTO": {
    "mode_id": "C_player_vs_mentor_paper",
    "left_units": ["player"],
    "right_units": ["mentor", "paper"],
    "axis_bias": {"method": 0.2, "baseline": 0.2, "language": 0.15},
    "debt_growth_mult": 1.2,
    "turn_limit": 4,
    "win_rules": ["objection_total_below_threshold"],
    "on_win_tag_ops": [{"op": "downgrade_negative", "axis": "method"}],
    "on_lose_tag_ops": [{"op": "add_negative", "axis": "scope"}]
  }
}
```

---

## 8. 分阶段落地

### M1（先做）

- 只上线 A/B/C 三模式。
- 复用同一遭遇框架，只切换编组与参数。
- 接通标签影响与战后标签变化。

### M2（迭代）

- 增加 D/E/F 扩展模式。
- 增加模式专属事件包和台词。
- 做少量视觉差异化（不改核心逻辑）。

---

## 9. 资源建议

- 优先级：高（论文线亮点候选）。
- 投入建议：先用中等资源完成 M1，验证留存与重复感，再决定是否扩展 M2。
- 关键不是“做更多模式”，而是“把导演器和标签联动做实”。

---

## 10. 实现清单（可勾选）

### 10.1 框架冻结项（先文档）

- [ ] 统一骨架冻结：`DDL倒计时 + 异议槽 + 返工债 + 通用胜负`。
- [ ] 模式池冻结：首发 A/B/C，扩展 D/E/F 仅登记不实现。
- [ ] 导演式抽取冻结：评分公式、参数区间、反重复护栏。
- [ ] 标签联动冻结：每个 axis 至少一条“战斗影响 + 战后影响”。
- [ ] 边界冻结：`ContextDTO -> RecipeDTO`，战斗只消费 `RecipeDTO`。

### 10.2 M1 实装项（最小可玩）

- [ ] 导演器服务：`build_recipe(context) -> recipe`。
- [ ] 配置表：A/B/C 三模式参数 JSON。
- [ ] 战斗入口接线：固定投稿前战斗读取 `recipe`。
- [ ] 标签回写：胜/败后标签变化写回论文标签池。
- [ ] 观测日志：记录模式分布、胜率、平均回合、重复率。

### 10.3 迭代门槛（再扩展前）

- [ ] 连续 10 局中，单一模式占比不超过 60%。
- [ ] 玩家可感知“标签在影响战斗”（可通过访谈或埋点佐证）。
- [ ] 单局时长稳定在目标区间（例如 4~8 分钟）。
