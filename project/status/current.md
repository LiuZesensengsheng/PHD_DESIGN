# 当前项目状态

- 状态: Draft
- 负责人: Team
- 范围: project-status-snapshot
- 最后复核: 2026-05-27

## 摘要

当前优先目标是把项目管理纳入仓库：会议纪要、TODO、里程碑和讨论摘要都应该能被 AI 读取，并能在 Wiki 上以更友好的方式展示。

第一版不做 OAuth，不做自建后台。先用 GitHub 和仓库文件作为后台，Wiki 作为前台。

## 当前阶段

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| 中文 Wiki V1 | 进行中 | 已建立中文 Wiki 骨架，本地可预览。 |
| Repo-first 项目管理 | 已建立 | 已建立 `docs/project/`、会议纪要、TODO、里程碑入口和 Wiki 项目管理页。 |
| GitHub 讨论同步 | 部分建立 | 已能拉取 Discussions 列表和评论数；评论正文和页面摘要仍待补。 |
| GitHub TODO 同步 | 已建立 | 已能拉取 Issues/Milestones 并生成 `docs/project/status/github.md` 和 JSON 快照。 |
| 站内写入/OAuth | 暂缓 | 等 V1/V2 稳定后再评估。 |

## 当前阻塞

| 阻塞 | 影响 | 下一步 |
| --- | --- | --- |
| 评论还不能嵌入页面 | 页面只能跳转到 GitHub Discussion | 先同步评论正文和摘要，再评估嵌入式展示。 |
| GitHub milestones 为空 | 当前 issue 无法按阶段自动统计 | 先决定是否在 GitHub 建 milestones，或继续由 `docs/project/milestones/` 管阶段。 |
| 线上发布需要 PR 合并 | 本地能看，线上要等部署 | 只提交本次 Wiki/Project 相关文件。 |

## 下一步

1. 核对当前项目管理 Wiki 页面是否好读。
2. 为 Discussions 同步补评论正文、最近评论和页面摘要。
3. 决定是否在 GitHub 建 milestones，或继续用仓库内里程碑文档。
4. 再评估页面内评论摘要的展示形态。
