# Combat Contract Convergence V1

## Supersession Notice

The energy-authority direction in this document was superseded on `2026-05-13`
by `docs/development/combat/COMBAT_ENERGY_UNIFICATION_V2.md`.

V1 remains useful historical context for the 80-point refactor baseline. Do not
continue migrating combat energy toward `archetype.energy_pool` authority.
The product rule is now unified scalar energy, and `energy_pool` is
migration-phase scaffolding to delete in small V2 slices.

## Problem

Combat compat-zero removed the old runtime shell, but a few domain contracts are
still dual-track. The first active example is player energy:

- `EnergyPolicy` spends from `archetype.energy_pool`.
- UI, tests, save snapshots, and simple helpers still read `player.energy`.
- `Player` still had a rollback snapshot field named `legacy_energy`, even
  though scalar energy is still an active projection.

## Constraints

- Do not change combat content balance in this line.
- Do not touch `combat_view` or other visual behavior.
- Do not reopen save compatibility after `Save Reset Policy V1`; current saves
  stay current-schema only.
- Keep `cardanalysis` / `combat_analysis` out of scope.
- Full `py -3.11 -m pytest -q` remains the commit gate.

## Complexity

Essential complexity:

- colored and colorless energy pools need to remain the payment authority for
  colored-card rules
- scalar `Energy` still supplies a compact read surface for HUD/tests/save
  serialization

Accidental complexity:

- rollback code names the scalar projection `legacy_energy`
- future agents may mistake the scalar projection for the payment authority
- save/reset work and combat energy convergence can get mixed if the boundary is
  not explicit

## Options

1. Delete scalar `player.energy` immediately.
   - Benefit: one energy model.
   - Cost: broad UI/test/save churn and higher risk than this slice needs.

2. Keep scalar `player.energy` as a projection while making
   `archetype.energy_pool` the explicit payment authority.
   - Benefit: small, automatable convergence path.
   - Cost: one read-side projection remains until UI/save/tests migrate.

3. Keep both tracks without policy.
   - Benefit: no immediate churn.
   - Cost: future agents keep reintroducing compatibility language and unclear
     ownership.

## Risks

- If scalar projection is removed too early, many combat assertions and HUD/save
  reads break without improving gameplay semantics.
- If the projection is left unnamed, it will keep looking like a compatibility
  layer rather than a transition contract.
- If payment code starts reading scalar energy again, colored-energy rules drift.

## Recommendation

Use option 2.

For V1, `archetype.energy_pool` is the write/payment authority. Scalar
`player.energy` remains a read-side projection and setup convenience until
tests, save mapper, and HUD reads can migrate deliberately.

Completed slices:

- removed the `legacy_energy` rollback field name and replaced it with
  `scalar_energy`, while keeping behavior stable
- moved the shared headless test energy setup/read helper toward the colorless
  pool as authority, while keeping the scalar projection synchronized
- made combat save mapper scalar energy fields derive from the colorless pool
  and resync scalar projection after pool restore
- made combat render-state scalar energy fields derive from the colorless pool
  while preserving the existing UI DTO fields

## Counter-Review

This is not the final destination. It deliberately leaves dual reads alive. That
is acceptable because the current highest-value move is to make ownership
explicit, not to rewrite every energy consumer in one branch.

Next slices should migrate one read family at a time. Good candidates are:

- direct combat test assertions that can assert through `energy_pool`
- small event/protocol/alias compatibility layers where replacement paths are
  already established

## Decision Summary

- Payment authority: `archetype.energy_pool`.
- Temporary projection: `player.energy`.
- Removed wording: `legacy_energy` in rollback snapshots.
- Headless test energy setup now reads/writes the colorless pool first.
- Combat save scalar energy fields now derive from the colorless pool.
- Combat render-state scalar energy fields now derive from the colorless pool.
- Not in this line yet: UI behavior, content balance, save compatibility, or a
  full scalar-energy deletion.

