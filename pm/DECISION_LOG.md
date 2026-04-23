# 决策日志（最小版）

## 目标

记录关键项目决策，让进度、取舍与回滚路径保持清晰。

## 何时新增记录

出现以下任一情况时新增一条：

1. 范围变更（里程碑内容增加或删除）。
2. 技术方向变更（引擎/工具链/流程）。
3. 删除策略出现例外（`P0/P1` 清理）。
4. 排期变化（里程碑延迟超过 1 周）。

## 编号与状态

- 编号格式：`DL-YYYYMMDD-XX`
- 状态取值：`Proposed` | `Accepted` | `Rejected` | `Superseded` | `Reverted`

## 记录模板（可复制）

```md
### [DL-YYYYMMDD-XX] <简短标题>

- 日期：YYYY-MM-DD
- 负责人：<name>
- 状态：Proposed/Accepted/Rejected/Superseded/Reverted
- 关联：<issue/pr/commit/doc links>

#### 背景
当前要解决的具体问题是什么？

#### 决策
我们具体选择了什么？

#### 人类工作量影响（核心）
- 减少的人类工时：
- 增加的人类工时：
- 对关键路径的变化：

#### AI 工作量假设
哪些部分交给 AI，哪些仍必须人工完成？

#### 备选方案
1. 方案A：
2. 方案B：

#### 风险与触发信号
- 风险1：
- 触发信号：

#### 验证计划
- 成功指标：
- 检查日期：

#### 回滚方案
若该决策失败，如何安全撤销？

#### 后续动作
下一步的具体动作与负责人。
```

## 初始记录

### [DL-20260223-01] 清理前先落地最小 PM 治理

- 日期：2026-02-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/pm/DELETE_POLICY.md`

#### 背景
需要清理废弃代码，但若缺少统一流程，删除风险较高。

#### 决策
先建立最小治理文档，再按批次执行删除并记录可回滚点。

#### 人类工作量影响（核心）
- 减少的人类工时：降低清理阶段审查与回滚沟通成本。
- 增加的人类工时：前期需要少量文档搭建时间。
- 对关键路径的变化：清理任务可更安全地并行推进。

#### AI 工作量假设
AI 负责候选清单与补丁草案；人工负责风险定级与最终删除决策。

#### 备选方案
1. 不设策略直接清理。
2. 先做完整重型 PM 系统再开始动作。

#### 风险与触发信号
- 风险：团队执行时不遵守策略。
- 触发信号：删除 commit 缺少测试证据或缺少日志记录。

#### 验证计划
- 成功指标：每个删除批次都包含测试、回滚哈希和决策记录。
- 检查日期：每周一次。

#### 回滚方案
回滚该删除批次 commit，并将候选项降级为 `P1/P0` 待人工复核。

#### 后续动作
先产出第一版删除候选清单，再执行一批 `P2` 清理。

### [DL-20260223-02] 执行首批 P2 清理（examples + robust 遗留）

- 日期：2026-02-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/pm/DELETE_POLICY.md`

#### 背景
用户确认 `linshi/` 作为日常尝试区保留，优先清理 `examples` 与 `robust_game_toolkit` 中低风险遗留项。

#### 决策
删除以下 `P2` 项：
1. `examples/stack_logger_example.py`
2. `robust_game_toolkit/rendering/**`（未被运行路径引用，且模块不完整）
3. `robust_game_toolkit/core/assets/fonts/SourceHanSans-Regular.otf`（实为 HTML 文件，非真实字体）

#### 人类工作量影响（核心）
- 减少的人类工时：降低目录噪音与后续误判成本，减少无效体积与审查干扰。
- 增加的人类工时：一次性引用检查和回归验证。
- 对关键路径的变化：不影响主流程开发，清理可持续推进。

#### AI 工作量假设
AI 负责引用扫描、候选筛选、删除执行和测试回报；人工负责删除范围确认与继续/停止决策。

#### 备选方案
1. 先不删，等功能冻结后统一清理。
2. 一次性清理 `robust_game_toolkit` 更多 0 引用模块。

#### 风险与触发信号
- 风险：存在未覆盖到的隐式导入路径。
- 触发信号：`pytest` 失败，或运行入口出现 ImportError/资源加载错误。

#### 验证计划
- 成功指标：`./.venv311/bin/python -m pytest -q` 通过（允许既有 warnings）。
- 检查日期：2026-02-23（已执行通过）。

#### 回滚方案
若后续发现回归，按本批次提交执行 `git revert <commit_hash>`；当前尚未提交，必要时可先从索引恢复。

#### 后续动作
继续做第二批 `P2` 候选评估，但保留 `linshi/`。

### [DL-20260223-03] 追加删除 robust 无引用大字体

- 日期：2026-02-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/pm/DELETE_POLICY.md`

#### 背景
`robust_game_toolkit` 体积较大，其中 `NotoSerifCJKsc.otf` 单文件约 53MB，且仓库内未检索到引用。

#### 决策
删除 `robust_game_toolkit/core/assets/fonts/NotoSerifCJKsc.otf`，并立即执行全量回归测试。

#### 人类工作量影响（核心）
- 减少的人类工时：降低仓库体积与后续同步/审查负担。
- 增加的人类工时：一次额外验证测试。
- 对关键路径的变化：不影响主功能开发节奏。

#### AI 工作量假设
AI 执行引用检查、删除和回归测试；人工只做删除边界确认。

#### 备选方案
1. 暂不删除，等发布前统一压缩。
2. 进一步清理 `robust_game_toolkit` 的低引用模块。

#### 风险与触发信号
- 风险：存在未覆盖的动态路径引用字体文件。
- 触发信号：运行期字体加载失败或 UI 字体回退异常。

#### 验证计划
- 成功指标：`./.venv311/bin/python -m pytest -q` 通过（允许既有 warning）。
- 检查日期：2026-02-23（已通过）。

#### 回滚方案
提交后使用 `git revert <commit_hash>`；未提交阶段可恢复暂存区。

#### 后续动作
继续按 `P2` 规则评估 `robust_game_toolkit/core` 内 0 引用模块，逐批处理。

### [DL-20260223-04] 清理 robust 低引用诊断与打包遗留

- 日期：2026-02-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/pm/DELETE_POLICY.md`

#### 背景
在前两批清理后，`robust_game_toolkit` 仍存在一组低价值遗留文件：本地打包脚本、未接入的诊断模块、未引用主题文件。

#### 决策
删除以下 `P2` 文件：
1. `robust_game_toolkit/setup.py`
2. `robust_game_toolkit/core/diagnostics.py`
3. `robust_game_toolkit/core/constants/diagnostics.py`
4. `robust_game_toolkit/core/assets/theme.json`

#### 人类工作量影响（核心）
- 减少的人类工时：减少目录噪音和误判成本，降低后续维护负担。
- 增加的人类工时：一次额外引用核查与回归测试。
- 对关键路径的变化：不影响主流程开发与测试链路。

#### AI 工作量假设
AI 负责扫描引用、执行删除、回归测试；人工负责最终删除边界确认。

#### 备选方案
1. 暂缓删除，待版本冻结统一清理。
2. 一次性清空 `robust_game_toolkit/core` 的所有低引用模块。

#### 风险与触发信号
- 风险：存在未覆盖到的隐式引用或手工脚本依赖。
- 触发信号：运行期 ImportError 或资源加载失败。

#### 验证计划
- 成功指标：`./.venv311/bin/python -m pytest -q` 通过（允许既有 warning）。
- 检查日期：2026-02-23（已通过）。

#### 回滚方案
提交后按批次 commit 进行 `git revert <commit_hash>`；未提交阶段可直接从索引恢复。

#### 后续动作
下一步仅评估 `robust_game_toolkit/core` 中“外部 0 引用且内部低依赖”的模块，不动主链路模块。

### [DL-20260314-01] 项目长期方向采用 pygame 内部 Godot 化

- 日期：2026-03-14
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/CURRENT_DIRECTION.md`

#### 背景
项目已经出现 Godot-like runtime UI 和 retained widget 方向，但是否要全面迁移 Godot 仍然需要明确，以避免后续讨论和实现不断摇摆。

#### 决策
长期方向明确为“pygame 的 Godot 化”：
- 保留现有 pygame 项目与运行时入口
- 优先推进节点化、runtime UI、清晰边界和可迁移架构
- 当前不做一次性 Godot 全量迁移

#### 人类工作量影响（核心）
- 减少的人类工时：减少架构讨论反复横跳和过早迁移带来的返工。
- 增加的人类工时：需要在一段时间内维护 mixed-mode 过渡状态和边界文档。
- 对关键路径的变化：允许内容开发和架构演进并行，不把关键路径押注到引擎重写。

#### AI 工作量假设
AI 适合帮助整理迁移边界、文档方向和过渡实现；人工仍负责决定哪些模块值得先迁移、哪些 mixed-mode 兼容层暂时保留。

#### 备选方案
1. 立即全面迁移 Godot。
2. 完全维持当前 pygame 结构，不主动做 Godot-like 架构收口。

#### 风险与触发信号
- 风险：mixed-mode 过渡时间过长，形成长期兼容壳。
- 触发信号：新 UI 交互长期无法脱离 legacy background 路径，或方向文档开始与实现持续脱节。

#### 验证计划
- 成功指标：新会话仅阅读核心记忆文档时，能稳定回答“长期方向是 pygame 的 Godot 化，而不是全面迁移 Godot”。
- 检查日期：每周回顾时检查一次。

#### 回滚方案
若该方向不再成立，在决策日志中显式新增替代决策，并同步更新 `CURRENT_DIRECTION.md` 与相关架构文档，而不是通过聊天口头覆盖。

#### 后续动作
把该方向写入核心记忆入口，并在后续 UI/架构设计讨论中默认以此为前提。

### [DL-20260314-02] 项目记忆继续采用轻量文件化方案

- 日期：2026-03-14
- 负责人：Team
- 状态：Accepted
- 关联：`AGENTS.md`, `docs/development/PROJECT_MEMORY_RULES.md`

#### 背景
Codex 协作需要稳定恢复项目方向和开发历史，但若过早引入重型平台、复杂数据库或游戏内 memory 机制，会增加维护成本并稀释真正高价值的信息。

#### 决策
项目记忆 V1 继续采用 Markdown 文件作为 source of truth：
- 长期方向与稳定规则写入 `docs/development/`
- 决策写入 `docs/pm/DECISION_LOG.md`
- 每日短期进展写入 `docs/logs/daily/`
- 新增 `docs/logs/weekly/` 作为压缩层
- Hybrid search 仅作为后续可选检索层，不是 V1 前提

#### 人类工作量影响（核心）
- 减少的人类工时：避免维护一套和文档并行的额外记忆平台。
- 增加的人类工时：需要持续维护短 daily log 和 weekly summary。
- 对关键路径的变化：把记忆维护成本保持在低水平，不影响主要开发节奏。

#### AI 工作量假设
AI 可以帮助生成 weekly summary 草稿、晋升建议和方向文档更新；人工仍保留对长期文档晋升的最终确认权。

#### 备选方案
1. 立即引入数据库或向量库作为主存储。
2. 完全不补记忆压缩层，只依赖 daily log 和聊天。

#### 风险与触发信号
- 风险：weekly summary 不维护时，旧 daily log 会再次堆积成噪音。
- 触发信号：Codex 需要频繁翻多份旧日志才能回答近期方向，或长期方向开始分散在多个文件中相互冲突。

#### 验证计划
- 成功指标：最近 7 天的工作可以通过 daily + weekly 快速恢复；长期方向可以通过少量核心文件稳定读出。
- 检查日期：每周回顾时检查一次。

#### 回滚方案
若轻量文件化方案无法满足恢复质量，再显式引入后续 Phase 2 检索层；在此之前不废弃现有 Markdown 记忆源。

#### 后续动作
补齐 `CURRENT_DIRECTION.md`、weekly summary 目录、读取规则和轻量自动化脚本。

### [DL-20260423-01] Campaign Forced Event 采用窄版长期方案

- 日期：2026-04-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md`,
  `docs/development/CAMPAIGN_TASK_AREA_TRIGGER_SURFACE_V1.md`,
  `docs/development/CAMPAIGN_LIFECYCLE_MACHINE_V1.md`

#### 背景
Campaign 的 forced event 已经进入生产生命周期路径，但当前实现仍然偏临时：
- 触发检测、pending 状态和展示打开还混在
  `CampaignTriggerReactionService` 中
- 事件 payload 仍以原始 `dict` 形态存在
- 展示暂时复用了 `gossip_modal`
- 虽然 `FORCED_EVENT_GATE` 已经存在，但 forced event 还没有一个真正稳定的
  runtime owner

如果继续在当前形态上叠加更多 forced event，后续很容易再次形成一套隐式、
散落、AI 不友好的中断逻辑。

#### 决策
Campaign forced event 从现在开始采用“窄版长期方案”，而不是：
- 保持现状继续堆临时逻辑
- 立即升级为 reward/meeting/forced-event 的统一中断平台

本次接受的长期方向是：
1. trigger 检测继续走 trigger surface 路径
2. pending/active forced event 要收口到专门 runtime owner
3. presentation 要收口到专门 presenter seam
4. `TURN_INTERRUPTS -> FORCED_EVENT_GATE` 保持为唯一强制进入口
5. 当前阶段不扩大到统一 interrupt framework，不重开 `view` 大重构

#### 人类工作量影响（核心）
- 减少的人类工时：后续新增 forced event 时，不需要再重新讨论“挂在
  lifecycle hook / raw domain event / 直接 modal 打开”的路径选择。
- 增加的人类工时：需要先补一层窄的 forced-event runtime/presenter 收口，
  并补一轮 gate/resolution 测试。
- 对关键路径的变化：把 forced event 的后续开发从“继续临时拼接”切到
  “沿既定切片稳定推进”，更适合自动化连续执行。

#### AI 工作量假设
AI 适合持续完成以下串行切片：
- 显式模型与 runtime owner
- presenter seam 抽离
- gate/resolution 契约收紧
- 首个扩展示例与 guardrail

人工仍保留这些决策权：
- 是否需要新的产品级 forced-event UI 形态
- 是否需要把 reward/meeting/forced-event 统一为更大平台
- 多事件合并/优先级规则是否要做产品层改动

#### 备选方案
1. 维持当前 forced event 的最小可工作实现，等后续需求更多再处理。
2. 立即做完整 interrupt family 平台化，把 reward/meeting/forced-event 一次统一。

#### 风险与触发信号
- 风险：如果切片失控，forced event 收口工作可能被带成 broader interrupt/UI
  重构。
- 风险：如果过早要求最终 UI 形态，会把当前窄方案重新放大。
- 触发信号：实现 forced event 时开始修改 `CampaignView`、reward gate、
  meeting prompt 主路径，或开始讨论 save schema 大迁移。

#### 验证计划
- 成功指标：
  - forced event 拥有独立 runtime owner
  - trigger reaction 不再直接依赖 `gossip_modal`
  - `FORCED_EVENT_GATE` 行为有显式测试覆盖
  - 后续新增 forced event 可以沿同一路径扩展
- 检查日期：每个切片提交后检查一次；完成 slice 3 后进行一次阶段回顾。

#### 回滚方案
若窄版长期方案被证明仍然无法控制复杂度，则在决策日志中显式追加新决策，
再评估是否升级到 broader interrupt framework。当前阶段不直接回退到
“继续保留临时 forced-event 形态”作为默认路线。

#### 后续动作
按 `docs/development/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md` 继续执行以下切片：
1. Slice 1：显式模型 + runtime owner
2. Slice 2：presenter seam 抽离
3. Slice 3：resolution/gate 契约收紧
4. Slice 4：首个扩展 guardrail
