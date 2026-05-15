# 控制卡牌生产人类决策包 V1

## 目的

`control_card_production_owner_decision_packet_v1` 是 `control_card_production_comparison_repair_v1` 之后的 report-only 人类决策层。

它消费当前被人类审查阻塞的对比/修正快照，把内容整理成低负担审查包：如果人类只有十分钟，只需要回答保留、修正、拒绝、合并、口味、强度、复杂度、禁用玩法和下一轮指令这些核心字段。

这个包不会选择包、不会草拟卡牌、不会提升或拒绝包版本，也不会生成修正计划。

## 人类阅读形式

人类主要阅读 `*_report.md`。报告正文使用中文：

- 中文十分钟审查问题；
- 中文包名；
- 中文玩法承诺；
- 中文主要风险；
- 中文主要修正建议；
- 中文等待人类输入说明；
- 中文边界说明。

`*_snapshot.json` 仍使用英文 id 和机器字段名，作为稳定的自动化契约。

## 输出范围

V1 输出：

- 建议人类审查顺序；
- 十分钟审查问题面板；
- 每个包版本一张决策卡；
- 每个包的一句话玩法承诺、机制轴、ideal id、建议层级、主要风险和主要修正建议；
- `keep`、`revise`、`reject`、`merge` 的空决策槽；
- 空的人类选择、拒绝、合并目标、口味、强度、复杂度、禁用玩法和下一轮指令字段；
- 决策就绪摘要；
- 可先准备事项和不能推进清单；
- 明确的 report-only 边界断言。

## 当前读数

默认 fixture 保留以下建议审查顺序：

1. `white_order_fail_state_packet_v1`：白序，失败可恢复控制包
2. `blue_truth_forecast_packet_v1`：蓝真，预判窗口控制包
3. `green_depth_compound_stability_packet_v1`：绿深，复合稳定控制包
4. `hand_future_planning_probe_v1`：未来手牌规划探针
5. `resource_tempo_denial_probe_v1`：资源/节奏压制风险探针

前两个仍是最快的人审候选。绿深和未来手牌规划是修正候选。资源/节奏压制仍然只是保留的风险探针。这些是审查顺序提示，不是权威选择。

## 人类暂时没空时

V1 fixture 保持阻塞：

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- `decision_packet_status = owner_decision_packet_ready_owner_review_blocked`
- `decision_packet_ready_for_owner_review = true`
- `owner_decision_ready = false`
- `owner_selection_recorded = false`
- `next_repair_plan_ready = false`
- `next_repair_plan_status = blocked_awaiting_owner_package_selection`
- 人类决策槽保持空；
- 不选择、提升、拒绝或合并任何包版本；
- 不声称证据已审查或已接受。

自动化可以格式化这份中文决策包、保留对比/修正建议、准备空的人类决策模板，并在人类选择后准备后续修正计划输入。自动化不能代替人类记录决策、选择包、生成修正计划、草拟正式卡牌或写运行时卡牌数据。

## 边界

V1 保持：

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.comparison_is_authoritative = false`
- `boundary_assertions.owner_decision_recorded = false`
- `boundary_assertions.owner_selection_recorded = false`
- `boundary_assertions.package_version_selected = false`
- `boundary_assertions.package_version_promoted = false`
- `boundary_assertions.package_version_rejected = false`
- `boundary_assertions.repair_plan_generated = false`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## 入口命令

生成当前中文人类决策包：

```powershell
python scripts/run_control_card_production_owner_decision_packet.py --output-dir tmp/combat_analysis/control_card_production_owner_decision_packet_current
```

验证 fixture：

```powershell
python scripts/run_control_card_production_owner_decision_packet.py --input tests/fixtures/combat_analysis/control_card_production_owner_decision_packet_v1 --json
```

Focused validation：

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_owner_decision_packet_v1.py tests/scripts/test_run_control_card_production_owner_decision_packet.py -q
```

## V1 Fixture

当前 fixture 输出位于：

`tests/fixtures/combat_analysis/control_card_production_owner_decision_packet_v1/`

它消费：

`tests/fixtures/combat_analysis/control_card_production_comparison_repair_v1/control_card_production_comparison_repair_v1_snapshot.json`

其中 `control_card_production_owner_decision_packet_v1_report.md` 是给人看的中文报告；`control_card_production_owner_decision_packet_v1_snapshot.json` 是给工具读的机器契约。

## 后续方向

如果人类填写这份包，下一步是针对被选中的一到两个包做 repair-plan generator。

如果人类仍然没空，继续改善证据、对比、审查问题和中文可读性。没有人类选择前，不进入完整卡牌草拟请求或可玩原型。
