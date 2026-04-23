# Combat Automation Backlog V1

## Problem

The combat MVC-removal work is now in a late migration phase:

- `CombatSession` is already the canonical runtime host.
- broad test/helper `CombatModel` usage has been cut down sharply.
- the remaining `CombatModel` references are now mostly intentional
  facade/render contract coverage.

What is still missing is not one giant refactor. It is a clean split between:

1. what we still want to keep as an explicit facade contract
2. what should continue being deleted from legacy test usage
3. what is actually a separate runtime/content bug cluster and should stop being
   mixed into MVC-removal work

This document is meant to be stable enough for future automations to use as the
default execution plan.

## Constraints

- No `combat_view` behavior change in this cleanup line.
- No combat content schema/save change in this cleanup line.
- Prefer session-first migration over large rewrites.
- Keep mainline runtime stable for UI, headless, and save/load.
- Automation should avoid blending:
  - facade-deletion work
  - render/presentation contract work
  - red-content runtime bug fixing

## Complexity

### Essential complexity

- `CombatController` / render / presentation tests still need a stable runtime
  adapter shape somewhere.
- Some tests genuinely verify `CombatModel` as a facade contract, not just as an
  accidental host.
- A known `red` power cluster still has behavior gaps under direct
  `CombatSession` execution.

### Accidental complexity

- Old tests used `CombatModel` even when they only needed:
  - `session.play_card(...)`
  - `session.state`
  - `CombatRenderStateAssembler.build(session)`
- The old migration backlog mixed together:
  - test cleanup
  - facade design
  - unrelated content/runtime failures

## Options

### Option A: keep pushing to hard-delete `CombatModel` immediately

- Migrate the remaining 4 test files off the facade.
- Rework render/presentation contracts around raw `session` or assembler output.
- Then delete `CombatModel`.

Pros:

- most aggressive simplification
- fewer public surfaces long-term

Cons:

- higher coordination cost with render/presentation behavior
- easier to accidentally destabilize controller/view contracts
- weak payoff right now because only a very small explicit facade surface remains

### Option B: freeze `CombatModel` as a tiny explicit facade for now, and split red failures into a separate backlog

- Treat the remaining 4 files as intentional facade/render contract coverage.
- Do not add new members to `CombatModel`.
- Continue using `CombatSession` directly everywhere else.
- Track the red-content failure cluster separately.

Pros:

- lowest-risk path
- keeps automation tasks narrow and unambiguous
- matches the current code reality
- best for AI safety: fewer mixed-purpose tasks

Cons:

- `CombatModel` still exists for a while
- full MVC-removal headline is deferred rather than fully “done”

### Option C: formally keep `CombatModel` as a long-lived presentation adapter

- Stop treating it as temporary.
- Document it as the permanent UI/presentation adapter.

Pros:

- simple story for UI callers
- no need for final deletion push

Cons:

- risks fossilizing a compatibility shell
- easier for new logic to drift back into the wrong layer
- works against the current “session-first runtime host” direction

## Risks

- If we choose Option A now, we may spend effort deleting a facade that is
  still useful as a small contract boundary for render/presentation tests.
- If we choose Option C, the repository may slowly grow new logic back into
  `CombatModel`.
- If we do not split the red failure cluster away from MVC-removal work,
  automations will keep producing noisy mixed diffs and unclear progress.

## Recommendation

Choose **Option B** now.

That means:

- freeze `CombatModel` as a tiny explicit facade
- keep only explicit facade/render contract tests on it
- stop migrating those remaining 4 files unless we later make a conscious
  decision to delete the facade contract itself
- treat the remaining red failures as a separate runtime/content workstream

This is the best tradeoff for stability, clarity, and automation friendliness.

## Counter-Review

The main argument against Option B is that it may let the facade linger too
long. That concern is real.

Why it is still the recommended path:

- the remaining explicit facade footprint is already very small
- the current pressure is no longer mainline runtime confusion
- the red failure cluster is now the more valuable cleanup target
- deleting a 4-file, 16-reference facade later is cheap once render/presentation
  ownership is even clearer

So the right move is not “never delete `CombatModel`.” It is “do not force the
last deletion step into the wrong batch.”

## Decision Summary

- Decision: `CombatModel` remains temporarily as a **frozen tiny facade**.
- Rule: no new `CombatModel` surface growth.
- Rule: all new runtime/content tests should use `CombatSession` directly.
- Rule: the remaining `CombatModel` tests are intentional contract coverage.
- Rule: the `red` power failure cluster is a separate backlog from MVC-removal.

## Current Snapshot

As of `2026-04-23`:

- remaining explicit `CombatModel` references under `tests/combat`: `16`
- remaining files: `4`
- files:
  - `tests/combat/test_combat_runtime_host_migration_v1.py`
  - `tests/combat/test_combat_render_state_contracts.py`
  - `tests/combat/test_combat_presentation_contract_v1.py`
  - `tests/combat/test_combat_runtime_surface_inventory_v1.py`

Known red-content/runtime failures to treat separately:

- `test_red_frontier_damage_core_adds_damage_to_frontier_card`
- `test_red_cross_amplify_first_non_red_gives_draw_and_confidence_once`
- `test_red_crossdomain_superconductor_reduces_next_red_cost`
- `test_red_last_line_grants_red_energy_once_on_first_frontier`
- `test_red_frontier_continuous_draw_draws_on_each_frontier_play`

## Automation Queue

### A1. Keep facade surface frozen

Goal:

- guard against new `CombatModel` growth

Automation-safe:

- yes

Expected actions:

- run:
  - `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- if a new `CombatModel` member appears, update neither code nor docs
  automatically; open a decision-needed summary instead

Stop condition:

- inventory test is green

### A2. Maintain session-first default for new tests

Goal:

- ensure newly added combat tests do not drift back to `CombatModel`

Automation-safe:

- yes

Expected actions:

- search:
  - `rg -n "CombatModel\\(session=|from contexts\\.combat\\.mvc\\.model import CombatModel" tests/combat`
- if new non-contract files appear, migrate them to:
  - `session.play_card(...)`
  - `session.state`
  - `CombatRenderStateAssembler.build(session)`

Stop condition:

- only the 4 allowlisted contract files remain

### A3. Red power/runtime bug triage

Goal:

- resolve the 5 known red failures as separate runtime/content work

Automation-safe:

- yes, but one failure family at a time

Expected order:

1. inspect one failing test
2. reproduce it in isolation
3. identify whether the gap is:
   - power registration
   - frontier flag propagation
   - timing dispatch
   - expected-value drift
4. patch the smallest correct runtime/content fix
5. rerun the isolated test, then the red-card file

Stop condition:

- each failure fixed in a separate small commit when possible

### A4. Optional future decision: delete the facade contract

Goal:

- revisit whether the remaining 4 files should stay on `CombatModel`

Automation-safe:

- no, this is decision-gated

Decision trigger:

- only revisit after the red runtime/content cluster is clean
- and only if we want to remove `get_renderable_state()` as a facade contract

### A5. Default validation pack for automation

Use this after each small step:

- `py -3.11 -m pytest tests/combat/test_combat_runtime_surface_inventory_v1.py -q`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q`

Use this after red-runtime fixes:

- `py -3.11 -m pytest tests/combat/test_json_red_cards.py -q`

Use this after broader test migration batches:

- `py -3.11 -m pytest tests/combat/test_card_pile_routing.py tests/combat/test_content_event_native_batch3.py tests/combat/test_content_event_native_batch4.py tests/combat/test_content_window_native_batch1.py tests/combat/test_content_window_native_batch2.py tests/combat/test_json_red_cards.py tests/combat/test_json_white_cards.py tests/combat/test_pointer_engine.py tests/combat/test_regulated_damage.py tests/combat/test_reposition_and_lockqueue.py tests/combat/test_sequence_damage_view.py tests/combat/test_white_defense_and_rollcall.py tests/combat/test_white_endpoint_and_summary.py tests/combat/test_white_pointer_moves.py tests/combat/test_white_regulated_archive_and_focus.py tests/combat/test_white_shuffle_blast.py tests/combat/test_white_ui_targeting_contracts.py tests/combat/test_combat_controller_runtime_integration.py tests/combat/test_playability_payment_basic.py -k "not test_red_frontier_damage_core_adds_damage_to_frontier_card and not test_red_cross_amplify_first_non_red_gives_draw_and_confidence_once and not test_red_crossdomain_superconductor_reduces_next_red_cost and not test_red_last_line_grants_red_energy_once_on_first_frontier and not test_red_frontier_continuous_draw_draws_on_each_frontier_play" -q`
