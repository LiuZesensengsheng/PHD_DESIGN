# 敌人/遭遇设计入口

- Status: Active
- Owner: Team
- Scope: enemy/encounter-design
- Canonical: Yes, as a directory index
- Supersedes: none
- Superseded By: none
- Implemented In: `data/combat/ta/`, `data/questlines/encounters_ta.json`
- Last Reviewed: 2026-05-17

> 目录名 `enemydesigon` 是历史拼写。本次治理只补状态和入口，不做目录重命名。

## 默认读取顺序

1. 先读 `../DESIGN_NORTH_STAR_V1.md`
2. TA 线实现或扩展先读 `TA_IMPLEMENTABILITY_MAPPING_V1.md`
3. 琐事宿主和点名链回看 `TA_TASK_HOST_MINIMUM_V1.md`
4. DDL 精英继续推进时读 `TA_DDL_PRECONDITIONS_V1.md`
5. 单个遭遇的语义、台词、原型再读 `ENCOUNTER_TA_*` 或 `TA-2_extracted/`

## 当前状态

| 文档 | 状态 | Canonical | 用途 |
| --- | --- | --- | --- |
| `TA_IMPLEMENTABILITY_MAPPING_V1.md` | Active | Yes, for TA encounter rollout | TA 线从设计到实现顺序的当前总入口。 |
| `TA_TASK_HOST_MINIMUM_V1.md` | Frozen | No | 点名/迟到学生最小琐事宿主的已落地前置评估。 |
| `TA_DDL_PRECONDITIONS_V1.md` | Active | Yes, for DDL follow-up | DDL 种植园主继续推进前的当前前置能力清单。 |
| `ENCOUNTER_TA_ROLL_CALL.md`, `ENCOUNTER_TA_QA.md`, `ENCOUNTER_TA_PRESENTATION.md`, `ENCOUNTER_TA_LAB_SAFETY_ROBOT.md` | Reference | No | 单场遭遇语义和组合参考。 |
| `TA-2_extracted/` | Reference / Archive | No | 从 `TA-2.zip` 解压保留的 TA 线原始资料，默认不直接作为实现权威；原始 zip 已删除。 |
| `ENCOUNTER_IDEAS_BACKLOG.md`, `enemy.MD`, `LIFE_MIDTERM_DEFENSE.md`, `论文boss*.md` | Draft / Reference | No | 设计灵感或专题草案，使用前需确认是否要晋升。 |
| `TA_TASK_CHAINING_V1.md` | Reference | No | 点名琐事链历史笔记；当前文件文本存在编码/转写问题，删除或重写前需要 owner 确认。 |

## Source Of Truth

- 当前 TA source-pack 身份在 `data/combat/ta/manifest.json`。
- 当前 TA 编辑源在 `data/combat/ta/*.csv`。
- 当前 TA 运行时遭遇产物是 `data/questlines/encounters_ta.json`。
- 如果设计文档与 runtime CSV/JSON 冲突，runtime 数据、代码和测试先作为已实现行为；设计文档需要单独更新或重新接受。

## 下一次治理建议

- 给 `ENCOUNTER_TA_*` 单场文档补 Reference 状态卡。
- 对 `TA_TASK_CHAINING_V1.md` 这类可疑旧文档，先列候选清单并让 owner 核对，再决定删除、重写或保留。
- 判断论文 boss 文档是保留为 future/draft，还是迁入 active enemy roadmap。
