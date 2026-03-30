# Campaign 视觉架构 V1

## 目标

为战役侧未来的视觉系统建立一套可以长期演进的架构基线，用来承接：

- 背景层与场景层
- 挂点型局部特效
- 屏幕空间覆盖层
- 滤镜与后处理
- 视觉编辑器的长期演化

这份文档的目标不是做一个通用引擎，而是明确：

- 视觉逻辑该如何分层
- runtime visual state 该放在哪里
- 编辑器未来该演化成什么
- DDD 在这块该用到什么程度

## 为什么现在要定这件事

当前代码已经有视觉管线的雏形，但还没有形成一套统一语言。

已经存在的好基础：

- `frame_stage.py`
- `content_stage.py`
- `frame_compositor.py`
- `render_cache.py`
- `flame_overlay_renderer.py`
- `fusion_fx_renderer.py`

已经出现的风险：

- 视觉状态仍然比较分散地挂在 `CampaignView` 上
- gameplay service 仍可能直接触发 view 的具体特效入口
- 滤镜 / 后处理还不是显式概念
- 编辑器当前主要还是背景层工具，不是完整的视觉 authoring 模型

如果继续按“每来一个效果就加一个 renderer 函数”的方式增长，视觉系统很容易重新坍回大文件和隐式依赖。

## 核心结论

未来视觉架构不应该走两种极端：

- 不是继续堆零散 renderer
- 也不是直接做成重型通用引擎

推荐路线是：

- 业务层发出 `VisualIntent`
- 视觉运行时维护 `VisualRuntimeState`
- 渲染层执行显式的 `RenderPipeline`
- 编辑器维护长期存在的 `Authoring Spec`
- 通过编译 / 归一化层把编辑器数据转成 runtime 可消费配置

一句话：

- 视觉 runtime 是运行时结构问题
- 视觉 editor 是 authoring model 问题
- 这两者都不等于 gameplay 业务 domain

## 非目标

- 不做一次性引擎迁移
- 不做 shader-first 的全屏特效体系
- 不把视觉 runtime 做成业务 DDD aggregate
- 不在一轮里重写全部 `CampaignView`
- 不把编辑器做成完整引擎编辑器

## 视觉复杂度分层

未来视觉复杂度建议明确拆成 4 类：

### 1. 静态视觉内容

例如：

- 背景层
- 桌面层
- 场景装饰层
- UI chrome

特点：

- 生命周期长
- 变化频率低
- 更适合由 scene spec / layer spec 驱动

### 2. 挂点型动态效果

例如：

- 融合特效
- hover 动画
- 角色或节点附着效果
- 按钮 pulse
- 局部 flame / glow / shake

特点：

- 跟随某个节点、块、挂点或局部区域
- 有明确生命周期
- 更适合由 effect controller 驱动

### 3. 屏幕空间覆盖层

例如：

- 点击 ripple
- 受击闪白
- 警告 tint
- vignette
- scanline
- 全屏提示覆盖层

特点：

- 直接依附屏幕空间
- 不跟具体 gameplay node 绑定
- 更适合放在 overlay pass

### 4. 后处理 / 合成层

例如：

- camera shake
- 全局缩放与偏移
- pseudo-3D
- 整体 tint / darken / brighten
- 统一 postprocess

特点：

- 作用在合成后的 surface 上
- 顺序敏感
- 成本较高，需要明确性能边界

## DDD 在这块的适用范围

## 不要对视觉 runtime 做重 DDD

视觉 runtime 的主要复杂度是：

- 场景结构
- 效果生命周期
- pass 顺序
- 性能与缓存

这不是 gameplay 业务规则复杂度。

因此：

- 不建议把 visual runtime 做成一套 aggregate / repository / domain service 的重 DDD 结构
- 不建议为了术语完整性，把 renderer / effect / overlay 强行包装成业务领域对象

## 仍然需要保留业务边界感

虽然视觉 runtime 不该重 DDD，但业务层仍然应该保持清晰边界：

- gameplay / domain / application 决定“为什么要触发视觉”
- visual runtime 决定“怎么表现”

也就是说：

- 业务层保留 DDD / orchestration 的边界感
- 视觉层采用 runtime pipeline + authoring model 架构

## 编辑器可以演化出轻量领域感

编辑器未来会演化成一个长期小模型。

但它更适合被看成：

- `scene authoring model`
- `visual spec model`

而不是：

- gameplay domain model

如果未来出现以下需求，编辑器侧可以逐步增强建模强度：

- undo/redo
- schema version / migration
- 多工具共享同一套 spec
- 明确的不变量和校验
- 模板 / 覆盖 / 继承关系

即便如此，也更适合先做“强 spec model”，而不是直接做成完整业务 DDD。

## 推荐的总体分层

### 1. 业务 / 编排层

职责：

- 决定什么时候触发视觉表现
- 发出视觉意图
- 不直接组织具体绘制实现

推荐做法：

- service / state 不再直接调 `view.start_xxx_effect(...)`
- 改为发出明确的 `VisualIntent`

例如：

- `fusion_started`
- `screen_flash`
- `warning_overlay_started`
- `meeting_focus_opened`

### 2. 视觉运行时层

职责：

- 保存当前激活中的视觉状态
- 更新 effect 生命周期
- 管理 overlay / camera / postprocess 运行时状态
- 消费来自业务层的 `VisualIntent`

建议未来存在这样一组对象：

- `VisualIntent`
- `VisualRuntimeState`
- `EffectController`
- `OverlayController`
- `CameraState`

这层是运行时控制层，不是业务 domain。

### 3. 渲染管线层

职责：

- 按顺序执行各个 pass
- 约束每个 pass 的输入输出 surface
- 统一管理合成顺序

它的重点不是“更多文件”，而是：

- pass 顺序显式
- 输入输出显式
- 每个 pass 的职责单一
- 性能成本可判断

### 4. 编辑器 / authoring 层

职责：

- 维护视觉 authoring 数据
- 提供可编辑投影和命令
- 把 authoring 数据保存为稳定 spec

建议未来主要维护以下 spec：

- `LayerSpec`
- `EffectSpec`
- `OverlaySpec`
- `PostProcessSpec`

### 5. 编译 / 基础设施层

职责：

- 把编辑器 spec 编译或归一化成 runtime 可消费结构
- 管理 preset / schema / override / asset 配置
- 提供 store adapter

这层更接近 infrastructure，不应该塞进 view 或 runtime node。

## 推荐的渲染管线

建议未来固定成一条显式视觉管线：

1. `Background Pass`
2. `Board / World Pass`
3. `Attached FX Pass`
4. `Screen Overlay Pass`
5. `PostProcess Pass`
6. `HUD Pass`
7. `Present Pass`

结合当前实现，大致可以对应为：

- `background_stage.py`
  - 未来的 `Background Pass`
- `content_stage.py`
  - 未来拆成 `Board / World Pass` 与 `Attached FX Pass`
- `frame_compositor.py`
  - 未来的 `PostProcess Pass + Present Pass`

关键要求不是“文件名正确”，而是以下 contract 必须明确：

- 这个 pass 读取什么 surface
- 这个 pass 可以修改哪一层
- 这个 pass 的顺序是否固定
- 这个 pass 能否做高成本变换
- 这个 pass 依赖哪些 runtime visual state

## Runtime Node 的位置

runtime node 在未来仍然有价值，但角色要保持克制。

runtime node 适合负责：

- 场景结构
- 挂点关系
- 局部变换
- 局部可见性
- 局部输入与交互承载

runtime node 不适合负责：

- gameplay 规则
- save schema
- editor spec 持久化
- 全局 postprocess 组织

一句话：

- node 负责“局部结构”
- pipeline 负责“全局画面”

## 编辑器未来应如何演化

编辑器未来应该从“背景层 override 工具”演化成“视觉 authoring 工具”，但仍然要保持小而专注。

建议的演化方向：

### 第一层：图层 authoring

编辑内容：

- layer 开关
- z-order
- 锚点
- 偏移
- 缩放
- 可见性

### 第二层：局部效果 authoring

编辑内容：

- flame / glow / pulse
- sprite-sheet 播放参数
- hover / trigger 对应关系
- 局部 shake / fade / loop

### 第三层：overlay authoring

编辑内容：

- vignette
- flash
- tint
- scanline
- screen mask

### 第四层：postprocess authoring

编辑内容：

- camera shake
- 整体 offset / zoom
- pseudo-3D 参数
- 全局色彩修正

## 编辑器与运行时的关系

编辑器和运行时不要直接共享内部对象。

推荐结构：

- `Editor Spec`
- `Compiled Scene Spec`
- `Runtime Visual State Consumption`

也就是：

1. 编辑器维护 authoring 数据
2. 通过 compiler 做归一化 / 编译
3. runtime 消费编译后的视觉配置

这样做的好处：

- 编辑器字段不会污染 runtime
- runtime 临时状态不会反向污染编辑器
- schema 演化更容易控制
- 测试边界更明确

## 推荐的目录方向

未来不必一次性全部建齐，但建议朝以下方向收口：

```text
contexts/campaign/rendering/
  pipeline/
  passes/
  effects/
  postprocess/
  cache/

contexts/campaign/ui_editor/
  specs/
  commands/
  projection/
  store/
  compiler/

contexts/campaign/infrastructure/
  visual_override_store.py
```

更具体一点：

- `rendering/passes/`
  - 负责真正的 draw / composite pass
- `rendering/effects/`
  - 负责 effect controller 和 runtime effect instance
- `rendering/postprocess/`
  - 负责全屏或准全屏后处理
- `ui_editor/specs/`
  - 负责 `LayerSpec / EffectSpec / OverlaySpec / PostProcessSpec`
- `ui_editor/compiler/`
  - 负责把编辑器数据编译成 runtime 友好的视觉 spec
- `infrastructure/*store.py`
  - 负责 JSON / preset / override 持久化

## 新增特效 / 滤镜时的设计规则

以后每新增一个视觉效果，都建议先回答以下问题：

1. 它属于哪一类：
   - 局部挂点效果
   - 屏幕空间 overlay
   - 后处理
2. 它应该在哪个 pass 执行
3. 它读哪些 runtime state
4. 它的生命周期由谁管理
5. 它是否需要进入编辑器 spec
6. 它的性能等级是什么：
   - 轻量
   - 中等
   - 昂贵
7. 它需要什么缓存策略

这条规则的目的是避免“先写进去，再想它属于哪层”。

## 对滤镜与后处理的现实建议

由于当前是 `pygame` 路线，未来滤镜设计应遵循：

- 优先支持低成本效果
- 不默认假设有 shader
- 不把全屏高成本 blur / bloom 当作基础能力

优先级更高的效果类型：

- tint / darken / brighten
- flash
- mask
- crossfade
- camera shake
- pseudo-3D
- vignette
- sprite-sheet 动画

优先级较低、应谨慎引入的效果类型：

- 高频全屏模糊
- 实时大范围畸变
- 多层动态发光
- 需要大量 per-frame surface 分配的效果

## 性能与缓存原则

未来视觉层必须遵守以下性能规则：

- 渲染阶段不做素材 IO
- 尽量复用 surface
- 变换结果缓存要显式
- bucket 化可接受的动画中间结果
- 高成本效果要可开关
- 滤镜和后处理要有 degrade 策略

现有的 `render_cache.py` 是一个好起点，但后续需要更明确地区分：

- 几何变换缓存
- mask 缓存
- effect 中间面缓存
- postprocess surface 复用

## 测试策略

未来视觉系统的测试重点不应该是大量整图快照，而应该是以下几类护栏：

### 1. Pass 顺序契约测试

验证：

- 哪个 pass 先执行
- 哪个 pass 后执行
- 哪层覆盖哪层

### 2. VisualIntent -> RuntimeState 测试

验证：

- 业务发出的视觉意图是否能正确转成运行时视觉状态

### 3. Spec round-trip 测试

验证：

- 编辑器 spec 的保存 / 读取 / 编译是否稳定

### 4. 局部像素或行为断言测试

验证：

- 效果有没有被画出来
- 位置是否正确
- alpha / 可见性是否变化

### 5. 运行时降级测试

验证：

- 某个效果失败时，整帧是否仍能安全渲染
- 高成本效果被关闭后，主路径是否仍可用

## 迁移顺序

建议未来按以下顺序推进：

1. 先把现有 `frame_stage / content_stage / frame_compositor` 正名成视觉管线骨架
2. 引入 `VisualIntent` 作为业务到视觉的显式 seam
3. 把当前分散在 `view` 上的视觉状态逐步收进 `VisualRuntimeState`
4. 把现有 `fusion / click / flame` 等效果逐步迁入 runtime effect controller
5. 扩展编辑器，让它承载 `LayerSpec / EffectSpec / OverlaySpec / PostProcessSpec`
6. 再逐步增加新的滤镜和视觉效果

不要反过来做：

- 不要先堆一堆新效果，再回头整理架构

## 当前推荐判断

对未来视觉系统，推荐的判断是：

- 不需要重 DDD
- 需要强边界
- 需要显式 visual runtime
- 需要显式 render pipeline
- 需要长期存在的 authoring model

一句话总结：

- gameplay 继续保持 DDD / orchestration 边界
- visual runtime 走 pipeline + state machine 思路
- editor 走 authoring spec 思路

## 完成定义

当以下条件逐步成立时，可以认为视觉架构开始进入稳定状态：

- service 不再直接依赖具体 view 特效方法
- 视觉状态不再散落在 `CampaignView` 的大量临时字段上
- 渲染 pass 有明确顺序和输入输出 contract
- 新增一个效果时，可以明确判断它属于哪个 pass 和哪个状态层
- 编辑器开始维护稳定的视觉 spec，而不只是临时 override
- 新协作者可以在短时间内判断“一个视觉改动该放哪一层”
