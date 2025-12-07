## 甘特图：DDL 贪吃蛇规则（屏幕语义版）

> 目标：让 DDL 在**屏幕上**每回合只前进一格，但在“今天”线附近仍然表现为「一步一步逼近并吃掉前方工作量」。

---

### 一、坐标系与前提

- 逻辑时间：
  - 以整数回合作为时间轴，记 `today = floor(current_turn)`。
  - 每次结束回合：`current_turn += 1`。
- 屏幕映射（简化）：
  - 对任意块：
    - 若 `start_turn <= today`：视为**已到达今天**，在屏幕上“钉住”，不再左移。
    - 若 `start_turn > today`：是“未来块”，在屏幕上以 1 格 / 回合的速度向左移动。
- DDL 特性：
  - `block_type = ddl`。
  - 不再直接修改 `start_turn` 做“蛇形位移”，而是完全依赖 `current_turn` 推进在屏幕上的移动。

---

### 二、DDL 贪吃蛇的 5 个 Case

以下规则按“同一轨道上、按 `start_turn` 排序后，DDL 左侧最近的块”为 `prev` 来描述。

记：
- `prev_start = prev.start_turn`
- `prev_dur = prev.duration`
- `ddl_start = ddl.start_turn`
- `today = int(current_turn)`

#### Case 1：左侧没有块

- 条件：
  - 该轨道上 DDL 是第一块（左侧无 `prev`）。
- 行为：
  - 本回合**不修改几何**（不改 `start_turn` / `duration`）。
  - 仅依赖 `current_turn += 1` 让 DDL 在屏幕上以 1 格 / 回合向左移动。

#### Case 2：左侧有块，但尚未到达今天 / 尚未贴边

- 条件：
  - 存在 `prev`，且满足：
    - `prev_start > today`（前块也是未来块，尚未怼到今天），**或**
    - `prev_start <= today` 但 **本回合不满足贴边条件**（见 Case 3）。
- 行为：
  - 视为“追赶阶段”：
    - 不修改任何块的 `start_turn` / `duration`。
    - 随着 `today` 增长，DDL 在屏幕上逐步靠近 `prev`，速度均为 1 格 / 回合。

#### Case 3：本回合刚好贴上前块右侧（发生吃一格）

- 条件（全部满足）：
  1. `prev_start <= today`：前块已经怼到今天，在屏幕上固定不动。
  2. `ddl_start > today`：DDL 仍在未来区域，可以继续前进。
  3. **贴边条件（屏幕几何）**：
     - 前块在屏幕上的右缘为：`grid_x + prev_dur * unit`；
     - DDL 在屏幕上的左缘为：`grid_x + (ddl_start - today) * unit`；
     - 因此，两者“首尾相接”的充要条件为：
       \[
       ddl\_start - today = prev\_dur
       \]
       即实现中使用：
       ```python
       int(round(ddl_start - today)) == int(prev_dur)
       ```

- 行为（吃一格）：
  - 前块：
    - `prev.duration -= 1`；
    - 若新的 `duration <= 0`，直接从 `_blocks` 中移除该块（被完全吃掉）。
  - DDL：
    - `ddl.duration += 1`；
    - `ddl.start_turn` **保持不变**（长度变化，由渲染层决定视觉上向左/向右扩展）。
  - 结果：
    - 屏幕上本回合两块仍然首尾相接；
    - 下一回合起，DDL 继续以 1 格 / 回合的速度逼近（若还有新的前块），长度已经变长 1 格。

#### Case 4：DDL 与前块在逻辑时间上已重叠（非法状态）

- 条件：
  - 逻辑区间存在交叉：`[prev_start, prev_start + prev_dur)` 与 `[ddl_start, ddl_start + ddl_dur)` 有真实交集。
- 行为：
  - 视为几何不变量被破坏的错误：
    - 由 `_assert_no_logical_overlap` 在 `resolve_fusion_and_stabilize` 完成后统一检查；
    - 检查条件：同一轨道上按 `start_turn` 排序后，若出现 `cur_start < prev_end` 则抛出 `AssertionError`。
  - 在开发期一旦出现该情况，直接 crash 并打印涉及的 block id 和区间，便于定位规则冲突。

#### Case 5：DDL 自身到达今天（停止贪吃）

- 条件：
  - `ddl_start <= today`。
- 行为：
  - 本回合以及之后均**不再对该 DDL 进行贪吃处理**：
    - 不再尝试吃前方块；
    - 不再修改 `duration` 或 `start_turn`。
  - 渲染上它也和普通任务块一样，钉在今天行动线的位置。

---

### 三、实现位置（代码参考）

- 服务：`contexts/campaign/services/track_block_service.py`
- 入口：
  - `TrackBlockService.resolve_fusion_and_stabilize()` → 首先调用 `_apply_ddl_snake_step()`，再执行常规融合与归一化。
  - `_apply_ddl_snake_step()` 内部：
    - 按轨道分组、按 `start_turn` 排序；
    - 对每条轨道的第一个 DDL 应用上述 Case 1–5 规则；
    - 每个逻辑回合、每条轨道最多处理一个 DDL（通过 `_ddl_snake_last_turn` 防重入）。

---

### 四、测试要点

1. **空白场景：不改几何**
   - 给定：`today=0`，轨道上有 `A[0,2)` 与 `DDL[5,7)`。
   - 预期：调用 `_apply_ddl_snake_step()` 后，二者的 `start_turn/duration` 均不变。

2. **贴边吃一格**
   - 给定：`today=2`，`prev=[0,2)`，`ddl_start = today + prev_dur = 4`，`ddl_dur=1`。
   - 预期：调用 `_apply_ddl_snake_step()` 后：
     - `prev.duration == 1`；
     - `ddl.duration == 2`；
     - 所有 `start_turn` 不变。

3. **DDL 到达今天后停止**
   - 给定：`ddl_start <= today`。
   - 预期：`_apply_ddl_snake_step()` 对该轨道不再做任何修改。


