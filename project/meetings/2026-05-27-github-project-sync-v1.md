# GitHub 项目同步 V1 会议纪要

- 日期: 2026-05-27
- 参与者: User, Codex
- 关联: `tools/project_sync/`, `docs/project/status/github.md`
- 状态: Draft

## 背景

用户要求开始执行项目管理同步迭代。目标是让 GitHub Issues、Milestones 和 Discussions 的项目管理信号进入仓库，方便 AI 读取、核对、追踪和生成后续建议。

## 结论

1. 新增 `tools/project_sync/` 作为只读同步工具。
2. 新增 `scripts/sync_project_management.py` 作为稳定入口。
3. 同步输出写入 `docs/project/status/github.md` 和 `docs/project/snapshots/*.json`。
4. 当前真实仓库同步结果：11 个 open issues，0 个 milestones，1 个 discussion。
5. Discussions V1 先同步讨论列表和评论数；评论正文和页面摘要留给下一步。

## TODO

| ID | 事项 | 负责人 | 状态 | 目标 |
| --- | --- | --- | --- | --- |
| PM-003 | 设计 GitHub Issues/Milestones 同步脚本 | Codex | Done | M2 |
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | Team | In Progress | M3 |
| PM-007 | 同步 Discussions 评论正文和最近评论摘要 | Team | Planned | M3 |
| PM-008 | 决定 GitHub milestones 是否作为阶段进度源 | Team | Planned | M2/M3 |

## 未决问题

1. 是否在 GitHub 里建立 M0/M1/M2/M3/M4 milestones，让同步报告能自动显示阶段进度。
2. Discussion 评论正文同步后，Wiki 页面是显示最近 N 条，还是显示 AI 摘要。
3. 站内写入仍暂缓，等待只读同步和展示体验稳定。
