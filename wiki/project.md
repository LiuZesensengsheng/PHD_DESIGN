# 项目管理

- 状态: Draft
- 负责人: Team
- 范围: 项目管理 Wiki 仪表盘
- 权威性: No
- 最后复核: 2026-05-27

## 目标

这个页面把项目管理数据展示给人看；真正的项目管理记录放在 `docs/project/`，后续会同步 GitHub Issues、Milestones 和 Discussions。

核心目标是：让 TODO、会议纪要、讨论和里程碑都能被 AI 读取、核对和追踪。

## 当前状态

| 区域 | 状态 | 入口 |
| --- | --- | --- |
| 项目管理入口 | 已建立 | [docs/project/README.md](../project/README.md) |
| 当前状态快照 | 已建立 | [current.md](../project/status/current.md) |
| GitHub 同步报告 | 已建立 | [github.md](../project/status/github.md) |
| 会议纪要 | 已建立 | [meetings/README.md](../project/meetings/README.md) |
| TODO 清单 | 已建立 | [todos/current.md](../project/todos/current.md) |
| 里程碑 | 已建立 | [milestones/README.md](../project/milestones/README.md) |
| JSON 快照 | 已建立 | [snapshots/README.md](../project/snapshots/README.md) |

## GitHub 同步快照

| 指标 | 当前值 |
| --- | --- |
| Open issues | 11 |
| GitHub milestones | 0 |
| Discussions | 1 |
| 最新报告 | [GitHub 项目同步报告](../project/status/github.md) |

## 会议纪要

| 日期 | 主题 | 纪要 |
| --- | --- | --- |
| 2026-05-27 | Wiki 项目管理 V1 | [Wiki 项目管理 V1 会议纪要](../project/meetings/2026-05-27-wiki-project-management-v1.md) |
| 2026-05-27 | GitHub 项目同步 V1 | [GitHub 项目同步 V1 会议纪要](../project/meetings/2026-05-27-github-project-sync-v1.md) |

## 当前 TODO

| ID | 事项 | 状态 | 目标 |
| --- | --- | --- | --- |
| PM-001 | 建立 `docs/project/` 项目管理骨架 | Done | M1 |
| PM-002 | 增加 Wiki 项目管理页面 | Done | M1 |
| PM-003 | 设计 GitHub Issues/Milestones 同步脚本 | Done | M2 |
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | In Progress | M3 |
| PM-005 | 页面底部显示讨论摘要 | Planned | M3 |
| PM-006 | 评估 OAuth 或 GitHub App 站内写入 | Later | M4 |
| PM-007 | 同步 Discussions 评论正文和最近评论摘要 | Planned | M3 |
| PM-008 | 决定 GitHub milestones 是否作为阶段进度源 | Planned | M2/M3 |

## 里程碑

| ID | 名称 | 状态 | 含义 |
| --- | --- | --- | --- |
| M0 | 中文 Wiki V1 | In Progress | 中文 Wiki 可浏览、可本地预览、可发布。 |
| M1 | Repo-first 项目管理 MVP | Done | 项目管理信息进入仓库并展示到 Wiki。 |
| M2 | GitHub TODO 同步 | Done | 从 Issues/Milestones 生成仓库快照。 |
| M3 | GitHub 讨论同步 | In Progress | 从 Discussions 生成页面评论和会议摘要。 |
| M4 | 站内写入评估 | Later | 决定是否需要 OAuth 或 GitHub App。 |

## 工作流

```text
开会 / 讨论 / 产生行动项
  -> docs/project/meetings/YYYY-MM-DD-topic.md
  -> docs/project/todos/current.md
  -> docs/project/milestones/README.md
  -> docs/wiki/project.md
  -> AI 读取并提出更新建议
```

## 后续增强

1. 自动从 GitHub Issues 拉取 TODO。
2. 自动从 GitHub Milestones 拉取阶段进度。
3. 自动从 GitHub Discussions 拉取页面评论。
4. 在 Wiki 页面底部展示最近讨论摘要。
5. 由 AI 定期生成项目状态更新 PR。
