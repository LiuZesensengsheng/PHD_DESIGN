## 美德（Judgment）演出与脚本设计（v1）

### 目标
- 以低成本但高可读的方式，呈现“压力突破阈值→理想判定→结果（美德/裂痕/粉碎）”的剧情与反馈。
- 可数据驱动、可扩展（不同理想、不同难度、不同台词/特效），并与现有事件系统无缝对接。

### 触发与终止规则
- 压力条总上限为200，但视觉条长度固定为100。
  - 0–100：彩色填充。
  - 100–200：在同一条上，从左侧叠加“黑色覆盖”显示溢出（200时全黑）。
- 触发时机（每战一次）：当压力从<100跨到≥100时，触发一次“美德表演”。
- 终止：当压力≥200时，玩家立刻死亡，战斗结束（Game Over）。

### 事件流（Domain/Event）
1) 玩家承伤 → 压力增长。
2) 当压力第一次达到≥100：发布 `StressThresholdReached(player_id, value)`。
3) Model 监听后调用 `JudgmentService`：
   - `compute_target_ideal(ideals)` 选取受检理想（按 lifetime/window 计数）
   - `compute_effective(...)` 计算有效权重
   - `decide_verdict(effective, crack_stacks)` 判定结果（美德/裂痕/粉碎）
   - `apply_verdict(player, color, verdict)` 应用效果（见下）
4) 发布 `JudgmentResolved(player_id, target_color, verdict)`，供 View 层演出。

### 应用效果（服务端逻辑）
- 美德（virtue）：
  - 清空该色 window_count；
  - 减压：`JUDGMENT_RELIEF_VIRTUE`（例如 15–25，可调）。
- 裂痕（crack）：
  - 该色 crack_stacks +1；
  - 清空该色 window_count。
- 粉碎（shatter）：
  - 从 active_colors 移除该理想色；
  - 清空该色所有计数（window/lifetime/crack）。

### 演出（View 层，建议总时长 ~3.0s，非阻塞或短暂停顿）
阶段 A（~0.8s）
- 顶部居中提示条淡入：“你的理想正在经受考验……”
- 压力条做轻微白闪/脉冲。

阶段 B（~1.5s）
- 中央小面板展示：理想图标 + 判定结果标签。
- 结果特效建议：
  - 美德：金色光效（粒子/放射），舒缓钟声；压力条白闪后回落（与服务端减压同步）。
  - 裂痕：紫色裂纹遮罩短闪，轻度震动/玻璃擦音；叠层 HUD 显示“裂痕+1”。
  - 粉碎：图标破碎粒子飞散，彩色褪去，玻璃破碎音；提示“理想粉碎”。

阶段 C（~0.5s）
- 台词二段式显示（见台词规范）；面板淡出，恢复交互。

### 台词规范（数据驱动）
- 结构：分为三个层级以便覆盖：
  1) 通用（default）
  2) 按理想色（white/blue/black/red/green）
  3) 按结果（virtue/crack/shatter）
- 每条支持多候选，运行时随机抽取。

示例 JSON（建议文件：`docs/event/virtue_dialogue.json`）
```json
{
  "default": {
    "prelude": ["你的理想正在经受考验……", "心之所向，正被拷问。"],
    "virtue": ["你坚守了初心。", "你没有背弃自己。"],
    "crack": ["你的信念出现了裂痕。", "这一次，你犹豫了。"],
    "shatter": ["你的某种理想粉碎了。", "你不再是刚才的你。"]
  },
  "white": {
    "prelude": ["秩序的信条，正在审视你。"],
    "virtue": ["你维护了秩序。"],
    "crack": ["秩序的边界开始松动。"],
    "shatter": ["秩序不再是你的答案。"]
  }
}
```

View 侧使用方式：
- 收到 `JudgmentResolved(target_color, verdict)` 后：
  - 先取 color 的 `prelude` 随机显示一条；
  - 再取 color 的 `verdict` 列表随机显示一条；
  - 若 color 缺省，退回 default；若 default 也缺省，退回固定保底文案。

### UI 组件（建议）
- 顶部提示条（PrequelToast）：
  - 属性：`text`, `duration_ms`, `fade_in_ms`, `fade_out_ms`。
  - 默认：`duration=800`, `fade=150/150`。
- 中央判定面板（JudgmentBanner）：
  - 属性：`icon_by_color`, `verdict_badge`, `sfx_key`, `vfx_key`。
  - 默认时长：1500ms。
- 压力条动画：
  - `pulse()`/`flash_white()`；
  - `animate_reduce(to_value, duration_ms)` 与服务端减压同步。

### 可配置参数（constants/combat_domain.py 建议）
- `STRESS_JUDGMENT_THRESHOLD = 100`
- `JUDGMENT_RELIEF_VIRTUE = 20`（示例）
- `JUDGMENT_LIFETIME_STEP`、`JUDGMENT_RANDOM_ENABLED`、`JUDGMENT_NEIGHBORHOOD_DELTA`、`JUDGMENT_NOISE_EPS`

### 开发任务清单（落地顺序建议）
1) 事件对接：确保 `StressThresholdReached` → `JudgmentService` → `JudgmentResolved` 流程只触发一次（用状态标记）。
2) UI：实现 PrequelToast 与 JudgmentBanner 两个轻量组件（或用现有文本/图片叠层模拟）。
3) 压力条动画接口：`pulse/flash/animate_reduce`。
4) 台词 JSON 加载器与选择逻辑（颜色→结果→随机选）。
5) 音效/特效映射（结果→sfx/vfx key）。
6) 可测试性：
   - 单元：输入 `window_count/lifetime/crack_stacks`，断言 `decide_verdict/apply_verdict`。
   - 端到端（headless）：模拟承伤→发事件→验证只触发一次与减压结果。

### 备注
- 后续可在“美德”时附加阵营专属奖励（如白色：获得“坚定+1”），但首版建议只做视觉与核心数值改动，避免牵连过多系统。


