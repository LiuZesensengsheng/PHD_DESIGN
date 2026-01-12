# 测试策略（最小可维护版）

本项目当前目标：**让每一次合并都能被自动化测试快速兜住最核心的“跑得起来 + 核心规则不回归”**。

> 原则：不追求“测试很多”，追求“测试刚好卡住最贵的崩溃点”。

## 1. 测试分层（按收益排序）

### A. Domain 单元测试（最高 ROI）
- **定义**：不依赖 UI（pygame/pygame_gui）、不读真实文件、纯规则/状态机/数值逻辑。
- **目标**：保证战斗规则、能量系统、卡牌可用性、事件/状态机等不回归。
- **典型位置**：`tests/combat/`、`tests/campaign/` 中的大多数纯逻辑测试。

### B. Application/Service 用例测试（中 ROI）
- **定义**：调用 Service（如 Meeting/Track/ThesisMeta 等）走“用例链路”，允许依赖少量内存仓储/假对象。
- **目标**：保证“按钮能点、流程能跑、状态能回到 CAMPAIGN”等关键路径。
- **典型位置**：`tests/campaign/test_meeting_service_core.py`、`tests/campaign/test_campaign_vertical_slice.py` 等。

### C. Headless E2E（兜底）
- **定义**：不真实开窗口，但会走到 UI/状态机的一些集成逻辑（可能触发 pygame_gui warnings）。
- **目标**：保证“最小可玩闭环”不会碎。
- **典型位置**：`tests/shared/test_e2e_headless_dialogue_to_campaign.py`、`tests/test_campaign_combat_integration.py` 等。

### D. 手动 Smoke（发布前）
- **定义**：本地跑 `run_campaign.py`，按脚本点几下。
- **目标**：验证 UI 布局、字体、视觉警告、交互体验（自动化不擅长的部分）。

## 2. 变更类型 → 必跑测试清单（合并前 checklist）

### 改战斗域（卡牌/能量/敌人/效果）
- 必跑：
  - `python -m pytest tests/combat -q`
  - `python -m pytest tests/test_campaign_combat_integration.py -q`

### 改战役域（Campaign/Track/Meeting/奖励/事件）
- 必跑：
  - `python -m pytest tests/campaign -q`
  - `python -m pytest tests/test_state_machine_minimal.py -q`

### 改 Shared Kernel（例如 `shared_kernel/color.py` 这种“全局类型”）
- 必跑：
  - `python -m pytest -q`（全量）

### 改 UI（`theme.json`、view/layout、字体）
- 必跑：
  - `python -m pytest tests/test_ui_layout_json.py -q`
  - `python -m pytest tests/test_ui_icon_paths.py -q`
  - 手动 smoke：至少进一次 IDEALS → CAMPAIGN → DECK → 回 CAMPAIGN

## 3. Warnings 策略（先管理噪音，再谈清零）

当前全量 pytest 已知会出现 pygame_gui 相关 warnings（例如字体未预加载、Label Rect 太小）。

约定：
- **P0（必须清零）**：任何 warning 代表逻辑错误/数据损坏/潜在崩溃（例如 Deprecation 导致未来版本崩）。
- **P1（尽量清零）**：会淹没日志、影响定位问题的 UI warnings（字体、布局）。
- **P2（可接受）**：第三方库的偶发噪音，但要在此文档中登记来源与原因。

登记位置：本文件“已知 warnings 列表”。

### 已知 warnings 列表
- **pygame_gui 字体预加载提示**：建议未来在 headless 测试初始化时集中 preload（可选优化）。
- **Label Rect 太小**：属于 UI 布局问题；目前不阻断合并，但建议统一处理（例如统一 label 宽度/自动换行/缩放策略）。

## 4. 覆盖矩阵（我们当前“有/缺”的关键回归点）

### 已覆盖（当前 tests 已在兜）
- **战斗能量/颜色支付/可出牌**：`tests/combat/test_energy_*`, `test_color_and_cost.py`, `test_playability_*`
- **战斗关键流程**：`test_enemy_execution_flow.py`, `test_combat_phase_machine.py`
- **Campaign 基础 guard / input lock**：`tests/campaign/test_campaign_guards.py`, `tests/test_state_machine_minimal.py`
- **Meeting 核心逻辑**：`tests/campaign/test_meeting_service_core.py`, `test_meeting_events_branching.py`

### 建议补齐（下一批高 ROI）
- **合并回归用例：Deck ↔ Campaign 往返**（本次 master 合并改动过 `contexts/deck/state.py`）
- **Combat 结束 → Campaign 奖励 → 解锁输入**（防止“卡死感”回归）
- **Meeting：导师分支的 2-step modal 流程（升级/删除）**（可以先做 Service 层测试，不碰 UI）


