# 卡牌数据工作流

本文档详细说明了本项目中用于管理和生成卡牌数据的自动化工作流。遵循此流程可以确保数据的一致性、易于管理，并最大程度地减少手动操作引入的错误。

## 核心理念：单一数据源 (Single Source of Truth)

我们所有的卡牌设计，包括卡牌ID、名称、描述、效果、稀有度等，都统一存储在项目根目录下的 `data/cards_master.csv` 文件中。

**这是我们项目中关于卡牌设计的唯一“圣经”。**

**绝对不要**手动修改位于 `data/cards/theorist/` 目录下的任何JSON文件。这些文件是由脚本自动生成的，任何手动修改都会在下次运行脚本时被覆盖。

## 工作流步骤

### 1. 设计与修改：编辑 `cards_master.csv`

当你想进行任何卡牌相关的设计或修改（例如，调整一张卡的费用，修改一个效果的数值，或者设计一张全新的卡），请使用表格编辑软件（如 Microsoft Excel, Google Sheets, LibreOffice Calc, 或者 VS Code的Excel插件）打开 `data/cards_master.csv` 文件。

文件中的每一行代表一张**基础版**卡牌，其升级版信息也包含在同一行内。

**关键列说明：**
- `character`: 角色名称 (例如, `theorist`)。
- `card_id`: 卡牌的唯一英文ID，**非常重要**，不能重复。
- `name`: 卡牌的中文名称。
- `cost`: 基础版费用。
- `type`: 卡牌类型 (`Attack`, `Skill`, `Power`)。
- `rarity`: 稀有度 (`Common`, `Uncommon`, `Rare`, `Special`)。
- `description`: 基础版效果描述文本。
- `effect[1-3]_type`: 效果1-3的类型 (例如, `damage`, `confidence`, `draw`)。
- `effect[1-3]_value`: 效果1-3的数值。
- `effect[1-3]_target`: 效果1-3的目标 (例如, `player`, `selected_enemy`, `all_enemies`)。
- `script_id`: 对于无法用通用效果描述的复杂逻辑，在此处填写其在代码中对应的脚本ID。
- `upgraded_cost`: **升级版**的费用。
- `upgraded_description`: **升级版**的效果描述文本。
- `upgraded_effect[1-3]_value`: **升级版**的效果1-3的数值。

### 2. 生成游戏数据：运行 `generate-cards` 命令

在你修改并保存了 `cards_master.csv` 文件后，你需要将这些改动应用到游戏中。

打开终端，进入项目根目录，然后运行以下命令：

```bash
python scripts/manage.py generate-cards
```

这个命令会：
1. 读取 `data/cards_master.csv` 文件。
2. 验证数据的基本格式。
3. 为每个角色（目前只有`theorist`）在 `data/cards/` 目录下生成对应的分片JSON文件（`common.json`, `uncommon.json` 等）。

游戏会从这些生成的JSON文件中加载卡牌数据。

### 3. (未来) 验证设计：运行 `test` 命令

为了确保你的设计在代码层面是有效的（例如，`effect_type`是代码认识的类型，数值在合理范围内），我们将开发一个测试命令。

运行方式（暂未实现）：
```bash
python scripts/manage.py test-cards
```

这个命令会加载CSV，并用一系列的规则去检查每一行数据，提前发现潜在的逻辑错误，避免你进入游戏后才发现问题。

## 总结

**日常工作流**:
1.  **想改卡？** -> 打开 `data/cards_master.csv`。
2.  **改完了？** -> 保存CSV文件。
3.  **想让游戏生效？** -> 运行 `python scripts/manage.py generate-cards`。
4.  **想启动游戏测试？** -> 运行 `python run_quick_combat.py`。

这个流程将是未来所有卡牌工作的核心。
