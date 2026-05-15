# Content Pack Runtime Resolver Readiness V1

## Purpose

Create a report-only readiness surface for the future content-pack runtime
resolver.

This layer answers whether the resolver's current inputs are internally
consistent. It does not load content, choose active runtime files, activate
packs, write saves, solve dependencies, or support hot reload.

## Inputs

- `ContentPackIdentityPreview`
  - active source pack ids
  - versions
  - content kinds
  - dependency ids
  - manifest paths
- `ContentPackRuntimeOutputIndex`
  - pack-to-runtime-output claims
  - missing runtime output files
  - runtime output collisions
  - packs with no declared runtime outputs
  - content kinds currently allowed to have no runtime outputs

## Output

`ContentPackRuntimeResolverReadinessReport` is the report-only read model for
the next resolver slice.

It reports:

- current active pack ids
- allowed empty-runtime-output content kinds
- per-pack runtime output summaries
- missing dependencies
- missing runtime outputs
- runtime output collisions
- disallowed empty-runtime-output packs
- identity/index drift
- content-kind mismatches between identity and runtime-output inputs

The current clean label is:

- `resolver_inputs_ready`

The current blocked label is:

- `blocked_on_resolver_input_issues`

The next report-only layer is
`ContentPackRuntimeResolverSelectionPreview`. It may consume a clean readiness
report to preview selected runtime-output rows, but it still does not load or
activate runtime content.

## Fail-Closed Conditions

`require_content_pack_runtime_resolver_readiness_report()` fails closed when any
of these conditions appear:

- a declared dependency id is missing
- a declared runtime output file is missing
- multiple packs claim the same runtime output path
- a pack has no runtime outputs and its `content_kind` is not allowed-empty
- identity preview and runtime-output index disagree about pack ids
- identity preview and runtime-output index disagree about a pack's content kind

## Current Pack State

- `tutorial` is a `narrative_source` pack and must keep declaring the three
  current narrative runtime outputs:
  - `data/questlines/encounters_tutorial.json`
  - `data/questlines/questline_tutorial.json`
  - `data/questlines/rewards_tutorial.json`
- `slack` is an `event_source` pack with no runtime outputs. That remains an
  allowed report-only state in V1.

## Non-Goals

- no runtime loading changes
- no resolver activation
- no dependency solver
- no save schema or pack pinning
- no plugin or mod platform
- no hot reload
- no UI changes
- no combat balance changes
- no `cardanalysis` or `combat_analysis` changes

## Commands

- Report runtime resolver input readiness:
  - `python scripts/content_pack_inventory.py --runtime-resolver-readiness`
- Export runtime resolver input readiness as JSON:
  - `python scripts/content_pack_inventory.py --runtime-resolver-readiness --json`
- Validate the focused read model:
  - `py -3.11 -m pytest tests/shared/test_content_pack_resolver_readiness.py tests/shared/test_content_pack_identity.py tests/shared/test_content_pack_runtime_outputs.py tests/shared/test_content_pack_inventory.py tests/scripts/test_data_pipeline_contracts.py -q`
