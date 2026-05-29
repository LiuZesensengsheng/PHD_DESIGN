# 机制

- 状态: Active
- 负责人: Team
- 范围: 核心玩法机制导航
- 权威性: No
- 最后复核: 2026-05-27

## 概览

机制页用于查“游戏规则怎么运转”。它对应经典爬塔 Wiki 里的 mechanics、status、intent、map、turn order 等页面。

当前项目仍处在架构和内容并行演进期，所以这里优先给入口，不把未完成系统写成已完成规则。

## 核心机制入口

| 机制 | 当前状态 | 入口 |
| --- | --- | --- |
| 战斗事件契约 | 活跃开发规则 | [COMBAT_EVENT_CONTRACT_V1.md](../development/combat/COMBAT_EVENT_CONTRACT_V1.md) |
| 战斗时序 | 活跃开发规则 | [COMBAT_TIMING_CONTRACT_V1.md](../development/combat/COMBAT_TIMING_CONTRACT_V1.md) |
| 能量模型 | 活跃方向 | [COMBAT_ENERGY_UNIFICATION_V2.md](../development/combat/COMBAT_ENERGY_UNIFICATION_V2.md) |
| 战役生命周期 | 活跃开发规则 | [CAMPAIGN_LIFECYCLE_MACHINE_V1.md](../development/campaign/CAMPAIGN_LIFECYCLE_MACHINE_V1.md) |
| 强制事件门 | 活跃开发规则 | [CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md](../development/campaign/CAMPAIGN_FORCED_EVENT_NARROW_PLAN_V1.md) |
| 内容包身份 | 活跃开发规则 | [CONTENT_PACK_MINIMAL_V1.md](../development/content/CONTENT_PACK_MINIMAL_V1.md) |

## 第一版机制词

| 词 | 说明 |
| --- | --- |
| 能量 | 当前方向是统一标量能量，而不是彩色能量池。 |
| 回合 | 战斗时序和触发顺序以 combat development docs、代码和测试为准。 |
| 自信 | 防御类资源或数值表现，具体行为以运行时实现为准。 |
| 任务区 | 战役中承载节点、任务、触发和 UI 交互的区域概念。 |
| forced event | 战役中需要被门控处理的强制事件，当前有窄版长期方案。 |
| content pack | 内容源包身份和加载边界，当前 V1 只做最小 manifest 约束。 |

## 运行时优先级

当 Wiki、设计文档和代码不一致时，优先级通常是：

1. 当前运行时数据、代码和测试。
2. `docs/development/` 中的活跃契约。
3. `docs/design/` 中带状态卡的 active spec。
4. Wiki 页面。

如果出现冲突，不要静默拼接；先记录差异，再决定更新文档还是调整实现。
