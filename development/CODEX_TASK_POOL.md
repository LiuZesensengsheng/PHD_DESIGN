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

### P1. Card Content Pipeline Hardening

- Goal: make the card content pipeline reliable enough for continued large-scale content work
- Inputs:
  - current card CSV/JSON pipeline
  - `scripts/cards_csv_to_json.py`
  - red/white/theorist card data under `data/cards/`
  - recent card text corruption findings from the daily log
- Outputs:
  - stronger validation for card text and core fields
  - a documented source-of-truth rule for CSV vs generated JSON vs legacy bootstrap JSON
  - a lightweight validation entry point or test coverage increase
  - a workflow document for safe card-data editing
- Boundaries:
  - do not redesign the combat runtime repository
  - do not rebalance all cards as part of this task
  - do not delete old bootstrap JSON in the same pass unless they are fully proven unused
- Done when:
  - broken card text or malformed card data fails before runtime
  - teammates can tell which files are editable source, runtime artifact, and legacy reference

### P1. Thesis And Judgment Complexity Review

- Goal: identify the next business-logic hotspot after current UI work
- Inputs:
  - thesis/judgment code paths
  - existing architecture docs
- Outputs:
  - decision-ready refactor plan
- Boundaries:
  - planning first, not immediate implementation by default
- Done when:
  - the next cleanup target is concrete and scoped

### P1. Content Data Validation Expansion

- Goal: extend validation beyond the current card text guardrails so content errors fail earlier and more clearly
- Inputs:
  - current CSV/JSON pipelines
  - card/enemy/event-related data files under `data/`
  - existing validation scripts and tests
- Outputs:
  - stronger validation rules or checks
  - clearer failure categories for missing fields, invalid values, broken references, and suspicious text
  - expanded test coverage or a lightweight validation entry point
- Boundaries:
  - do not replace the whole content pipeline in one pass
  - do not redesign runtime repositories as part of this task
- Done when:
  - common malformed content cases fail before runtime and produce actionable errors

### P1. Investigate Why Virtue/Torment Does Not Trigger At 100

- Goal: find out why the "美德 / 折磨" mechanic does not trigger when the expected threshold reaches 100
- Inputs:
  - current combat/domain implementation for the relevant mechanic
  - card/effect/archetype data that should drive the threshold behavior
  - any existing tests or logs showing the threshold reaching 100 without triggering
- Outputs:
  - root-cause analysis
  - minimal fix plan or implementation if the cause is clear and low-risk
  - regression test coverage for the 100-threshold trigger
- Boundaries:
  - do not rebalance unrelated cards or systems in the same pass
  - do not redesign the mechanic before confirming current intended behavior
- Done when:
  - we can explain whether the failure is caused by logic, data, rounding, event order, or expectation mismatch
  - and there is a reproducible test guarding the intended 100-threshold behavior

## Deferred Tasks

These stay in the pool, but are not the current default daytime execution targets.

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

## Exit Rules

Remove or downgrade a task when:

- the task has been implemented
- the task is blocked on design decisions
- the task no longer fits the current production phase
- the task turns out to require constant subjective feedback
