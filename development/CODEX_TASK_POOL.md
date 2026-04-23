# Codex 任务池

## 用途

这份文档只记录一类事情：

- 哪些任务适合 Codex 独立连续执行几小时
- 这些任务需要什么输入
- 产出是什么
- 哪些任务已经可以直接做，哪些还需要先继续定
- 已完成的大块任务只保留热区索引，详细记录移动到 `docs/development/task_pool_archive/`

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
  - `2026-03-16` 判定更新：`combat orchestration v1` 已可视为完成，后续转入更小切片的 chore / card-play / planner / policy 收口
  - v1 之后的剩余 fallback 面默认只包括条件型、属性来源型和其他小众复杂效果

### P1. Combat Global Compat-Zero (Engineering Surface)

- 目标：
  - 在已完成 `runtime-mainline compat-zero` 的基础上，继续清掉 combat
    剩余的工程兼容层
  - 把 `CombatModel` / MVC facade、session underscore compat、`state -> turn_context`
    桥、低价值 test/import shim 分阶段收口
  - 让后续 automation 可以沿着稳定 backlog 持续推进，而不是每次重新判断边界
- Current execution rules:
  - follow `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
  - default target is `engineering zero`, not `strict historical/save zero`
  - do not start long-running execution until the decision gates in that doc are accepted
  - keep this work separate from:
    - red runtime/content bug fixes
    - animation/video blocking semantics
    - `combat_view` behavior changes
    - save schema redesign
  - once decisions are accepted, execute serially:
    - `G1` MVC facade plane removal
    - `G2` session wrapper tightening
    - `G3` `turn_context` bridge collapse
    - `G4` low-value test/import shim cleanup
    - `G5` retained adapter review
- Main inputs:
  - `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
  - `docs/development/COMBAT_RUNTIME_SURFACE_INVENTORY_V1.md`
  - `docs/development/COMBAT_AUTOMATION_BACKLOG_V1.md`
  - `contexts/combat/`
  - `tests/combat/`
- 预期输出：
  - combat 全域兼容层的分阶段删除或显式保留决策
  - automation-safe backlog + stop condition + validation pack
  - 更薄的 combat engineering surface
- 边界：
  - 不把 save backward compatibility 当作默认首轮删除目标
  - 不顺手处理 unrelated red content failures
  - 不混入视觉或动画实现
  - 不在同一批里同时做多个高风险兼容层大删改
- 当前阶段判断：
  - 规划文档已建立
  - `2026-04-23` 已接受 `Engineering Zero` 决策包，见 `docs/pm/DECISION_LOG.md`
  - 默认自动化执行顺序为 `G1 -> G2 -> G3 -> G4 -> G5`
  - `2026-04-23` `G1` 已完成：
    - `CombatModel` / `mvc.factory` 已物理删除
    - live runtime/test/script import surface 已归零
    - 仅保留两处测试中的 removal guard 文本断言
  - `2026-04-23` `G2` 已完成：
    - `CombatSession` underscore compat wrapper 已物理删除
    - live `session._...` wrapper read surface 已归零
    - guard 已更新为禁止 wrapper 静默回流
  - `2026-04-23` `G3` 第一小批已完成：
    - `action_executor.py`、`pointer_queue_white.py`、`misc.py`、
      `pile_service.py` 的本批 runtime 读写已改为直接走
      `state.turn_context`
    - 对应测试与 guard 已收紧到同一基线
  - `2026-04-23` `G3` 第二小批已完成：
    - `enemy_tween_planner.py` 已改为直接写 `state.turn_context`
    - `CombatState` 上的 `enemy_tween_*` 桥属性已物理删除
    - `enemy cleanup / tween planner` 相关测试与 guard 已同步收口
  - `2026-04-23` `G3` 第三小批已完成：
    - `player.py`、`powers.py`、`effects/base.py`、
      `effects/impl/red.py`、`effects/impl/pile.py`、
      `traits_demo_impl.py` 的本批 helper/fallback 已改为优先创建并使用
      `state.turn_context`
    - `CombatState` 上一批非 tween bridge 属性已物理删除：
      - `draw_locked`
      - `reposition_count_this_turn`
      - `reposition_limit_per_turn`
      - `frontier_batch_counter`
      - `red_extra_draw_context`
      - `red_frontier_damage_bonus_current_play`
      - `red_offcolor_damage_bonus_current_play`
      - `force_frontier_next_cards`
      - `traits_double_current_effects`
      - `scribble_played_this_turn`
    - core-state contract 与 compat-zero guard 已同步到新基线
  - `2026-04-23` `G3` 第四小批已完成：
    - `render_state_assembler.py` 已改为从 `state.turn_context` 读取
      `lock_queue_active`
    - `CombatState.lock_queue_active` bridge 已物理删除
    - render-state contract 与 compat-zero guard 已同步到新基线
  - `2026-04-23` `G3` 第五小批已完成：
    - `action_executor.py` 的 frontier batch reservation 与
      `render_state_assembler.py` 的 frontier usage projection
      已改为直接走 `state.turn_context`
    - `CombatState` 上最后两项 bridge 属性已物理删除：
      - `frontier_used_batches`
      - `non_red_played_this_turn`
    - render/red touched tests 与 compat-zero guard 已同步到新基线
  - `2026-04-23` `G4` 第一小批已完成：
    - `tests/combat/test_damage_service.py` 已改为直接从
      `contexts.combat.domain.effects.impl.core` 导入 `DamageEffect`
    - `contexts/combat/domain/effects/implementations.py` 已物理删除
    - compat-zero guard 已更新为禁止该 shim 文件和旧导入路径回流
  - `2026-04-23` `G4` 第二小批已完成：
    - `tests/combat/test_action_queue.py` 已改为直接通过
      `ChoreResolutionPlanner` 做 chore-resolution mapping 覆盖
    - `ChoreResolutionOrchestrator._map_actions(...)` 已物理删除
    - compat-zero guard 已更新为禁止该 shim 方法与旧调用形态回流
  - `2026-04-23` `G4` 第三小批已完成：
    - `Enemy.select_skill_for_turn()` /
      `Enemy.use_selected_skill()` 已物理删除
    - compat-zero guard 已更新为禁止这两个 enemy legacy method 的定义与调用回流
  - `2026-04-23` `G5` retained adapter review 已完成：
    - save backward-compat migration / session save host 被正式归类为 retained backward-compat boundary
    - `ModelEnvironmentArenaEffect` / `DefaultTurnStartEnvironmentInjector` 被正式归类为 intentional runtime adapter
    - `CardInstance.card_id` / `CardInstance.cost_for_player(...)` 被正式归类为 stable convenience contract
    - `EffectContext` 不属于 retained adapter，后续若处理应作为单独的 dead scaffold 小清理
    - player scalar energy / colored pool convergence 不属于 compat-zero 收尾，应另开专题线
  - 当前这条 automation-safe compat-zero 执行线已在 `Engineering Zero` 意义上闭环
  - save backward compatibility 仍不属于首轮自动删除范围
  - 后续若继续做 combat 工程收口，应拆为独立专题而不是继续沿这条 compat-zero 主线顺推：
    - save lifecycle / schema decision
    - energy contract convergence
    - dead scaffold cleanup

### P1. Narrative Pipeline V1

- 目标：
  - 为叙事事件建立一条清晰的 `draft -> normalized source -> build -> runtime -> acceptance` 管线
  - 统一当前 narrative/questline 主链与 legacy campaign-event 路线，避免继续双真相增长
  - 让策划与 Codex 可以在不碰 runtime 细节的前提下稳定扩写 narrative 内容
- Current execution rules:
  - follow `docs/development/NARRATIVE_PIPELINE_V1.md`
  - use `docs/development/NARRATIVE_PIPELINE_TASK_TABLE_V1.md` as the rollout order
  - treat `data/questlines/*.json` as the active runtime path during migration
  - do not add new growth to `contexts/campaign/infrastructure/events/*.json`
  - do not retire legacy narrative runtime files until:
    - migration inventory exists
    - normalized source schema exists
    - source -> runtime build parity is proven on the active tutorial path
  - prefer serial rollout, not multiple competing narrative architecture branches
- Main inputs:
  - `docs/development/NARRATIVE_PIPELINE_V1.md`
  - `docs/development/NARRATIVE_PIPELINE_TASK_TABLE_V1.md`
  - `docs/development/DATA_PIPELINE_GUARDRAILS_V1.md`
  - `contexts/shared/quest_loader.py`
  - `contexts/shared/quest_runtime.py`
  - `contexts/narrative/application/service.py`
  - `contexts/event/state.py`
  - `data/questlines/`
  - `data/events_drafts/`
  - `data/events_src/`
- 预期输出：
  - 一套 normalized narrative source schema
  - draft/source/build tooling for narrative content
  - tutorial narrative path migrated onto the new source/build model
  - narrative scenario acceptance tests covering the active tutorial event/combat/reward path
  - a clear legacy retirement plan for the old campaign event route
- 边界：
  - 不重写 `EventState` 展示层
  - 不把 narrative pipeline 扩成通用脚本 VM
  - 不把 combat event bus 与 narrative event pipeline 混为一谈
  - 不在 schema 尚未稳定前一口气迁完所有 legacy narrative content
  - 不让 runtime 直接读 draft 文件
- 当前阶段判断：
  - `Phase 0` 可以视为已准备完成
  - 默认下一步是 `Phase 1 + Phase 2`
  - 在 tutorial path 构建等价 build 之前，不应删除全部 legacy narrative 内容

### P1. Campaign Simplification V1

- 目标：
  - 在不重开整轮 UI 重写、全量 DDD 推进或节点树迁移的前提下，完成一轮 campaign 侧的 targeted simplification
  - 让当前 mixed-mode campaign 架构更容易读、更安全扩展，也更便于 Codex 长时间连续协作
- Current execution rules:
  - follow `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md` serially
  - `2026-04-05`: `Phase 0` landed
  - `2026-04-05`: `Phase 1` landed: removed residual thesis / meeting compat wrappers and old headless meeting paths
  - `2026-04-05`: `Phase 2` landed: moved `CampaignState` service wiring into a dedicated service bundle while keeping stable host attrs/seams
  - `2026-04-05`: `Phase 3` landed: split `MeetingService` into focused selection / shop / event-flow helpers while keeping the stable service surface
  - `2026-04-05`: `Phase 4` landed: split campaign mouse input into dedicated intent resolution + dispatch helpers while preserving click priority and state seams
  - `2026-04-05`: the mainline simplification pass is effectively complete through `Phase 4`
  - `Phase 5` is now a triggered backlog slice, not an automatic next step
  - only start `Phase 5` when near-term roadmap work directly touches DDL / fusion / compaction rules or shared board invariants
  - do not mix this with a large UI rewrite, full DDD push, or full node migration work
- Main inputs:
  - `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md`
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
  - `docs/development/CAMPAIGN_HOTSPOT_DEFER_LIST_V1.md`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/meeting_service.py`
  - `contexts/campaign/services/campaign_mouse_event_service.py`
  - `contexts/campaign/services/track_block_service.py`
  - `contexts/campaign/services/thesis_meta_service.py`
- 预期输出：
  - 简化计划、热点文档和任务系统状态保持同步
  - focused guardrail tests + `scripts/run_repo_smoke_baseline.py` 保护关键 seams
  - 一轮以删旧路径、收紧 host seams、拆高 ROI 热点为主的 campaign targeted refactor
- 边界：
  - 不做 whole-campaign facade
  - 不做 full `CampaignView` rewrite
  - 不做 repository-everywhere
  - 不做 purity-driven `Track` aggregate promotion
  - 不把 runtime UI 演进扩成另一轮全局架构重写
- 当前阶段判断：
  - `Phase 0` 到 `Phase 4` 已完成并可视为当前主线收口
  - `Phase 5` 只保留为 triggered backlog，不再视为自动下一步
  - 只有近期待做直接触及 DDL / fusion / compaction 或 shared board invariants 时才启动

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

## 已归档完成任务（热区只保留索引）

- `Campaign UI Handoff Orchestration`
  - 已在 `2026-03-17` 收口，完整子任务、主要产出与重开条件见 `docs/development/task_pool_archive/2026-03_2026-04_completed.md`
- `Combat Queue Full Cutover` 与 `Combat Queue Residual Closure`
  - phase-2 与 residual 收尾均已归档，active `red/white` fallback 边界已在 `2026-03-31` 收口到 `0`
- `Campaign Aggregate / Orchestration Closure`
  - thesis、task-area、DDD follow-up 的本轮收口已归档
- `Combat Analysis Capability Iteration V1`
  - 当前轮已在 `2026-04-05` 完成；下一轮应重新拆任务，不再把 V1 checklist 长期留在热区

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

### P2. Resource Guardrail Convergence V1

- 目标：
  - 在现有 `scripts/check_resource_contracts.py` 与 `scripts/check_asset_manifest_consistency.py` 骨架之上，逐步收敛资源入口与清单漂移
  - 让资源问题尽量在 repo guard / smoke baseline 阶段暴露，而不是在运行期或打包期才发现
- 当前已落地基线：
  - `repo-guards` 已包含 resource contract 与 asset manifest consistency 检查
  - manifest / enum 漂移已修复
  - 当前仍有一批 `assets/` 硬编码路径告警，主要集中在 campaign / combat / deck / loading / main_menu / shared ui
- 主要输入：
  - `scripts/check_resource_contracts.py`
  - `scripts/check_asset_manifest_consistency.py`
  - `scripts/run_repo_smoke_baseline.py`
  - `contexts/shared/infrastructure/assets/`
  - 当前告警文件清单
- 预期输出：
  - 一份按优先级分组的资源入口迁移清单
  - 第一批高价值运行时路径从硬编码 `assets/` 收口到统一资源入口
  - 更小的 allowlist / 更少的 warning 数量
  - 条件成熟时，把部分 warning 升级为 hard-fail contract
- 边界：
  - 不做一次性“全仓库统一资源系统重写”
  - 不为了资源治理重开整轮 UI / rendering 重构
  - 不在当前主线优先级之前抢占 combat / campaign 主路径工作
- 当前不优先的原因：
  - 资源 guardrail 骨架已经落地，短期风险已从“不可见”降到“可见”
  - 剩余问题主要是工程债收敛，不是阻断当前近期主线的 P0
  - 更适合按模块顺手收口，而不是立刻开一条重型治理支线

### P2. Combat Analysis 下一轮拆分

- 当前状态（`2026-04-05`）：
  - `Combat Analysis Capability Iteration V1` 已完成并归档
  - 下一轮不沿用旧 checklist，等样本缺口和校准目标更清楚后再重新拆任务
- 当前下一轮规则：
  - 保持 `source facts -> reviewed annotation -> projection`
  - 不直接从卡牌文本跳共享语义
  - 只有同一种失败模式在多个角色重复出现时，才上升为共享语义
- 当前建议顺序：
  1. 先稳 core benchmark
  2. 再按角色逐个稳辅助层
  3. 先扩验证集，再扩模型表面
  4. 辅助层稳定后，再继续 `enemy pressure -> matchup -> recommendation`
- 当前默认观察入口：
  - 先刷 `combat_analysis_portfolio_report` 看组合级数据理解，再决定下一轮该补哪一层
- 下一轮候选方向：
  - 扩 STS 正负样本与 near-neighbor
  - 继续做遗物 / 时序 / 状态表达校准
  - 继续扩敌人 pressure 报告可视化
  - 继续观察值得共享化的时序语义：
    - `hold / retain / cross-turn value`
    - `delayed resolution / delayed payoff`
    - `conditional trigger window`
    - `threshold burst window`
  - 保持角色私有复杂度留在 `projection_gap`，不要过早污染共享层
- 当前不优先的原因：
  - 先观察本轮 benchmark / snapshot / HTML 报告是否稳定
  - 下一轮最好基于新增失败样本重新定义主攻点

### P3. 内容接入工作流

- 目标：
  - 文档化新卡牌 / 新敌人 / 新特质接入流程
- 当前不优先的原因：
  - 当前更需要先把 TA 线和数据链继续做稳

## 最近完成

- `Combat Analysis Capability Iteration V1`
  - 当前轮完成并已归档
- `Combat Queue Full Cutover` / `Combat Queue Residual Closure`
  - active `red/white` fallback 边界已在 `2026-03-31` 收口到 `0`
- `Campaign UI Handoff Orchestration`
  - 交接链已完成并已归档
- `Campaign Aggregate / Orchestration Closure`
  - thesis / task-area / DDD follow-up 的本轮收口已完成并归档
- 更早完成项：
  - 见 `docs/development/task_pool_archive/2026-03_2026-04_completed.md`
  - 以及最近周报、日报与专项文档

## 退出规则

当出现以下任一情况时，任务应该从活跃区移走：

- 已经实现
- 被新的设计决策阻塞
- 不再适合当前生产阶段
- 需要持续高频人工主观反馈
