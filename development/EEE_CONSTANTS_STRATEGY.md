# EEE 常数组织策略 (长期记忆)

## 📋 **最终确定的混合策略**

经过实际项目验证，我们采用**混合常数组织策略**：

### ✅ **保留在领域对象中的**
- **枚举和类型定义** (业务概念)
- **领域状态常量** (与业务逻辑紧密相关)

```python
# ✅ 正确位置：contexts/combat/domain/card.py
class Rarity(Enum):
    BASIC = "Basic"
    COMMON = "Common"
    RARE = "Rare"

class CardType(Enum):
    ATTACK = "Attack"
    SKILL = "Skill"
```

### ✅ **移到constants包的**
- **UI实现细节** (引擎特定名称)
- **配置参数** (可能需要调整的值)
- **格式化模板** (显示相关)

```python
# ✅ 正确位置：constants/combat_ui.py
CARD_MAKER_NAME: str = "card_maker"
MOUSE_RAY_NAME: str = "mouseRay"
HP_TEXT_FORMAT: str = "HP: {}"
```

### 🟡 **可以容忍的魔法值**
- **日志消息** (维护成本 > 收益)
- **临时调试字符串**
- **一次性使用的简单字符串**

```python
# 🟡 可接受：contexts/combat_logger.py
logger.info(f"玩家使用卡牌: {card_name}")  # 可接受的魔法值
```

## 🎯 **决策原则**

1. **业务价值优先** - 影响用户体验的常数优先整理
2. **维护成本考虑** - 避免过度工程化
3. **AI coding适配** - 保持代码对AI友好的结构

## 📊 **成本效益分析**

| 常数类型 | 整理收益 | 维护成本 | 建议 |
|----------|----------|----------|------|
| UI配置 | 高 | 低 | ✅ 整理 |
| 业务枚举 | 高 | 低 | ✅ 保持现状 |
| 日志字符串 | 低 | 高 | 🟡 容忍 |

---
*更新日期: 2025-07-05*
*状态: 已验证并采纳* 