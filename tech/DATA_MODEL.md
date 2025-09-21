# 游戏核心数据模型 (Core Data Model)

本文档定义了《绝不延毕》游戏中需要被持久化（存档）的核心数据结构。它是游戏状态的完整快照，也是所有游戏系统交互的“单一事实来源”。

---

### 1. 玩家核心状态 (PlayerState)
*描述：玩家瞬时、易变的核心资源。*
- **`pressure`**: `int` - 当前压力值。
- **`max_pressure`**: `int` - 最大压力值。
- **`sanity`**: `int` - 当前理智值。
- **`inspiration`**: `int` - 灵感，用于购买物品，基本等价于金钱。

---

### 2. 玩家核心属性 (PlayerAttributes)
*描述：玩家通过游戏进程缓慢培养的“三位一体”核心能力。*
- **`sanity`**: `int` - [心智光谱]值，衡量精神状态，是"里世界"的体现。
- **`academic_depth`**: `int` - [学术深度]值，理论学者的特殊数值。
- **`rigor_exp`**: `int` - [严谨]经验值，代表学术硬实力。
- **`ideological_depth_exp`**: `int` - [思想深度]经验值，代表学术洞察力与创造力。

---

### 3. 社会关系图谱 (SocialGraph)
*描述：玩家与NPC之间的关系量化。*
- **`senior_brother_relationship`**: `int` - [师兄关系]值。
- **`mentor_relationship`**: `int` - [导师关系]值。
- *... (可扩展至其他NPC)*

---

### 4. 项目状态 (ProjectState)
*描述：核心的 m/n 系统，驱动答辩等关键事件。*
- **`modules`**: `dict`
  - `key`: `string` (模块ID, e.g., "backend", "frontend")
  - `value`: `object`
    - `m`: `int` (已完成工作量)
    - `n`: `int` (总工作量)
- **示例**:
  ```json
  "project_status": {
      "module_A_backend": {"m": 15, "n": 20},
      "module_B_frontend": {"m": 5, "n": 30},
      "module_C_algorithm": {"m": 0, "n": 25},
      "module_D_docs": {"m": 10, "n": 10}
  }
  ```

---

### 5. 持有物 (Inventory)
*描述：玩家拥有的物品。*
- **`key_items`**: `list[string]` - 关键故事物品ID列表 (e.g., `["senior_brother_notes"]`)。
- **`consumables`**: `dict` - 消耗品及其数量 (e.g., `{"instant_relief_pills": 2}`).

---

### 6. 特质与状态 (Traits & Statuses)
*描述：影响玩家能力的永久性特质和临时性状态。*
- **`traits`**: `list[string]` - 玩家获得的永久特质ID列表 (e.g., `["academic_backbone", "slacking_fish"]`)。
- **`statuses`**: `list[object]` - 玩家当前的临时状态列表。
  - `name`: `string` (状态ID, e.g., "client_trust")
  - `duration`: `int` (剩余持续时间，单位：天)

---

### 7. 事件历史 (EventHistory)
*描述：记录玩家经历，是“图论”式事件触发系统的基石。*
- **`completed_events`**: `list[string]` - 已完成事件的ID列表 (e.g., `["event_ask_senior_about_project", "event_late_night_snack"]`)。

---

### 8. 战斗卡组 (CardDeck)
*描述：玩家拥有的所有卡牌。*
- **`deck`**: `list[string]` - 玩家卡组中所有卡牌的ID列表。

---

### 9. 全局游戏状态 (GameState)
*描述：宏观游戏进程的记录。*
- **`current_day`**: `int` - 游戏进行的总天数。
- **`current_questline`**: `string` - 当前主线任务的ID (e.g., "QUESTLINE_TUTORIAL_PROJECT")。
- **`current_node_id`**: `string` - 当前任务链所处的节点ID (e.g., "NODE_2_INTERACTIONS")。
