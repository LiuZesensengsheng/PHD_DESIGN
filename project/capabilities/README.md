# 能力台账

- 状态: Draft
- 负责人: Team
- 范围: project-capability-registry
- 最后复核: 2026-05-28

## 目标

能力台账记录项目已经具备、正在建设或准备沉淀的能力。
它不是功能愿望清单，而是“我们实际能依赖什么”的状态表。

机器可读源是 `registry.json`。Wiki 展示面向人的摘要，工具负责检查结构。

## 字段

| 字段 | 含义 |
| --- | --- |
| `id` | 稳定 ID，格式为 `CAP-AREA-001`。 |
| `name` | 能力名称。 |
| `domain` | 能力域，例如 `wiki`、`project_management`、`content_pipeline`。 |
| `status` | 成熟度，和资产台账共用状态。 |
| `owner` | 当前维护负责人。 |
| `authoritative_page` | 权威说明入口。 |
| `related_files` | 能力相关源码、数据或文档。 |
| `evidence` | 测试、报告、会议纪要或其他验证证据。 |
| `milestone` | 相关阶段目标。 |
| `risks` | 已知风险。 |
| `next_step` | 下一步动作。 |

## 什么时候新增能力

满足以下任一情况时，新增或更新能力台账：

1. 某个工具或流程已经可以被重复使用。
2. 某个工程能力有测试或报告支撑。
3. 某个项目管理流程会影响后续 AI 协作。
4. 某个能力不再可靠，需要降级或退休。

## 维护命令

```bash
python scripts/check_project_control.py
```
