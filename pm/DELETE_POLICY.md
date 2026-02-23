# 代码删除策略（最小版）

## 目标

在尽量低风险的前提下删除废弃代码，并尽量降低人类管理成本。

## 原则

1. 人类时间是瓶颈，优先优化人工审查效率。
2. 小批次删除，避免一次性大清理。
3. 每次删除都必须可回滚。
4. 行为稳定性优先于“代码整洁感”。

## 适用范围

纳入范围：

- Python 源码（`contexts/`、`shared_kernel/`、`infrastructure/`、`scripts/`、`tools/`）
- 已无引用的资源或配置
- 旧原型与临时文件

不纳入范围：

- 在同一批次里混入功能开发
- 架构级重写

## 风险分级

- `P0`：核心运行路径（`run_campaign.py`、在线状态机路径、存读档路径）
- `P1`：当前工作流高频使用的脚本/测试/文档
- `P2`：原型、草稿、旧实验、无引用资产

## 标准流程

1. 建立候选清单（写明删除理由与风险等级）。
2. 删除前证明“无有效引用”。
3. 按小批次删除（`<=20` 文件或单一主题）。
4. 运行对应测试。
5. 记录决策与回滚点。

## 删除前必须证据

执行引用检查：

```bash
rg -n "<name_or_symbol>" contexts shared_kernel infrastructure scripts tools tests
rg --files | rg "<filename_or_folder>"
```

若出现有效运行时引用，标记为 `P0/P1`，不走快速删除路径。

## 批次规则

1. 每个删除批次单独一个 commit。
2. 同一 commit 不允许混入功能实现。
3. 控制审查体量（建议变更行数 `<=300`）。

## 验证规则

按触达区域选测试（参考 `docs/development/TEST_STRATEGY.md`）：

- 战斗相关：`python -m pytest tests/combat -q`
- 战役相关：`python -m pytest tests/campaign -q`
- 共享内核/全局契约：`python -m pytest -q`

## 回滚规则

出现回归时，优先按 commit 回滚：

```bash
git revert <commit_hash>
```

除非回滚失败，不做手工“半恢复”。

## 删除检查清单（可复制）

- [ ] 候选清单已更新并标注风险等级
- [ ] 已完成 `rg` 引用检查
- [ ] 批次规模符合策略
- [ ] 对应测试已通过
- [ ] 已在 `docs/pm/DECISION_LOG.md` 记录决策
- [ ] 已记录可回滚 commit 哈希

## 删除批次记录表

| 日期 | 批次ID | 范围 | 风险 | 测试 | 结果 | 回滚点 |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | DEL-001 | 例：`linshi/` 清理 | P2 | `pytest ...` | PASS | `<hash>` |
| 2026-02-23 | DEL-20260223-01 | 删除 `examples/stack_logger_example.py`；删除 `robust_game_toolkit/rendering/**`；删除异常文件 `robust_game_toolkit/core/assets/fonts/SourceHanSans-Regular.otf` | P2 | `./.venv311/bin/python -m pytest -q` | PASS（仅既有 warning） | 待提交（提交后补 hash） |
| 2026-02-23 | DEL-20260223-02 | 删除 `robust_game_toolkit/core/assets/fonts/NotoSerifCJKsc.otf`（53MB，无引用） | P2 | `./.venv311/bin/python -m pytest -q` | PASS（仅既有 warning） | 待提交（提交后补 hash） |
