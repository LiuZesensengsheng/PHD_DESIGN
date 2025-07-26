# 理论派设计 V2 - 结构重构版

本文件基于“严谨度”为核心光环的理念，重新设计理论派卡牌。

## 核心机制：严谨度 (Rigor) - 可消耗的智力资源

“严谨度”是理论派的核心战斗资源，它会因卡牌效果而动态增减。它代表了博士在辩论中的学术气势。

*   **正向增益：** 当严谨度为正数时，它会等值增强你的攻击伤害和技能格挡值。
*   **负向惩罚 (“学术债”)：** 当严谨度为负数时，它会等值削弱你的攻击伤害和技能格挡值。

### 消耗与偿还规则：

1.  **使用即消耗：** 每当你打出一张**受“严谨度”加成**的攻击牌或技能牌，你会消耗**1点**严谨度。
2.  **偿还学术债：** 当你处于“学术债”（负严谨度）状态下，每打出一张受惩罚的牌，你的严谨度会**恢复1点**（例如，从-4变为-3），代表你正在“偿还”你的逻辑漏洞。
3.  **多段攻击：** `旋风斩`、`连续拳`等多段攻击牌，整张牌**只消耗1点**严谨度。
4.  **自动触发：** `自引`、`势不可挡`等由能力牌自动触发的伤害效果，每次触发时也**消耗1点**严谨度。
5.  **间接收益：** `格挡反击`这类基于其他数值造成伤害的卡牌，其最终伤害会**再次享受**严谨度的加成（即 `伤害 = 格挡值 + 严谨度`），并消耗1点严谨度。

---

## 1. 公理 (Axiom) - 能力牌
**定位：** 理论体系的基石，**严谨度光环**的主要来源，提供永久性、被动性的增益。

| 中文名称 | 卡牌名称 (英文) | 类型 | 费用 | 效果描述 (中文) | 效果描述 (英文) |
|---|---|---|---|---|---|
| **第一性原理** | Demon Form | Power | 3 | 在每回合开始时，获得 2(3) 点 **严谨度**。 | At the start of each turn, gain 2(3) **Rigor**. |
| **不动点原理** | Metallicize | Power | 1 | 在你的回合结束时，获得 3(4) 点 **自信**。 | At the end of your turn, gain 3(4) **Block**. |
| **幻想型人格** | Feel No Pain | Power | 1 | 每当一张牌被 **消耗**，获得 3(4) 点 **自信**。 | Whenever a card is **Exhausted**, gain 3(4) **Block**. |
| **对偶理论** | Dark Embrace | Power | 2(1) | 每当一张牌被 **消耗**，抽 1 张牌。 | Whenever a card is **Exhausted**, draw 1 card. |
| **充分条件** | Barricade | Power | 3(2) | **自信** 在你的回合开始时不会被移除。 | **Block** is not removed at the start of your turn. |
| **自引** | Combust | Power | 1 | 在你的回合结束时，损失 1 点生命并对所有敌人造成 5(7) 点伤害。 | At the end of your turn, lose 1 HP and deal 5(7) damage to ALL enemies. |
| **辩证法** | Evolve | Power | 1 | 每当你抽到一张状态牌，抽 1(2) 张牌。 | Whenever you draw a Status card, draw 1(2) card(s). |
| **正则化** | Inflame | Power | 1 | 获得 2(3) 点 **严谨度**。 | Gain 2(3) **Rigor**. |
| **知耻** | Rupture | Power | 1 | 每当你因卡牌失去生命，获得 1(2) 点 **严谨度**。 | Whenever you lose HP from a card, gain 1(2) **Rigor**. |
| **挂arxiv** | Berserk | Power | 0 | 获得 2(1) 层 **破防**。在你的回合开始时，获得 1 点 **能量**。 | Gain 2(1) **Vulnerable**. At the start of your turn, gain 1 **Energy**. |
| **上早八** | Brutality | Power | 0 | (**固有**。) 在你的回合开始时，损失 1 点生命并抽 1 张牌。 | (**Innate**.) At the start of your turn, lose 1 HP and draw 1 card. |
| **自我PUA** | Corruption | Power | 3(2) | 技能牌费用变为0。每当你打出一张技能牌，**消耗** 它。 | Skills cost 0. Whenever you play a Skill, **Exhaust** it. |
| **反驳型人格** | Refuter Personality | Power | 3(2) | 每当你通过格挡抵挡一次攻击，对攻击者造成等同于你当前格挡值的伤害。 | Whenever you block an attack, deal damage to the attacker equal to your current **Block**. |
| **讨伐型人格** | Juggernaut | Power | 2 | 每当你获得 **自信**，对随机敌人造成 5(7) 点伤害。 | Whenever you gain **Block**, deal 5(7) damage to a random enemy. |

---

## 2. 定理 (Theorem) - 攻击牌
**定位：** 核心的伤害输出手段。大部分“定理”牌的伤害值会受到你当前“严谨度”光环的加成。

| 中文名称 | 卡牌名称 (英文) | 类型 | 费用 | 效果描述 (中文) | 效果描述 (英文) |
|---|---|---|---|---|---|
| **基础理论** | Strike | Attack | 1 | 造成 6(9) 点伤害。 | Deal 6(9) damage. |
| **高阶微积分** | Bash | Attack | 2 | 对敌人造成 8(10) 点伤害。施加 2(3) 层 **破防**。 | Deal 8(10) damage. Apply 2(3) **Vulnerable**. |
| **那我问你** | Anger | Attack | 0 | 造成 6(8) 点伤害。将此牌的一张复制品置入你的弃牌堆。 | Deal 6(8) damage. Add a copy of this card to your discard pile. |
| **论文发表** | Body Slam | Attack | 1(0) | 造成等同于你 **自信** 值的伤害。 | Deal damage equal to your **Block**. |
| **理论洁癖** | Clash | Attack | 0 | 仅当手牌中所有牌都是攻击牌时才能打出。造成 14(18) 点伤害。 | Can only be played if every card in your hand is an Attack. Deal 14(18) damage. |
| **群论** | Cleave | Attack | 1 | 对所有敌人造成 8(11) 点伤害。 | Deal 8(11) damage to ALL enemies. |
| **高度抽象** | Clothesline | Attack | 2 | 对敌人造成 12(14) 点伤害。施加 2 层 **虚弱**。 | Deal 12(14) damage. Apply 2 **Weak**. |
| **易得** | Headbutt | Attack | 1 | 造成 9(12) 点伤害。将弃牌堆中的一张牌置于抽牌堆顶。 | Deal 9(12) damage. Place a card from your discard pile on top of your draw pile. |
| **高阶范数** | Heavy Blade | Attack | 2 | 造成 14 点伤害。**严谨度** 对此牌效果翻 3(5) 倍。 | Deal 14 damage. **Rigor** affects Heavy Blade 3(5) times. |
| **作用力和反作用力** | Iron Wave | Attack | 1 | 获得 5(7) 点 **自信**。造成 5(7) 点伤害。 | Gain 5(7) **Block**. Deal 5(7) damage. |
| **运筹学** | Pommel Strike | Attack | 1 | 造成 9(10) 点伤害。抽 1(2) 张牌。 | Deal 9(10) damage. Draw 1(2) card(s). |
| **随机过程** | Sword Boomerang | Attack | 1 | 对随机敌人造成 3 点伤害 3(4) 次。 | Deal 3 damage to a random enemy 3(4) times. |
| **你们不对！** | Thunderclap | Attack | 1 | 对所有敌人造成 4(7) 点伤害并施加 1 层 **破防**。 | Deal 4(7) damage and apply 1 **Vulnerable** to ALL enemies. |
| **共轭** | Twin Strike | Attack | 1 | 造成 5(7) 点伤害两次。 | Deal 5(7) damage twice. |
| **导师救我** | Blood for Blood | Attack | 4(3) | 本场战斗中你每损失一次生命，此牌费用-1。造成 18(22) 点伤害。 | Costs 1 less energy for each time you lose HP in combat. Deal 18(22) damage. |
| **量子力学** | Carnage | Attack | 2 | **虚无**。造成 20(28) 点伤害。 | **Ethereal**. Deal 20(28) damage. |
| **微分流型** | Dropkick | Attack | 1 | 对敌人造成 5(8) 点伤害。如果敌人处于 **破防** 状态，则获得 1 点能量并抽 1 张牌。 | Deal 5(8) damage. If the enemy is **Vulnerable**, gain 1 energy and draw 1 card. |
| **钻牛角尖** | Hemokinesis | Attack | 1 | 损失 2 点生命。造成 15(20) 点伤害。 | Lose 2 HP. Deal 15(20) damage. |
| **追问** | Pummel | Attack | 1 | 造成 2 点伤害 4(5) 次。**消耗**。 | Deal 2 damage 4(5) times. **Exhaust**. |
| **贝塞尔曲线** | Rampage | Attack | 1 | 造成 8 点伤害。此牌在本场战斗中每次被打出，伤害增加 5(8)。 | Deal 8 damage. Increase this card's damage by 5(8) this combat. |
| **进化论** | Searing Blow | Attack | 2 | 造成 12(16) 点伤害。可以升级任意次数。 | Deal 12(16) damage. Can be upgraded any number of times. |
| **奥卡姆剃刀** | Sever Soul | Attack | 2 | **消耗** 手中所有非攻击牌。造成 16(22) 点伤害。 | **Exhaust** all non-Attack cards in your hand. Deal 16(22) damage. |
| **显然** | Uppercut | Attack | 2 | 造成 13 点伤害。施加 1(2) 层 **虚弱**。施加 1(2) 层 **破防**。 | Deal 13 damage. Apply 1(2) **Weak**. Apply 1(2) **Vulnerable**. |
| **深度穷举** | Whirlwind | Attack | X | 对所有敌人造成 5(8) 点伤害 X 次。 | Deal 5(8) damage to ALL enemies X times. |
| **派对结束** | Bludgeon | Attack | 3 | 造成 32(42) 点伤害。 | Deal 32(42) damage. |
| **洛希极限** | Feed | Attack | 1 | 造成 10(12) 点伤害。如果此牌击杀一个非爪牙敌人，获得 3(4) 点永久最大生命值。**消耗**。 | Deal 10(12) damage. If this kills a non-minion enemy, gain 3(4) permanent Max HP. **Exhaust**. |
| **代表作** | Fiend Fire | Attack | 2 | **消耗** 手中所有牌。每 **消耗** 一张牌，造成 7(10) 点伤害。**消耗**。 | **Exhaust** all cards in your hand. Deal 7(10) damage for each **Exhausted** card. **Exhaust**. |
| **吐槽** | Reaper | Attack | 2 | 对所有敌人造成 4(5) 点伤害。回复等同于未被格挡伤害的生命值。**消耗**。 | Deal 4(5) damage to ALL enemies. Heal HP equal to unblocked damage. **Exhaust**. |

---

## 3. 方法 (Method) - 技能牌
**定位：** 核心的防御与功能牌。大部分“方法”牌的格挡值会受到你当前“严谨度”光环的加成。

| 中文名称 | 卡牌名称 (英文) | 类型 | 费用 | 效果描述 (中文) | 效果描述 (英文) |
|---|---|---|---|---|---|
| **基本假设** | Defend | Skill | 1 | 获得 5(8) 点 **自信**。 | Gain 5(8) **Block**. |
|**深呼吸** | Armaments | Skill | 1 | 获得 5 点 **自信**。升级手中一(所有)张牌，持续到战斗结束。 | Gain 5 **Block**. Upgrade a(ALL) card(s) in your hand for the rest of combat. |
| **紧急科研** | Flex | Skill | 0 | 获得 2(4) 点 **严谨度**。在你的回合结束时，失去 2(4) 点 **严谨度**。 | Gain 2(4) **Rigor**. At the end of your turn, lose 2(4) **Rigor**. |
| **随想** | Havoc | Skill | 1(0) | 打出你抽牌堆顶的牌并 **消耗** 它。 | Play the top card of your draw pile and **Exhaust** it. |
| **“好的”** | Shrug It Off | Skill | 1 | 获得 8(11) 点 **自信**。抽 1 张牌。 | Gain 8(11) **Block**. Draw 1 card. |
| **冷静思考** | True Grit | Skill | 1 | 获得 7(9) 点 **自信**。**消耗** 手中一(指定)张随机牌。 | Gain 7(9) **Block**. **Exhaust** a random(not random) card from your hand. |
| **“收到”** | Warcry | Skill | 0 | 抽 1(2) 张牌。将手中一张牌置于抽牌堆顶。**消耗**。 | Draw 1(2) card(s). Place a card from your hand on top of your draw pile. **Exhaust**. |
| **头脑风暴** | Battle Trance | Skill | 0 | 抽 3(4) 张牌。本回合你无法再抽牌。 | Draw 3(4) cards. You cannot draw additional cards this turn. |
| **拧大腿** | Bloodletting | Skill | 0 | 损失 3 点生命。获得 2(3) 点能量。 | Lose 3 HP. Gain 2(3) Energy. |
| **推倒重来** | Burning Pact | Skill | 1 | **消耗** 1 张牌。抽 2(3) 张牌。 | **Exhaust** 1 card. Draw 2(3) cards. |
| **Ctrl C** | Dual Wield | Skill | 1 | 复制手中一(两)张攻击牌或能力牌。 | Create a(2) copy(s) of an Attack or Power card in your hand. |
| **膨胀** | Entrench | Skill | 2(1) | 使你当前的 **自信** 翻倍。 | Double your current **Block**. |
| **厚脸皮** | Flame Barrier | Skill | 2 | 获得 12(16) 点 **自信**。本回合每当你被攻击，对攻击者造成 4(6) 点伤害。 | Gain 12(16) **Block**. Whenever you are attacked this turn, deal 4(6) damage to the attacker. |
| **画饼充饥** | Ghostly Armor | Skill | 1 | **虚无**。获得 10(13) 点 **自信**。 | **Ethereal**. Gain 10(13) Block. |
| **说点啥吧** | Infernal Blade | Skill | 1(0) | 将一张随机攻击牌置入手牌，其本回合费用为0。**消耗**。 | Add a random Attack to your hand. It costs 0 this turn. **Exhaust**. |
| **拍马屁** | Intimidate | Skill | 0 | 对所有敌人施加 1(2) 层 **虚弱**。**消耗**。 | Apply 1(2) **Weak** to ALL enemies. **Exhaust**. |
| **学者风采** | Rage | Skill | 0 | 本回合你每打出一张攻击牌，获得 3(5) 点 **自信**。 | Whenever you play an Attack this turn, gain 3(5) **Block**. |
| **底线思维** | Second Wind | Skill | 1 | **消耗** 手中所有非攻击牌，每消耗一张获得 5(7) 点 **自信**。 | **Exhaust** all non-Attack cards in your hand and gain 5(7) **Block** for each card **Exhausted**. |
| **深度思考** | Seeing Red | Skill | 1(0) | 获得 2 点能量。**消耗**。 | Gain 2 energy. **Exhaust**. |
| **降维打击** | Shockwave | Skill | 2 | 对所有敌人施加 3(5) 层 **虚弱** 和 **破防**。**消耗**。 | Apply 3(5) **Weak** and **Vulnerable** to ALL enemies. **Exhaust**. |
| **导师脸色** | Spot Weakness | Skill | 1 | 如果敌人意图攻击，获得 3(4) 点 **严谨度**。 | If the enemy intends to attack, gain 3(4) **Rigor**. |
| **“您说的都对”** | Disarm | Skill | 1 | 使敌人失去 2(3) 点 **力量**。 | Weaken the enemy's strength by 2(3). |
| **双盲实验** | Double Tap | Skill | 1 | 本回合你的下一(两)张攻击牌会打出两次。 | This turn, your next (2) Attack(s) is(are) played twice. |
| **考古式科研** | Exhume | Skill | 1(0) | 将 **消耗** 堆中的一张牌置入手牌。**消耗**。 | Put a card from your **Exhaust** pile into your hand. **Exhaust**. |
| **自我催眠** | Impervious | Skill | 2 | 获得 30(40) 点 **自信**。**消耗**。 | Gain 30(40) **Block**. |
| **尤里卡！** | Limit Break | Skill | 1 | 使你的 **严谨度** 翻倍。**消耗**(不**消耗**)。 | Double your **Rigor**. **Exhaust**(Don't **Exhaust**). |
| **赌上毕生所学** | Offering | Skill | 0 | 损失 6 点生命。获得 2 点能量。抽 3(5) 张牌。**消耗**。 | Lose 6 HP. Gain 2 energy. Draw 3(5) cards. **Exhaust**. |

---

## 4. 猜想 (Conjecture) - 博士的课题板

灵感来源于《小丑牌》(Balatro) 中动态、惊喜的成长机制。我们决定将“猜想”从一个卡牌类型，升级为理论派角色**固有的、常驻的核心系统**。这代表了博士在应对眼前挑战的同时，脑海中始终在进行的、永不停歇的后台研究。

该系统旨在为理论派提供超越单场战斗的、贯穿整个游戏流程的独特成长路线和长线策略目标。

### 核心玩法循环

1.  **提出课题 (Project Proposal)**: 在关键节点（如每场战斗开始时，或完成上一个课题后），系统会从一个庞大的“课题池”中随机抽取3个不同的“猜想”，呈现在玩家面前。
2.  **选择课题 (Project Selection)**: 玩家进行**三选一**，这个选择本身就是一次重要的策略决策。每个“猜想”都明确绑定了其完成后的**唯一奖励**，选择课题即选择了你期望的回报。
3.  **验证猜想 (Conjecture Verification)**: 玩家通过在战斗内外达成特定条件来推进课题进度。当前课题的目标会常驻在UI界面上，作为持续的提醒。
4.  **获得成果 (Rewarding Breakthrough)**: 一旦条件达成，玩家立刻获得该课题绑定的奖励，并可以从新出现的三张课题中选择下一个进行挑战，形成“解决问题 -> 获得成长”的持续正反馈循环。

### 课题与奖励的多样性设计

“课题”的设计将远超战斗内的范畴，奖励也不再局限于强化单张卡牌，以创造更丰富的策略维度。

| 课题类别 | 课题示例 | 绑定奖励 |
|---|---|---|
| **战斗内课题** | **[一击毙命]**: 用单次超过50点的伤害击败一个敌人。 | 随机强化一张攻击牌，使其获得“**穿透**”（忽略格挡）属性。 |
| **战斗内课题** | **[理论风暴]**: 在一回合内打出10张或更多牌。 | 将一张“**尤里卡！**”（费用1，使你的**严谨度**翻倍，消耗）加入你的牌库。 |
| **跨战斗课题** | **[学术苦旅]**: 在抵达下一个篝火前，连续进入3个“？”房间。 | 在下一个篝V火处，你可以**免费升级两次**。 |
| **跨战斗课题** | **[项目基金]**: 累计获得200金币。 | 获得**100金币**。 |
| **元课题** | **[学术大爆炸]**: 完成你当前选择的课题。 | 你接下来完成的**两个**课题，其奖励将**翻倍**。 |
| **史诗级元课题** | **[并行研究]**: 在一场首领战中，在不损失生命值的情况下获胜。 | **[史诗奖励]**: 解锁角色的隐藏潜力，你现在可以**同时进行两个课题**。 |

---

## 5. 状态与诅咒 (Status & Curses)
*这部分我们后续再进行“换皮”设计。*

---
---

# 附录：角色设计总览 (Appendix: Character Design Overview)

本章节简要记录已构思的、拥有完全独立核心机制的四个博士角色。该设计思路旨在通过提供截然不同的玩法体验，最大化游戏的可玩性和深度。所有角色将共享同一个世界的敌人、通用遗物和地图事件。

### 1. 理论派 (The Theorist) - 战略规划家
*   **核心机制**: **博士的课题板 (The PhD's Project Board)**
*   **玩法体验**: 游戏的核心是完成在战斗内外发布的、三选一的“课题”任务。玩家需要在“完成当前战斗”和“推进长期课题”之间进行策略权衡。成长主要来源于完成课题后的多样化奖励（如金币、遗物、卡牌突变等），而非单场战斗。
*   **一句话总结**: 深思熟虑，大局为重，用智慧而非蛮力取胜。

### 2. 实验派 (The Experimentalist) - 资源收藏家
*   **核心机制**: **自走棋式的“三合一”聚合升级 (Auto-Chess Fusion)**
*   **玩法体验**: 玩法的核心乐趣在于通过各种手段（商店、战斗奖励）收集三张同名的牌，将其自动融合成一张更强大的“升星”版本。整个游戏过程是不断地进行资源管理和收集，以凑齐关键组合，见证卡牌从量变到质变。
*   -句话总结**: 只要样本够多，总能做出想要的结果。牌库就是我的实验室！

### 3. AI研究员 (The AI Researcher) - 高能魔法师
*   **核心机制**: **Dota2卡尔式的元素祈求 (Invoker-style Invocation)**
*   **玩法体验**: 通过打出基础的“元素”牌（如数据、算法、学习），来填充元素槽，然后“祈求”出根据元素组合而成的、强大的临时技能。为了防止最优解固化，引入“模型污染”机制惩罚连续使用相同组合的行为，鼓励玩家记忆和使用更多样的技能组合。
*   **一句话总结**: 我的回合，操作拉满！牌不重要，重要的是我脑中的公式。

### 4. 博弈论学者 (The Game Theorist) - 引擎构筑大师
*   **核心机制**: **学术扑克之“双重博弈” (Academic Poker - The Dual Gambit)**
*   **玩法体验**:
    1.  **外部博弈 (对敌)**: 将手牌组成“扑克牌型”（对子、同花、顺子等）打出，造成伤害。此操作不消耗能量。
    2.  **内部博弈 (对己)**: 消耗**能量**，打出单张牌，触发其“工具效果”（如抽牌、看牌库），或激活强大的“能力牌”（Joker）作为永久被动。
*   **核心抉择**: 珍贵的“能力牌”既可以花费能量激活为永久被动（长期投资），也可以作为“癞子”凑成顶级牌型打出并消耗掉（短期爆发）。
*   **一句话总结**: 牌局是我思想的延伸，每一步都是精心计算的博弈。

### 5. [DLC] 生命科学家 (The Life Scientist) - 召唤养成大师
*   **核心机制**: **基因培养皿 (The Gene Petri Dish)**
*   **玩法体验**: 玩法的核心不再是强化自身，而是通过“**创造**”、“**变异**”和“**指挥**”三类卡牌，在专属的“培养皿”槽位中召唤、养成并指挥能够自主战斗的生命体。玩家需要像《万智牌》的召唤师一样，管理场面、牺牲棋子、并保护自己培养出的核心生物，用“生物大军”淹没敌人。
*   **一句话总结**: 我的造物将为你带来最终的解决方案，或者……一场灾难。

