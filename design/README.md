# 设计文档入口

## 目的

`docs/design/` 存放游戏设计资料，但这里不应该是一堆同等权重的散文档。
本入口用于区分哪些文档是当前设计依据，哪些只是草稿、参考、未来想法或历史归档。

## 默认读取顺序

1. 先读 `North Star`
2. 再读对应系统的 `Active Spec`
3. 需要背景时再读 `Reference`
4. 不默认读取 `Draft`
5. `Future` 与 `Archive` 只在任务明确需要时读取

## 文档角色

### North Star

用于记录长期设计方向、不可轻易改变的体验原则和跨系统约束。

当前入口：

- [DESIGN_NORTH_STAR_V1.md](DESIGN_NORTH_STAR_V1.md)

### Active Spec

用于记录当前正在执行或可被实现引用的设计规格。

规则：

- 每个高流量设计区域应尽量只有一个 canonical active spec。
- 如果多个 active 文档互相冲突，必须先确认 source of truth。
- 新实现默认引用 active spec，而不是草稿或旧总结。

### Reference

用于存放参考资料、样例、矩阵、预算表、CSV/XLSX、历史分析和支撑材料。

规则：

- reference 可以帮助判断，但不能自动覆盖 active spec。
- 如果 reference 变成实现依据，需要晋升或链接到 active spec。

### Draft

用于存放正在探索但尚未被接受的设计。

规则：

- draft 不应被 runtime、正式数据或测试契约默认依赖。
- draft 晋升为 active 前，需要补齐状态卡和 review 记录。

### Future

用于存放“以后可能做”的方向。

规则：

- future 文档不能被当作当前承诺。
- future 被重新启用时，必须先转成 draft 或 active spec。

### Archive

用于存放被替代、过期或只保留历史价值的文档。

规则：

- archive 默认不参与当前设计判断。
- 需要引用历史时，说明它和当前 active spec 的关系。

## 推荐状态卡

新设计文档建议在顶部放置简短状态卡：

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

## 当前整理原则

- 不把所有 `V1/V2/V3/FINAL` 文件平铺视为同等可信。
- 不因为文件名写着 `FINAL` 就默认它是当前 source of truth。
- 不把 matrix、budget、csv、xlsx 自动当作最终规格。
- 优先补状态和索引，再做大规模移动。

## 未来目录形态

目标形态可以逐步靠近：

```text
docs/design/
├── README.md
├── north_star/
├── active/
│   ├── core/
│   ├── campaign/
│   ├── combat/
│   ├── event/
│   └── cards/
├── reference/
├── drafts/
├── future/
└── archive/
```

这只是目标方向，不要求一次性迁移现有目录。

## 近期试点

优先选择少数高流量区域做治理试点：

1. `ideal/`
2. `campaign/`
3. `enemydesigon/`

每个试点先回答：

- 哪个文档是当前 canonical？
- 哪些文档只是 reference？
- 哪些文档应标为 draft、future 或 archive？
- 是否需要一个局部 README 做入口？
