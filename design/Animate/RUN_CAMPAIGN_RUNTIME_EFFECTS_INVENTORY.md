# `run_campaign.py` 真实运行动画与特效清单

## 1. 文档目的

这份文档不再按技术模块分组，而是改成按 `run_campaign.py` 的**真实运行阶段**来整理。

这样看文档时，可以直接沿着玩家实际看到的流程往下读：

1. 开始界面
2. 理想选择界面
3. 甘特图界面
4. 战斗界面
5. 其他穿插界面
6. 结局界面

## 2. 统计范围

本文只统计当前代码里**已经接线、真实会在运行时出现**的内容：

- 视觉特效
- UI 动画
- hover / 点击反馈
- 横幅、遮罩、粒子、位移、变形、演出时间线

本文不统计：

- 纯音频行为，例如 `BGM` 切换、`SFX` hover / click
- 只存在于 editor 工具链中的内容
- 只在旧设计稿里存在、但运行时没有真正渲染的方案
- 只有 hook、但现在没有可见输出的占位代码

## 3. `run_campaign.py` 运行阶段总览

`run_campaign.py -> contexts/shared/game_runtime.py::main()` 当前注册的主要状态有：

- `MAIN_MENU`
- `CAMPAIGN`
- `LOADING`
- `IDEALS`
- `EVENT`
- `DIALOGUE`
- `COMBAT`
- `DECK`
- `MEETING`
- `ENDING`

从玩家视角看，比较自然的流程分组是：

1. 开始界面阶段：`MAIN_MENU`、`LOADING`
2. 理想选择阶段：`IDEALS`
3. 甘特图主界面阶段：`CAMPAIGN`
4. 战斗阶段：`COMBAT`
5. 甘特图衍生 / 穿插界面：`DECK`、`MEETING`、`EVENT`、`DIALOGUE`
6. 结局阶段：`ENDING`

## 4. 阶段一：开始界面

对应状态：

- `MAIN_MENU`
- `LOADING`

### 4.1 `MAIN_MENU`

状态文件：

- `contexts/main_menu/state.py`

当前结论：

- **没有发现独立的视觉特效系统**

当前表现特点：

- 主要是静态菜单 UI
- 有 hover / click 音频反馈
- 有 BGM 淡出
- 但没有专门的动画层、粒子层、遮罩演出层

### 4.2 `LOADING`

状态文件：

- `contexts/loading/state.py`

当前结论：

- **没有独立特效系统**

当前表现特点：

- 主要是加载进度展示
- 目前没有额外的动态视觉演出可单独归类

## 5. 阶段二：理想选择界面

对应状态：

- `IDEALS`

### 5.1 `IDEALS`

状态文件：

- `contexts/ideals_select/state.py`

当前已接入的视觉表现：

1. 深色全屏底色
2. 一层比较克制的边框式画面处理

具体表现：

- `draw()` 中直接铺深色背景
- 再画一圈边框，形成比较轻的“框景 / vignette-like”观感

当前结论：

- 这里有**轻量级画面处理**
- 但还没有进入完整的动画 / 粒子 / 演出系统层级

## 6. 阶段三：甘特图界面

对应状态：

- `CAMPAIGN`

这一阶段是当前项目里**视觉反馈最密集**的一个区域之一。

### 6.1 点击涟漪

代码位置：

- `contexts/campaign/ui/effects.py::ClickEffectsManager`

触发来源：

- `contexts/campaign/services/campaign_mouse_click_intent_dispatcher.py`

应用位置：

- 甘特图画布上的有效点击

表现：

- 一个白色圆环从点击点向外扩散
- 透明度在约 `300ms` 内衰减

### 6.2 回合结束前的阶段式左移

触发来源：

- `contexts/campaign/services/end_turn_service.py`

应用位置：

- 当下一回合会发生头部融合时，回合结束会先进入一个“预演阶段”

参与渲染的模块：

- `CampaignView.set_three_click_stage_shift(...)`
- `contexts/campaign/rendering/block_renderer.py`
- `contexts/campaign/rendering/time_grid_renderer.py`
- `contexts/campaign/rendering/fusion_fx_renderer.py`

表现：

- 大部分可见任务块先整体向左轻微偏移
- 作为真正融合动画前的 anticipation

### 6.3 任务块 hover 描边

代码位置：

- `contexts/campaign/rendering/block_renderer.py`

应用位置：

- 鼠标悬停的甘特图任务块

表现：

- 可操作块：白色描边
- 不可操作块：灰色描边

### 6.4 `DDL` 当前触线脉冲

代码位置：

- `contexts/campaign/rendering/block_renderer.py`

应用位置：

- `DDL` 块与“今天线 / 行动线”重合时

表现：

- 描边宽度脉冲变化
- 外扩 glow 区域
- 强化危机感

### 6.5 行动线呼吸式暗化

代码位置：

- `contexts/campaign/rendering/action_line_breath_renderer.py`

调用位置：

- `contexts/campaign/rendering/content_stage.py`

应用位置：

- 行动线左右的一条竖向区域

表现：

- 区域亮度做周期性的乘法暗化 / 恢复
- 看起来像一条“呼吸中的聚焦带”

### 6.6 融合动画

触发来源：

- `contexts/campaign/services/end_turn_service.py`

动画创建：

- `CampaignView.start_fusion_effect(...)`

渲染位置：

- `contexts/campaign/rendering/fusion_fx_renderer.py`

应用位置：

- 发生融合的任务块

三段式表现：

1. 两个块互相吸附、并排靠拢
2. 轻微压缩 / 回弹式冲击
3. 过渡成融合后的结果块

内含子效果：

- additive 软 glow
- energy rim
- orbit glints
- spark burst
- 原块到融合块的交叉淡变

### 6.7 火焰顶层覆盖

代码位置：

- `contexts/campaign/rendering/flame_overlay_renderer.py`

调用位置：

- `contexts/campaign/rendering/frame_stage.py`

应用位置：

- `CAMPAIGN` 最顶层 frame overlay

表现：

- 基于 sprite sheet 的火焰动画
- 支持 frame 切换、旋转、缩放、视口裁剪

说明：

- 参数会读取 UI editor 保存下来的 override 数据
- editor 本身不属于 `run_campaign.py` 运行链路

### 6.8 BackgroundV2 hover 图层反馈

预加载位置：

- `CampaignView._preload_extra_layers()`

渲染位置：

- `contexts/campaign/rendering/background_renderer.py`
- `contexts/campaign/rendering/extra_layers_renderer.py`

应用位置：

- BackgroundV2 的额外装饰图层
- 例如 deck-view trigger、fish trigger、phone-power 相关图层

表现：

- hover 时换成更亮版本
- 某些图层只在 hover 时出现
- 某些图层在 hover 时隐藏
- 某些配对图层会发生 hover 切换

### 6.9 卷轴 hover 亮化

代码位置：

- `contexts/campaign/rendering/background_renderer.py`

应用位置：

- 当 scroll 图层本身被配置为 `deck_view` 触发器时

表现：

- hover 后卷轴整体亮度增强

### 6.10 伪 3D / 透视变形

合成位置：

- `contexts/campaign/rendering/frame_compositor.py`

应用位置：

- campaign 内容层
- 最终整帧输出

表现：

- scale + offset
- 顶边内收的透视 warp
- slice-based 倾斜变形

结果：

- 整个甘特图界面会有“纸面 / 桌面上的伪 3D 透视感”

### 6.11 当前未实际生效的占位项

代码位置：

- `contexts/campaign/ui/effects.py::FogRenderer`

当前状态：

- 只是预留 hook
- 现在没有可见渲染结果

因此：

- **不计入当前真实运行特效**

## 7. 阶段四：战斗界面

对应状态：

- `COMBAT`

这是当前项目里另一个**特效和演出最密集**的区域。

### 7.1 阶段横幅与敌人行动横幅

渲染态组装：

- `contexts/combat/mvc/render_state_assembler.py`

触发来源：

- `contexts/combat/runtime/session.py`
- `contexts/combat/runtime/enemy_turn_runtime_driver.py`

渲染位置：

- `contexts/combat/mvc/views/combat_view.py`

应用位置：

- 进入玩家回合
- 进入敌人回合
- 单个敌人行动摘要提示

表现：

- 顶部 phase banner 渐显
- 敌人行动 banner 单独出现
- `lock_queue` 时会额外显示文字横幅

### 7.2 敌人位移动画

元数据来源：

- `contexts/combat/application/orchestration/action_executor.py`
- `contexts/combat/runtime/enemy_tween_planner.py`

渲染位置：

- `contexts/combat/mvc/views/enemy_row_view.py`

应用位置：

- 敌人重排、reposition 一类动作

表现：

- 敌人从旧槽位缓动插值到新槽位

### 7.3 待机呼吸

渲染位置：

- `contexts/combat/mvc/views/enemy_row_view.py`
- `contexts/combat/mvc/views/ally_row_view.py`

应用位置：

- 敌人
- 玩家
- 论文队友

表现：

- 纵向 scale 小幅周期摆动
- 做出待机呼吸感

### 7.4 指针目标 bob 标记

渲染位置：

- `contexts/combat/mvc/views/enemy_row_view.py`

应用位置：

- 当前 pointer 选中的敌人上方

表现：

- 一个上下浮动的小箭头

### 7.5 shake / wobble 受击反应

控制位置：

- `contexts/combat/mvc/views/combat_view.py`

应用位置：

- 玩家 stress 上升时
- 敌人 / 玩家受到冲击时

表现：

- shake：随机抖动偏移
- wobble：带衰减的正弦摆动

### 7.6 飘字

管理位置：

- `contexts/combat/mvc/views/fx_controller.py`

触发位置：

- `CombatView._check_health_changes(...)`

应用位置：

- 玩家 stress 增减
- 敌人生命增减
- 玩家自信变化
- 敌人自信变化

表现：

- 数字向上漂浮
- 透明度逐渐减弱
- 大伤害 / crit 会有更强强调

### 7.7 受击粒子

生成位置：

- `contexts/combat/mvc/views/fx_controller.py`

绘制位置：

- `contexts/combat/rendering/fx.py::draw_hit_particles`

应用位置：

- 暴击或强调型伤害反馈

表现：

- additive glowing 粒子爆发
- 红 / 橙 / 黄暖色系

### 7.8 治疗粒子

生成位置：

- `contexts/combat/mvc/views/fx_controller.py`

绘制位置：

- `contexts/combat/rendering/fx.py::draw_heal_particles`

应用位置：

- 治疗
- 正向恢复类反馈
- 部分正向自信变化

表现：

- 柔和 halo
- 十字闪光
- 中心亮点

### 7.9 手牌飞入 / 翻面 / hover 抬升

代码位置：

- `contexts/combat/mvc/views/hand_view.py`

应用位置：

- 新进手卡
- hover 卡
- dragged 卡

表现：

- 卡牌从屏幕下方飞入
- 飞入时带翻面动画
- 手牌呈扇形 / 弧线排布
- hover / drag 的卡会上抬
- hover 卡会放大

### 7.10 `frontier` 高亮

代码位置：

- `contexts/combat/mvc/views/hand_view.py`

应用位置：

- `is_frontier == True` 的卡

表现：

- 一圈金色高亮边框
- 会跟随卡牌当前旋转角度

### 7.11 不可打卡牌遮罩

代码位置：

- `contexts/combat/mvc/views/hand_view.py`

应用位置：

- `playable == False` 的卡

表现：

- 一层暗色遮罩
- 顶层卡路径会额外显示“不可用”提示

### 7.12 拖拽瞄准箭头

代码位置：

- `contexts/combat/mvc/views/combat_view.py`

应用位置：

- 需要指定目标的拖拽出牌

表现：

- 一条二次曲线箭头
- 先画深色粗描边，再画亮色主线
- 末端有箭头头部

### 7.13 打牌飞出表现

代码位置：

- `contexts/combat/mvc/views/fx_controller.py`

应用位置：

- 手牌打出后的表现动画

流程：

1. 卡牌先飞到屏幕中央
2. 中央做一次快速缩放 / 聚焦
3. 再向右下角飞出屏幕
4. 飞行中留下流星尾迹
5. 第三阶段末端表现成发光光球

### 7.14 战斗场景分层

代码位置：

- `contexts/combat/rendering/layers.py`
- `contexts/combat/mvc/views/combat_view.py`

应用位置：

- 背景层
- 状态条层
- 左右前景层

说明：

- 这更像展示分层而不是时间型特效
- 但它确实属于当前真实运行时可见表现面的一部分

### 7.15 战败 `game over` 时间线演出

代码位置：

- `contexts/combat/mvc/views/combat_view.py::_render_game_over`

应用位置：

- 战斗失败时

表现流程：

1. 红字 ease-out 渐入
2. 文字有轻微呼吸缩放
3. 文字有细小振动偏移
4. 背后暗色圆角 panel 渐入
5. 文字 hold 后淡出
6. virtue 图像渐入
7. virtue 图像 hold 后淡出

## 8. 阶段五：其他穿插界面

这一类不是主流程的核心“长停留界面”，但会在 `run_campaign.py` 运行过程中穿插进入。

对应状态：

- `DECK`
- `MEETING`
- `EVENT`
- `DIALOGUE`

### 8.1 `DECK`

状态文件：

- `contexts/deck/state.py`

当前已接入效果：

1. 整屏半透明黑色遮罩
2. hover 卡牌大预览

应用位置：

- 从 `CAMPAIGN` 打开的卡组查看页

### 8.2 `MEETING`

状态文件：

- `contexts/meeting/state.py`

当前结论：

- `MEETING` 自身没有独立的复杂特效系统
- 但会调用共享模态层效果

会间接出现的效果：

- `DeckChoiceModal` 的 hover 放大预览
- `ChoiceModal` / `ListChoiceModal` / `RewardBundleModal` 的 dim 遮罩

### 8.3 `EVENT`

状态文件：

- `contexts/event/state.py`

当前结论：

- **没有独立特效系统**

当前表现：

- 主要是叙事文本与选项 UI
- 更像事件壳层，而不是动画场景

### 8.4 `DIALOGUE`

状态文件：

- `contexts/dialogue/state.py`

当前结论：

- **没有独立特效系统**

当前表现：

- 主要是对话文本与选项 UI
- 目前没有明显动画演出链

## 9. 阶段六：结局界面

对应状态：

- `ENDING`

### 9.1 `ENDING`

状态文件：

- `contexts/ending/state.py`

当前结论：

- **没有独立特效系统**

当前表现：

- 主要是不同结局原因对应的背景色
- 文本信息分块展示
- 目前还没有复杂的收束动画或转场时间线

## 10. 共享模态层效果

这部分不属于某一个单独阶段，但会穿插出现在多个阶段中，所以单独列出。

### 10.1 全屏 dim 遮罩

代码位置：

- `contexts/shared/ui/choice_modal.py`
- `contexts/shared/ui/reward_bundle_modal.py`
- `contexts/shared/ui/judgment_theater_modal.py`

应用位置：

- 阻塞型模态出现时

表现：

- 背后铺一层半透明黑色全屏遮罩

### 10.2 `DeckChoiceModal` 的 hover 放大预览

代码位置：

- `contexts/shared/ui/deck_choice_modal.py`

使用位置：

- `contexts/meeting/state.py`

应用位置：

- meeting 中的大卡牌选择层

表现：

- hover 的那张卡先不在网格里画
- 再在上层画一张 `1.5x` 的大预览

### 10.3 `JudgmentTheaterModal` 剧场演出

代码位置：

- `contexts/shared/ui/judgment_theater_modal.py`

应用位置：

- judgment / reviewer theater 演出

表现流程：

1. 全屏 dim
2. 老虎机式 reviewer reels
3. 三列依次停下
4. reviewer flash
5. editor reveal flash
6. 屏幕式 shake
7. 槽位边灯动态闪烁

## 11. 结论

### 11.1 当前特效密度最高的两个阶段

从真实运行链路看，特效和动画最集中的还是两块：

1. 甘特图界面阶段
2. 战斗界面阶段

### 11.2 当前最成熟的几条效果链

从代码完整度看，当前最成熟的运行时效果链是：

- 甘特图融合动画
- 甘特图火焰 overlay
- 战斗飘字 / 粒子 / 打牌飞出
- judgment theater 老虎机式演出

### 11.3 后续如果继续拆文档，最自然的方向

下一步如果还要继续细化，比较适合拆成：

1. `CAMPAIGN_RUNTIME_EFFECT_FLOW.md`
   - 只写甘特图阶段
2. `COMBAT_RUNTIME_EFFECT_FLOW.md`
   - 只写战斗阶段
3. `RUNTIME_EFFECT_OWNERSHIP_MAP.md`
   - 按“业务触发 -> 运行时状态 -> renderer”整理 ownership

