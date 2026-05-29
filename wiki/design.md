# 设计总览

- 状态: Active
- 负责人: Team
- 范围: 设计资料导航
- 权威性: No
- 最后复核: 2026-05-27

## 用途

这个页面负责回答一个问题：当前那么多设计文档里，哪些最值得先看。

它不是 `docs/design/` 的替代品。真正的设计依据仍然来自活跃设计文档、运行时数据、代码和测试。

## 当前权威入口

| 区域 | 入口 | 当前姿态 |
| --- | --- | --- |
| 跨系统体验原则 | [DESIGN_NORTH_STAR_V1.md](../design/DESIGN_NORTH_STAR_V1.md) | 活跃北极星。用于判断敌人、遭遇、事件和卡牌是否有共鸣、感动、乐趣和谈资。 |
| 设计文档治理 | [DESIGN_DOC_GOVERNANCE_V1.md](../development/architecture/DESIGN_DOC_GOVERNANCE_V1.md) | 活跃规则。用于区分 Active、Draft、Reference、Future、Archive。 |
| 设计资料总入口 | [docs/design/README.md](../design/README.md) | 当前设计目录的权威地图。 |
| 理想与卡牌 | [ideal/README.md](../design/ideal/README.md) | 试点治理中。红色和白色较活跃，绿色仍偏草案。 |
| 战役与教程 | [campaign/README.md](../design/campaign/README.md) | 试点治理中。教程任务链是当前主要落地点。 |
| 敌人与遭遇 | [enemydesigon/README.md](../design/enemydesigon/README.md) | 试点治理中。TA 线已有实现映射。 |
| 归档设计 | [archive/README.md](../design/archive/README.md) | 默认不进入当前实现路径。 |
| 清理候选 | [CLEANUP_CANDIDATES.md](../design/archive/CLEANUP_CANDIDATES.md) | 只是复核队列，不等于删除许可。 |

## 运行时锚点

| 运行时区域 | 位置 |
| --- | --- |
| 红色卡牌 | `data/cards/red/` |
| 白色卡牌 | `data/cards/white/` |
| 教程叙事源 | `data/narrative_src/packs/tutorial/` |
| 教程运行时任务链 | `data/questlines/questline_tutorial.json` |
| TA 战斗源包 | `data/combat/ta/` |
| TA 运行时遭遇 | `data/questlines/encounters_ta.json` |

## 第一版 Wiki 的边界

| 做 | 不做 |
| --- | --- |
| 把信息整理成可浏览索引 | 不删除、不移动源文档 |
| 标明活跃、草案、参考和归档关系 | 不把草案写成已实现 |
| 给每个栏目提供下一跳链接 | 不重写 `docs/design/` 的原始内容 |
| 为讨论和评论预留入口 | 不在当前版本内嵌实时评论 |

## 清理原则

旧设计文档需要小批次处理：

1. 先让活跃规格和运行时锚点可见。
2. 先提出低风险候选：临时文件、重复旧稿、乱码笔记、已解压保留的原始包。
3. 对价值不清楚的设计材料，优先标记为草案、参考、未来、归档或被替代。
4. 删除必须经过 owner 明确确认。
