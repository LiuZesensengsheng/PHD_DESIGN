# 敌人设计总览（Enemies Design Index）

目录结构：
- `TEMPLATE_ENEMY_PROTO.md`：原型模板（字段/意图/数值带）
- `INTENTS_CATALOG.md`：意图目录（图标/效果/冷却/权重）
- `ACT1_ROSTER.md`：Act 1 阵容纲要（8普+2精英+1Boss）
- `WHITE_Order.md`：白色（秩序/防御/组织）
- `BLUE_Knowledge.md`：蓝色（抽控/预判/信息）
- `BLACK_Ambition.md`：黑色（代价/虹吸/压迫）
- `RED_Impact.md`：红色（爆发/多段/推进）
- `GREEN_Growth.md`：绿色（增殖/再生/拖延）

写作规范：
- 敌人以“颜色身份”为主文件，具体个体在对应颜色文档中分条描述；跨色变体在该色文档内以“Variant”标注。
- 数值采用“带”（Band）表达，便于调参：例如 HP 28–34、伤害 5–7。
- 意图条目包含：图标、效果、数值带、冷却（回合）、权重（0–1）、条件触发。
- 与理想/心魔挂钩以“Hook”标注：引诱/污染/审判助推等。

> 若需添加新的颜色或特殊机制，请先在此处登记，再扩展相应文档。
