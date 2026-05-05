# 战役UI状态机与存档契约（Architecture Overview）

## 1. 唯一入口与状态机链路

- 入口：`run_campaign.py → GameStateMachine`
- 状态：`MAIN_MENU / CAMPAIGN / DIALOGUE / EVENT / COMBAT / LOADING`
- 原则：各 State 并列，互不直接依赖；切换由状态机驱动。

## 2. 数据模型（Domain DTO）

- `BlockDTO`（唯一战役块模型）：
  - 字段：`id, block_type, track_index, start_turn, duration, track_span, tags`
  - 方法：`to_dict()/from_dict()`（纯JSON，跨分辨率/平台安全）
- View 只读 DTO；State 维护 List[BlockDTO] 与业务逻辑。

## 3. 责任边界

- `CampaignState`
  - 维护回合、块列表、路由队列；产生“请求 payload”给子状态
  - 接收子状态 `result` 并更新战役数据（移除块、发奖励等）
  - 提供 `to_snapshot()/from_snapshot()`（存档友好）
- `CampaignView`
  - 布局/缩放/渲染/贴图缓存；禁止渲染期加载IO
  - UI原始事件→语义调用（`on_end_turn()`、`on_click_block(id)`）
- 其它 State（Dialogue/Event/Combat/Loading）
  - 消费请求 payload，渲染与结算，回写 `result`

## 4. 事件与数据流

- UI事件 → View命中判定 → 调用 State 语义方法 → State 更新 DTO → 下一帧 View 渲染
- CAMPAIGN → 子状态：通过 persistent 传 `*_request`（如 encounter_id/seed/player_snapshot）
- 子状态 → CAMPAIGN：回写 `result`（outcome/rewards/污染等）+ `event_resolved=True`

## 5. 存档（Save/Load）

- SaveManager（`contexts/shared/domain/save_manager.py`）：JSON 存档/读档
- 存档结构：
```json
{
  "meta": {"version": 1, "timestamp": 0, "current_state": "CAMPAIGN", "rng_seed": 12345},
  "campaign": {"current_turn": 3, "blocks": [], "pending_block_id": 10, "route_queue": ["EVENT"]},
  "dialogue": {},
  "event": {},
  "combat": {},
  "player": {"hp": 60, "deck": [], "relics": [], "resources": {}}
}
```
- 各 State 提供 `to_snapshot()/from_snapshot()`；状态机聚合/还原整局快照。

## 6. 解耦与性能

- State 不引用像素常量；回合→像素换算在 View
- 资源初始化加载、缩放缓存（key=(name,w,h)）避免每帧 `smoothscale`
- 统一 logging；随机性注入 `rng_seed` 以支持可复现

### 6.1 渲染护栏（RenderGuard）

- 目的：防止在非绘制阶段误调用 `pygame.draw.*`/`blit` 类渲染API。
- 用法：状态机 `draw()` 包裹 `with RenderGuard.state_draw():`；UI 绘制包裹 `with RenderGuard.ui_draw():`。
- 开关：默认仅在上下文中启用；环境变量 `RENDER_GUARD_ENABLED=0` 可全局关闭（如发行版）。

### 6.2 契约键名（Contracts）

统一在 `contexts/shared/domain/contracts.py` 定义：

```
PENDING_BLOCK_ID, ROUTE_QUEUE, EVENT_RESOLVED, RESOLVED_BLOCK_ID,
START_COMBAT_ENCOUNTER_ID, REWARD_ID
```

跨状态传参与回写统一使用上述常量，避免拼写不一致。

## 7. 待办路线图（已开始）

- [x] 引入 `BlockDTO` 与统一持久化
- [x] `CampaignView` 兼容 DTO，加入缩放缓存
- [x] `SaveManager` 基础实现
- [ ] 为 `GameStateMachine` 增加 `save()/load()` 接口
- [ ] 各 State 的 `to_snapshot()/from_snapshot()` 完整化
- [ ] 事件路由契约键名统一（`*_request`/`result`）

> 本文档将随实现进度迭代更新，始终作为架构与协作的“单一事实来源（SSOT）”。

## 8. UI 包结构（建议拆分）

```
contexts/campaign/ui/
  facade.py           # 对外入口（保持与 CampaignState 接口稳定）
  layout.py           # 缩放、几何、坐标换算
  assets.py           # 资源加载与回退、缩放缓存条目创建
  block_renderer.py   # 甘特块渲染（文本、边框、高亮）
  chrome.py           # 顶部状态栏、进度条、图例、按钮
  effects.py          # 点击涟漪、行动线、雾层等
  events_adapter.py   # 原始事件→语义事件的适配
  cache.py            #（可选）缓存与淘汰策略
```

迁移顺序：`facade + layout + assets` → `block_renderer` → `events_adapter/chrome`，每步保持 `CampaignState` 接口不变。
