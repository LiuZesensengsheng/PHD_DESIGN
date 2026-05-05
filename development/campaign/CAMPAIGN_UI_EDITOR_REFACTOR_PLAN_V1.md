# Campaign UI 编辑器重构计划 V1

## 文档定位

这份文档记录 campaign UI 编辑器这条工具链在 V1 阶段的目标、已落地结构、当前收益和剩余缺口。

它的关注范围仍然是：

- `run_ui_editor.py`
- `contexts/campaign/ui_editor/`
- `contexts/campaign/infrastructure/ui_editor_override_store.py`
- 与这条工具链直接相连的 `ui_runtime/ui_node.py`、`view.py` 兼容 seam

它不是一份 gameplay DDD 重写计划，也不是 `CampaignView` 全量清理计划。

## 目标

本轮重构的目标没有变化：

- 按职责做物理隔离
- 对人和 AI 都更容易安全阅读
- 在模块边界上可测试
- 能支撑后续持续演化

## 当前结论

截至当前仓库状态，UI 编辑器已经从“单文件巨型脚本”收口为“薄入口 + 多个职责模块”的结构。

这意味着：

- `run_ui_editor.py` 已不再承担主逻辑
- 编辑器模型、预览数学、树投影、命令、builder、会话状态、布局 UI、渲染、事件循环都已有明确归属
- override 持久化已经从误导性的 `phone_widget_store.py` 归位到 `infrastructure`
- 相关逻辑已经可以在不启动完整编辑器的前提下被聚焦测试

但这轮重构也有明确边界：

- 当前仍然是 override-first 的编辑器，不是完整的 `Editor Spec -> Compiler -> Runtime` 体系
- `CampaignView` 与 runtime 兼容 seam 仍然保留
- `ui_runtime/ui_node.py` 继续只做 runtime primitive，不吸收编辑器职责

## 重构前的问题

原始热点主要集中在旧版 `run_ui_editor.py`：

- 编辑器数据模型、树投影、预览几何、素材组装、保存逻辑、pygame 事件循环混在一起
- `EditableLayer` 既承载运行时节点，又承担编辑器元数据和序列化
- 树分组和排序策略埋在主脚本内部
- override 读写放在 `contexts/campaign/ui_runtime/phone_widget_store.py`
- 新协作者必须读完整个入口脚本，才能判断一个改动该落在哪

本轮的重点就是把这些职责拆开，而不是直接发明更重的新抽象。

## 当前模块结构

当前实际结构如下：

```text
run_ui_editor.py

contexts/campaign/ui_editor/
  __init__.py
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

contexts/campaign/ui_runtime/
  ui_node.py
  phone_widget_store.py   # 兼容转发层
```

## 职责分布

### 1. 入口

- `run_ui_editor.py`
  - 只保留薄入口和少量兼容导出
  - 允许旧测试或旧调用点暂时继续工作

### 2. 纯配置 / 常量

- `contexts/campaign/ui_editor/constants.py`
  - 窗口尺寸
  - 面板宽度
  - 预览缩放常量
  - 树列表绘制常量
  - 编辑器 UI 颜色

### 3. 预览几何与坐标映射

- `contexts/campaign/ui_editor/preview_layout.py`
  - `PreviewLayout`
  - 预览显示矩形
  - source rect / display rect 计算
  - zoom / pan 坐标换算

这是当前最纯的一层数学逻辑边界。

### 4. 编辑器模型与 payload

- `contexts/campaign/ui_editor/editor_models.py`
  - `EditableLayer`
  - `build_background_override_payload(...)`
  - `build_flame_override_payload(...)`
  - `iter_editor_nodes(...)`

这里已经把“编辑器数据结构”和“保存时 payload 组装”从主循环里拿出来。

### 5. 树投影

- `contexts/campaign/ui_editor/tree_projection.py`
  - `EditorTreeGroup`
  - `EditorTreeRow`
  - 分组标签和路径归一化
  - tree rows 构建
  - 选中项展开辅助

树逻辑现在被明确看作 projection，而不是 runtime node 行为。

### 6. 编辑器命令

- `contexts/campaign/ui_editor/editor_commands.py`
  - entry 解析
  - reorder
  - size input 应用
  - resize/reorder 能力判断

这层已经形成第一层比较清楚的“编辑器动作 seam”。

### 7. builder / 组装层

- `contexts/campaign/ui_editor/background_entry_builder.py`
  - 背景层 surface 载入与缩放
  - darken 处理
  - `BackgroundV2` 基础层与 extra layers 组装
  - flame overlay entry 构建

这部分已经从主循环中隔离出来，但目前仍然是 override-first builder，不是独立 compiler。

### 8. 会话状态

- `contexts/campaign/ui_editor/session_state.py`
  - `EditorSessionState`
  - 选中、拖拽、滚动、zoom、pan、输入框、状态栏等临时运行状态

这一步的主要收益是让主循环不再依赖大量松散局部变量。

### 9. 布局 UI

- `contexts/campaign/ui_editor/editor_layout_ui.py`
  - 树面板矩形
  - 滚动条几何
  - Inspector 行文本
  - 尺寸输入框和排序按钮几何

这是本轮后半段新增的拆分，用来继续压缩 `editor_app.py` 热点。

### 10. 渲染层

- `contexts/campaign/ui_editor/editor_rendering.py`
  - tree panel 绘制
  - preview panel 绘制
  - inspector panel 绘制
  - 选中高亮和 real-view overlay 绘制

### 11. 循环 / 编排层

- `contexts/campaign/ui_editor/editor_loop.py`
  - session 初始化
  - 每帧上下文准备
  - 窗口重建
  - 保存编排
  - 输入事件处理

### 12. 应用壳

- `contexts/campaign/ui_editor/editor_app.py`
  - 负责把 `loop` 与 `rendering` 接起来
  - 当前已经收缩成非常薄的 bootstrap / main loop 壳

### 13. 持久化

- `contexts/campaign/infrastructure/ui_editor_override_store.py`
  - `load_ui_editor_overrides(...)`
  - `load_background_v2_overrides(...)`
  - `load_flame_overlay_overrides(...)`
  - `save_background_v2_overrides(...)`
  - `save_flame_overlay_overrides(...)`
  - `get_ui_editor_overrides_mtime(...)`

### 14. 兼容壳

- `contexts/campaign/ui_runtime/phone_widget_store.py`
  - 现在仅作为兼容转发层存在
- `contexts/campaign/ui_runtime/ui_node.py`
  - 继续作为 runtime primitive，保持小而纯

## 已达成的收益

### 1. 物理隔离已经成立

当前已经不再依赖“读完整个入口脚本”来理解编辑器。

一个协作者现在可以更直接地定位：

- 预览数学在哪
- 树逻辑在哪
- 命令在哪
- builder 在哪
- store 在哪
- 主循环在哪
- 渲染在哪

### 2. 阅读成本明显下降

最明显的变化有两个：

- `run_ui_editor.py` 已经不是热点
- `editor_app.py` 在第二轮拆分后也不再是巨型文件

现在真正的阅读方式变成“按职责进文件”，而不是“先冲进一个大文件再搜索函数名”。

### 3. 测试边界已经形成

当前已经存在的相关测试包括：

- `tests/campaign/test_ui_editor_tree_rows.py`
- `tests/campaign/test_ui_editor_background_overrides.py`
- `tests/campaign/test_background_v2_layer_manifest.py`
- `tests/campaign/test_campaign_runtime_ui_boundary_contract.py`
- `tests/campaign/test_ui_editor_preview_layout.py`
- `tests/campaign/test_ui_editor_payload_contract.py`
- `tests/campaign/test_ui_editor_commands.py`
- `tests/campaign/test_ui_editor_override_store.py`
- `tests/campaign/test_ui_editor_layout_ui.py`
- `tests/campaign/test_ui_editor_loop_smoke.py`

这说明：

- preview 数学可单测
- payload 合约可单测
- command 行为可单测
- store 读写可单测
- 布局 UI 几何可单测
- loop 与 rendering 至少有 smoke 级别护栏

### 4. 兼容迁移路径更清楚

当前已有比较明确的迁移策略：

- 新归属放到 `ui_editor/` 和 `infrastructure/`
- 旧路径通过兼容壳暂时转发
- runtime primitive 保持不动
- `CampaignView` 兼容 seam 留到后续独立 cut

## 当前还没做完的部分

下面这些点是“当前结构健康，但尚未完成”的部分。

### 1. 还不是 spec / compiler 架构

虽然编辑器已经模块化，但仍然是：

- `EditableLayer`
- override payload
- store adapter

这还不是：

- `Editor Spec`
- `Compiled Scene Spec`
- `Runtime Consumption`

也就是说，当前已经是干净的编辑器模块化结构，但还不是视觉架构文档里更长期的 authoring-spec 形态。

### 2. builder 仍然是 override-first

`background_entry_builder.py` 当前会直接读取 store 和常量配置来组装 entry。

这在当前阶段是合理的，但后续如果要继续升级成更稳的 authoring model，需要把它进一步收口成：

- 输入更显式
- store 依赖更外移
- 能为 future compiler 层让路

### 3. runtime 兼容 seam 仍然在

本轮明确没有处理：

- `CampaignView.handle_runtime_ui_event(...)`
- `CampaignView.update_runtime_ui(...)`
- `CampaignView.render_runtime_ui(...)`
- `background_stage.py` 中与旧路径相关的兼容调用

这些仍然应该作为后续单独一轮工作。

## 当前推荐判断

对于 UI 编辑器这条路径，当前最准确的判断是：

- V1 的模块化目标已经大体达成
- 入口和热点文件已经显著缩小
- 边界已可测试
- 结构已经适合继续迭代

但同时：

- 还没有进入 `spec / compiler / runtime consumption` 的下一阶段
- 还不值得引入更强的 DDD-heavy 分层

也就是说，当前正确方向仍然是：

- 继续模块化
- 继续收紧边界
- 逐步向 authoring spec 演化

而不是突然升级成重领域模型。

## 下一步建议

如果继续沿着这条文档推进，下一步最值得做的是：

1. 把“编辑器模型 -> override payload”再向 “编辑器 spec -> 编译后配置” 推进一步
2. 逐步把 `BackgroundV2` / flame overlay 的编辑数据从 override 语义提升成更明确的 authoring spec
3. 在不动 runtime primitive 的前提下，继续清理 `CampaignView` 周边兼容 seam
4. 随着视觉 authoring 增长，再考虑 `EffectSpec / OverlaySpec / PostProcessSpec`

## 完成定义

可以认为这轮 V1 重构已经进入“已落地、可继续迭代”的状态，当下列事实同时成立时：

- `run_ui_editor.py` 是薄入口
- `editor_app.py` 也是薄壳，而不是新的巨型文件
- tree、model、commands、builder、layout_ui、rendering、loop、store 都有明确归属
- `ui_runtime/ui_node.py` 仍然保持小而纯
- override 持久化已归位到 `infrastructure`
- 聚焦测试能够保护主要边界
- 新协作者不需要读完整个编辑器实现，就能判断一个改动应该放在哪里

## Last Updated

- `2026-04-02`
