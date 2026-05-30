# PHD 模拟器 Wiki

- 状态: Active
- 负责人: Team
- 范围: 面向读者的项目 Wiki 首页
- 权威性: No
- 最后复核: 2026-05-27

## 首页

这里是 `PHD_SIMULATER` 的第一版中文 Wiki。它借鉴经典爬塔类 Wiki 的结构，把信息拆成容易浏览的栏目：卡牌、机制、敌人、事件、路线、奖励、术语和开发状态。

Wiki 是阅读层，不是第二套真相源。真正的设计依据仍然在 `docs/design/`、`docs/development/`、`docs/pm/`、运行时数据和测试里。

## 快速入口

| 栏目 | 适合查看什么 | 页面 |
| --- | --- | --- |
| 当前状态 | 项目方向、哪些内容可靠、哪些只是草案 | [设计总览](design.md) |
| 角色与理想 | 红色、白色、绿色理想的定位和状态 | [角色与理想](characters.md) |
| 卡牌 | 卡牌颜色、卡牌数据、当前已落地卡组入口 | [卡牌](cards.md) |
| 机制 | 战斗、能量、回合、战役和数据规则 | [机制](systems.md) |
| 战役与路线 | 教程任务链、节点、路线和运行时数据 | [战役与路线](campaign.md) |
| 敌人与遭遇 | TA 线、单场遭遇、敌人数据入口 | [敌人与遭遇](enemies.md) |
| 事件与叙事 | 教程叙事、事件草案、叙事 source pack | [事件与叙事](events.md) |
| 奖励与长期系统 | 致谢、期刊、声望、会议等暂未完全收口的系统 | [奖励与长期系统](rewards.md) |
| 进展总览 | 核心方向、方向评估、优先级和项目管理闭环 | [进展总览](progress.md) |
| 项目管理 | 会议纪要、TODO、里程碑、当前进展 | [项目管理](project.md) |
| 项目计划 | 目标、需求、任务、进度统计和甘特图 | [项目计划](planning.md) |
| 资产与能力 | 项目资产、能力成熟度、证据和下一步 | [资产与能力](assets.md) |
| 术语 | 常用设计词和状态标签 | [术语表](glossary.md) |
| 开发协作 | 架构、入口命令、文档治理、发布方式 | [开发与治理](development.md) |

## 像经典游戏 Wiki 一样读

| 你想查 | 先看 | 再看 |
| --- | --- | --- |
| 这张牌现在有没有实现 | [卡牌](cards.md) | `data/cards/red/`, `data/cards/white/` |
| 某条设计现在能不能信 | [设计总览](design.md) | `docs/design/README.md` 和状态卡 |
| TA 线有哪些敌人和遭遇 | [敌人与遭遇](enemies.md) | `data/combat/ta/`, `data/questlines/encounters_ta.json` |
| 教程剧情现在在哪里 | [事件与叙事](events.md) | `data/narrative_src/packs/tutorial/` |
| 当前项目方向是什么 | [开发与治理](development.md) | `docs/development/CURRENT_DIRECTION.md` |
| 当前 TODO 和会议纪要在哪里 | [项目管理](project.md) | `docs/project/` |
| 当前目标、需求和任务是什么 | [项目计划](planning.md) | `docs/project/planning/` |
| 当前核心进展方向是什么 | [进展总览](progress.md) | `docs/project/progress/overview.md` |
| 哪些资产和能力可依赖 | [资产与能力](assets.md) | `docs/project/assets/` 和 `docs/project/capabilities/` |

## 内容状态

| 状态 | 含义 |
| --- | --- |
| 已落地 | 已经有运行时数据、代码或测试支撑 |
| 活跃设计 | 当前可作为设计依据，但仍可能继续调整 |
| 草案 | 有想法或局部设计，不能直接当作实现承诺 |
| 参考 | 有历史价值或辅助判断价值，不自动覆盖活跃设计 |
| 归档 | 默认不进入当前实现路径 |
| 待整理 | 需要人工确认后再决定保留、重写、归档或删除 |

## 讨论入口

每个生成后的网页底部都有 GitHub Discussion 链接。仓库是私有时，讨论仍受私有仓库权限控制；有权限的人可以互相看到讨论内容。

当前版本的评论是“跳转到 GitHub 讨论”，还没有把评论实时嵌入页面。后续可以做讨论同步，让 AI 定期读取讨论并生成 Wiki 更新建议。
