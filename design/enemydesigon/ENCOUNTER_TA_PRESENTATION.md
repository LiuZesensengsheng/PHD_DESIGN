# 期末汇报战：领导评审合议体（3-Boss Presentation)

## 设计目标
- 将期末从“考试/抓错”转为“讲对/说服”，以注意力与异议管理为核心，营造高张力“台上三评审”对抗。
- 三Boss：导师（Method/Support）、学院领导A（Time/KPI）、学院领导B（Optics/Provocation）。玩家可带1名学生作为队友助阵。

## 核心资源与胜负
- 注意力 Attention（全局条）：代表现场听众与评审的聚焦度。降至 0 则崩盘；保持 ≥ ATTN_PASS 阈值直至收束即胜。
- 异议 Objections（层数）：代表尚未被化解的质疑点。达到 OBJ_MAX 触发“请收尾/重做”重击（严重扣Attention/直接失败条件由难度决定）。
- 时间钟 Clock：每回合滴答；超时会触发“Wrap-up”压制事件。
- 三段式灯（动机-方法-结果）：玩家需在时限内点亮三灯（通过对应叙事动作/卡效果/环境牌配合）。

## 回合结构（P1→P2→P3）
- P1 期待设定（开场 1–2 回合）
  - 领导A：发布软规则（本回合出牌 ≤ PLAY_CAP；回合末手牌 ≤ HAND_CAP），宣告时间与KPI。
  - 导师：提供“温和窗口”（一次性 Leniency+1 或移除1层异议）。
  - 领导B：Optics提示（鼓励结构清晰/动机先行），若本回合你点亮“动机”则得到 ATTENTION_PULSE。
- P2 交叉火力（主体 3–N 回合）
  - 三人交替行动（见“Boss意图与冷却”）。你以环境牌与队友技能回应。
- P3 收束（尾段 2 回合）
  - 领导A触发“统一收束 Wrap-up”；
  - 判定：Attention ≥ ATTN_PASS 且 Objections < OBJ_MAX 且 三灯点亮 → Pass with comments；否则补做/延后（进入事件）。

## Boss 意图与冷却（示例）
- 导师（蓝/白，攻击低、偏支持）
  - Method Probe（CD 2）：抛出方法论细问。若本回合未使用 Citation/Clarify → Objections+1；若使用→移除1层Objections并返 ATTENTION_SMALL。
  - Supportive Note（CD 3）：你上一回合用 Clarify 命中时触发，直接移除1层Objections或给 Leniency+1。
  - Time Extension（稀有）：Clock -1 滴答（仅一次）。

- 学院领导A（白/黑，中压、时间/KPI）
  - Rule Banner（CD 2）：设置软规则（PLAY_CAP/HAND_CAP），本回合超限触发“小额罚分”= Attention-ATTN_MINOR。
  - Please Wrap Up（CD 3）：若 Clock 低于阈值或你连续两回合未点亮新灯→强迫收束（若未满足收束条件，Attention-ATTN_MAJOR 并 Objections+1）。
  - Budget Reminder（CD 2）：KPI提醒（小压力/小Attention-）。

- 学院领导B（蓝/红，视觉/挑刺，波动大）
  - Optics Critique（CD 2）：若你未打出 Highlight，本回合 Attention-ATTN_OPTICS；打出了则减半。
  - Applause Window（CD 3）：宣布欣赏窗口。你若在当回合打出 Highlight 或做一次无干扰 Demo → 获得 ATTENTION_PULSE 并移除1层轻质疑。
  - Laser Pointer（CD 2）：锁定你当前讲点。下一回合若你切题，Attention-ATTN_SWITCH；若承接并给出证据，返 ATTENTION_SMALL。

## 环境牌（0费，统一风格）
- Highlight（每回合 1 张）：指定当前讲点，短时 Attention+ATTN_HL；在“Applause Window”内额外 +ATTN_BONUS。
- Citation（CD 2 回合）：移除1层 Objection（优先“方法/数据源”标签），并返 ATTENTION_SMALL。
- Demo Plan B（战中 1–2 次）：启用备援演示，若当回合存在设备/场噪干扰，则避免 Attention 暴跌并返少量。

## 玩家队友（学生，选 1，均为 1 被动 + 1 主动）
- 勤奋（白）
  - 被动：标准答案守护（Leniency 上限 +1）。
  - 主动：纠错贴纸（CD 3）：移除1层 Objection；若标签为“文本/格式”，额外 ATTENTION_SMALL。
- 旁听（绿）
  - 被动：洞见（每 2 回合 +1 领悟，满层触发一次洞见）。
  - 主动：跨学科类比（CD 3）：移除 1 条刁钻追问；Attention+ATTN_SMALL。
- 代到（蓝）
  - 被动：转移检查（战中 1 次）：当触发“Wrap-up/抽查”时转移到自己，Clock +1 拍。
  - 主动：合影打卡（CD 4）：当回合免一次 Wrap-up 罚分（不免时限推进）。
- 混子（黑）
  - 被动：白噪镇场：场噪触发率-REDUCE_NOISE%。
  - 主动：按掉闹钟（CD 3）：取消下一次设备/场噪事件。
- 装逼（黑白）
  - 被动：人设经营：自身小护盾（不叠高）。
  - 主动：自我引用（CD 3）：嘲讽领导B 1 回合（成功→将其下一次 Optics Critique 改为 Applause Window；失败→自黑台词触发，小额 Attention-）。

## 三灯判定（动机-方法-结果）
- 动机：在任一回合使用 Highlight 指向“问题陈述/意义”并无被打断→点亮。
- 方法：在导师 Method Probe 后 1 回合内用 Citation 回应→点亮。
- 结果：在 Applause Window 内做一次成功 Demo 或给出关键数据结论→点亮。

## 数值与调参旋钮（占位）
- ATTN_PASS、OBJ_MAX、Clock 起始/长度、ATTN_HL/SMALL/MAJOR/OPTICS/PULSE、REDUCE_NOISE 等。
- 规则严苛度：PLAY_CAP/HAND_CAP；姿态切换频率与CD。
- 队友冷却与每场上限（如代到转移检查仅 1 次）。

## 台词样例（可本地化）
- 导师
  - Method Probe：“这个边界条件怎么处理？”
  - Supportive：“嗯，这一段说清楚了，就很好。”
- 领导A
  - Rule Banner：“请注意时间与结构。”
  - Wrap-up：“到这里可以收束了。”
- 领导B
  - Optics：“这页信息密度很高，观众可能跟不上。”
  - Applause：“刚才这个例子很好。”

## 演出与UI
- 舞台三屏：时间钟/异议层/注意力条；三灯位于标题下方。
- 姿态切换以灯光/聚光扫射表现；Applause 有观众弹幕与掌声波形。
- 误会撤回用“红章变蓝章”的视觉。

> 若需“形态级规则”调整，请先更新《理想系统 v9.0》并回链。
