- Status: Draft
- Owner: Team
- Scope: thesis review / paper-line prototype
- Canonical: No
- Supersedes: none
- Superseded By: none
- Implemented In: none
- Last Reviewed: 2026-05-04

# 论文德州与审稿老虎机原型 V1

> 目标：把当前关于“论文牌型 + 审稿老虎机 Boss + 裁决拔河”的讨论收口成一个可继续推演的原型草案。
> 本文是 `Draft`，用于记录当前机制思想，不代表已经接受为当前实现规范。

## 1. 当前原型结论

1. 论文部分采用“德州扑克”表达。
2. 审稿部分采用“可战斗的老虎机 Boss”表达，而不是战前直接摇 verdict。
3. 论文牌型必须是审稿 Boss 战斗配置的主因，而不是战中实时判分窗口。
4. 审稿 Boss 的主目标不是击杀玩家，而是争夺一条编辑裁决槽：
   - `Reject <- Major <- Minor <- Accept`
5. 战斗中的伤害、压力、召唤物是附加压力；本场战斗的真正赌注是论文结果，而不是整局旅途立刻结束。
6. 审稿随机性不直接摇最终 verdict，而是摇出：
   - 本回合出现什么审稿意见符号
   - 哪些意见形成共鸣
   - 共鸣后召唤什么压力或攻击
7. `Accept / Minor / Major / Reject` 仍然保留，但它们应当是审稿 Boss 战后的编辑裁决结果，而不是 Boss 战前的固定标签。

## 2. 原型边界

### 2.1 本文覆盖

1. 论文四花色方向定义
2. 论文牌型与审稿结果的关系
3. 审稿老虎机 Boss 的身体结构与回合逻辑
4. 审稿人意见符号、怪癖、共鸣与可预测性原则
5. 原型阶段建议新增的数据表
6. 可替换当前实现的 MVP 代码/数据设计方向

### 2.2 本文不覆盖

1. 具体 UI 布局与动效
2. 具体数值平衡
3. 最终美术包装与完整演出分镜
4. 评奖/队友对打德州模式

## 3. 论文牌面原型

### 3.1 四个花色方向

论文德州的四个方向先定为：

1. `黑桃`：问题 / 理论
2. `梅花`：方法 / 实现
3. `方片`：实验 / 证据
4. `红桃`：表达 / 定位

选择理由：

1. 四个方向足够正交，便于让不同 reviewer 有清晰偏好。
2. 它们覆盖论文常见争议点：值不值得做、怎么做、证据够不够、讲得清不清。
3. “创新”不单列为花色，而是作为跨方向副属性存在，因为创新可以发生在问题、方法、实验设计或表达 framing 上。

### 3.2 创新作为副属性

当前建议：

1. 创新不作为第五方向，也不作为单独花色。
2. 创新作为副属性，影响：
   - 卡牌稀有度
   - reviewer 偏好触发
   - 牌型解释文案
3. 原型阶段先不单独做一张“创新表”，而是允许卡牌定义里带：
   - `innovation_level`
   - `risk_level`
   - `focus_level`

### 3.3 论文牌型在审稿 Boss 中的角色

1. 论文牌型在进入审稿 Boss 前只结算一次。
2. 结算结果不在战斗中作为实时牌型窗口反复展示，也不直接充当最终判分器。
3. 牌型用于生成“论文化身”的战斗配置：
   - 初始论文稳定度 / 标签生命线
   - 基础战斗力
   - 被动能力
   - 与主花色相关的防御、支援或干扰老虎机能力
4. 强牌意味着论文化身有更高基础强度与更好的防守/反制能力。
5. 弱牌意味着论文化身进入审稿场时更脆，但玩家仍可以依靠既有战斗牌库与战场临时牌操作来争取结果。
6. 论文牌型不直接对应 `Accept / Minor / Major / Reject`；它只决定你带着什么样的“论文体质”和“拆老虎机手段”进入审稿场。

一句话：论文牌型负责把论文编译成“战斗化身”，审稿老虎机负责把审稿过程编译成一个可对抗的荒诞机器。

### 3.4 战斗牌库边界

1. 玩家主卡组不是审稿战中临时编辑出来的。
2. 主卡组来自战前逐步积累的构筑，进入审稿 Boss 时已经决定。
3. 审稿 Boss 战可以额外发放少量“战场概念牌”，但这些牌应当是临时战斗工具，不应污染长期主牌库。
4. 战场概念牌用于表达审稿场动作，例如：
   - `补充说明`
   - `回应质疑`
   - `追加引用`
   - `重跑 baseline`
   - `请求导师介入`
   - `编辑部申诉`
5. 这些临时牌的来源可以是：
   - 论文化身根据牌型生成
   - reviewer 怪癖触发
   - 老虎机共鸣触发
   - 特定战斗阶段触发
6. 原型阶段的关键边界是：战中操作牌库是 combat 系统的事情；论文德州只负责战前编译论文状态，老虎机 Boss 只负责制造与审稿有关的战场压力。

## 4. 审稿老虎机 Boss 原型

### 4.1 结构

一次审稿 Boss 战时：

1. 先计算论文最佳牌型，并生成论文化身战斗配置。
2. 再生成一个“编辑部老虎机 Boss”：
   - `摇柄`：编辑动作，控制下一次摇奖启动
   - `三个轴`：三位 reviewer 的意见轴
   - `裁决槽`：`Reject <- Major <- Minor <- Accept`
   - `论文稳定度`：本轮投稿是否崩盘的底线
3. 每回合编辑拉动摇柄，三个 reviewer 轴摇出本回合意见符号。
4. 若符号形成共鸣，触发大奖、灾难、召唤物或裁决槽大幅偏移。
5. 玩家通过既有卡组、论文化身能力、针对老虎机身体的操作与临时概念牌，对抗本回合审稿结果。
6. 战斗结束后，根据裁决槽停点与论文稳定度，映射为 `Accept / Minor / Major / Reject`。

### 4.2 Boss 身体语义

当前推荐的语义是：

1. `编辑` 不占用某个普通敌人位，而是体现在：
   - 摇柄
   - 裁决槽
   - 共鸣后的宣判动作
2. `三个轴` 对应三位 reviewer，而不是三个普通小怪。
3. reviewer 的存在感来自：
   - 他们轴上的符号池
   - 他们默认怪癖
   - 他们造成的共鸣类型
4. 如果后续演出上想强化编辑人格，可以把中轴视觉做成“编辑盖章轴”，但 MVP 阶段不建议先改掉“三位 reviewer 三轴”的语义。

### 4.3 审稿意见符号

每个 reviewer 轴不会直接给 verdict，而是摇出意见符号。符号分为三类：

1. `负面符号`
   - `baseline 不足`
   - `实验不可复现`
   - `表达混乱`
   - `创新不足`
   - `撞学生工作`
2. `正面符号`
   - `问题有趣`
   - `工作量扎实`
   - `精准引用`
   - `叙事清晰`
   - `实验诚实`
3. `中性/变体符号`
   - `建议补充消融`
   - `建议改标题`
   - `建议换 framing`
   - `编辑要求补说明`

这些符号不是战后文案，而是本回合真的会推动裁决槽、产生攻击或召唤物的战场对象。

### 4.4 审稿人的机制身份与怪癖

当前分类先定为三类：

1. `硬怪癖`
   - 真正改写老虎机轴的危险性或裁决槽上限
   - 例：`baseline 不足不可 accept`
   - 例：`撞学生工作，重罚`
2. `软怪癖`
   - 轻微改写符号权重、细节攻击或小幅推档
   - 例：`注重细节`
   - 例：`讨厌大标题`
3. `彩蛋怪癖`
   - 主要负责吐槽、名号、戏剧性，偶尔带少量偏移
   - 例：`你居然引用了我 2018 年那篇冷门短文`
   - 例：`这方向我学生也在做`

### 4.5 可预测性原则

这个原型必须遵守：

1. 抽到谁是随机的。
2. 抽到什么怪癖是半随机的。
3. 怪癖怎么判你是确定的。

也就是：

1. 组合来源可以随机。
2. 一旦摇出来，规则就必须稳定且可解释。
3. 玩家应当能在事后明确看到：
   - 谁压了自己
   - 为什么压
   - 压了多少

### 4.6 共鸣、大奖与召唤物

共鸣不再只是风味名号，而是老虎机 Boss 的核心戏剧点：

1. 每回合先摇出三个 reviewer 的真实符号。
2. 再检测是否命中某个共鸣配方。
3. 命中后触发：
   - 大幅推动裁决槽
   - 召唤具象化质疑物
   - 造成对玩家或论文的额外压力
   - 播放对应吐槽或异名

示例：

1. `实验不足 + 实验不足 + 实验不足`
   - `来自地狱的实验审判`
   - 效果：裁决槽左移，并召唤 `可复现性质疑`
2. `撞学生工作 + 创新不足 + 方法相似`
   - `优先权灾难`
   - 效果：大幅推向 `Reject`
3. `问题有趣 + 工作量扎实 + 精准引用`
   - `编辑突然坐直`
   - 效果：裁决槽右移，并压低一个负面轴权重
4. `格式问题 + 格式问题 + 格式问题`
   - `格式炼狱`
   - 效果：不一定直接致命，但会疯狂制造小修压力

### 4.7 裁决拔河与附加伤害

当前推荐的主次目标分离为：

1. `主目标`：争夺编辑裁决槽。
2. `次目标`：保住论文稳定度。
3. `附加代价`：承受玩家压力、资源损失、负面状态与召唤物干扰。

具体原则：

1. 这场 Boss 战首先决定的是这篇论文的命运，而不是整局 run 是否立即死亡。
2. 论文稳定度归零，应当直接判定本轮投稿 `Reject`。
3. 玩家压力溢出优先转化为战后 debuff、资源惩罚或状态后果，而不是立刻结束整局旅途。
4. 如果后续存在“毕业最终答辩”之类超高风险节点，才考虑恢复“压力爆表可能导致 run 终局”的特例。

### 4.8 玩家与老虎机的交互方式

玩家打的不是抽象 verdict，而是老虎机的具体部位。当前推荐交互动词：

1. `打摇柄`
   - 延迟下一次摇奖
   - 降低下回合共鸣倍率
2. `打轴`
   - 压制某位 reviewer 的负面符号概率
   - 暴露其本回合即将出现的意见
3. `锁轴`
   - 保留一个有利结果
4. `重摇`
   - 赌掉一个坏结果
5. `拨轴`
   - 把一个坏符号拨成较轻结果
6. `卡轴`
   - 让某位 reviewer 短暂失声
7. `转化`
   - 把某个坏意见转成 `补充说明`、`小修建议` 或中性建议

这些动作的来源可以是：

1. 玩家原有战斗牌
2. 论文化身被动
3. 审稿战临时概念牌
4. 特定 reviewer 怪癖的反制窗口

### 4.9 审稿结果映射

为避免“明明打赢了却还是大修”的错位感，当前建议如下：

1. `Accept`
   - 裁决槽停在 `Accept`
   - 且论文稳定度未崩
2. `Minor`
   - 裁决槽停在 `Minor`
   - 或非常接近 `Accept` 但仍留有边角问题
3. `Major`
   - 裁决槽停在 `Major`
   - 这不表示“打赢了”，而表示“撑住了，但没有说服编辑”
4. `Reject`
   - 裁决槽停在 `Reject`
   - 或论文稳定度归零

一句话：`Accept/Minor` 才是“赢得漂亮/赢了”，`Major` 是“活下来了但没赢”，`Reject` 才是彻底输掉这篇论文。

## 5. 原型阶段的数据表规划

## 5.1 结论

最小原型建议：

1. **新增 6 张表**
2. **扩展 1 张旧表**
3. **可选再补 1 张 flavor 表**

这里的“表”不要求一定是 CSV；按当前仓库风格，原型阶段优先用 JSON 更顺。

## 5.2 新增 6 张表

### 表 1：论文卡牌目录表

- 建议文件：`data/paper/paper_holdem_card_catalog.json`
- 作用：
  - 定义可获得的论文牌
  - 记录花色、点数、副属性、来源标签
- 核心字段建议：
  - `card_id`
  - `name`
  - `suit`
  - `rank`
  - `innovation_level`
  - `risk_level`
  - `source_pool`
  - `notes`

### 表 2：论文拿牌/换牌规则表

- 建议文件：`data/paper/paper_holdem_offer_rules.json`
- 作用：
  - 定义战斗后、事件后、里程碑后的拿牌机会
  - 定义 `3选1`、换牌、跳过等原型规则
- 核心字段建议：
  - `trigger_id`
  - `source_type`
  - `offer_count`
  - `pick_count`
  - `replace_allowed`
  - `pool_tags`

### 表 3：论文牌型战斗配置表

- 建议文件：`data/paper/paper_avatar_combat_profiles.json`
- 作用：
  - 定义不同牌型进入审稿 Boss 时生成的论文化身配置
- 核心字段建议：
  - `hand_rank`
  - `power_tier`
  - `base_stability`
  - `base_attack`
  - `passive_slots`
  - `slot_control_actions`
  - `temporary_card_pool`
  - `suit_scaling`
  - `notes`

### 表 4：审稿人怪癖表

- 建议文件：`data/paper/reviewer_quirks.json`
- 作用：
  - 统一管理硬怪癖、软怪癖、彩蛋怪癖
- 核心字段建议：
  - `quirk_id`
  - `name`
  - `quirk_class`
  - `trigger_type`
  - `affected_suits`
  - `modifier_kind`
  - `modifier_value`
  - `incompatible_with`
  - `flavor_line`

### 表 5：老虎机意见符号表

- 建议文件：`data/paper/review_slot_symbols.json`
- 作用：
  - 定义每个 reviewer 轴可能摇出的意见符号
- 核心字段建议：
  - `symbol_id`
  - `name`
  - `symbol_class`
  - `source_archetypes`
  - `affected_suits`
  - `verdict_shift`
  - `spawn_effect`
  - `rarity`
  - `bark_key`

### 表 6：老虎机共鸣/大奖表

- 建议文件：`data/paper/review_slot_resonances.json`
- 作用：
  - 定义符号组合命中后的大奖、灾难、召唤物与裁决偏移
- 核心字段建议：
  - `resonance_id`
  - `name`
  - `required_symbols`
  - `required_classes`
  - `verdict_shift`
  - `summon_id`
  - `handle_modifier`
  - `paper_stability_damage`
  - `bark_key`

## 5.3 扩展 1 张旧表

### 扩展表：reviewer_slot_policy

- 现有文件：`data/paper/reviewer_slot_policy.json`
- 当前已有内容：
  - tier 基础权重
  - archetype bias
  - reel archetype weights
- 原型阶段建议扩展：
  - archetype 中文名
  - archetype 默认怪癖池
  - archetype 偏好花色
  - archetype 厌恶花色
  - archetype 默认符号池
  - archetype 共鸣偏置
  - reel 抽样黑白名单

也就是说，prototype 不必新开“审稿人原型表”；直接在现有 policy 文件上扩展即可，让它继续承担“谁来审、他们偏好什么、他们更容易摇出什么”的职责。

## 5.4 可选第 7 张 flavor 表

如果不想把 reviewer 吐槽文案继续塞进 `thesis_text_pools.json`，可以补：

- 建议文件：`data/paper/review_barks.json`

作用：

1. 专门管理 reviewer 吐槽
2. 专门管理共鸣异名台词
3. 专门管理少量彩蛋公告文案

如果原型阶段希望收得更紧，这张表可以先不加，直接先挂到现有文案池里。

## 6. 当前推荐的最小落地清单

如果只做最小原型，我建议先做：

1. `paper_holdem_card_catalog.json`
2. `paper_holdem_offer_rules.json`
3. `paper_avatar_combat_profiles.json`
4. `reviewer_quirks.json`
5. `review_slot_symbols.json`
6. `review_slot_resonances.json`
7. 扩展 `reviewer_slot_policy.json`

这样就够把：

1. 论文牌面
2. 审稿老虎机身体
3. reviewer 怪癖
4. 共鸣大奖
5. 论文牌型战斗配置

全部串起来。

## 7. MVP 替换实现建议

### 7.1 替换目标

当前代码仍是“先抽审稿 verdict，再决定是否进 Boss”。
MVP 目标应改为：

1. DDL 触发后不再直接给最终 verdict。
2. DDL 触发后生成：
   - 论文牌型快照
   - 论文化身配置
   - 审稿老虎机 Boss payload
3. 强制进入审稿 Boss 战。
4. 战斗结束后再映射 `Accept / Minor / Major / Reject`。

### 7.2 建议新增/替换的服务边界

1. `PaperHandService`
   - 计算最佳牌型、主花色、副属性摘要
2. `PaperAvatarCompiler`
   - 把牌型编译为论文化身配置
3. `ReviewSlotSpinService`
   - 根据 reviewer policy、怪癖、符号池生成老虎机轴结果
4. `ReviewBossTransitionBuilder`
   - 把论文状态和审稿 Boss payload 写进 combat transition
5. `ReviewBossOutcomeResolver`
   - 根据战斗结束状态、裁决槽停点、论文稳定度回写最终 verdict

### 7.3 当前实现中最可能受影响的入口

1. `contexts/campaign/services/thesis_judgment_service.py`
   - 从“direct verdict”改为“build review boss payload”
2. `contexts/campaign/services/thesis_judgment_flow_service.py`
   - 从“直接应用审稿结果”拆成“启动战斗”和“战后结算结果”
3. `contexts/shared/domain/contracts.py`
   - 扩展 `CombatStartRequest`，加入 thesis review boss payload
4. `contexts/combat/scene_builder.py`
   - 从 payload 生成老虎机 Boss 身体与论文化身
5. `contexts/campaign/services/thesis_slice.py`
   - 处理战后 thesis review payload 的持久化回写

### 7.4 建议新增的战斗往返 payload

进入战斗前：

1. `paper_hand_snapshot`
2. `paper_avatar_profile`
3. `review_slot_machine_payload`
   - reviewer archetypes
   - quirks
   - symbol pools
   - resonance tables
   - initial verdict gauge position

战斗返回后：

1. `review_verdict_band`
2. `paper_stability_after`
3. `review_reel_summary`
4. `resonances_triggered`
5. `pressure_after`

## 8. 下一步建议

下一轮如果继续推进，建议顺序是：

1. 先冻结四花色定义
2. 再冻结老虎机 Boss 的核心身体语义
3. 再冻结 reviewer 原型列表与默认符号池
4. 再做怪癖分类表
5. 再做牌型战斗配置表
6. 最后才写具体彩蛋名号与吐槽

原因很简单：先把骨架定住，再往上长戏。

## 9. 编码前还要核对的点

1. `paper_tags` 是直接迁移成 `paper_cards / paper_hand_state`，还是 MVP 期双轨共存。
2. 普通战斗/事件后，玩家在哪里获取论文牌。
3. 审稿 Boss 是否继续复用旧 encounter id，还是新建独立审稿老虎机 encounter。
4. 论文稳定度与玩家压力的战后后果怎么区分，避免“拒稿等于 run 结束”。
5. 现有 `PaperAlly` 是否继续作为论文化身的 MVP 容器。
6. 三轴是否坚持“三位 reviewer”，还是后续演出上改成“编辑轴 + reviewer 轴”。

## 10. 一句收口

这个原型当前最重要的判断是：

**论文部分用德州组织“结构”，审稿部分用老虎机组织“审判”，而玩家真正争夺的不是血条，而是编辑裁决。**
