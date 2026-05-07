# Cardanalysis 基础轴人工审核包 01

- 审核包 id: `foundation_axis_review_packet_01`
- 日期: `2026-05-06`
- 来源文档: `docs/development/cardanalysis/CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`
- 范围: status lineage、search/tutor certainty、temporary generation duration
- 运行时影响: none
- 权限边界: `advisory_context_only`

## 先说人话

这份审核包不是正式卡牌设计，也不会进入 runtime、正式数据、UI/save、hard gate、default synthesis、learned 或 reranker。

它只想请人判断三类基础轴问题是否值得继续收集 reviewed evidence：

1. `status` 的负担、收益、清理和所有权是否能被玩家看懂。
2. `search_tutor` 的确定性是否有真实代价，而不是把回合变成固定脚本。
3. `temporary_generation` 的生成来源、数量、持续时间和过期方式是否足够清楚。

每条只需要填：

```text
决定:
信心:
备注:
```

## 决定怎么填

| 选项 | 含义 | 后续处理 |
| --- | --- | --- |
| A | 先收下 | 值得作为后续 reviewed seed 候选 |
| B | 需要更多证据 | 方向有用，但还缺具体正反例 |
| C | 拒绝过度推断 | 说得太大或不安全，暂不提升 |
| D | 合并重复 | 与别的 request 或案例太像 |
| E | 无法判断 | 情境不够清楚，需要重写 |

信心可以填：高 / 中 / 低。

## 重要边界

下面的情境都是审核问题，不是正式卡牌。它们保持：

```text
design_note / human_curated / review_needed / advisory_context_only
```

本审核包不会自动生成 reviewed case，也不会修改机制 viability 评分逻辑。

## 审核条目

### 1. 状态负担能不能看清是谁造成的？

- item id: `foundation_review_item_01_status_visible_owner`
- request id: `status_lineage_cleanup_review_v1`
- 相关基础轴: `status`, `compression_removal`

假想情境：一个效果给玩家牌组塞入一张负担牌，同时承诺之后可以把它清理掉并换成收益。玩家在选择时能看到：这张负担是谁造成的、会留多久、清理需要付出什么、清理后能得到什么。

你要判断：这种“负担来源和清理路线都清楚”的状态机制，是否值得作为健康 status 设计的正例继续收集证据？

风险边界：如果只有收益清楚、负担来源和持续时间不清楚，玩家可能会觉得被暗中收税。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 2. 状态清理会不会变成强制交税？

- item id: `foundation_review_item_02_status_mandatory_cleanup`
- request id: `status_lineage_cleanup_review_v1`
- 相关基础轴: `status`, `compression_removal`

假想情境：玩家获得收益后，牌组里留下多张负担牌。之后几回合最合理的行动几乎都变成“清理负担”，否则牌组会卡死；但清理过程本身没有新的选择，只是在还债。

你要判断：这种“清理是必须做、但过程没有玩法”的状态机制，是否应作为 status 失败边界继续收集证据？

风险边界：如果所有状态负担都被判成坏事，会误伤那些负担本身就是有趣资源的机制。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 3. 检索确定性有没有真实代价？

- item id: `foundation_review_item_03_search_certainty_cost`
- request id: `search_tutor_certainty_cost_review_v1`
- 相关基础轴: `search_tutor`, `filter`, `draw`

假想情境：玩家可以从牌组里找一张关键牌，但代价是本回合少做一件事，或者暴露下一回合会变弱。即使目标牌暂时不适合，玩家仍然有普通出牌路线可以走。

你要判断：这种“能确定找牌，但确定性有机会成本和 fallback”的检索机制，是否值得作为健康 search/tutor 正例继续收集证据？

风险边界：如果代价太轻，检索会把随机性和牌组构筑压力全部抹平。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 4. 工具箱会不会把回合变成固定脚本？

- item id: `foundation_review_item_04_search_scripted_toolbox`
- request id: `search_tutor_certainty_cost_review_v1`
- 相关基础轴: `search_tutor`, `filter`, `draw`

假想情境：一套牌带了很多窄用途答案。每次遇到某类敌人，玩家几乎总是检索同一张答案牌。其他牌只是为了让这条固定路线更稳定，回合选择越来越像照脚本执行。

你要判断：这种“检索让每个问题只有一个正确答案”的工具箱机制，是否应作为 search/tutor 失败边界继续收集证据？

风险边界：不要把所有工具箱都判坏；好的工具箱应该在多个合理答案之间制造选择。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 5. 临时生成物的来源和持续时间够不够清楚？

- item id: `foundation_review_item_05_generation_clear_duration`
- request id: `temporary_generation_duration_origin_review_v1`
- 相关基础轴: `temporary_generation`, `status`, `search_tutor`

假想情境：一个效果临时生成两张选项牌。玩家能清楚看到它们从哪里来、这回合结束是否消失、没打出去会不会进弃牌堆、以及它们是否会污染后续抽牌。

你要判断：这种“生成来源、数量、持续时间、过期方式都清楚”的临时生成机制，是否值得作为健康 temporary generation 正例继续收集证据？

风险边界：如果生成物太像正式牌组的一部分，玩家会误判后续牌组质量。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 6. 临时生成会不会让玩家读太多选项？

- item id: `foundation_review_item_06_generation_option_overload`
- request id: `temporary_generation_duration_origin_review_v1`
- 相关基础轴: `temporary_generation`, `status`, `search_tutor`

假想情境：一回合里连续生成许多临时选项，每张都要读效果、比较收益、考虑顺序。玩家还没开始执行计划，就已经花了大量注意力理解这些临时牌。

你要判断：这种“生成选项过载导致执行负担”的情境，是否应作为 temporary generation 失败边界继续收集证据？

风险边界：不要把所有临时生成都判坏；少量、清楚、有时间限制的生成可以提供很好的战术弹性。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

## Codex 后续处理

人类填完后，Codex 应该：

1. 把 A 转成 reviewed seed 候选，而不是直接改 case tier。
2. 把 B 转成后续证据队列。
3. 把 C/D/E 作为停止线、合并线或重写线保存。
4. 继续保持 `advisory_context_only`，直到明确生成 reviewed-decision shard。
5. 跑 focused tests、case input validator、architecture、encoding、capability graph 和 `git diff --check`。
