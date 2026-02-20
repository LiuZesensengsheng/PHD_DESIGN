# 论文线标签池 SSOT（Single Source of Truth）v1 草案

> 目标：统一论文线“标签”口径。  
> 本文定义唯一数据源：`paper_tags`（单标签池）。  
> 任何阶段（Idea/实验/写作/审稿/Boss/Response）都只读写这一个池子。

---

## 1. 核心结论（唯一口径）

- 论文线全程只有一个标签池：`paper_tags[]`。
- 标签只有两种极性：`positive`（正向）与 `negative`（负向）。
- 玩家的探索表现、战斗结果、事件选择，都会向同一个池子增删标签。
- 最终 Boss 层/审稿结果层，只读取“当前标签池快照 + 投稿层级（T0~T4）”进行结算。
- 不再并行维护“仅风味、不入结算”的第二套论文标签系统。

---

## 2. 数据模型（最小可实现）

```json
{
  "paper_tags": [
    {
      "id": "method_rigorous",
      "name": "方法严谨",
      "polarity": "positive",
      "axis": "method",
      "weight": 2,
      "source": "experiment",
      "phase_added": "research",
      "stackable": false,
      "ttl_rounds": null
    }
  ]
}
```

字段定义（MVP）：
- `id`: 唯一标识（机器可读，snake_case）。
- `name`: 展示文本。
- `polarity`: `positive | negative`。
- `axis`: 标签轴（如 `novelty/method/language/figure/baseline/impact/ethics`）。
- `weight`: 权重，建议 `1..3`（默认 `1`）。
- `source`: 来源（`idea/experiment/writing/review/boss/event`）。
- `phase_added`: 写入阶段（`idea/research/writing/review/response`）。
- `stackable`: 是否可重复叠加（MVP 建议默认 `false`）。
- `ttl_rounds`: 生命周期（`null` 表示常驻；MVP 建议大多数常驻）。

---

## 3. 标签池生命周期（按流程）

### 3.1 Idea 阶段（初始化）
- 生成 2-3 个正向“核心卖点”标签（如 `problem_important`, `method_novel`）。
- 可同时生成 0-1 个负向“潜在风险”标签（如 `scope_too_wide`）。

### 3.2 研究/实验阶段（主增益期）
- 成功探索主要新增正向执行标签（`sample_solid`, `replicable_design`）。
- 失败或偷懒可新增负向标签（`insufficient_controls`, `data_noise`）。

### 3.3 写作阶段（规范化）
- 修正类任务可移除部分负向标签（`language_rough`, `figure_blurry`）。
- 赶工/跳步会新增对应负向标签。

### 3.4 审稿战/Boss 阶段（攻防）
- 敌方技能可直接移除正向标签或新增负向标签。
- 玩家通过战斗、奖励、换位/策略可恢复或新增正向标签。

### 3.5 Response 阶段（只读结算）
- 默认不再让玩家微操标签明细。
- 使用标签池快照生成“最终问题”“应对检定”“结果倾向”。

---

## 4. 结算口径（Boss 与审稿统一）

定义聚合量：
- `P = sum(weight of positive tags)`
- `N = sum(weight of negative tags)`
- `B = core_positive_alive_count`（核心卖点幸存数）

建议的统一质量分（概念）：
- `submission_score = base + a*P - b*N + c*B + tier_modifier(Tx)`

统一规则：
- 若 `B == 0`，触发“核心卖点坍塌”惩罚（强烈降低接收倾向）。
- 若 `N` 超阈值，提升 Major/Reject 倾向。
- T0~T4 只作为投稿难度与裁决口味修正，不替代标签结算。

---

## 5. 投稿层级与标签池关系（与现规则兼容）

- 首投层级可选，最高 T0；Reject 必降一档直到 T4。
- 每次裁决都读取同一份 `paper_tags`（不重置）。
- 返修阶段允许通过任务移除/缓解负向标签后再重投。
- T4 不再降档，且仍可能 Reject；可根据标签质量给出“体面接收/勉强接收/再次重投”的叙事差异。

---

## 6. UI 与可读性（玩家可理解）

- 论文显示“标签池面板”：推荐显示 6-8 个关键标签（其余折叠）。
- 正向标签用亮色徽章；负向标签用警示色。
- Hover 显示：来源、轴、当前影响（简述）。
- 回合日志记录：`+标签/-标签` 变动，确保玩家理解因果。

---

## 7. 系统接口（实现约束）

- Track/Campaign/Boss/Review 系统不得自行维护“第二标签状态”。
- 所有变更通过统一接口提交（示例）：
  - `add_tag(tag_id, meta)`
  - `remove_tag(tag_id, reason)`
  - `replace_tag(old_tag_id, new_tag_id)`
  - `snapshot_tags()`（用于裁决与回放）
- 审稿/Boss 只消费 `snapshot_tags()`，不直接拼接文案推断状态。

---

## 8. 不变量与校验

- 同一 `id` 且 `stackable=false` 时不可重复入池。
- `weight` 必须在有效区间（建议 `1..3`）。
- `polarity` 与 `axis` 必须合法。
- 每篇论文至少应存在 1 个“核心卖点标签”来源于 Idea 阶段。

---

## 9. 与现有文档的对齐指引

需统一的旧口径：
- 把“标签仅风味、不做硬数值”改为：风味可保留，但底层统一落到 `paper_tags`。
- 把“流程块 tags（waiting/review_judgment）”与“论文语义标签”区分命名：
  - 流程块标签建议保留为 `block_tags`；
  - 论文语义标签统一称 `paper_tags`。

---

## 10. MVP 验收（Definition of Done）

- 能在一局内看到标签池从 Idea 到审稿的连续变化。
- 每个关键阶段至少触发一次 `+positive` 与一次 `+negative`。
- 最终裁决可复盘到标签快照（可解释“为什么是这个结果”）。
- Reject 重投后标签池不丢失，且可通过返修任务改善。
- 程序层只存在一个论文语义标签池数据源。

---

## 11. 版本注记

- v1 草案定位：先统一语义与接口，不追求复杂公式最优。
- 后续可扩展：
  - 分类权重（按 axis 分开系数）
  - 标签联动（组合加成/冲突）
  - 层级化审稿人口味模型（Reviewer persona）

