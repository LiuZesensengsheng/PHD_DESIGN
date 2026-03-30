# Campaign UI 编辑器重构计划 V1

## 目标

把当前的 UI 编辑器实现整理成一种更适合长期迭代的结构，使它具备：

- 按职责做物理隔离
- 对人和 AI 都更容易安全阅读
- 在模块边界上可测试
- 能支撑后续持续演化

这份计划只针对 `run_ui_editor.py` 这条工具链及其关联的节点树 / 编辑器逻辑。

它不是一份 DDD 重写计划。

## 当前问题

当前编辑器路径是可用的，但文件组织方式不适合继续长期生长。

主要问题：

- `run_ui_editor.py` 把编辑器数据模型、树投影、预览几何、素材组装、保存逻辑、pygame 事件循环都混在一个文件里
- `EditableLayer` 目前同时混合了运行时节点数据、编辑器元数据和序列化行为
- 树分组和排序策略直接写在主编辑器脚本内部
- override 的读取 / 保存放在 `ui_runtime/phone_widget_store.py`，当前已经是误导性的归属位置
- campaign view / rendering 里仍有运行时兼容 seam，会让人误判当前真正活跃的实现路径

当前的大文件热点：

- `run_ui_editor.py`
- `contexts/campaign/view.py`
- `contexts/campaign/state.py`

这份计划只直接处理第一个热点。

## 重构原则

1. 先按职责拆分，再考虑是否需要新抽象。
2. 优先做保持行为不变的提取，不先做重新设计。
3. 保持 runtime node primitive 简单，不和编辑器逻辑混住。
4. 先把纯逻辑挪到纯模块里。
5. 先围住测试边界，再改行为。
6. 只有当编辑器规则真的长出明显领域复杂度时，才考虑更重的 DDD 分层。

## 非目标

- 不做一次性 UI 重写
- 不做引擎级通用 scene graph
- 不在这轮里重写 `CampaignView` 或 `CampaignState`
- 不把编辑器树逻辑做成完整 DDD
- 不把兼容 seam 清理和本轮提取工作混在同一个 cut 里

## 当前源码分布

当前编辑器流程主要集中在：

- `run_ui_editor.py`
- `contexts/campaign/ui_runtime/ui_node.py`
- `contexts/campaign/ui_runtime/phone_widget_store.py`

当前运行时兼容 seam 主要出现在：

- `contexts/campaign/view.py`
- `contexts/campaign/rendering/background_stage.py`

## 目标模块结构

建议的新结构：

- `run_ui_editor.py`
  - 只保留薄入口
- `contexts/campaign/ui_editor/__init__.py`
- `contexts/campaign/ui_editor/constants.py`
- `contexts/campaign/ui_editor/preview_layout.py`
- `contexts/campaign/ui_editor/editor_models.py`
- `contexts/campaign/ui_editor/tree_projection.py`
- `contexts/campaign/ui_editor/editor_commands.py`
- `contexts/campaign/ui_editor/background_entry_builder.py`
- `contexts/campaign/ui_editor/session_state.py`
- `contexts/campaign/ui_editor/editor_app.py`
- `contexts/campaign/infrastructure/ui_editor_override_store.py`

应该继续留在原位置的文件：

- `contexts/campaign/ui_runtime/ui_node.py`
  - 继续作为 runtime primitive 保持小而稳定

迁移期间需要暂时保留的兼容壳：

- `contexts/campaign/ui_runtime/phone_widget_store.py`
  - 在迁移阶段可转发到 `contexts/campaign/infrastructure/ui_editor_override_store.py`

## 文件级迁移计划

### 1. `contexts/campaign/ui_editor/constants.py`

把编辑器专用常量从 `run_ui_editor.py` 拆出来。

预期内容：

- 窗口尺寸
- 面板宽度
- 列表行高
- 缩放上下限
- 编辑器颜色
- 编辑器专用标签或排序常量

从 `run_ui_editor.py` 迁出的候选项：

- `WINDOW_SIZE`
- `MIN_WINDOW_SIZE`
- `LEFT_PANEL_W`
- `RIGHT_PANEL_W`
- `NODE_ROW_HEIGHT`
- 各种 zoom 常量
- preview UI 尺寸常量

原因：

- 把稳定配置从逻辑里分离出来
- 让硬编码值更容易查看、比较和测试审查

### 2. `contexts/campaign/ui_editor/preview_layout.py`

抽出预览区域几何和坐标换算辅助函数。

预期内容：

- `PreviewLayout`
- `fit_size_preserve_aspect(...)`
- `build_preview_layout(...)`
- `get_preview_display_rect(...)`
- `clamp_preview_zoom(...)`
- `get_preview_source_rect(...)`
- `map_display_to_preview_point(...)`
- `get_zoomed_preview_center(...)`
- `get_preview_zoom_ui_rects(...)`
- `build_preview_rect(...)`

原因：

- 这部分大多是纯数学逻辑
- 不应该待在 pygame 主循环里
- 很适合做独立单测

### 3. `contexts/campaign/ui_editor/editor_models.py`

抽出编辑器数据结构。

预期内容：

- `EditableLayer`
- payload 序列化辅助逻辑

保留在该文件中的行为：

- `EditableLayer.build_payload(...)`

原因：

- 编辑器需要一个稳定、可命名的数据模型边界
- 序列化行为应该跟着编辑器模型走，而不是留在主脚本里

重要规则：

- `EditableLayer` 可以引用 `ImageNode`
- 但它不能继续长出 campaign 业务规则

### 4. `contexts/campaign/ui_editor/tree_projection.py`

把树构建逻辑抽成一个投影模块。

预期内容：

- `EditorTreeGroup`
- `EditorTreeRow`
- `get_background_tree_group_parts(...)`
- `get_tree_leaf_label(...)`
- `build_editor_tree_rows(...)`
- `get_tree_group_ids_for_node(...)`
- `expand_tree_groups_for_node(...)`
- `find_tree_row_index_for_node(...)`

原因：

- 树分组本质上是 projection 问题，不是 runtime node 问题
- 它应该能在不启动整个编辑器的情况下被测试
- 这里是最适合整理成 AI 友好纯逻辑模块的区域之一

### 5. `contexts/campaign/ui_editor/editor_commands.py`

抽出那些会变更或解析编辑器状态的动作函数。

预期内容：

- `get_entry_for_node(...)`
- `resolve_drag_target(...)`
- `reorder_background_entries(...)`

后续可增长的内容：

- 可见性切换命令
- 尺寸调整命令
- 选择辅助逻辑
- 将来如果需要，也可承接 undo/redo 的命令包装

原因：

- 变更动作不应该继续埋在主脚本内部
- 这会形成编辑器第一层比较清楚的应用式 seam，而不需要直接上 DDD

### 6. `contexts/campaign/ui_editor/background_entry_builder.py`

抽出背景层构建和素材到 entry 的组装逻辑。

预期内容：

- `_load_image(...)`
- `_scale_surface(...)`
- `_darken_surface_mul(...)`
- `_background_darken_for(...)`
- `_make_layer_node(...)`
- `_background_path(...)`
- `_get_runtime_preview_offset_scale(...)`
- `_build_background_base_entries(...)`
- `build_background_entries(...)`

原因：

- 它和树投影、编辑器交互是不同责任
- 它是 layout -> entry 组装逻辑的自然归属位置
- 可以把素材 / 配置解释从事件循环中隔离出来

### 7. `contexts/campaign/ui_editor/session_state.py`

给编辑器的临时运行状态一个明确归属，而不是继续散成 `main()` 里的很多局部变量。

预期内容：

- 当前选中的 node
- 拖拽状态
- 滚动位置
- collapsed group ids
- debug overlay 开关
- zoom 状态
- pan 状态
- 当前输入框状态
- 状态栏提示文字

建议形态：

- `EditorSessionState` dataclass

原因：

- 当前局部状态太散，主循环很难读
- 显式 session state 会明显提升可读性和可测试性

### 8. `contexts/campaign/ui_editor/editor_app.py`

抽出那些不适合直接放在入口脚本里的高层编辑器编排逻辑。

预期内容：

- 窗口重建编排
- 保存编排
- 选择同步
- 顶层事件处理辅助

从 `run_ui_editor.py` 迁出的候选项：

- `save_editor_layout(...)`
- `rebuild_window_state(...)`
- 其他围绕编辑器 session 的非渲染编排函数

原因：

- `run_ui_editor.py` 应该逐步收缩成一个薄启动壳
- 编排逻辑应该能在不扫完整个渲染 / 数学 helper 的情况下被读懂

### 9. `contexts/campaign/infrastructure/ui_editor_override_store.py`

新建一个命名准确的 override 持久化适配器。

预期内容：

- `load_ui_editor_overrides(...)`
- `load_background_v2_overrides(...)`
- `load_flame_overlay_overrides(...)`
- `save_background_v2_overrides(...)`
- `save_flame_overlay_overrides(...)`
- `get_ui_editor_overrides_mtime(...)`

迁移规则：

- 暂时保留 `contexts/campaign/ui_runtime/phone_widget_store.py`
- 在迁移阶段让它成为转发层，直到 imports 清理完成

原因：

- 当前文件名暗示的是 runtime widget 归属
- 但它实际承担的是编辑器 override 持久化
- 更适合放在 infrastructure 或 editor adapter 层

### 10. `run_ui_editor.py`

把它收缩成一个薄可执行入口。

目标职责仅保留：

- pygame 初始化
- display / bootstrap
- 实例化 editor app / session
- 跑主循环
- 把 event / update / render 委托给拆出的模块

应该从这个文件移走的内容：

- 树投影细节
- payload 组装细节
- 背景层构建细节
- 保存 / store 细节
- 大多数编辑器状态簿记逻辑

## 保留 / 不要移动的部分

### 保持 `contexts/campaign/ui_runtime/ui_node.py` 小而纯

这个文件当前状态是健康的，应该继续维持成 runtime primitive 层。

它应该继续只负责：

- parent / child 结构
- visible
- 事件遍历
- 绘制遍历
- global rect / position 辅助

它不应该吸收：

- 编辑器持久化
- campaign 业务逻辑
- 编辑器树分组策略
- save schema 逻辑

### 提取过程中保持兼容 seam 稳定

不要把本轮编辑器提取和下列兼容 seam 清理混在一起：

- `CampaignView.handle_runtime_ui_event(...)`
- `CampaignView.update_runtime_ui(...)`
- `CampaignView.render_runtime_ui(...)`
- `background_stage.py` 里的兼容调用

那部分应该作为后续单独一轮清理。

## 测试计划

### 现有需要保住的测试

- `tests/campaign/test_ui_editor_tree_rows.py`
- `tests/campaign/test_ui_editor_background_overrides.py`
- `tests/campaign/test_background_v2_layer_manifest.py`
- `tests/campaign/test_campaign_runtime_ui_boundary_contract.py`

### 提取过程中要新增的测试

- `tests/campaign/test_ui_editor_preview_layout.py`
  - 校验预览几何和坐标映射
- `tests/campaign/test_ui_editor_payload_contract.py`
  - 校验 `EditableLayer.build_payload(...)` 的行为和边界条件
- `tests/campaign/test_ui_editor_commands.py`
  - 校验重排和 node-to-entry 解析行为
- `tests/campaign/test_ui_editor_override_store.py`
  - 校验 load / save / mtime 适配器行为

### 测试策略规则

每一步提取都遵守：

1. 一次只移动一类责任
2. 保持行为稳定
3. 补或调整聚焦测试
4. 然后再继续下一步

不要把多个行为变化打包到同一个提取 cut 里。

## 迁移顺序

建议顺序：

1. 新建 `ui_editor` 包
2. 先移动纯常量和预览数学
3. 再移动树投影
4. 再移动编辑器模型
5. 再移动编辑器命令
6. 再移动背景 entry builder
7. 新增 infrastructure override store，并保留临时兼容转发层
8. 引入显式 session state
9. 把 `run_ui_editor.py` 收缩成薄入口 / orchestration
10. 最后单独做兼容 seam 清理

## 分阶段闸门

### Phase 1：纯提取

目标：

- 提取常量
- 提取预览数学
- 提取树投影

退出条件：

- 编辑器仍能运行
- 树相关测试仍通过

### Phase 2：编辑器模型与命令边界

目标：

- 稳定 `EditableLayer`
- 隔离重排和选择辅助逻辑

退出条件：

- payload 和 reorder 测试已经存在
- 保存输出没有行为变化

### Phase 3：builder 与 store 隔离

目标：

- 隔离素材组装逻辑
- 把持久化归属改成准确命名

退出条件：

- builder 测试和 store 测试通过
- `run_ui_editor.py` 不再承担素材 / 配置解释细节

### Phase 4：薄入口

目标：

- 把 `run_ui_editor.py` 收缩成一个可读的壳

退出条件：

- 新协作者在 1 分钟内能定位 tree、state、builder、store 分别在哪个文件

## 未来何时才值得引入更强 DDD

不要把这条编辑器路径升级成 DDD-heavy 结构，除非以下大多数条件同时出现：

- 编辑器需要 undo/redo 和命令历史
- 编辑器出现超出文件 / 文件夹投影之外的可复用约束与不变量
- 同一套编辑器模型要被多个工具共享
- 保存格式需要明确的版本迁移策略
- 编辑器动作开始具备明显的业务语义，而不只是 UI 操作

在那之前，正确方向是模块化，不是 DDD 化。

## 完成定义

当满足以下条件时，可以认为这轮重构成功：

- `run_ui_editor.py` 不再是混合巨型文件，而是薄入口
- editor tree、model、commands、builder、store 都有明确的模块归属
- runtime node primitive 仍然隔离在 `ui_runtime/ui_node.py`
- override 持久化不再看起来属于 phone widget runtime 代码
- 聚焦测试保护住每个提取边界
- 新协作者不需要读完整个编辑器实现，就能判断一个安全改动该落在哪
