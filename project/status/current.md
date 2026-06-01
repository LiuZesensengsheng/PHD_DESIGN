# 当前项目状态

- 状态: Draft
- 负责人: Team
- 范围: project-status-snapshot
- 最后复核: 2026-06-02

## 摘要

当前优先目标是把项目管理纳入仓库：会议纪要、TODO、里程碑、资产、能力、进展和讨论摘要都应该能被 AI 读取，并能从 Docmost 快照中核对。

Wiki 正文源收敛到 Docmost。Git 不再维护独立 `docs/wiki` 内容源，只保存 Docmost 导出的快照、项目管理文件和审计记录。

## 当前阶段

| 阶段 | 状态 | 说明 |
| --- | --- | --- |
| Docmost Wiki 源 | 试运行 | Docmost 是唯一 Wiki 正文源；Git 保存导出快照。 |
| Repo-first 项目管理 | 已建立 | 已建立 `docs/project/`、会议纪要、TODO、里程碑入口和项目管理 dashboard。 |
| GitHub 讨论同步 | 已建立 | 已能拉取 Discussions 列表、评论数和最近评论正文，作为项目快照材料。 |
| GitHub TODO 同步 | 已建立 | 已能拉取 Issues/Milestones 并生成 `docs/project/status/github.md` 和 JSON 快照。 |
| 资产与能力台账 | 已建立 | 已新增资产台账、能力台账和 Project Control 检查工具。 |
| 目标-需求-任务计划 | V1 已建立 | 已建立 `docs/project/planning/`，可生成项目计划总览和甘特图。 |
| Docmost 本地协作层 | 试运行 | 本地 Docmost 用于富文本、评论、会议和临时协作；Git 保存镜像快照。 |
| 站内写入/OAuth | 暂缓 | 等 V1/V2 稳定后再评估。 |

## 当前阻塞

| 阻塞 | 影响 | 下一步 |
| --- | --- | --- |
| Docmost 快照仍需手动导出 | Docmost 新正文和评论不会自动进入 Git | 先手动运行导出脚本；稳定后评估定时导出或自动 PR。 |
| GitHub milestones 为空 | 当前 issue 无法按阶段自动统计 | 先决定是否在 GitHub 建 milestones，或继续由 `docs/project/milestones/` 管阶段。 |
| Docmost 与 Git 的事实源关系需要稳定 | 如果不定期导出，AI 只能看到旧快照 | 先采用“Docmost 正文源，Git 审计快照，AI 整理 PR”的本地试运行流程。 |
| 旧静态 Wiki 链路已删除 | 旧 `docs/wiki` 内容源、静态 HTML 构建器和 Cloudflare Workers 配置已移除 | 仅保留 Docmost 导出的历史快照；默认检查转向 Docmost 快照。 |
| 废弃 `phd-wiki` 外部检查已清理 | `Workers Builds: phd-wiki` 来自 Cloudflare Workers and Pages 外部 App，不是仓库 GitHub Actions | 已在 Cloudflare 侧处理废弃服务/集成；下一次 PR 验证该外部检查不再出现。 |
| cardanalysis 进入 hosted router + 中文人审包阶段 | 已有 report-only 生成、修复、验证、能力图和路由链路 | 当前路由结果会在需要时请求人类审核；下一步是把中文审核反馈回灌成下一轮约束。 |

## 下一步

1. 本地试运行 Docmost 一到两周，观察评论、会议纪要和 TODO 是否能顺畅整理回 Git。
2. 继续补充目标、需求和任务，并用 `python scripts/generate_project_planning_dashboard.py` 生成总览。
3. 维护资产与能力台账 V1，并用 `python scripts/check_project_control.py` 检查。
4. 评估是否把 Discussions/Docmost 同步改成自动 PR，而不是手动触发。
5. 决定是否在 GitHub 建 milestones，或继续用仓库内里程碑文档。
6. 验证下一次 PR 不再出现废弃的 `Workers Builds: phd-wiki` 外部检查。
7. 继续 cardanalysis 的“中文审核反馈 -> 下一轮约束”闭环。
