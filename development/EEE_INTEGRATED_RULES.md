# EEE Integrated Rules

## Purpose

This document captures the still-useful parts of the older EEE framing without relying on retired tooling.

## Core Goal

- Reduce AI context recovery cost
- Keep project rules explicit in files
- Prefer direct, inspectable workflows over hidden umbrella commands

## Success Signals

- Low context-recovery time
- Stable quality gates
- Fewer repeated architectural misunderstandings

## Tier 1: Proven Rules

### 1. Semantic Constants

- Avoid magic values in business logic
- Keep constants centralized and named

### 2. Strong Structure

- Prefer explicit interfaces and typed boundaries
- Keep protocols and service boundaries readable

### 3. Fast Feedback

- Run direct quality checks with `pytest`, `mypy`, and `pylint`
- Use documented direct entrypoints instead of retired wrapper CLIs

## Tier 2: Partially Realized Practices

### 4. Localized Bug Memory

- Keep bug history close to code when practical
- Do not confuse bug notes with project-direction memory

### 5. Knowledge Escape Rule

- If a path keeps failing, stop looping and widen the search

### 6. Task Framing

- Task documents can exist
- Current task-entry surface should be file-based and direct:
  - `docs/development/CODEX_TASK_POOL.md`
  - relevant workflow docs
  - direct scripts or tests

## Tier 3: Exploratory Ideas

- Architecture contracts
- Intent contracts
- Cost-aware tool selection

These remain ideas, not mandatory process.

## Cursor / Collaboration Interpretation

### Core Modules

- Highest bar for type safety and regression confidence

### Context Modules

- Strong boundaries and readable structure

### Experimental Modules

- Faster iteration is acceptable
- Still avoid avoidable ambiguity

### Tooling Layer

- Source of truth:
  - `AGENTS.md`
  - `docs/development/CURRENT_DIRECTION.md`
  - `docs/development/DEFAULT_ENTRYPOINTS.md`
- Default execution:
  - direct scripts
  - direct pytest targets

## Note

Older versions of this document referenced retired wrapper-style commands.
Those entrypoints are retired and should not be treated as current workflow.
