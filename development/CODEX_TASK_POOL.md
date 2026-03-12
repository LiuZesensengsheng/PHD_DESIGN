# Codex Task Pool

## Purpose

This document tracks work that Codex can execute independently for several hours with limited supervision.

Use it to choose daytime execution tasks after night planning is complete.

This file is not:

- a daily progress log
- an architecture rulebook
- a decision log

## How To Use

For each task:

1. Confirm the task still matches current priority
2. Confirm required inputs exist
3. Hand the task to Codex together with any needed plan or constraints
4. Record execution results in the daily log

## Task Selection Rules

Choose tasks with these properties:

- clear input files or source documents
- clear output files or acceptance criteria
- low dependence on subjective visual judgment
- low dependence on real-time human feedback
- strong fit for test-first or document-first execution

Avoid assigning Codex long unsupervised work on:

- pure visual polish
- final narrative tone decisions
- high-subjectivity UX decisions
- final hand-tuned balance passes that depend on feel

## Active Tasks

These are the current default candidates for the next daytime execution block.

### Ready To Implement Tomorrow

### P1. TA Batch Two Enemy Implementation

- Goal: implement the second TA enemy batch on the main runtime path after the first-batch skeletons proved out
- Inputs:
  - `docs/design/enemydesigon/TA_IMPLEMENTABILITY_MAPPING_V1.md`
  - first-batch TA CSV/JSON pipeline under `data/combat/ta/`
  - current enemy runtime intent adapter and encounter loader
- Targets:
  - ????
  - ??
  - ???
- Outputs:
  - CSV source rows for the second-batch TA enemies
  - regenerated runtime JSON content
  - at least one new TA encounter exercising second-batch behavior
  - regression coverage for the new enemy intents
- Boundaries:
  - do not implement full task host or elite-only mechanics
  - keep behaviors within the currently supported runtime effect subset, adding only minimal support if strictly necessary
- Done when:
  - all three second-batch enemies can enter combat from the main runtime path and pass smoke/runtime tests

### P1. Content Data Validation Expansion

- Goal: extend validation beyond the current card text guardrails so content errors fail earlier and more clearly
- Inputs:
  - current CSV/JSON pipelines
  - card/enemy/event-related data files under `data/`
  - existing validation scripts and tests
- Outputs:
  - stronger validation rules or checks
  - clearer failure categories for missing fields, invalid values, broken references, and suspicious text
  - expanded test coverage for content validation
- Boundaries:
  - do not replace the whole content pipeline in one pass
  - do not redesign runtime repositories as part of this task
- Done when:
  - common malformed content cases fail before runtime and produce actionable errors

### P1. TA Minimal Task Host Implementation

- Goal: implement the smallest combat-side task host needed to support `迟到学生 / 代到学生`
- Inputs:
  - `docs/design/enemydesigon/TA_IMPLEMENTABILITY_MAPPING_V1.md`
  - `docs/design/enemydesigon/TA_TASK_HOST_MINIMUM_V1.md`
  - current TA CSV/JSON pipeline and runtime enemy adapter
- Outputs:
  - a minimal combat task host runtime object
  - countdown ticking and target-task completion support
  - a minimal enemy transform path for `迟到学生 -> 代到学生`
  - regression tests for the new host behavior
- Boundaries:
  - do not implement the full TA shared task system
  - do not implement three-slot task UI or elite-only rules
  - keep the first version limited to deadline target elimination tasks
- Done when:
  - a `迟到学生` encounter can publish a deadline task, tick countdown, and transform into `代到学生` on failure

## Pending Or Needs More Decisions

### P2. Enemy Balance Baseline V1

- Goal: define the first usable HP / damage / pressure curve for normal, elite, and boss enemies
- Inputs:
  - existing enemy design docs
  - current red/white card baseline
  - current combat tests and simulation scenarios
- Outputs:
  - baseline balance document
  - initial numeric recommendations
  - any required test or scenario updates
- Boundaries:
  - do not redesign enemy identities
  - do not rebalance all colors at once
- Done when:
  - there is a documented enemy curve that can support ongoing encounter implementation
- Why pending now:
  - enemy design and mechanism mapping are not finished yet
  - starting from numbers first would create fake precision without enough design grounding

### P2. Red White Second-Pass Tuning

- Goal: adjust only the problem cards discovered after first-pass playtesting
- Inputs:
  - playtest notes
  - `RED_WHITE_BALANCE_BASELINE_V1.md`
- Outputs:
  - small numeric delta set
  - updated balance notes
- Boundaries:
  - do not run another full-pool rewrite
  - do not change core card identities
- Done when:
  - only the identified outliers were changed and the new baseline remains test-clean

### P2. Headless Balance Checks

- Goal: create lightweight headless checks for obvious overpowered, underpowered, or malformed content
- Inputs:
  - existing simulation scenarios
  - current combat tests
- Outputs:
  - repeatable headless checks
  - simple report format for anomalies
- Boundaries:
  - do not build a complex search or optimizer system
- Done when:
  - a small fixed suite can catch obvious balance regressions

### P3. Content Integration Workflow

- Goal: document and tighten the workflow for adding new cards, enemies, and traits
- Inputs:
  - current card pipeline
  - current enemy schema docs
- Outputs:
  - workflow doc
  - minimum required tests/checks per content type
- Boundaries:
  - do not redesign content architecture
- Done when:
  - a teammate can add a new content item without guessing the process

## Recently Completed

- `Card Content Pipeline Hardening`
- `Thesis And Judgment Complexity Review`
- `Investigate Why Virtue/Torment Does Not Trigger At 100`
- `Thesis Runtime State Third Cut`
- `TA Enemy Implementability Mapping`
- `TA First-Batch Skeleton Enemy Runtime Path`
- `Repository Data Pipeline Guardrails`
- `TA Batch-Three Minimum Task Host Evaluation`

## Exit Rules

Remove or downgrade a task when:

- the task has been implemented
- the task is blocked on design decisions
- the task no longer fits the current production phase
- the task turns out to require constant subjective feedback
