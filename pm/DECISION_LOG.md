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
- 关联：`docs/development/campaign/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md`,
  `docs/development/campaign/CAMPAIGN_TASK_AREA_TRIGGER_SURFACE_V1.md`,
  `docs/development/campaign/CAMPAIGN_LIFECYCLE_MACHINE_V1.md`

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
按 `docs/development/campaign/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md` 继续执行以下切片：
1. Slice 1：显式模型 + runtime owner
2. Slice 2：presenter seam 抽离
3. Slice 3：resolution/gate 契约收紧
4. Slice 4：首个扩展 guardrail

### [DL-20260423-02] Combat 全域 Compat-Zero 采用 Engineering Zero 边界

- 日期：2026-04-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/combat/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`, `docs/development/CODEX_TASK_POOL.md`, `docs/logs/daily/2026-04-23.md`

#### 背景
combat 的 `runtime-mainline compat-zero` 已经完成，`CombatSession` 也已经成为 UI、headless、save/load 共用的 canonical runtime host。但这不等于 combat 全域兼容层已经清零。当前仍残留：

- `CombatModel` / MVC facade
- `CombatSession` 上的 underscore compat wrapper
- `CombatState -> turn_context` 字段桥
- 一批低价值 test/import shim
- save/schema backward-compat 路径
- 少量看起来像 compat、但可能应保留的 adapter

如果不先锁定边界，后续自动化很容易把：

- MVC 删除
- 字段桥收口
- save backward compatibility
- 红卡内容 bug
- 视觉/动画工作

混在同一条执行线上，导致 diff 噪音高、回滚困难、风险判断失真。

#### 决策
接受 `docs/development/combat/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 中推荐的决策包，定义本轮 combat 全域 compat-zero 为 **Engineering Zero**，具体为：

1. `D0 = Engineering zero`
2. `D1 = Delete CombatModel in this program`
3. `D2 = Staged collapse for turn_context bridge`
4. `D3 = Delete low-value test/import shims after migration`
5. `D4 = Keep save backward-compat for now`
6. `D5 = Treat adapter-like survivors as retained unless later re-decided`

由此锁定本轮默认自动化顺序：

1. `G1` 删除 MVC facade plane
2. `G2` 删除 `CombatSession` compat wrapper
3. `G3` 分阶段收掉 `state -> turn_context` 桥
4. `G4` 删除低价值 test/import shim
5. `G5` 只做 retained adapter review，不继续越界

并显式排除以下工作，不得混入本轮自动化主线：

- `tests/combat/test_json_red_cards.py` 的 red runtime/content failure 修复
- 动画 / 视频阻塞语义实现
- `combat_view` 行为或视觉改动
- save schema redesign

#### 人类工作量影响（核心）
- 减少的人类工时：减少每轮自动化前的边界重判、diff 解释和范围争议。
- 增加的人类工时：需要一次性接受更细粒度的 staged cleanup 决策，而不是笼统说“继续删兼容层”。
- 对关键路径的变化：把 combat compat cleanup 从一次性大重构改为可持续、可暂停、可自动化恢复的串行执行线。

#### AI 工作量假设
AI / automation 负责：

- 按 `G1-G4` 串行执行小步删除
- 运行聚焦验证包
- 更新今日日志与相关开发文档
- 在遇到越界风险时停止并报告

仍需人工决策的部分：

- 后续是否继续触碰 save backward compatibility
- retained adapter 是否应从“显式保留”升级为“继续删除”
- 若某阶段删除开始触碰视觉/动画协作边界时是否继续

#### 备选方案
1. `Strict full zero`：把 save backward compatibility 也纳入本轮 compat-zero 一起删掉。
2. 继续维持 `CombatModel` 为冻结 tiny facade，只做局部 test migration，不推进全域 compat-zero。

#### 风险与触发信号
- 风险：`turn_context` 桥的 staged collapse 过程中出现隐蔽的双读写回归。
- 触发信号：pointer / reposition / draw-lock 相关 focused pack 出现非内容型失败。
- 风险：自动化把 red 内容 bug、动画语义或 save/schema 风险误并入 compat cleanup。
- 触发信号：变更开始触碰 `test_json_red_cards.py`、`combat_view`、save payload migration 或 schema 文档。
- 风险：删除 `CombatModel` 时意外破坏 render/presentation contract coverage 的可读性。
- 触发信号：为保住测试而被迫重新引入另一个 broad facade。

#### 验证计划
- 成功指标：
  - `G1-G4` 可以按阶段独立执行、独立验证、独立提交。
  - 每一阶段都有 focused validation pack，且不依赖 red 内容修复才能前进。
  - combat 工程层剩余 compat surface 明显收缩，而 save backward compatibility 保持稳定不被误删。
- 检查日期：每次自动化唤醒与每个阶段完成后检查一次。

#### 回滚方案
若任一阶段证明风险高于收益：

- 按阶段 commit 执行 `git revert <commit_hash>`，而不是在工作中途堆叠新的补丁修补旧补丁。
- 保留本决策，但将失败阶段降级为新的 decision-gated backlog。
- 不通过口头改口把失败阶段继续混在后续自动化里。

#### 后续动作
- 以 `docs/development/combat/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 作为该工作线的 source-of-truth 执行蓝图。
- 在 `docs/development/CODEX_TASK_POOL.md` 中将该任务视为 active、decision-frozen 的自动化执行线。
- 配置当前线程的 30 分钟 heartbeat automation，默认按 `G1 -> G2 -> G3 -> G4 -> G5` 继续推进。

### [DL-20260423-03] Combat Compat-Zero 的 G5 retained adapter review 收口

- 日期：2026-04-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/combat/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`, `docs/development/CODEX_TASK_POOL.md`, `docs/logs/daily/2026-04-23.md`

#### 背景
`G1-G4` 已经完成，combat compat-zero 的 automation-safe 删除面已经基本收干净。此时剩下的对象里，既有真正的历史兼容边界，也有只是“看起来像 compat”的稳定契约，还有少量几乎没有接入的迁移脚手架。

如果继续把这三类东西混在一起按“像兼容层就继续删”推进，会把：

- save backward compatibility
- session/save host contract
- turn-start environment adapter
- 卡牌便捷访问契约
- 死脚手架清理

重新揉成同一条工作线，导致范围失真，也会让后续 AI 自动化无法判断哪里应该停手。

#### 决策
将 `G5 retained adapter review` 视为一个**决策收口阶段**，并正式给出以下分类：

1. 以下内容归类为 **retained backward-compat boundary**，不纳入本轮 compat-zero 删除范围：
   - `contexts/combat/application/save/combat_save_service.py`
   - `contexts/combat/application/save/save_snapshot_mapper.py`
   - `CombatSession.create_save_snapshot(...)` / `CombatSession.apply_save_snapshot(...)`
   - `Player` 中与 save/rollback 相关的 `legacy_energy` snapshot/restore 路径
2. 以下内容归类为 **intentional runtime adapter**，保留：
   - `ModelEnvironmentArenaEffect`
   - `DefaultTurnStartEnvironmentInjector`
3. 以下内容归类为 **stable convenience contract**，保留：
   - `CardInstance.card_id`
   - `CardInstance.cost_for_player(...)`
4. 以下内容**不视为 retained adapter**：
   - `contexts/combat/domain/effects/context.py::EffectContext` 归类为 dead scaffold，后续若要处理，应作为单独的小型安全清理切片
   - `Player` 的 scalar energy / colored pool 双轨同步不归入本轮 compat-zero 收尾，应另开一条 `energy contract convergence` 决策线

据此判定：本轮 combat global compat-zero 已在 **Engineering Zero** 意义上完成收口，不再继续沿同一条 compat-zero 主线做“顺手再删一轮”。

#### 人类工作量影响（核心）
- 减少的人类工时：后续不必反复解释“哪些 survivor 是故意留下的，哪些是还没来得及删”。
- 增加的人类工时：需要把后续工作拆成更明确的专题线，而不是继续沿 compat-zero 笼统推进。
- 对关键路径的变化：combat compat-zero 主线到此闭环；剩余工作改为 save lifecycle、energy convergence、dead scaffold cleanup 等独立 follow-up。

#### AI 工作量假设
AI / automation 后续适合继续做的部分：

- 小型 dead scaffold 清理
- 新专题线中的聚焦验证和文档同步
- 在已接受边界内继续维护 compat-zero guard

仍需人工决策的部分：

- 是否要启动 save lifecycle / schema redesign 相关工作
- 是否要启动 energy contract convergence
- retained convenience contract 将来是否有必要进一步收窄

#### 备选方案
1. `Strict survivor purge`：把 `ModelEnvironmentArenaEffect`、`card_id`、`cost_for_player()`、save backward-compat 一起继续压进 compat-zero 清理。
2. `停在 G4 不归档`：不继续删，但也不正式定义 survivor 的性质。

#### 风险与触发信号
- 风险：把 retained adapter 与 dead scaffold 混为一谈，导致后续误删稳定契约。
- 触发信号：后续变更开始把 save/load、simulation、timing contract 的稳定接口也视为默认删除对象。
- 风险：把 energy 双轨同步问题误包进 compat-zero 收尾，导致工程线重新失焦。
- 触发信号：后续 PR 同时修改 compat-zero guard、save payload、energy 规则与 UI/render contract。

#### 验证计划
- 成功指标：
  - compat-zero 主线在 `G5` 后明确闭环，不再存在“还有没有下一轮顺手清理”的歧义。
  - save backward-compat、environment adapter、card convenience contract 被文档显式标记为 retained。
  - dead scaffold 与 energy convergence 被单独识别为后续专题，而不是继续混在 compat-zero 内。
- 检查日期：下一次触发 combat 工程 backlog 拆分时检查一次。

#### 回滚方案
若后续证明某个 retained adapter 实际上持续制造工程噪音：

- 新增独立 decision log，而不是口头撤销本条记录。
- 将该对象从 retained 分类中移出，并单开新的专题线与验证包。

#### 后续动作
- 在 `docs/development/combat/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 中把 `G5` 标记为已完成的决策收口。
- 在 `docs/development/CODEX_TASK_POOL.md` 中把 combat compat-zero 主线标记为已闭环，并拆出后续专题方向。
- 保持 `save backward-compat`、动画/视频阻塞语义、`combat_view` 视觉协作边界继续独立，不回混到 compat-zero 主线。

### [DL-20260423-04] Start combat_analysis modelization as learned reranking

- Date: `2026-04-23`
- Owner: `Team`
- Status: `Accepted`
- Related:
  - `tools/combat_analysis/docs/MODELIZATION_MIGRATION_PATH_V1.md`
  - `tools/combat_analysis/recommendation/draft/__init__.py`
  - `tools/combat_analysis/retrieval_sidecar.py`
  - `tools/combat_analysis/design_engine/fast_card_loop.py`

#### Background

Recent external STS holdout work, especially the Silent semantic-drift lane, showed
that the main growth pressure is no longer missing benchmark structure. The main growth
pressure is heuristic accumulation inside ranking-heavy modules.

The project needs a clear decision about what should stay explicit and what should move
toward modelization before automation expands this work further.

#### Decision

Adopt a hybrid architecture:

1. Keep the current rule stack as the baseline fallback.
2. Start modelization in ranking/reranking layers first.
3. Keep contracts, legality constraints, benchmark gates, and closure diagnostics
   explicit and test-locked.
4. Use reviewed external STS holdout evidence as the main honesty surface for
   autonomy claims.
5. Defer `fun` / `feel` modelization until reviewed benchmark depth is materially
   stronger.

#### Human Workload Impact (Core)

- Reduced human work:
  less repeated manual score tweaking across multiple ranking modules.
- Increased human work:
  more up-front reviewed labeling, evaluation review, and promotion discipline.
- Critical path effect:
  shifts near-term effort from patching local heuristics toward dataset and shadow
  evaluation infrastructure.

#### AI Workload Assumption

AI can carry most of:

- reviewed coverage inventory
- feature export
- offline reranker experiments
- shadow comparison reports
- focused reviewed-case expansion

Human review remains required for:

- enabling any default learned blend
- introducing new dependencies
- moving `fun` or `feel` beyond proxy claims

#### Alternatives

1. Continue pure heuristic expansion.
2. Jump directly to end-to-end learned generation.

#### Risks And Triggers

- Risk:
  overfitting a learned reranker to narrow reviewed packs.
- Trigger:
  apparent gains vanish when evaluated on held-out character lanes or new reviewed
  failure families.

- Risk:
  blurring benchmark gate ownership with learned scoring.
- Trigger:
  any proposal starts letting the learned layer decide legality or hard pass/fail.

#### Validation Plan

- Success indicators:
  - deterministic reviewed ranking exports
  - offline learned reranker beats the baseline on held-out reviewed contrast slices
  - shadow runs improve weak semantic-discrimination lanes without weakening explicit
    gate ownership
- Review cadence:
  after each phase in `MODELIZATION_MIGRATION_PATH_V1.md`

#### Rollback Plan

If the learned path does not hold up, keep the exported dataset and reports, but revert
to pure baseline ordering by configuration and stop promotion at the shadow layer.

#### Follow-Up

1. Build deterministic reviewed feature export.
2. Train a small interpretable reranker offline.
3. Keep automation focused on reviewed coverage growth, export stability, and shadow
   evaluation before any default-on promotion.

### [DL-20260424-01] Campaign 下一轮采用 Boundary Hardening 主线

- 日期：2026-04-24
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/campaign/CAMPAIGN_BOUNDARY_HARDENING_V1.md`,
  `docs/development/CODEX_TASK_POOL.md`,
  `docs/development/campaign/CAMPAIGN_DIRECT_SEAM_POLICY_V1.md`,
  `docs/development/campaign/CAMPAIGN_RUNTIME_UI_BOUNDARY_V1.md`

#### 背景
Campaign 侧的前两轮主线已经基本完成：

- `Campaign Simplification V1`
- `Campaign Self Refactor V1`
- forced-event narrow plan 的既定切片
- lifecycle result / snapshot / read-surface 收口

当前真正缺少的不是再来一轮 broad cleanup，而是把已经接受的方向变成一条可自动化、可暂停、可恢复的边界硬化主线。否则后续自动化很容易把：

- lifecycle contract tightening
- trigger / forced-event ownership
- direct seam review
- `services` 目录纯化
- `thesis_slice` / task-area hotspot 清理

重新混成一条范围失真的大任务。

#### 决策
接受 `Campaign Boundary Hardening V1` 作为下一轮 active campaign architecture line，并冻结以下规则：

1. scope 限定在 `campaign/tests/docs`
2. 目标是 boundary hardening，而不是 broad cleanup 或目录纯化
3. 本轮不做物理 `services -> application/ui` 迁移
4. `hit_test_service` 只作为 optional late-phase seam review
5. `thesis_slice` 与 task-area hotspot 继续保持 triggered backlog，只有出现真实 writer/identity 或 board-rule 压力时才重开
6. hard-fail 只覆盖已稳定的 campaign boundary 规则；touch count、文件长度等指标保持 report-only
7. 每个自动化 slice 都必须同步：
   - task pool
   - 相关长期文档
   - 当日日志
8. 默认验证节奏为：
   - slice 级 targeted tests
   - phase close 跑 `py -3.11 -m pytest tests/campaign -q`
   - line closure 或高风险阶段收口时再跑 smoke baseline

#### 人类工作量影响（核心）
- 减少的人类工时：减少后续每轮自动化前对 campaign 下一步边界的重新判断成本。
- 增加的人类工时：需要一次性接受 hard-fail / report-only、主线 / optional / backlog 的更细分类。
- 对关键路径的变化：把 campaign 下一步从“看情况再决定做哪块清理”切成“按 phase 串行推进的边界硬化线”。

#### AI 工作量假设
AI / automation 适合继续做：

- lifecycle contract closure
- trigger / forced-event boundary closure
- campaign-side guardrail hardening
- optional `hit_test_service` seam review

仍需人工决策的部分：

- 是否重开 `CampaignView` / visual-runtime / shared cleanup
- 是否启动 `thesis_slice` 或 task-area hotspot 的新专题线
- 将来是否值得做物理 `services` taxonomy migration

#### 备选方案
1. 维持当前 docs 现状，只做 feature-driven 局部修补。
2. 直接重开更大范围的 campaign purity / taxonomy cleanup。

#### 风险与触发信号
- 风险：自动化将 boundary hardening 线重新做成 broad cleanup。
- 触发信号：开始大范围触碰 `contexts/campaign/view.py`、`rendering/**`、`ui_runtime/**` 或 `contexts/shared/**`。
- 风险：把 `thesis_slice` 和 task-area hotspot 当作 cleanliness 任务提前拉回主线。
- 触发信号：没有新的 writer/identity / board-rule 压力，却开始大规模改动 `thesis_slice` 或 `track_block_service`。
- 风险：将不稳定指标硬升级为 hard-fail，导致 guardrail 噪音高于收益。
- 触发信号：touch count、文件长度、职责数量这类波动指标开始频繁阻断正常推进。

#### 验证计划
- 成功指标：
  - 下一轮 campaign 自动化有单一 source-of-truth。
  - lifecycle / trigger / forced-event / direct-seam 规则不再需要依赖多份旧文档拼接判断。
  - `thesis_slice`、task-area hotspot、目录纯化没有误并入同一条执行线。
- 检查日期：每个 phase 收口后检查一次。

#### 回滚方案
若该主线被证明仍然范围过宽或收益不足：

- 不口头改线，必须新增 decision log 显式替代。
- 将失败 phase 作为 queued / backlog task 降级。
- 保留已接受的 supporting docs，不通过删除历史来假装从未做过该判断。

#### 后续动作
1. 新增 `docs/development/campaign/CAMPAIGN_BOUNDARY_HARDENING_V1.md` 作为主文档。
2. 更新 `docs/development/CODEX_TASK_POOL.md` 的 active campaign task。
3. 在 daily log 中记录本次 decision freeze。
4. 后续 automation 默认按 `Phase 0 -> Phase 1 -> Phase 2 -> Phase 3 -> optional Phase 4` 串行执行。

### [DL-20260426-01] Project Memory Health 采用 report-first 治理

- 日期：2026-04-26
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/PROJECT_MEMORY_HEALTH_V1.md`,
  `scripts/check_project_memory_health.py`,
  `docs/development/PROJECT_MEMORY_RULES.md`

#### 背景
项目记忆系统已经依赖 `AGENTS.md`、长期开发文档、任务池、决策日志、
daily log 和 weekly summary 共同维持上下文连续性。近期开发速度很高，
如果 daily/weekly、任务池或默认入口滞后，后续 AI 会话会重新增加读取噪音和
误判风险。

#### 决策
新增轻量 `Project Memory Health` 检查，并采用 report-first 默认策略：

1. 默认入口为 `python scripts/check_project_memory_health.py`。
2. 默认模式只对结构性缺失使用 `FAIL`，对节奏漂移和体量膨胀使用 `WARN`。
3. `--strict` 仅用于专门的记忆系统维护批次。
4. warning 只有在稳定、低噪音、修复路径明确时，才考虑升级为 hard-fail。
5. 继续保持 Markdown 文件为 source of truth，不引入数据库或重型记忆平台。

#### 人类工作量影响（核心）
- 减少的人类工时：更早发现 daily/weekly 滞后、任务池缺验证、入口文件膨胀等
  可恢复性问题。
- 增加的人类工时：需要在高强度 session 后查看一次健康报告并判断是否需要收口。
- 对关键路径的变化：不阻断功能开发；只在记忆维护分支或 strict 模式下收紧。

#### AI 工作量假设
AI 适合维护检查脚本、补文档入口、运行 report 并提出收口建议。人工仍决定哪些
warning 应该升级为硬规则，以及哪些信息值得晋升到长期文档。

#### 备选方案
1. 不加检查，继续依赖人工记得维护 daily/weekly。
2. 直接把所有记忆漂移规则做成 hard-fail。

#### 风险与触发信号
- 风险：健康检查变成低价值噪音。
- 触发信号：warning 经常出现但没有明确修复动作，或阻碍无关功能开发。
- 风险：默认入口继续膨胀成工具大全。
- 触发信号：`DEFAULT_ENTRYPOINTS.md` 持续增长，且 subsystem 细节没有回收到本地
  runbook。

#### 验证计划
- 成功指标：
  - `python scripts/check_project_memory_health.py` 能输出清晰的 fail/warn 摘要。
  - focused tests 覆盖缺今日志、缺核心文件、strict warning 行为。
  - 默认入口和记忆规则能指向该检查。
- 检查日期：每次记忆系统维护分支收口时检查。

#### 回滚方案
如果检查噪音高于收益，保留文档策略但从默认入口移除 strict 建议，并将脚本降级为
手动诊断工具。

#### 后续动作
1. 运行 focused tests。
2. 运行默认健康报告。
3. 根据报告决定是否需要 weekly summary 或 entrypoint 压缩 follow-up。

### [DL-20260429-01] Cardanalysis adopts case-backed multi-head direction

- Date: `2026-04-29`
- Owner: `Team`
- Status: `Accepted`
- Related:
  - `docs/development/cardanalysis/CARDANALYSIS_NORTH_STAR_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`
  - `docs/development/cardanalysis/CARDANALYSIS_CAPABILITY_DEPENDENCY_AND_CONFLICT_GRAPH_V1.md`

#### Background

Recent `cardanalysis` work expanded many report-only and reviewed surfaces:
mechanism viability, deck compression, fun/health, package health, campaign
power curve, evidence bundles, autonomous design review, and capability graph
planning. Continuing to add more independent evaluators without a shared input
contract would make semantic drift and multi-agent contamination harder to
control.

#### Decision

Adopt a case-backed multi-head direction for `cardanalysis`:

1. Use a short north-star contract to keep the system focused on mechanism
   discovery, evaluation, package/campaign reasoning, and autonomous design
   support.
2. Use a normalized case input contract as the shared anti-corruption layer for
   new case-like evidence.
3. Treat feature projection as the boundary between normalized cases and future
   capability/model heads.
4. Keep report-only outputs advisory and preserve reviewed hard-gate ownership.
5. Register the new direction, case input, normalized case, and feature
   projection artifacts in the capability dependency/conflict graph.

#### Human Workload Impact

- Reduced human work:
  future case collection can reuse one input shape instead of inventing a local
  schema for every new evaluator.
- Increased human work:
  new case families need light provenance, review-status, and allowed-consumer
  metadata.
- Critical path effect:
  shifts near-term work from writing more rules toward accumulating and
  normalizing reusable cases.

#### AI Workload Assumption

AI can help normalize cases, expand reviewed packs, maintain the capability
graph, and run impact/batch checks. Human review remains required for evidence
promotion, default-on learned behavior, and any hard-gate authority change.

#### Alternatives

1. Continue adding independent report-only evaluators with local fixture shapes.
2. Jump directly to a learned end-to-end design model without a normalized case
   and feature-projection boundary.

#### Risks And Triggers

- Risk:
  the case input contract grows into a large ontology too early.
- Trigger:
  agents start adding typed fields for one-off labels instead of using
  `feature_hints` first.

- Risk:
  source-mined or speculative evidence is mistaken for reviewed evidence.
- Trigger:
  downstream reports omit `evidence_tier`, `review_status`, or
  `authority_boundary`.

#### Validation Plan

- Success indicators:
  - capability graph validates with the new nodes and artifacts,
  - new case-backed work can declare which artifacts it consumes/provides,
  - parallel-agent batches can report soft/hard conflicts before implementation.
- Review cadence:
  after the first task-node batch is registered.

#### Rollback Plan

If the shared contract proves too heavy, keep the north-star direction but
downgrade the case input contract to a recommended adapter format rather than a
default input requirement.

#### Follow-Up

1. Register task nodes for stress/resolve, campaign experience, BBS/social, and
   case-library normalization work.
2. Use `scripts/validate_capability_graph.py --batch ...` before assigning the
   next parallel agent set.

### [DL-20260512-01] Test Strategy V1 adopts layered smoke feedback

- Date: `2026-05-12`
- Owner: `Team`
- Status: `Accepted`
- Related:
  - `docs/development/testing/TEST_STRATEGY_V1.md`
  - `docs/development/testing/TEST_BASELINE_2026-05-12.md`
  - `scripts/run_test_smoke.py`
  - `docs/development/DEFAULT_ENTRYPOINTS.md`

#### Background

Full `py -3.11 -m pytest -q` currently takes about four minutes on the active
workstation. That is acceptable as a final gate, but it is slow feedback for
AI-assisted architecture refactor slices that need many small checks.

The project already has a broader `run_repo_smoke_baseline.py`, but it is not
the fastest ordinary-refactor loop. The current test suite also needs a shared
vocabulary for focused, smoke, contract, integration, slow, and full-suite
validation.

#### Decision

Adopt `Test Strategy V1`:

1. Keep the existing full-suite commit gate unchanged for now.
2. Add a fast `quick` smoke profile for non-cardanalysis refactor feedback.
3. Add a `contract` smoke profile for boundary and source-scanning closure
   checks.
4. Register pytest marker vocabulary before mass-tagging tests.
5. Treat cardanalysis / combat_analysis test optimization as out of scope for
   this line unless explicitly reopened.

#### Human Workload Impact

- Reduced human work:
  routine architecture refactors can get useful feedback in seconds or tens of
  seconds before waiting for the full suite.
- Increased human work:
  the team needs to choose the right validation tier and avoid treating smoke
  as a replacement for full regression without a later gate decision.
- Critical path effect:
  later combat/campaign/save/content refactor work can iterate faster while the
  final safety net stays intact.

#### AI Workload Assumption

AI can maintain smoke profiles, update marker coverage, and split repeated slow
tests after profiling. Human review remains required before changing the commit
gate or deleting coverage.

#### Alternatives

1. Keep only full pytest for all feedback.
2. Enable pytest-xdist immediately.

#### Risks And Triggers

- Risk:
  smoke profiles are mistaken for full commit readiness.
- Trigger:
  a PR claims full validation while only smoke profiles ran.

- Risk:
  test speed work turns into coverage deletion.
- Trigger:
  slow tests are removed without equivalent or stronger contract coverage.

#### Validation Plan

- Success indicators:
  - quick smoke passes locally
  - contract smoke passes locally
  - test strategy docs and default entrypoints agree
  - full suite remains green before committing
- Review cadence:
  after the first deeper fixture-deduplication slice.

#### Rollback Plan

If the smoke profiles become noisy or misleading, remove the new smoke script
and keep the documentation as a report-only testing note. The full pytest gate
remains the rollback safety net.

#### Follow-Up

1. Add marker coverage only to tests owned by the smoke profiles.
2. Profile repeated campaign/combat fixture setup before changing helpers.
3. Evaluate xdist only after global state and filesystem assumptions are known.

### [DL-20260512-02] Architecture Refactor Season V1 adopts scoped execution lines

- Date: `2026-05-12`
- Owner: `Team`
- Status: `Accepted`
- Related:
  - `docs/development/architecture/ARCHITECTURE_REFACTOR_SEASON_V1.md`
  - `docs/development/testing/TEST_STRATEGY_V1.md`
  - `docs/development/CODEX_TASK_POOL.md`

#### Background

The project has a short window with no immediate content-development pressure.
The user is willing to accept a period of AI-heavy refactor work, but UI work
still needs human visual review. Old saves can be treated aggressively because
there is no external save-compatibility obligation yet.

The previous `Test Strategy V1` work added fast quick/contract smoke profiles,
so refactor slices can get useful feedback before waiting for the full suite.

#### Decision

Adopt `Architecture Refactor Season V1` as the top-level coordination plan for
the next architecture work. Execution lines are:

1. `Save Reset Policy V1`
2. `Combat Contract Convergence V1`
3. `CampaignState Strangler V1`
4. `Content Pack Minimal V1`
5. `UI Runtime Refactor Window`
6. `Test Strategy Follow-Up`

Each line must land as a separate branch/PR with its own scope, validation
pack, and stop conditions. The default first implementation line is
`Save Reset Policy V1`, followed by combat contract convergence.

#### Human Workload Impact

- Reduced human work:
  agents can choose the next refactor slice from a shared map instead of
  re-litigating the project direction every time.
- Increased human work:
  humans still need to review save-policy, UI behavior, and any product-facing
  content-pack identity decisions.
- Critical path effect:
  the next refactor window shifts from opportunistic cleanup to staged,
  independently reviewable architecture lines.

#### AI Workload Assumption

AI can safely carry the planning, save reset, combat contract, and campaign
strangler work when each slice has focused tests and smoke validation. UI
runtime refactors require human review before broad execution.

#### Alternatives

1. Continue choosing refactor tasks opportunistically after each PR.
2. Run one large architecture cleanup branch touching save, combat, campaign,
   content, and UI together.

#### Risks And Triggers

- Risk:
  the season plan becomes permission for broad rewrites.
- Trigger:
  one PR starts changing multiple execution lines or broad UI behavior.

- Risk:
  save reset decisions leak into combat/content work without an explicit policy.
- Trigger:
  combat or content-pack PRs delete save compatibility code before
  `Save Reset Policy V1` lands.

- Risk:
  UI refactor proceeds without human visual review.
- Trigger:
  changes touch `contexts/campaign/view.py`, `rendering/**`, or `ui_runtime/**`
  while no review window is available.

#### Validation Plan

- Success indicators:
  - top-level season doc exists and is referenced from task pool
  - each execution line has scope, no-touch list, validation, and stop
    conditions
  - quick smoke, contract smoke, and full pytest pass before committing the
    planning line
- Review cadence:
  after each execution line lands, before starting the next line.

#### Rollback Plan

If the season plan proves too broad, demote it to a reference doc and run only
the explicitly accepted execution line. Do not delete the history; supersede it
with a narrower decision-log entry.

#### Follow-Up

1. Open `Save Reset Policy V1` as the first implementation branch.
2. Draft `Combat Contract Convergence V1` with energy convergence as the first
   likely topic.
3. Keep UI runtime work queued until human visual review is available.

### [DL-20260512-03] Save Reset Policy V1 rejects pre-alpha legacy saves

- Date: `2026-05-12`
- Owner: `Team`
- Status: `Accepted`
- Related:
  - `docs/development/architecture/SAVE_RESET_POLICY_V1.md`
  - `contexts/shared/save/machine_snapshot_service.py`
  - `contexts/shared/save/game_save_slot_service.py`

#### Background

The project has no shipped external save corpus, and the user accepted that old
pre-alpha saves may be invalidated during the current refactor window. The old
save schema spec still described reliable old-save loading as the default goal,
which conflicted with the active architecture refactor season.

#### Decision

Adopt `Save Reset Policy V1` for the current pre-content stage:

1. Current whole-game saves must use `meta.snapshot_schema_version`,
   `persistent`, and `state_snapshots`.
2. Save slot payloads must wrap the current machine snapshot under
   `machine_snapshot`.
3. Legacy machine snapshots, missing machine snapshot versions, and unwrapped
   slot payloads fail closed instead of being migrated by guesswork.
4. Combat save slot payloads must wrap the current combat snapshot under
   `combat_snapshot`.
5. Legacy combat v0 raw payloads, raw current combat snapshots without the slot
   wrapper, and full machine snapshot `COMBAT` fallback payloads fail closed
   instead of being migrated by guesswork.
6. Player energy scalar/pool compatibility remains outside this save policy and
   belongs to `Combat Contract Convergence V1`.

#### Human Workload Impact

- Reduced human work:
  less time spent preserving local historical saves that are not product
  commitments.
- Increased human work:
  any later compatibility promise must be documented before migrations are
  reintroduced.
- Critical path effect:
  future combat and content-pack save decisions can build on a smaller current
  contract.

#### AI Workload Assumption

AI can remove low-value compatibility layers and keep current round-trip tests
green. Human decision remains required before promising external save
compatibility or content-pack identity pinning.

#### Alternatives

1. Keep reliable old-save loading as the default.
2. Delete all save version metadata and rely only on current shapes.

#### Risks And Triggers

- Risk:
  a developer expects an old local save to load during testing.
- Trigger:
  support or playtest feedback identifies a save corpus worth preserving.

- Risk:
  future agents add ad hoc migrations without updating policy.
- Trigger:
  migration code appears without fixture-backed tests and a policy update.

#### Validation Plan

- Success indicators:
  - current machine snapshot round trips still pass
  - legacy machine snapshots are rejected explicitly
  - legacy unwrapped slot payloads are rejected explicitly
  - legacy combat v0/raw/full-machine fallback payloads are rejected explicitly
  - full pytest passes before commit
- Review cadence:
  after the next combat save or content-pack identity slice.

#### Rollback Plan

Supersede this decision with a compatibility policy, restore fixture-backed
migrations for the required historical schemas, and keep rejection tests only
for unsupported versions.

#### Follow-Up

1. Evaluate combat snapshot v0 migration separately.
2. Record content-pack identity only after the save reset stance is stable.
