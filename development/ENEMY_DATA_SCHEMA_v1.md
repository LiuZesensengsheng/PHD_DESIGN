## 敌人数据 Schema 草案 v1（点名小队对接）

> 目标：定义“敌人JSON结构 + CSV列规范”，支持职业定位、简明被动、意图池（权重/冷却/条件）、台词（Barks），并尽量复用卡牌效果的轻量 Effect 形态以便统一查看与导出。该Schema面向策划与数据导出，非引擎最终实现接口。

---

## 1. JSON 结构（单个敌人）

必填字段：
- `id: string(UUIDv4)` 敌人主键。
- `slug: string` 人类可读代号（如 `rollcall_substitute`）。
- `name_zh: string` 中文名直写。
- `name_en: string` 英文名直写（可留空）。
- `color: "WHITE|BLUE|BLACK|RED|GREEN|COLORLESS"` 颜色身份（用于展示/掉落权重）。
- `role: "WARRIOR|MAGE|DEBUFFER|SUPPORT|TANK|CONTROLLER|BRUISER|SCALER"` 职业定位枚举（可多选以 `role_tags` 表达）。
- `max_hp: number` 生命上限（Act基线）。
- `passives: Passive[]` 被动列表（简明规则）。
- `intents: Intent[]` 意图池。

推荐字段：
- `role_tags?: string[]` 辅助标签（如 `{"priority_target"}`）。
- `barks_zh?: string[]` 战斗台词（中文）。
- `barks_en?: string[]` 战斗台词（英文）。
- `notes?: string` 设计备注/护栏。

### 1.1 Passive
```json
{
  "id": "passive_id",
  "name_zh": "课代表",
  "name_en": "Class Rep",
  "description_zh": "回合开始获得3点格挡。",
  "description_en": "At turn start, gain 3 Block.",
  "hook": "on_turn_start"  // 可选：提示触发窗口
}
```

### 1.2 Intent
```json
{
  "id": "intent_id",
  "name_zh": "普通攻击",
  "name_en": "Strike",
  "type": "Attack|Defend|Debuff|Power|Special",
  "weight": 40,                 // 抽取权重
  "cooldown": 0,                // 回合冷却
  "conditions": ["progress>=3"], // 文案条件（可空）
  "telegraph": false,           // 是否为“预告”意图
  "effects": [                  // 轻量效果列表（复用卡牌Effect子集）
    { "type": "damage", "value": 7 },
    { "type": "status", "status_type": "Vulnerable", "duration": 1, "target": "player" }
  ],
  "notes": "仅示例。"
}
```

说明：
- 为降低实现负担，Intent 的 `effects` 仅用于导出/校对；引擎侧可以用自有意图脚本或服务映射。
- 常用 Effect 子集：`damage`、`status(Vulnerable|Weak)`、`block`（若需要防御）、`power_flag`（仅作标记）。

---

## 2. CSV 列规范（用于Excel）

推荐列：
- 敌人主列：`id,slug,name_zh,name_en,color,role,role_tags,max_hp,passives_flat,barks_zh,notes`
- 意图行列：`intent_id,intent_name_zh,type,weight,cooldown,conditions,effects_flat,intent_notes`

扁平写法：
- `passives_flat`: `课代表:on_turn_start=block3|困倦:on_turn_start=skip25%`
- `effects_flat`: `damage(7)；status(Vulnerable,1->player)`（多效果用全角分号分隔）

---

## 3. 实现护栏（对齐本项目现状）
- 数据层先行：可以写入超出引擎现状的规则（如“溜号→高伤后离场”），在 `notes` 中写清口径，后续由程序挂接事件或临时替换。
- 单回合强意图避免连放：可用 `cooldown>=1` 表达，或在实现层加“最近使用记忆”。
- 逃离类：建议分两步意图（`溜号准备`/`溜号`），便于读招与打断。

---

## 4. 示例（简）
```json
{
  "id": "b7f2f1a0-02e1-4b2d-9b2e-9a99c8b10000",
  "slug": "rollcall_substitute",
  "name_zh": "代课学生",
  "name_en": "Substitute",
  "color": "BLUE",
  "role": "CONTROLLER",
  "role_tags": ["priority_target"],
  "max_hp": 80,
  "passives": [
    { "id": "signin_only", "name_zh": "只为签到", "description_zh": "点名回合开始：签到进度+1（至多3）。", "hook": "on_turn_start" }
  ],
  "intents": [
    { "id": "scan_qr", "name_zh": "扫码签到", "type": "Power", "weight": 40, "cooldown": 0,
      "effects": [{"type":"power_flag","value":"progress+1"}], "notes": "进度=3后转入溜号准备" },
    { "id": "photo_checkin", "name_zh": "合影打卡", "type": "Debuff", "weight": 25, "cooldown": 2,
      "effects": [{"type":"damage","value":5},{"type":"status","status_type":"Weak","duration":1,"target":"player"}] },
    { "id": "flee_prep", "name_zh": "溜号准备", "type": "Special", "weight": 100, "cooldown": 0, "telegraph": true,
      "conditions":["progress>=3"], "effects": [{"type":"power_flag","value":"flee_next"}], "notes":"下回合必溜号" },
    { "id": "flee", "name_zh": "溜号", "type": "Special", "weight": 100, "cooldown": 0,
      "conditions":["flee_next"], "effects": [{"type":"damage","value":30},{"type":"power_flag","value":"leave_battle"}],
      "notes": "当回合若被‘点名’命中则失败并进度-1" }
  ],
  "barks_zh": ["我就来扫个码。","二维码在哪？"],
  "notes": "示例：真实数值以策划调参为准。"
}
```
