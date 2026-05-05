# Cardanalysis Source Followup 人类审核包 01

> 新版请优先使用：
> `docs/qa/cardanalysis/source_followup_review_packet_01_scenarios.md`
>
> 这份原始版保留机器字段更多，不适合直接做人类审核。

- 审核包 id: `source_followup_review_packet_01`
- 日期: `2026-05-05`
- 来源库: `source_followup_case_library_v1`
- 范围: 从 500 条 advisory case 里抽 15 条做第一次人类审核试跑
- 运行时影响: 无

## 先说人话

你不用翻数据库，也不用改 JSON。你只需要在每一条的“你的审核”里填三行：

```text
决定:
信心:
备注:
```

可以很短。比如：

```text
决定: 同意建议
信心: 中
备注: 可以，先收下
```

如果某条你觉得不对，也可以写：

```text
决定: 拒绝过度推断
信心: 中
备注: 这个不能泛化，因为……
```

## 决定怎么填

你可以直接填中文，也可以填 A/B/C/D。我后续会负责翻译成机器字段。

| 选项 | 中文决定 | 机器含义 |
| --- | --- | --- |
| A | 先收下 | `accept_seed`，这条值得成为后续 reviewed seed 候选 |
| B | 需要更多证据 | `needs_more_evidence`，方向有用，但还缺例子或反例 |
| C | 拒绝过度推断 | `reject_overclaim`，说得太大或不安全，不该提升 |
| D | 合并重复 | `duplicate_or_merge`，和别的条目重叠，应合并 |

信心可以填：

- 高
- 中
- 低

## 重要边界

这份审核包本身不会提升证据等级。下面所有 case 仍然保持：

```text
design_note / human_curated / review_needed / advisory_context_only
```

也就是说，它们只是“设计审核线索”，不是正式卡牌规则，不是运行时逻辑，不是默认生成依据。只有你明确审核后，我才会另外生成一个 reviewed-decision shard。

## 常用词小字典

- 连锁疲劳: 连续打出、循环、重复触发越来越累，避免无限循环或无脑连招。
- 抽牌热度: 抽牌、换牌、循环手牌带来的注意力压力和手牌拥挤。
- 能量不稳定: 爆发能量、欠债、退款、回滚、下回合崩掉之类的问题。
- 污染市场: 现在拿收益，之后要清理负担，比如状态牌、废牌、延迟代价。
- 套件崩塌: 一组牌缺启动器、缺收益、缺兜底、缺安全阀，导致整套机制失灵。

## 审核条目

### 1. 连锁疲劳: 退出后动量反弹

- `case_id`: `human_curated_chain_fatigue_exit_momentum_rebound_followup_case_v1`
- 它在问: 退出一条连锁后，损失的动量会不会太多，导致玩家不愿意再回到这条路线？
- 风险: 重新进入体验变差，前面攒的势头像被清空。
- 还缺的证据: 平滑重新进入的例子，动量能反弹的例子，不愿重新进入的反例。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

### 2. 连锁疲劳: 循环和爆发连招的区别

- `case_id`: `human_curated_chain_fatigue_loop_vs_combo_sample_pair_followup_case_v1`
- 它在问: 什么情况算确定性循环，什么情况只是有边界的一回合爆发连招？
- 风险: 正常爆发回合可能被误判成循环问题。
- 还缺的证据: 确定性循环例子，有边界的爆发连招例子。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 3. 连锁疲劳: 反例边界

- `case_id`: `human_curated_chain_fatigue_counterexample_coverage_followup_case_v1`
- 它在问: 哪些反例能阻止“连锁疲劳”把不相关的连招也吸进去？
- 风险: 连锁疲劳这个概念可能管得太宽。
- 还缺的证据: 明确的反例集合，不相关连招样本。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 4. 抽牌热度: 反复重抽疲劳

- `case_id`: `human_curated_draw_heat_redraw_fatigue_followup_case_v1`
- 它在问: 反复重抽会不会在真正获得收益前，就先耗掉玩家注意力？
- 风险: 回合开始前选择负担太重，准备动作比收益还累。
- 还缺的证据: 简单重抽例子，重抽疲劳例子，手牌被锁住的对照。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

### 5. 抽牌热度: 真收益抽牌和低价值循环

- `case_id`: `human_curated_draw_heat_payload_vs_cantrip_followup_case_v1`
- 它在问: 真正带来收益的抽牌，是否应该和低价值的空转循环分开看？
- 风险: 大量低价值小循环会被误认为有意义的收益。
- 还缺的证据: 高收益抽牌例子，低价值循环对照。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 6. 抽牌热度: 反例范围

- `case_id`: `human_curated_draw_heat_counterexample_scope_followup_case_v1`
- 它在问: 哪些反例不应该纳入抽牌热度的主要审核范围？
- 风险: 反例被误写成规则，导致评价器变硬。
- 还缺的证据: 明确的反例范围，过度泛化失败样本。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 7. 能量不稳定: 回滚后仍然卡死

- `case_id`: `human_curated_energy_instability_rollback_lockout_followup_case_v1`
- 它在问: 能量进入坏状态后，是否还有可恢复的后备状态？
- 风险: 看似有回滚，其实这一回合还是被卡死。
- 还缺的证据: 回滚安全例子，回滚后仍卡死例子，备用出口对照。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

### 8. 能量不稳定: 爆发后的恢复

- `case_id`: `human_curated_energy_instability_burst_recovery_sample_pair_followup_case_v1`
- 它在问: 不稳定能量爆发回合之后，下一步会发生什么？
- 风险: 单回合爆发看起来很好，但会掩盖后续崩盘。
- 还缺的证据: 爆发收益例子，恢复或还债的后续例子。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 9. 能量不稳定: 反例边界

- `case_id`: `human_curated_energy_instability_counterexample_boundary_followup_case_v1`
- 它在问: 哪些能量反例不应该被泛化成通用规则？
- 风险: 个别反例被误写成全局政策。
- 还缺的证据: 明确的反例边界，过度泛化失败样本。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 10. 污染市场: 批量清理上限

- `case_id`: `human_curated_pollution_market_cleanup_batch_limit_followup_case_v1`
- 它在问: 如果污染只能批量清理，清理税会不会突然变得不公平？
- 风险: 批量清理让代价峰值过高。
- 还缺的证据: 单次清理例子，批量上限例子，被动清理对照。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

### 11. 污染市场: 短期成本和长期成本

- `case_id`: `human_curated_pollution_market_short_term_long_term_cost_pair_followup_case_v1`
- 它在问: 污染成本是临时的、长期的，还是两者都有？
- 风险: 短期负担和长期负担被混在一起。
- 还缺的证据: 临时污染例子，长期污染例子。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 12. 污染市场: 反例范围

- `case_id`: `human_curated_pollution_market_counterexample_scope_followup_case_v1`
- 它在问: 哪些污染反例应该留在主要证据边界之外？
- 风险: 反例被误写成政策文字。
- 还缺的证据: 明确的反例范围，过度泛化失败样本。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 13. 套件崩塌: 启动器底线不足

- `case_id`: `human_curated_plateau_package_enabler_floor_gap_followup_case_v1`
- 它在问: 收益牌要求配合前，这套牌是否有足够启动器底线？
- 风险: advisory note 被过度解读成证据，导致错误判断套件缺启动器。
- 还缺的证据: 启动器底线足够的例子，边界例子，失败例子。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

### 14. 套件崩塌: 主收益没触发时仍有价值

- `case_id`: `human_curated_plateau_package_fail_state_void_followup_case_v1`
- 它在问: 当主要收益没触发时，这套牌还能不能产生有用价值？
- 风险: 没有失败态价值会让整套牌在抽歪时变成空牌。
- 还缺的证据: 失败态仍有价值的例子，边界例子，反例。
- 建议: 先收下

你的审核:

```text
决定:
信心:
备注:
```

### 15. 套件崩塌: 缺少安全阀

- `case_id`: `human_curated_plateau_package_safety_valve_absent_followup_case_v1`
- 它在问: 临时生成过载时，这套牌是否有安全阀？
- 风险: 生成出来的牌太多，反而变成负担。
- 还缺的证据: 有安全阀的例子，边界例子，失败例子。
- 建议: 需要更多证据

你的审核:

```text
决定:
信心:
备注:
```

## 快速审核方式

如果你觉得建议基本合理，可以每条只写：

```text
决定: 同意建议
信心: 中
备注: 可以
```

如果你不确定，就写：

```text
决定: 需要更多证据
信心: 低
备注: 我现在判断不了
```

## Codex 后续处理

你填完后，我会：

1. 读取这些中文审核块。
2. 把“先收下”的条目转成单独的 reviewed-decision shard。
3. 把“需要更多证据”的条目转成后续证据队列。
4. 把“拒绝过度推断”和“合并重复”作为停止线或合并线保存。
5. 跑 case input 验证、focused tests、architecture、encoding、capability graph 和 `git diff --check`。
