# 🤖 AI工具链使用指南

> 自动生成时间: 2025-07-02 22:43:46
> 工具版本: v2.0 (重构版，遵循EEE方法论)
## 核心工具：合规暴君 v2.0 (manage_v2.py)
位置: `python scripts/manage_v2.py [命令]`

### 🚀 EEE架构升级亮点：
- **模块化设计**: 539行臃肿脚本重构为清晰包结构
- **常量外部化**: 所有魔法值移至constants.py，消除硬编码
- **自解释代码**: 提高AI协作效率，降低认知负担

### 核心命令（日常使用）：
1. **run** - 智能运行：自动检查 + 运行主程序 🔥MAIN
2. **setup** - 一键设置现代工具链 (Poetry + pre-commit)
3. **deps** - 检查项目依赖状况
4. **format-code** - 格式化代码 (black + isort)
5. **ai-guide** - 生成本指南

### 进阶命令（特殊需求）：
6. **check** - 手动运行合规检查 (lab/industrial/aerospace级别)
7. **lint** - 单独的代码质量检查
8. **clean-build** - 创建用于打包的干净构建
9. **deep-check** - 深度检查：工具链诊断专用 ⭐⭐⭐

### 项目状态快照：
✅ Poetry已安装
✅ pyproject.toml存在
✅ .pylintrc存在
✅ mypy.ini存在

### 极简工作流：
1. **首次设置**: `python scripts/manage_v2.py setup`
2. **日常开发**: `python scripts/manage_v2.py run` 🔥 智能检查+运行，一个命令搞定！

### 🎯 EEE方法论体现：
- **Protocol-Driven**: 清晰的接口定义 (constants.py)
- **Zero Magic Values**: 消除硬编码，提高可维护性
- **Plugin-based**: 模块化架构，易于扩展

---
📝 此指南由工具链自动生成 (v2.0 重构版)
🎯 遵循EEE原则：让"做正确的事"比"走捷径"更容易
