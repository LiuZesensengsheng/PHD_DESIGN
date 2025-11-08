# 论文线·美术清单（MVP）

> 目标：在不增加实现复杂度的前提下，为论文线提供统一风格的UI/图标/演出元素。覆盖甘特块、Pinned节点、审判席小剧场、等待泡泡、期刊层级皮肤、徽章与综述卡等。仅列交付清单、规格与风格，不涉实现。

---

## 1. 视觉与风格基调
- 核心：学术冷幽默 + 轻戏剧的“审判风味”
- 色系（建议）：
  - 层级色（Tier Skins）：T0=金黑；T1=深蓝；T2=石灰；T3=青绿；T4=橙灰（带“开源”绿标）
  - 审判章：ACCEPT=金；MINOR=蓝；MAJOR=红；REJECT=黑
- 字体：与现有全局字体一致；章/法槌标题可用更粗体切换（不新增字体文件为宜）

---


## 3. 层级皮肤与标签（T0–T4）
- 层级角标：T0/T1/T2/T3/T4，置于相关面板/卡片右上角
- 开源标记（OA）：“（开源）/Open Access”胶囊标，绿底白字
- IF/分区（玩笑用）：小圆徽“IF 40–80+ / Q0”等，仅作展示

---

## 4. 审判席小剧场（文字版演出配套）
- 章（Stamp）PNG（透明底，各1套双语文案可同底替换）
  - ACCEPT（接收）金色；MINOR（小修）蓝色；MAJOR（大修）红色；REJECT（拒稿）黑色
  - 尺寸：建议 640×360/1280×720 双规格（等比缩放），含轻阴影
- 法槌（Gavel）PNG + 简单压下序列（2–3帧）
- 审稿人名牌条（Reviewer Nameplate）
  - 三条：Reviewer1/2/3；右上小图标：天使/格式/措辞/拖延/奇葩
- 计票条（Result Tally）
  - 小图标列：ACCEPT/MINOR/MAJOR/REJECT，随章落亮起
- 编辑裁决横幅（Editor Verdict Banner）
  - 文案置中；底部细纹理，支持“快速模式”减弱动画

---

## 5. 战斗关联的UI（非数值，仅风味）
- “意见护盾”筹码（Opinion Chips）
  - 语言/格式/方法 三类图标小筹码；被击破时变灰
- 审稿战开场条（Battle Intro Strip）
  - 显示层级皮肤 + 本场主题（语言/格式/方法的权重提示，仅文案）

---

## 6. 等待期与泡泡（0回合）
- 泡泡样式 4 套：AE/系统/合作者/工具链（气泡色与小图标略区分）
  - 文案一行，自动折行；最大并发显示 2 个（样式不重叠）
- 等待角标与进度条
  - Desk checking…/AE queued…/PDF reflow… 轮播，弱动效

---

## 7. 期刊名与徽章/卡片
- 期刊名条（Journal Bar）
  - 左：层级角标 + OA胶囊；中：期刊名；右：IF圆徽
- 期刊“迷你封面”（可选）
  - 128×160 小竖卡，统一版式（标题上、层级色底、OA角标）
- 发表卡徽章（纯装饰）
  - Prereg/Data/Code/OA 四类勋章小图标，放在卡片底行

---

## 8. 综述卡（Review Card）
- 版式模板
  - 标题（上）+ 副标题（中）+ 摘要（下）
  - 徽章行（Prereg/Data/Code/OA）
  - 截图安全区（避免被UI遮挡）
- 尺寸：横 1280×720 / 1920×1080（适配现有分辨率系）

---

## 9. 动效与节拍（建议）
- 审判席：总时长 8–12 秒，可跳过；快速模式缩至 3–5 秒
  - 章落：280–320ms/枚；法槌落：400ms；计票条亮起：120ms/格
- 泡泡：淡入 150ms/淡出 150ms；等待角标轻呼吸 1.5s 循环

---

## 10. 音效（占位清单）
- 章落“砰”/法槌“咚”/打字机“噼啪”/轻“whoosh”切场
- 静音模式/快速模式时降噪（不新增复杂路由）

---

## 11. 规格与导出（建议）
- 分辨率：基准 1080p；需可等比适配 720p/1440p/4K
- 文件：PNG（透明底），少量可做 9-slice（角标/胶囊）
- 命名规范：
  - ui/thesis/gantt/block_workload.png
  - ui/thesis/gantt/block_workload_x2.png
  - ui/thesis/pinned/writing_boss.png
  - ui/thesis/pinned/review_ddl.png
  - ui/thesis/stamp/accept.png | minor.png | major.png | reject.png
  - ui/thesis/gavel/gavel_01.png … gavel_03.png
  - ui/thesis/badge/tier_T0.png … tier_T4.png
  - ui/thesis/badge/oa_capsule.png
  - ui/thesis/bubble/bubble_ae.png | system.png | collab.png | tools.png
  - ui/thesis/chip/opinion_language.png | format.png | method.png
  - ui/thesis/review_card/template_1080p.png

---

## 12. 交付清单（Checklist）
- 甘特块：工作量常态/合并态各1；Pinned（写作×导师/审稿结果）各1；0回合事件小胶囊（投稿/重投/发表）各1
- Gate 图标：伦理/设备/功效 各1
- 层级角标：T0–T4；OA 胶囊；IF/Qx 圆徽（玩笑）
- 审判席：章×4；法槌×1（2–3帧）；名牌×3；计票条×1；编辑横幅×1
- 意见护盾筹码：语言/格式/方法 ×各1
- 泡泡：AE/系统/合作者/工具链 ×各1；等待角标/进度条 ×1
- 期刊名条 ×1；（可选）迷你封面 ×1 模板
- 发表综述卡模板（1080p/可放大） ×1

---

## 13. 备注（落地约束）
- 不新增字体与大型序列帧；以静态PNG + 轻动效组合实现
- 颜色/素材尽量沿用现有UI规范；避免风格跳变
- 支持“快速模式/跳过”时的视觉完整性（无强依赖长动画）


