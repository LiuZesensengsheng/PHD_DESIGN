# 能力台账

- 状态: Draft
- 负责人: Team
- 范围: project-capability-registry
- 最后复核: 2026-05-29

## 目标

这里记录项目当前已经具备、正在试验或计划补齐的能力。

能力和资产的区别：

- 资产是“有什么东西”，例如 Wiki、工具链、内容包、设计资料。
- 能力是“能稳定做什么”，例如构建 Wiki、导出 Docmost、同步 GitHub、运行验证。

机器可读源是 [registry.json](registry.json)。

## 状态

| 状态 | 含义 |
| --- | --- |
| idea | 只有想法，还没有稳定入口。 |
| draft | 有草稿流程，但还不能稳定复用。 |
| prototype | 可以执行，但仍需要人工看护。 |
| validated | 有测试、脚本或实际输出支撑。 |
| stable | 已成为常规工作流。 |
| retired | 已停止使用，但保留历史记录。 |

## 能力摘要

| ID | 名称 | 能力域 | 状态 | 权威入口 |
| --- | --- | --- | --- | --- |
| CAP-WIKI-001 | 静态 Wiki 构建与本地预览 | wiki | validated | `tools/wiki_site/README.md` |
| CAP-DOCMOST-001 | Docmost 页面导出到 Git 快照 | collaboration | prototype | `tools/docmost_mirror/README.md` |
| CAP-PROJECT-001 | 会议纪要、TODO、里程碑的 repo-first 管理 | project_management | prototype | `docs/project/README.md` |
| CAP-DISCUSS-001 | GitHub 项目信号同步 | collaboration | validated | `tools/project_sync/README.md` |
| CAP-ASSET-001 | 资产与能力台账维护 | governance | prototype | `docs/project/assets/README.md` |
| CAP-CONTENT-001 | 内容包身份和运行时输出可见性 | content_pipeline | validated | `docs/development/content/CONTENT_PACK_MINIMAL_V1.md` |
| CAP-CARDANALYSIS-001 | 卡牌与战斗设计分析 | design_assist | validated | `tools/combat_analysis/README.md` |
| CAP-LONGTERM-001 | 长期系统设计资料治理 | content_governance | draft | `docs/wiki/rewards.md` |
| CAP-GOVERNANCE-001 | 文档治理和删除确认流程 | governance | validated | `docs/development/architecture/DESIGN_DOC_GOVERNANCE_V1.md` |
| CAP-VALIDATION-001 | 仓库验证与测试入口 | validation | validated | `docs/development/DEFAULT_ENTRYPOINTS.md` |

## 维护规则

1. 能力必须有入口，最好有验证方式。
2. `validated` 以上状态必须能指出测试、脚本、报告或实际产物。
3. 能力台账不承诺功能已经产品化；它只描述 AI 和团队现在能不能稳定依赖。
4. 能力发生退化时，先降级状态，不直接删除记录。
