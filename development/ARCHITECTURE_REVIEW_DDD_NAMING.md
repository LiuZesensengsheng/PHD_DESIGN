# 架构 / 命名 / DDD 评审（绝不延毕）

> 结论先行：项目已经具备“按业务上下文（bounded context）拆分”的雏形，`combat` 的 DDD 分层最接近目标；但入口与“Context/State”两套框架并存，导致命名与分层边界出现系统性不一致。建议先统一运行时状态机与生命周期接口，再收敛 `constants/` 的职责，最后补齐 `application` 层与端口/适配器（ports/adapters）。

## 当前仓库的真实运行架构（以代码为准）

- 目前“真正驱动游戏运行”的入口是 `run_campaign.py`，使用 `contexts/shared/game_state_machine.py` 的 `GameStateMachine + BaseState`。
- 旧的 `main.py` + `contexts/base_context.py` + `contexts/game_state_machine.py` 属于并行/遗留实现，与现有 `BaseState` 生命周期并不一致，容易造成误导与维护成本。

## 命名问题（高优先级）

### 1) `Context` vs `State`：术语不统一

- 实际运行：`MainMenuState / CampaignState / CombatState`（`BaseState`）
- 遗留命名：`BaseContext`、`Game.change_context(...)`、`contexts/game_state_machine.py` 的 `GameStateMachine`

建议：
- 选定一个术语作为“对外/对内都唯一的主架构名词”：
  - 若继续采用 `GameStateMachine`：统一称为 **State**（推荐，已经跑通）
  - 删除或显式标记弃用旧的 `Context` 体系（或迁移到 `BaseState`）

### 2) `constants/` 命名误导（“常量”实际承载了配置/枚举/UI布局/域概念）

现状：
- 存在 `constants/campaign_domain.py`、`constants/campaign_ui.py`、`constants/combat_domain.py` 等。

问题：
- `domain` 相关的概念放在全局 `constants/` 下，会让“领域模型归属哪个 bounded context”不清晰。
- `ui` 配置与玩法/规则常量混放，难以做边界检查（例如禁止 domain 层依赖 UI 常量）。

建议：
- 将 `constants/` 拆分为更语义化目录（不一定一步到位）：
  - `config/`：运行时可调参（分辨率、音量、开关等）
  - `ui_config/`：UI布局、主题开关、渲染参数
  - `contexts/<ctx>/domain/constants.py`：该上下文的领域常量/规则键（仅业务含义）
  - `contexts/<ctx>/presentation/ui_constants.py`：该上下文 UI 常量

### 3) 版本后缀命名：`player_v2.py`

问题：
- 在 DDD/长期维护里，类型/实体一般不建议用 `v2` 后缀长期存在（历史应由 git 承载）。

建议：
- 过渡期可以保留，但设一个“改名窗口”：稳定后把 `player_v2.py` 合并/重命名为 `player.py`。

## 分层是否合理？（与 DDD 的贴合度）

### 1) combat：分层较好（接近 DDD + ports/adapters）

优点：
- `contexts/combat/domain/` 比较“纯”，有 services、values、effects、enemies 等明显领域建模。
- 有 `infrastructure/`（数据校验、DTO、仓库/加载），并且测试覆盖相对多。
- 有 `scripts/validate_architecture.py` 试图约束 domain 违规写入（很加分）。

主要改进点：
- domain 仍会依赖全局 `constants.*` 做开关（例如能量彩池），建议逐步改为：
  - domain 内部 `config.py`（同 context 内）
  - 或通过 application 层注入（更 DDD 正统）

### 2) campaign：处于“State 作为 application + presentation 的大编排器”

现状：
- `CampaignState` 同时负责：
  - UI 事件处理（presentation）
  - 大量流程编排与服务组合（application）
  - 直接操作/持有领域数据（domain DTO / block 列表）

优点：
- 已经开始把逻辑抽到 `contexts/campaign/services/`（`TrackBlockService`、`EndTurnService` 等），这是往 application 层走的正确方向。

风险：
- `services/` 里如果出现大量 `pygame_gui`、UI widget 的创建/销毁，会导致 application/presentation 边界继续模糊。

建议：
- 明确 `contexts/campaign/services/` 的定位：
  - 如果它们是 **application services**：就尽量只处理“用例编排 + 领域调用 + 返回 ViewModel/命令”
  - UI widget 的创建/布局/呈现尽量集中在 `view.py`/`ui/`（presentation）

## 是否遵循 DDD？（结论）

整体：**部分遵循**，尤其 combat 很接近“轻量 DDD”；campaign 目前更像“传统游戏状态机 + 服务抽取”，还没完全落在 DDD 的四层（domain/application/infrastructure/presentation）边界上。

如果目标是“严格 DDD”，建议的演进路线：

1. **统一主入口与生命周期**：以 `run_campaign.py` + `BaseState` 为准；`main.py` 明确弃用或迁移。
2. **收敛 constants 的职责**：至少做到“UI 常量不被 domain 依赖”、“domain 常量归属到各自 context”。
3. **补齐 application 层**：把复杂流程（回合推进、奖励结算、meeting 触发、战斗路由）集中成可测试的 use-cases。
4. **端口/适配器化外部依赖**：音频、资源加载、存档、随机数等，通过接口隔离，让 domain 更纯、测试更稳。

## 立刻可做的三件小事（低风险/高收益）

1. 在 README 或 docs 中写清楚“正式入口是 `run_campaign.py`”，并标注 `main.py` 为 legacy。
2. 给 `scripts/validate_architecture.py` 增加规则：combat/campaign 的 `domain/` 禁止导入 `pygame`、`pygame_gui`、`constants.*ui*`。
3. 约定跨 context 依赖只能通过 `contexts/shared` 或 `shared_kernel` 的稳定接口（避免深层文件互相 import）。


