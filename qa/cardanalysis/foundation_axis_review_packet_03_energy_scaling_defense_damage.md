# Cardanalysis 基础轴人工审核包 03

- 审核包 id: `foundation_axis_review_packet_03`
- 日期: `2026-05-06`
- 来源文档: `docs/development/cardanalysis/CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`
- 范围: energy/scaling identity override、defense/damage closure
- 运行时影响: none
- 权限边界: `advisory_context_only`

## 先说人话

这份审核包不是正式卡牌设计，也不会进入 runtime、正式数据、UI/save、hard gate、default synthesis、learned 或 reranker。

它只想请人判断两类基础轴问题是否值得继续收集 reviewed evidence：

1. `energy`、`scaling`、`damage` 是在支撑机制，还是已经把机制身份吞掉。
2. `defense_block` 和 `damage` 是否能把生存转成推进，而不是停在纯防御或纯数值。

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

### 1. 额外能量是在制造花费选择，还是让玩家什么都能做？

- item id: `foundation_review_item_13_energy_spend_choice`
- request id: `energy_scaling_identity_override_review_v1`
- 相关基础轴: `energy`, `damage`, `scaling`

假想情境：玩家获得额外能量。好的情况是玩家必须判断先打防御、先启动机制、还是把能量留给更高收益窗口。坏的情况是额外能量多到足以做完所有事情，顺序和取舍都消失。

你要判断：这种“能量是否仍然制造花费选择”的问题，是否值得作为 energy 支撑机制的正例边界继续收集证据？

风险边界：不要把所有高能量回合都判坏；问题是高能量是否让机制选择消失。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 2. 能量爆发之后有没有释放窗口和恢复代价？

- item id: `foundation_review_item_14_energy_release_recovery`
- request id: `energy_scaling_identity_override_review_v1`
- 相关基础轴: `energy`, `damage`, `scaling`

假想情境：一套牌能在某回合获得大量能量并打出爆发。好的情况是爆发窗口清楚，之后的恢复、债务或压力也清楚。坏的情况是玩家只是在等一个完美爆发，错过窗口后前几回合的准备都变成空转。

你要判断：这种“爆发能量是否有清楚释放窗口和恢复代价”的问题，是否值得继续收集 reviewed evidence？

风险边界：硬性回滚能量通常体验很差； softer debt 或状态负担可能更容易被接受，但仍需要证据。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 3. 成长数值会不会替代机制本身？

- item id: `foundation_review_item_15_scaling_replaces_mechanism`
- request id: `energy_scaling_identity_override_review_v1`
- 相关基础轴: `scaling`, `damage`, `energy`

假想情境：一个机制本来强调时机、状态或组合。但只要成长层数足够高，玩家可以忽略机制细节，直接用越来越高的伤害或防御解决战斗。

你要判断：这种“scaling 把机制身份吞掉”的情境，是否应作为 identity override 失败边界继续收集证据？

风险边界：成长机制本身可以很有趣；问题是成长是否让原本的高级机制不再重要。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 4. 防御能不能转成推进？

- item id: `foundation_review_item_16_defense_converts_to_progress`
- request id: `defense_damage_closure_review_v1`
- 相关基础轴: `defense_block`, `damage`, `scaling`

假想情境：玩家通过防御稳定局面。好的情况是稳定之后能转入反击、蓄力释放、资源转换或明确的收尾路线。坏的情况是玩家只是活着，但每回合都没有更接近胜利。

你要判断：这种“生存是否能转成推进”的问题，是否值得作为 defense/block 健康设计的正例边界继续收集证据？

风险边界：有些控制机制允许慢速胜利；关键是慢速是否仍然有可见进展。

建议: B，需要更多证据。

你的审核:

```text
决定:
信心:
备注:
```

### 5. 纯防御会不会变成无聊拖延？

- item id: `foundation_review_item_17_defense_stall_without_closure`
- request id: `defense_damage_closure_review_v1`
- 相关基础轴: `defense_block`, `damage`, `scaling`

假想情境：一套牌拥有足够防御，敌人很难突破。但它缺少收尾、反击或资源转化，玩家只是重复堆防御，等待很久才结束战斗。

你要判断：这种“stall without closure”的情境，是否应作为 defense/block 失败边界继续收集证据？

风险边界：不要误伤那些防御过程本身会积累明确胜利条件的机制。

建议: A，先收下。

你的审核:

```text
决定:
信心:
备注:
```

### 6. 伤害是机制赚来的，还是原始数值直接压过去？

- item id: `foundation_review_item_18_damage_earned_vs_raw_rate`
- request id: `defense_damage_closure_review_v1`
- 相关基础轴: `damage`, `defense_block`, `scaling`

假想情境：一个机制最后用伤害收尾。好的情况是伤害来自玩家前面的时机、规划、状态管理或资源转换。坏的情况是卡牌本身伤害率太高，即使完全不玩机制也足够强。

你要判断：这种“damage 是否由机制赚来”的问题，是否值得作为 damage closure 的正反对照继续收集证据？

风险边界：高伤害不一定坏；问题是它是否让机制选择变得可有可无。

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

