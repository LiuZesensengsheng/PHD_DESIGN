# 《绝不延毕》项目文档

本项目采用EEE（Explanation-Embedded Engineering）方法论进行开发，文档按照清晰的四层架构组织：

## 📁 文档结构（新）

### 🎨 art/
UI 与美术设计
- `ART_STYLE_GUIDE.md` 美术风格指南
- `CARD_ART_GUIDE.md` 卡牌美术指南
- `MAIN_UI_STRUCTURE.md` UI 结构
- `VISual_CONCEPT_FOR_UI.md` UI 概念稿

### 🧭 design/
游戏策划总目录

- campaign/ 战役策划
  - `events/` 战役事件文档
  - `questline_tutorial/` 新手战役流程
  - `ACADEMIC_PRESTIGE_SYSTEM.md` 学术声望系统
  - `ACKNOWLEDGEMENTS_SYSTEM.md` 致谢系统
  - `JOURNAL_SYSTEM_DESIGN.md` 日志系统
  - `CAMPAIGN_SYSTEM_GANTT_CHART.md` 战役系统甘特

- combat/ 战斗策划与数值
  - `CARD_SYSTEM.md` 卡牌系统总览
  - `card_sets/` 卡组与卡池配置
  - `BOSS_FIGHT.md`/`BOSS_FIGHT_V2.md` Boss 设计
  - `ENEMY_DESIGN.md` 敌人设计
  - `COMBAT_SYSTEM_*` 战斗系统文档（含平衡表）
  - `DRAFT_ENEMIES_MEME.md` 敌人草案

- core/ 核心机制与特性
  - `CORE_MECHANICS.md` 核心循环与规则
  - `TRAITS_MASTER_LIST.md` 特性总表
  - `BASIC_TRAITS_DESIGN.md` 基础特性设计
  - `DND_STYLE_TRAIT_SYSTEM.md` DnD 风格特性
  - `TRAIT_SYSTEM_DESIGN.md` 特性系统设计

- characters/ 角色设定
  - 角色档案与卡面提示词等

- 顶层设计文档（位于 design 根目录）
  - `GAME_DESIGN_OVERVIEW.md` 游戏设计概览
  - `CORE_DESIGN_PHILOSOPHY.md` 设计哲学
  - `game_core_loop_and_innovation.md` 核心循环与创新
  - `GANTT_TRIS_MODEL_GDD.md` 规划与进度模型

### 🏗️ tech/
技术架构与实现规划
- `DATA_MODEL.md` 数据模型
- `TECHNICAL_CHOICE_RATIONALE.md` 技术选型理由
- `SCENARIO_FLOWS.md` 场景与流程
- `COMBAT_EVENTS_AND_SERVICES.md` 战斗事件与服务
- `CARD_VFX_PLAN.md` 卡牌特效规划

### 🧪 development/
开发方法论与协作规范
- `AI_COLLABORATION_PRINCIPLES.md`
- `AI_COLLABORATION_TOOLCHAIN.md`
- 其他开发流程与规范文档

### 📣 marketing/
宣传与对外材料
- `promo_video_script.md`/`promo_video_script_part2.md` 宣传视频脚本

### 🗄️ archive/
历史废案与归档材料（保留溯源，不默认展示）

## 🎯 阅读指南

### 新成员入门顺序
1. 先读 `development/AI_COLLABORATION_TOOLCHAIN.md` 了解工具链
2. 再读 `design/GAME_DESIGN_OVERVIEW.md` 与 `design/CORE_DESIGN_PHILOSOPHY.md`
3. 阅读 `tech/DATA_MODEL.md` 与相关技术说明
4. 根据分工进入 `design/campaign` 或 `design/combat`

### AI协作者快速上手
直接运行项目根目录的 `python scripts/manage.py ai-guide` 命令，获得实时的项目状态和工具链指南。

## 🔧 EEE方法论核心

本项目严格遵循EEE的三大支柱：
1. **Protocol-Driven**: 强制使用typing.Protocol定义接口
2. **Plugin-based Toolchain**: 以manage.py为核心的自动化工具
3. **Zero Magic Values**: 根除硬编码值，集中管理常量

目标是实现**调试周期计数(DCC) ≤ 10**，提高"首次提交正确率"。 