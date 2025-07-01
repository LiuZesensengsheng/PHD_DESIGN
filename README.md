# 《绝不延毕》项目文档

本项目采用EEE（Explanation-Embedded Engineering）方法论进行开发，文档按照清晰的四层架构组织：

## 📁 文档结构

### 🛠️ development_methodology/
开发方法论和AI协作相关文档
- `AI_COLLABORATION_PRINCIPLES.md` - AI协作的核心原则
- `AI_COLLABORATION_TOOLCHAIN.md` - 自解释工具链设计
- `DSEDD_CRITIQUE.md` - DSEDD方法论评论

### 🎮 game_design/
游戏设计理念和核心机制
- `GAME_DESIGN_DOCUMENT.md` - 游戏设计文档
- `GAME_DESIGN_OVERVIEW.md` - 游戏设计概览
- `game_core_loop_and_innovation.md` - 游戏核心循环和创新点
- `GAME_NAME` - 游戏命名方案

### 🏗️ technical_architecture/
技术架构和系统设计
- `ROBUST_GAME_TOOLKIT_ARCHITECTURE.md` - 游戏工具包架构
- `SYSTEM_IMPLEMENTATION_PLAN.md` - 系统实现计划
- `TECHNICAL_CHOICE_RATIONALE.md` - 技术选型理由

### 📋 project_management/
项目管理和策略规划
- `STRATEGY_BLUEPRINT.md` - 策略蓝图
- `PROJECT_PLAN_MVP.md` - MVP项目计划

## 📚 其他文档目录

### core_mechanics/
核心游戏机制设计
- 学术声望系统、致谢系统、战斗系统等

### content_design/
内容设计和角色设计
- 卡牌系统、敌人设计、事件设计等

### ui_and_art/
UI和美术设计
- 美术风格指南、卡牌美术指南、UI结构等

### devlogs/
开发日志
- 记录开发过程中的重要决策和技术突破

## 🎯 阅读指南

### 新成员入门顺序
1. **先读** `development_methodology/AI_COLLABORATION_TOOLCHAIN.md` - 了解工具链
2. **然后** `game_design/GAME_DESIGN_OVERVIEW.md` - 理解游戏理念
3. **接着** `technical_architecture/SYSTEM_IMPLEMENTATION_PLAN.md` - 掌握技术架构
4. **最后** `project_management/PROJECT_PLAN_MVP.md` - 了解项目规划

### AI协作者快速上手
直接运行项目根目录的 `python scripts/manage.py ai-guide` 命令，获得实时的项目状态和工具链指南。

## 🔧 EEE方法论核心

本项目严格遵循EEE的三大支柱：
1. **Protocol-Driven**: 强制使用typing.Protocol定义接口
2. **Plugin-based Toolchain**: 以manage.py为核心的自动化工具
3. **Zero Magic Values**: 根除硬编码值，集中管理常量

目标是实现**调试周期计数(DCC) ≤ 10**，提高"首次提交正确率"。 