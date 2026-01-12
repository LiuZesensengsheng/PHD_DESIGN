## 架构边界契约（DDD·独游务实版）

> 目的：让“UI / Services / Domain / Infrastructure”的边界一眼就能裁判，减少返工与隐式耦合。

### 核心规则（依赖只能向内）

- **Domain（领域层）**：`contexts/*/domain/**`
  - **允许依赖**：`shared_kernel`、`contexts/shared/domain`、Python 标准库（纯）
  - **禁止依赖**：`pygame/pygame_gui`、`contexts/*/ui`、`contexts/*/rendering`、`contexts/*/mvc`、`contexts/*/infrastructure`、文件/网络IO（除非通过注入的接口）
  - **职责**：规则、实体/值对象、领域事件、纯算法；尽量可单测、可 headless 运行

- **Services（应用层 / 用例层）**：`contexts/*/services/**`
  - **允许依赖**：本 context 的 `domain`；以及“端口接口”（repo/presenter等 Protocol）
  - **禁止依赖**：直接 import UI/pygame；直接 `new` 具体基础设施实现（如 JsonRepo）
  - **职责**：用例编排、流程状态机、把领域结果组织成可展示的纯数据（ViewModel/DTO）

- **UI / Presentation（展示层）**：`contexts/*/ui/**`、`contexts/*/rendering/**`、`contexts/*/mvc/**`
  - **允许依赖**：Services（调用用例/提交选择）、UI 框架（pygame）
  - **禁止做**：写业务规则/结算；绕过 Services 直接修改 Domain 深层状态
  - **职责**：渲染、输入事件、把点击/按键翻译成“命令/选择”交给 Services

- **Infrastructure（基础设施层）**：`contexts/*/infrastructure/**`、`infrastructure/**`
  - **允许依赖**：Domain（类型/接口）与标准库；第三方库（IO/资源）
  - **职责**：JSON/存档/资源加载/Repo 实现/适配器

### Cross-Context 规则（限界上下文）

- **禁止**：`contexts.A` 直接 import `contexts.B` 的内部模块（除 `contexts.shared` 外）。
- **允许**：通过 `shared_kernel` 或显式契约（DTO/Protocol/DomainEvent）沟通。

### PR/提交前自检（5秒版）

- Domain 文件里是否出现了：`pygame` / `ui` / `rendering` / `mvc` / `infrastructure` import？
- Service 是否在直接处理 pygame event/创建 UI 控件？
- Service 是否在 `new JsonXXXRepository()`（应改为注入接口）？
- shared/kernel 是否反向依赖具体 context？


