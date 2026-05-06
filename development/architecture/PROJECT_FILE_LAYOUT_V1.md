# 项目文件布局 V1

## 目标

定义项目长期稳定的文件布局，用于约束：

- 运行时资源放哪里
- 外部美术源文件放哪里
- `contexts/shared/` 应该怎么分
- 测试应该放哪里
- 人工临时区和程序临时区如何区分

这份文档是：

- 目标终态
- 渐进迁移规则

不是要求现在一次性重命名整个仓库。

## 范围

本文档覆盖：

- 仓库根目录布局
- 运行时资源目录
- 仓库外部美术源文件目录
- 共享代码边界
- 顶层测试目录
- `scratch/` 与 `tmp/` 的语义

本文档不覆盖：

- 具体 gameplay 架构细节
- 卡牌/事件/战斗数据 schema
- 某个 renderer 的内部实现

## 核心结论

### 0. 采用 Unreal-inspired 的内容治理，不照搬 Unreal 引擎架构

本项目确定采用的是：

- Unreal 风格的内容目录治理
- runtime asset 与 source art 分离
- manifest / registry 驱动的资源引用
- editor/source 与 runtime/export 分层

但不采用完整 Unreal 架构作为代码模型。

也就是说：

- 不引入 UObject / Actor / Component 式通用对象模型
- 不把业务规则迁进场景对象或视觉节点
- 不改变当前“pygame 内部 Godot 化 + DDD/orchestration 边界”的长期方向

这份文件只冻结文件布局、资产来源、共享代码和测试目录的长期规则。

### 1. 运行时资源保留在 Git 仓库内

Git 仓库里只保留游戏运行时真正读取的资源，例如：

- 导出的 PNG/JPG/WebP
- 已批准音频文件
- 字体
- shader
- manifest

这些文件统一放在 `assets/` 下。

运行时不应依赖 PSD/KRA/CLIP/ASE 这类源文件。

### 2. 美术源文件放在 Git 仓库外部

可编辑的大型美术源文件应放在仓库外部的同级目录，由团队外部同步/版本工具管理，例如坚果云。

推荐本地目录：

```text
<workspace>/
├─ PHD_SIMULATER/
└─ PHD_SIMULATER_ART/
```

`PHD_SIMULATER_ART/` 不属于 Git 仓库。

不要把它放进仓库里再靠 `.gitignore` 隐藏，那个只能作为过渡方案，不能作为长期终态。

### 3. 运行时只读 manifest 和稳定路径，不读“目录里最新版本”

运行时应该读取：

- 稳定的导出路径
- manifest 注册信息

不要实现下面这种运行时逻辑：

- 扫目录
- 找版本号
- 取最大版本

因为这种做法会让构建不可复现，也会让未审核的资源直接漏进游戏。

### 4. `contexts/shared/` 只放共享代码，不放真实媒体资源

`contexts/shared/` 的长期职责应该是：

- 共享 domain 代码
- 共享 service 代码
- 共享 adapter / infrastructure 代码

不应该继续作为：

- 真实图片目录
- 真实音频目录

真实媒体资源应统一归位到 `assets/`。

### 5. `window` 不是 UI 资源总类

`window` 只是界面资源中的一个子类。

因此约定：

- `interface/` 作为界面资源总类
- `windows/` 只表示弹窗、面板、窗口类资源

不要用 `window/` 作为全部 UI 资源的顶层目录名。

### 6. `tmp/` 和人工临时区不是一回事

- `tmp/`：程序生成的临时输出，可随时删除
- `scratch/`：人工临时区，放截图、参考、试验、草稿

因此：

- `linshi/` 应该长期收口到 `scratch/`
- 不应该并入 `tmp/`

### 7. 测试继续放在仓库顶层

测试保持在顶层 `tests/` 目录下。

不要把测试拆进 `contexts/*` 里做 colocated test。

### 8. `skills/` 是可选层，不属于运行时架构

如果项目保留 `skills/`，它的职责只能是：

- AI 可复用工作流
- AI 方法说明

不能承载：

- 当前项目状态
- 长期架构 source of truth
- 运行时内容
- 资产管线配置

如果这些 skill 不再有实际价值，可以删除，不影响主架构。

## 目标终态目录

```text
PHD_SIMULATER/
├─ assets/
│  ├─ interface/
│  │  ├─ screens/
│  │  │  ├─ campaign/
│  │  │  ├─ combat/
│  │  │  ├─ dialogue/
│  │  │  └─ main_menu/
│  │  ├─ hud/
│  │  ├─ windows/
│  │  ├─ buttons/
│  │  ├─ icons/
│  │  ├─ cards/
│  │  └─ common/
│  ├─ audio/
│  │  ├─ bgm/
│  │  └─ sfx/
│  ├─ fonts/
│  ├─ shaders/
│  └─ manifests/
│     ├─ assets.json
│     ├─ audio_manifest.json
│     └─ art_manifest.json
│
├─ data/
│  ├─ cards/
│  ├─ combat/
│  ├─ events_drafts/
│  ├─ narrative_src/
│  └─ questlines/
│
├─ contexts/
│  ├─ campaign/
│  │  ├─ domain/
│  │  ├─ services/
│  │  ├─ infrastructure/
│  │  ├─ ui/
│  │  ├─ ui_runtime/
│  │  ├─ rendering/
│  │  └─ ui_editor/
│  ├─ combat/
│  │  ├─ domain/
│  │  ├─ services/
│  │  ├─ infrastructure/
│  │  ├─ mvc/
│  │  └─ rendering/
│  ├─ dialogue/
│  ├─ event/
│  ├─ main_menu/
│  ├─ loading/
│  ├─ deck/
│  └─ shared/
│     ├─ domain/
│     ├─ ui/
│     ├─ assets/
│     │  ├─ application/
│     │  └─ infrastructure/
│     ├─ audio/
│     │  ├─ application/
│     │  └─ infrastructure/
│     ├─ save/
│     │  ├─ application/
│     │  ├─ infrastructure/
│     │  └─ contracts/
│     ├─ config/
│     ├─ logging/
│     └─ repro/
│
├─ docs/
│  ├─ development/
│  ├─ art/
│  ├─ design/
│  ├─ pm/
│  └─ logs/
│
├─ scripts/
├─ tools/
├─ tests/
│  ├─ campaign/
│  ├─ combat/
│  ├─ shared/
│  ├─ save/
│  ├─ scripts/
│  ├─ toolkit/
│  └─ simulation/
│
├─ scratch/
├─ tmp/
└─ skills/   # 可选
```

## 外部美术源文件目录

推荐的外部源文件目录：

```text
PHD_SIMULATER_ART/
├─ interface/
│  ├─ screens/
│  ├─ hud/
│  ├─ windows/
│  ├─ buttons/
│  ├─ icons/
│  ├─ cards/
│  └─ common/
├─ characters/
├─ cards/
├─ audio_src/
└─ archive/
```

这个目录用于放：

- PSD/KRA/CLIP/ASE 源文件
- 原始分层工程
- 美术迭代历史
- 原始音频工程或分轨

这个目录不会在游戏启动时被直接读取。

## 运行时资源契约

Git 仓库里只保留批准后的运行时导出结果。

示例：

```text
PHD_SIMULATER_ART/interface/screens/campaign/bg_desktop/
├─ bg_desktop_v000011.psd
├─ bg_desktop_v000012.psd
└─ bg_desktop_v000013.psd

PHD_SIMULATER/assets/interface/screens/campaign/bg_desktop.png
```

manifest 示例：

```json
{
  "interface.campaign.screen.bg_desktop": {
    "source_ref": "interface/screens/campaign/bg_desktop/bg_desktop_v000012.psd",
    "runtime_path": "assets/interface/screens/campaign/bg_desktop.png",
    "status": "approved"
  }
}
```

规则：

- `source_ref` 指向外部美术目录中的逻辑路径
- `runtime_path` 指向仓库里的运行时文件
- 运行时只读取 `runtime_path`
- 工具链或审查流程才会去查看 `source_ref`

## `contexts/shared/` 的布局规则

长期不建议继续保持这种混合结构：

```text
contexts/shared/
├─ infrastructure/assets/
├─ audio/
└─ save/
```

因为这里混了两种维度：

- `audio/` 和 `save/` 是“子系统维度”
- `infrastructure/assets/` 是“分层维度”

读起来会很别扭，也不利于后续扩展。

目标形态应该是“子系统优先”：

```text
contexts/shared/
├─ assets/
│  ├─ application/
│  └─ infrastructure/
├─ audio/
│  ├─ application/
│  └─ infrastructure/
└─ save/
   ├─ application/
   ├─ infrastructure/
   └─ contracts/
```

这样做的好处：

- 共享代码按真实子系统聚合
- 每个子系统内部再表达层次
- 后续迁移更小、更清楚

## 当前目录到目标目录的映射

### 界面资源

- 当前：`assets/ui/**`
- 目标：`assets/interface/**`

### 共享媒体资源

- 当前：`contexts/shared/audio/music/**`
- 目标：`assets/audio/**`

### 共享资源代码

- 当前：`contexts/shared/infrastructure/assets/**`
- 目标：`contexts/shared/assets/infrastructure/**`

### 共享存档代码

- 当前：`contexts/shared/save/*.py`
- 目标：`contexts/shared/save/{application,infrastructure,contracts}/`

### 人工临时区

- 当前：`linshi/`
- 目标：`scratch/`

## 迁移规则

### Phase 1：先冻结新漂移

从现在开始对新内容执行：

- 新运行时美术资源放 `assets/`
- 新源美术文件放外部 `PHD_SIMULATER_ART/`
- 新人工临时文件放 `scratch/`
- 新脚本输出放 `tmp/`

不要继续把新资源塞进 `contexts/shared/audio/` 这类代码路径。

### Phase 2：引入 manifest 和稳定路径

- 保持运行时读取稳定文件路径
- 用 manifest 把运行时资源和批准源文件关联起来
- 不允许运行时做版本扫描和“取最大版本”

### Phase 3：把真实媒体资源迁出 `contexts/shared/`

- 把真实音频迁到 `assets/audio/`
- 保留音频 adapter 代码在 `contexts/shared/`
- 更新 manifest 和 loader

### Phase 4：把 `shared` 内部收口成子系统结构

- 共享资源代码迁到 `shared/assets/`
- 共享音频代码迁到 `shared/audio/application|infrastructure`
- 共享存档代码迁到 `shared/save/application|infrastructure|contracts`

### Phase 5：把 `linshi/` 改名为 `scratch/`

- 可以有一个短期兼容窗口
- 等脚本和团队习惯稳定后删除旧名字

## 非目标

- 不是一次性全仓重命名
- 不是让运行时直接依赖坚果云路径
- 不是实现目录里自动取最新版本
- 不是现在就强行把所有 `ui/` 代码改成新命名

## 最终总结

1. Git 仓库存放：运行时资源、代码、数据、文档、测试。
2. 外部美术仓库存放：源文件和版本历史。
3. 运行时只读批准后的导出资源和 manifest。
4. `contexts/shared/` 只放共享代码，不放大媒体文件。
5. `scratch/` 和 `tmp/` 必须保持分离。
6. `window` 是子类，不是顶层资源类别。
