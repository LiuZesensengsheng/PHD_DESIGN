# 战役与路线

- 状态: Active
- 负责人: Team
- 范围: 战役、教程任务链和路线导航
- 权威性: No
- 最后复核: 2026-05-27

## 概览

战役页对应经典爬塔 Wiki 里的地图、楼层、事件路线和进程说明。本项目当前最清楚的战役内容是教程任务链。

## 当前入口

| 内容 | 当前状态 | 入口 |
| --- | --- | --- |
| 战役设计索引 | 活跃索引 | [campaign/README.md](../design/campaign/README.md) |
| 教程任务链总览 | 活跃设计 | [00_overview_and_core_mechanics.md](../design/campaign/questline_tutorial/00_overview_and_core_mechanics.md) |
| 教程节点细节 | 参考 | `docs/design/campaign/questline_tutorial/01_*` 到 `03_*` |
| 教程叙事源 | 已落地数据 | `data/narrative_src/packs/tutorial/` |
| 教程运行时任务链 | 已落地数据 | `data/questlines/questline_tutorial.json` |

## 教程 source pack

| 文件 | 用途 |
| --- | --- |
| `manifest.json` | 内容包身份 |
| `nodes.csv` | 教程节点 |
| `choices.csv` | 选项 |
| `conditions.csv` | 条件 |
| `consequences.csv` | 后果 |
| `locales_zh_CN.csv` | 中文文本 |
| `_draft_id_map.csv` | 草案 ID 映射辅助表 |

## 战役开发锚点

| 主题 | 入口 |
| --- | --- |
| 战役生命周期 | [CAMPAIGN_LIFECYCLE_MACHINE_V1.md](../development/campaign/CAMPAIGN_LIFECYCLE_MACHINE_V1.md) |
| 任务区边界 | [CAMPAIGN_TASK_AREA_BOUNDARY_V1.md](../development/campaign/CAMPAIGN_TASK_AREA_BOUNDARY_V1.md) |
| 任务区触发表面 | [CAMPAIGN_TASK_AREA_TRIGGER_SURFACE_V1.md](../development/campaign/CAMPAIGN_TASK_AREA_TRIGGER_SURFACE_V1.md) |
| 战役状态收口 | [CAMPAIGN_STATE_STRANGLER_V1.md](../development/campaign/CAMPAIGN_STATE_STRANGLER_V1.md) |

## 待补页面

后续可以补：

1. 教程路线图。
2. 节点列表。
3. 事件触发条件。
4. 战役 UI 页面截图和说明。
