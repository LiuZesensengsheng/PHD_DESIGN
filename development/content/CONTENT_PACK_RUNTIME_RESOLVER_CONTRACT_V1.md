# Content Pack Runtime Resolver Contract V1

## Purpose

Define the future content-pack runtime resolver contract before it becomes
runtime authority.

This document freezes the input and output shape that a later implementation
must satisfy. It does not implement runtime loading, activate packs, write save
data, solve dependencies, or change current runtime paths.

## Current Inputs

The future resolver may only promote from the existing report-only chain after
the chain is clean:

- `ContentPackRuntimeResolverReadinessReport`
  - confirms active pack identity and runtime-output index consistency
  - fails closed on missing dependencies, missing outputs, collisions,
    disallowed empty packs, identity/index drift, or content-kind mismatch
- `ContentPackRuntimeResolverSelectionPreview`
  - previews the runtime-output rows that a future resolver could consider
  - emits no selected rows while readiness is blocked
  - keeps allowed empty-runtime-output packs visible without treating them as
    runtime content
- `ContentPackRuntimeReferencePreview`
  - previews the resolved runtime-output reference shape that a future resolver
    should return
  - emits no references while selection preview is blocked
  - remains report-only and explicitly not runtime authority

The current CLI surfaces are:

- `python scripts/content_pack_inventory.py --runtime-resolver-readiness`
- `python scripts/content_pack_inventory.py --runtime-resolver-readiness --json`
- `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview`
- `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview --json`
- `python scripts/content_pack_inventory.py --runtime-reference-preview`
- `python scripts/content_pack_inventory.py --runtime-reference-preview --json`
- `python scripts/content_pack_inventory.py --narrative-path-provider-preview`
- `python scripts/content_pack_inventory.py --narrative-path-provider-preview --json`
- `python scripts/content_pack_inventory.py --quest-loader-shadow-adapter`
- `python scripts/content_pack_inventory.py --quest-loader-shadow-adapter --json`
- `python scripts/content_pack_inventory.py --quest-loader-handoff-contract`
- `python scripts/content_pack_inventory.py --quest-loader-handoff-contract --json`
- `python scripts/content_pack_inventory.py --quest-loader-promotion-readiness`
- `python scripts/content_pack_inventory.py --quest-loader-promotion-readiness --json`
- `python scripts/content_pack_inventory.py --quest-loader-handoff-factory`
- `python scripts/content_pack_inventory.py --quest-loader-handoff-factory --json`

## Resolver Output Shape

When a later slice promotes this contract into runtime authority, the resolver
output should expose resolved runtime-output references. Each reference should
carry enough identity to explain where the runtime file came from:

- `output_path`
- `pack_id`
- `pack_version`
- `content_kind`
- `manifest_path`

The first implementation should preserve the selected-row identity already
emitted by `ContentPackRuntimeResolverSelectionPreview`. The contract does not
require JSON payload loading, parsed domain objects, or gameplay activation in
the same slice.

The current `ContentPackRuntimeReferencePreview` is the report-only rehearsal of
this output shape. It is not a runtime resolver and must not be used as
authoritative game loading input until a later promotion PR changes that
boundary explicitly.

## Fail-Closed Rules

A resolver implementation must fail closed before returning authoritative
runtime references when any of these input issues exist:

- a declared dependency id is missing
- a declared runtime output file is missing
- multiple packs claim the same runtime output path
- a pack has no runtime outputs and its `content_kind` is not allowed-empty
- active pack identity and runtime-output index disagree about pack ids
- active pack identity and runtime-output index disagree about a pack's
  `content_kind`
- selected runtime-output rows contain a `content_kind` that the resolver slice
  does not explicitly handle

The current allowed-empty content kind is:

- `event_source`

That allowed-empty status is report-only visibility. It is not a hidden loader
and not a promise that event source packs have runtime activation.

## Current Pack State

- `tutorial` is a `narrative_source` pack. It must continue to declare and own
  the three current narrative runtime outputs:
  - `data/questlines/encounters_tutorial.json`
  - `data/questlines/questline_tutorial.json`
  - `data/questlines/rewards_tutorial.json`
- `ta` is a `combat_source` pack. It currently declares and owns:
  - `data/questlines/encounters_ta.json`
  This ownership is visible in the global resolver-input read model only; it
  does not make TA part of the tutorial narrative path provider or QuestLoader
  handoff chain. QuestLoader shadow/promotion reports classify it as a
  pack-owned non-handoff loader-visible sidecar rather than a truly unmanaged
  path.
- `slack` is an `event_source` pack with no runtime outputs. That remains an
  allowed empty-runtime-output report-only state in V1, not an error.

## Promotion Criteria

Before this contract becomes runtime authority, a later PR must prove:

- runtime resolver readiness is clean
- runtime resolver selection preview is clean
- runtime reference preview is clean and preserves the resolved reference shape
- selected tutorial narrative runtime outputs match the current active
  `data/questlines/*.json` paths
- the narrative runtime resolver shadow compare is clean for tutorial-owned
  runtime outputs after consuming runtime reference preview rows
- the narrative runtime path provider preview can group selected paths into
  questline, encounter, and reward families
- the QuestLoader shadow adapter preview confirms those provider paths are
  visible to the current `QuestLoader` base directory and filename-prefix scan
- the QuestLoader handoff contract preview is clean and exposes the future
  loader handoff shape without taking loading authority
- the QuestLoader promotion readiness guard is clean, preserves the tutorial
  three-path handoff, keeps `slack` visible as required allowed-empty input,
  and preserves TA encounter ownership as global resolver-input state without
  adding `data/questlines/encounters_ta.json` to the tutorial QuestLoader
  handoff
- slack remains visible as an allowed empty `event_source` pack
- shadow comparison against current runtime paths passes before ownership
  changes
- focused tests name the explicit resolver family being promoted
- the PR description states which runtime paths become resolver-owned

## Non-Goals

- no runtime JSON loading in this contract slice
- no `QuestLoader.load_all()` changes in this contract slice
- no runtime activation
- no save schema changes or pack pinning
- no dependency solver
- no plugin or mod platform
- no hot reload
- no UI changes
- no combat balance changes
- no `cardanalysis` or `combat_analysis` changes
- no content directory migration

## Relationship To Existing Docs

- `CONTENT_PACK_MINIMAL_V1.md` owns the overall minimal content-pack direction.
- `CONTENT_PACK_RUNTIME_RESOLVER_READINESS_V1.md` owns resolver input readiness.
- `CONTENT_PACK_RUNTIME_RESOLVER_SELECTION_PREVIEW_V1.md` owns report-only
  selected-row preview.
- This document owns the future promotion contract from report-only selected
  rows to resolver-owned runtime references.
- `contexts/shared/infrastructure/content_pack_runtime_references.py` currently
  owns the report-only runtime reference preview for the future resolver output
  shape. It does not load runtime JSON or change loading authority.
- `contexts/shared/infrastructure/content_pack_resolver_shadow.py` currently
  owns the narrative-only shadow compare that checks runtime reference preview
  rows against current tutorial-owned runtime paths without taking loading
  authority.
- `contexts/shared/infrastructure/content_pack_narrative_path_provider.py`
  currently owns the report-only narrative path provider preview for the future
  loader handoff. It does not change `QuestLoader`.
- `contexts/shared/infrastructure/content_pack_quest_loader_shadow.py`
  currently owns the report-only QuestLoader shadow adapter preview. It checks
  provider paths against the current loader prefix contract before any later
  slice changes loading authority.
- `contexts/shared/infrastructure/content_pack_quest_loader_handoff.py`
  currently owns the report-only QuestLoader handoff contract preview. It
  defines the future loader handoff input shape without changing
  `QuestLoader.load_all()`.
- `contexts/shared/infrastructure/content_pack_quest_loader_promotion_readiness.py`
  currently owns the report-only QuestLoader promotion readiness guard. It is a
  final promotion-input check before runtime loading changes, not runtime
  authority.
- `QuestLoader.load_from_runtime_paths()` is the inactive explicit-path loader
  entry for the future handoff. It can load caller-provided questline,
  encounter, and reward JSON paths without directory prefix scanning, but
  current runtime call sites still use `QuestLoader.load_all()` until a later
  promotion PR explicitly changes loading authority.
- `contexts/shared/infrastructure/content_pack_quest_loader_factory.py`
  currently owns the QuestLoader handoff factory. It can build a loaded
  `QuestLoader` from clean handoff/promotion inputs.
- `contexts/shared/infrastructure/content_pack_narrative_loader.py` currently
  owns the first runtime loader promotion boundary for narrative startup. It
  uses the verified handoff factory to load tutorial narrative runtime paths
  without directory prefix scanning. Combat startup still uses
  `QuestLoader.load_all()` and continues to see TA encounter sidecar content
  through the existing path until a separate combat/loader promotion slice
  changes that authority.
- `contexts/shared/infrastructure/content_pack_quest_loader_load_all_guard.py`
  currently owns the report-only guard for remaining production
  `QuestLoader.load_all()` call sites. It allows only the current legacy
  combat/campaign surfaces and is not runtime authority. New narrative or
  resolver-owned paths should use promoted content-pack handoff boundaries
  instead of returning to directory prefix scanning.
