---
docmost_id: "019e6f70-b527-7214-96c2-fc793f7d7b82"
slug_id: "WIKICFACC1"
title: "Cloudflare 私有 Wiki 发布说明"
status: "active"
space: "General"
parent_page_id: "019e6f70-b503-7d81-bca1-28e3ff1598b1"
created_at: "2026-05-28 16:35:17.88626+00"
updated_at: "2026-05-31 01:43:18.447+00"
deleted_at: ""
---

# Cloudflare 私有 Wiki 发布说明

- Status: `active`
- Path: `PHDGAME 正式 Wiki / Cloudflare 私有 Wiki 发布说明`
- Slug: `WIKICFACC1`

## Content

来源：docs/wiki/CLOUDFLARE_PAGES_ACCESS_RUNBOOK.md





状态: Draft



负责人: Team



范围: 私有 Wiki 部署



权威性: No



最后复核: 2026-05-27

目标

把 docs/wiki/*.md 发布成一个带访问门禁的私有网站，同时让 GitHub 继续作为 Markdown、提交记录、PR 和讨论的源头。

docs/wiki/*.md
  -> tools/wiki_site/build.py
  -> Cloudflare Workers static assets
  -> Cloudflare Access 登录


仓库构建设置

Cloudflare 可能把入口显示成 Create a Worker，这没有问题。仓库里的 wrangler.jsonc 会告诉 Cloudflare 上传 site/wiki 里的静态文件。







设置项



推荐值





Project name



phd-wiki





Production branch



master





Build command



python tools/wiki_site/build.py --source docs/wiki --output site/wiki --repo-url https://github.com/LiuZesensengsheng/PHDGAME --repo-ref master --discussion-category general





Root directory



仓库根目录





Python version



3.11

如果 Cloudflare 没有自动识别 Python 3.11，可以增加环境变量：







变量



值





PYTHON_VERSION



3.11

不要把 build command 留空。仓库不提交预构建 HTML，Cloudflare 需要先运行构建命令，再上传 site/wiki。

Access 门禁

为 Workers 域名创建一个 Cloudflare Access application。

推荐第一版策略：







字段



值





Action



Allow





Include



指定邮箱列表或指定邮箱域名





Login method



One-time PIN 或 GitHub identity provider





Session duration



1 周到 3 个月，按团队体验调整

不要把“不公开网址”当作隐私方案。私有 Wiki 应该在加载任何 HTML、图片或搜索索引前先经过 Access 登录。

GitHub Discussions

GitHub Discussions 保持开启。每个生成页面底部都有“讨论此页”链接，会打开对应的 GitHub Discussion 草稿。

私有仓库中，讨论内容仍受仓库成员权限控制。也就是说，有仓库访问权限的人可以互相看到讨论。

图片

Wiki 图片放在：

docs/wiki/assets/
docs/wiki/<section>/assets/


Markdown 写法：

![图片说明](assets/example.png)


构建器会复制 docs/wiki 下任意 assets/ 目录到生成站点。

本地验证

py -3.11 tools/wiki_site/build.py --source docs/wiki --output site/wiki --repo-url https://github.com/LiuZesensengsheng/PHDGAME --repo-ref master --discussion-category general
py -3.11 -m pytest tests/tools/test_wiki_site_build.py -q


构建后打开：

site/wiki/index.html


当前限制







限制



当前状态



后续方向





评论展示



现在是跳转到 GitHub Discussions



后续可把讨论摘要同步回仓库并展示在页面





AI 感知



AI 目前通过仓库文件和手动拉取讨论感知



后续可做定期同步脚本





Cloudflare Access 配置



账号侧配置，不完整存进仓库



保留 runbook，必要时截图或补充步骤

## Comments

_No comments exported for this page._
