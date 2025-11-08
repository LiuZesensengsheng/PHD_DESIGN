# 论文线（Thesis Track）GDD v0.9

目标：把“论文很难写 / 审稿人很折磨”转化为可玩且可感知的长期系统体验，并与现有甘特（Campaign）与战斗（Combat）系统自然勾连，传递压力、返修、被拒、玄学等真实学术体验，同时保持轻量的实现路径与可调性。

---

## 一、核心体验（玩家视角）
- 感受“长期不确定性”：写作—投稿—审稿—返修—再次投稿的循环；每一次推进都可能被随机事件打断（例如：审稿人2发难）。
- 明确“当下能做什么”：阶段性任务给出可操作的短目标（凑字数、补实验、改格式、降重等）。
- 代价与牺牲：为赶DDL/返修，你会付出压力、时间、牌组灵活度等代价，换来“研究进度/命名权/更强卡”。
- 黑色幽默：审稿意见既扎心又好笑；有强迫式格式修正/图像分辨率/参考文献标点等小折磨。

---

> 版本口径（MVP）：仅实现“论文线=甘特上一条轨道 + 任务推进”。美德/折磨不接入此线；其触发条件固定为“压力≥100”，与论文线无直接联动。

## 二、轨道与阶段（甘特接入）
论文轨道是独立的一条主线（`TRACK_ID = paper`），贯穿战役始终，采用“阶段—任务块—事件”的层级：

1) 开题（Proposal）
- 目标：确定课题卡（Thesis），绑定主色（与理想色一致或当前主色），解锁“研究进度环”。
- 任务块（Gantt）：选题仪式（一次性）→ 文献综述（可多次）→ 方案设计（一次）
- 事件：导师拍板/改题（轻随机）；玄学灵感（抽到同色课题卡时的加成）

2) 实验/研究（Experiments）
- 目标：攒“研究数据”“可复现度”“样本量到阈值”。
- 任务块：实验批次（多段、可失败/返工）、数据清洗、可视化与图表、统计功效验证
- 事件：设备故障/数据污染/学长借机抢装置/伦理审查补材料（轻中断）

3) 写作（Writing）
- 目标：形成初稿；字数、图表数、引用数达到门槛；语言质量通过最低门槛。
- 任务块：引言/方法/实验/讨论/结论（五段式），每段可多次微调；润色/格式化/降重
- 事件：Reference地狱、格式宗教、图像dpi不达标、LaTeX编译炸了

4) 投稿（Submission）
- 目标：选择期刊（影响命中率/周期/版面费）；付出“投稿成本（时间/版面费）”。
- 任务块：期刊选择（短）、封面信（短）、系统填报（短/概率出bug）
- 事件：系统崩溃/邮件进垃圾箱/Desk-Reject（Desk拒稿）

5) 审稿（Review）
- 目标：走完一轮或多轮“魔鬼循环”：审稿—意见—返修—复审
- 任务块：审稿中（随机时长条，受“可复现度/命题清晰度/图像质量”等加速/减速）
- 事件（核心）：审稿意见生成（详见“审稿人系统”）；阶段结果：Accept/Minor/Major/Reject

6) 返修（Revision）
- 目标：逐条解决意见，完成复现/补实验/改格式/补图/改写等；按回合数/甘特时长限制推进。
- 任务块：意见列表化为“可检查小目标”，每完成一个，返修评分+1；返修评分达到阈值才可“重新提交”。
- 事件：合作者消失/数据源过期/新Reviewer加入/主编“再补两组”

7) 发表（Publish）/ 拒稿（Reject）
- 发表：获得“命名仪式”（卡牌命名/署名角标）与“学术光环”（轻被动）；进入“下一个工作”的软引导。
- 拒稿：保留“已有改动”但损失部分“期刊信用”，可降级投稿或重新选择期刊；易触发“焦虑/内耗”等折磨状态。

---

## 三、系统资源与数值（抽象）
- 研究进度（progress_ring: 0..5）：五段式环（立论→方法→实验→讨论→结论）；达成解锁“突破/命名”。
- 可复现度（replicability: 0..100）：加速审稿期、降低审稿毒性；靠高质量实验/严格方法获得。
- 语言质量（language: 0..100）：影响Desk-Reject/小修的概率；靠润色与引用/拼写检查获得。
- 图表合规（fig_ok: bool）：图像dpi/标注/对齐；若false，必触发格式地狱事件。
- 投稿成本（sub_cost：金币/能量/时间片）：进入审稿的费用与“时间占用”。
- 审稿人折磨值（review_torture: 0..100）：审稿里程中叠加（Reviewer 2倾向较高）；越高越容易Major/Reject。
- 期刊信用（journal_credit: -2..+2）：同一刊多次拒稿会降低；降级投稿更容易命中但收益较低。

---

## 四、审稿人系统（Reviewer System）
### 4.1 审稿人原型（示例）
- Reviewer 1（友善）：关注语言/结构，常给 Minor；提出“拼写、格式、图注”等意见。
- Reviewer 2（毒性）：关注核心方法与对比实验，倾向 Major 或 Reject；有“玄学地狱”意见（模型不成立、换任务、再做10组）。
- Reviewer 3（不在线）：意见短且模糊（1-2句），有几率“未回”；由主编替补意见或延长审稿期。
- AE/主编：关键性规则者；总意见偏向 Desk 与“额外增长周期”。

### 4.2 审稿意见生成（数据驱动）
建议数据文件（后续可以CSV/JSON落地）：
```json
{
  "reviewers": [
    {"id": "r1", "name": "Reviewer 1", "tone": "friendly", "weight_minor": 0.6, "weight_major": 0.3, "weight_reject": 0.1},
    {"id": "r2", "name": "Reviewer 2", "tone": "toxic", "weight_minor": 0.2, "weight_major": 0.5, "weight_reject": 0.3},
    {"id": "r3", "name": "Reviewer 3", "tone": "absent", "weight_minor": 0.4, "weight_major": 0.2, "weight_reject": 0.1, "may_missing": true}
  ],
  "comments": {
    "format": ["参考文献标点混用。", "图注未按规范书写。", "图像分辨率不足。"],
    "method": ["实验设计存在内生性偏差。", "统计功效不足。", "缺少关键对比组。"],
    "language": ["语言不够清晰，需要润色。", "标题与摘要信息不一致。"],
    "toxic": ["建议完全更换研究问题。", "结论不成立，请重写。", "再做10组实验。"]
  }
}
```
生成规则（简化）：综合 `replicability`、`language`、`fig_ok` 与 `review_torture`，抽样 2-3 条意见，给出总结果（Minor/Major/Reject）。

### 4.3 返修评分（revision_score）
- 每条意见拆成可执行小任务（如“补实验X”“润色Y段”“修图Z张”）。
- 完成每条 +1 分，达到“期刊要求评分阈值”（随结果 Minor/Major 变化）才允许重新提交。

---

## 五、与战斗系统的联动（本MVP不接入，保留为后续方向）
- 可选方向（暂不实现）：
  - 折磨状态注入：在“漫长审稿/返修”阶段，触发绿色“焦虑”、白色“内耗”等轻度负面。
  - 灵感回声：关键节点触发一次性小奖励（抽1/能量+1等）。
  - DDL战：返修DDL临近时触发短挑战以改变审稿周期。

---

## 六、甘特映射（任务块规格）
最小可玩包只需实现下列块（每块 1-3 回合时长）：
- 文献综述（写作+1 / 语言+5）
- 小型实验（可复现度+5~10，可能失败返工）
- 图表修正（若 fig_ok=false，优先生成此块；完成后 fig_ok=true）
- 降重润色（language+5~15，可能触发“语言地狱”）
- 投稿准备（提交→进入“审稿中”状态）
- 返修（生成意见列表→拆解成小块→完成阈值后“重新提交”）
- DDL（事件战/短挑战）

---

### 6.1 MVP任务块定义与样例（仅任务，不用事件）
- 公共字段（与模型对齐）：`type="TASK"`, `theme="paper"`, `track="paper"`, `length`, `tags[]`,（可选）`gating{}`，（可选）`autoadvance: bool`
- 行为约定：
  - 点击“今天线”左侧的任务块执行 on_click 效果并移除该块；
  - `autoadvance=true` 的“等待块”不需点击，会随回合自动消耗长度直至完成。

示例（伪JSON）：
```json
[
  {
    "id": "paper_proposal",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "proposal"],
    "gating": { "requires_progress_ring_at_most": 0 },
    "on_click": { "progress_ring_delta": 1, "set_fig_ok": true, "set_language_delta": 5 }
  },
  {
    "id": "paper_lit_review",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "writing"],
    "gating": { "requires_progress_ring_at_least": 0 },
    "on_click": { "language_delta": 10 }
  },
  {
    "id": "paper_small_exp",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 2,
    "tags": ["paper", "experiment"],
    "gating": { "requires_progress_ring_at_least": 1 },
    "on_click": { "replicability_delta": 10 }
  },
  {
    "id": "paper_fix_figures",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "format"],
    "gating": { "requires_fig_ok": false },
    "on_click": { "set_fig_ok": true, "language_delta": 5 }
  },
  {
    "id": "paper_submission",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "submission"],
    "gating": { "requires_progress_ring_at_least": 3, "requires_fig_ok": true },
    "on_click": { "enter_review_wait": true }
  },
  {
    "id": "paper_review_wait",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 3,
    "tags": ["paper", "review", "wait"],
    "autoadvance": true,
    "on_auto_finish": { "spawn_revision_tasks": { "count": 3, "severity": "minor" } }
  },
  {
    "id": "paper_revision_task",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "revision"],
    "on_click": { "revision_score_delta": 1, "when_reach_threshold_then": "spawn_resubmit" }
  },
  {
    "id": "paper_resubmit",
    "type": "TASK",
    "theme": "paper",
    "track": "paper",
    "length": 1,
    "tags": ["paper", "resubmit"],
    "on_click": { "enter_review_wait": true }
  }
]
```

### 6.2 生成与推进规则（MVP）
- 生成（Spawning）
  - 每 4-6 回合，保证在 `track=paper` 生成 1 个论文任务块；按 `gating` 控制可见度与顺序；
  - 若 `fig_ok=false`，优先生成 `paper_fix_figures`；
  - 执行 `paper_submission` 后自动生成 `paper_review_wait`。
- 推进（Advancing）
  - 结束回合→全体块左移一格；`autoadvance=true` 的等待块自动消耗长度；
  - `paper_review_wait` 完成后，根据简化规则（`replicability/language/fig_ok`）生成 `paper_revision_task` 若干，或 `Publish/Reject` 边界块。
- 处理（Clearing）
  - 点击今天线左侧的论文块→执行 `on_click` → 移除该块。

### 6.3 审稿结果与返修阈值（MVP）
- 审稿等待基础长度=3；高 `replicability`/`language` 可加速（+25~40%）。
- Minor→生成 2-3 个 `paper_revision_task`；Major→4-6 个；Accept→生成 `Publish`；Reject→生成 `Reject` 并重置到写作/实验阶段。

---

## 七、UI/UX（轻量实现）
- 顶栏：论文进度环 + 当前阶段标签（如：写作/审稿/返修）。
- 审稿中：以“loading条+随机小气泡（审稿意见/AE处理/等邮件）”形式；条的速度受 `replicability/language/fig_ok` 影响。
- 审稿意见弹窗：条目式意见列表（可勾选完成）；毒性意见使用黄/红色徽标与黑色幽默文案。
- 提示横幅（toast）：投稿/Desk/Minor/Major/Reject/Accept 关键状态。

---

## 八、数值护栏（易调参数）
- Desk概率基线：language<40 或 fig_ok=false 时提升；`P_desk = base(0.15) + format_penalty + language_penalty`
- Minor/Major分配：`P_minor = f(rep,lang)`；`P_major = 1 - P_minor - P_reject`
- Reject触发：review_torture>70 或 replicability<30 且 method类意见≥2条时上升
- 审稿周期：基线3-5回合；`replicability>=70` 或 `language>=70` 时加速 25%-40%
- 返修阈值：Minor=2-3条，Major=4-6条（同刊可调）；每条小任务 1 回合内可完成

---

## 九、黑色幽默文案（样例）
- Reviewer 2：“你这个研究最好在另一个宇宙做。”
- AE：“谢谢你的投稿。我们很快会给出非常漫长的审稿周期。”
- 系统：“您的稿件因‘图片压缩过度’被退回到起点。”
- 合作者：“我在飞机上，网络不好，下周再说。”（每周一次）

---

## 十、与现有系统的对齐
- 美德/折磨：不接入本MVP；其触发条件固定为“压力≥100”，不因论文线而改变。
- 与甘特：`GANTT_TRIS_UI_SPEC.md` 中顶栏“论文（卡组）”入口沿用；论文轨道第一任务结算标“选题”。
- 与白色卡牌/事件系统：作为后续可选联动，不在本MVP范围。

---

## 十一、数据落地与实现顺序
1) 最小骨架：顶栏进度环、阶段标签、投稿→审稿→返修→再次投稿的循环；Minor/Major/Reject/Accept 结局路径（数值占位）。
2) 审稿意见系统：基于 JSON/CSV 的意见池随机生成，返修评分阈值判断。
3) 甘特任务块：文献综述/小实验/图表修正/降重/返修块；DDL小战。
4) 体验打磨：毒性意见权重、周期调速、黑色幽默文案池。

---

## 十二、后续扩展（非必要）
- 期刊分层（一区~四区）与降级投稿机制
- 版面费与减免/优惠券/审稿券
 - 开源复现：上传补充材料触发复现实验（一次性奖励）
- 审稿人关系系统：长期负面/正面累计影响（下一篇）


