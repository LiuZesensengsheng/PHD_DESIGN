# 资产与能力

- 状态: Draft
- 负责人: Team
- 范围: 项目资产与能力台账
- 权威性: No
- 最后复核: 2026-05-28

## 目标

这个页面是资产和能力台账的阅读入口。机器可读源放在：

- [资产台账](../project/assets/registry.json)
- [能力台账](../project/capabilities/registry.json)

台账的目标不是增加文档负担，而是让项目进度、资产状态、代码证据和下一步工作能被人和 AI 同时核对。

## 成熟度

| 状态 | 含义 |
| --- | --- |
| Idea | 只有想法，还没有稳定文件。 |
| Draft | 已有草稿，但缺少验证或权威收口。 |
| Prototype | 可以使用，但仍在快速变化。 |
| Tested | 有测试、报告或流程证据支撑。 |
| Stable | 已长期使用，且变更需要明确复核。 |
| Retired | 已停止使用，但保留历史记录。 |

## 资产台账摘要

| ID | 名称 | 类型 | 状态 | 权威入口 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| ASSET-WIKI-001 | 中文 Wiki 阅读入口 | documentation | Prototype | [docs/wiki/README.md](README.md) | 补齐进度与资产管理页面，并稳定发布链路。 |
| ASSET-PROJECT-001 | Repo-first 项目管理目录 | project_management | Tested | [docs/project/README.md](../project/README.md) | 由 project_control 工具检查核心台账关系。 |
| ASSET-SYNC-001 | GitHub 项目信号同步快照 | tooling | Tested | [tools/project_sync/README.md](../../tools/project_sync/README.md) | 评估是否用 GitHub Action 自动同步并开 PR。 |
| ASSET-CONTENT-001 | 核心内容设计文档集合 | content_design | Draft | [docs/wiki/design.md](design.md) | 逐页把稳定结论沉淀到 Wiki，旧文档只做候选归档清单。 |

## 能力台账摘要

| ID | 名称 | 能力域 | 状态 | 权威入口 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| CAP-WIKI-001 | 静态 Wiki 构建与本地预览 | wiki | Tested | [tools/wiki_site/README.md](../../tools/wiki_site/README.md) | 把生产发布链路纳入项目控制检查。 |
| CAP-PROJECT-001 | 会议纪要、TODO、里程碑的 repo-first 管理 | project_management | Prototype | [docs/project/README.md](../project/README.md) | 用 project_control 工具检查 ID、状态和引用关系。 |
| CAP-DISCUSS-001 | GitHub Discussions 评论同步与 Wiki 页脚展示 | collaboration | Tested | [tools/project_sync/README.md](../../tools/project_sync/README.md) | 评估自动同步 PR 和独立 Wiki discussion 分类。 |
| CAP-CONTENT-001 | 内容包身份和运行时输出可见性 | content_pipeline | Tested | [CONTENT_PACK_MINIMAL_V1.md](../development/content/CONTENT_PACK_MINIMAL_V1.md) | 把内容包能力摘要纳入资产与能力 Wiki。 |

## 维护方式

```bash
python scripts/check_project_control.py
```

后续如果台账变大，可以由工具从 JSON 自动生成本页表格。V1 先保持手工可读和工具可查。
