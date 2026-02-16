# Simulation Layering Spec

## Goal

Separate long-running simulation capability from short CI tests.

## Layering

1. Simulation capability package
- Path: `contexts/simulation/`
- Contains: scenario loading, batch orchestration, summary metrics, parameter search.
- Must not depend on `pytest`.

2. Short tests
- Path: `tests/`
- Role: contract tests, smoke tests, fast regression guards.
- Should execute quickly in default local/CI runs.

3. Data and config
- Runtime/game content: `data/...`
- Simulation scenario inputs: `data/simulation/scenarios/...`
- Simulation execution profiles: `config/simulation/...`
- Test-only tiny fixtures: `tests/fixtures/...`

## Slow jobs policy

- Long sequence simulation and balance search are run by dedicated commands/tools,
  not by default pytest suite.
- Nightly/manual execution can consume `contexts/simulation` and `data/simulation`.

## Current status

- `contexts/simulation` package skeleton is established.
- `HeadlessCombatSimulationExecutor` runs real combat logic in headless mode.
- `tools/simulation/validate_scenarios.py` validates scenario payloads quickly.
- `config/simulation/metric_targets_v1.json` defines initial metric redlines/targets.
- Fast tests under `tests/simulation` verify package behavior.
