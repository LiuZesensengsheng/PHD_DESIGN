# 论文线 EA 方案：研究方向-研究课题-论文题目（导师来源版）

## 1. 目标与范围

本方案用于 EA/Demo 阶段，先跑通论文线立意主流程：

1. 立意来源先收敛为唯一来源：导师给题（组会入口）。
2. 立意结构拆分为三层：`研究方向(Direction)`、`研究课题(Topic)`、`论文题目(Title)`。
3. 玩家在组会对话中只做一个决定：`接受` 或 `拒绝`。
4. 一旦接受，立即创建论文线并锁定该线甘特图规模。
5. 同局可并行多条论文线，但都归属同一局内主研究方向。

本方案不覆盖：

1. 自主发现和机会触发来源（后续版本再接）。
2. 局外成长系统（先不做数值化成长）。
3. 审稿战细则与战斗平衡。

## 2. 核心定义

### 2.1 研究方向（Direction）

1. 定义：本局学术身份与大方向（例如：具身智能）。
2. 作用：决定可抽取的 Topic 池与叙事语气。
3. 生命周期：按局生效，局内锁定。

### 2.2 研究课题（Topic）

1. 定义：某条论文线的具体问题（例如：动态场景语义分析）。
2. 作用：决定该条线甘特图模板、内容标签倾向、风险特征。
3. 生命周期：按论文线生效，接受时锁定。

### 2.3 论文题目（Title）

1. 定义：投稿阶段展示的最终标题表达。
2. 作用：叙事与风味，不直接改战斗数值。
3. 生命周期：可有历史版本（初稿/返修/终稿），任一时刻仅一个生效标题。

## 3. EA 核心规则（定版草案）

1. `run_direction_id` 初始为 `null`。
2. 第一次接受导师 Topic 时锁定 `run_direction_id`。
3. 后续导师只发该 `run_direction_id` 下的 Topic Offer。
4. 同局允许多论文线并行，但不得跨方向。
5. 立意质量（`LOW/MID/HIGH`）决定蓝图规模（长度/节点/奖励密度）。
6. 立意质量在 `accept` 时一次性锁定，不在立意环节二次改写。

## 4. 数据结构（持久化建议）

在 `persistent` 增加：

1. `run_direction_id: str | null`
2. `meeting_topic_cooldowns: dict[str, int]`
3. `meeting_topic_seen_counts: dict[str, int]`
4. `pending_topic_offer: dict | null`
5. `thesis_track_meta[track_index]` 扩展字段：
   - `direction_id: str`
   - `topic_id: str`
   - `idea_quality: "low" | "mid" | "high"`

说明：

1. `pending_topic_offer` 在 EA 可限制为最多一条待处理。
2. `thesis_track_meta` 继续作为论文线追踪主入口。

## 5. CSV 设计（首版模板）

## 5.1 `data/paper/research_directions.csv`

```csv
direction_id,name,opening_weight,enabled,desc
embodied_ai,具身智能,100,true,感知-决策-动作闭环
```

字段说明：

1. `opening_weight`：当本局未锁方向时用于抽方向。
2. `enabled`：开关字段，便于灰度。

## 5.2 `data/paper/research_topics.csv`

```csv
topic_id,direction_id,name,offer_weight,quality_low,quality_mid,quality_high,workload_profile,min_meeting_idx,max_meeting_idx,cooldown_meetings,once_per_run,dialogue_open,dialogue_accept,dialogue_reject,tags,risk_tags
emb_topic_001,embodied_ai,动态场景语义分析,30,45,40,15,W2,0,99,1,false,"导师：这个题不花哨，但能做、能发。接不接？","你：接，先把可复现链路打通。","你：先不接，我想再观察一轮。","#SEMANTIC,#DYNAMIC","#DATA_NOISE"
emb_topic_002,embodied_ai,姿态辨识鲁棒性优化,25,35,45,20,W3,0,99,1,false,"导师：把鲁棒性做出来，这条线会很硬。","你：接，我从基线复现实验开始。","你：不接，这轮周期太紧。","#POSE,#ROBUST","#TIME_PRESSURE"
```

字段说明：

1. `offer_weight`：同方向 topic 池中的抽取权重。
2. `quality_low/mid/high`：该 topic 的质量分布权重，总和必须为 100。
3. `workload_profile`：映射到甘特图模板配置（如 `W1/W2/W3`）。
4. `min_meeting_idx/max_meeting_idx`：出现时间窗（按组会计数）。
5. `dialogue_*`：组会对话文案。

## 5.3 `data/paper/paper_title_templates.csv`

```csv
template_id,direction_id,pattern,weight
title_emb_001,embodied_ai,基于{method}的{object}在{scenario}中的研究,40
title_emb_002,embodied_ai,{scenario}下{object}的{metric}优化方法,30
```

字段说明：

1. `pattern` 用于投稿时生成最终题目。
2. EA 阶段可先不实现变量填充，先用固定字符串池。

## 6. 组会发题流程（导师来源）

## 6.1 触发条件

1. 进入组会并点击导师给题入口。
2. 若 `pending_topic_offer` 非空，先要求处理现有 Offer。

## 6.2 生成步骤

1. 选方向：
   - 若 `run_direction_id` 为空：按 `research_directions.csv` 权重抽一个方向。
   - 若已锁定：直接使用该方向。
2. 选 Topic：
   - 从 `research_topics.csv` 过滤 `direction_id` 相同且满足时间窗/冷却/once 规则的条目。
   - 按 `offer_weight` 抽 1 条。
3. 选质量：
   - 按该 topic 的 `quality_low/mid/high` 权重抽 `idea_quality`。
4. 写入 `pending_topic_offer`，弹组会对话（`dialogue_open`）。

## 6.3 玩家决策

1. 接受：
   - 如未锁方向，写入 `run_direction_id`。
   - 调用论文蓝图应用服务创建新线。
   - 在 `thesis_track_meta` 写入 `direction_id/topic_id/idea_quality`。
   - 清空 `pending_topic_offer`，并更新 topic 冷却/seen。
2. 拒绝：
   - 不创建论文线。
   - 清空 `pending_topic_offer`。
   - topic 进入短冷却（建议 1 次组会）。

## 7. 与现有实现的最小接入点

1. 组会入口：`contexts/meeting/state.py` 的导师按钮回调。
2. 组会业务：`contexts/campaign/services/meeting_service.py` 增加导师发题用例。
3. 论文线创建：统一通过 `ThesisBlueprintAppService.apply_thesis_blueprint`，避免绕开元数据初始化。
4. 旧入口治理：暂时关闭手动 low/mid/high 立意弹窗入口（按钮与 F8/I）防止双系统冲突。

## 8. 验收标准（EA）

1. 导师入口可稳定产出 Topic Offer 对话。
2. 接受后立即新增论文线，且 `thesis_track_meta` 含 `direction_id/topic_id/idea_quality`。
3. 拒绝后不新增论文线，且 topic 冷却生效。
4. 同局多线并行时，所有新线 `direction_id` 一致。
5. 存档读档后，`run_direction_id` 与 topic 冷却状态正确恢复。

## 9. 待讨论项（下一轮对齐）

1. 本局初始是否允许玩家在第一次导师对话前预选方向。
2. `pending_topic_offer` 是否允许并存多条（EA 默认不允许）。
3. `workload_profile` 与 `idea_quality` 的映射是否双向覆盖还是主从关系。
4. 拒绝 topic 的冷却长度是否固定 1，还是按 topic 配置。
5. 题目模板变量（`{method}` 等）在 EA 是否先静态替换。

## 10. 意象统一：烛火 -> 发表星图固化（EA 收束版）

参考意象基线：

1. `docs/design/VIGOR_STRESS_SYSTEM.md` 中“知识荒原/火焰化作星辰/历史回响”段落。
2. 星图定位为“论文发表仪式”的视觉表达，不作为战斗中高频交互系统。

### 10.1 概念映射（定版草案）

1. `Direction`：星海中的一个研究区域。
2. `Topic`：该区域内一个待成形的“研究子图”（内部概念，不在战斗中频繁展示）。
3. 论文线战斗与关键块推进只产出“研究进展记录”（现有标签/里程碑数据），不弹星图界面。
4. 论文发表时统一读取该线进展记录，生成并固化一张“星座结果图”。
5. 最终 `Title` 与发表文案基于 `Direction + Topic + 该线标签摘要` 拼装。

### 10.2 标签与节点关系（定版草案）

1. 标签仍来自论文线既有流程（战斗结算/关键事件/里程碑），不新增“节点掉落”子系统。
2. 星图节点仅作为发表时的可视化映射结果，不反向驱动标签产出。
3. 同标签重复收益与平衡规则继续沿用现有标签系统，不在星图层重复实现一套逻辑。
4. 目标是保证“看起来在探索”，但系统核心仍是卡牌与论文线原流程。

### 10.3 EA 规模控制（防系统过重）

1. EA 不在“每次战斗后”展示可交互星图，避免形成第二玩法循环。
2. 战斗后允许极轻反馈（1 条短文本或微弱光效提示），但不进入星图界面。
3. 星图完整演出只在“论文发表”时触发一次。
4. EA 阶段不做跨局节点继承，只做本局内发表固化展示。

### 10.4 发表过场（叙事表现）

1. 触发：投稿结果为接收（或阶段性里程碑达成）。
2. 演出顺序：
   - 烛火被托起（个人努力）。
   - 进入知识荒原（未知空间）。
   - 火焰落地化星（贡献被固化）。
   - 镜头拉远见星海（个人与学术共同体关系）。
3. 文案拼装：
   - 固定句式 + `Direction` + 该篇固化子网摘要标签。

### 10.5 与主循环的边界

1. 星图系统只影响立意/内容生成与叙事呈现。
2. 不直接给战斗数值加成（攻击/防御/能量等）。
3. 不新增独立资源条与高频决策层，继续保持“卡牌战斗强度由卡组与战斗内决策主导”。

---

本文件为 EA 版讨论稿。  
定位：先做最小闭环，确保“导师发题 -> 接受/拒绝 -> 新论文线落地”可玩可测。
