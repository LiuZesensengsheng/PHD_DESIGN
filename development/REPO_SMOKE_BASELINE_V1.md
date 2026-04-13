# Repo Smoke Baseline V1

## Goal

Define the default repository-wide smoke baseline for multi-area changes.

This baseline is meant to answer one question quickly:

- "Did we break a core repo-level path or guardrail?"

It is intentionally broader than a single bounded-context gate, but much
smaller than `python -m pytest -q`.

## Default Entrypoint

```bash
python scripts/run_repo_smoke_baseline.py
```

Helpful variants:

```bash
python scripts/run_repo_smoke_baseline.py --list
python scripts/run_repo_smoke_baseline.py --group combat-mainline
python scripts/run_repo_smoke_baseline.py --group repo-guards
```

## Included Groups

### 1. Combat Mainline

Purpose:

- keep the combat compat-zero and queue-only mainline green
- fail fast if old fallback/helper seams reappear

Coverage:

- `scripts/check_combat_compat_zero.py`
- focused combat mainline gate tests
- combat smoke-pack coverage
- combat UI targeting / controller guardrails for drag-to-play white-card flows

### 2. Campaign Orchestration

Purpose:

- protect the stable campaign-shell seams that UI and runtime work depend on

Coverage:

- campaign UI-safe shell seams
- interaction-sequence click/modal regressions
- campaign simplification guardrails
- transition request contracts
- encounter contract checks
- orchestration aggregate invariants
- reward / thesis guardrail flow contracts

### 3. Cross-Context

Purpose:

- protect the smallest state-machine and headless end-to-end flows across
  dialogue, campaign, combat, and reward return paths

Coverage:

- state-machine minimal contract
- campaign/combat integration
- headless encounter smoke

### 4. Repo Guards

Purpose:

- fail fast on repo-wide drift in data, encoding, or static contract rules

Coverage:

- card/data pipeline contracts
- resource contract guards
- asset manifest consistency check
- text encoding guards
- naming/contract police guards

## When To Run It

Run this baseline by default when:

- a change touches more than one bounded context
- a tooling or workflow change needs fast repo-wide confidence
- a refactor changes shared contracts or default runtime entrypoints
- you want one standard pre-merge confidence pass without jumping straight to
  the full suite

## What It Does Not Replace

This baseline does not replace local deep validation.

After touching a hot area, still escalate to the fuller suites for that area:

- combat runtime/content: `python -m pytest tests/combat -q` and
  `python -m pytest tests/simulation -q`
- campaign runtime/orchestration: `python -m pytest tests/campaign -q`
- UI/theme/static assets: run the relevant UI layout/icon/static checks

## Design Rule

Keep this baseline:

- memorable
- direct
- focused on high-value breakage
- small enough that collaborators will actually run it

If a new check is valuable only for one subsystem, keep it in that subsystem's
own gate instead of expanding this baseline by default.
