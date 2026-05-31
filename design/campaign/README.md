# 战役设计入口

- Status: Active
- Owner: Team
- Scope: campaign/tutorial-design
- Canonical: Yes, as a directory index
- Supersedes: none
- Superseded By: none
- Implemented In: `data/narrative_src/packs/tutorial/`, `data/questlines/`
- Last Reviewed: 2026-05-17

## 默认读取顺序

1. 先读 `../DESIGN_NORTH_STAR_V1.md`
2. 教程任务链先读 `questline_tutorial/00_overview_and_core_mechanics.md`
3. 需要节点细节时再读 `questline_tutorial/01_*` 到 `03_*`
4. 需要系统灵感时再读本目录其他 campaign reference
5. 运行时、加载、content-pack 权威关系读 `docs/development/content/CONTENT_PACK_MINIMAL_V1.md`

## 当前状态

| 文档 | 状态 | Canonical | 用途 |
| --- | --- | --- | --- |
| `questline_tutorial/00_overview_and_core_mechanics.md` | Active | Yes, for tutorial questline design | 教程任务链的当前设计入口。 |
| `questline_tutorial/01_node1_onboarding.md` 到 `03_node3_defense_and_endings.md` | Reference | No | 节点细节和历史设计展开。 |
| `GANTT_TASKS_EVENTS.md`, `GANTT_FUSION_RULES.md`, `GANTT_DDL_SNAKE_RULES.md` | Reference | No | 甘特任务、融合、DDL snake 等玩法灵感和机制草案。 |
| `ACKNOWLEDGEMENTS_SYSTEM_v2.md` | Draft | No | 致谢系统较新的设计草案。 |
| `ACKNOWLEDGEMENTS_SYSTEM.md` | Frozen | No | 致谢系统早期参考稿，保留在 campaign 目录；当前扩展以 v2 为准。 |
| `ACADEMIC_PRESTIGE_SYSTEM.md`, `JOURNAL_SYSTEM_DESIGN.md`, `MEETING_EVENTS_BRANCHING.md`, `NODE_MEETING_ONPAGER.md` | Draft / Reference | No | 战役系统局部设计，使用前需确认当前实现边界。 |

## Source Of Truth

- 教程内容的当前规范化来源是 `data/narrative_src/packs/tutorial/`。
- 当前运行时产物在 `data/questlines/questline_tutorial.json`, `data/questlines/rewards_tutorial.json`, `data/questlines/encounters_tutorial.json`。
- content-pack 和 loader 权威关系以 `docs/development/content/CONTENT_PACK_MINIMAL_V1.md` 及相关实现为准。
- 本目录文档可以解释设计意图，但不能覆盖运行时数据、加载契约或测试。

## 下一次治理建议

- 给 `questline_tutorial/01_*` 到 `03_*` 补 Reference 状态卡。
- 判断致谢、期刊、组会、学术声望系统中哪一条下一步会进入 active。
- 如果新的战役系统被接受，需要同步补 decision log 或 `docs/development/campaign/` 规则。
