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

- 当前推荐执行方式：
  - 先做 `combat orchestration v1`，暂不碰 UI 节点化
  - 串行推进，不并行开多条 combat 主路径重构
  - 允许短期迁移窗口，但不接受长期双轨
  - `2026-03-16` 判定更新：`combat orchestration v1` 已可视为完成，后续转入 `Combat Queue Full Cutover`
  - v1 之后的剩余 fallback 面默认只包括条件型、属性来源型和其他小众复杂效果

### P1. Combat Action Contracts + Queue Skeleton V1

- 目标：
  - 建立最小 `CombatAction`、`ResolutionContext`、`ActionQueue`、`ActionExecutor`
  - 先把“动作语义”和“顺序执行入口”立起来，而不是一次性迁完所有 effect
- 主要输入：
  - `contexts/combat/domain/services/play_card_transaction.py`
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/domain/task_host.py`
- 预期输出：
  - 一版最小动作合同与队列骨架
  - 一组 focused tests，覆盖 `push_front` / `push_back` / `drain`
  - 一份简短说明，约定后续新复杂机制优先走新编排口
- 边界：
  - 不切 UI
  - 不全量迁移卡牌效果
  - 不顺手重写 `CombatModel`
- 完成标准：
  - 队列骨架可独立测试
  - 至少几类基础动作可通过执行器稳定落状态
  - 后续任务可以在这套骨架上继续串行推进

### P1. Task Resolution Orchestration Cutover V1

- 目标：
  - 先把 `CombatTaskHost` 的 resolution actions 并入统一动作队列
  - 消除 `CombatModel._apply_task_resolution_actions()` 里的大分支解释器
- 主要输入：
  - `contexts/combat/domain/task_host.py`
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/mvc/factory.py`
- 预期输出：
  - `TaskResolutionOrchestrator`
  - `CombatTaskResolutionAction -> CombatAction` 的映射层
  - 任务宿主倒计时 / 发布后续任务 / 变身 / 敌人 buff 的 focused tests
- 边界：
  - 不扩写新的 task host 抽象运动
  - 不把 card play 主路径一起大改
- 完成标准：
  - task resolution 主路径切到新队列
  - 旧 `_apply_task_resolution_actions()` 主解释逻辑删除或降为薄适配层
  - 任务链式发布和倒计时回归不退化

### P1. Card Play Orchestrator Entry Cutover V1

- 目标：
  - 为出牌建立显式编排入口，减少“`CardPlayed` 事件 + `CombatModel` 订阅”承担主流程的程度
- 主要输入：
  - `contexts/combat/domain/player.py`
  - `contexts/combat/domain/services/play_card_transaction.py`
  - `contexts/combat/mvc/model.py`
- 预期输出：
  - `CardPlayOrchestrator`
  - 明确的出牌编排入口与后处理 checkpoint
  - 一份简短说明，记录 `CardPlayed` 在迁移期内是通知还是主入口
- 边界：
  - 不要求此阶段把所有 effect 都改成 action
  - 保留事务层校验 / 扣费 / 回滚逻辑
- 完成标准：
  - 出牌主路径有单一编排入口
  - 卡牌后处理顺序比当前更显式
  - 不再继续向旧 `CombatModel` 直执行路径堆新复杂逻辑

### P1. High-Frequency Effect Planner V1

- 目标：
  - 先把高频、低风险卡牌效果改成“先规划动作，再顺序执行”
- 主要输入：
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/domain/effects/impl/core.py`
  - 高频战斗回归测试
- 预期输出：
  - 一版最小 `EffectPlanner`
  - 至少 4 类高频效果 action 化：
    - 单体伤害
    - 格挡
    - 抽牌
    - 上 buff / debuff
- 边界：
  - 不一次性迁 60 类 effect
  - pile / pointer / 强随机复杂牌先不求一轮做完
- 完成标准：
  - 高频效果通过 queue 稳定结算
  - 结算顺序、连锁 follow-up 和后续扩展点更显式
  - 旧执行器只保留有限兼容用途，不再扩新逻辑

### P1. Combat Post-Resolution Policies V1

- 目标：
  - 把清理死亡敌人、卡牌去向、异色后处理、战斗结束检查收成统一 checkpoint
- 主要输入：
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/domain/services/pile_service.py`
  - `contexts/combat/domain/services/ideal_policy.py`
- 预期输出：
  - 一组 post-resolution policy/helper
  - focused regression tests，保护 card route / prune / combat end 顺序
- 边界：
  - 不做 UI 侧动画编排
  - 不顺手改 render state 协议
- 完成标准：
  - 出牌与任务动作结算后的收尾路径更统一
  - 顺序错误不再依赖隐式调用链兜住

### P2. Turn Flow Orchestration V1

- 目标：
  - 显式整理 enemy turn start / end、task tick、turn checkpoint 的流程点
- 当前不优先的原因：
  - 先把 task resolution 和 card play 两条最贵主路径切稳
  - 这一块适合在前几步稳定后继续收口

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

### P2. Combat Task Host V2（在 task resolution cutover 后再继续）

- 目标：
  - 在现有 shared task host、链式 `publish_task`、DDL 压力表达已经可跑的基础上，把任务宿主沉淀成更稳定的战斗中层能力
- 当前已落地基线：
  - `CombatTaskHost` 已挂到 `CombatState`
  - 点名主题共享宿主、链式后续任务、DDL 一回合倒计时与失败分档表达已存在
- 当前不优先的原因：
  - 当前更高 ROI 的切口是先把 resolution path 并入统一编排层
  - 若过早继续扩宿主抽象，容易在主路径尚未切稳前形成新的双轨

### P2. Combat Queue Full Cutover（拆分任务池）

- 总目标：
  - 在 `combat orchestration v1` 完成后，把剩余仍依赖 fallback 的主路径继续收口到统一 action queue
  - 这一阶段不再做新架构形态探索，而是做“剩余面缩减 + 旧兼容层变薄”
- 默认执行顺序：
  1. `Queue Red Hand Generation Cutover V1`
  2. `Queue Red Utility Trigger Cutover V1`
  3. `Queue White Pointer Core Cutover V1`
  4. `Queue Active Fallback Boundary Tests V1`
  5. `Legacy Effect Executor Thin-Compat Pass V1`
- 当前状态（`2026-03-16`）：
  - 上述 5 个串行 cutover/收尾任务已完成
  - `Combat Queue Full Cutover` 这一轮可以视为已收口
  - 后续若继续推进，不再是 phase-2 主链重构，而是按具体复杂 effect 继续缩小 fallback 面
- 总边界：
  - 不重写整个战斗系统
  - 不做 UI 节点化
  - 不引入通用脚本 DSL
  - 保留 `PlayCardTransaction` 作为出牌事务入口
  - 允许少量短期 fallback，但不接受继续扩散旧执行器分支

### P2. Queue Red Hand Generation Cutover V1

- 目标：
  - 先把红色现役里最集中的“向手牌生成新牌”路径收口到 queue
  - 优先覆盖：
    - `create_card_in_hand`
    - `red_create_random_red_in_hand`
    - `red_create_random_offcolor_in_hand`
- 主要输入：
  - `contexts/combat/application/orchestration/effect_planner.py`
  - `contexts/combat/application/orchestration/action_executor.py`
  - `contexts/combat/domain/effects/impl/pile.py`
  - `contexts/combat/domain/effects/impl/red.py`
  - 红色生成类卡牌 focused tests
- 预期输出：
  - 一版最小“生成到手牌”动作合同
  - planner 能把固定生成与随机生成映射成 queue actions
  - frontier bonus / 临时费用改写 / 同批次 frontier 标记继续保持现语义
- 边界：
  - 不扩成通用卡牌工厂 DSL
  - 不顺手处理抽牌、弃牌、猜牌等其他红色特殊效果
- 完成标准：
  - 现役红色“生成到手牌”主链不再因为该 effect 类型整体 fallback
  - 随机池过滤、生成数量、frontier 语义与当前回归一致

### P2. Queue Red Utility Trigger Cutover V1

- 目标：
  - 继续收口红色现役里仍高频但语义简单的小工具效果
  - 优先评估并处理：
    - `gain_energy`
    - `red_mark_next_frontier`
    - 可直接表达成最小 follow-up action 的红色 trigger 效果
- 主要输入：
  - `contexts/combat/application/orchestration/effect_planner.py`
  - `contexts/combat/application/orchestration/action_executor.py`
  - `contexts/combat/domain/effects/impl/core.py`
  - `contexts/combat/domain/effects/impl/red.py`
  - 红色 utility 卡牌 focused tests
- 预期输出：
  - 一版受控的小型 utility action 集合
  - 不再需要把简单能量/标记类效果塞回 legacy executor
  - planner-safe / fallback 边界更清楚
- 边界：
  - 不提前处理红色复杂猜牌、随机弃牌连锁、按费用打伤害等组合效果
  - 不把所有 trigger 效果泛化成通用条件脚本
- 完成标准：
  - 简单 utility 效果不再成为高频 fallback 面
  - 剩余红色 fallback 主要集中到复杂组合型效果

### P2. Queue White Pointer Core Cutover V1

- 目标：
  - 收口白色现役里最核心、最常用的一段指针链路
  - 优先覆盖：
    - `pointer_engine`
    - `pointer_warp`
    - `white_pointer_focus_burst`
    - `white_pointer_burst_from_x`
- 主要输入：
  - `contexts/combat/domain/effects/impl/pointer_queue_white.py`
  - `contexts/combat/application/orchestration/effect_planner.py`
  - `contexts/combat/application/orchestration/action_executor.py`
  - 白色指针 focused tests
- 预期输出：
  - 一版最小白色指针动作合同
  - 指针初始化、位移、burst 伤害进入显式 queue
  - 指针相关顺序不再依赖 effect body 隐式串联
- 边界：
  - 不一轮吃掉全部白色 reposition / summary / sequence / lock queue 组合
  - 不顺手重写整套 pointer runtime
- 完成标准：
  - 现役白色指针核心卡不再默认回落到旧路径
  - 指针主链的状态推进与 burst 结算有 focused tests 护栏

### P2. Queue Active Fallback Boundary Tests V1

- 目标：
  - 把 planned path / fallback path 的边界固定成可回归测试，而不是口头约定
- 主要输入：
  - `tests/combat/test_effect_planner.py`
  - `tests/combat/test_card_play_orchestrator.py`
  - `tests/combat/test_play_card_transaction.py`
- 预期输出：
  - 一组 focused tests，覆盖：
    - 红色生成效果进入 planned path
    - 红色 utility 效果进入 planned path
    - 白色指针核心进入 planned path
    - mixed planned/fallback effect 顺序稳定
    - fallback 保持受控且不会吞掉 follow-up queue 语义
- 边界：
  - 不把测试做成 UI-heavy 集成大杂烩
  - 不要求覆盖所有冷门卡牌
- 完成标准：
  - 队列边界与 fallback 边界都能被测试直接说明
  - 后续 cutover 不再主要依赖人工记忆

### P2. Legacy Effect Executor Thin-Compat Pass V1

- 目标：
  - 在前几项完成后，把旧 `EffectExecutor` 再压薄一轮
  - 明确它在 queue 时代只负责：
    - legacy fallback 执行
    - target resolution / build seam
    - 迁移期必要兼容
- 主要输入：
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/application/orchestration/`
  - 主回归测试
- 预期输出：
  - 一版更薄的 legacy executor 职责边界
  - 少量注释或文档说明“新逻辑不要再进这里”
  - 收官结论，说明 full cutover 还剩哪些少数复杂 effect
- 边界：
  - 不要求立即删除 executor
  - 不顺手做 DDD 大扫除
- 完成标准：
  - 旧执行器不再是默认扩展点
  - queue/orchestrator 成为明确主入口

### P2. Combat Queue Residual Closure（phase-2 后收尾）

- 总目标：
  - 在 `Combat Queue Full Cutover` 已收口之后，把 active `red/white` 里剩余仍依赖 fallback 的 effect 继续按小切片收口
  - 这一轮不再是新架构阶段，而是“剩余 effect 缩面 + 边界测试更新”
- 默认执行顺序：
  1. `Queue White Direct Effects Cutover V1`
  2. `Queue White Queue State Cutover V1`
  3. `Queue White Reposition Core Cutover V1`
  4. `Queue Red Complex Draw Branch Cutover V1`
  5. `Queue Final Active Fallback Boundary Pass V1`
- 当前状态（`2026-03-16`）：
  - 前 3 个白色 residual cutover 已完成
  - active white fallback 已基本收缩到 `swap_with_paper`
  - 默认下一步切 `Queue Red Complex Draw Branch Cutover V1`
- 总边界：
  - 不重写整个 combat runtime
  - 不做 UI 节点化
  - 不把 queue 泛化成脚本 DSL
  - 允许极少数跨上下文/剧情专用 effect 继续保留 fallback，但必须集中、可测、可点名

### P2. Queue White Direct Effects Cutover V1

- 目标：
  - 把白色里“不改敌人队列顺序、只做直接结算”的 effect 收进口到 planner
  - 优先覆盖：
    - `white_endpoint_damage`
    - `white_confidence_half_damage`
    - `white_reposition_summary`
    - `white_regulated_from_x`
    - `white_focus_pull_damage`
- 主要输入：
  - `contexts/combat/application/orchestration/effect_planner.py`
  - `contexts/combat/application/orchestration/action_executor.py`
  - `tests/combat/test_effect_planner.py`
  - 白色 focused/integration tests
- 预期输出：
  - 不新增脚本解释层，只新增收尾所需的最小 action 组合
  - 这些 effect 不再默认落回 legacy executor
- 边界：
  - 不在这一轮处理 `reposition` 本体
  - 不重写 pointer runtime
- 完成标准：
  - 以上 effect 进入 planned path
  - 原有白色行为回归不退化

### P2. Queue White Queue State Cutover V1

- 目标：
  - 把白色里“修改队列状态但不涉及复杂条件分支”的 effect 收进口到 queue
  - 优先覆盖：
    - `lock_queue`
    - `sequence_damage`
    - `queue_reverse`
- 主要输入：
  - `contexts/combat/application/orchestration/effect_planner.py`
  - `contexts/combat/application/orchestration/action_executor.py`
  - `tests/combat/test_action_queue.py`
  - `tests/combat/test_active_queue_boundaries.py`
- 预期输出：
  - 最小 queue-state actions
  - 顺序、tween metadata、状态标记仍保持现有语义
- 边界：
  - 不顺手吞掉 `reposition`
  - 不扩成通用队列编辑 DSL
- 完成标准：
  - `lock_queue / sequence_damage / queue_reverse` 不再依赖 fallback 主体
  - active 边界测试更新为新 planned path

### P2. Queue White Reposition Core Cutover V1

- 目标：
  - 单独处理 `reposition` 这条较重链路
  - 保留当前显式语义：
    - pointer target 校验
    - lock/limit 判定
    - tween metadata
    - reposition count
    - power hook
    - no-move bonus
- 当前不优先的原因：
  - 相比其他残余 effect，它涉及的运行时副作用最多
  - 更适合作为白色收尾的最后一刀
- 当前状态（`2026-03-16`）：
  - 已完成
  - `reposition` 已进入 planned path
  - 保留了 pointer target 校验、lock/limit、tween、reposition count、power hook、no-move bonus

### P2. Queue Red Complex Draw Branch Cutover V1

- 目标：
  - 收口红色剩余“先抽/先生成，再按结果分支”的复杂 effect
  - 优先覆盖：
    - `red_guess_draw_type`
    - `red_draw_then_random_damage_from_costs`
    - `red_random_hand_discount_then_discard`
    - `play_top_of_draw_then_exhaust`
- 边界：
  - 不扩成通用随机脚本系统
  - 优先保留当前 pile/随机语义一致

### P2. Queue Final Active Fallback Boundary Pass V1

- 目标：
  - 在上面几刀之后，重新扫描 active `red/white` effect 类型
  - 把“仍然允许 fallback 的最后列表”固化成文档和 focused tests
- 完成标准：
  - active fallback 面缩到极小且可枚举
  - 后续若继续推进，就不再叫“队列化主工程”，而是逐 effect 微收口

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

- `Combat Orchestration V1`
- `Seed Replay / Repro Tool v1`
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
