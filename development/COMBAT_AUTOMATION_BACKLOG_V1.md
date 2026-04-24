# Combat Automation Backlog V1

## Status

This document is now **historical pre-decision context**, not the active
execution plan.

It was superseded on `2026-04-23` by:

- `docs/pm/DECISION_LOG.md`
  - `DL-20260423-02`
- `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
- `docs/development/COMBAT_RUNTIME_SURFACE_INVENTORY_V1.md`

The old recommendation in this file to freeze `CombatModel` as a tiny facade is
obsolete. `G1` has completed and the legacy MVC facade modules are now deleted.

## Retained Takeaways

Even though the old freeze recommendation is obsolete, these points remain
useful:

- keep compat-zero cleanup separate from red runtime/content bug fixing
- keep compat-zero cleanup separate from `combat_view`, animation, and save
  schema work
- prefer small serial validation packs over mixed-purpose large refactors
- keep the automation stop condition explicit whenever a task touches a
  different risk boundary

## Current Snapshot

As of `2026-04-23`, after `G1` completion:

- `contexts/combat/mvc/model.py`: deleted
- `contexts/combat/mvc/factory.py`: deleted
- live runtime/test/script imports or constructions of the removed modules: `0`
- remaining textual mentions under `tests/combat`: `2` files
  - `tests/combat/test_combat_runtime_host_migration_v1.py`
  - `tests/combat/test_combat_runtime_surface_inventory_v1.py`
- those remaining mentions are explicit removal guards only

Known red-content/runtime failures that still stay in a separate backlog:

- `test_red_frontier_damage_core_adds_damage_to_frontier_card`
- `test_red_cross_amplify_first_non_red_gives_draw_and_confidence_once`
- `test_red_crossdomain_superconductor_reduces_next_red_cost`
- `test_red_last_line_grants_red_energy_once_on_first_frontier`
- `test_red_frontier_continuous_draw_draws_on_each_frontier_play`

## Active Automation Queue

The active serialized queue is no longer "freeze facade vs delete facade." That
question is already resolved.

Use `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md` as the
execution source of truth:

1. completed: `G1` MVC facade plane removal
2. next: `G2` session wrapper tightening
3. then: `G3` `turn_context` bridge collapse
4. then: `G4` low-value test/import shim cleanup
5. finally: `G5` retained adapter review

## Default Validation Discipline

After each small compat-zero step:

- `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`

After `G2-G4` slice work:

- rerun the focused validation pack named in
  `docs/development/COMBAT_GLOBAL_COMPAT_ZERO_AUTOMATION_V1.md`
- do not jump from a compat cleanup diff straight into unrelated red-content
  failures

After separate red-runtime fixes:

- `py -3.11 -m pytest tests/combat/test_json_red_cards.py -q`

Use this after broader test migration batches:

- `py -3.11 -m pytest tests/combat/test_card_pile_routing.py tests/combat/test_content_event_native_batch3.py tests/combat/test_content_event_native_batch4.py tests/combat/test_content_window_native_batch1.py tests/combat/test_content_window_native_batch2.py tests/combat/test_json_red_cards.py tests/combat/test_json_white_cards.py tests/combat/test_pointer_engine.py tests/combat/test_regulated_damage.py tests/combat/test_reposition_and_lockqueue.py tests/combat/test_sequence_damage_view.py tests/combat/test_white_defense_and_rollcall.py tests/combat/test_white_endpoint_and_summary.py tests/combat/test_white_pointer_moves.py tests/combat/test_white_regulated_archive_and_focus.py tests/combat/test_white_shuffle_blast.py tests/combat/test_white_ui_targeting_contracts.py tests/combat/test_combat_controller_runtime_integration.py tests/combat/test_playability_payment_basic.py -k "not test_red_frontier_damage_core_adds_damage_to_frontier_card and not test_red_cross_amplify_first_non_red_gives_draw_and_confidence_once and not test_red_crossdomain_superconductor_reduces_next_red_cost and not test_red_last_line_grants_red_energy_once_on_first_frontier and not test_red_frontier_continuous_draw_draws_on_each_frontier_play" -q`
