# Codex 任务池

## 用途

这份文档只记录一类事情：

- 哪些任务适合 Codex 独立连续执行几小时
- 这些任务需要什么输入
- 产出是什么
- 哪些任务已经可以直接做，哪些还需要先继续定

这份文档不是：

- 日报
- 架构原则文档
- 决策日志

## 使用方式

每次选择任务时，先确认 4 件事：

1. 任务是否仍符合当前优先级
2. 输入文档或数据是否已经存在
3. 完成标准是否足够清楚
4. 是否适合低监督连续执行

## 任务选择规则

优先交给 Codex 的任务：

- 输入文件明确
- 输出文件明确
- 测试标准明确
- 不依赖高频人工审美判断
- 不依赖实时试玩手感

暂时不要交给 Codex 长时间独立推进的任务：

- 纯视觉打磨
- 最终剧情语气定稿
- 高主观性的 UX 调整
- 最后阶段的纯手感平衡

## 当前活跃任务

## 待定 / 需要更多前置条件

### P2. 三端精英前置机制评估

- 目标：
  - 盘清“微信 / QQ / 邮箱”三端精英需要的最小宿主能力
- 当前不优先的原因：
  - 复杂度高于 DDL 精英
  - 依赖更重的精英专属规则

### P2. 敌人数值基线 v1

- 目标：
  - 给普通敌 / 精英 / boss 建第一版数值曲线
- 当前不优先的原因：
  - TA 主题机制还在继续落地
  - 现在先做数值会产生假精确

### P2. 红白卡第二轮调数

- 目标：
  - 只修首轮平衡后暴露的问题卡
- 当前不优先的原因：
  - 需要更多试玩反馈

### P2. Headless 平衡检查

- 目标：
  - 建立轻量的无 UI 平衡体检
- 当前不优先的原因：
  - 机制建设优先级更高

### P2. Combat Task Host V2（在 shared host v1 基础上收口）

- 目标：
  - 在现有 shared task host、链式 `publish_task`、DDL 压力表达已经可跑的基础上，把任务宿主沉淀成更稳定的战斗中层能力
- 当前已落地基线：
  - `CombatTaskHost` 已挂到 `CombatState`
  - 点名主题共享宿主、链式后续任务、DDL 一回合倒计时与失败分档表达已存在
- 当前不优先的原因：
  - 当前 v1 主路径已经可跑，短期更缺的是架构收口与验证护栏，而不是继续扩任务宿主抽象
  - 过早扩宿主容易把需求推成抽象运动

### P2. Combat Action Queue V1

- 目标：
  - 让卡牌战斗从“效果对象立即执行为主”逐步演进为“动作对象 + 顺序队列执行”的混合模式
- 主要输入：
  - `contexts/combat/domain/services/play_card_transaction.py`
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/domain/task_host.py`
  - `contexts/combat/domain/state.py`
  - 当前高频卡牌效果与战斗回归测试
- 预期输出：
  - 一版最小 `CombatAction` 抽象与 `ActionQueue` / `ActionManager`
  - 至少几类高频效果改为先产出 action 再顺序执行
  - headless 模式下可一次 drain 队列的测试入口
  - 一份简短结论，说明哪些效果适合继续 action 化，哪些暂时保留即时执行
- 边界：
  - 不重写整个战斗系统
  - 不一次性把全部 effect 都 action 化
  - 保留 `PlayCardTransaction` 作为出牌事务入口
  - 不顺手扩成完整动画系统或 replay 平台
- 完成标准：
  - 至少 3 到 4 类高频效果可通过 action queue 稳定执行
  - 现有战斗主回归不退化
  - 动作顺序、连锁效果和后续扩展点比当前更显式
- 当前不优先的原因：
  - 先要把当前 TA / DDL 主线和编排层收口工作做稳
  - 需要避免在机制仍快速变化时过早把整套战斗逻辑框架化

### P2. Thesis Aggregate Boundary Review

- 目标：
  - 明确 thesis 线当前谁是事实聚合根、哪些状态修改必须走统一入口，而不是继续散落在 `CampaignState`、service 和临时字典之间
- 主要输入：
  - `contexts/campaign/domain/thesis_runtime_state.py`
  - `contexts/campaign/services/thesis_*.py`
  - `contexts/campaign/state.py`
  - `docs/design/PAPER_LINE_TRACK_SERVICE_SPEC.md`
- 预期输出：
  - 一份 thesis 聚合边界判断
  - 至少 1 个真实写路径收口切口
  - 对应不变量或 seam 回归测试
- 边界：
  - 不重写 thesis 全链路
  - 不顺手做 board/UI 重构
  - 允许保留过渡 DTO 和 runtime seam
- 完成标准：
  - 明确 thesis 相关“哪些改动必须通过统一入口发生”
  - 至少减少 1 处 thesis 散装状态写入
- 当前不优先的原因：
  - 先让当前 runtime seam 和编排层收口稳定一段时间
  - 需要避免在 thesis 线仍有活跃需求时过早冻结整体建模

### P2. Campaign Aggregate Candidate Review

- 目标：
  - 判断 campaign block / track / route 相关对象里，哪些值得继续保持 DTO + service，哪些已经到了应该收成聚合根的阶段
- 主要输入：
  - `contexts/campaign/domain/block_dto.py`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/`
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
- 预期输出：
  - 一份候选聚合图
  - 明确“不建议现在聚合化”的部分
  - 至少 1 条高频修改路径的收口建议
- 边界：
  - 不为了 DDD 名词强行引入聚合
  - 不重写整个 campaign runtime
  - 允许结论是“继续保持 DTO + 编排层更合适”
- 完成标准：
  - 能解释清楚 campaign 当前最值得聚合化的对象边界
  - 能解释清楚哪些部分暂时不聚合反而更稳
- 当前不优先的原因：
  - 当前 campaign 仍处于 mixed-mode UI 过渡期
  - 需要先继续观察 block / route / reward 高频改动路径

### P2. Repository Boundary Cleanup V1

- 目标：
  - 盘清哪些地方值得正式 repository 化，哪些继续保持 session / persistent / helper 即可，避免 repository 模式被过早泛化
- 主要输入：
  - `contexts/shared/save/save_repository.py`
  - `contexts/shared/save/file_save_repository.py`
  - 当前 campaign / combat / content 读写路径
  - `docs/development/ARCHITECTURE_BOUNDARIES.md`
- 预期输出：
  - repository 候选清单
  - 不建议 repository 化的边界清单
  - 至少 1 个高价值边界的抽象建议或切口
- 边界：
  - 不搞全仓库 repository 化运动
  - 不为了模式统一重写稳定路径
  - 允许结论是“某些边界继续保持 helper/store 更合适”
- 完成标准：
  - 明确哪些 repository 是真正高价值的
  - 至少减少 1 处“service 直接碰具体数据实现”的风险点
- 当前不优先的原因：
  - 当前最成熟的 repository 样板主要集中在 save/load
  - 需要先把更高优先级的编排层和 runtime seams 做稳

### P2. Aggregate Invariant Tests V1

- 目标：
  - 把关键聚合或候选聚合的不变量写成可回归测试，而不是只停留在口头判断和聊天上下文
- 主要输入：
  - thesis / combat / campaign 的高价值聚合候选
  - 现有 domain / service regression tests
  - 当前 runtime seam 和 contract helper
- 预期输出：
  - 一组围绕不变量的 focused tests
  - 一份简短说明，记录当前测试在保护哪些边界
- 边界：
  - 不要求先把所有聚合形式化完成
  - 先保护最贵的非法状态和越界写入
  - 不把测试写成 UI-heavy 集成大杂烩
- 完成标准：
  - 至少 2 到 3 组高价值不变量被测试兜住
  - 后续相关重构不再完全依赖口头记忆
- 当前不优先的原因：
  - 需要先完成部分聚合边界判断，否则测试目标容易飘
  - 当前更优先的是继续把运行时 seam 和 contract 收清

### P2. State Host Facade V1

- 目标：
  - 为高复杂 campaign service 提供更窄的 host / facade，减少 `state: Any` 成为默认依赖
- 当前不优先的原因：
  - 需要先通过 `依赖倒置与编排层收口 v1` 找到最高 ROI 的切口
  - 还不适合全量统一

### P2. Encounter Contract Expansion

- 目标：
  - 扩 encounter / enemy / task-chain 的内容 contract、字段约束和引用校验
- 当前不优先的原因：
  - 当前先把活跃 TA 主线做稳
  - 需要在现有运行链上确定最常见的坏数据形态

### P2. Seed Replay / Repro Tool

- 目标：
  - 给关键 battle / campaign 流程提供更稳定的 seed 复现或最小 replay 能力
- 当前不优先的原因：
  - 先有 headless smoke 再做 replay 更划算
  - 需要先确定哪些随机入口最值得固定

### P2. Balance Report Script V1

- 目标：
  - 建立轻量数值体检脚本，先做异常发现，不做复杂平衡 AI
- 当前不优先的原因：
  - 敌人与任务机制仍在继续落地
  - 现在做深平衡容易产生假精确

### P3. 内容接入工作流

- 目标：
  - 文档化新卡牌 / 新敌人 / 新特质接入流程
- 当前不优先的原因：
  - 当前更需要先把 TA 线和数据链继续做稳

## 最近完成

- `内容数据校验扩展`
- `Snapshot Diff Tool v1`
- `Transition Contract Cleanup v1`
- `Headless Encounter Smoke v1`
- `Thesis Runtime State Fourth Cut`
- `依赖倒置与编排层收口 v1`
- `Card Content Pipeline Hardening`
- `Thesis And Judgment Complexity Review`
- `Investigate Why Virtue/Torment Does Not Trigger At 100`
- `Thesis Runtime State Third Cut`
- `TA Enemy Implementability Mapping`
- `TA DDL 精英前置机制评估 v1`
- `TA DDL 精英最小能力实现 v1`
- `TA 第一批骨架敌人主运行链接入`
- `仓库级数据链护栏`
- `TA 最小任务宿主`
- `TA 任务宿主 v1`
- `TA 任务链式发布 v1`

## 退出规则

当出现以下任一情况时，任务应该从活跃区移走：

- 已经实现
- 被新的设计决策阻塞
- 不再适合当前生产阶段
- 需要持续高频人工主观反馈
