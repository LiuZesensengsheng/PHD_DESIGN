# Cardanalysis source-followup 审核交接说明

* 交接 id: `source_followup_review_workflow_handoff`
* 日期: `2026-05-06`
* 覆盖范围: 审核包 02-08
* 状态: 人工审核工作流说明
* 运行时影响: 无

## 一句话版本

现在这条 lane 已经把 105 条待审材料翻译成中文场景。你只需要按审核编号填写 A/B/C/D/E；在你填写之前，它们都只是待审队列，不是 reviewed 证据。

## 先看哪个文件

建议按这个顺序看：

1. `docs/qa/cardanalysis/source_followup_review_queue_index.md`
2. `docs/qa/cardanalysis/source_followup_reviewability_layer_index.md`
3. `docs/qa/cardanalysis/source_followup_review_readability_hygiene_scan.md`
4. 具体审核包：`source_followup_review_packet_02_scenarios.md` 到 `source_followup_review_packet_08_scenarios.md`

如果你只想快速开始，直接打开第 2 个文件，优先填“可先直接审”的审核编号。

## 怎么填

每个审核编号下面都有这个块：

```text
决定:
信心:
备注:
```

可用决定：

| 选项 | 意思 | 后续处理 |
| -- | -- | -- |
| A | 先收下 | 可转成 reviewed seed 候选记录，但仍不晋升原 source case |
| B | 需要更多证据 | 进入后续证据队列 |
| C | 拒绝过度推断 | 记录为停止线 |
| D | 合并重复 | 记录为合并线 |
| E | 无法判断 | 打回重写 |

信心可以写：高 / 中 / 低。

## 最省力填法

可以只写一行很短的判断：

```text
决定: A
信心: 中
备注: 这个场景能理解，可以保留
```

如果某条看了 20 秒仍然不确定，就填：

```text
决定: E
信心: 高
备注: 人类不可判读，建议重写
```

## 不能做什么

在人工填写结果被读取并另建 decision shard 之前，不能做这些事：

1. 不能说 packet 02-08 已经 reviewed。
2. 不能把待审条目当成正式卡牌、正式敌人或正式规则。
3. 不能把 source-mined、generated、human-curated 自动说成 reviewed。
4. 不能改 runtime、正式卡牌/敌人数据、UI、存档。
5. 不能改 capability graph、report-only registry、hard gates、默认生成、learned 或 reranker 行为。

## Codex 后续会怎么处理

你填完一个包后，Codex 可以做一轮很小的处理：

1. 读取你填好的中文块。
2. 生成对应的 decision shard。
3. 把 A/B/C/D/E 分别记录成候选、后续证据、停止线、合并线、重写线。
4. 继续保持原 source case 是 `review_needed / advisory_context_only`。
5. 更新队列索引、daily log 和 focused tests。

## 当前最建议的人工顺序

1. 先填 60 条“可先直接审”里的任意一小批，比如 10-15 条。
2. packet 08 是重写候选队列，如果你这轮只想判断可读性和停止线，可以优先填它。
3. 暂时跳过“先补例子”的 30 条，除非你很有感觉。
4. 对可读性卫生扫描里标出来的相似项，如果你觉得重复，填 D；如果只是相关但不重复，填 A 或 B。
5. 对缺停止线的条目，如果你觉得说得太大，填 C。

## 当前边界

这份交接说明本身也是队列说明，不是审核结果。所有 pending 材料仍然保持：

```text
review_needed / advisory_context_only
```

没有人工填写结果时，不会生成新的 decision shard，也不会创建 reviewed 证据。
