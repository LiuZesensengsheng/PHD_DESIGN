# 资产台账

- 状态: Draft
- 负责人: Team
- 范围: project-asset-registry
- 最后复核: 2026-05-28

## 目标

资产台账记录项目中值得长期追踪的文档、内容、工具和工程资产。
它回答三个问题：

1. 这个资产现在在哪里？
2. 它当前成熟到什么程度？
3. 下一步要如何让它更可靠？

机器可读源是 `registry.json`。本页解释填写规则，Wiki 负责展示摘要。

## 字段

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定 ID，格式为 `ASSET-AREA-001`。 |
| `name` | 人可读名称。 |
| `type` | 资产类型，例如 `documentation`、`content_design`、`tooling`。 |
| `status` | 成熟度，见下方状态表。 |
| `owner` | 当前维护负责人。 |
| `authoritative_page` | 权威入口，优先指向 Wiki 或项目治理文档。 |
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

## 维护命令

```bash
python scripts/check_project_control.py
```

该命令会检查 ID、状态、必填字段、文件引用和证据引用。
