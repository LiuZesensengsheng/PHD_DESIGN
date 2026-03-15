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

### P1. TA 任务链式发布 v1

- 目标：
  - 把点名主题从“单次 deadline”升级成“小型链式任务压力”
- 主要输入：
  - `docs/design/enemydesigon/TA_TASK_CHAINING_V1.md`
  - `docs/design/enemydesigon/TA_TASK_HOST_MINIMUM_V1.md`
  - 当前 TA CSV -> JSON 运行链
- 预期输出：
  - 至少 1 条真实可跑的链式任务遭遇
  - `publish_task` 在运行时的稳定落地
  - 对应回归测试
- 边界：
  - 不做任务 UI
  - 不做完整任务 DSL
  - 不直接做 DDL 或三端
- 完成标准：
  - 任务失败/完成都可以发布后续任务
  - 点名主题 encounter 可以完整走完链式压力循环

### P1. TA DDL 精英前置机制评估

- 目标：
  - 盘清 DDL 种植园主要落地还缺哪些最小中层能力
- 主要输入：
  - `docs/design/enemydesigon/TA-2_extracted/TA/战斗/敌人设计/精英/DDL种植园主.md`
  - `docs/design/enemydesigon/TA_IMPLEMENTABILITY_MAPPING_V1.md`
  - 当前 TA 任务宿主实现
- 预期输出：
  - 一份 DDL 精英前置机制评估文档
  - 已支持 / 待补 / 不建议现在做 的清单
  - 推荐实现顺序
- 边界：
  - 本轮只做评估，不直接实现精英
  - 不顺手扩成完整 TA 全任务系统
- 完成标准：
  - 明确 DDL 精英是否只需要扩任务宿主，还是还需要额外中层能力

### P1. TA DDL 精英最小能力实现

- 目标：
  - 把 DDL 种植园主需要的 3 个最小中层能力补出来
- 主要输入：
  - `docs/design/enemydesigon/TA_DDL_PRECONDITIONS_V1.md`
  - 当前 TA 任务宿主与链式任务实现
- 预期输出：
  - 任务数量查询接口
  - 共享倒计时固定为 1 的 encounter 级配置
  - 基于未完成任务数的分档 intent / 伤害表达
- 边界：
  - 本轮先补前置能力，不直接把 DDL 精英整套做完
  - 不顺手做三端、不做完整任务 UI
- 完成标准：
  - DDL 精英已经具备第一版可实现的最小宿主能力

### P1. 内容数据校验扩展

- 目标：
  - 继续扩内容数据校验，让坏数据更早失败
- 主要输入：
  - 当前 CSV/JSON 数据链
  - `docs/development/DATA_PIPELINE_GUARDRAILS_V1.md`
  - 现有校验脚本和测试
- 预期输出：
  - 更强的字段、引用、非法值校验
  - 更清楚的失败提示
  - 对应测试补强
- 边界：
  - 不重写整个内容系统
  - 不顺手改 runtime repository
- 完成标准：
  - 常见坏内容能在 runtime 前失败，并给出明确错误

### P1. 依赖倒置与编排层收口 v1

- 目标：
  - 收窄 `CampaignState -> services` 的依赖面，把“拆出去但仍强耦合 state”的假分层，推进成更稳定的编排层边界
- 主要输入：
  - `docs/development/ARCHITECTURE_BOUNDARIES.md`
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/*.py`
  - `contexts/shared/save/save_repository.py`
  - `contexts/shared/save/save_load_service.py`
- 预期输出：
  - 一份依赖收口清单（哪些 service 仍直接依赖整个 state，哪些值得先改）
  - 至少 1 到 2 个高价值 service 改为依赖更窄的 host/facade/port，而不是 `state: Any`
  - 对应回归测试，确保行为不变
  - 一份简短结论，说明哪些地方适合继续做 DIP，哪些地方暂不值得抽象
- 边界：
  - 不做全仓库接口化运动
  - 不为了 DIP 重写 UI 层
  - 不强行把所有 service 一次性改完
  - 允许保留过渡层，但新依赖关系不能比现在更宽
- 完成标准：
  - 至少识别并记录当前最值得改的 5 个依赖热点
  - 至少完成 1 个真实依赖收窄切口，并保留测试护栏
  - 后续新增 service 默认不再直接吃整个 `CampaignState`

### P1. Thesis Runtime State Fourth Cut

- 目标：
  - 继续把 thesis 相关可变状态从 `CampaignState` 收到更明确的 runtime host / domain object，减少兼容代理层长期滞留
- 主要输入：
  - `contexts/campaign/domain/thesis_runtime_state.py`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/thesis_*.py`
  - `tests/campaign/test_thesis_runtime_state.py`
- 预期输出：
  - 更清晰的 thesis runtime 状态归属
  - 减少 `CampaignState` 上 thesis 兼容字段或代理
  - 对应 snapshot/load 回归测试补强
- 边界：
  - 不重写 thesis 全链路
  - 不顺手做 UI 重构
  - 允许保留少量过渡代理，但新增状态不再回流到 `CampaignState`
- 完成标准：
  - 至少 1 组 thesis 运行时字段完成归位
  - `tests/campaign/test_thesis_runtime_state.py` 与相关回归保持通过

### P1. Transition Contract Cleanup v1

- 目标：
  - 统一 campaign / combat / dialogue / event 之间的 request / result 传递模式，继续减少散装 payload 键名和隐式协议
- 主要输入：
  - `contexts/shared/domain/contracts.py`
  - `contexts/shared/game_state_machine.py`
  - 各 state 的 transition / persistent 读写路径
- 预期输出：
  - 更清晰的跨状态 contract 清单
  - 新增或补齐的 helper / DTO / contract key
  - 对应回归测试
- 边界：
  - 不一次性统一所有历史键名
  - 不重写状态机
  - 优先清理高频路径，不碰低价值历史路径
- 完成标准：
  - 至少 1 到 2 条高频状态切换链路完成显式 contract 收口
  - 后续新增跨状态 payload 不再默认直接写裸字符串键

### P1. Headless Encounter Smoke v1

- 目标：
  - 为关键 encounter / campaign / thesis 主路径建立“能跑通、不崩、不缺关键数据”的无 UI smoke 覆盖
- 主要输入：
  - 当前 campaign / combat / thesis 关键测试入口
  - `docs/development/TEST_STRATEGY.md`
  - 已存在的 headless / regression helpers
- 预期输出：
  - 一组高价值 smoke tests
  - 对关键遭遇和主流程的最小回归护栏
  - 失败时更清楚的定位信息
- 边界：
  - 不做完整平衡模拟
  - 不追求覆盖全部 encounter
  - 只兜最贵的“跑不起来 / 接不起来”回归点
- 完成标准：
  - 至少覆盖 3 条关键主路径或关键遭遇
  - 失败时能明确指出是数据问题、流程问题还是状态恢复问题

### P1. Snapshot Diff Tool v1

- 目标：
  - 建一套轻量 snapshot diff / inspect 能力，帮助快速比较状态变化和定位回归
- 主要输入：
  - `contexts/shared/save/machine_snapshot_service.py`
  - 当前 save/load 与 snapshot 结构
  - 典型 campaign / thesis / combat snapshot 样本
- 预期输出：
  - 一个 focused script 或 helper
  - 至少一组对应测试
  - 一份简短使用说明
- 边界：
  - 不做复杂 GUI 工具
  - 先支持 JSON 级 diff 与关键字段摘要
  - 不顺手扩成完整调试平台
- 完成标准：
  - 能快速比较两份 machine snapshot 的关键差异
  - 能帮助定位“状态为什么和预期不一样”

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

### P2. Combat Task Host V2

- 目标：
  - 在现有 TA / DDL 任务链落地后，把任务宿主沉淀成更稳定的战斗中层能力
- 当前不优先的原因：
  - 先要让当前 P1 链式任务和 DDL 最小能力落地
  - 过早扩宿主容易把需求推成抽象运动

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

- `Card Content Pipeline Hardening`
- `Thesis And Judgment Complexity Review`
- `Investigate Why Virtue/Torment Does Not Trigger At 100`
- `Thesis Runtime State Third Cut`
- `TA Enemy Implementability Mapping`
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
