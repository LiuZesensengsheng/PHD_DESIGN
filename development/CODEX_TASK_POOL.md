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
  - `contexts/combat/domain/chore_host.py`
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

### P1. Chore Resolution Orchestration Cutover V1

- 目标：
  - 先把 `CombatChoreHost` 的 resolution actions 并入统一动作队列
  - 消除 `CombatModel._apply_chore_resolution_actions()` 里的大分支解释器
- 主要输入：
  - `contexts/combat/domain/chore_host.py`
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/mvc/factory.py`
- 预期输出：
  - `ChoreResolutionOrchestrator`
  - `CombatChoreResolutionAction -> CombatAction` 的映射层
  - 任务宿主倒计时 / 发布后续任务 / 变身 / 敌人 buff 的 focused tests
- 边界：
  - 不扩写新的 task host 抽象运动
  - 不把 card play 主路径一起大改
- 完成标准：
  - chore resolution 主路径切到新队列
  - 旧 `_apply_chore_resolution_actions()` 主解释逻辑删除或降为薄适配层
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
  - 先把 chore resolution 和 card play 两条最贵主路径切稳
  - 这一块适合在前几步稳定后继续收口

### P1. Campaign UI Handoff Orchestration（按时间优先级串行）

- 适用前提：
  - 当近期目标变成“让另一个人尽快安全接手 UI 开发”时，优先切换到这一组任务
  - 这组任务按时间优先级排序，不按架构完整度排序
  - 默认目标不是把 campaign 一次性重构成完整 DDD，而是先做出可交接的稳定中层
- 总目标：
  - 让 UI 开发主要停留在 `ui/`、`ui_runtime/`、`view` 与少量 presenter/adapter
  - 避免 UI 直接依赖 `CampaignState` 深层字段、散装 transition 写入和隐式流程顺序
  - 先做“可安全协作”的编排层，再继续决定后续是否深挖 DDD / 节点化
- 默认执行顺序：
  1. `Campaign UI Interaction Contract V1`
  2. `Campaign Modal Lock Contract V1`
  3. `Campaign Block Click Orchestrator V1`
  4. `Campaign End Turn Orchestrator V1`
  5. `Campaign Transition Request Contract V1`
  6. `Campaign Startup Seam Cleanup V1`
  7. `Campaign Event Input Split V1`
  8. `Campaign Thesis Submission Flow Cut V1`
  9. `Campaign Runtime UI Boundary V1`
  10. `Campaign UI Handoff Tests V1`
  11. `Campaign UI Handoff Doc V1`
  12. `Campaign Hotspot Defer List V1`
- 总边界：
  - 不要求先把 campaign 全量重写成完整 DDD
  - 不为了交接 UI 先全面铺开节点树
  - 不顺手做大规模视觉重构
  - 允许保留少量 legacy/mixed-mode 兼容层，但必须明确“UI 不该直接碰”
- 完成标准：
  - 新 UI 开发有一组稳定入口可依赖
  - 高风险主路径不再要求 UI 直接理解业务细节
  - 有最小测试和文档护栏支撑并行协作

### P1. Campaign UI Interaction Contract V1

- 目标：
  - 先定义 campaign UI 可以安全依赖的稳定入口与禁止越界边界
- 主要输入：
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/`
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `docs/development/ARCHITECTURE_RUNTIME_NODES_VS_DOMAIN_BOUNDARIES_V1.md`
- 预期输出：
  - 一份 UI 交互契约说明
  - 明确 UI 允许调用的入口，例如：
    - block click
    - end turn request
    - modal choice submit
    - runtime widget event
  - 明确禁止 UI 直接改写的 state/runtime 字段
- 边界：
  - 不先改视觉
  - 不先做大规模代码搬迁
- 完成标准：
  - 能明确回答“UI 层可以依赖什么，不可以依赖什么”
  - 后续任务可围绕这份契约继续收口

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_UI_INTERACTION_CONTRACT_V1.md`
  - 默认下一步：`Campaign Modal Lock Contract V1`

### P1. Campaign Modal Lock Contract V1

- 目标：
  - 把 campaign 里 modal 的 `show/hide/lock/unlock/event consume` 统一成一套规则
- 主要输入：
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/campaign_modal_dispatch_service.py`
  - `contexts/campaign/services/campaign_input_lock_service.py`
  - `contexts/campaign/services/modal_coordinator.py`
  - 相关 campaign modal tests
- 预期输出：
  - 一套显式 modal 锁协议
  - 一组 focused tests，覆盖事件消费顺序和 owner 语义
- 边界：
  - 不顺手改整套 UI 树
  - 不做 UI 视觉层重写
- 完成标准：
  - UI 协作者不需要猜 modal 锁语义
  - 底层点击/按键不会再绕过 blocking modal

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_MODAL_LOCK_CONTRACT_V1.md`
  - 已补 focused tests，覆盖 owner 语义、冲突拒绝和 reward/meeting prompt defer
  - 默认下一步：`Campaign Block Click Orchestrator V1`

### P1. Campaign Block Click Orchestrator V1

- 目标：
  - 把 `block click -> 业务判断 -> transition/request` 收成一个显式编排入口
- 主要输入：
  - `contexts/campaign/services/campaign_mouse_event_service.py`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/transition_helper.py`
  - `contexts/campaign/services/thesis_slice.py`
- 预期输出：
  - 一版 block-click orchestrator 或同级 use-case seam
  - UI event adapter 只负责把点击翻译成调用，不再自己承载业务分支
- 边界：
  - 不要求这一步处理全部 thesis 细节
  - 不顺手重写 hit-test/view math
- 完成标准：
  - block 点击主路径有单一入口
  - combat/event/non-combat 分支顺序更显式、更可测

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_BLOCK_CLICK_ORCHESTRATOR_V1.md`
  - 已补 focused tests，覆盖分支顺序、combat/event wiring 和事件层委派
  - 默认下一步：`Campaign End Turn Orchestrator V1`

### P1. Campaign End Turn Orchestrator V1

- 目标：
  - 把 `end turn` 推进顺序固定成 UI 可安全依赖的显式入口
- 主要输入：
  - `contexts/campaign/services/campaign_turn_orchestrator.py`
  - `contexts/campaign/services/end_turn_service.py`
  - `contexts/campaign/state.py`
- 预期输出：
  - 统一的 end-turn 请求入口
  - focused tests，保护 turn advance / board stabilize / side effects 顺序
- 边界：
  - 不顺手清空所有 campaign 旧逻辑
  - 不把 track geometry 和 DDL snake 全部改写
- 完成标准：
  - UI 只发起“结束回合”请求
  - 回合推进顺序不再散落在 UI 事件和 runtime update 中

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_END_TURN_ORCHESTRATOR_V1.md`
  - 已新增 `CampaignEndTurnOrchestrator`
  - 已补 focused tests，覆盖 direct/staged request、forced-DDL block 和 UI adapter 委派
  - 默认下一步：`Campaign Transition Request Contract V1`

### P1. Campaign Transition Request Contract V1

- 目标：
  - 统一 campaign 发往 combat / deck / ending / 其他 state 的 transition 请求格式
- 主要输入：
  - `contexts/campaign/services/transition_helper.py`
  - `contexts/campaign/services/campaign_route_resolution_service.py`
  - `contexts/shared/domain/contracts.py`
  - `contexts/campaign/state.py`
- 预期输出：
  - 一版稳定 transition request contract
  - focused tests，保护 request payload shape 和 startup return path
- 边界：
  - 不做跨全仓库 state machine 重构
  - 不顺手改 legacy 入口以外的所有调用方
- 完成标准：
  - UI 不再直接散装改 `persistent`
  - transition 数据 shape 可被文档和测试直接说明

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_TRANSITION_REQUEST_CONTRACT_V1.md`
  - 已新增 state-level request seams，覆盖 deck/event/combat/dev-combat/meeting/ending
  - UI/event adapter、meeting prompt、thesis event/combat 路径已切到统一 request seam
  - 已补 focused tests，覆盖 payload shape、state seam、startup return path 和 UI 委派
  - 默认下一步：`Campaign Startup Seam Cleanup V1`

### P1. Campaign Startup Seam Cleanup V1

- 目标：
  - 把 startup/hydration/effects 继续收口成 UI 不需要理解的后台流程
- 主要输入：
  - `contexts/campaign/services/campaign_startup_hydration_service.py`
  - `contexts/campaign/services/campaign_startup_effects_service.py`
  - `contexts/campaign/state.py`
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
- 预期输出：
  - 更清晰的 startup seam
  - 更少的 UI 启动期隐式副作用暴露给外层
- 边界：
  - 不要求 startup 逻辑完全纯化
  - 不顺手做存档系统重写
- 完成标准：
  - UI 开发不需要知道 hydration/effects 细节才能安全改启动表现

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_STARTUP_SEAM_CLEANUP_V1.md`
  - 已新增 `CampaignStartupOrchestrator`
  - `CampaignState.startup()` 已收成 lifecycle entrypoint + orchestrator mainline
  - 已补 focused tests，覆盖 startup 顺序和 startup-flag failure reset
  - 默认下一步：`Campaign Event Input Split V1`

### P1. Campaign Event Input Split V1

- 目标：
  - 把 campaign 里的“输入适配”与“业务编排”进一步拆开
- 主要输入：
  - `contexts/campaign/services/campaign_mouse_event_service.py`
  - `contexts/campaign/services/campaign_keyboard_event_service.py`
  - `contexts/campaign/services/campaign_ui_button_event_service.py`
  - `contexts/campaign/state.py`
- 预期输出：
  - presentation/event adapter 与 application orchestration 的更清晰边界
  - 少量 host/protocol 或 seam 方法，避免 event service 继续膨胀
- 边界：
  - 不要求一次性清掉全部 `self.state.*`
  - 不重写所有输入交互
- 完成标准：
  - pygame event handling 不再继续成为默认业务入口
  - 业务判断和 UI 事件翻译职责更清楚

- 当前状态（`2026-03-17`）：
  - 已完成
  - 产出：`docs/development/CAMPAIGN_EVENT_INPUT_SPLIT_V1.md`
  - 已新增 `CampaignEventInputOrchestrator`
  - mouse/button/keyboard adapter 中剩余 gossip/idea/meeting/choice-toggle intent 已切到 state seam
  - 已补 focused tests，覆盖 debounce、meeting entry、choice toggle 和 line-bubble 委派
  - 默认下一步：`Campaign Thesis Submission Flow Cut V1`

### P1. Campaign Thesis Submission Flow Cut V1

- 目标：
  - 把 thesis 里最常碰 UI 的提交/弹窗/确认链路单独收口
- 主要输入：
  - `contexts/campaign/services/thesis_meta_service.py`
  - `contexts/campaign/services/thesis_judgment_flow_service.py`
  - `contexts/campaign/services/thesis_publication_flow_service.py`
  - `contexts/campaign/state.py`
- 预期输出：
  - 一版 thesis submission/use-case seam
  - UI 不再直接依赖 `_blocks`、meta、persistent 的散装写入
- 边界：
  - 不要求 thesis 全链路聚合化完成
  - 不顺手做完整 thesis DDD 重构
- 完成标准：
  - 提交/确认/发表相关 UI 可通过统一入口驱动
  - 该链路的主要状态写入更集中

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_THESIS_SUBMISSION_FLOW_CUT_V1.md`
  - added `ThesisSubmissionFlowService`
  - `CampaignState` now exposes `check_and_prompt_thesis_submission()` and `request_thesis_submission_for_writing_block(block)`
  - `ThesisMetaService` and `ThesisSlice` now delegate thesis submission flow through the unified seam
  - focused regressions cover submission prompt, writing removal, review-chain activation, and publication-flow modal-lock compatibility

### P1. Campaign Runtime UI Boundary V1

- 目标：
  - 明确 runtime node/widget 与编排层之间的边界，便于别人专注做节点树/UI 表现
- 主要输入：
  - `contexts/campaign/ui_runtime/`
  - `contexts/campaign/state.py`
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `docs/development/ARCHITECTURE_RUNTIME_NODES_VS_DOMAIN_BOUNDARIES_V1.md`
- 预期输出：
  - runtime UI 责任说明
  - 约定 runtime widget 只负责节点、命中、局部动画、局部状态
- 边界：
  - 不要求把全 campaign UI 都迁成节点树
  - 不在这一轮扩成完整引擎层
- 完成标准：
  - 新 UI 开发者知道哪些逻辑该进 `ui_runtime/`，哪些不该进

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_RUNTIME_UI_BOUNDARY_V1.md`
  - added `tests/campaign/test_campaign_runtime_ui_boundary_contract.py`
  - documented `CampaignView` runtime hooks and the `ui_runtime` ownership line
  - protected local runtime-widget event/update/render delegation and phone-widget-local interaction
  - default next step: `Campaign UI Handoff Tests V1`

### P1. Campaign UI Handoff Tests V1

- 目标：
  - 用 focused tests 固定“交接 UI 所需”的高价值边界
- 主要输入：
  - campaign existing tests
  - block click / end turn / modal / transition 相关实现
- 预期输出：
  - 一组最小 handoff contract tests，覆盖：
    - block click
    - end turn request
    - modal lock/event consume
    - transition request payload
    - thesis submission 主链
- 边界：
  - 不把测试写成 UI-heavy 大集成
  - 不追求覆盖所有边角 case
- 完成标准：
  - UI 交接不再完全依赖口头说明
  - 高风险边界能被回归测试直接保护

- Status (`2026-03-17`):
  - complete
  - output: `tests/campaign/test_campaign_ui_handoff_contracts.py`
  - handoff pack now locks block click, end-turn request, modal-owner guard, transition request surface, and thesis submission seam
  - deeper existing tests remain as detailed behavior coverage; this pack is the compact UI-safe surface contract
  - default next step: `Campaign UI Handoff Doc V1`

### P1. Campaign UI Handoff Doc V1

- 目标：
  - 给后续 UI 开发者一份最短可执行的 handoff 文档
- 主要输入：
  - 上述收口结果
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `docs/development/ARCHITECTURE_BOUNDARIES.md`
- 预期输出：
  - 一页文档说明：
    - 能改什么
    - 不该碰什么
    - 从哪些入口接 UI
    - 哪些热点暂时保留 legacy
- 边界：
  - 不写成长篇架构论文
  - 不重复现有大段文档内容
- 完成标准：
  - 新 UI 协作者能快速开工
  - 项目方可以用这份文档做交接基线

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_UI_HANDOFF_DOC_V1.md`
  - the incoming UI developer now has one short handoff note covering safe work areas, host seams, contract tests, and stop-signs
  - default next step: `Campaign Hotspot Defer List V1`

### P1. Campaign Hotspot Defer List V1
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_HOTSPOT_DEFER_LIST_V1.md`
  - the remaining campaign legacy hotspots are now explicitly deferred instead of silently expanding scope
  - the `Campaign UI Handoff Orchestration` track can now be treated as closed for this phase

- 目标：
  - 明确哪些 campaign 热点先不收，避免 UI handoff 工程无限扩 scope
- 主要输入：
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
  - `contexts/campaign/services/thesis_meta_service.py`
  - `contexts/campaign/services/track_block_service.py`
  - 当前 UI handoff 主线成果
- 预期输出：
  - 一份 defer list，明确：
    - 哪些热点继续保留
    - 为什么暂缓
    - 什么信号出现时再继续收口
- 边界：
  - 不把 defer list 写成“永不处理”
  - 不因为热点存在就阻塞 UI 交接
- 完成标准：
  - 任务边界可控
  - 团队知道哪些 legacy 风险是已知且暂时接受的
	
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

### P2. Combat Chore Host V2（在 chore resolution cutover 后再继续）

- 目标：
  - 在现有 shared chore host、链式 `publish_chore`、DDL 压力表达已经可跑的基础上，把琐事宿主沉淀成更稳定的战斗中层能力
- 当前已落地基线：
  - `CombatChoreHost` 已挂到 `CombatState`
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
  - active white fallback 曾基本收缩到 `swap_with_paper`
  - `2026-03-17` 更新：
    - `Queue Red Complex Draw Branch Cutover V1` 已完成
    - `Queue Final Active Fallback Boundary Pass V1` 已完成
    - active fallback allowlist 已收口到仅剩 `thesis_swap_with_paper`
  - `2026-03-31` 更新：
    - `swap_with_paper` 已进入 planned path
    - active `red/white` fallback 边界扫描已收口到 `0`
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
- Status (`2026-03-17`):
  - complete
  - added dedicated queue actions for the remaining active red complex draw branch:
    - `RedGuessDrawTypeAction`
    - `RedRandomHandDiscountThenDiscardAction`
    - `RedDrawThenRandomDamageFromCostsAction`
    - `PlayTopOfDrawThenExhaustAction`
  - moved the following effect types onto the planned path:
    - `red_guess_draw_type`
    - `red_random_hand_discount_then_discard`
    - `red_draw_then_random_damage_from_costs`
    - `play_top_of_draw_then_exhaust`
  - kept legacy behavior aligned around:
    - draw-result branching and extra draw follow-up
    - random hand discount plus discard ordering
    - drawn-card base-cost burst damage
    - top-of-draw nested effect resolution followed by forced exhaust
  - added focused coverage in:
    - `tests/combat/test_action_queue.py`
    - `tests/combat/test_active_queue_boundaries.py`
  - validation:
    - `python -m pytest tests/combat/test_action_queue.py tests/combat/test_active_queue_boundaries.py -q`
    - `python -m pytest tests/combat/test_effect_planner.py tests/combat/test_card_play_orchestrator.py tests/combat/test_json_red_cards.py -q`
    - `python -m pytest tests/combat -q`
  - default next step: `Queue Final Active Fallback Boundary Pass V1`

### P2. Queue Final Active Fallback Boundary Pass V1

- 目标：
  - 在上面几刀之后，重新扫描 active `red/white` effect 类型
  - 把“仍然允许 fallback 的最后列表”固化成文档和 focused tests
- Status (`2026-03-17`):
  - complete
  - widened planned-path support for:
    - multi-target simple `status`
    - `red_scribble_finisher`
  - added executable active-card boundary scan in
    `tests/combat/test_active_queue_boundaries.py`
  - `2026-03-31` update:
    - `swap_with_paper` moved onto the planned path
    - final active fallback allowlist is now empty
  - future queue work should reopen per named residual effect, not as another
    broad queue-architecture phase
- 完成标准：
  - active fallback 面缩到极小且可枚举
  - 后续若继续推进，就不再叫“队列化主工程”，而是逐 effect 微收口

### P2. Thesis Aggregate Boundary Review

- Status (`2026-03-17`):
  - partial progress via `Thesis Write-Path Consolidation V1`
  - added `contexts/campaign/services/thesis_write_path_service.py`
  - `ThesisMetaService` now delegates thesis tier/meta/publication/submission-history writes to the shared write-path seam
  - `ThesisSubmissionFlowService` now records submitted rounds through the shared write seam instead of mutating meta inline
  - added focused coverage in `tests/campaign/test_thesis_write_path_service.py`
  - completed `Thesis Block Mutation Consolidation V1`
  - added `contexts/campaign/services/thesis_block_mutation_service.py`
  - `ThesisSubmissionFlowService`, `ThesisJudgmentFlowService`, and `ThesisRoundService` now route thesis block-list mutations through the shared block seam
  - added focused coverage in `tests/campaign/test_thesis_block_mutation_service.py`
  - completed `Thesis Verdict Follow-Up Contract V1`
  - added focused verdict-order contract coverage in `tests/campaign/test_thesis_verdict_follow_up_contract.py`
  - completed `Thesis Aggregate Invariant Tests V1`
  - added thesis aggregate consistency coverage in `tests/campaign/test_thesis_aggregate_invariants.py`
  - completed `Thesis State Host Narrowing V1`
  - added narrower host protocols for thesis write/block/submission/judgment seams in `contexts/campaign/services/campaign_service_protocols.py`
  - `ThesisSubmissionFlowService` and `ThesisJudgmentFlowService` no longer default to broad untyped `CampaignState` dependencies
  - default next step: reopen thesis aggregate review only when a new hotspot appears; otherwise continue with broader campaign aggregate review

- Recommended serial cuts:
  1. `Thesis Block Mutation Consolidation V1`
  2. `Thesis Verdict Follow-Up Contract V1`
  3. `Thesis Aggregate Invariant Tests V1`
  4. `Thesis State Host Narrowing V1`

#### P2. Thesis Block Mutation Consolidation V1

- Goal:
  - move thesis block-list mutation ownership out of `submission/judgment` flow services
  - centralize:
    - review-chain activation for submitted round
    - writing-block removal
    - round-block removal after verdict
    - next dormant round activation
- Main inputs:
  - `contexts/campaign/services/thesis_submission_flow_service.py`
  - `contexts/campaign/services/thesis_judgment_flow_service.py`
  - `contexts/campaign/services/thesis_round_service.py`
  - `contexts/campaign/state.py`
- Expected output:
  - one dedicated thesis block mutation seam/service
  - focused tests for thesis block activation/removal behavior
- Status (`2026-03-17`):
  - complete

#### P2. Thesis Verdict Follow-Up Contract V1

- Goal:
  - make thesis verdict follow-up order explicit after the block-mutation seam lands
  - protect ordering across:
    - verdict record
    - tag writes
    - block mutation
    - next-round activation
    - publication/combat follow-up
- Main inputs:
  - `contexts/campaign/services/thesis_judgment_flow_service.py`
  - `tests/campaign/test_thesis_judgment_flow_service.py`
- Expected output:
  - thinner, better-ordered verdict application mainline
  - focused regression around reject/accept/major/minor sequencing
- Status (`2026-03-17`):
  - complete

#### P2. Thesis Aggregate Invariant Tests V1

- Goal:
  - lock the current thesis aggregate boundaries with executable contract tests
- Main inputs:
  - `tests/campaign/test_thesis_*`
  - `tests/campaign/test_campaign_ui_handoff_contracts.py`
- Expected output:
  - focused invariants covering tier/runtime/meta/block consistency
- Status (`2026-03-17`):
  - complete

#### P2. Thesis State Host Narrowing V1

- Goal:
  - reduce thesis services' reliance on broad `CampaignState` access
- Main inputs:
  - `contexts/campaign/services/campaign_service_protocols.py`
  - `contexts/campaign/services/thesis_*.py`
- Expected output:
  - narrower host protocols around the matured thesis seams
- Status (`2026-03-17`):
  - complete

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
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_AGGREGATE_CANDIDATE_REVIEW_V1.md`
  - conclusion:
    - `Campaign` remains a shell/orchestration owner, not a promoted aggregate root
    - `Task Area` remains a real subdomain but is not ready for full aggregate promotion
    - the closest mature aggregate candidate is track-local `Thesis` progression, not the whole campaign shell
  - small seam landed:
    - `CampaignState.get_campaign_blocks_for_track(track_index)`
    - `ThesisWritePathService` and `ThesisMetaService` now use the track-local read seam instead of open-coded full-list scans
  - focused validation:
    - `python -m pytest tests/campaign/test_thesis_write_path_service.py tests/campaign/test_thesis_submission_flow_service.py tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_guardrail_flow_contracts.py tests/campaign/test_campaign_dependency_narrowing_services.py tests/campaign/test_campaign_ui_state_contracts.py -q`
  - default next step: `Aggregate Invariant Tests V1`

### P2. Campaign vs Task Area Boundary V1

- Goal:
  - define the architectural split between `Campaign` as shell and `Task Area`
    as the campaign scheduling subdomain
  - make `track/task line/block/event bubble` ownership explicit before further
    board-side refactors
- Main inputs:
  - `contexts/campaign/state.py`
  - `contexts/campaign/domain/block_dto.py`
  - `contexts/campaign/services/track_block_service.py`
  - `docs/design/campaign/GANTT_TASKS_EVENTS.md`
  - `docs/design/PAPER_LINE_TRACK_SERVICE_SPEC.md`
  - `docs/development/CAMPAIGN_UI_HANDOFF_DOC_V1.md`
- Expected output:
  - one boundary RFC
  - one recommended vocabulary map
  - one small-step follow-up sequence instead of a vague aggregate rewrite
- Boundaries:
  - do not force a full `Track` aggregate rewrite now
  - do not reopen broad UI handoff scope
  - do not pretend `Task Area` is a sibling runtime state
- Completion criteria:
  - can explain clearly:
    - what belongs to `Campaign`
    - what belongs to `Task Area`
    - why `Event Bubble` is not a `Block`
    - why thesis is a specialization on top of task-area primitives

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_TASK_AREA_BOUNDARY_V1.md`
  - recommendation: treat `Campaign` as outer shell and `Task Area` as named
    scheduling subdomain inside campaign
  - default next step: `Task Area Terminology Alignment V1`

### P2. Task Area Terminology Alignment V1

- Goal:
  - align active docs and runtime comments around:
    - `Campaign`
    - `Task Area`
    - `Task Line / Track`
    - `Block`
    - `Event Bubble`
- Main inputs:
  - `docs/development/CAMPAIGN_TASK_AREA_BOUNDARY_V1.md`
  - active campaign development docs
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/track_block_service.py`
- Expected output:
  - small terminology cleanup pass
  - no behavioral change
- Boundaries:
  - do not mass-rename every historical design doc
  - do not introduce new runtime abstractions yet
- Completion criteria:
  - current architecture docs and the most active runtime files stop using
    `campaign` as the name for both shell and task-board subdomain

- Status (`2026-03-17`):
  - complete
  - aligned active docs:
    - `docs/development/CAMPAIGN_UI_HANDOFF_DOC_V1.md`
    - `docs/development/CAMPAIGN_HOTSPOT_DEFER_LIST_V1.md`
    - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
  - aligned runtime terminology comments/docstrings:
    - `contexts/campaign/state.py`
    - `contexts/campaign/services/track_block_service.py`
    - `contexts/campaign/services/campaign_visible_blocks_service.py`
    - `contexts/campaign/services/line_bubble_service.py`
  - kept scope documentation-only; no behavior change
  - default next step: `Task Area Write-Path Contract V1`

### P2. Task Area Write-Path Contract V1

- Goal:
  - identify and tighten the real task-area write paths around block mutation
    and board stabilization
- Main inputs:
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/track_block_service.py`
  - task-area callers in thesis/meeting/startup flows
- Expected output:
  - one explicit write-path note or seam set for task-area mutations
  - smaller risk of ad hoc `_blocks` mutation spreading
- Boundaries:
  - do not force repository-style abstraction yet
  - do not rewrite DDL snake or fusion rules for theory's sake
- Completion criteria:
  - can point to the preferred task-area mutation entrypoints for the
    highest-frequency writers

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_TASK_AREA_WRITE_PATH_CONTRACT_V1.md`
  - added state seams:
    - `get_next_task_area_track_index()`
    - `apply_task_area_blueprint_plans(plans)`
  - migrated external writers:
    - `contexts/campaign/services/thesis_blueprint_app_service.py`
    - `contexts/campaign/services/campaign_keyboard_event_service.py`
  - added focused coverage:
    - `tests/campaign/test_task_area_write_path_contract.py`
    - `tests/campaign/test_campaign_keyboard_event_service.py`
  - default next step: `Task Area Invariant Tests V1`

### P2. Task Area Invariant Tests V1

- Goal:
  - lock the current task-area invariants with focused tests
- Main inputs:
  - `contexts/campaign/services/track_block_service.py`
  - campaign block and line-bubble tests
- Expected output:
  - focused coverage for:
    - no logical overlap
    - trailing DDL enforcement
    - fusion safety
    - event-bubble vs block separation
- Boundaries:
  - do not expand into UI-heavy integration tests
  - do not wait for a full aggregate rewrite to add protection
- Completion criteria:
  - future task-area refactors can fail fast on broken board invariants

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_TASK_AREA_INVARIANT_TESTS_V1.md`
  - added focused coverage:
    - `tests/campaign/test_task_area_invariants.py`
  - invariant pack now explicitly protects:
    - no logical overlap on the same track
    - trailing DDL per task line
    - event-bubble vs block separation
  - default next step: `Task Area Host Narrowing V1`

### P2. Task Area Host Narrowing V1

- Goal:
  - narrow mature task-area services away from broad `CampaignState` access
    where the seam is already stable
- Main inputs:
  - `contexts/campaign/services/track_block_service.py`
  - `contexts/campaign/services/line_bubble_service.py`
  - `contexts/campaign/state.py`
- Expected output:
  - narrower host/seam notes or protocols for task-area services with clear ROI
- Boundaries:
  - do not widen into a fake universal facade
  - stop if the protocol starts mirroring too much internal state
- Completion criteria:
  - at least one task-area hotspot becomes easier to reason about without
    increasing abstraction noise

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_TASK_AREA_HOST_NARROWING_V1.md`
  - added narrower task-area host protocols in:
    - `contexts/campaign/services/campaign_service_protocols.py`
  - narrowed mature services:
    - `contexts/campaign/services/line_bubble_service.py`
    - `contexts/campaign/services/thesis_blueprint_app_service.py`
  - added thin host seams on `CampaignState`:
    - `lock_gossip_inputs()`
    - `unlock_gossip_inputs()`
    - `ensure_task_area_thesis_meta(...)`
    - `clear_saved_thesis_tier_for_track(...)`
  - added focused stub-host coverage:
    - `tests/campaign/test_campaign_dependency_narrowing_services.py`
  - default next step: `Track Aggregate Re-evaluation V1`

### P2. Track Aggregate Re-evaluation V1

- Goal:
  - revisit whether a true `Track` aggregate is worth doing after the task-area
    naming, write paths, and invariants are clearer
- Current lower-priority reason:
  - the current task-board hotspot is still geometry-heavy
  - the team now needs clearer boundaries more than deeper purity
  - this decision should be made after smaller task-area cuts, not before

- Status (`2026-03-17`):
  - complete
  - output: `docs/development/TRACK_AGGREGATE_REEVALUATION_V1.md`
  - recommendation:
    - do not promote a full `Track` aggregate now
    - keep the current incremental `Task Area` model
    - only revisit aggregate promotion when explicit track identity or shared
      lane-local writer pressure appears
  - default next step:
    - keep task-area work on seam-driven maintenance for now
    - do not open a full aggregate rewrite without a new trigger

### P2. Campaign Orchestration Closure V1

- Goal:
  - close the current campaign orchestration phase around shell invariants,
    encounter request safety, and small session-access seams so follow-up work
    can stay UI-first instead of reopening broad architecture churn
- Recommended serial cuts:
  1. `Orchestration Aggregate Invariants V1`
  2. `Encounter Contract Expansion V1`
  3. `Persistent / Session Access Cleanup V1`
  4. `Orchestration Closure Doc V1`
  5. `Focused Smoke Pack V1`
- Status (`2026-03-17`):
  - complete
  - outputs:
    - `docs/development/CAMPAIGN_ORCHESTRATION_CLOSURE_V1.md`
    - `docs/development/CAMPAIGN_ORCHESTRATION_SMOKE_PACK_V1.md`
  - default next step:
    - treat campaign orchestration as closed for this phase
    - reopen only when a concrete seam trigger appears during UI or content work

#### P2. Orchestration Aggregate Invariants V1

- Goal:
  - lock the current campaign-shell orchestration boundaries with executable
    invariants instead of relying on recent memory
- Main inputs:
  - `contexts/campaign/state.py`
  - startup/cleanup/route-resolution tests
  - thesis combat-sync and publication follow-up flows
- Expected output:
  - one compact invariant pack around startup-cleanup roundtrip, one-shot route
    resolution, and consume-once thesis sync behavior
- Boundaries:
  - do not wait for a formal aggregate root rewrite
  - do not turn this into a UI-heavy end-to-end suite
- Status (`2026-03-17`):
  - complete
  - added `tests/campaign/test_campaign_orchestration_aggregate_invariants.py`
  - locked:
    - cleanup/startup shell roundtrip
    - route-resolution consume-once behavior across startup + cleanup
    - thesis combat-sync apply-once behavior

#### P2. Encounter Contract Expansion V1

- Goal:
  - tighten the campaign-side encounter request contract around block click,
    state-level combat requests, and transition payload shape
- Main inputs:
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/campaign_block_click_orchestrator.py`
  - `contexts/shared/domain/contracts.py`
- Expected output:
  - trimmed and validated encounter ids before combat transition requests mutate
    shell state
  - widened request-contract regressions for invalid encounter input
- Boundaries:
  - do not reopen combat content validation scope
  - keep this at the campaign orchestration boundary, not a new cross-repo
    encounter initiative
- Status (`2026-03-17`):
  - complete
  - `CampaignState.request_combat_transition()` now rejects blank encounter ids
    before mutating `pending_block_id`
  - added request-contract coverage for trimmed and rejected encounter ids in:
    - `tests/campaign/test_campaign_transition_request_contract.py`

#### P2. Persistent / Session Access Cleanup V1

- Goal:
  - move a few remaining orchestration-phase session writes off ad hoc service
    access and behind thin host/store intent seams
- Main inputs:
  - `contexts/campaign/domain/session_store.py`
  - `contexts/campaign/services/meeting_flow_app_service.py`
  - `contexts/campaign/services/thesis_publication_flow_service.py`
  - `contexts/campaign/services/thesis_slice.py`
  - `contexts/campaign/state.py`
- Expected output:
  - narrower service responsibilities around:
    - meeting-turn handled persistence
    - innovation placeholder selection persistence
    - thesis combat-sync consume-once access
- Boundaries:
  - do not introduce repository-style abstractions
  - prefer one or two explicit shell/store seams over a fake universal facade
- Status (`2026-03-17`):
  - complete
  - added thin shell/store seams for:
    - meeting-turn handled persistence
    - innovation placeholder choice recording
    - thesis combat-sync payload consumption
  - widened focused coverage in:
    - `tests/campaign/test_campaign_session_store.py`
    - `tests/campaign/test_meeting_flow_app_service.py`
    - `tests/campaign/test_campaign_dependency_narrowing_services.py`

#### P2. Orchestration Closure Doc V1

- Goal:
  - write down the stable campaign orchestration surface, deferred hotspots, and
    explicit reopen triggers so future UI work does not rely on chat memory
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_ORCHESTRATION_CLOSURE_V1.md`

#### P2. Focused Smoke Pack V1

- Goal:
  - define the small regression pack that should be the default confidence check
    for future campaign orchestration touches
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/CAMPAIGN_ORCHESTRATION_SMOKE_PACK_V1.md`

### P2. DDD Layer Planning RFC V1

- Goal:
  - decide what the repo should mean by "DDD layer progress" after the campaign
    orchestration closure and combat queue cutover work
  - avoid mixing action queue, aggregate promotion, and repository scope into
    one oversized cleanup phase
- Main inputs:
  - `docs/development/CAMPAIGN_ORCHESTRATION_CLOSURE_V1.md`
  - `docs/development/TRACK_AGGREGATE_REEVALUATION_V1.md`
  - `docs/development/ARCHITECTURE_BOUNDARIES.md`
  - `contexts/combat/application/orchestration/*`
  - `contexts/shared/save/*`
  - `contexts/campaign/services/thesis_*`
  - `contexts/campaign/services/track_block_service.py`
- Expected output:
  - one L3 RFC that answers:
    - how to treat action queue maturity
    - which aggregate candidates are real
    - where repositories are worth keeping narrow
    - what the phased DDD order should be if reopened later
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/DDD_LAYER_PLANNING_V1.md`
  - recommendation:
    - treat combat queueing as a bounded sequencing substrate, not the main DDD blocker
    - keep repositories narrow and IO-focused
    - treat aggregate work as selective and trigger-driven
  - recommended future DDD order if reopened:
    1. `Repository Boundary Cleanup V1`
    2. `Campaign Aggregate Candidate Review`
    3. `Aggregate Invariant Tests V1`
    4. `State Host Facade V1`
    5. reopen thesis/task-area aggregate work only on a new hotspot
  - default next step:
    - keep the overall project priority UI-first
    - do not open queue + aggregate + repository work as one combined epic

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
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/REPOSITORY_BOUNDARY_CLEANUP_V1.md`
  - kept `SaveRepository` / `FileSaveRepository` as the real shared repository boundary
  - kept `CampaignSessionStore` as a typed session helper/store seam, not a universal repository candidate
  - `GameStateMachine` save-slot operations now use an injectable `save_slot_service_factory` seam instead of open-coded `FileSaveRepository(...)` construction in each method
  - added focused seam coverage in `tests/shared/test_state_machine_save_slots.py`
  - default next step: `Campaign Aggregate Candidate Review`

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
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/AGGREGATE_INVARIANT_TESTS_V1.md`
  - added focused aggregate-candidate coverage in:
    - `tests/campaign/test_campaign_aggregate_invariants.py`
  - locked the current high-value invariants around:
    - cleanup/startup roundtrip preserving multi-track thesis partition
    - track-local thesis tier writes staying isolated across tracks
    - thesis verdict follow-up mutating only the target track
  - explicitly built on the existing invariant packs:
    - `tests/campaign/test_campaign_orchestration_aggregate_invariants.py`
    - `tests/campaign/test_task_area_invariants.py`
    - `tests/campaign/test_thesis_aggregate_invariants.py`
  - focused validation:
    - `python -m pytest tests/campaign/test_campaign_aggregate_invariants.py tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py tests/campaign/test_task_area_invariants.py -q`
  - default next step: `State Host Facade V1`

### P2. State Host Facade V1

- 目标：
  - 为高复杂 campaign service 提供更窄的 host / facade，减少 `state: Any` 成为默认依赖
- 当前不优先的原因：
  - 需要先通过 `依赖倒置与编排层收口 v1` 找到最高 ROI 的切口
  - 还不适合全量统一
- Status (`2026-03-17`):
  - complete
  - output: `docs/development/STATE_HOST_FACADE_V1.md`
  - narrowed `ThesisMetaService` onto a focused `ThesisMetaHost` instead of broad `state: Any`
  - added thin `CampaignState` thesis facade seam methods for:
    - submission completion delegation
    - publication modal delegation
    - innovation placeholder follow-up delegation
  - kept `TrackBlockService` and full campaign-wide facade work deferred
  - added focused stub-host coverage in:
    - `tests/campaign/test_campaign_dependency_narrowing_services.py`
  - focused validation:
    - `python -m pytest tests/campaign/test_campaign_dependency_narrowing_services.py tests/campaign/test_thesis_write_path_service.py tests/campaign/test_thesis_submission_flow_service.py tests/campaign/test_thesis_publication_flow_service.py tests/campaign/test_thesis_judgment_flow_service.py tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_guardrail_flow_contracts.py tests/campaign/test_thesis_innovation_placeholder_flow.py -q`
  - default next step:
    - treat the current DDD follow-up sequence as closed for this phase
    - reopen only on a new hotspot trigger

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

### P1. Combat Analysis Capability Iteration V1（按顺序串行）

- 适用前提：
  - 当前 `tools/combat_analysis/` 已有稳定主 benchmark：
    - 正样本 `14/14`
    - 负样本 `13/13`
    - near-neighbor `12/12`
    - 主 benchmark 当前 `PASS`
  - 当前 `relic-aware` 仍处于诊断层：
    - 严格通过 `13/13`
    - 新增预期 package/axis 恢复 `11/13`
    - cross-density 提升 `12/13`
  - exploratory 层已接入：
    - upgrade-sensitive `4/4`
  - 因此下一阶段不应该直接扩大功能面，而应该先把“遗物诊断 -> 表达增强 -> 分层 benchmark -> 扩验证集”做扎实
- 总目标：
  - 让 `combat_analysis` 从“能解释一批卡组”推进到“能稳定解释遗物修正、时序窗口与近邻差异”
  - 先提升模型可信度，再进入敌人压力与推荐系统
- 默认执行顺序：
  1. `Combat Analysis Relic Failure Analysis V1`
  2. `Combat Analysis Relic Calibration Round 1`
  3. `Combat Analysis Semantic / Timing Expressivity V1`
  4. `Combat Analysis Benchmark Layering V1`
  5. `Combat Analysis Validation Expansion V1`
  6. `Combat Analysis Enemy Pressure Profile V1`
  7. `Combat Analysis Matchup Analysis V1`
  8. `Combat Analysis Recommendation V1`
- 总边界：
  - 不在 relic-aware 仍未稳定前，把它并入主硬门槛
  - 不在验证集还偏薄时，急着扩太多新机制
  - 不把遗物简单当成普通手牌；继续坚持
    `persistent pseudo-card + possible rule modifier`
  - 推荐系统放到最后，建立在稳定 benchmark 与 matchup 能力之上

#### P1. Combat Analysis Relic Failure Analysis V1

- 目标：
  - 把当前 relic-aware 未严格通过的 `10/13` case 做稳定误差拆解
  - 明确失败主因到底是：
    - 缺包
    - 缺轴
    - 时序表达不够
    - pseudo-card 权重不对
    - 规则修改器建模不足
- 主要输入：
  - `tools/combat_analysis/reports/relic_samples/__init__.py`
  - `tools/combat_analysis/adapters/sts_reference/relic_sample_decks.py`
  - `tools/combat_analysis/adapters/sts_reference/core_relic_links.py`
  - `tools/combat_analysis/reports/generated/sts1_ironclad_full_v1_snapshot.json`
- 预期输出：
  - 一份稳定的 relic failure report
  - 一组 failure type 统计
  - 每个失败 case 的主因标注与短解释
- 边界：
  - 先不调权重
  - 先不扩样本
  - 先做“为什么没过”的稳定解释层
- 完成标准：
  - `13` 个 relic sample 全部有稳定失败归因
  - `10/13` 失败 case 至少能归并成少数可行动类型
  - 报告可以直接回答“缺包 / 缺轴 / 时序 / pseudo-card / rule modifier”几个问题
- 当前状态（`2026-04-05`）：
  - 已完成
  - 产出：`tools/combat_analysis/reports/relic_failures/__init__.py`
  - 已形成稳定 failure report，能按缺包 / 缺轴 / 时序 / rule modifier / pseudo-card weight 做归因

#### P1. Combat Analysis Relic Calibration Round 1

- 目标：
  - 校准遗物 pseudo-card 与 rule-modifier 的第一轮建模
  - 把 relic-aware 严格通过从 `3/13` 提到至少 `8/13`
- 重点对象：
  - `Snecko Eye`
  - `Runic Pyramid`
  - `Calipers`
  - `Necronomicon`
  - `Medical Kit`
  - `Mark of Pain`
- 重点问题：
  - 这些遗物很多不是“纯收益牌”
  - 更像“规则修改器 + 持续环境”
- 主要输入：
  - `tools/combat_analysis/adapters/sts_reference/core_relic_links.py`
  - `tools/combat_analysis/adapters/sts_reference/data/sts1_ironclad_core_relic_links_v1.json`
  - `tools/combat_analysis/reports/relic_samples/__init__.py`
- 预期输出：
  - 更新后的 relic pseudo-card 投影
  - 更明确的 rule-modifier 标记与解释
  - relic-aware 结果回升报告
- 边界：
  - 不把所有遗物一起纳入
  - 只调核心机制遗物
  - 不动主 benchmark 硬门槛
- 完成标准：
  - 严格通过至少 `8/13`
  - 失败 case 不再集中卡在明显漏语义上
  - cross-density / confidence 的回升方向与语义改善一致
- 当前状态（`2026-04-05`）：
  - 已完成
  - 核心遗物 pseudo-card + rule-modifier 校准已落地
  - 当前 strict pass 已提升到 `13/13`

#### P1. Combat Analysis Semantic / Timing Expressivity V1

- 目标：
  - 强化模型对“包识别对了，但 confidence / cross-density 不合理”的解释力
  - 提高时序型遗物、延迟收益型构筑、规则改写型联动的可读性
- 优先补的语义：
  - `frontload`
  - `scaling`
  - `utility`
  - `multiplier`
  - `payoff_support`
  - `highroll`
- 优先补的时序能力：
  - 跨回合保留
  - 费用压缩
  - 留牌
  - 延迟收益
  - 条件成立窗口
- 主要输入：
  - `tools/combat_analysis/model/`
  - `tools/combat_analysis/projections/`
  - `tools/combat_analysis/analysis/`
  - relic failure / calibration 结果
- 预期输出：
  - 更稳定的语义轴或状态表达
  - 补充的 near-neighbor / relic-aware 解释能力
  - 对特殊时序联动更合理的 confidence / density 变化
- 边界：
  - 不先扩敌人
  - 不直接跳推荐系统
  - 不为了覆盖率引入假精确
- 完成标准：
  - 关键遗物样本不再频繁出现“识别到了壳，但没识别到真正收益窗口”
  - 近邻卡与时序卡的分离更稳定
- 当前状态（`2026-04-05`）：
  - 已完成
  - 已补 `frontload / scaling / utility / multiplier / payoff_support / highroll` 的表达承载
  - 已补 supporting packages / supporting axes，用于更好描述资源、留牌、控制等二级但关键收益

#### P1. Combat Analysis Benchmark Layering V1

- 目标：
  - 把 benchmark 明确拆成三层，避免探索性样本把主 gate 拖红
- 分层目标：
  - `core benchmark`
    - 主硬门槛，继续保持稳定
  - `relic benchmark`
    - 次级门槛，先做 tuning dashboard
  - `exploratory benchmark`
    - 新机制、新样本、新假设，不并入主 gate
- 主要输入：
  - `tools/combat_analysis/reports/snapshots/__init__.py`
  - `tools/combat_analysis/reports/markdown/__init__.py`
  - `tools/combat_analysis/reports/html/__init__.py`
  - `tests/toolkit/combat_analysis/test_reports.py`
- 预期输出：
  - 分层 benchmark summary
  - 更清晰的 snapshot 结构
  - HTML / markdown 中的分层展示
- 边界：
  - 不改变主 benchmark 的通过标准
  - 不把 exploratory 失败解释成主模型退化
- 完成标准：
  - 主 benchmark 继续稳定 `PASS`
  - relic-aware 有自己的次级门槛与趋势显示
  - exploratory 样本可以持续增加而不污染主 gate
- 当前状态（`2026-04-05`）：
  - 已完成
  - snapshot / markdown / html 已形成 `core / relic / exploratory` 三层 benchmark 展示
  - relic benchmark 保持次级门槛，exploratory benchmark 保持独立探索层

#### P1. Combat Analysis Validation Expansion V1

- 目标：
  - 先扩验证集，而不是先扩功能面
  - 先证明模型更可信，再谈更广覆盖
- 重点扩充：
  - 更多正样本
  - 更像真实构筑的负样本
  - upgrade 敏感样本
  - 更多 near-neighbor 对比
- 主要输入：
  - `tools/combat_analysis/adapters/sts_reference/data/`
  - `tools/combat_analysis/reports/snapshots/__init__.py`
  - `tests/toolkit/combat_analysis/`
- 预期输出：
  - 更厚的样本库
  - 稳定 benchmark 回归层
  - 更新后的 snapshot JSON 与 HTML 报告
- 边界：
  - 不为了凑数量降低样本质量
  - 正负样本都要保留明确的解释意图
- 完成标准：
  - core / relic / exploratory 三层都有明确样本边界
  - upgrade-sensitive 与 near-neighbor 成为稳定验证维度
- 当前状态（`2026-04-05`）：
  - 已完成
  - 验证集已扩到 `14` 正样本、`13` 负样本、`12` near-neighbor、`4` upgrade-sensitive
  - 参考报告产物已刷新为新的 snapshot JSON + 单页 HTML

#### P2. Combat Analysis Enemy Pressure Profile V1

- 目标：
  - 开始把敌人看成 pressure object，而不是单纯敌人列表
- 主要输入：
  - `tools/combat_analysis/model/enemies/`
  - `tools/combat_analysis/model/encounters/`
  - 现有 pressure / state / axis 语言
- 预期输出：
  - 第一版 enemy pressure profile
  - hallways / elites / bosses 的基础压力维度
- 边界：
  - 先做压力画像，不先做完整敌人模拟
- 完成标准：
  - 可以用统一语言描述敌人给卡组施加的关键压力
- 当前状态（`2026-04-05`）：
  - 已完成
  - 已新增 `tools/combat_analysis/adapters/sts_reference/enemy_pressure.py`
  - 已形成首批 STS enemy pressure profile 种子集

#### P2. Combat Analysis Matchup Analysis V1

- 目标：
  - 让 deck/package 可以与 pressure profile 做 matchup 分析
- 主要输入：
  - deck identity / package closure
  - enemy pressure profile
- 预期输出：
  - deck/package vs pressure 的 matchup 结论
  - 一组可解释的“擅长 / 害怕”结构结论
- 边界：
  - 先做结构 matchup，不做复杂对局模拟器
- 完成标准：
  - 已知流派能在压力维度上表现出合理强弱差异
- 当前状态（`2026-04-05`）：
  - 已完成
  - 已新增 `tools/combat_analysis/analysis/matchup/__init__.py`
  - 现阶段采用统一 axis 空间 + state coverage 的结构型 matchup 分析

#### P2. Combat Analysis Recommendation V1

- 目标：
  - 在 benchmark、relic、matchup 都稳定后，再做推荐系统
- 主要能力：
  - draft recommendation
  - pivot recommendation
  - relic-aware 组合建议
  - pressure-aware 风险提醒
- 主要输入：
  - validation benchmark
  - relic-aware identity
  - matchup analysis
- 预期输出：
  - 第一版推荐策略
  - 与结构风险绑定的解释型建议
- 边界：
  - 推荐必须建立在已经验证的结构能力上
  - 不用“看起来聪明”的启发式替代 benchmark
- 完成标准：
  - 推荐结论能追溯到 package / relic / pressure 证据
- 当前状态（`2026-04-05`）：
  - 已完成当前轮
  - draft recommendation 已接入 enemy-pressure-aware pick 解释
  - 后续优先级转向扩大样本库与继续校准遗物/敌人覆盖面，而不是提前扩推荐花样

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
