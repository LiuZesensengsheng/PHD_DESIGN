# Project Control 台账 V1

- 日期: 2026-05-28
- 参与者: User, Codex
- 关联: `docs/project/assets/`, `docs/project/capabilities/`, `tools/project_control/`, `docs/wiki/assets.md`
- 状态: Draft

## 背景

项目需要一个能长期维护整体进度、资产、能力和后续工作的治理层。
用户希望 Wiki 逐步成为统一入口，同时仍然需要工具核查源文档和代码进展是否一致。

## 结论

采用轻量 Project Control V1：

1. `docs/project/assets/registry.json` 作为资产台账机器源。
2. `docs/project/capabilities/registry.json` 作为能力台账机器源。
3. `docs/wiki/assets.md` 作为面向人的资产与能力阅读入口。
4. `tools/project_control` 和 `scripts/check_project_control.py` 负责检查 ID、状态、必填字段和文件引用。
5. 先保持手工更新和工具检查，不引入数据库、OAuth 或重型项目管理平台。

## TODO

| ID | 事项 | 负责人 | 状态 | 目标 |
| --- | --- | --- | --- | --- |
| PM-009 | 建立资产台账和能力台账 V1 | Codex | Done | M5 |
| PM-010 | 建立 Project Control 检查工具 | Codex | Done | M5 |
| PM-011 | 评估台账自动生成 Wiki 表格 | Team | Planned | M5 |

## 未决问题

- 台账后续是否由工具自动生成 Wiki 表格。
- 是否把 Cloudflare 发布链路也纳入能力台账检查。
- 是否需要为游戏内容资产建立更细的卡牌、敌人、事件分表。

## 后续同步

先用 V1 检查器维护结构健康。等台账条目增加后，再评估自动生成页面和健康分。
