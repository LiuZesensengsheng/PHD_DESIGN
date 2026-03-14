# 项目文档总览

本目录存放项目设计、技术、协作与记忆文档。

## 目录分层

### `development/`

- 长期架构规则
- AI 协作约定
- 项目记忆入口
- 默认工具入口

### `design/`

- 战役、战斗、角色与核心机制设计

### `tech/`

- 数据模型
- 技术选型
- 关键实现规划

### `art/`

- UI 与美术相关说明

### `marketing/`

- 对外展示与宣传材料

### `archive/`

- 历史文档与归档材料

## 推荐阅读顺序

### 新成员

1. 先读根目录 `AGENTS.md`
2. 再读 `docs/development/CURRENT_DIRECTION.md`
3. 如需执行工具或维护任务，读 `docs/development/DEFAULT_ENTRYPOINTS.md`
4. 然后按任务进入相关 `design/`、`tech/`、`development/` 文档

### AI 协作恢复

请按以下入口恢复当前状态，不要依赖已移除的旧聚合脚本：

1. `AGENTS.md`
2. `docs/development/CURRENT_DIRECTION.md`
3. `docs/development/DEFAULT_ENTRYPOINTS.md`
4. 当天 daily log
5. 最近一份有内容的 weekly summary

## EEE 方法当前理解

本项目曾使用 EEE（Explanation-Embedded Engineering）作为协作方法表达。
当前仍保留的有效核心是：

1. `Protocol-Driven`
2. `Documented Toolchain`
3. `Zero Magic Values`

其中工具链部分已经从旧的聚合入口，收敛为“文档入口 + 直接脚本/pytest 命令”。
