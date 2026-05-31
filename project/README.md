# 项目管理入口

- 状态: Draft
- 负责人: Team
- 范围: repo-first 项目管理
- 权威性: Yes, as a project-management index
- 最后复核: 2026-05-27

## 目标

`docs/project/` 用来把项目管理数据放进仓库，让人和 AI 都能读取、核对、追踪和复盘。

这里不替代 GitHub Issues、Milestones、Projects 或 Discussions。第一版采用轻量闭环：

```text
GitHub 讨论 / TODO / 里程碑
  -> 同步或人工整理
  -> docs/project/
  -> docs/project/snapshots/docmost/
  -> AI 读取、总结、提出更新建议
```

## 目录

| 区域 | 文件 | 用途 |
| --- | --- | --- |
| 当前状态 | [status/current.md](status/current.md) | 当前项目管理快照、阻塞项和下一步。 |
| GitHub 同步报告 | [status/github.md](status/github.md) | 从 GitHub Issues、Milestones、Discussions 拉取的只读摘要。 |
| 进展总览 | [progress/overview.md](progress/overview.md) | 当前核心方向、方向评估、优先级和项目驾驶舱闭环。 |
| 项目计划 | [planning/README.md](planning/README.md) | 目标、需求、任务和自动生成的计划总览。 |
| 会议纪要 | [meetings/README.md](meetings/README.md) | 每次会议的索引和记录模板。 |
| TODO | [todos/current.md](todos/current.md) | 当前手工维护的 TODO 清单。 |
| 里程碑 | [milestones/README.md](milestones/README.md) | 阶段目标、完成标准和当前进度。 |
| 资产台账 | [assets/README.md](assets/README.md) | 项目文档、工具、数据包和协作资产的状态索引。 |
| 能力台账 | [capabilities/README.md](capabilities/README.md) | Wiki、Docmost、同步、治理和验证能力的状态索引。 |
| 同步快照 | [snapshots/README.md](snapshots/README.md) | AI 可读 JSON 快照。 |

## 规则

1. 每次形成项目管理结论时，补一条会议纪要。
2. 会议纪要里的行动项要进入 `todos/current.md`，除非它只是口头备忘。
3. 目标、需求、任务尽量有稳定 ID，方便 AI 和人引用。
4. 里程碑只记录阶段目标，不塞日常碎任务。
5. GitHub Issues/Discussions 同步上线前，本目录可以手工维护。
6. 后续脚本同步时，保留人工摘要，不把原始 API 快照当成唯一可读入口。
7. 资产和能力进入台账后，必须能被 `python scripts/check_project_control.py` 检查。

## 与其他目录的边界

| 目录 | 边界 |
| --- | --- |
| `docs/project/` | 项目管理、会议、TODO、里程碑、AI 可读进展。 |
| `docs/project/snapshots/docmost/` | Docmost 的 Git 快照；用于 AI 感知、审计和回滚。 |
| `docs/development/` | 稳定架构、开发规则、工作流规则。 |
| `docs/pm/` | 重要决策、取舍、回滚说明。 |
| `docs/logs/` | 短期 AI 交接和周期性记忆压缩。 |

## 后续自动化方向

| 阶段 | 目标 |
| --- | --- |
| V1 | 手工维护项目管理文件，Docmost 负责展示。 |
| V2 | 从 GitHub Issues/Milestones 拉取 TODO 和进度快照。 |
| V3 | 从 GitHub Discussions 拉取页面评论和会议讨论摘要。 |
| V4 | 资产、能力和进展台账进入项目驾驶舱。 |
| V5 | AI 定期生成项目状态更新 PR。 |
| V6 | 评估是否需要 OAuth 或 GitHub App 站内写入。 |

## 同步命令

```bash
python scripts/sync_project_management.py --fetch-github --repo LiuZesensengsheng/PHDGAME
```

该命令只读 GitHub，输出 `docs/project/status/github.md` 和 `docs/project/snapshots/*.json`。

## 项目控制检查

```bash
python scripts/check_project_control.py
```

该命令检查资产台账、能力台账、TODO、会议纪要、里程碑、进展页和核心项目管理入口是否存在且基本一致。

## 项目计划生成

```bash
python scripts/generate_project_planning_dashboard.py
```

该命令从 `docs/project/planning/*.json` 生成项目计划总览。
