# Save Reset Policy V1

## Goal

Make the current pre-content save policy explicit: old local saves are not a
compatibility promise yet.

The project has no shipped external save corpus and the user has accepted that
pre-alpha saves may be invalidated during this refactor window. Save code should
therefore prefer a small current contract over long-lived migration shims.

## Current Policy

- New saves are always written in the latest current schema.
- Whole-game machine snapshots must include:
  - `meta.current_state`
  - `meta.snapshot_schema_version`
  - `persistent`
  - `state_snapshots`
- Save slot payloads must wrap the machine snapshot under `machine_snapshot`.
- Missing, old, malformed, or unsupported machine snapshot schemas fail closed.
- `GameStateMachine.load_slot(...)` returns `False` for unsupported saves.
- `MachineSnapshotService.parse_snapshot(...)` returns `None` for unsupported
  machine snapshots.

## Compatibility Stance

Unsupported during the current pre-content stage:

- legacy machine snapshots shaped like
  `{"meta": {"current_state": ...}, "<STATE>": {...}}`
- current-looking machine snapshots without `meta.snapshot_schema_version`
- save slot payloads where the payload itself is the machine snapshot
- deriving campaign persistent data from active-state snapshots

Still allowed:

- current-schema round trips
- conservative failure on malformed external JSON
- versioned current-schema parsing when the version equals
  `MachineSnapshotService.CURRENT_SCHEMA_VERSION`

## Version Layers

The project still has separate version layers:

- Slot envelope: `SaveGameData.version`
- Machine snapshot: `meta.snapshot_schema_version`
- Combat snapshot: `schema_version`

This policy only tightens the whole-game machine snapshot and save-slot wrapper
behavior in the first slice. Combat snapshot migration is intentionally left to
a later save/combat slice.

## Change Rules

When editing save fields during this pre-content stage:

1. Prefer bumping the relevant schema and rejecting unsupported old schemas over
   adding broad compatibility guesses.
2. Keep save/load round-trip coverage for the current schema.
3. Add explicit rejection tests for removed legacy shapes.
4. Do not mix machine snapshot policy changes with combat energy semantics or
   content-pack identity work.
5. Record any future compatibility promise in this policy before adding
   migrations.

## Reversal Path

If the project later needs external save compatibility, supersede this document
with a narrower versioned migration policy, then add explicit fixture-backed
migrations for the save versions that must be supported.

