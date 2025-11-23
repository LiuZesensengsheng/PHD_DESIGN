### 组会事件池：分支条件与选择逻辑（MVP → 可扩展蓝图）

本文件定义“组会（Meeting）事件池”的分支条件、筛选与选择算法，以及效果落地与持久化规范，作为实现与迭代的蓝图。目标是做到：
- 清晰、可验证、可扩展；
- 与领域服务（Track/Reward/Thesis 等）解耦；
- 零魔法值（常量集中），并遵守DDD内向依赖。

本设计与当前代码对齐：`contexts/campaign/services/meeting_service.py`、`contexts/campaign/services/meeting_event_templates.py`、`constants/campaign_meeting.py`。

---

#### 1) 关键术语与输入信号
- 回合与触发：
  - 组会固定触发轮次：`MEETING_ROUNDS = {0,5,10,15,20,25,30,35}`。
  - 当前回合：`state.current_turn`（int）。
- 任务线与上限：
  - 当前任务线数量：`len({b.track_index for b in state._blocks})`。
  - 上限：`MAX_TASK_LINES = 4`。
- 货币与经济：
  - 灵感：`state.persistent['inspiration']`，服务层通过 `InspirationService` 读写。
- 牌组与改造：
  - 当前卡组：`state.persistent['deck_card_ids']`（list[str]）。
  - 升级过的卡：`state.persistent['upgraded_card_ids']`（list[str]）。
- 会话与冷却：
  - 会话回合：`state.persistent['meeting_session_turn']`。
  - 事件冷却与计数：见 5) 持久化。

可选/未来信号（当前未实现，仅预留）：
- 近K回合“进度/活跃度”评分（如完成事件/战斗/DDL推进，命名：`progress_score_last_k`）。
- 负面状态/临时debuff（如DDL压力）。
- 特质/标签（`state.persistent['traits']`）。

---

#### 2) 事件结构定义（逻辑层面的数据模型）
事件（MeetingEvent）建议扩展以下字段（模板中的最小子集已存在）：
- id: str（唯一）
- title: str（标题）
- who: str（“导师”|“师兄”|“自语”）
- category: str（"mentor"|"peer"|"flavor"|"system"）
- trigger_window: { min_turn?: int, max_turn?: int }（可选触发窗口）
- requires_can_add_line: bool（是否仅在未达上限时允许出现）
- conditions: 
  - all_of: [Condition]（全部满足）
  - any_of: [Condition]（至少一个满足）
- weight: int（权重；默认1）
- cooldown: int（单位：会议次数；默认0）
- once_per_run: bool（是否一局只出现一次；默认False）
- effects: [Effect]（点击选项后应用的效果声明；最小可为"grant_inspiration"、"defer_add_task_line"等）

Condition（MVP建议的原子条件）：
- can_add_task_line: bool（由 MeetingService._can_add_line() 提供）
- inspiration_ge: int
- inspiration_le: int
- tracks_lt: int（当前任务线数量 < X）
- deck_size_ge: int
- upgraded_cards_ge: int
- turn_in: set[int]（通常不必，用于演示或特殊剧情）

Effect（MVP建议的原子效果）：
- grant_inspiration: { amount: int }（正负皆可）
- defer_add_task_line: {}（在返回战役后应用新任务线）
- grant_trait: { id?: str|"random" }（若特质系统未完备，先用占位）
- open_reward: { reward_id: str }（复用 RewardService）

注：条件与效果仅声明，真实执行交由服务层完成（MeetingService/RewardService/TrackService 等）。  

---

#### 3) 选择算法（过滤 → 加权抽取 → 回退）
输入：事件池 E，全局/会话状态 S。
输出：一个可展示的事件（含若干选择项）。

步骤：
1. 过滤（Filter）
   - 时间窗口过滤：若定义了 `trigger_window` 则需满足。
   - 冷却/次数：命中 `cooldown` 或 `once_per_run` 约束的事件剔除。
   - 条件判断：满足 `all_of` 且至少一个 `any_of`（若定义）。
   - 特殊约束：`requires_can_add_line = True` 时，只有在未达上限时保留。
2. 加权选择（Weighted Sample）
   - 对剩余事件按 `weight` 求和并进行一次随机抽取。
3. 回退（Fallback）
   - 若无事件通过过滤，回退到“风味”类（category="flavor"）的保底事件（例如简单的灵感+10 / 无变化）。
4. 展示
   - 将事件的 `title`、`who`、`choices[text]` 展示在 `MeetingEventModal`。
   - 点击选项后按 `effects` 顺序逐个应用。

注意：
- “新增任务线”建议不是直接落地，而是通过 `defer_add_task_line` 在返回战役时由 `CampaignState.startup()` 应用（现已实现），以保持状态边界清晰。

---

#### 4) 事件类别与分支指引（首批）
- Mentor（导师类）
  - “保持状态”：面向近K回合活跃（未来接 K 评分）；当前MVP以 `inspiration_ge`/`upgraded_cards_ge` 作为弱替代。
  - “督促改进”：面向低活跃；奖励较小或为承诺类（下次加大，MVP先占位）。
  - “新增任务线”提示：仅在 `can_add_task_line` 时出现。
- Peer（同侪类）
  - 给与中小额灵感、开卡奖励或特质建议（购卡/特质的提示或折扣事件，MVP先用 grant_inspiration）。
- Flavor（风味类）
  - 纯文本+小数值奖励（灵感+10~20），无结构影响，作为回退与“上限已满”的降级路径。

---

#### 5) 持久化与冷却
持久化位置：`state.persistent`
- 事件冷却表：`meeting_event_cooldowns: Dict[str,int]`（事件id → 距离可用还需的会议次数）
- 已出现计数：`meeting_event_seen_counts: Dict[str,int]`（事件id → 已出现次数）
- 本次会话回合：`meeting_session_turn: int`
- 免费升级剩余：`meeting_free_upgrade_left: int`
- 待新增任务线标记：`meeting_pending_add_line: bool`

冷却更新策略（每次选中的事件 e）：
1. `seen_counts[e.id] += 1`
2. 若定义 `cooldown > 0`，则设置 `cooldowns[e.id] = cooldown + 1`，并在下次会议 `open()` 时全体 `-1`（最低0）。

---

#### 6) 示例（与当前MVP对齐）
1) 事件：导师检查—继续保持
- 条件：
  - `any_of: [upgraded_cards_ge: 1, inspiration_ge: 80]`
  - `requires_can_add_line: False`
- 选项：
  - “继续保持（灵感+20）” → `grant_inspiration: +20`
- 冷却：`cooldown=1`（下一次会议不再出现）

2) 事件：导师检查—承诺改进
- 条件：
  - `all_of: [inspiration_le: 50]`
- 选项：
  - “立flag（下次达标灵感+40，占位）” → 先不加，记录 `meeting_flag_promise=True`（未来接入）
- 冷却：`cooldown=1`

3) 事件：导师建议—新增任务线
- 条件：
  - `requires_can_add_line: True`
- 选项：
  - “好的” → `defer_add_task_line: {}`（返回战役后新增一条任务线）
- 冷却：`cooldown=2`

4) 风味：咖啡与灵感
- 条件：无
- 选项：
  - “再来一杯（灵感+15）” → `grant_inspiration: +15`
  - “算了（无变化）” → `grant_inspiration: 0`
- 冷却：0

---

#### 7) 流程集成（当前实现与待办）
- 已实现
  - 事件对话UI（`MeetingEventModal`）；
  - 选择后应用基础效果（灵感变化、待新增任务线标记）；
  - 返回战役时新增任务线（尊重 `MAX_TASK_LINES` 上限）。
- 待办（下一步）
  - 在 `MeetingService` 引入条件编译器（将 Condition DSL 映射到当前可用的状态查询）；
  - 扩展 `meeting_event_templates.py` 为“数据+条件”的集合；
  - 冷却与 seen_counts 的读写与衰减；
  - 真正的“进度评分”信号与 mentor 类事件的精准分支；
  - 单测：条件编译器、冷却衰减、once_per_run、回退策略。

---

#### 8) 测试建议（最小集）
- 过滤与回退：
  - 当所有 mentor/peer 被条件或冷却剔除时，必回退到 flavor。
- 上限与降级：
  - `requires_can_add_line=True` 的事件在达到 `MAX_TASK_LINES` 后不能入选； flavor 替代出现。
- 效果应用：
  - `grant_inspiration` 正确累计；
  - `defer_add_task_line` 正确在战役返回时落地（已有测试）。
- 冷却与计数：
  - 选择某事件后 `seen_counts` 增加且 `cooldowns` 生效；下一次会议不应再次出现。

---

#### 9) 版本化与演进
- v0（当前）：硬编码模板 + 轻量条件/效果；核心路径稳定、可玩。
- v1：抽象 Condition/Effect 编译器；事件池数据化（JSON/py结构化）；引入冷却/计数持久化。
- v2：引入“进度评分”与真实 mentor 分支；事件线/剧情多段式；数据驱动权重动态调整。



