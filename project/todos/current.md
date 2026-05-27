# 当前 TODO

- 状态: Draft
- 负责人: Team
- 范围: project-todo-board
- 最后复核: 2026-05-27

## 规则

TODO 第一版先手工维护。后续接入 GitHub Issues 后，本页可以变成同步摘要，而不是唯一数据源。

状态取值：

| 状态 | 含义 |
| --- | --- |
| Planned | 已确认要做，但还没开始。 |
| In Progress | 正在做。 |
| Blocked | 被外部条件或决策卡住。 |
| Review | 等待人工核对或 PR 复核。 |
| Done | 已完成。 |
| Later | 暂缓，不进入当前阶段。 |

## TODO 清单

| ID | 事项 | 状态 | 负责人 | 目标阶段 | 备注 |
| --- | --- | --- | --- | --- | --- |
| PM-001 | 建立 `docs/project/` 项目管理骨架 | Done | Codex | M1 | 本次迭代创建入口、会议、TODO、里程碑。 |
| PM-002 | 增加 Wiki 项目管理页面 | Done | Codex | M1 | 在 Wiki 中展示项目管理入口。 |
| PM-003 | 设计 GitHub Issues/Milestones 同步脚本 | Done | Codex | M2 | 已新增 `tools/project_sync/` 和 `scripts/sync_project_management.py`。 |
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | Done | Codex | M3 | 已同步讨论列表、评论数和最近评论正文。 |
| PM-005 | 页面底部显示讨论摘要 | Done | Codex | M3 | Wiki 页脚已显示最近讨论和评论预览。 |
| PM-006 | 评估 OAuth 或 GitHub App 站内写入 | Later | Team | M4 | 等只读同步和展示稳定后再判断。 |
| PM-007 | 同步 Discussions 评论正文和最近评论摘要 | Done | Codex | M3 | 已写入 `docs/wiki/_discussion_cache/discussions.json`。 |
| PM-008 | 决定 GitHub milestones 是否作为阶段进度源 | Planned | Team | M2/M3 | 当前 GitHub milestones 为空。 |

## 当前焦点

当前 M3 的只读讨论链路已经建立：GitHub Discussions 评论会同步进仓库缓存，并在 Wiki 页脚展示最近讨论。下一步是评估是否需要自动同步 PR 或单独的 Wiki 讨论分类。
