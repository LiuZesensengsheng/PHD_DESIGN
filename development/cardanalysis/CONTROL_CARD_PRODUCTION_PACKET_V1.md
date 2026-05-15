# 控制卡牌生产包 V1

## 目的

`control_card_production_packet_v1` 是控制职业卡牌生产试验里的第一份人类可读 report-only 生产包。

它消费当前的 control discipline + ideal candidate batch、candidate batch exam、candidate batch exam evidence 快照，把这些建议性输入整理成多套可供人类审查的控制包版本。

## 人类阅读形式

人类主要阅读 `*_report.md`。从本版本开始，报告正文使用中文：

- 中文包名；
- 中文玩法承诺；
- 中文机制轴说明；
- 中文半正式概念槽；
- 中文乐趣、强度、风险、人审问题。

`*_snapshot.json` 仍保留英文 id 和机器字段名，作为稳定的自动化契约。不要把 JSON 快照当作主要人审界面。

## 输出范围

V1 输出三到五个控制包版本。每个包包含：

- 玩法承诺；
- 机制轴与 ideal 来源；
- 预期循环；
- 角色槽；
- 八个半正式概念槽；
- 组合与反组合说明；
- 乐趣与强度评估；
- 前期、中期、后期强度曲线；
- 复杂度预算；
- 泛用强卡漂移风险与第二职业风险；
- 证据和人类审查问题；
- 可先准备事项、阻塞字段、推荐下一步。

半正式概念槽可以有类似卡牌名、费用段、角色和机制意图，但它们不是正式卡牌文本，也不是运行时卡牌数据。

## 当前包版本

默认 fixture 产生五个未审查包版本：

- `white_order_fail_state_packet_v1`：白序，失败可恢复控制包；
- `blue_truth_forecast_packet_v1`：蓝真，预判窗口控制包；
- `green_depth_compound_stability_packet_v1`：绿深，复合稳定控制包；
- `resource_tempo_denial_probe_v1`：资源/节奏压制风险探针；
- `hand_future_planning_probe_v1`：未来手牌规划探针。

前三个来自候选批次考试后的保留集，后两个来自生产试验计划的可选对比探针。

## 人类暂时没空时

当前 fixture 保持阻塞：

- `review_status = awaiting_owner_review`
- `blocked_by_owner_review = true`
- 人类决策槽保持空；
- 不声称证据已审查或已接受；
- 不提升或拒绝任何包版本；
- 不生成可玩原型、完整卡牌草拟请求、正式卡牌文本或运行时卡牌数据。

自动化仍可格式化报告、保留证据引用、准备审查问题，并在未来人类选择一到两个包版本后，为草拟请求做准备。

## 边界

V1 保持：

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `boundary_assertions.report_only = true`
- `boundary_assertions.advisory_context_only = true`
- `boundary_assertions.blocked_by_owner_review = true`
- `boundary_assertions.official_card_data_modified = false`
- `boundary_assertions.runtime_card_data_written = false`
- `boundary_assertions.formal_card_text_generated = false`
- `boundary_assertions.formal_cards_promoted = false`
- `boundary_assertions.candidate_promoted = false`
- `boundary_assertions.candidate_rejected = false`
- `boundary_assertions.ranking_changed = false`
- `boundary_assertions.scorecard_weights_changed = false`
- `boundary_assertions.hard_gate_created = false`
- `boundary_assertions.reviewed_evidence_claim_created = false`
- `boundary_assertions.accepted_evidence_claim_created = false`
- `boundary_assertions.llm_api_called = false`
- `boundary_assertions.default_synthesis_enabled = false`
- `boundary_assertions.learned_or_reranker_enabled = false`

## 入口命令

生成当前中文报告、机器快照和 manifest：

```powershell
python scripts/run_control_card_production_packet.py --output-dir tmp/combat_analysis/control_card_production_packet_current
```

验证 fixture：

```powershell
python scripts/run_control_card_production_packet.py --input tests/fixtures/combat_analysis/control_card_production_packet_v1 --json
```

Focused validation：

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_control_card_production_packet_v1.py tests/scripts/test_run_control_card_production_packet.py -q
```

## V1 Fixture

当前 fixture 输出位于：

`tests/fixtures/combat_analysis/control_card_production_packet_v1/`

其中 `control_card_production_packet_v1_report.md` 是给人看的中文报告；`control_card_production_packet_v1_snapshot.json` 是给工具读的机器契约。

## 后续方向

如果人类选择一到两个包版本，下一步应做这些包的完整卡牌草拟请求包。

如果人类仍然没空，下一步应继续改善对比、证据、审查问题和中文人审体验，不应进入正式卡牌草拟或可玩原型。
