# Cardanalysis 基础轴人工审核包 02

- 审核包 id: `foundation_axis_review_packet_02`
- 日期: `2026-05-06`
- 来源文档: `docs/development/cardanalysis/CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`
- 范围: retain/filter setup tax、compression/removal breakpoint
- 运行时影响: none
- 权限边界: `advisory_context_only`

## 先说人话

这份审核包不是正式卡牌设计，也不会进入 runtime、正式数据、UI/save、hard gate、default synthesis、learned 或 reranker。

它只想请人判断两类基础轴问题是否值得继续收集 reviewed evidence：

1. `retain` 和 `filter` 是在制造有压力的规划，还是只是在让玩家等一个显而易见的答案。
2. `compression_removal` 是在改善牌组可靠性，还是把牌组压到没有摩擦、没有选择。

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

### 1. 保留牌是在规划，还是在囤积？

- item id: `foundation_review_item_07_retain_planning_pressure`
- request id: `retain_filter_setup_tax_review_v1`
- 相关基础轴: `retain`, `filter`, `draw`

假想情境：玩家可以把一张关键牌保留到下回合。好的情况是敌人压力让玩家必须判断“现在用掉、还是冒险留到更好的窗口”。坏的情况是保留几乎没有代价，玩家只是把答案攒在手里，直到最明显的时机出现。

你要判断：这种“保留是否真的制造规划压力”的问题，是否值得作为 retain 设计的 reviewed evidence request 继续收集证据？

风险边界：不要把所有保留都判成囤积；真正有压力的保留可以让未来窗口变得更有表达力。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 2. 过滤是在选择，还是假装给选择？

- item id: `foundation_review_item_08_filter_real_choice`
- request id: `retain_filter_setup_tax_review_v1`
- 相关基础轴: `filter`, `draw`, `search_tutor`

假想情境：一个效果让玩家看几张牌并丢掉一部分。好的情况是玩家必须在防御、伤害、后续组合之间取舍。坏的情况是永远都有一张明显最差的牌，过滤只是机械地移除垃圾。

你要判断：这种“过滤选择是否真实”的问题，是否值得作为 filter 设计的正反对照继续收集证据？

风险边界：如果过滤永远只是无脑剔除最差牌，它可能在体验上更接近隐形抽牌，而不是机制选择。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 3. 设置税会不会让玩家一直等？

- item id: `foundation_review_item_09_setup_tax_tunnel`
- request id: `retain_filter_setup_tax_review_v1`
- 相关基础轴: `retain`, `filter`, `draw`

假想情境：一套牌需要先保留关键牌、过滤手牌、等待特定窗口，然后才能开始真正收益。玩家每回合都在准备，但准备本身缺少即时价值，失败时也没有有用输出。

你要判断：这种“为了未来收益而连续空转”的 setup-tax tunnel，是否应作为 retain/filter 失败边界继续收集证据？

风险边界：不要误伤那些准备过程本身有防御、过牌或资源价值的慢速机制。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 4. 压缩牌组后还剩不剩摩擦？

- item id: `foundation_review_item_10_compression_friction_remaining`
- request id: `compression_removal_breakpoint_review_v1`
- 相关基础轴: `compression_removal`, `exhaust`, `discard`

假想情境：玩家通过移除、消耗或过滤让牌组更稳定。好的情况是牌组更可靠，但仍然要在防御、输出、资源之间做选择。坏的情况是牌组被压到几乎每回合都重复同一条路线。

你要判断：这种“压缩后是否还保留足够摩擦”的问题，是否值得作为 compression/removal 正例边界继续收集证据？

风险边界：如果完全没有摩擦，机制可能变成自动执行，而不是玩家决策。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 5. 免费删牌会不会把所有弱牌变成收益？

- item id: `foundation_review_item_11_free_removal_upside`
- request id: `compression_removal_breakpoint_review_v1`
- 相关基础轴: `compression_removal`, `exhaust`, `discard`

假想情境：一个效果可以非常便宜地删除或消耗弱牌，而且删除本身还会触发收益。玩家原本应该承担的牌组杂质，变成了几乎没有代价的燃料。

你要判断：这种“免费压缩把摩擦变成纯收益”的情境，是否应作为 compression/removal 失败边界继续收集证据？

风险边界：不要把有真实机会成本的 exhaust 或 discard 也误判成免费收益。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 6. 正常牌组大小下还能不能运转？

- item id: `foundation_review_item_12_normal_deck_size_viability`
- request id: `compression_removal_breakpoint_review_v1`
- 相关基础轴: `compression_removal`, `exhaust`, `discard`

假想情境：一套机制在极薄牌组里非常顺畅，但在正常牌组大小下经常找不到关键牌、无法闭环、或者每次都要先做很多清理。设计问题不是机制不存在，而是它只在过度压缩后才像机制。

你要判断：这种“机制是否只在极薄牌组里成立”的问题，是否值得作为 compression/removal breakpoint 继续收集证据？

风险边界：一些机制本来就是薄牌组奖励；问题是它是否被伪装成普通机制支持。

建议: B，需要更多证据。

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
