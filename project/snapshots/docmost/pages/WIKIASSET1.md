---
docmost_id: "019e6f70-b520-7493-b781-bc7cc477c10b"
slug_id: "WIKIASSET1"
title: "资产与能力"
status: "active"
space: "General"
parent_page_id: "019e6f70-b503-7d81-bca1-28e3ff1598b1"
created_at: "2026-05-28 16:35:17.88626+00"
updated_at: "2026-05-28 16:35:17.88626+00"
deleted_at: ""
---

# 资产与能力

- Status: `active`
- Path: `PHDGAME 正式 Wiki / 资产与能力`
- Slug: `WIKIASSET1`

## Content

来源：docs/wiki/assets.md





状态: 草案



负责人: 团队



范围: 项目资产与能力台账



权威性: 否



最后复核: 2026-05-28

目标

这个页面是资产和能力台账的阅读入口。机器可读源放在：





资产台账



能力台账

台账的目标不是增加文档负担，而是让项目进度、资产状态、代码证据和下一步工作能被人和 AI 同时核对。
本页展示使用中文名称；底层 JSON 台账仍保留英文枚举，便于脚本校验和自动化同步。

成熟度







状态



含义





想法



只有想法，还没有稳定文件。





草案



已有草稿，但缺少验证或权威收口。





原型



可以使用，但仍在快速变化。





已验证



有测试、报告或流程证据支撑。





稳定



已长期使用，且变更需要明确复核。





已退役



已停止使用，但保留历史记录。

资产台账摘要







ID



名称



类型



状态



权威入口



下一步





ASSET-WIKI-001



中文 Wiki 阅读入口



文档资产



原型



docs/wiki/README.md



补齐进度与资产管理页面，并稳定发布链路。





ASSET-PROJECT-001



Repo-first 项目管理目录



项目管理



已验证



docs/project/README.md



由 project_control 工具检查核心台账关系。





ASSET-SYNC-001



GitHub 项目信号同步快照



工具链



已验证



tools/project_sync/README.md



评估是否用 GitHub Action 自动同步并开 PR。





ASSET-CONTENT-001



核心内容设计文档集合



内容设计



草案



docs/wiki/design.md



逐页把稳定结论沉淀到 Wiki，旧文档只做候选归档清单。





ASSET-PROGRESS-001



项目进展总览



项目管理



原型



docs/project/progress/overview.md



用 Project Control 继续检查进展页是否存在并可被 Wiki 读取。

能力台账摘要







ID



名称



能力域



状态



权威入口



下一步





CAP-WIKI-001



静态 Wiki 构建与本地预览



Wiki 建设



已验证



tools/wiki_site/README.md



把生产发布链路纳入项目控制检查。





CAP-PROJECT-001



会议纪要、TODO、里程碑的 repo-first 管理



项目管理



原型



docs/project/README.md



用 project_control 工具检查 ID、状态和引用关系。





CAP-DISCUSS-001



GitHub Discussions 评论同步与 Wiki 页脚展示



协作评论



已验证



tools/project_sync/README.md



评估自动同步 PR 和独立 Wiki discussion 分类。





CAP-CONTENT-001



内容包身份和运行时输出可见性



内容管线



已验证



CONTENT_PACK_MINIMAL_V1.md



把内容包能力摘要纳入资产与能力 Wiki。





CAP-VISUAL-001



Wiki Mermaid 逻辑图渲染



Wiki 建设



原型



tools/wiki_site/README.md



核对本地和线上发布环境是否都能渲染逻辑图。

维护方式

python scripts/check_project_control.py


后续如果台账变大，可以由工具从 JSON 自动生成本页表格。V1 先保持手工可读和工具可查。

## Comments

_No comments exported for this page._
