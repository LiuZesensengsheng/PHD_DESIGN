# Darkest Dungeon Virtue Affliction Statistics V1

## Purpose

本文件统计《Darkest Dungeon 1》的美德与折磨系统，关注两个问题：

- 美德到底奖励什么方向？
- 折磨到底损坏什么方向？

结论先行：DD1 没有给每个战斗机制配一个对应惩罚。它用统一的压力阈值制造低频大事件；美德是纯正向英雄时刻，折磨主要损坏角色可靠性、队伍压力、行动控制和远征后勤。

## Source Boundary

- `source_status = design_reference`
- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- 本文件用于设计学习，不是项目数值模板。
- DD1 的具体数值不应直接复制到本项目。
- 本文件统计的是 DD1 主体结构，并把 DLC/特殊状态分开标记。

## Sources

| Source | Use |
| --- | --- |
| Darkest Dungeon Wiki: Stress | 压力来源、100/200 阈值、压力治疗结构。 |
| Darkest Dungeon Wiki: Virtue | 美德概率、共通增益、5 种美德具体效果。 |
| Darkest Dungeon Wiki: Affliction | 7 种基础折磨、Rapturous、Refracted 的数值、act-out、拒绝行为、历史权重。 |
| Game Developer: Darkest Dungeon's Affliction System | Red Hook 对设计意图的解释：压力反应、人性、失控、戏剧节点。 |
| Red Hook official about page | 官方定位：不只战斗怪物，也战斗压力。 |

## Core Loop

| Stage | DD1 behavior | Design meaning |
| --- | --- | --- |
| Stress accumulation | 战斗、暴击、黑暗、陷阱、饥饿、奇物、拖延战斗、队友死亡等都会积累压力。 | 压力是统一入口，不绑定某张技能牌或某个机制。 |
| 100 stress | 到 100 时触发 resolve check，结果为 Virtue 或 Affliction。 | 阈值事件是大戏剧节点。 |
| Virtue chance | 基础美德概率 25%，受饰品、怪癖、等级差等影响，有最低/最高限制。 | 美德是稀有翻盘，不是稳定构筑收益。 |
| Afflicted state | 折磨后仍继续积累压力。 | 折磨不是结算结束，而是远征继续恶化的开始。 |
| 200 stress | 折磨者达到 200 会心脏病，进入 Death's Door；若已在 Death's Door 则死亡。美德者到 200 时失去美德并压力归零。 | 折磨有二段升级，形成撤退/治疗/硬撑的战略压力。 |
| Recovery | 城镇 Abbey/Tavern、闲置、露营、战斗技能、暴击、击杀等可减压。 | 远征外恢复是资源管理和角色轮换。 |

## Virtue Statistics

### Shared Virtue Effects

| Shared effect | Coverage | Design direction |
| --- | ---: | --- |
| +25% Stun/Blight/Bleed/Disease/Debuff/Move Resist | 5/5 virtues | 美德统一提高抗压与抗异常能力。 |
| Becoming virtuous reduces party stress and sets the hero's stress down to around mid-low stress | 5/5 virtues | 美德先稳定局势，再给个体能力。 |
| Can exceed 100 stress without affliction and avoids normal 200-stress heart attack behavior | 5/5 virtues | 美德把危机转成保护窗口。 |
| Start-of-turn positive act-out chance | 5/5 virtues | 美德不只加属性，还会偶发帮助队伍。 |

### Virtue Detail Table

| Virtue | Self stat gain | Start-turn act-out | Primary reward axis | Secondary reward axis |
| --- | --- | --- | --- | --- |
| Stalwart | +15% PROT, +8% Death Blow Resist | 25%: self stress -15 | 生存/承伤 | 自我减压 |
| Courageous | -33% stress received, +2 SPD | 25%: other heroes stress -4 | 队伍压力管理 | 速度 |
| Focused | +10 ACC, +8% CRIT | 25%: buff one ally +10 ACC, +10% CRIT | 命中/暴击 | 单体队友输出支援 |
| Powerful | +25% DMG | 25%: buff other heroes +15% DMG | 伤害 | 全队输出支援 |
| Vigorous | +4 SPD, +10 DODGE | 25%: self heal 10% MAX HP | 速度/闪避 | 自我恢复 |

### Virtue Reward Direction Counts

| Reward direction | Count | Members | Interpretation |
| --- | ---: | --- | --- |
| Direct offense | 2/5 | Focused, Powerful | 美德有明确输出翻盘方向，但不是唯一方向。 |
| Defense/survival | 2/5 | Stalwart, Vigorous | 美德能让濒危角色继续活。 |
| Stress economy | 2/5 direct act-outs, plus shared entry relief | Stalwart, Courageous | 美德最核心的收益之一是稳定压力链。 |
| Party support | 3/5 | Courageous, Focused, Powerful | 美德常常影响队伍，而不是只强化个人。 |
| Tempo/speed | 2/5 | Courageous, Vigorous | 美德可以把危机转成先手/行动节奏。 |
| HP recovery | 1/5 | Vigorous | 生命恢复存在，但不是美德主轴。 |

### Virtue Design Read

DD1 的美德很克制：

- 美德数量少，只有 5 种基础类型。
- 每种美德有一个清晰主题：承伤、勇气、专注、力量、活力。
- 美德是纯正向，不混入惩罚。
- 美德的 act-out 是帮助玩家，而不是夺走控制。
- 美德的队伍价值很强，尤其是压力缓解和队友 buff。

这说明 DD1 的美德不是“某机制变强”，而是“角色在压力下变得可靠、鼓舞、能扛、能打、能救场”。

## Base Affliction Statistics

### Shared Affliction Effects

| Shared damage | Coverage | Design direction |
| --- | ---: | --- |
| -15% Stun/Blight/Bleed/Disease/Debuff/Move/Trap Resist | 7/7 base afflictions | 降低抗异常与环境容错。 |
| -10% MAX HP | 7/7 base afflictions | 降低生存安全边际。 |
| Combat comments can add stress to allies or party | 7/7 base afflictions | 折磨会传染队伍压力。 |
| Start-turn forced act-outs | 7/7 base afflictions | 折磨损坏行动可靠性。 |
| Refusal or compulsive behavior outside normal command | 7/7 base afflictions, but severity differs | 折磨损坏玩家管理权。 |

### Base Affliction Detail Table

| Affliction | Stat changes beyond shared penalties | Act-out total | Main act-outs | Comments / contagion triggers | Other reliability damage | Damage direction |
| --- | --- | ---: | --- | --- | --- | --- |
| Fearful | -25% DMG, +10 DODGE, +2 SPD | 31.5% | party stress, move back, pass turn | hero attacked, ally attacked, ally misses, ally curio | refuse movement, refuse camping skill, worship curio compulsion | 退缩、跳过、输出下降 |
| Paranoid | -25% DMG, -5 ACC, +10 DODGE, +2 SPD | 31.25% | party stress, move back, random skill, attack ally | hero attacked, ally attacked | refuse retreat/move/heal/buff/item/eat/camp | 不信任队伍、拒绝协作 |
| Selfish | -5 ACC, -10% DMG, +5 DODGE | 33.33% | party stress, move back, pass turn, random skill | hero hit, ally attacks, ally curio | refuse camping skill, treasure curio compulsion | 抢资源、低协作 |
| Masochistic | -15 DODGE | 33.33% | party stress, move forward, self attack, mark self | hero attacked, ally hit, ally curio, ally trap | refuse retreat/move/heal/buff/item/eat/camp, torture curio compulsion | 自伤、找死、暴露自己 |
| Abusive | -5 ACC, +20% DMG, -15 DODGE | 29.4% | party stress, attack ally | ally hit, ally attacks | refuse movement, refuse camping skill | 攻击性、队内伤害、压力扩散 |
| Hopeless | -5 ACC, -5 DODGE, -3 SPD | 35% | party stress, random move, pass, random skill, self attack, mark self | ally trap | refuse retreat/heal/buff/item/eat/camp | 放弃、行动崩坏 |
| Irrational | -5 ACC, -10% DMG, -5 DODGE, +2 SPD | 33.33% | party stress, random move, pass, random skill, attack ally, self attack, mark self | hero attacked, ally attacked, ally attacks, ally curio, ally trap | refuse retreat/move/heal/buff/item/eat/camp, any curio compulsion | 混乱、综合失控 |

### Special / DLC Afflictions

| Affliction | Availability | Stat changes | Act-out total | Main act-outs | Design note |
| --- | --- | --- | ---: | --- | --- |
| Rapturous | Flagellant only, Crimson Court | +25% DMG, -20 DODGE, +3 SPD | 41.67% | stress, move forward, random skill, attack ally, attack self | 不是普通折磨；Flagellant 总会获得它，且不能获得美德。 |
| Refracted | Farmstead / Color of Madness | +20% stress received, -5 SPD, +15% bleed skill chance, +15% blight skill chance, ignore stealth | 39% | stress, random move, pass, attack ally, mark self, use random item | 更像特殊维度污染，包含正向异常技能率与负向压力/速度。 |

## Affliction Damage Direction Counts

### Stat Damage

| Stat direction | Base count | Members | Interpretation |
| --- | ---: | --- | --- |
| Shared resist loss + max HP loss | 7/7 | all base afflictions | 折磨统一降低底层安全性。 |
| DMG down | 4/7 | Fearful, Paranoid, Selfish, Irrational | 多数折磨降低输出能力。 |
| DMG up | 1/7 | Abusive | 折磨可有局部正收益，但整体仍损坏队伍。 |
| ACC down | 5/7 | Paranoid, Selfish, Abusive, Hopeless, Irrational | 命中损坏是最常见个性化削弱。 |
| DODGE down | 4/7 | Masochistic, Abusive, Hopeless, Irrational | 半数以上降低防御可靠性。 |
| DODGE up | 3/7 | Fearful, Paranoid, Selfish | 退缩/自保类折磨反而更会躲。 |
| SPD down | 1/7 | Hopeless | 只有绝望显著拖慢。 |
| SPD up | 3/7 | Fearful, Paranoid, Irrational | 焦虑/混乱类折磨可能更快行动，但不代表更可靠。 |

### Agency Damage

| Agency damage | Base count | Members | Interpretation |
| --- | ---: | --- | --- |
| Any start-turn act-out | 7/7 | all base afflictions | 折磨核心是低频夺走控制权。 |
| Pass turn | 4/7 | Fearful, Selfish, Hopeless, Irrational | 直接损坏行动经济。 |
| Random skill | 4/7 | Paranoid, Selfish, Hopeless, Irrational | 让角色从工具变成不稳定因素。 |
| Forced movement | 6/7 | all except Abusive | 破坏站位和技能条件。 |
| Refuse retreat | 4/7 | Paranoid, Masochistic, Hopeless, Irrational | 破坏战略止损权。 |
| Refuse heal/buff/move | 4/7 direct high-severity | Paranoid, Masochistic, Hopeless, Irrational | 破坏救援与恢复窗口。 |
| Refuse camping skill | 7/7 in some form | all base afflictions | 破坏远征恢复计划。 |

### Team Damage

| Team damage | Base count | Members | Interpretation |
| --- | ---: | --- | --- |
| Party stress act-out | 7/7 | all base afflictions | 每种折磨都能污染队伍压力。 |
| Attack ally | 3/7 | Paranoid, Abusive, Irrational | 只有一部分折磨直接伤害队友。 |
| Ally-triggered stress comments | 7/7 in some form | all base afflictions | 队友行为会被折磨者重新解释成压力源。 |
| Curio/resource disruption | 4/7 direct compulsion | Fearful, Selfish, Masochistic, Irrational | 折磨影响战斗外资源收益与风险。 |

### Self-Damage / Exposure

| Self-damage direction | Base count | Members | Interpretation |
| --- | ---: | --- | --- |
| Attack self | 3/7 | Masochistic, Hopeless, Irrational | 自毁不是所有折磨的通用规则，只属于部分人格方向。 |
| Mark self | 3/7 | Masochistic, Hopeless, Irrational | 让敌人更容易集中火力。 |
| Move forward into danger | 2/7 direct | Masochistic, Hopeless | 折磨可以改变站位风险。 |
| Max HP shared loss | 7/7 | all base afflictions | 即使不自伤，所有折磨都降低生存底线。 |

## Affliction History

| History rule | Meaning |
| --- | --- |
| 每种基础折磨初始权重相同。 | 第一次折磨大体平等随机。 |
| 英雄每次获得某种折磨，该折磨未来权重上升。 | 角色会形成“习惯性崩溃方式”。 |
| 美德/折磨的先验检查独立于具体折磨历史。 | 先判定是否美德，再用历史决定具体折磨类型。 |
| 美德历史权重也会增长，但增长幅度低于折磨。 | 角色历史影响未来，但折磨人格更容易积累。 |

这点很重要：DD1 的“人格”不是开局选一个标签，而是由角色经历沉淀出来。玩家记住的不是公式，而是“这个人上次就这样崩过”。

## Design Interpretation

### What Virtue Rewards

| Reward layer | Evidence from DD1 | Design read |
| --- | --- | --- |
| Reliability | 美德不会拒绝命令，反而给正向 act-out。 | 美德首先是可靠性上升。 |
| Party stabilization | Courageous、Focused、Powerful 都直接帮队友；入场时也缓解压力。 | 美德不是个人 buff，而是队伍救场。 |
| Crisis conversion | 100 压力本应危险，美德把它变成翻盘窗口。 | 美德的价值来自发生在危机点。 |
| Simple archetype | 5 个美德主题非常直白。 | 美德不需要复杂树或机制绑定。 |

### What Affliction Damages

| Damage layer | Evidence from DD1 | Design read |
| --- | --- | --- |
| Reliability | act-out、pass、random skill、forced movement。 | 折磨核心是角色不能稳定执行计划。 |
| Team trust | party stress、ally attack、ally-triggered comments。 | 折磨会把一个人的崩溃变成队伍问题。 |
| Recovery windows | refuse heal/buff/camping/item/eat/retreat。 | 折磨不只影响战斗，还影响玩家止损。 |
| Survival margin | shared max HP/resist loss，DODGE/ACC/DMG 变化。 | 折磨让危险事件更容易滚起来。 |
| Exploration economy | curio compulsion、trap/curio comments。 | 折磨损坏远征资源管理。 |

### What DD1 Does Not Do

| Not done | Why it matters |
| --- | --- |
| 不给每个战斗机制单独配代价。 | 避免设计过重，也避免玩家觉得每张技能都被审计。 |
| 不把美德做成构筑路线奖励。 | 美德是危机中的戏剧反转，不是长期天赋树。 |
| 不让折磨只等于数值 debuff。 | 折磨通过行为、拒绝、队伍压力和探索破坏产生体验。 |
| 不隐藏压力条。 | 压力可见，阈值可预期，失控才可接受。 |

## Implications For Our Project

| Lesson | Apply to our design |
| --- | --- |
| 压力统一入口 | 不要让理想给每个机制配惩罚；压力可以来自战斗、事件、路线和选择。 |
| 美德纯正向 | 美德应是低频强正向，不要混入代价。 |
| 折磨损坏可靠性 | 折磨不必惩罚某个机制；它可以损坏出牌可靠性、奖励选择、事件选项、恢复窗口。 |
| 阈值必须可见 | 玩家需要看到压力条和危机接近。 |
| 个性来自历史 | 理想/经历可以改变美德/折磨候选权重，而不是每回合评价玩家行为。 |
| 数量要克制 | DD1 只有 5 个美德、7 个基础折磨。我们第一版应该更少。 |

## Suggested Minimal Adaptation

如果借 DD1，第一版不应做“大理想机制树”，而应做：

```text
1 个压力条
3 个美德
3 个折磨
少量历史权重
清晰的危机表现
```

示例结构：

| Component | Minimal version |
| --- | --- |
| Stress | 战斗伤害、失败事件、强行推进路线会增加。 |
| Resolve check | 压力满时检查美德/折磨。 |
| Virtue | 纯正向：减压、抽牌、强化下一张牌、保护一次失败。 |
| Affliction | 损坏可靠性：随机弃牌、拒绝奖励选项、临时塞入负面牌、压力传染。 |
| Ideal influence | 理想只调整候选权重和表现文本，不给每张牌加审计。 |
| History | 某英雄上次出现的折磨，下一次更容易重复。 |

## Key Takeaway

DD1 的统计结论很清楚：

```text
美德 = 危机中的可靠性上升 + 队伍稳定 + 纯正向反转。
折磨 = 可靠性下降 + 压力传染 + 恢复/撤退/资源管理被破坏。
```

它不是“机制越强，惩罚越强”的系统。它是“压力满后，人会以不同方式变得更可靠或更不可靠”的系统。

