# Campaign 视觉架构 V1

## 文档定位

这份文档定义 campaign 视觉系统的长期分层方向，并结合当前已经落地的代码结构，说明：

- 视觉 runtime 该如何继续收口
- 当前 UI 编辑器在整个视觉体系里的位置
- 哪些部分已经落地
- 哪些部分仍然是下一阶段工作

它不是“现在立刻重写全部视觉代码”的计划，也不是要把视觉系统变成重型通用引擎。

## 核心目标

战役侧视觉系统需要一条能长期演进的路径，用来承接：

- 背景层与场景层
- 挂点型局部特效
- 屏幕空间覆盖层
- 滤镜与后处理
- 视觉编辑器的长期演化

## 当前核心结论

当前最合适的整体判断仍然是：

- gameplay 继续保持 DDD / orchestration 边界
- visual runtime 继续朝 `pipeline + runtime state` 方向收口
- editor 继续朝 `authoring model / authoring spec` 方向演化

不要走两个极端：

- 不是继续堆零散 renderer
- 也不是直接做成重型通用引擎

## 当前代码与这套方向的对齐情况

### 已经对齐的部分

#### 1. runtime node primitive 保持克制

`contexts/campaign/ui_runtime/ui_node.py` 仍然只负责：

- parent / child 结构
- visible
- 事件遍历
- 绘制遍历
- global rect / position 辅助

它没有被编辑器持久化、树投影或 save schema 污染，这一点非常符合本架构的要求。

#### 2. 编辑器已经从单文件脚本演化成模块化 authoring 工具壳

当前 `ui_editor` 路径已经拆分为：

```text
contexts/campaign/ui_editor/
  constants.py
  preview_layout.py
  editor_models.py
  tree_projection.py
  editor_commands.py
  background_entry_builder.py
  session_state.py
  editor_layout_ui.py
  editor_rendering.py
  editor_loop.py
  editor_app.py
```

这说明编辑器已经不再是“背景层 override 脚本”，而是一个有明确内部边界的小型 authoring 工具。

#### 3. 持久化已经归位到 infrastructure

`contexts/campaign/infrastructure/ui_editor_override_store.py` 现在负责：

- UI editor override 读写
- background_v2 override 读写
- flame overlay override 读写

这符合“持久化属于 infrastructure，不应该塞进 runtime node 或 view”的要求。

#### 4. 入口已经变薄

`run_ui_editor.py` 现在只是薄入口和兼容导出壳，而不再是编辑器主实现。

这意味着编辑器这条路径已经符合“authoring 工具应该能被按职责阅读”的基本要求。

### 尚未完全对齐的部分

#### 1. 还没有显式 `VisualIntent`

当前视觉 runtime 仍然没有形成统一的：

- `VisualIntent`
- `VisualRuntimeState`
- `EffectController`
- `OverlayController`
- `CameraState`

因此，视觉系统整体仍然处在“局部已有方向感，但 runtime 总体结构还未完全显式”的阶段。

#### 2. 当前编辑器仍然是 override-first，不是 spec-first

虽然编辑器已经模块化，但当前保存路径仍然主要是：

- `EditableLayer`
- override payload
- store adapter

也就是说，当前更接近：

- 稳定的 authoring tool shell
- 仍偏 override 语义的数据模型

而不是完整的：

- `Editor Spec`
- `Compiled Scene Spec`
- `Runtime Consumption`

#### 3. render pipeline 还没有完全正名

当前已有良好基础：

- `background_stage.py`
- `content_stage.py`
- `frame_compositor.py`
- `render_cache.py`
- `flame_overlay_renderer.py`
- `fusion_fx_renderer.py`

但这些还没有被彻底统一成显式的 pipeline contract。

## 推荐的总体分层

### 1. 业务 / 编排层

职责：

- 决定为什么要触发视觉
- 决定什么时候触发视觉
- 不直接依赖具体 renderer 或 view 特效函数

这层未来应该发出明确的 `VisualIntent`，而不是直接调某个具体视觉入口。

### 2. 视觉运行时层

职责：

- 保存当前激活中的视觉状态
- 更新 effect 生命周期
- 管理 overlay / camera / postprocess 的运行时状态
- 消费来自业务层的视觉意图

建议未来收口为一组显式对象：

- `VisualIntent`
- `VisualRuntimeState`
- `EffectController`
- `OverlayController`
- `CameraState`

### 3. 渲染管线层

职责：

- 按顺序执行各个 pass
- 约束 pass 的输入输出 surface
- 管理最终合成顺序

当前建议的显式顺序仍然是：

1. `Background Pass`
2. `Board / World Pass`
3. `Attached FX Pass`
4. `Screen Overlay Pass`
5. `PostProcess Pass`
6. `HUD Pass`
7. `Present Pass`

### 4. 编辑器 / authoring 层

职责：

- 维护视觉 authoring 数据
- 提供可编辑投影和命令
- 把 authoring 数据保存成稳定模型

当前这层已经有实际落地，但还处在“override-first authoring shell”阶段。

### 5. 编译 / 基础设施层

职责：

- 把编辑器模型归一化或编译成 runtime 可消费配置
- 管理 schema / override / preset / asset 配置
- 提供 store adapter

当前的 `ui_editor_override_store.py` 已经落位，但 compiler 层还没有正式建立。

## 视觉复杂度分层

未来视觉系统仍然建议按 4 类复杂度拆分：

### 1. 静态视觉内容

例如：

- 背景层
- 桌面层
- 场景装饰层
- UI chrome

特点：

- 生命周期长
- 变化频率低
- 更适合由 `LayerSpec / SceneSpec` 驱动

### 2. 挂点型动态效果

例如：

- 融合特效
- hover 动画
- 角色或节点附着效果
- 局部 flame / glow / shake

特点：

- 跟随某个节点或局部区域
- 有明确生命周期
- 更适合由 effect controller 驱动

### 3. 屏幕空间覆盖层

例如：

- ripple
- flash
- vignette
- tint
- scanline

特点：

- 直接依附屏幕空间
- 不绑定具体 gameplay node
- 更适合进入 overlay pass

### 4. 后处理 / 合成层

例如：

- camera shake
- 全局 offset / zoom
- pseudo-3D
- 全局 tint / darken / brighten

特点：

- 作用在合成后的 surface 上
- 顺序敏感
- 需要明确性能边界

## 编辑器在这套视觉架构中的当前位置

### 当前已经具备的 authoring 能力

当前编辑器实际上已经覆盖了第一层 authoring 的核心部分：

- layer 开关
- z-order
- 偏移
- 缩放
- 可见性
- extra layer 分组投影

另外也已经开始触及局部效果 authoring 的边缘：

- flame overlay
- hover 触发相关层的 manifest 与 override 继承

### 当前还没成为完整 authoring spec 的部分

目前尚未正式承载：

- `EffectSpec`
- `OverlaySpec`
- `PostProcessSpec`
- compiler / normalization 层
- schema version / migration

所以，当前最准确的判断是：

- 编辑器已经是健康的模块化 authoring 工具
- 但还不是完整的视觉 spec 系统

## 推荐的目录方向

当前编辑器方向已经落在：

```text
contexts/campaign/ui_editor/
  constants.py
  preview_layout.py
  editor_models.py
  tree_projection.py
  editor_commands.py
  background_entry_builder.py
  session_state.py
  editor_layout_ui.py
  editor_rendering.py
  editor_loop.py
  editor_app.py

contexts/campaign/infrastructure/
  ui_editor_override_store.py
```

在此基础上，未来更长期的目录收口建议仍然是：

```text
contexts/campaign/rendering/
  pipeline/
  passes/
  effects/
  postprocess/
  cache/

contexts/campaign/ui_editor/
  specs/
  projection/
  commands/
  compiler/

contexts/campaign/infrastructure/
  visual_override_store.py
```

注意这里的意思不是“现在立刻重命名全部目录”，而是：

- 当前模块化成果已经足够支撑下一步演化
- 未来新增 `specs/`、`compiler/` 时会更自然

## 对当前 UI 编辑器路径的架构判断

当前 UI 编辑器路径和本视觉架构文档的关系可以概括为：

- 已经完成了“先模块化，再谈更强 authoring model”的第一步
- 已经证明这条路径适合继续演化
- 现在还不应该过早升级成重 DDD 结构

换句话说，当前推荐动作不是：

- 把编辑器直接改造成重型领域模型

而是：

- 在现有模块化结构上继续长出更强的 spec model

## 当前最值得推进的下一步

如果按照这份文档继续往前走，最值得做的顺序仍然是：

1. 先把现有 `frame_stage / content_stage / frame_compositor` 继续朝显式 pipeline 骨架收口
2. 引入 `VisualIntent`，让业务到视觉的触发 seam 显式化
3. 把散落在 `CampaignView` 上的视觉状态逐步收进 `VisualRuntimeState`
4. 让编辑器从 override-first 继续升级成更稳定的 `Editor Spec`
5. 在那之后，再逐步引入 `EffectSpec / OverlaySpec / PostProcessSpec`

不要反过来做：

- 不要先堆更多视觉效果，再回头整理边界

## 完成定义

可以认为视觉架构开始进入更稳定状态，当下列条件逐步同时成立时：

- service 不再直接依赖具体 view 特效入口
- 视觉状态不再散落在 `CampaignView` 的大量临时字段上
- render pass 有明确顺序和输入输出 contract
- 编辑器从 override 工具继续演化成稳定的 authoring spec 工具
- 新增一个视觉改动时，协作者可以快速判断它属于哪一层

## Last Updated

- `2026-04-02`
