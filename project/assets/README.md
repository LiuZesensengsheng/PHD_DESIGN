# 资产台账

- 状态: Draft
- 负责人: Team
- 范围: project-asset-registry
- 最后复核: 2026-05-30

## 目标

这里记录项目里值得被长期追踪的资产：文档入口、工具链、数据包、协作系统和关键治理材料。

资产台账不是删除清单。它的作用是帮助人和 AI 知道：

1. 哪些东西当前可依赖。
2. 哪些东西只是原型或草案。
3. 哪些入口是权威入口。
4. 后续整理时应该先看哪里。

机器可读源是 [registry.json](registry.json)。本页解释填写规则；Docmost 负责面向团队的阅读和讨论。

## 字段

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定 ID，格式为 `ASSET-AREA-001`。 |
| `name` | 人可读名称。 |
| `type` | 资产类型，例如 `documentation`、`content_design`、`tooling`。 |
| `status` | 成熟度，见下方状态表。 |
| `owner` | 当前维护负责人。 |
| `authoritative_page` | 权威入口，优先指向 Docmost 快照、项目治理文档或工具说明。 |
| `related_files` | 相关源码、文档或数据文件。 |
| `evidence` | 测试、会议纪要、报告或其他可核查证据。 |
| `milestone` | 相关阶段目标。 |
| `risks` | 已知风险。 |
| `next_step` | 下一步动作。 |

## 状态

| 状态 | 含义 |
| --- | --- |
| Idea | 只有想法，还没有稳定文件。 |
| Draft | 已有草稿，但缺少验证或权威收口。 |
| Prototype | 可以使用，但仍在快速变化。 |
| Tested | 有测试、报告或流程证据支撑。 |
| Stable | 已长期使用，且变更需要明确复核。 |
| Retired | 已停止使用，但保留历史记录。 |

## 资产摘要

| ID | 名称 | 类型 | 状态 | 权威入口 |
| --- | --- | --- | --- | --- |
| ASSET-WIKI-001 | 旧静态 Wiki 阅读入口 | documentation | Retired | `tools/wiki_site/README.md` |
| ASSET-DOCMOST-001 | Docmost Wiki 正文源 | collaboration | Prototype | `tools/docmost_mirror/README.md` |
| ASSET-PROJECT-001 | Repo-first 项目管理目录 | project_management | Tested | `docs/project/README.md` |
| ASSET-SYNC-001 | GitHub 项目信号同步工具 | tooling | Tested | `tools/project_sync/README.md` |
| ASSET-DOCMOST-SNAPSHOT-001 | Docmost 到 Git 快照 | snapshot | Prototype | `docs/project/snapshots/docmost/index.md` |
| ASSET-CONTENT-001 | 核心内容设计文档集合 | content_design | Draft | `docs/project/snapshots/docmost/index.md` |
| ASSET-TA-001 | TA 敌人与遭遇内容包 | content_pack | Tested | `data/combat/ta/manifest.json` |
| ASSET-CARDANALYSIS-001 | Combat Analysis 设计辅助工具链 | tooling | Tested | `tools/combat_analysis/README.md` |
| ASSET-ACK-001 | 致谢系统设计资料 | design_reference | Draft | `docs/design/campaign/ACKNOWLEDGEMENTS_SYSTEM_v2.md` |
| ASSET-GOVERNANCE-001 | 文档治理与删除策略 | governance | Tested | `docs/development/architecture/DESIGN_DOC_GOVERNANCE_V1.md` |

## 维护命令

```bash
python scripts/check_project_control.py
```

该命令会检查 ID、状态、必填字段、文件引用和证据引用。

## 维护规则

1. 新增重要协作面、工具、数据包或设计集合时，补一条资产记录。
2. 资产状态只能描述“当前可信程度”，不能替代删除确认。
3. `retired` 表示不再主动使用，不等于可以删除。
4. 删除、归档、移动资产前，仍然需要人工确认。
