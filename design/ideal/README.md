# 理想卡牌设计入口

- Status: Active
- Owner: Team
- Scope: ideal/card-design
- Canonical: Yes, as a directory index
- Supersedes: none
- Superseded By: none
- Implemented In: `data/cards/red/`, `data/cards/white/`
- Last Reviewed: 2026-05-17

## 默认读取顺序

1. 先读 `../DESIGN_NORTH_STAR_V1.md`
2. 红色实现或扩展先读 `RED_IDEAL_CARD_DESIGN_V2.md`
3. 白色实现或扩展先读 `WHITE_IDEAL_CARD_DESIGN_V3.md`
4. 绿色仍读 `GREEN_IDEAL_CARD_DESIGN_V1.md`，但它是 draft，不是当前 runtime 承诺
5. 需要历史语义、命名或矩阵时，再读旧版本和 CSV reference

## 当前状态

| 文档 | 状态 | Canonical | 用途 |
| --- | --- | --- | --- |
| `RED_IDEAL_CARD_DESIGN_V2.md` | Active | Yes, for red ideal cards | 红色前沿/小批注/混色轴的当前设计依据。 |
| `WHITE_IDEAL_CARD_DESIGN_V3.md` | Active | Yes, for white ideal cards | 白色指针/排序轴和 v4 已实现卡组的当前设计依据。 |
| `GREEN_IDEAL_CARD_DESIGN_V1.md` | Draft | No | 绿色厚积方向草案，未作为当前 runtime 承诺。 |
| `../archive/ideal/RED_IDEAL_CARD_DESIGN_V1.md` | Archived | No | 红色语义历史版本，被 v2 收口。 |
| `../archive/ideal/WHITE_IDEAL_CARD_DESIGN_V1.md` / `../archive/ideal/WHITE_IDEAL_CARD_DESIGN_V2.md` | Archived | No | 白色早期方向，被 v3/v4 实装口径收口。 |
| `RED_CARD_SLOT_MATRIX_V0*.csv` / `red_cards_revised.csv` | Reference | No | 规划表和工作表，不能自动覆盖 active spec。 |
| `SHARED_SEED_TEMPLATES_V0.md` | Reference | No | 可复用 seed 模板。 |
| `RED_TEMPTATION_AND_NEAREST_PLAYSTYLE_NOTES_V0.md` | Reference | No | 红色近似玩法和体验备忘。 |

## Source Of Truth

- 设计意图以 active spec 为准。
- 已落地行为以 `data/cards/red/`, `data/cards/white/`, 生成后的 runtime JSON、代码和测试为准。
- 如果 active spec 与 runtime 数据冲突，不要静默混用；先记录差异，再决定是更新设计文档还是调整实现。

## 下一次治理建议

- 判断绿色是否进入 active 设计，或继续保留为 draft。
- 把 CSV 工作表中真正权威的列写回 active spec，避免表格暗中成为第二套 source of truth。
