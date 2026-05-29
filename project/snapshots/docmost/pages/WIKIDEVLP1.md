---
docmost_id: "019e6f70-b524-7f64-bf5b-7b0c360f52c2"
slug_id: "WIKIDEVLP1"
title: "开发与治理"
status: "active"
space: "General"
parent_page_id: "019e6f70-b503-7d81-bca1-28e3ff1598b1"
created_at: "2026-05-28 16:35:17.88626+00"
updated_at: "2026-05-28 16:35:17.88626+00"
deleted_at: ""
---

# 开发与治理

- Status: `active`
- Path: `PHDGAME 正式 Wiki / 开发与治理`
- Slug: `WIKIDEVLP1`

## Content

来源：docs/wiki/development.md





状态: Active



负责人: Team



范围: 开发协作、架构入口和文档治理导航



权威性: No



最后复核: 2026-05-27

项目方向

当前长期方向是 pygame 内部的 Godot 化：优先推进架构迁移、节点化、runtime UI 和清晰边界，而不是一次性迁移到 Godot。







主题



入口





当前方向



CURRENT_DIRECTION.md





默认命令



DEFAULT_ENTRYPOINTS.md





开发文档索引



development/README.md





任务池



CODEX_TASK_POOL.md





决策日志



DECISION_LOG.md





项目管理



docs/project/README.md

文档治理







规则



入口





设计文档治理



DESIGN_DOC_GOVERNANCE_V1.md





项目记忆规则



PROJECT_MEMORY_INDEX.md





删除策略



DELETE_POLICY.md





Cloudflare 私有发布



Cloudflare 私有 Wiki 发布说明





Wiki 项目仪表盘



项目管理

常用验证







场景



命令





构建 Wiki



py -3.11 tools/wiki_site/build.py --source docs/wiki --output site/wiki --repo-url https://github.com/LiuZesensengsheng/PHDGAME --repo-ref master --discussion-category general





测 Wiki 构建器



py -3.11 -m pytest tests/tools/test_wiki_site_build.py -q





卡牌生成



python scripts/cards_csv_to_json.py --generate-all-colors





卡牌生成测试



python -m pytest tests/scripts/test_cards_csv_to_json.py -q





仓库完整测试



python -m pytest -q

评论和 AI 感知

当前版本：





Wiki 页面由 docs/wiki/*.md 生成。



页面底部链接到 GitHub Discussions。



讨论内容受私有仓库权限控制。



AI 能直接感知仓库文件；讨论内容需要后续同步或手动拉取。

后续增强可以做：





周期性拉取 GitHub Discussions。



把讨论摘要写入 docs/wiki/_discussion_cache/。



让 AI 基于摘要提出 Wiki 修改建议。



经过人工确认后再改 Markdown。

## Comments

_No comments exported for this page._
