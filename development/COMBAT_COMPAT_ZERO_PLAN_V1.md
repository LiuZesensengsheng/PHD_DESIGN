# Combat Compat-Zero Plan V1

## 摘要
- 目标：把战斗 runtime 从“thin compat shell”推进到“语义兼容清零”，让所有新内容只见到 window-native / event-native / queue-native 主线。
- 现状：时序/事件主线已落地，但 Player public wrapper、trait/power legacy hook、Enemy passive `hook` 输入、EffectExecutor 旧方法名仍在；这些接口继续存在会让 300+ 卡牌、100+ 特质、复杂敌人拓展难以维持一致语义。
- 原则：仅处理“combat 语义兼容层”，暂不触及 UI alias、save 迁移、view helper 之类的外围兼容点；保持 phase machine、action queue 既有架构不重写。

## Scope 边界
- **包含**：Player 公开 compat 入口、legacy hook API、enemy passive 输入结构、effect executor fallback 接口、对应门禁测试与文档。
- **不含**：药水/地图/奖励系统、MVC 视图 alias、save service legacy 读写、战斗外 phase 控制。
- **依赖**：`COMBAT_TIMING_CONTRACT_V1`、`COMBAT_EVENT_CONTRACT_V1` 继续作为唯一真相；`tests/combat`、`tests/simulation` 需保持全绿。

## 当前 compat 面
1. `Player.start_turn / dispatch_turn_start_reactions / dispatch_combat_event_reactions / _run_legacy_*` 仍暴露给外部 ([contexts/combat/domain/player.py](../../contexts/combat/domain/player.py)).
2. `ITrait/IPower/BaseTrait/BasePower` 还定义 `on_turn_start/on_card_drawn/...` 等 legacy hook，且 `EventMapped*` 继续带兼容语义 ([contexts/combat/domain/traits.py](../../contexts/combat/domain/traits.py)，[contexts/combat/domain/powers.py](../../contexts/combat/domain/powers.py)).
3. 敌方 passive blueprint 仍依赖 `hook`，runtime 通过 `_run_compat_passives_for_window()` 调度 ([contexts/combat/domain/enemies/entity.py](../../contexts/combat/domain/enemies/entity.py)，[docs/development/ENEMY_DATA_SCHEMA_v1.md](../development/ENEMY_DATA_SCHEMA_v1.md)).
4. `EffectExecutor` 旧 API (`execute_card_effects/execute_effect_data/execute_effect`) 仍被主线 orchestrator 调用 ([contexts/combat/domain/effects/executor.py](../../contexts/combat/domain/effects/executor.py)，[contexts/combat/application/orchestration/card_play_orchestrator.py](../../contexts/combat/application/orchestration/card_play_orchestrator.py)).
5. 门禁文档 `COMBAT_MAINLINE_GATE_V1` 仍允许上述 compat seam 作为“暂存”，未定义清零门槛。

## 阶段划分
### Phase A：Player 公开 compat 清零
- 删除 `Player.start_turn()` 与 `dispatch_*` 公开入口；保留极薄 `@compat(alias)` shim 仅供测试注入（如需要），默认 raise。
- `_run_legacy_turn_start_reactions/_run_legacy_combat_event_reactions` 改为 `@deprecated` stub，主线里不再 fallback；契约测试改用 orchestrator/dispatcher 驱动。
- 更新 `COMBAT_MAINLINE_GATE`：禁止新增任何 `player.*` legacy wrapper 调用；allowlist 应为 0。
- Tests：
  - `tests/combat/test_combat_mainline_allowlist_v1.py`：断言 repo 内 无 `player.start_turn(` / `dispatch_*`.
  - `tests/combat/test_combat_timing_contract_v1.py` / `test_combat_event_contract_v1.py`：使用 state/orchestrator 触发，不再直接 call wrapper。

### Phase B：Trait/Power hook API 清零
- 从 `ITrait/IPower/BaseTrait/BasePower` 移除 `on_*` legacy 方法；`WindowMapped*`、`EventMapped*` 仅保留 window/event 映射。
- 提供 lint/test：扫描 combat 目录是否还定义 `def on_turn_start(` 等 legacy hook。
- 把 `COMBAT_MAINLINE_GATE_V1` 的 hook allowlist 升级为“违例即 fail”的 contract 测试。
- Tests：
  - `tests/combat/test_combat_mainline_allowlist_v1.py` 增加 `assert not rg('def on_turn_start')`.
  - 代表 trait/power 覆盖 window/event 行为，确保 runtime、preview、simulation 一致。

### Phase C：Enemy Passive 输入主线化
- Blueprint schema：用 `windows` 数组取代 `hook`；`hook` 字段标记为 deprecated，reader 在无 `windows` 时发 warning 并映射一次。
- Runtime：删除 `Enemy.start_turn(..., run_passives=True)` 与 `_run_compat_passives_for_window`；enemy passive 仅能作为 dispatcher reaction source；`Enemy.react_to_timing_window` 只负责 orchestrator 注入。
- 文档：更新 `ENEMY_DATA_SCHEMA_v1`，补 examples；把所有现有 JSON 切换到 `windows`。
- Tests：
  - `tests/combat/test_combat_reaction_dispatcher_v1.py`：覆盖 enemy passives 在 `ENEMY_START/END/COMBAT_START_REACTIONS` 的顺序。
  - 新增 blueprint regression（可能放在 `tests/scripts/test_generate_ta_enemy_content.py`）确保没有 `hook`.

### Phase D：Effect Executor 名称/入口收口
- 为 queue 主线添加中性 API：`execute_card_fallback`, `execute_effect_payload`, `execute_effect_once`（命名可再讨论），主线只调用新 API。
- `EffectExecutor` 中旧方法变成 `@deprecated` shim 并最终删除；`CardPlayOrchestrator` / `ActionExecutor` / 任意 effect impl 改用新名。
- 所有还没 queue 化的效果继续走 fallback，但入口不再叫 `legacy`.
- Tests：
  - `tests/combat/test_card_play_orchestrator.py`、`test_action_queue.py` 覆盖新 API。
  - `tests/combat/test_active_queue_boundaries.py` 验证 shim 被调用时抛 Assertion（或记录 warning）。

### Phase E：门槛与移交
- 更新 `docs/development/COMBAT_MAINLINE_GATE_V1.md` → `..._V2.md`：写入 compat-zero 门槛、测试套件、扩卡准入规则。
- 补 `docs/logs/daily` & Weekly summary 说明 compat-zero 完成。
- 建立“新增内容前检查”：例如 `scripts/check_combat_compat_zero.py` 或 pytest marker。

## 时间排序 & 依赖
1. Phase A (Player) 是所有阶段的前置（其他阶段都会少量触及 player/timing)。
2. Phase B 可以与 Phase C 并行，但 enemy blueprint 迁移涉及内容团队，建议 Phase A 完成后立刻 kick-off Phase C、并行 Phase B。
3. Phase D 依赖 Phase A/B：因为 orchestrator/traits/powers 将只使用新 API，再统一 effect executor。
4. Phase E 在前四阶段的回归全绿后执行。

## 资源 & 执行建议
- 默认以“工程包”形式（每包 2~3 天），每包先补契约测试再改实现。
- 每包结束必须跑：
  - `python -m pytest tests/combat -q`
  - `python -m pytest tests/simulation -q`
- 版本管理：继续在 `codex/MM-DD-topic` 子分支上切包，保持 PR 小而快。

## 风险与缓解
- **外部依赖**：若有脚本仍直接调用 `Player.start_turn()`，Phase A 前需全 repo 搜索，并在文档/社交渠道广播迁移窗口。
- **内容蓝图**：Phase C 改 schema 前需通知内容团队导出脚本；提供一次性迁移脚本，把 `hook` 翻译成 `windows`。
- **未 queue 化效果**：Phase D 保障 fallback 仍可执行；同时建立“剩余 legacy effect 列表”，逐步 queue 化。
- **测试噪音**：旧 hook 方法名移除可能导致 lint/flake 报错；先在 Phase B 里建立 allowlist 测试再清理。

## 验收条件（Compat-Zero Done）
1. repo 内无 `player.start_turn`, `dispatch_turn_start_reactions`, `dispatch_combat_event_reactions`, `_run_legacy_*` 调用/定义。
2. combat 代码中无 `def on_turn_start/on_card_drawn/...` legacy hook；`EventMapped*` 仅保留新接口。
3. 所有 enemy blueprint 使用 `windows`；runtime 中无 `_run_compat_passives_for_window`。
4. 主线 orchestrator/执行器不再引用 `execute_card_effects/execute_effect_data/execute_effect`；`EffectExecutor` 中无 `legacy` 命名。
5. `COMBAT_MAINLINE_GATE_V2` + pytest allowlist 均为 0；`tests/combat`、`tests/simulation` 全绿。
6. 日志/文档记录完成，内容团队默认以 compat-zero 标准扩卡。
