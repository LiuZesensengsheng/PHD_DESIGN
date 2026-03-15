# Seed Replay / Repro Tool V1

## Goal

Provide a focused developer tool for reproducing the most expensive headless state-machine paths with a stable `case + seed` pair.

This tool is for:

- replaying main-path runtime drift
- producing machine snapshots for diff/debug work
- re-running the same encounter flow after a regression

It is not a generic event recorder or a UI input playback framework.

## Built-in Cases

- `dialogue_to_campaign`
- `combat_reward_loop`
- `thesis_judgment_to_combat`

Each case uses the real `GameStateMachine` and real state objects, then captures:

- `before_snapshot.json`
- `after_snapshot.json` on success
- `failure_snapshot.json` on failure
- `result.json` with case, seed, final state, checkpoint, and artifact paths

## Default Command

```bash
python scripts/repro_headless_flow.py dialogue_to_campaign --seed 12345
```

Another built-in case:

```bash
python scripts/repro_headless_flow.py combat_reward_loop --seed 12345
```

Write artifacts to a custom directory:

```bash
python scripts/repro_headless_flow.py thesis_judgment_to_combat --seed 12345 --output-dir logs/repro/manual_check
```

## Output Summary

Console output includes:

- `case`
- `seed`
- `success`
- `final_state`
- `checkpoint`
- snapshot artifact path

Artifacts default to `logs/repro/<case>_<seed>/`.

## Workflow With Snapshot Diff

This tool is designed to pair with the existing snapshot diff entrypoint:

```bash
python scripts/diff_machine_snapshots.py <before.json> <after.json>
```

Typical usage:

1. Run the seeded repro case.
2. Compare the produced snapshots.
3. Re-run the same `case + seed` after a fix to confirm drift is gone.

## Notes

- The tool uses a shared `runtime_repro_seed` contract so campaign thesis text generation and combat runtime RNG can follow the same seed.
- v1 intentionally stays on three high-value headless main paths instead of expanding into a general replay platform.
