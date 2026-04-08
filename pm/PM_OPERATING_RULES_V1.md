# PM Operating Rules V1

## Goal

Treat project management as the second control plane after agent execution while keeping
the system lightweight enough for a small team plus AI workers.

## Position In The Stack

- `agent` owns execution throughput.
- `pm` owns scope truth, delivery truth, and blocker visibility.
- `docs/pm/` stores stable PM rules and milestone definitions.
- `tools/delivery_tracker/` stores the live slice inventory and generated current-state
  reports.
- `docs/logs/daily/` and `docs/logs/weekly/` store historical change notes, not the
  live dashboard.

## Rules

1. Do not keep repeatedly generated current reports in `docs/pm/`.
2. Do not measure delivery by chat history.
3. Do not count `future` work toward the current launch target.
4. Prefer deliverable slices over abstract task lists.
5. Prefer fixed gates over subjective status labels.
6. Let scripts generate the report; do not hand-write the current completion snapshot.

## Minimal Source Of Truth

The minimal source-of-truth flow is:

`slice inventory -> report generator -> current markdown/json`

The live inventory may be maintained by humans or agents, but the report should always
be program-derived.

## AI Boundary

AI is useful for:

- drafting or splitting slices
- proposing blockers
- clustering work into lanes
- reviewing suspicious gaps

AI should not be the durable source of truth for the current report. Once the slice data
is updated, the current report should come from a script.

## Ownership Rule

Every active slice should have:

- one owner
- one target horizon
- one lane
- one current next gate

If a slice has no owner or no horizon, it is not ready to count as managed scope.
