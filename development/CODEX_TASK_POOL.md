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

### P1. Thesis Runtime State Third Cut

- Goal: extract a thinner thesis runtime host so thesis state and publication/innovation persistence stop spreading across `CampaignState`, services, and session helpers
- Inputs:
  - current thesis/judgment outcome + flow split
  - `contexts/campaign/state.py`
  - thesis runtime fields and session persistence accessors
  - publication / innovation persistence paths
- Outputs:
  - a thinner thesis runtime host or state object
  - clearer ownership rules for runtime-only state vs persisted thesis data
  - regression coverage for the extracted runtime host
- Boundaries:
  - do not redesign publication UX or thesis copy
  - do not reopen the first/second cuts unless needed for compatibility
  - keep runtime extraction incremental, not a full thesis subsystem rewrite
- Done when:
  - thesis runtime state has a clearer host than raw `CampaignState` fields
  - publication/innovation persistence boundaries are enforced in code and tests

### P1. TA Enemy Implementability Mapping

- Goal: turn the TA enemy design package into an implementation-ready mapping against the current combat system
- Inputs:
  - `docs/design/enemydesigon/TA-2_extracted/`
  - current enemy/card/task-related combat systems
  - current enemy balance assumptions
- Plan Document:
  - `docs/design/enemydesigon/TA_IMPLEMENTABILITY_MAPPING_V1.md`
- Outputs:
  - a per-enemy mechanism mapping table
  - a list of mechanics that already exist vs mechanics that still need engine support
  - a recommended implementation order for the TA line
  - a short research summary of which parts of the TA design can land immediately
- Boundaries:
  - do not implement full TA enemies in the same pass
  - do not finalize balance numbers before enemy baseline work
- Done when:
  - we can say which TA enemies are directly implementable, which need support work, and which should wait

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

## Exit Rules

Remove or downgrade a task when:

- the task has been implemented
- the task is blocked on design decisions
- the task no longer fits the current production phase
- the task turns out to require constant subjective feedback
