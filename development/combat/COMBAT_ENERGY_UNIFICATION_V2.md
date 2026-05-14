# Combat Energy Unification V2

## Problem

The previous combat contract pass promoted `archetype.energy_pool` as the
payment authority because colored energy still looked like a possible future
rule.

The product rule is now decided: combat uses one unified energy resource. There
is no colored-energy design target for this game.

That changes the architecture direction:

- scalar `Energy(current, max_value)` should be the combat energy authority
- `energy_pool` and `Color.COLORLESS` energy handling are removed
  over-abstraction, not future-facing or compatibility contracts
- save, render, payment, tests, and helpers should use scalar energy directly

Level: `L3 Architecture`

Date: `2026-05-13`

Status: accepted planning direction

Update `2026-05-13`:

- The user confirmed the target should match Slay the Spire's scalar energy
  model without a colored-pool compatibility layer.
- Active combat runtime, current combat save payloads, render DTOs, helpers,
  and tests should not retain `EnergyPool` or `energy_pool` surfaces.
- `Color.COLORLESS` remains valid only as card/content identity data.

Update `2026-05-14`:

- Active ideal colors are card/content identity and judgment state only. They
  must not automatically add start-turn energy.

Supersedes:

- the energy-authority recommendation in
  `docs/development/combat/COMBAT_CONTRACT_CONVERGENCE_V1.md`

## Constraints

- Do not rebalance combat cards or enemy content in this line.
- Do not touch `combat_view` visual behavior beyond DTO field cleanup.
- Do not reopen old save compatibility; pre-alpha combat saves may fail closed.
- Keep `cardanalysis` / `combat_analysis` out of scope.
- Keep `Color` only where it still represents card/content identity; do not use
  it to model energy.
- Keep full `py -3.11 -m pytest -q` as the commit gate until the repository
  policy changes.
- Land this as small implementation slices with focused validation.

## Complexity

### Essential Complexity

Combat still needs a stable energy resource:

- current amount
- max amount
- spend/add/refill operations
- X-cost and preview reads
- save/load round trips for the current schema
- HUD/render state reads

That complexity belongs in scalar `Energy` and small helper surfaces around it.

### Accidental Complexity

The following surfaces no longer describe the target architecture:

- `EnergyPool` as a payment authority
- `Color.COLORLESS` as a stand-in for unified energy
- `energy_pool_current` / `energy_pool_max` combat save fields
- render-state `energy_pool` fields for combat HUD energy
- test helpers whose only purpose is to sync scalar energy with a colorless
  pool
- payment code that branches through a pool map before spending unified energy

These surfaces are not part of the active combat contract.

## Options

### Option A. Keep `EnergyPool` As A One-Color Model

Use `Color.COLORLESS` forever and treat `EnergyPool` as the generic energy
container.

Pros:

- lowest immediate churn
- preserves the recent 80-point energy-pool migration work

Cons:

- keeps a fake color abstraction in the core payment path
- encourages future agents to design colored-energy behavior that the product
  does not want
- makes save/render/test DTOs heavier than the actual game rule

### Option B. Delete `EnergyPool` In One Broad Step

Remove pool fields, save fields, render fields, helpers, and tests in one PR.

Pros:

- fastest route to a clean model if it lands perfectly
- avoids a second transition period

Cons:

- touches payment, player state, save/load, render DTOs, and many tests at once
- weak rollback story
- likely to mix real behavior regressions with mechanical cleanup

### Option C. Flip Authority To Scalar Energy First, Then Delete Pool Surfaces

Make scalar energy the write/payment authority, then remove one read/write family
per slice.

Pros:

- matches the new product rule
- keeps each implementation slice reviewable
- lets tests prove behavior before deleting scaffolding
- reduces over-abstraction without a broad rewrite

Cons:

- leaves a short transition period where pool fields still exist but are
  explicitly deprecated
- requires guardrails so new code does not add more `energy_pool` usage during
  the transition

## Risks

- If pool deletion happens before payment and preview paths are scalar-owned,
  X-cost and refund behavior may regress.
- If save fields are removed without explicit current-schema tests, unsupported
  old saves may fail unclearly instead of failing closed.
- If render DTO fields are removed before HUD consumers are checked, visual
  energy display can silently drift.
- If this line deletes `Color` broadly, it may break card/content identity that
  is unrelated to energy.

## Recommendation

Choose **Option C** for the first authority flip, then collapse the remaining
compatibility layer once the user explicitly removed the transition
requirement.

For V2:

- scalar `Energy` is the combat energy authority
- `player.energy` / `archetype.energy` are the canonical read/write surfaces
  until a narrower final owner is chosen
- `energy_pool` is not retained as runtime, save, render, helper, or test
  scaffolding
- new combat payment, preview, save, render, and test code should not add
  `energy_pool` dependencies

### Slice Order

1. **Plan freeze**
   - add this document
   - mark the V1 energy-pool authority direction as superseded
   - update the refactor season and task pool docs
   - no runtime behavior change

2. **Scalar payment authority**
   - simplify `EnergyPolicy` and direct payment helpers toward scalar `Energy`
   - keep behavior stable for normal cost, X-cost, refunds, and turn refill
   - focused validation:
     - `tests/combat/test_energy_policy_and_playability.py`
     - `tests/combat/test_playability_payment_basic.py`
     - `tests/combat/test_x_cost_energy_basic.py`
     - `tests/combat/test_start_turn_energy.py`
     - nearby payment/action tests touched by the slice

3. **Remove colored-pool compatibility layer**
   - remove `EnergyPool` from active combat runtime
   - remove `energy_pool_current` / `energy_pool_max` from current combat save
     payloads and fixtures
   - remove render DTO `energy_pool`
   - move helpers and assertions to scalar energy
   - delete tests whose only value was proving pool behavior
   - add a narrow guardrail preventing active combat code, tests, and combat
     save fixtures from reintroducing the removed pool model
   - focused validation:
     - payment/start-turn/X-cost tests
     - `tests/combat/test_combat_save_snapshot_mapper.py`
     - `tests/combat/test_combat_render_state_contracts.py`
     - `tests/helpers/test_headless_test_base_energy_helpers.py`
     - `tests/shared/test_naming_and_contract_guards.py`

4. **Closure review**
   - run focused combat packs, quick smoke, contract smoke, and full pytest
   - update docs with retained energy surfaces and any explicitly deferred
     cleanup

### Superseded Earlier Slice Plan

The original staged plan separated these into later slices. That slower
transition was superseded by the no-compatibility-layer direction above.

3. **Scalar save and render contract**
   - make combat save payloads serialize scalar energy as the current schema
   - remove or explicitly reject pool-dependent current-looking payloads
   - make render-state energy fields derive from scalar energy
   - focused validation:
     - `tests/combat/test_combat_save_snapshot_mapper.py`
     - `tests/combat/test_combat_render_state_contracts.py`
     - save reset focused tests if schema behavior changes

4. **Test helper and assertion migration**
   - move headless and combat helper setup back to scalar energy
   - migrate direct pool assertions to scalar assertions where color is not the
     behavior under test
   - delete tests whose only value was proving `Color.COLORLESS` synchronization

5. **Runtime pool surface deletion**
   - remove `EnergyPool` from active combat runtime if no current code depends
     on it
   - remove `energy_pool_current` / `energy_pool_max` from current save schema
   - remove render DTO `energy_pool` once HUD consumers no longer need it
   - add a narrow guardrail that active combat runtime does not reintroduce
     `energy_pool` outside any temporary allowlist

6. **Closure review**
   - run focused combat packs, quick smoke, contract smoke, and full pytest
   - update docs with retained energy surfaces and any explicitly deferred
     cleanup

## Counter-Review

Why not keep the pool because the recent 80-point pass just moved toward it?

- That pass was correct under the then-open assumption that colored energy might
  be future-facing. The product rule changed. Keeping a fake color layer now
  would be sunk-cost architecture.

Why not delete scalar `player.energy` and introduce a brand-new `EnergyService`
instead?

- The current problem is over-abstraction. A new service could be useful later,
  but V2 should first remove the false dual model and keep the existing scalar
  value object as the stable authority.

Why not make this part of save reset or content-pack work?

- Energy authority cuts across combat payment, save, render, and tests. It
  should land as its own combat contract line so save/content decisions stay
  smaller.

## Decision Summary

1. Combat uses one unified scalar energy resource.
2. Colored-energy and colorless-pool authority are no longer product targets.
3. `COMBAT_CONTRACT_CONVERGENCE_V1` remains historical context but is
   superseded for energy authority by this V2 plan.
4. The 90-point architecture pass should use scalar energy directly and keep a
   guardrail against reintroducing colored-pool energy surfaces.
5. This line intentionally does not touch content balance, visual combat UI, or
   `cardanalysis` / `combat_analysis`.
6. Active ideal color selection does not grant automatic start-turn energy.
