# 资产与能力

- 状态: Draft
- 负责人: Team
- 范围: 项目资产与能力台账
- 权威性: No
- 最后复核: 2026-05-29

## 目标

这个页面是资产和能力台账的阅读入口。机器可读源放在：

| 台账 | 入口 |
| --- | --- |
| 资产台账 | [registry.json](../project/assets/registry.json) |
| 能力台账 | [registry.json](../project/capabilities/registry.json) |

台账的目标不是增加文档负担，而是让项目进度、资产状态、代码证据和下一步工作能被人和 AI 同时核对。

## 成熟度

| 状态 | 含义 |
| --- | --- |
| 想法 | 只有想法，还没有稳定入口。 |
| 草案 | 已有草稿，但缺少验证或权威收口。 |
| 原型 | 可以使用，但仍在快速变化。 |
| 已验证 | 有测试、报告或流程证据支撑。 |
| 稳定 | 已长期使用，且变更需要明确复核。 |
| 已退役 | 已停止使用，但保留历史记录。 |

## 资产台账摘要

| ID | 名称 | 类型 | 状态 | 权威入口 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| ASSET-WIKI-001 | 中文 Wiki 阅读入口 | 文档资产 | 原型 | [Wiki 首页](README.md) | 补齐进展、资产与能力页面，并稳定发布链路。 |
| ASSET-DOCMOST-001 | Docmost 本地协作层 | 协作系统 | 原型 | [Docmost Mirror](../../tools/docmost_mirror/README.md) | 本地试运行一到两周。 |
| ASSET-PROJECT-001 | Repo-first 项目管理目录 | 项目管理 | 已验证 | [项目管理入口](../project/README.md) | 用检查脚本降低手工维护漂移。 |
| ASSET-SYNC-001 | GitHub 项目信号同步工具 | 工具链 | 已验证 | [Project Sync](../../tools/project_sync/README.md) | 评估定期同步 PR。 |
| ASSET-DOCMOST-SNAPSHOT-001 | Docmost 到 Git 快照 | 快照 | 原型 | [Docmost 快照索引](../project/snapshots/docmost/index.md) | 固定评论处理规则。 |
| ASSET-CONTENT-001 | 核心内容设计文档集合 | 内容设计 | 草案 | [设计总览](design.md) | 稳定结论进 Wiki，旧文档只进候选清单。 |
| ASSET-TA-001 | TA 敌人与遭遇内容包 | 内容包 | 已验证 | [TA manifest](../../data/combat/ta/manifest.json) | 逐步生成 TA 敌人和遭遇索引。 |
| ASSET-CARDANALYSIS-001 | Combat Analysis 设计辅助工具链 | 工具链 | 已验证 | [Combat Analysis](../../tools/combat_analysis/README.md) | 把常用能力提升到能力台账。 |
| ASSET-ACK-001 | 致谢系统设计资料 | 设计参考 | 草案 | [致谢系统 v2](../design/campaign/ACKNOWLEDGEMENTS_SYSTEM_v2.md) | 保留并标注可信度。 |
| ASSET-GOVERNANCE-001 | 文档治理与删除策略 | 治理 | 已验证 | [设计文档治理](../development/architecture/DESIGN_DOC_GOVERNANCE_V1.md) | 删除或归档前先给 owner 确认。 |

## 能力台账摘要

| ID | 名称 | 能力域 | 状态 | 权威入口 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| CAP-WIKI-001 | 静态 Wiki 构建与本地预览 | Wiki 建设 | 已验证 | [Wiki Site Tooling](../../tools/wiki_site/README.md) | 把资产和进展页纳入导航。 |
| CAP-DOCMOST-001 | Docmost 页面导出到 Git 快照 | 协作评论 | 原型 | [Docmost Mirror](../../tools/docmost_mirror/README.md) | 本地试运行并整理评论。 |
| CAP-PROJECT-001 | 会议纪要、TODO、里程碑的 repo-first 管理 | 项目管理 | 原型 | [项目管理入口](../project/README.md) | 每次整理后更新项目状态。 |
| CAP-DISCUSS-001 | GitHub 项目信号同步 | 协作评论 | 已验证 | [Project Sync](../../tools/project_sync/README.md) | 决定 milestones 是否作为阶段源。 |
| CAP-ASSET-001 | 资产与能力台账维护 | 治理 | 原型 | [资产台账](../project/assets/README.md) | 先维护核心对象。 |
| CAP-CONTENT-001 | 内容包身份和运行时输出可见性 | 内容管线 | 已验证 | [Content Pack Minimal](../development/content/CONTENT_PACK_MINIMAL_V1.md) | 纳入更多内容包摘要。 |
| CAP-CARDANALYSIS-001 | 卡牌与战斗设计分析 | 设计辅助 | 已验证 | [Combat Analysis](../../tools/combat_analysis/README.md) | 标出最可靠入口。 |
| CAP-LONGTERM-001 | 长期系统设计资料治理 | 内容治理 | 草案 | [奖励与长期系统](rewards.md) | 把致谢、声望、期刊、会议等长期系统分批标注可信度。 |
| CAP-GOVERNANCE-001 | 文档治理和删除确认流程 | 治理 | 已验证 | [设计文档治理](../development/architecture/DESIGN_DOC_GOVERNANCE_V1.md) | 继续坚持确认后再删。 |
| CAP-VALIDATION-001 | 仓库验证与测试入口 | 验证 | 已验证 | [默认命令](../development/DEFAULT_ENTRYPOINTS.md) | 把项目控制检查纳入维护流程。 |

## 维护方式

```bash
python scripts/check_project_control.py
```

后续如果台账继续变大，可以由工具从 JSON 自动生成本页表格。V1 先保持手工可读和工具可查。
