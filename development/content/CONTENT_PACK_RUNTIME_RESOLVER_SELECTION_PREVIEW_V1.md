# Content Pack Runtime Resolver Selection Preview V1

## Purpose

Create a report-only dry run for the future content-pack runtime resolver.

This layer previews which active source pack currently declares each runtime
output after the resolver input readiness report is clean. It does not load
runtime JSON, choose game runtime content, activate packs, write saves, solve
dependencies, or support hot reload.

## Input

- `ContentPackRuntimeResolverReadinessReport`

The selection preview only produces selected rows when the readiness report has
no readiness issues.

The next report-only layer is the narrative resolver shadow compare. It may use
selected `narrative_source` rows to compare future resolver input against the
current tutorial-owned `data/questlines/*.json` runtime paths, but it still does
not load or activate runtime content.

The selection preview can also feed the runtime reference preview, which maps
clean selected rows into the future resolver output shape. That reference
preview is still report-only, emits no references when selection is blocked, and
does not make the selected rows authoritative runtime input.

After the shadow compare is clean, the narrative path provider preview may group
selected paths into questline, encounter, and reward families for a future
loader handoff. That preview is still report-only and does not change
`QuestLoader`.

After the path provider preview is clean, the QuestLoader shadow adapter preview
may compare those grouped paths with the current `QuestLoader` base directory
and filename-prefix scan. That adapter preview is still report-only and does not
call or change `QuestLoader.load_all()`.

## Output

`ContentPackRuntimeResolverSelectionPreview` reports:

- active source pack ids
- selected runtime-output rows
- allowed empty-runtime-output pack ids
- blocked pack ids when readiness is not clean
- readiness label and readiness blockers

Each selected row contains:

- runtime output path
- pack id
- pack version
- content kind
- manifest path
- `selected_report_only` status

## Current Pack State

- `tutorial` is selected for the three current narrative runtime outputs:
  - `data/questlines/encounters_tutorial.json`
  - `data/questlines/questline_tutorial.json`
  - `data/questlines/rewards_tutorial.json`
- `slack` remains an allowed empty-runtime-output `event_source` pack and has
  no selected runtime outputs.

## Blocked Behavior

If readiness has missing dependencies, missing outputs, collisions, disallowed
empty packs, identity/index drift, or content-kind mismatches, the preview is
blocked and emits no selected runtime-output rows.

## Non-Goals

- no runtime loading
- no runtime activation
- no save schema or pack pinning
- no dependency solver
- no plugin or mod platform
- no hot reload
- no UI changes
- no combat balance changes
- no `cardanalysis` or `combat_analysis` changes

## Commands

- Report runtime resolver selection preview:
  - `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview`
- Export runtime resolver selection preview as JSON:
  - `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview --json`
- Report runtime reference preview:
  - `python scripts/content_pack_inventory.py --runtime-reference-preview`
- Export runtime reference preview as JSON:
  - `python scripts/content_pack_inventory.py --runtime-reference-preview --json`
- Report narrative runtime resolver shadow compare:
  - `python scripts/content_pack_inventory.py --narrative-resolver-shadow-compare`
- Export narrative runtime resolver shadow compare as JSON:
  - `python scripts/content_pack_inventory.py --narrative-resolver-shadow-compare --json`
- Report narrative runtime path provider preview:
  - `python scripts/content_pack_inventory.py --narrative-path-provider-preview`
- Export narrative runtime path provider preview as JSON:
  - `python scripts/content_pack_inventory.py --narrative-path-provider-preview --json`
- Report QuestLoader shadow adapter preview:
  - `python scripts/content_pack_inventory.py --quest-loader-shadow-adapter`
- Export QuestLoader shadow adapter preview as JSON:
  - `python scripts/content_pack_inventory.py --quest-loader-shadow-adapter --json`
- Validate the focused preview:
  - `py -3.11 -m pytest tests/shared/test_content_pack_resolver_selection.py tests/shared/test_content_pack_runtime_references.py tests/shared/test_content_pack_resolver_readiness.py tests/shared/test_content_pack_narrative_path_provider.py tests/shared/test_content_pack_quest_loader_shadow.py tests/scripts/test_data_pipeline_contracts.py -q`
