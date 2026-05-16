# Content Pack Runtime Resolver Contract V1

## Purpose

Define the content-pack runtime resolver contract now that resolved runtime
references have become runtime authority for promoted helper boundaries.

This document freezes the input and output shape that promoted runtime loaders
must satisfy. It activates resolved runtime references as the authority for
promoted helper boundaries, but it does not activate packs, write save data,
solve dependencies, support hot reload, or change current runtime artifact
paths.

## Current Inputs

The future resolver may only promote from the existing report-only chain after
the chain is clean:

- `ContentPackActiveSet`
  - names the pack ids enabled for the current resolver build
  - defaults to all discovered active source packs, currently `ta`, `slack`,
    and `tutorial`
  - can accept explicit pack ids for tests, CLI reports, and future activation
    inputs
  - fails closed on unknown pack ids, inactive requested packs, or selected
    packs whose declared dependencies are not also selected
  - is not a dependency solver, runtime activation layer, save pack pinning
    source, hot-reload mechanism, or UI DLC selector
- `ContentPackRuntimeResolverReadinessReport`
  - confirms active pack identity and runtime-output index consistency
  - consumes the active pack set before comparing identity and runtime-output
    index inputs
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

- `python scripts/content_pack_inventory.py --active-pack-set`
- `python scripts/content_pack_inventory.py --active-pack-set --json`
- `python scripts/content_pack_inventory.py --active-pack-set --active-pack-id tutorial`
- `python scripts/content_pack_inventory.py --runtime-resolver-readiness`
- `python scripts/content_pack_inventory.py --runtime-resolver-readiness --json`
- `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview`
- `python scripts/content_pack_inventory.py --runtime-resolver-selection-preview --json`
- `python scripts/content_pack_inventory.py --runtime-reference-preview`
- `python scripts/content_pack_inventory.py --runtime-reference-preview --json`
- `python scripts/content_pack_inventory.py --runtime-resolver`
- `python scripts/content_pack_inventory.py --runtime-resolver --json`
- `python scripts/content_pack_inventory.py --runtime-resolver --active-pack-id tutorial --json`
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
- `python scripts/content_pack_inventory.py --combat-encounter-loader-shadow`
- `python scripts/content_pack_inventory.py --combat-encounter-loader-shadow --json`
- `python scripts/content_pack_inventory.py --campaign-reward-loader-shadow`
- `python scripts/content_pack_inventory.py --campaign-reward-loader-shadow --json`

## Resolver Output Shape

The runtime resolver exposes resolved runtime-output references. Each reference
carries enough identity to explain where the runtime file came from:

- `output_path`
- `pack_id`
- `pack_version`
- `content_kind`
- `manifest_path`

The first implementation preserves the selected-row identity already emitted by
`ContentPackRuntimeResolverSelectionPreview`. The resolver does not load JSON
payloads or parse domain objects itself; promoted loader boundaries consume its
resolved paths and perform their own current loading work.

The resolver result also reports `activation_mode`, `requested_pack_ids`,
`active_pack_ids`, and `discovered_active_pack_ids`. These fields are the
current resolver input selection, not shipped DLC activation state and not save
pinning. When explicit pack ids are supplied, only selected active packs
contribute resolved runtime references; allowed empty packs such as `slack`
remain visible as allowed empty inputs when selected.

The current `ContentPackRuntimeReferencePreview` remains the report-only
rehearsal of this output shape. `content_pack_runtime_resolver.py` is the
runtime authority over the clean resolved reference set. Its authority boundary
is `runtime_authority_over_resolved_pack_runtime_references`.

## Fail-Closed Rules

A resolver implementation fails closed before returning authoritative runtime
references when any of these input issues exist:

- an explicit active pack id is unknown
- an explicit active pack id exists but is not an active source pack
- a selected pack declares a dependency that is missing or not also selected
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

The runtime authority promotion is valid only while these checks stay true:

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
- the combat encounter loader shadow is clean for current loader-visible
  `encounters_*.json` runtime outputs, including tutorial and TA encounter
  files, before a separate combat-specific handoff changes authority
- the campaign reward loader shadow is clean for current loader-visible
  `rewards_*.json` runtime outputs, including the tutorial reward file, before
  a separate reward-specific handoff changes authority
- slack remains visible as an allowed empty `event_source` pack
- shadow comparison against current runtime paths passes before ownership
  changes
- focused tests name the explicit resolver family being promoted
- the PR description states which runtime paths become resolver-owned

Current resolver-owned runtime paths are:

- `data/questlines/encounters_ta.json`
- `data/questlines/encounters_tutorial.json`
- `data/questlines/questline_tutorial.json`
- `data/questlines/rewards_tutorial.json`

## Non-Goals

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
- `contexts/shared/infrastructure/content_pack_runtime_resolver.py` owns the
  authoritative resolved runtime-reference set. It promotes clean preview rows
  into resolver-owned references, fails closed when preview inputs are blocked,
  and still does not parse runtime JSON payloads.
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
- `QuestLoader.load_from_runtime_paths()` is the explicit-path loader entry for
  promoted content-pack handoffs. It can load caller-provided questline,
  encounter, and reward JSON paths without directory prefix scanning.
- `contexts/shared/infrastructure/content_pack_quest_loader_factory.py`
  currently owns the QuestLoader handoff factory. It can build a loaded
  `QuestLoader` from clean handoff/promotion inputs.
- `contexts/shared/infrastructure/content_pack_narrative_loader.py` currently
  owns the first runtime loader promotion boundary for narrative startup. It
  uses the verified handoff factory to load tutorial narrative runtime paths
  without directory prefix scanning.
- `contexts/shared/infrastructure/content_pack_quest_loader_load_all_guard.py`
  currently owns the report-only guard for production `QuestLoader.load_all()`
  call sites. The default allowed set is empty; new narrative, combat, reward,
  or resolver-owned paths should use promoted content-pack handoff boundaries
  instead of returning to directory prefix scanning.
- `contexts/shared/infrastructure/campaign_reward_loader.py` currently owns
  campaign reward-definition lookup as a narrow content-pack resolver consumer.
  It loads resolver-owned `rewards_*.json` paths through
  `QuestLoader.load_from_runtime_paths()` and no longer calls
  `QuestLoader.load_all()`.
- `contexts/shared/infrastructure/combat_encounter_loader.py` currently owns
  combat encounter-definition lookup as a narrow content-pack resolver
  consumer. It loads resolver-owned `encounters_*.json` paths, including TA and
  tutorial encounter files, through `QuestLoader.load_from_runtime_paths()` and
  no longer calls `QuestLoader.load_all()`.
- `contexts/shared/infrastructure/content_pack_combat_encounter_loader_shadow.py`
  currently owns the report-only combat encounter helper shadow. It verifies
  that `data/questlines/encounters_tutorial.json` and
  `data/questlines/encounters_ta.json` are declared, present, collision-free,
  and visible through the current combat encounter helper. It preserves
  `slack` as an allowed empty-runtime-output pack and is not runtime loading
  authority.
- `contexts/shared/infrastructure/content_pack_campaign_reward_loader_shadow.py`
  currently owns the report-only campaign reward helper shadow. It verifies
  that `data/questlines/rewards_tutorial.json` is declared, present,
  collision-free, and visible through the current campaign reward helper. It
  preserves `slack` as an allowed empty-runtime-output pack and is not runtime
  loading authority.
