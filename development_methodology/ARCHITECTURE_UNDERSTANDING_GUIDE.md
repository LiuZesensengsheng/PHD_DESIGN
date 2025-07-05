# 《绝不延毕》架构理解指南

## 🎯 **目标：重新掌控代码架构**

这份指南将帮助您在1-2天内重新理解整个代码架构，减少对AI的依赖，为后续经济开发打基础。

## 📋 **核心系统地图**

### **系统全景图**
```
《绝不延毕》
├── 🎮 主游戏循环 (main.py)
├── 🗺️ 战役系统 (contexts/campaign/)
├── ⚔️ 战斗系统 (contexts/combat/)  
├── 🎨 渲染引擎 (robust_game_toolkit/)
├── 📊 常量系统 (constants/)
└── 🔧 工具链 (scripts/, tools/)
```

## 🔍 **重点理解路径**

### **第1步：主游戏循环理解 (30分钟)**

**阅读顺序**：
1. `main.py` - 游戏入口点
2. `shared_kernel/asset_keys.py` - 核心资源定义
3. `constants/__init__.py` - 核心常量

**关键问题**：
- [ ] 游戏如何启动？
- [ ] 不同Context之间如何切换？
- [ ] 资源管理机制是什么？

### **第2步：战役系统深入 (90分钟)**

**核心文件导读**：
```
contexts/campaign/
├── domain/           # 🏛️ 业务核心
│   ├── campaign_map.py    # 战役地图
│   ├── track.py           # 进度轨道  
│   ├── node.py            # 节点定义
│   └── event.py           # 事件系统
├── application/      # 🎯 用例层
│   └── campaign_service.py   # 战役服务
├── infrastructure/   # 💾 数据层
│   └── json_event_repository.py
└── presentation/     # 🎨 展示层
    └── (UI相关)
```

**理解检查清单**：
- [ ] `CampaignMap`如何管理轨道？
- [ ] `Node`的执行机制是什么？
- [ ] 事件系统如何工作？
- [ ] 战役如何触发战斗？

### **第3步：战斗系统解析 (90分钟)**

**核心文件导读**：
```
contexts/combat/
├── domain/           # ⚔️ 战斗核心
│   ├── card.py            # 卡牌定义
│   ├── combat_state.py    # 战斗状态
│   └── buff_system.py     # Buff系统
├── managers/         # 🎮 管理器
│   ├── combat_manager.py  # 战斗管理
│   └── hand_manager.py    # 手牌管理
└── presentation/     # 🎨 战斗UI
    ├── card_renderer.py   # 卡牌渲染
    └── constants.py       # UI常量
```

**理解检查清单**：
- [ ] 战斗状态如何管理？
- [ ] 卡牌系统如何工作？
- [ ] Buff系统如何实现？
- [ ] 战斗结果如何返回战役？

### **第4步：系统集成点 (60分钟)**

**关键集成文件**：
1. `contexts/campaign/context.py` - 战役上下文
2. `contexts/combat/context.py` - 战斗上下文  
3. `main.py` - 上下文切换逻辑

**集成理解检查**：
- [ ] 战役如何启动战斗？
- [ ] 战斗结果如何影响战役？
- [ ] 数据如何在系统间传递？

## 🛠️ **理解工具**

### **架构可视化**
```bash
# 生成系统依赖图
python scripts/validate_architecture.py

# 检查模块关系
python scripts/quality_guard.py
```

### **代码追踪技巧**
1. **从用例出发**：选择一个具体功能，追踪完整流程
2. **接口优先**：先理解Protocol和抽象类
3. **数据流向**：关注DTO和领域对象的转换

## 📝 **理解成果验收**

完成上述学习后，您应该能够：
- [ ] 画出战役-战斗系统交互图
- [ ] 解释任意一个功能的完整实现路径
- [ ] 识别系统的扩展点和修改点
- [ ] 预估新功能的开发复杂度

## 🎯 **下一步规划**

### **成本优化策略**
1. **80/20原则**：80%用免费工具，20%用Claude-4
2. **混合开发**：简单重复用GPT-4，复杂逻辑用Claude-4
3. **模板化**：建立常用代码模板，减少AI依赖

### **开发效率提升**
1. **预设计**：功能开发前先设计，减少AI试错
2. **渐进式**：小步快跑，每次只用AI解决一个小问题
3. **验证驱动**：用测试驱动开发，减少调试时间

---

**记住**：理解架构不是为了替代AI，而是为了更好地**指挥AI**！

当您理解架构后，您将从"AI用户"升级为"AI架构师" 🎯 