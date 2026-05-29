---
docmost_id: "019e6f54-85f4-7744-902d-257ca5f2e075"
slug_id: "dr8JDgn1Zs"
title: "富文本与结构图试验"
status: "deleted"
space: "General"
parent_page_id: ""
created_at: "2026-05-28 16:04:30.834123+00"
updated_at: "2026-05-28 16:07:03.178+00"
deleted_at: "2026-05-29 00:46:11.21+00"
---

# 富文本与结构图试验

- Status: `deleted`
- Path: `富文本与结构图试验`
- Slug: `dr8JDgn1Zs`

## Content

用途

 

这一页专门测试 Docmost 是否适合作为唯一内容源：能不能同时承载正文、任务、结构图、项目管理记录和评论。

结构图试验：人-AI-Wiki 闭环

flowchart TD
  A[团队在 Docmost 写作和评论] --> B[AI 读取评论和页面]
  B --> C[提炼成 Wiki 正文改动]
  C --> D[更新 Docmost 正式页]
  D --> E[导出到 Git 镜像分支]
  E --> F[审计 / 回滚 / 静态 Wiki 生成]
  F --> B


任务清单试验





 评论处理前必须转成页面正文或 TODO。



 处理完成后允许解决评论，不把评论当长期档案。



 Docmost 作为唯一内容源，Git 作为镜像和审计层。

项目管理字段试验







方向



状态



下一步





评论治理



进行中



写一个评论收集与处理流程





富文本能力



测试中



验证 Mermaid / 表格 / 图片





唯一源策略



待确认



决定 Docmost 写回流程

评论治理规则草案





评论可以被解决后消失。



解决前必须确认：评论里的要求已经进入正文、TODO、会议纪要或明确拒绝记录。



AI 的工作不是保存所有评论，而是及时把评论变成可维护的 Wiki 内容。

## Comments

_No comments exported for this page._
