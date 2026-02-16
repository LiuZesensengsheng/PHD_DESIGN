# Save Schema Evolution Spec

## 1. Scope

This document defines how save data versions evolve, migrate, and are tested.
It applies to:

- Whole-game machine snapshot (`MachineSnapshotService`)
- Combat snapshot (`CombatSaveSnapshot` / `CombatSaveService`)
- Slot envelope (`SaveGameData` in repository)

Goal: **new builds can reliably load old saves**, while new saves are always written in latest schema.

## 2. Version Layers (Do Not Mix)

There are 3 independent versions:

1. Slot envelope version  
Key: `SaveGameData.version`  
Owner: `contexts/shared/save/save_load_service.py`  
Meaning: repository payload wrapper version.

2. Whole-game snapshot version  
Key: `meta.snapshot_schema_version` in machine snapshot  
Owner: `contexts/shared/save/machine_snapshot_service.py`  
Meaning: structure of `meta/persistent/state_snapshots`.

3. Combat snapshot version  
Key: `schema_version` in combat snapshot  
Owner: `contexts/combat/application/save/save_contracts.py` and `contexts/combat/application/save/combat_save_service.py`  
Meaning: structure of combat runtime fields.

Rule: bump only the layer you changed.

## 3. Compatibility Policy

Current policy (MVP -> EA):

- Write path: always write latest schema.
- Read path: must support all known historical schemas implemented in code.
- Unknown/future schema:
  - if data shape is parseable, allow tolerant read;
  - if critical keys are missing or invalid, fail safely (do not half-restore).

`GameStateMachine.load_slot(...)` should return `False` on invalid payload.

## 4. What Counts as a Breaking Save Change

Breaking (must bump schema + migration):

- Rename key
- Remove key
- Change type (e.g. `int -> dict`)
- Change semantic meaning of existing key
- Move key across sections (`state_snapshots -> persistent`, etc.)

Non-breaking (no bump required):

- Add optional key with safe default
- Add ignorable metadata

## 5. Migration Rules

### 5.1 Machine Snapshot (`MachineSnapshotService`)

- Latest schema: `CURRENT_SCHEMA_VERSION`.
- Migration entrypoint: `parse_snapshot(...)` internally normalizes payload via `_migrate_to_current_schema(...)`.
- Add migrations as chained pure functions:
  - `_migrate_v1_to_v2(...)`
  - `_migrate_v2_to_v3(...)`
  - ...

Hard requirements:

- Migration must be deterministic and idempotent.
- Never mutate input payload in place.
- Keep fallback defaults conservative (`{}`, `[]`, `0`, `False`) and avoid guessing.

### 5.2 Combat Snapshot (`CombatSaveService`)

- Migration entrypoint: `migrate_snapshot_dict(...)`.
- Keep version-specific transforms explicit:
  - `_migrate_v0_to_v1(...)`
  - future `_migrate_v1_to_v2(...)`, etc.

## 6. Save Contract Invariants

After migration to latest:

- Machine snapshot has:
  - `meta.current_state: str`
  - `meta.snapshot_schema_version: int`
  - `persistent: dict`
  - `state_snapshots: dict`
- Combat snapshot has all contract keys from `CombatSaveSnapshot.to_dict()`.
- Loader never throws on malformed external JSON; invalid snapshot returns failure and logs.

## 7. Testing Requirements

For every schema bump:

1. Unit migration tests
- old -> latest conversion assertions
- malformed payload tolerance

2. Roundtrip tests
- latest write -> latest read retains critical fields

3. Fixture tests (recommended)
- Keep canonical fixtures under `tests/fixtures/saves/...`
- one fixture per important stage/state boundary

Minimum gates:

- `tests/shared/test_machine_snapshot_service.py`
- `tests/save/test_game_save_slot_service.py`
- `tests/save/test_combat_save_service.py`
- relevant e2e snapshot tests

## 8. Change Checklist (When Editing Save Fields)

1. Decide layer version bump (envelope / machine / combat).
2. Add migration function(s).
3. Keep writer output on latest schema only.
4. Add/adjust tests for:
- migration
- roundtrip
- invalid payload guardrail
5. Update this document:
- version map
- changed keys
- fallback behavior

## 9. Current Version Map

As of now:

- Slot envelope (`SaveGameData.version`): `1`
- Machine snapshot (`meta.snapshot_schema_version`): `2`
- Combat snapshot (`schema_version`): `1`

