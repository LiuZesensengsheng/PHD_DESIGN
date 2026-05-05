# EEE Rules Comparison

## Goal

Compare the older EEE framing with the parts that still matter in the current repository.

## Data Sources Compared

1. EEE contract ideas
2. User/developer collaboration rules
3. Project memory rules
4. Current document-based workflow

## Stable Overlap

### 1. Avoid Magic Values

- Still valid
- Best represented through constants and explicit naming

### 2. Strong Interfaces

- Still valid
- Best represented through typed modules and readable boundaries

### 3. Fast Quality Feedback

- Still valid
- Now represented by direct test and validation commands instead of a central wrapper script

## Partial Overlap

### 4. Architecture Self-Explanation

- Still useful as a design goal
- Better expressed through stable docs and clean module boundaries

### 5. Bug History

- Still useful
- Should stay close to implementation, not inside long-term project memory

### 6. Task-Driven Execution

- Still useful
- Current implementation direction:
  - `docs/development/CODEX_TASK_POOL.md`
  - workflow-specific docs
  - direct scripts and direct pytest targets

## Current Differences From Older EEE Wording

- No centralized wrapper-style toolchain
- No retired command as the default resume mechanism
- No retired command as the default task discovery surface

## Recommendation

### Keep

- The quality philosophy
- The emphasis on explicit rules
- The preference for inspectable workflows

### Do Not Keep

- Retired umbrella tooling
- Hidden command surfaces that are hard to remember
- Workflow descriptions that disagree with current hot-memory docs

## Practical Default

When in doubt, use:

1. `AGENTS.md`
2. `docs/development/CURRENT_DIRECTION.md`
3. `docs/development/DEFAULT_ENTRYPOINTS.md`
4. the relevant direct script or pytest target
