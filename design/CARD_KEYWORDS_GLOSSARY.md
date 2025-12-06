## 卡牌关键词对照表（draft v1.1，中文详解）

> 目的：统一中文术语与数据/引擎Key，支撑白色v2（范式/坚定/规整/队列）与五色法典（颜色/心魔）接入。本文在 v1 基础上补充中文解释、触发窗口与边界规则。

---

## 版本
- 文档：v1.1（白色v2对接，中文详解）
- 适用：`data/cards/white/` 首批卡池；全局CSV导出

---

## A. 基础元信息与颜色（字段+说明）
- 颜色（理想色）
  - 白色：`WHITE` —— 秩序/范式/队列
  - 蓝色：`BLUE` —— 理论/控制/抽检
  - 黑色：`BLACK` —— 代价/掠夺/压迫
  - 红色：`RED` —— 行动/爆发/连动
  - 绿色：`GREEN` —— 节律/复利/成长
  - 无色：`COLORLESS` —— 不参与颜色冲突与同色-1
- 卡牌元字段（卡级）
  - `card_id: string`：唯一ID。
  - `name_key: string`：卡面名称（可作本地化Key）。
  - `description_key: string`：卡面描述（或本地化Key）。
  - `color: "WHITE|BLUE|BLACK|RED|GREEN|COLORLESS"`：卡牌所属颜色。
  - `type: "Attack|Skill|Power"`：攻击/技能/能力。
  - `rarity: "Common|Uncommon|Rare"`：常见/非常见/稀有。
  - `cost: number`：整数费用，≥0。
  - `keywords: string[]`：机制关键词（用于检索、统计、护栏提示）。
  - `tags: string[]`：主题/构筑标签（非机制）。
  - 常见布尔：`exhaust_on_play`（消耗）/ `ethereal`（虚无）/ `unplayable`（无法打出）/ `symmetric`（对称生效）。
- 效果数组
  - `effects: Effect[]`：按序结算的效果清单（详见 G 节）。

---

## B. 回合/事件触发窗口（Turn Hooks，语义）
- `on_turn_start`（回合开始）：本回合计数初始化、范式脉冲、状态衰减在此阶段触发。
- `on_turn_end`（回合结束）：清空自信、结转状态、清除“当回合”装填（如坚定标记）。
- `on_card_played`（出牌时）：出牌型触发（如端点脉冲）、心魔生成计数入口。
- `on_perfect_block`（完美格挡时）：一次伤害被自信完全吸收时触发（0溢出伤害）。
- `on_damage_instance`（伤害实例产生）：多段伤害逐段产生的早期窗口。
- `on_damage_finalized`（伤害最终结算）：护甲/减免计算后，将要入生命的最终数值；规整在此追加纯伤。
- `on_enemy_repositioned`（敌人位置改变后）：成功完成移动/交换后触发；失败则不触发。
- `on_sequence_step`（序列步进）：序列类效果在每一步目标变化时的步进窗口。

边界：
- “完美格挡”仅在最终伤害=0 且由自信吸收时成立；被“免疫/无敌”化解不算“由自信吸收”。
- 多段伤害每段独立产生与结算，分别触发与计数。

---

## C. 通用状态（Statuses）
- 破防：`Vulnerable` —— 承受的攻击伤害提高50%（乘算）。
- 虚弱：`Weak` —— 造成的攻击伤害降低（乘算）。
- 规整：`Regulated` —— 白色v2新增的“纯伤追加”状态（详见 D.3）。

---

## D. 白色 v2 核心机制（中文详解）

### D.1 范式（Paradigm）
- 定义：一种“持续的全局规则”。加入后在指定窗口（通常为`on_turn_start`）按顺序触发其“载荷效果（payload）”。可同时存在多个不同范式。
- 目的：建立秩序，形成稳定且可预测的收益或限制，使队列/坚定/规整等子系统有节律地工作。
- 数据建议：
  - `type: "add_paradigm"`
  - `paradigm_id: string`：同名范式的识别ID。
  - `activation_window: "on_turn_start" | ...`：触发窗口。
  - `symmetric: boolean`：是否对称作用于敌我双方。
  - `payload: Effect[]`：在触发窗口执行的一组效果（如“获得自信”“对全体敌人施加本回合规整+1”）。
  - 可选：`stack_strategy: "keep_highest" | "keep_latest"`：同名不叠加时的保留策略（建议默认 `keep_highest`，具体以实现定稿）。
  - 可选：`soft_caps: Record<string, number>`：同类数值效果的合计软上限（如“回合开始自信总获得量≤5”）。
- 并存与顺序：
  - 允许不同范式并存；结算顺序为“玩家→敌人”，同侧内部按加入顺序。
  - 同名/同ID范式不叠加；按 `stack_strategy` 决定保留版本。
- 典型例子：
  - 充分条件：你的自信在回合结束时不移除（`payload: persist_confidence`）。
  - 公理体系：回合开始时你与敌人各获得X点自信（`symmetric: true`）。
  - 学术伦理：每单位每回合首次受到的攻击伤害减半（附“每回合仅一次”的护栏）。
- 边界：
  - 范式的“对称”只决定效果是否同时作用于双方，不改变其触发顺序。
  - 范式载荷应尽量使用“上限/阈值”避免指数增长（通过 `soft_caps` 表达）。

### D.2 坚定（Steadfast）
- 定义：可跨回合保存的“完美格挡奖励”Buff。相关牌会“装填”坚定标记（可多种类型、可叠加）；坚定不会在回合结束自动清空。每当触发完美格挡，消耗1层并结算对应的坚定效果。
- 触发条件：在`on_perfect_block`窗口（最终伤害由自信完全吸收）。
- 标记类型（装填用）：
  - 精力充沛：触发时获得能量（`STEADFAST_ENERGY`）。
  - 思如泉涌：触发时抽牌（`STEADFAST_DRAW`）。
  - 妙语连珠：触发时对当前所有敌人造成X点伤害（`STEADFAST_WITTY_STRIKE`，`target: leftmost_enemy`）。
- 数据建议：
  - 装填：`{ type: "add_steadfast_token", token_type: "STEADFAST_ENERGY|STEADFAST_DRAW|STEADFAST_WITTY_STRIKE", value: number }`
  - 结算：由系统在`on_perfect_block`窗口按类型消耗层数并结算；`persists_across_turns: true`。
- 边界：
  - 当回合可多次装填与多次触发；每次触发后相应类型的层数-1；未触发不清空，可跨回合保留。
  - 未达成完美格挡（有任意生命伤害）不触发；护盾/无敌免伤不算“由自信完全吸收”。

### D.3 规整（Regulated）
- 定义：跨回合持续的“秩序化惩罚”。只有在层数 L>0 时，本回合启用“递增纯伤”逻辑：当该单位本回合每次受到“未被完全格挡”的伤害，在“最终结算”追加 `k+1` 点纯伤，并令 `k := k+1`；回合结束 `k` 清零。下回合开始 `L` 衰减（通常-1）。
- 触发窗口：
  - `on_turn_start`：`L := max(0, L-1)`（若有范式脉冲，可在衰减前/后再+1以维持≥1）。
  - `on_damage_finalized`：当本次伤害未被自信完全吸收时，追加 `k+1` 纯伤，随后 `k:=k+1`。
- 多段与群体：
  - 多段：每段独立触发与递增（例：同回合连续4段→+1, +2, +3, +4）。
  - 群体：每个单位独立维护自身的 `L` 与 `k`。
- 来源标签（便于数据与遥测）：`Regulated_Source:Paradigm|Compliance|Direct`（范式脉冲/合规则奖励/直赋）。
- 边界：
  - 规整的追加伤害为“纯伤”（不参与易伤/力量乘算），仅受“纯伤减免类”白名单影响（若存在）。
  - 当回合 `k` 从0开始；回合结束清零；不跨回合。

### D.4 端点 / 序列（Queue / Endpoints / Sequence）
- 端点（Endpoints）：将战场敌人按从左到右形成“队列”。
  - 最左端点：`leftmost_enemy`；最右端点：`rightmost_enemy`。
  - 目标锁定类牌可指定端点以获得额外收益（如返能/加伤）。
- 队列操作（Reposition）：
  - 交换相邻：`{ type: "reposition", op: "swap_with_right" }`（需存在右侧）。
  - 移至端点：`{ type: "reposition", op: "move_to_leftmost|move_to_rightmost" }`。
  - 成功条件：目标确实改变了位置；若目标不可移动（定身/锚定），视为失败，不触发“成功移位”奖励。
- 序列结算（Sequence）：
  - 定义：按队列从一端向另一端逐个结算，每步伤害或效果可按步进系数递增。
  - 数据表示（示例）：`{ type: "sequence_damage", base: 3, step: 2, target: "left_to_right" }` 表示最左开始，依次对下一个+2。
  - 边界：遇到击杀时继续指向“新的相邻单位”；若队列为空则结束。

---

## E. 护栏与并存规则（推荐选项）
- 触发频次上限：
  - `per_turn_limit`：每回合触发次数上限（如“并行处理”每回合≤5）。
  - `per_unit_per_turn_limit`：每单位每回合上限。
- 范式并存：
  - 同名不叠加：`stack_strategy: "keep_highest" | "keep_latest"`（默认建议 `keep_highest`）。
  - 同类软上限：`soft_caps` 限制同类增益的合计（避免指数膨胀）。
  - 结算顺序：玩家→敌人；同侧按加入顺序：`ordering: "join_order"`。
- 0费护栏：
  - `zero_cost_frequency_guard: true`：对0费牌/0费触发类效果的全局频次限制（避免无限）。

---

## F. 心魔（Ideals 对接）
- 统一ID：
  - 混乱（白）：`CURSE_CHAOS`
  - 短视（蓝）：`CURSE_MYOPIA`
  - 软弱（黑）：`CURSE_WEAKNESS`
  - 迟疑（红）：`CURSE_HESITATION`
  - 枯萎（绿）：`CURSE_WITHER`
- 生成规则（摘要）：
  - 在 `on_card_played` 判定“出牌颜色与理想冲突”→在回合结束时向弃牌堆注入对应心魔。
  - 上限：`per_play_curse_cap = 2`；`per_battle_curse_cap = 6`（防止雪崩）。

---

## G. 常用效果Key（语义与示例）
- 伤害：
  - 格式：`{ type: "damage", value, hit_count?, target }`
  - `target` 可为：`selected_enemy|all_enemies|random_enemy|leftmost_enemy|rightmost_enemy`。
  - 多段：`hit_count`>1 表示同一目标多段；序列多目标请使用 `sequence_damage`。
- 自信（格挡）：
  - `confidence` 效果：`{ type: "confidence", value, target: "player|ally" }`。
  - 与“充分条件（自信不清空）”的交互通过范式处理。
- 状态：
  - `status`：`{ type: "status", status_type: "Vulnerable|Weak|Regulated|...", duration?, value?, target }`。
  - `Regulated` 多采用“本回合+X”的赋值，跨回合维持由范式脉冲负责。
- 抽牌/能量：
  - 抽牌：`{ type: "draw", count, target: "player" }`。
  - 能量：`{ type: "gain_energy" | "lose_energy", value }`。
- 严谨度：
  - 永久/临时：`{ type: "rigor" | "temporary_rigor", value, target: "player" }`。
- 位置与队列：
  - `reposition`：`{ op: "swap_with_right|move_to_leftmost|move_to_rightmost", target: "selected_enemy" }`。
- 范式：
  - `add_paradigm`：见 D.1；`payload` 中可放入任意效果列表。
- 坚定装填：
  - `add_steadfast_token`：见 D.2；由系统在 `on_perfect_block` 合并结算。

---

## H. 关键词（`keywords` 字段建议值：中文详解）
- `Paradigm`（范式）：标记该牌/被动创建或交互“范式”。用于库内检索、统计与UI提示。
- `Steadfast`（坚定）：涉及“完美格挡触发”的奖励机制。
- `Steadfast_Load`（坚定装填）：该牌会为“下一次坚定”装填一个或多个标记。
- `Regulated`（规整）：与“规整”状态相关（施加/触发/维持）。
- `Regulated_Source:Paradigm|Compliance|Direct`：规整的来源标记（范式脉冲/合规则奖励/直赋）。
- `Endpoint`（端点）：与“最左/最右”位置或“位移到端点”相关。
- `Sequence`（序列）：按队列逐步结算的效果或伤害。
- `PerTurnLimit:N`：该牌/被动每回合最多触发N次（用于读招与平衡护栏）。
- `Symmetric`（对称）：效果同时作用于敌我双方（多见于范式）。
- `Exhaust`（消耗）：打出后本战移除。
- `Ethereal`（虚无）：回合结束若在手牌中则消失。
- `Unplayable`（无法打出）：本身不能被玩家手动使用（用于心魔等）。

---

## I. 待确认（校对项）
- [ 先保留 ] 范式同名并存策略：默认采用 `keep_highest` 是否符合你的实现偏好？
- [ 对 ] 规整的追加伤害一律作为“纯伤”处理（不参与易伤/力量乘算），仅受明确的“纯伤减免白名单”影响
- [ 先暂定保留 ] 坚定装填三种类型的英文Key：`STEADFAST_ENERGY / STEADFAST_DRAW / STEADFAST_WITTY_STRIKE` 是否保留？
- [ 暂定保留 ] 端点目标命名：`leftmost_enemy / rightmost_enemy` 是否符合你的引擎与UI文案风格？

---

备注：本对照表为数据定义基线，不涉及具体数值。确认后将据此在 `data/cards/white/` 录入首批白色v2卡池，并同步生成CSV（扁平化 effects 以便Excel检索）。
