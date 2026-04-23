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

### [DL-20260423-01] Combat 全域 Compat-Zero 采用 Engineering Zero 边界

- 日期：2026-04-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`, `docs/development/CODEX_TASK_POOL.md`, `docs/logs/daily/2026-04-23.md`

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
接受 `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 中推荐的决策包，定义本轮 combat 全域 compat-zero 为 **Engineering Zero**，具体为：

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
- 以 `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 作为该工作线的 source-of-truth 执行蓝图。
- 在 `docs/development/CODEX_TASK_POOL.md` 中将该任务视为 active、decision-frozen 的自动化执行线。
- 配置当前线程的 30 分钟 heartbeat automation，默认按 `G1 -> G2 -> G3 -> G4 -> G5` 继续推进。

### [DL-20260423-02] Combat Compat-Zero 的 G5 retained adapter review 收口

- 日期：2026-04-23
- 负责人：Team
- 状态：Accepted
- 关联：`docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`, `docs/development/CODEX_TASK_POOL.md`, `docs/logs/daily/2026-04-23.md`

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
- 在 `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` 中把 `G5` 标记为已完成的决策收口。
- 在 `docs/development/CODEX_TASK_POOL.md` 中把 combat compat-zero 主线标记为已闭环，并拆出后续专题方向。
- 保持 `save backward-compat`、动画/视频阻塞语义、`combat_view` 视觉协作边界继续独立，不回混到 compat-zero 主线。
