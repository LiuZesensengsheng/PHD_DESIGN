# Wiki 项目管理 V1 会议纪要

- 日期: 2026-05-27
- 参与者: User, Codex
- 关联: `docs/wiki/`, `docs/project/`
- 状态: Draft

## 背景

用户希望项目管理数据进入仓库，让 AI 能及时读取、追踪、核对和总结。使用体验要尽量友好，但最核心的是数据可追踪、可版本化、可被 AI 感知。

## 结论

1. 第一版采用 repo-first 项目管理，不立即做 OAuth 或自建后台。
2. GitHub Issues/Milestones/Discussions 作为后续协作后台。
3. `docs/project/` 作为 AI 和人都能读取的项目管理层。
4. Wiki 增加“项目管理”页面，用更友好的方式展示会议、TODO、里程碑和讨论入口。
5. 每次形成项目管理结论时，都应该在 `docs/project/meetings/` 增加会议纪要。

## TODO

| ID | 事项 | 负责人 | 状态 | 目标 |
| --- | --- | --- | --- | --- |
| PM-001 | 建立 `docs/project/` 项目管理骨架 | Codex | Done | 本次迭代 |
| PM-002 | 增加 Wiki 项目管理页面 | Codex | Done | 本次迭代 |
| PM-003 | 设计 GitHub Issues/Milestones 同步脚本 | Team | Planned | 下一阶段 |
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | Team | Planned | 下一阶段 |
| PM-005 | 评估是否需要 OAuth 或 GitHub App 站内写入 | Team | Later | 同步展示稳定后 |

## 未决问题

1. TODO 是否完全迁移到 GitHub Issues，还是保留仓库内手工 TODO 清单作为主入口。
2. 会议纪要是优先写 Markdown，还是优先开 GitHub Discussion 后同步回来。
3. 页面评论摘要是否展示全文、最近 N 条，还是 AI 摘要。

## 后续同步

本次会议产生的行动项已进入 `docs/project/todos/current.md`，阶段目标进入 `docs/project/milestones/README.md`。
