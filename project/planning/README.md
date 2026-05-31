# 项目计划

- 状态: Draft
- 负责人: Team
- 范围: goals-requirements-tasks
- 最后复核: 2026-05-30

## 目标

这里把项目管理从单层 TODO 升级为三层结构：

```text
目标 Goal
  -> 需求 Requirement
    -> 任务 Task
```

里程碑不作为第四层，而是横向的时间/阶段容器。一个目标、需求或任务可以挂到某个里程碑。

## 文件

| 文件 | 用途 |
| --- | --- |
| [goals.json](goals.json) | 目标：为什么做，成功长什么样。 |
| [requirements.json](requirements.json) | 需求：要交付什么能力，有哪些验收条件。 |
| [tasks.json](tasks.json) | 任务：具体要做什么，谁负责，当前状态。 |
| [dashboard.md](dashboard.md) | 由脚本生成的项目计划总览和甘特图。 |

## 状态

| 层级 | 状态 |
| --- | --- |
| 目标 | `planned`, `active`, `at_risk`, `blocked`, `review`, `done`, `later` |
| 需求 | `planned`, `active`, `blocked`, `review`, `done`, `later` |
| 任务 | `planned`, `in_progress`, `blocked`, `review`, `done`, `later` |

## 维护方式

先改 JSON，再生成总览：

```bash
python scripts/generate_project_planning_dashboard.py
python scripts/check_project_control.py
```

后续你们可以在 Docmost 里讨论目标、需求和任务；AI 负责把稳定结论整理回这些 JSON 和总览页。
