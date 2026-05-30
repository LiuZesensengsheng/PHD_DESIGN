# 当前项目状态

- 状态: Draft
- 负责人: Team
- 范围: project-status-snapshot
- 最后复核: 2026-05-27

## 摘要

当前优先目标是把项目管理纳入仓库：会议纪要、TODO、里程碑、资产、能力、进展和讨论摘要都应该能被 AI 读取，并能在 Wiki 上以更友好的方式展示。

第一版不做 OAuth，不做自建后台。先用 GitHub、Docmost 本地试验和仓库文件作为协作/审计层，Wiki 作为前台阅读层。

## 当前阶段

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| 中文 Wiki V1 | 进行中 | 已建立中文 Wiki 骨架，本地可预览。 |
| Repo-first 项目管理 | 已建立 | 已建立 `docs/project/`、会议纪要、TODO、里程碑入口和 Wiki 项目管理页。 |
| GitHub 讨论同步 | 部分建立 | 已能拉取 Discussions 列表和评论数；评论正文和页面摘要仍待补。 |
| GitHub TODO 同步 | 已建立 | 已能拉取 Issues/Milestones 并生成 `docs/project/status/github.md` 和 JSON 快照。 |
| 资产与能力台账 | V1 已建立 | 已建立资产、能力和进展总览的源码入口，供 AI 后续维护。 |
| 目标-需求-任务计划 | V1 已建立 | 已建立 `docs/project/planning/`，可生成项目计划总览和甘特图。 |
| Docmost 本地协作层 | 试运行 | 本地 Docmost 用于富文本、评论、会议和临时协作；Git 保存镜像快照。 |
| 站内写入/OAuth | 暂缓 | 等 V1/V2 稳定后再评估。 |

## 当前阻塞

| 阻塞 | 影响 | 下一步 |
| --- | --- | --- |
| 评论还不能嵌入页面 | 页面只能跳转到 GitHub Discussion | 先同步评论正文和摘要，再评估嵌入式展示。 |
| GitHub milestones 为空 | 当前 issue 无法按阶段自动统计 | 先决定是否在 GitHub 建 milestones，或继续由 `docs/project/milestones/` 管阶段。 |
| 线上发布需要 PR 合并 | 本地能看，线上要等部署 | 只提交本次 Wiki/Project 相关文件。 |
| Docmost 与 Git 的事实源关系需要稳定 | 如果不整理，评论和正文可能漂移 | 先采用“Docmost 协作，Git 审计，AI 整理 PR”的本地试运行流程。 |

## 下一步

1. 本地试运行 Docmost 一到两周，观察评论、会议纪要和 TODO 是否能顺畅整理回 Git。
2. 继续补充目标、需求和任务，并用 `python scripts/generate_project_planning_dashboard.py` 生成总览。
3. 维护资产与能力台账 V1，并用 `python scripts/check_project_control.py` 检查。
4. 为 Discussions/Docmost 同步补评论正文、最近评论和页面摘要。
5. 决定是否在 GitHub 建 milestones，或继续用仓库内里程碑文档。
