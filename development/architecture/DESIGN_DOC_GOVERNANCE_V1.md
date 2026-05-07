# 设计文档治理 V1

## 目标

让游戏设计文档能被人类和 AI 稳定使用，核心是把“可信程度”和“当前权威”写清楚。

任何设计文档在被拿来指导实现前，都应该能快速回答：

1. 现在应该相信哪一份文档？
2. 哪些只是参考、草稿或未来想法？
3. 哪些已经被替代或只保留历史价值？

## 范围

本规则适用于 `docs/design/` 下的设计资料，包括 Markdown 规格、矩阵、CSV/XLSX 规划表、设计图片、导出包和归档说明。

本规则不直接决定玩法内容，只管理设计文档如何声明状态、负责人、适用范围和 source of truth 关系。

## 核心规则

### 1. 每个高流量区域尽量只有一份 canonical active doc

高流量区域包括：

- 核心循环
- 战役结构
- 卡牌设计
- 敌人设计
- 事件设计

如果同一区域存在多份文档，旧文档或局部文档应该标为 `Reference`、`Draft`、`Future`、`Archived` 或 `Superseded`，不要默认把它们都当成同等权威。

### 2. 文档状态必须显式

推荐状态：

- `Draft`：探索草稿，不能直接作为实现权威
- `Active`：当前可引用的设计依据
- `Frozen`：已接受且稳定，但暂不主动编辑
- `Superseded`：已被新文档替代
- `Future`：未来可能方向
- `Archived`：历史记录

### 3. 新文档尽量补状态卡

推荐状态卡：

```md
- Status: Draft | Active | Frozen | Superseded | Future | Archived
- Owner: <name>
- Scope: <system/content/feature>
- Canonical: Yes/No
- Supersedes: <old doc or none>
- Superseded By: <new doc or none>
- Implemented In: <code/data/doc path or none>
- Last Reviewed: YYYY-MM-DD
```

`Canonical: Yes` 应该很少。如果两份 canonical 文档互相冲突，先解决 source of truth，再做实现。

### 4. 重大决定仍写入 decision log

设计文档可以解释方向，但只要改变项目方向、工作流、回滚路径或实现边界，就应该在 `docs/pm/DECISION_LOG.md` 记录决策。

### 5. Future 和 Archive 不是默认读取面

`Future` 与 `Archived` 文档默认不参与 AI 恢复和实现判断，除非任务明确要求读取它们。

这样做是为了避免旧想法或未来想法悄悄覆盖当前设计。

### 6. 数据表默认只是支撑材料

`.csv`、`.xlsx`、matrix、budget、catalog 等文件默认是 reference 或 working sheet。

如果某个表格成为权威来源，需要由 active spec 明确链接，并说明可信列、可信页签或可信字段。

### 7. 文件名不能决定权威

不要因为文件名包含 `FINAL`、`new`、`latest`、`v8_FINAL` 就默认它可信。

权威来自：

- active 索引
- 状态卡
- supersede 链接
- 必要时的 decision log
- 已实现代码、数据或测试引用

## 文档角色

`docs/design/` 使用这些角色：

1. `North Star`
2. `Active Spec`
3. `Reference`
4. `Draft`
5. `Future`
6. `Archive`

面向读者的入口是 `docs/design/README.md`。

## 使用前检查清单

把一份设计文档作为实现依据前，检查：

1. 它有没有状态？
2. 它是不是该区域的 canonical 文档？
3. 它是否替代了旧文档，或已经被新文档替代？
4. 它是否和当前代码、数据、测试冲突？
5. 这个变化是否应该同步写入 `docs/pm/DECISION_LOG.md`？

## 迁移策略

不要一次性清理整个 `docs/design/`。

推荐顺序：

1. 先维护 `docs/design/README.md`。
2. 选择 2-3 个高流量区域做试点。
3. 每个试点先标出一份 canonical active doc。
4. 把明显旧的文档标为 `Reference`、`Future`、`Superseded` 或 `Archived`。
5. 等状态和链接清楚后，再考虑移动文件。

初始试点候选：

- `ideal/`
- `campaign/`
- `enemydesigon/`

## Source Of Truth 边界

- `docs/design/` 负责设计说明、设计状态和设计入口。
- `docs/development/` 负责长期架构和工作流规则。
- `docs/pm/DECISION_LOG.md` 负责已接受决策、取舍和回滚说明。
- `docs/logs/daily/` 负责短期进展和交接。
- 真实 shipped behavior 仍以代码、正式数据和测试为准。

如果这些来源互相冲突，不要静默拼接，先记录冲突并确认 owner。

## 非目标

- 不在治理初始化时重写所有设计内容。
- 不通过移动文件把 draft 偷偷升级为实现权威。
- 不把 `Future` 或 `Archive` 放进默认恢复面。
- 不用本规则直接修改 runtime 行为或正式数据。
