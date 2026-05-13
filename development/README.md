# Development Docs Index

This directory stores long-term project memory: architecture boundaries, stable workflow rules, and design-analysis contracts.

## Root Hot Files

- `CURRENT_DIRECTION.md`: short north-star and current priorities.
- `DEFAULT_ENTRYPOINTS.md`: recurring command memory.
- `CODEX_TASK_POOL.md`: active and queued Codex-ready work.
- `PROJECT_MEMORY_INDEX.md`: where to read and write project memory.
- `PROJECT_MEMORY_RULES.md`: memory maintenance rules.
- `PROJECT_MEMORY_HEALTH_V1.md`: memory-health policy.
- `PROJECT_MEMORY_DIGEST_V1.md`: read-only recovery digest contract.

## Subdirectories

- `architecture/`: cross-cutting architecture, save policy, UI, DDD, EEE, and boundary docs.
- `campaign/`: campaign runtime, UI, lifecycle, task-area, and campaign-analysis docs.
- `cardanalysis/`: case-backed design-analysis contracts, evidence libraries, mechanism axes, and advisory model docs.
- `combat/`: combat runtime contracts, gates, compatibility plans, and automation backlogs.
- `content/`: formal content-data contracts and balance baselines.
- `narrative/`: narrative pipeline, source schema, instance model, and task tables.
- `platform/`: repository tooling, smoke baselines, data pipeline guardrails, and test strategy.
- `thesis/`: thesis-specific lifecycle, write-path, verdict, and aggregate docs.
- `task_pool_archive/`: completed task-pool entries moved out of the hot task file.

## Rule Of Thumb

Keep the root small enough to recover project context quickly. Put topic-specific long-term docs in the matching subdirectory, then update references and the daily log.
