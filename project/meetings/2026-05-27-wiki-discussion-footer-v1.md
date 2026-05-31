# Wiki 讨论页脚 V1

- 日期: 2026-05-27
- 参与者: User, Codex
- 关联: `docs/wiki/`, `tools/project_sync/`, `tools/wiki_site/`
- 状态: Draft

## 背景

Wiki 正文需要继续保留在仓库 Markdown 中，方便 Git 追踪、PR 复核和回滚。
讨论和评论更适合放在 GitHub Discussions 中，保留互动、图片、通知和权限能力。

## 结论

采用“Wiki 正文 + 页面底部讨论区摘要”的方案：

1. GitHub Discussions 继续作为评论和讨论来源。
2. `tools/project_sync` 只读同步 Discussions 的最近评论。
3. 同步结果写入 `docs/wiki/_discussion_cache/discussions.json`。
4. Wiki 构建器在页面底部渲染“最近讨论”和最近评论预览。
5. 如果页面已有对应 Discussion，底部按钮直接链接到已有讨论；否则链接到新建讨论表单。

## TODO

| ID | 事项 | 负责人 | 状态 | 目标 |
| --- | --- | --- | --- | --- |
| PM-004 | 设计 GitHub Discussions 评论同步脚本 | Codex | Done | M3 |
| PM-005 | 页面底部显示讨论摘要 | Codex | Done | M3 |
| PM-007 | 同步 Discussions 评论正文和最近评论摘要 | Codex | Done | M3 |

## 未决问题

- 是否需要为 Wiki 讨论单独创建 GitHub Discussion category。
- 是否需要 GitHub Action 定期运行同步脚本并自动开 PR。
- 评论预览是否需要显示图片附件摘要。

## 后续同步

先用手动同步验证体验。稳定后再决定是否做自动同步 PR。
