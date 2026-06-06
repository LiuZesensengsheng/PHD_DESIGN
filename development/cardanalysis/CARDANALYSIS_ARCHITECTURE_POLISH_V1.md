# Cardanalysis Architecture Polish V1

## Problem

The current programmatic complete-card draft chain is useful but still large.
The biggest maintenance risk is not one oversized module by itself; it is drift
between four surfaces that describe the same hosted repair path:

- the unified repair-stage CLI,
- the hosted-router command plan,
- the repair-stage descriptor registry,
- focused tests and tmp-independent fixtures.

When those surfaces disagree, future agents can accidentally revive old wrappers,
depend on historical `tmp/combat_analysis` outputs, or create another parallel
repair route with the same meaning.

## Constraints

- Keep all cardanalysis output `report_only` / `advisory_context_only`.
- Do not write runtime card data or promote formal cards.
- Do not create hard gates, change score weights, change default synthesis, enable
  learned/reranker paths, call LLM/API, or promote speculative/source-mined
  material to reviewed evidence.
- Do not do a broad rewrite while the system is still learning from human review.
- Normal implementation branches should not edit daily logs.

## Complexity

The essential complexity is the design loop itself: generated hypothesis drafts,
schema validation, advisory exams, Chinese review packets, and repair iterations.

The accidental complexity is duplicated route metadata: old stage names,
per-stage wrapper history, command text in the router, and tests that can silently
fall back to old `tmp` snapshots.

## Options

1. Keep only the current unified CLI and accept metadata drift.
   - Low immediate cost.
   - Leaves the hosted router and archive plan weaker.

2. Add descriptor parity around the existing unified repair-stage CLI.
   - Small implementation cost.
   - Gives the router, tests, and future archive decisions one shared contract.

3. Rewrite the repair-stage modules into one large stage engine now.
   - Highest cleanup potential.
   - Too risky while card quality rules are still changing quickly.

## Risks

- Descriptor metadata can become stale if a future stage is added only to the CLI.
- Tests can overfit to implementation names if they assert too much incidental text.
- A descriptor registry may look like delete approval unless the archive boundary is
  explicit.

## Recommendation

Superseded by the later slimming pass.

The former unified repair-stage entrypoint and descriptor registry have been
retired along with the historical round-named repair-stage modules. The hosted
router should still read old report-only snapshots, but when an old route asks
to continue that retired chain it must stop with
`stop_for_retired_repair_stage_route` and point the next pass toward current
generation, exam, advisory-input, or Chinese human-review routes.

Focused tests should enforce:

- retired repair-stage routes do not produce command plans,
- old snapshot contracts remain readable for handoff decisions,
- tmp-independent tests do not depend on repository historical outputs,
- report-only/advisory boundaries remain unchanged.

## Counter-Review

This does not meaningfully shrink the largest modules yet. It is still worth doing
because it makes later shrinking safer: once route metadata, router suggestions, and
tests agree, old wrappers or repeated stage surfaces can be archived with less
guesswork.

The next larger cleanup should not start until this smaller parity contract is green
and the owner agrees which stage modules are historical versus active.

## Decision Summary

Adopt a small architecture polish pass:

- no broad rewrite,
- no new card-generation capability,
- keep the unified repair-stage CLI as the default entrypoint,
- keep descriptor/router/test parity as the guard against route drift,
- continue using focused tmp-independent fixtures for cardanalysis repair tests.
