# Delivery Horizons V1

## Goal

Define delivery horizons for the project so near-term progress can be measured without
future-facing work inflating the number.

## Horizons

### `internal_playtest`

- The team can run the main loop end to end.
- Critical blockers are visible instead of hidden.
- Placeholder content and rough presentation are still acceptable.

### `closed_test`

- The game has enough representative content to validate the intended loop.
- Core runtime paths, save/load, and content import paths are stable enough for outside
  testers or a small trusted group.
- Major design holes are known and tracked.

### `ea_launch`

- The Early Access scope is explicitly frozen.
- Store, build, crash-triage, basic art/audio pass, and launch checklist work are in
  scope.
- The product is commercially presentable even if it is not yet "finished".

### `v1_0`

- The intended launch-quality content and polish bar are complete.
- Remaining work is mostly maintenance, live-ops, or expansions.

### `future`

- Important work that is real, but intentionally excluded from the current release
  target.
- Long-horizon refactors, speculative systems, and post-launch content belong here.

## Counting Rule

- Delivery reports are cumulative by horizon.
- When focus is `internal_playtest`, only `internal_playtest` slices count.
- When focus is `closed_test`, `internal_playtest + closed_test` slices count.
- When focus is `ea_launch`, `internal_playtest + closed_test + ea_launch` slices
  count.
- When focus is `v1_0`, everything up to `v1_0` counts.
- future never counts toward nearer horizons.

## Slice Gates

Each slice moves through the same fixed gates:

1. `scope`
2. `spec`
3. `runtime`
4. `validation`
5. `playtest`
6. `polish`

The tracker should prefer gate truth over vague `todo/doing/done` labels.

## Recommended Size Weights

Use small weighted sizes so progress is harder to game and easier to compare:

- `1`
- `2`
- `3`
- `5`
- `8`

## Release Rule

If a slice is useful but not required for the current target, move it to a later horizon
instead of keeping it in the current horizon and mentally "ignoring" it.
