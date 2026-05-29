# 项目同步快照

- 状态: Generated / Review
- 负责人: Team
- 范围: AI-readable-project-sync-snapshots
- 最后复核: 2026-05-27

## 文件

| 文件 | 内容 |
| --- | --- |
| `project_sync_snapshot.json` | 汇总快照，包含 summary、issues、milestones、discussions。 |
| `issues.json` | 规范化后的 GitHub Issues 列表。 |
| `milestones.json` | 规范化后的 GitHub Milestones 列表。 |
| `discussions.json` | 规范化后的 GitHub Discussions 列表。 |

## 生成命令

```bash
python scripts/sync_project_management.py --fetch-github --repo LiuZesensengsheng/PHDGAME
```

## 边界

这些文件是同步产物，用于 AI 读取和人类复核。GitHub 仍然是 Issues、Milestones 和 Discussions 的协作源。
