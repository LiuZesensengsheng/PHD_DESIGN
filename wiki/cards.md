# 卡牌

- 状态: Active
- 负责人: Team
- 范围: 卡牌与运行时数据导航
- 权威性: No
- 最后复核: 2026-05-27

## 概览

卡牌是当前最接近经典爬塔 Wiki 的部分：可以按颜色、稀有度、类型、关键词和运行时数据来查。

当前已明确的主入口是红色和白色卡牌。绿色理想还在草案阶段，不应当被默认当成运行时承诺。

## 卡牌颜色

| 颜色 | 当前状态 | 设计入口 | 运行时数据 |
| --- | --- | --- | --- |
| 红色 | 已落地 / 活跃设计 | [RED_IDEAL_CARD_DESIGN_V2.md](../design/ideal/RED_IDEAL_CARD_DESIGN_V2.md) | `data/cards/red/` |
| 白色 | 已落地 / 活跃设计 | [WHITE_IDEAL_CARD_DESIGN_V3.md](../design/ideal/WHITE_IDEAL_CARD_DESIGN_V3.md) | `data/cards/white/` |
| 绿色 | 草案 | [GREEN_IDEAL_CARD_DESIGN_V1.md](../design/ideal/GREEN_IDEAL_CARD_DESIGN_V1.md) | 暂无默认运行时承诺 |

## 数据入口

| 文件 | 用途 |
| --- | --- |
| `data/cards/red/cards_red.csv` | 红色卡牌源表 |
| `data/cards/red/effects_red.csv` | 红色效果源表 |
| `data/cards/red/cards_generated.json` | 红色生成产物 |
| `data/cards/white/cards_white.csv` | 白色卡牌源表 |
| `data/cards/white/effects_white.csv` | 白色效果源表 |
| `data/cards/white/cards_generated.json` | 白色生成产物 |

## Wiki 读法

| 想知道 | 读哪里 |
| --- | --- |
| 卡牌设计意图 | `docs/design/ideal/` 下的 active spec |
| 卡牌当前是否存在 | `data/cards/<color>/cards_generated.json` |
| 卡牌如何从表格生成 | `scripts/cards_csv_to_json.py` |
| 卡牌数据契约是否安全 | `tests/scripts/test_cards_csv_to_json.py` 和 `tests/scripts/test_data_pipeline_contracts.py` |

## 当前关键词线索

| 线索 | 说明 |
| --- | --- |
| 红色前沿 / 批注 | 偏向主动推进、首张牌、节奏收益和小批注派生牌。 |
| 白色指针 / 排序 | 偏向敌人位置、端点、指针移动、审查和结构化控制。 |
| 自信 | 当前防御类数值语义之一，实际行为以运行时实现为准。 |
| 消耗 | 打出后离开本局战斗循环的卡牌标记，具体字段以数据和代码为准。 |

## 待补页面

后续可以把卡牌页继续拆成：

1. 红色卡牌列表。
2. 白色卡牌列表。
3. 关键词索引。
4. 单卡页面模板。
