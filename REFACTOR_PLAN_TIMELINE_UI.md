# 游戏玩法重构计划：动态时间线与忽视度系统

本文档旨在记录并指导下一阶段的核心玩法重构工作。我们将分两个主要阶段来实现两个新的核心机制。

---

## 阶段一：实现"横向时间线推进"

**核心玩法**：将每个轨道改造为一条"传送带"。玩家只能选择每条轨道最左侧的"当前"节点。选择后，该节点被消耗，轨道向前推进一格，揭示下一个节点。

**目标**：将玩家的决策焦点从"多选一"转变为"在几个关键选项中权衡"。

### 步骤1：领域层 (Domain)

-   **文件**: `contexts/campaign/domain/track.py`
-   **`Track` 类**:
    -   [ ] 添加新属性 `current_node_index: int = 0`，用于追踪当前节点的索引。
    -   [ ] 添加新方法 `get_current_node() -> Node`，返回 `self.nodes[self.current_node_index]`。如果索引超出范围，可以返回 `None`。
    -   [ ] 添加新方法 `advance_to_next_node()`，将 `current_node_index` 的值加一。

### 步骤2：应用层 (Application)

-   **文件**: `contexts/campaign/application/campaign_service.py`
-   **`CampaignService` 类**:
    -   [ ] 修改方法签名，从 `select_node(self, track_id: str, node_id: str)` 变为 `select_node(self, track_id: str)`。
    -   [ ] 重写 `select_node` 内部逻辑：
        1.  通过 `track_id` 找到 `Track` 对象。
        2.  调用 `track.get_current_node()` 获取当前节点。
        3.  执行节点逻辑: `node.execute(self.game)`。
        4.  推进轨道: `track.advance_to_next_node()`。
        5.  更新全局DDL状态: `self.campaign_map.advance_time()`。

### 步骤3：表现层 (Presentation)

-   **文件**: `contexts/campaign/context.py`
-   **`CampaignContext` 类**:
    -   [ ] 重写 `_build_ui` 方法：不再循环所有节点，而是循环所有轨道 (`track in map_dto.tracks`)，并只为每个轨道的"当前节点"创建一个按钮。
    -   [ ] 修改 `handle_event` 方法：当按钮被点击时，获取其 `track_id` 并调用新的 `campaign_service.select_node(track_id)`。
    -   [ ] (可选) 在 `render` 方法中，可以在当前节点右侧绘制后续节点的缩略图或名称，以增强"传送带"的视觉效果。

---

## 阶段二：实现"动态轨道排序 (忽视度系统)"

**核心玩法**：为每条轨道引入"忽视度"。当玩家选择一条轨道时，其他所有轨道的忽视度会增加。忽视度最高的轨道会自动"浮"到屏幕顶端，在视觉上强调其紧迫性。

**目标**：创造"按下葫芦浮起瓢"的博士生困境，迫使玩家进行长线资源和注意力管理。

### 步骤1：领域层 (Domain)

-   **文件**: `contexts/campaign/domain/track.py`
    -   [ ] **`Track` 类**: 添加新属性 `neglect_level: int = 0`。
-   **文件**: `contexts/campaign/domain/campaign_map.py`
    -   [ ] **`CampaignMap` 类**: 添加核心方法 `update_neglect_and_sort(self, chosen_track_id: str)`。
        -   **逻辑**: 遍历所有轨道。对于被选择的轨道，`neglect_level` 重置为0；对于所有其他轨道，`neglect_level` 加一。
        -   **排序**: 在更新完所有忽视度后，根据 `neglect_level` 对 `self.tracks` 列表进行降序排序。

### 步骤2：应用层 (Application)

-   **文件**: `contexts/campaign/application/campaign_service.py`
    -   [ ] **`CampaignService` 类**: 在 `select_node` 方法的逻辑末尾，增加对 `self.campaign_map.update_neglect_and_sort(track_id)` 的调用。
-   **文件**: `contexts/campaign/application/dtos.py`
    -   [ ] **`TrackDTO`**: 添加新字段 `neglect_level: int`，以便将此信息传递给UI。

### 步骤3：表现层 (Presentation)

-   **文件**: `contexts/campaign/context.py`
    -   [ ] **`CampaignContext` 类**:
        -   **几乎无需改动！** `_build_ui` 方法会自然地按照DTO中已排好序的轨道列表从上到下进行渲染，自动实现"浮动"效果。
        -   [ ] (可选) 可以在渲染轨道时，将 `track.neglect_level` 的数值显示出来，为玩家提供更明确的反馈。

---
**结论**: 该计划将分两步，清晰地实现两个核心玩法。我们将优先完成第一阶段，为新的交互模式奠定基础。 