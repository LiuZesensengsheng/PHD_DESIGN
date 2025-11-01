## 卡牌数据 Schema 草案 v1.1（WHITE v2 对接 + UUID 与双语）

> 目标：定义“卡牌JSON结构 + CSV列规范”，满足白色v2（范式/坚定/规整/队列）最小可用数据需求，并与《CARD_KEYWORDS_GLOSSARY.md》一致；在工程层引入 UUID 主键与中英双语字段。

---

## 1. JSON 结构（单卡）

必填字段（卡级）：
- `id: string(UUIDv4)` 全局唯一主键（工程用）。
- `color: "WHITE|BLUE|BLACK|RED|GREEN|COLORLESS"` 颜色（理想色）。
- `type: "Attack|Skill|Power"` 卡牌类型。
- `rarity: "Common|Uncommon|Rare"` 品质。
- `cost: number` 费用（整数，≥0）。
- `effects: Effect[]` 按序结算的效果列表（见 2 章）。

推荐字段：
- `slug?: string` 人类可读的稳定代号（便于策划/调试，如 `white_axiomatic_system`）。
- `name_zh?: string` 中文名直写。
- `name_en?: string` 英文名直写。
- `description_zh?: string` 中文描述直写。
- `description_en?: string` 英文描述直写。

可选字段：
- `keywords?: string[]` 机制关键词（用于检索/护栏/UI提示）。
- `tags?: string[]` 主题/构筑标签（非机制）。
- `exhaust_on_play?: boolean` 消耗。
- `ethereal?: boolean` 虚无。
- `unplayable?: boolean` 无法打出。
- `symmetric?: boolean` 对称（多用于能力/范式）。
- `upgraded_id?: string(UUID)` 升级形态的UUID（指向“该卡的升级版”）。
- `is_upgraded?: boolean` 是否为“升级形态”的实体记录（默认省略/false；当该JSON本身即为升级形态时置为true）。
- 兼容旧版（可选保留，逐步废弃）：`name_key?`, `description_key?`, `upgraded_card_id?`。

命名与本地化策略：
- 运行期以 `name_zh/name_en/description_zh/description_en` 直显为主；若接入外部本地化，再使用 `name_key/description_key` 映射到资源表。
- `slug` 仅用于人类可读与资产映射，不作为主键；主键一律使用 `id(UUID)`。
- 建议约定：
  - 基础形态：`is_upgraded=false/省略`，并在自身包含 `upgraded_id` 指向升级形态。
  - 升级形态：`is_upgraded=true`；无需再包含 `upgraded_id`（避免链式）。

示例（片段）：
```json
{
  "id": "3a3f18b3-7b42-4b8b-9a40-9b2a3f4f3a2e",
  "slug": "white_axiomatic_system",
  "name_zh": "公理体系",
  "name_en": "Axiomatic System",
  "description_zh": "【范式】回合开始：所有单位获得2点自信。",
  "description_en": "Paradigm: At turn start, all units gain 2 Confidence.",
  "color": "WHITE",
  "type": "Power",
  "rarity": "Uncommon",
  "cost": 2,
  "keywords": ["Paradigm", "Symmetric"],
  "tags": [],
  "effects": [
    {
      "type": "add_paradigm",
      "paradigm_id": "axiomatic_system",
      "activation_window": "on_turn_start",
      "symmetric": true,
      "payload": [
        { "type": "confidence", "value": 2, "target": "all_units" }
      ],
      "stack_strategy": "keep_highest"
    }
  ]
}
```

---

## 2. Effect 定义（最小可用子集）

通用字段：
- `type: string` 效果类型（如下各小节）。
- `target?: string` 目标（枚举见 3 章）。
- 其他字段按类型定义。

2.1 伤害/自信/抽能
- `damage`：`{ type:"damage", value:number, hit_count?:number, target }`
- `confidence`：`{ type:"confidence", value:number, target:"player|ally|all_units" }`
- `draw`：`{ type:"draw", count:number, target:"player" }`
- `gain_energy` / `lose_energy`：`{ type:"gain_energy"|"lose_energy", value:number }`

2.2 状态
- 通用：`{ type:"status", status_type:"Vulnerable|Weak|Regulated|...", duration?:number, value?:number, target }`
- 规整（推荐以“本回合+X”直赋）：`{ type:"status", status_type:"Regulated", value:number, target }`
- 语义与结算顺序详见《[STATUS_EFFECTS_V1.md](./STATUS_EFFECTS_V1.md)》。

2.3 严谨度
- 永久/回合内：`{ type:"rigor"|"temporary_rigor", value:number, target:"player" }`

2.4 位置与序列
- 位置：`{ type:"reposition", op:"swap_with_right|move_to_leftmost|move_to_rightmost|move_to_middle", target:"selected_enemy" }`
- 序列伤害：`{ type:"sequence_damage", base:number, step:number, target:"left_to_right|right_to_left", view_only?:boolean }`

2.5 范式（Paradigm）
- 添加范式：
```json
{
  "type": "add_paradigm",
  "paradigm_id": "string",
  "activation_window": "on_turn_start",
  "symmetric": false,
  "payload": [ /* Effect[] 在触发窗口执行 */ ],
  "stack_strategy": "keep_highest",
  "soft_caps": { /* 可选：同类合计上限，如 "turn_start_gain_confidence": 5 */ }
}
```

2.6 坚定（Steadfast）
2.7 指针（Pointer）
- 关键词：`Pointer`（带此关键词的白色卡触发指针 Bootstrap）
- 原语：
  - `pointer_bootstrap`: `{ type:"pointer_bootstrap" }`（若无指针则建立：最左，PD=2，per_turn_limit=5，dir=right）
  - `pointer_pd_add`: `{ type:"pointer_pd_add", value:number, duration?:"this_turn|permanent" }`
  - `pointer_step`: `{ type:"pointer_step", value:1, dir?:"auto|left|right" }`
  - `pointer_warp`: `{ type:"pointer_warp", to:"leftmost|rightmost|middle|lowest" }`
  - `pointer_limit_add`: `{ type:"pointer_limit_add", value:number, duration?:"this_turn|permanent" }`
  - `lock_queue`: `{ type:"lock_queue", duration:number }`

示例（片段）：
```
pointer_bootstrap(); pointer_warp(to=middle); pointer_pd_add(value=1|duration=this_turn)
```
- 装填标记：
```json
{
  "type": "add_steadfast_token",
  "token_type": "STEADFAST_ENERGY|STEADFAST_DRAW|STEADFAST_WITTY_STRIKE",
  "value": 1
}
```
- 系统语义（引擎实现）：坚定可跨回合保存；在 `on_perfect_block` 消耗1层并结算。

---

## 3. 目标枚举（targets）
- 单位侧：`player`（我方角色）、`ally`（友军）、`selected_enemy`、`random_enemy`、`all_enemies`、`leftmost_enemy`、`rightmost_enemy`、`all_units`（敌我全体）。
- 序列方向：`left_to_right` / `right_to_left`（用于序列类效果的目标扫描）。

---

## 4. 护栏与规则（数据侧可表述）
- 频次：`per_turn_limit` / `per_unit_per_turn_limit`（置于Power/范式的效果对象内，供引擎读取）。
- 并存：同名范式 `stack_strategy` 默认 `keep_highest`；同类效果合计上限使用 `soft_caps`。
- 0费护栏：引擎侧统一控制，数据可通过 `keywords: ["PerTurnLimit:N"]` 做读招提示。
- 规整：追加伤害为“纯伤”，不参与易伤/力量乘算；多段逐段触发；当回合 `k` 递增，回合结束清零；`L` 在回合开始衰减。
- 坚定：可跨回合保存，`on_perfect_block` 每次触发消耗1层；未触发不清空。

---

## 5. CSV 列规范（用于Excel）

推荐列：
- `id`（UUID）
- `slug`
- `name_zh`
- `name_en`
- `description_zh`
- `description_en`
- `color`
- `type`
- `cost`
- `rarity`
- `is_upgraded`（true/false）
- `upgraded_id`（UUID；基础形态才会填写）
- `keywords`（以 `|` 分隔）
- `tags`（以 `|` 分隔）
- `effects_flat`（扁平化效果字符串，见下）
- `notes`（可选）

`effects_flat` 书写规范：
- 例1（范式：回合开始我与敌人各+2自信）：
  - `add_paradigm(paradigm_id=axiomatic_system|window=on_turn_start|symmetric=true|payload=confidence:2->all_units)`
- 例2（装填坚定：+1能量）：
  - `steadfast(token=ENERGY|value=1)`
- 例3（规整：本回合对目标+1）：
  - `status(type=Regulated|value=1->selected_enemy)`

注意：CSV为设计/校对用视图，落地仍以JSON为准。

---
