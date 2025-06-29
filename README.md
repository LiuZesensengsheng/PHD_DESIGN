# 游戏设计文档总览

本文档是"博士模拟器"所有设计文档的入口点，旨在帮助开发人员快速定位相关信息，避免在海量文档中迷失。

## 1. 顶层设计与愿景 (Top-Level Design & Vision)

此部分包含项目的宏观定义、目标和战略规划。

- **[游戏核心循环与创新](./0_vision_and_strategy/game_core_loop_and_innovation.md)**: 描述游戏的核心玩法循环和创新点。
- **[游戏设计文档 (GDD)](./0_vision_and_strategy/GAME_DESIGN_DOCUMENT.md)**: 完整、详细的游戏设计文档。
- **[游戏设计总览](./0_vision_and_strategy/GAME_DESIGN_OVERVIEW.md)**: GDD的高度概括版本。
- **[项目计划：MVP](./0_vision_and_strategy/PROJECT_PLAN_MVP.md)**: 最小可行性产品的开发计划。
- **[稳健游戏工具包架构](./0_vision_and_strategy/ROBUST_GAME_TOOLKIT_ARCHITECTURE.md)**: 关于我们正在构建的可复用工具包的架构设计。
- **[技术选型基本原理](./0_vision_and_strategy/TECHNICAL_CHOICE_RATIONALE.md)**: 解释为什么我们选择当前的技术栈（Panda3D, DDD等）。

## 2. 核心机制 (Core Mechanics)

此部分详细说明了游戏中的关键系统和玩法。

- **[学术声望系统](./1_core_mechanics/ACADEMIC_PRESTIGE_SYSTEM.md)**: 玩家如何获得和失去声望。
- **[致谢系统](./1_core_mechanics/ACKNOWLEDGEMENTS_SYSTEM.md)**: 游戏中的社交和关系网络。
- **[战斗系统](./1_core_mechanics/BATTLE_SYSTEM.md)**: 核心战斗循环、卡牌效果等。
- **[战役系统UI设计](./1_core_mechanics/CAMPAIGN_SYSTEM_UI_DESIGN.md)**: 战役地图的界面和用户体验设计。
- **[核心机制总览](./1_core_mechanics/CORE_MECHANICS.md)**: 对所有核心机制的简要概述。
- **[日志系统设计](./1_core_mechanics/JOURNAL_SYSTEM_DESIGN.md)**: 游戏中的任务和叙事记录系统。

## 3. 内容设计 (Content Design)

此部分包含所有具体游戏内容的设计，如卡牌、敌人、事件等。

### 3.1 卡牌与战斗 (Cards & Combat)
- **[卡牌系统](./2_content_design/CARD_SYSTEM.md)**: 卡牌的设计理念、类型和模板。
- **[审稿回复卡牌设计](./2_content_design/REVIEW_RESPONSE_CARD_DESIGN.md)**: 针对"审稿"这一核心玩法的特殊卡牌。
- **[论文作为牌组设计](./2_content_design/thesis_as_deck_design.md)**: 如何将玩家的研究论文具象化为卡牌牌组。
- **[敌人设计](./2_content_design/ENEMY_DESIGN.md)**: 各种敌人的机制和特点。
- **[Boss战设计](./2_content_design/BOSS_FIGHT.md)**: Boss战的详细设计文档。
- **[Boss战设计V2](../BOSS_FIGHT_V2.md)**: Boss战设计的第二个版本。
- **[草稿：敌人(梗)](./2_content_design/DRAFT_ENEMIES_MEME.md)**: 基于学术圈"梗"的敌人设计草案。

### 3.2 角色 (Characters)
- **[范式：实验主义者](./2_content_design/characters/PARADIGM_EXPERIMENTALIST.md)**
- **[范式：理论家](./2_content_design/characters/PARADIGM_THEORIST.md)**
- **[社会科学家设计](./2_content_design/characters/social_scientist_design.md)**

### 3.3 事件 (Events)
- **[草稿：通用事件](./2_content_design/events/DRAFT_EVENTS_COMMON.md)**
- **[草稿：事件(梗)](./2_content_design/events/DRAFT_EVENTS_MEME.md)**

## 4. 美术与UI (Art & UI)

- **[美术风格指南](./3_ui_and_art/ART_STYLE_GUIDE.md)**: 游戏的整体视觉风格。
- **[卡牌美术指南](./3_ui_and_art/CARD_ART_GUIDE.md)**: 卡牌的具体美术规范。
- **[主UI结构](./3_ui_and_art/MAIN_UI_STRUCTURE.md)**: 游戏主界面的布局和结构。
- **[UI视觉概念](./3_ui_and_art/VISual_CONCEPT_FOR_UI.md)**: UI的视觉设计草图和概念。
- **[UI视觉概念(根目录)](../VISual_CONCEPT_FOR_UI.md)**: (与上方文件内容可能重复)

## 5. 开发日志与计划 (Devlogs & Plans)

- **[开发日志 2024-06-24: 战役系统](../DEVLOG_2024-06-24_Campaign_System.md)**
- **[开发日志 2025-06-28: Panda3D UI集成](./devlogs/2025-06-28_Panda3D_UI_Integration.md)**
- **[重构计划：时间线UI](../REFACTOR_PLAN_TIMELINE_UI.md)**
- **[公告1](../ANNOUNCEMENT_1.md)** 