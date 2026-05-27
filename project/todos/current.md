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
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | In Progress | Team | M3 | 当前只同步讨论列表和评论数；评论正文待补。 |
| PM-005 | 页面底部显示讨论摘要 | Planned | Team | M3 | 先只读展示，不站内发评论。 |
| PM-006 | 评估 OAuth 或 GitHub App 站内写入 | Later | Team | M4 | 等只读同步和展示稳定后再判断。 |
| PM-007 | 同步 Discussions 评论正文和最近评论摘要 | Planned | Team | M3 | 为页面评论摘要和 AI 感知准备。 |
| PM-008 | 决定 GitHub milestones 是否作为阶段进度源 | Planned | Team | M2/M3 | 当前 GitHub milestones 为空。 |

## 当前焦点

当前焦点转向 M3：把 GitHub Discussions 的评论正文和页面摘要同步进仓库，让评论能被 AI 更及时地感知。
