---
docmost_id: "019e6f70-b518-7d3b-8d1d-baf8bf479c66"
slug_id: "WIKIPROGR1"
title: "进展总览"
status: "active"
space: "General"
parent_page_id: "019e6f70-b503-7d81-bca1-28e3ff1598b1"
created_at: "2026-05-28 16:35:17.88626+00"
updated_at: "2026-05-31 01:36:28.657+00"
deleted_at: ""
---

# 进展总览

- Status: `active`
- Path: `PHDGAME 正式 Wiki / 进展总览`
- Slug: `WIKIPROGR1`

## Content

来源：docs/wiki/progress.md





状态: Draft



负责人: Team



范围: 项目驾驶舱与进展评估



权威性: No



最后复核: 2026-05-28

当前核心方向

当前最重要的方向是把 Wiki 做成项目驾驶舱：让项目进展、资产、能力、TODO、里程碑和讨论摘要都能被人浏览，也能被 AI 稳定读取和核对。

源头记录在 docs/project/progress/overview.md。本页是给人阅读的 Wiki 摘要。

方向评估







方向



当前判断



成熟度



证据



下一步





中文 Wiki 阅读层



已可本地预览、可发布，并开始有分级导航。



原型



Wiki 构建器



补齐进展总览、逻辑图和信息架构。





Repo-first 项目管理



会议纪要、TODO、里程碑、当前状态已经进入仓库。



已验证



项目管理入口



用检查工具降低手工维护漂移。





GitHub 信号同步



Issues、Milestones、Discussions 已能生成只读快照。



已验证



GitHub 同步报告



评估自动同步 PR。





资产与能力台账



资产、能力和 Project Control 检查已经建立。



已验证



资产与能力



评估从 JSON 自动生成 Wiki 表格。





内容设计治理



Wiki 正在承接设计阅读入口，旧文档仍需分批治理。



草案



设计总览



先做候选归档清单，不主动删除。





AI 协作入口



AGENTS.md、进展页、台账和 Wiki 形成 AI 上下文。



原型



开发与治理



让每次项目管理迭代更新进展摘要。





Docmost 协作层试验



已准备本地 sandbox 配置，但当前机器还未安装 Docker，尚未启动。



想法



Docmost sandbox



安装 Docker Desktop 后验证编辑、评论、图和导出体验。

管理闭环

flowchart TD
  A[讨论 / 会议 / GitHub 信号] --> B[人工或脚本同步]
  B --> C[docs/project 源文档]
  C --> D[JSON 台账与快照]
  C --> E[docs/wiki 阅读页]
  D --> F[Project Control 检查]
  E --> G[私有 Wiki 预览 / 发布]
  F --> H[AI 读取并提出 PR 建议]
  G --> H
  H --> I[人类复核与合并]
  I --> C


近期优先级







优先级



工作



完成信号





P0



进展总览和 Wiki 逻辑图



本页可浏览，Mermaid 图能渲染。





P1



Project Control 扩展检查



检查器覆盖 progress、TODO、会议、里程碑的基础关系。





P1



讨论同步自动化评估



有 GitHub Action 或手动同步 runbook。





P2



台账生成 Wiki 表格



assets.md 表格可以由工具生成或校验。





P2



设计文档分批治理



每批只提出候选，删除或归档经过 owner 确认。

读法







想知道



去哪里





当前项目管理事实



项目管理





资产和能力是否可靠



资产与能力





当前设计哪些可信



设计总览





当前协作和发布方式



开发与治理





机器可读进展源



docs/project/progress/overview.md

## Comments

_No comments exported for this page._
