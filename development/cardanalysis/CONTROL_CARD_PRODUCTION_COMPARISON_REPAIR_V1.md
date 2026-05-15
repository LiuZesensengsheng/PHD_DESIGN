# 控制卡牌生产包对比与修正建议 V1

## 目的

`control_card_production_comparison_repair_v1` 是 `control_card_production_packet_v1` 之后的 report-only 对比与修正建议层。

它消费当前被人类审查阻塞的控制卡牌生产包，对五个未审查包版本做确定性对比，并整理给人类审查用的修正建议。它不选择包、不草拟卡牌、不提升任何包版本。

## 人类阅读形式

人类主要阅读 `*_report.md`。报告正文使用中文，包含：

- 中文对比表；
- 中文修正建议；
- 中文机制路线对比；
- 中文等待人类输入说明；
- 中文边界说明。

`*_snapshot.json` 仍使用英文 id 和机器字段名，作为稳定的自动化契约。

## 输出范围

V1 输出：

- 每个包版本一行对比结果；
- 乐趣承诺清晰度；
- 前期、中期、后期强度曲线风险；
- 复杂度、泛用强卡漂移、第二职业风险摘要；
- 来源证据和就绪度摘要；
- 修正优先级标签与建议修正 notes；
- 白序 vs 蓝真、蓝真 vs 未来手牌、绿深 vs 领跑包、资源节奏压制风险探针等路线对比；
- 适合优先人审、修正候选、保留为探针、人类边界审查等建议层级；
- 保持为空的人类决策槽；
- 可先准备事项和不能推进清单；
- 明确的 report-only 边界断言。

## 当前读数

默认 fixture 对比五个包版本：

- `white_order_fail_state_packet_v1`：白序，失败可恢复控制包；
- `blue_truth_forecast_packet_v1`：蓝真，预判窗口控制包；
- `green_depth_compound_stability_packet_v1`：绿深，复合稳定控制包；
- `resource_tempo_denial_probe_v1`：资源/节奏压制风险探针；
- `hand_future_planning_probe_v1`：未来手牌规划探针。

当前建议层级：

- 优先人审：`white_order_fail_state_packet_v1`、`blue_truth_forecast_packet_v1`
- 修正候选：`green_depth_compound_stability_packet_v1`、`hand_future_planning_probe_v1`
- 保留为探针：`resource_tempo_denial_probe_v1`

这些层级不是权威选择，只是帮助人类更快审查的建议。

## 人类暂时没空时

V1 fixture 保持阻塞：

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- `repair_notes_status = automatic_comparison_repair_notes_ready_owner_review_blocked`
- `next_repair_plan_ready = false`
- `next_repair_plan_status = blocked_awaiting_owner_package_selection`
- 人类决策槽保持空；
- 不选择、提升、拒绝或合并任何包版本；
- 不声称证据已审查或已接受。

自动化可以比较未审查包版本、保留修正建议、收集人审问题、准备后续审查包所需的证据引用。自动化不能选择包、草拟正式卡牌、创建运行时数据或开始可玩原型工作。

## 边界

V1 保持：

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.source_packet_is_authoritative = false`
- `boundary_assertions.comparison_is_authoritative = false`
- `boundary_assertions.owner_selection_recorded = false`
- `boundary_assertions.repair_plan_generated = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.package_version_promoted = false`
- `boundary_assertions.package_version_rejected = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## 入口命令

生成当前中文对比/修正报告：

```powershell
python scripts/run_control_card_production_comparison_repair.py --output-dir tmp/combat_analysis/control_card_production_comparison_repair_current
```

验证 fixture：

```powershell
python scripts/run_control_card_production_comparison_repair.py --input tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1 --json
```

Focused validation：

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_comparison_repair_v1.py tests/scripts/test_run_control_card_production_comparison_repair.py -q
```

## V1 Fixture

当前 fixture 输出位于：

`tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1/`

它消费：

`tests/fixtures/combat_analysis/control_card_production_packet_v1/control_card_production_packet_v1_snapshot.json`

其中 `control_card_production_comparison_repair_v1_report.md` 是给人看的中文报告；`control_card_production_comparison_repair_v1_snapshot.json` 是给工具读的机器契约。

## 后续方向

如果人类开始审查，下一步是 owner decision packet，用来记录 keep、revise、reject、merge，以及下一轮指令。

如果人类仍然没空，继续提升证据质量、对比质量和中文审查问题。没有人类选择前，不进入完整卡牌草拟请求或可玩原型。
