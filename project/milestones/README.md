# 里程碑

- 状态: Draft
- 负责人: Team
- 范围: project-milestones
- 最后复核: 2026-05-27

## 目标

这里记录项目管理系统本身的阶段目标。游戏内容、架构或发布里程碑仍应保留在它们各自的规划文档中。

## 当前里程碑

| ID | 名称 | 状态 | 完成标准 |
| --- | --- | --- | --- |
| M0 | 中文 Wiki V1 | In Progress | 中文 Wiki 页面可本地预览，导航结构稳定，能发布到 Cloudflare。 |
| M1 | Repo-first 项目管理 MVP | Done | `docs/project/` 有会议、TODO、里程碑、当前状态，Wiki 有项目管理页面。 |
| M2 | GitHub TODO 同步 | Done | 能从 GitHub Issues/Milestones 拉取快照并生成 AI 可读摘要。 |
| M3 | GitHub 讨论同步 | In Progress | 能从 Discussions 拉取页面评论和会议讨论摘要，并展示在 Wiki。 |
| M4 | 站内写入评估 | Later | 根据使用体验决定是否引入 OAuth 或 GitHub App。 |
| M5 | Project Control 台账 | In Progress | 资产台账、能力台账和检查工具可用于核查项目治理结构。 |

## 当前阶段说明

M1 的目的不是做完整项目管理后台，而是建立最小闭环：

1. 项目管理事实进入仓库。
2. Wiki 能展示这些事实。
3. AI 能读取这些事实。
4. 后续同步脚本有明确目标格式。
