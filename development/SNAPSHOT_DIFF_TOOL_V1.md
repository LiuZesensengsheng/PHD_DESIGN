# Snapshot Diff Tool V1

## Goal

Provide a focused developer tool for comparing two machine snapshots and quickly seeing why runtime state drifted.

## What It Compares

- `meta.current_state`
- `persistent`
- the active state's `state_snapshots[<current_state>]`

The tool is meant for:

- regression debugging
- save/load state comparison
- inspecting why two runs diverged

It is not meant to be a general JSON diff platform or a GUI debugger.

## Default Command

```bash
python scripts/diff_machine_snapshots.py <before.json> <after.json>
```

Show path-level details:

```bash
python scripts/diff_machine_snapshots.py <before.json> <after.json> --details
```

## Output Shape

Default output includes:

- current state before/after
- changed paths under `persistent`
- changed paths under the active state snapshot

`--details` adds path-level lines like:

- `persistent.pending_block_id`
- `persistent.pending_transitions[0].payload.reward_id`
- `state_snapshots.CAMPAIGN.current_turn`

## Notes

- Supports current machine snapshot shape and existing legacy campaign snapshot shape
- Uses the project snapshot structure directly; it does not rewrite or migrate save files
- Prefer this tool before hand-inspecting large snapshot JSON files
