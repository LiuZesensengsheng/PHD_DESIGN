# UI 架构原则 v1

> 目标：为 `Campaign` 及后续 UI 重构提供统一约束，让“不懂前端的人 + AI + 一般前端协作者”也能稳定维护。

## 1. 设计目标

当前 UI 架构的首要目标不是“前端优雅”，而是：

1. 可维护
2. AI 友好
3. 可持续扩内容
4. 低耦合、高内聚
5. 不依赖个人前端经验

这意味着本项目的 UI 层应优先选择“笨但稳”的结构，而不是复杂抽象。

## 2. 核心原则

### 2.1 View 要薄

`View` 只负责：

- 创建控件
- 更新显示
- 绘制画面
- 提供命中区域、坐标换算、只读渲染辅助

`View` 不负责：

- 业务判断
- 状态切换
- 输入锁策略
- reward / meeting / ending 之类流程编排

一句话：`View` 是表现层，不是业务层。

### 2.2 State 是 UI 宿主，不是业务垃圾堆

`CampaignState` 允许负责：

- UI 生命周期入口
- 事件总分发
- 持有 `view`、`choice_modal`、`judgment_modal`、gossip UI 宿主对象
- 调用 service，而不是深入实现细节

`CampaignState` 不应继续承担：

- 大段 startup 业务编排
- 大段 transition 组装
- modal 锁状态的散装写入
- gossip / meeting / reward 的细节流程

一句话：`State` 是宿主，不是超级节点。

### 2.3 Service 负责 UI 相关业务编排

对于 UI 相关但不属于纯显示的逻辑，放进 service：

- 是否该显示某个 prompt
- 是否该打开某个 modal
- startup 时需要施加哪些 UI 相关副作用
- 输入锁和 owner 语义
- gossip / meeting / reward 的流程编排

service 可以依赖 state 的稳定表面能力，但不应直接扩散到渲染细节。

### 2.4 生命周期必须显式

所有 UI 宿主对象都应尽量有清晰生命周期：

- `bootstrap`
- `show`
- `hide`
- `cleanup`
- `lock`
- `unlock`

不允许把这些动作散落在多个 handler、多个 callback、多个 if 分支里而没有统一规则。

### 2.5 Modal 必须遵守一套锁规则

所有 modal / prompt / 阻塞窗口必须遵守统一契约：

- show 时如何加锁
- hide 时如何解锁
- owner 如何标识
- 谁能释放谁的锁
- modal 消费事件后，底层 handler 必须停止

不允许不同 modal 各自发明不同的锁语义。

### 2.6 测试先于 UI 重构

没有测试边界，不允许动 UI 结构。

优先要补的测试类型：

- 生命周期测试
- 输入锁测试
- modal 事件消费顺序测试
- UI 状态与业务判断分离测试

## 3. 当前推荐职责边界

### 3.1 `CampaignState`

保留：

- startup / cleanup 主入口
- `handle_event` / `update` / `draw` 总分发
- 持有 `view`、`choice_modal`、`judgment_modal`、gossip UI 宿主对象
- 调用 service，不直接深入实现细节

逐步移出：

- meeting prompt UI 生命周期
- gossip bootstrap / cleanup
- modal lock / show / hide 统一策略
- 与 startup 强绑定的 UI 业务副作用

### 3.2 `CampaignView`

保留：

- UI 创建
- 资源读取与缓存
- 画面绘制
- 坐标 / block rect / 渲染辅助

当前阶段不优先重构 `CampaignView`。

原因：

- 当前主问题不是视觉表现，而是 UI 宿主层边界不清
- 先动 `CampaignView` 风险大，收益不如先收 lifecycle / lock

### 3.3 UI 相关 Service

推荐继续演进出的 service：

- `MeetingPromptUiService`
- `GossipUiLifecycleService`
- `ModalLockCoordinator` 或同类统一协调器

这些 service 的目标不是替代 `View`，而是把 UI 生命周期和业务判断从 `CampaignState` 里拿出来。

## 4. 当前阶段的重构优先级

按推荐顺序执行：

1. `meeting prompt` UI 生命周期
2. `gossip` bootstrap / cleanup
3. modal 的 `show/hide/input-lock` 统一
4. UI 显示状态和业务判断进一步分开
5. 最后才考虑是否继续拆 `CampaignView`

当前不建议优先做：

- 视觉重构
- 渲染管线大改
- 组件系统重写
- 复杂前端模式（MVVM、事件总线泛化、过度组件化）

## 5. 当前测试护栏情况

### 5.1 已有护栏

目前已经补上的边界主要有：

- `meeting prompt` 生命周期
  - startup 只创建一次
  - close / enter 后 prompt 清理与解锁
- `modal_dispatch` / `input_lock` 事件消费顺序
- reward-style modal 的基础锁语义
- gossip lock 的基本解锁语义
- gossip UI shell 的基础 startup / cleanup 安全性
- UI 状态与业务判断的最小契约边界

对应测试文件：

- `tests/campaign/test_meeting_prompt_ui_lifecycle.py`
- `tests/campaign/test_campaign_state_modal_event_consumption.py`
- `tests/campaign/test_campaign_modal_lock_contract.py`
- `tests/campaign/test_gossip_ui_lifecycle.py`
- `tests/campaign/test_gossip_flow_app_service.py`
- `tests/campaign/test_campaign_ui_state_contracts.py`

### 5.2 仍然缺的护栏

当前还建议继续补：

1. `cleanup` 后 UI 引用残留的更细断言
   - 例如 gossip button / badge / modal 引用是否应显式置空
2. `owner` 语义更严格的统一契约
   - 当前已有基础测试，但还没有覆盖所有 modal / prompt 组合
3. startup 失败场景的更细粒度护栏
   - 例如 view 初始化成功但局部 UI bootstrap 失败时，残留对象的精确边界
4. `CampaignView` 级别的显示契约测试
   - 不是视觉快照，而是更细的 `show/hide/update` 行为边界

结论：测试护栏已经足够支持开始做 UI 生命周期和 lock 统一类重构，但还不足以安全推进 `CampaignView` 级别的大拆。

## 6. 面向 AI 协作的附加规则

为了让 AI 能稳定参与前端 / UI 改动，后续改动应尽量满足：

1. 一个文件只承担一类职责
2. show / hide / cleanup 入口显式存在
3. 锁状态和 owner 可断言
4. UI 显示判断可以脱离真实控件单测
5. 不把业务判断藏进 view callback

一句话：对 AI 友好的 UI 架构，不是更聪明，而是更明确。

## 7. 当前结论

本项目 UI 的正确演进方向不是“更像前端框架”，而是：

- `薄 View`
- `薄 State`
- `显式生命周期`
- `统一锁契约`
- `测试先行`

这就是当前阶段 UI 架构的主设计思想。
