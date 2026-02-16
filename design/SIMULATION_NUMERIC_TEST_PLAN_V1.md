# Simulation Numeric Test Plan V1

## Scope

This plan covers data-driven numeric testing for combat simulation.

## Implemented in V1

1. Real execution path
- Engine: `contexts/simulation/headless_combat_executor.py`
- Uses the real `CombatModel` and domain logic (no UI dependency).

2. Run metrics
- `turns_played`
- `total_damage_dealt_to_enemies`
- `total_damage_taken_by_player`
- `total_confidence_gained`
- `total_stress_gained`
- `remaining_player_health`
- `remaining_player_stress`
- `remaining_enemy_count`

3. Redlines / targets
- Global stress redline: `200`
- Config file: `config/simulation/metric_targets_v1.json`
- Evaluator: `contexts/simulation/metric_targets.py`

4. Gold scenario set
- Location: `data/simulation/scenarios`
- Current set includes baseline + 8 gold scenarios.

## How to run

- Validate scenario JSON:
  - `python tools/simulation/validate_scenarios.py`
- Run a profile on one scenario:
  - `python tools/simulation/run_profile.py gold_rollcall_average_single_v1 --profile quick_regression`

## CI policy suggestion

- Keep `tests/simulation` as fast smoke/contract checks.
- Run profile-level long simulation in nightly/manual pipelines.
