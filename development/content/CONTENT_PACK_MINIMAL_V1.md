# Content Pack Minimal V1

## Problem

Future content and DLC work needs stable pack identity before the project grows
more content. The current repo already has source-pack directories, but only
the tutorial narrative source pack had a manifest, and that manifest mixed
pack identity with narrative-specific schema fields.

Level: `L3 Architecture`

Date: `2026-05-12`

## Constraints

- Prepare for future content/DLC without building a plugin or mod platform.
- Keep active runtime paths unchanged.
- Keep `data/questlines/*.json` as current narrative runtime artifacts.
- Treat old pre-alpha saves aggressively, but do not add save pack pinning in
  this first content-pack slice.
- Do not touch `cardanalysis` / `combat_analysis`.

## Complexity

Essential complexity:

- each content source pack needs a stable `pack_id`
- future save/content work needs a pack `version`
- dependencies and deprecation policy need a declared shape before content grows

Accidental complexity:

- pack directories can exist without a manifest
- narrative manifest validation is domain-specific and should not become the
  universal content-pack contract
- a broad plugin framework would add more surface than the current game needs

## Options

### Option A. Keep Pack Identity Local To Each Pipeline

Let narrative, events, cards, and future content define their own manifest shape.

Pros:

- lowest immediate code churn
- each pipeline can move independently

Cons:

- future DLC/save pinning would need adapters for every content family
- agents may invent slightly different pack-id and dependency conventions

### Option B. Add A Minimal Shared Manifest Contract

Define only pack identity fields and validate active source packs.

Pros:

- gives DLC/content work a stable identity floor
- does not force all content into one schema
- keeps dependency handling declarative without a solver

Cons:

- adds one more small validator and test surface
- existing import scripts need to preserve or create manifest metadata

### Option C. Build A Full Pack Platform Now

Add discovery, dependency solving, enable/disable state, hot reload, and runtime
activation.

Pros:

- closer to a mature mod/DLC system

Cons:

- too large for the current content-free refactor window
- creates platform maintenance before the game has enough content pressure
- risks over-abstracting the architecture we are trying to simplify

## Risks

- A "minimal" manifest could grow into a full platform by accident.
- Version fields could be mistaken for a shipped compatibility promise.
- Dependency metadata could be treated as runtime ordering before there is a
  real loader.

## Recommendation

Choose **Option B**.

The V1 manifest contract is:

- `manifest.json` in each active source-pack directory
- `manifest_version`: current manifest shape, currently `1`
- `pack_id`: stable lowercase id matching the directory name
- `display_name`: human-readable label
- `version`: semver-like source-pack version
- `content_kind`: small lowercase family label, for example `narrative_source`
  or `event_source`
- `status`: source lifecycle marker
- `dependencies`: list of pack ids only; no version constraints or solver in V1
- `deprecated`: boolean deprecation marker

V1 validation checks shape, id stability, duplicate/self dependencies, and
basic semver-like versions. It intentionally does not solve dependency order,
enable/disable packs at runtime, or pin packs into save files yet.

## Counter-Review

Why not add save pinning now?

- save reset policy is clear, but pack identity should stabilize first. Save
  pinning belongs in a later small slice after active manifests are guarded.

Why not support dependency version constraints immediately?

- no active content depends on another pack yet. Pack-id dependencies give us a
  clean shape without inventing resolver semantics.

Why add this before content production?

- once content grows, changing pack ids and manifest shape becomes more
  expensive. This is cheap now and useful later.

## Decision Summary

1. Active source packs should have `manifest.json`.
2. Shared manifest validation owns only identity, version, dependency, and
   deprecation shape.
3. Domain-specific schemas stay in their own validators.
4. V1 is not a plugin platform, hot-reload system, dependency solver, or save
   pinning implementation.

## Implementation Notes

- `contexts/shared/infrastructure/content_pack_manifest.py` owns the shared
  manifest contract and read model.
- `scripts/content_pack_manifest.py` remains the CLI wrapper for validating
  source-pack manifests.
- `contexts/shared/infrastructure/content_pack_registry.py` provides a
  read-only registry over active source-pack directories. It discovers and
  groups manifests, detects duplicate pack ids, and reports missing dependency
  ids without solving load order or enabling runtime pack activation.
- The registry may be asked to fail closed on missing dependencies for
  validation/CI, but this is still not a dependency solver or runtime pack
  enablement system.
- `contexts/shared/infrastructure/content_pack_identity.py` provides a
  report-only active pack identity preview over the registry. It is a future
  resolver/save-pinning input surface only; it does not write save fields or
  choose active runtime content.
- `contexts/shared/infrastructure/content_pack_inventory.py` provides a
  report-only inventory over discovered source packs, their source files, and
  declared runtime outputs. It is a resolver input/audit surface, not runtime
  activation.
- `ContentPackRuntimeOutputIndex` is derived from the inventory and reports
  pack-to-runtime-output claims, missing output files, output collisions, and
  source packs with no declared runtime outputs. It is report-only resolver
  input, not runtime loading authority.
- `contexts/shared/infrastructure/content_pack_runtime_outputs.py` provides
  narrow report-only query helpers over the runtime-output index. The current
  helper covers narrative runtime outputs under `data/questlines/*.json` and
  can fail closed on missing outputs, collisions, or disallowed empty packs.
  It is still not a runtime resolver, loader, activation layer, or dependency
  solver.
- `contexts/shared/infrastructure/content_pack_resolver_readiness.py` combines
  the active pack identity preview with the runtime-output index into a
  report-only runtime resolver input readiness report. It can fail closed on
  missing dependencies, missing outputs, output collisions, disallowed empty
  packs, identity/index drift, or content-kind mismatches. It is still not
  runtime loading, runtime activation, save pinning, hot reload, or a
  dependency solver.
- `contexts/shared/infrastructure/content_pack_resolver_selection.py` consumes
  a clean runtime resolver readiness report and produces a report-only runtime
  resolver selection preview. It lists the runtime-output rows that a future
  resolver would be able to consider from current source-pack declarations. If
  readiness is blocked, it emits no selected rows. It is still not runtime
  loading, runtime activation, save pinning, hot reload, or a dependency
  solver.
- `contexts/shared/infrastructure/content_pack_runtime_references.py` consumes
  a clean runtime resolver selection preview and produces a report-only runtime
  reference preview. It preserves the future resolver output shape
  (`output_path`, `pack_id`, `pack_version`, `content_kind`, `manifest_path`)
  without loading JSON payloads or becoming runtime authority. If selection
  preview is blocked, it emits no references.
- `contexts/shared/infrastructure/content_pack_resolver_shadow.py` provides a
  narrative-only report-only shadow compare between runtime reference preview
  rows and the current tutorial-owned `data/questlines/*.json` runtime paths.
  It reports unmanaged current runtime paths, such as `encounters_ta.json`,
  without treating them as selection drift. It is still not runtime loading,
  runtime activation, save pinning, hot reload, or a dependency solver.
- `contexts/shared/infrastructure/content_pack_narrative_path_provider.py`
  provides a report-only narrative runtime path provider preview over the clean
  shadow compare. It groups selected tutorial runtime paths into questline,
  encounter, and reward path families for a future loader handoff, while leaving
  `QuestLoader` and active runtime loading unchanged.
- `contexts/shared/infrastructure/content_pack_quest_loader_shadow.py` provides
  a report-only QuestLoader shadow adapter preview over the narrative path
  provider preview. It checks that provider-selected questline, encounter, and
  reward paths remain visible to the current `QuestLoader` base directory and
  filename-prefix scan before any later handoff changes loading authority. It
  also reports current loader-visible paths that are not selected by the
  content-pack chain, such as `data/questlines/encounters_ta.json`, without
  treating them as runtime-output failures.
- `contexts/shared/infrastructure/content_pack_quest_loader_handoff.py`
  provides a report-only QuestLoader handoff contract preview over the clean
  shadow adapter. It exposes the future loader handoff shape: `base_dir`,
  questline paths, encounter paths, reward paths, selected pack ids, and
  allowed empty pack ids. It emits no handoff paths when the shadow adapter is
  blocked and still does not change `QuestLoader` or runtime loading.
- `contexts/shared/infrastructure/content_pack_quest_loader_promotion_readiness.py`
  provides a report-only QuestLoader promotion readiness guard over the handoff
  contract preview. It confirms the current tutorial handoff paths, required
  selected pack ids, required allowed-empty pack ids, and unmanaged
  loader-visible observations before any later slice changes `QuestLoader`
  loading authority. It still does not change `QuestLoader.load_all()`, load
  runtime JSON, activate packs, write saves, solve dependencies, or support hot
  reload.
- `docs/development/content/CONTENT_PACK_RUNTIME_RESOLVER_CONTRACT_V1.md`
  freezes the future resolver promotion contract over readiness and selection
  preview inputs. It defines the expected resolved runtime-output reference
  shape, fail-closed rules, current tutorial/slack pack state, and promotion
  criteria before any later slice turns the report-only chain into runtime
  authority.
- Active data-pipeline guards should consume `ContentPackRegistry` and
  `ContentPackInventory` when validating source-pack identity and declared
  runtime outputs. Narrative source packs should continue to prove runtime
  parity with `build_narrative_runtime.py --all --check`.
- Event source packs may be registry/inventory/runtime-output-index visible
  before they declare runtime outputs. In V1 this is an explicit allowed
  report-only state, not a missing runtime loader implementation.

## Command Runbook

- Validate current source-pack manifests and dependency completeness:
  - `python scripts/content_pack_manifest.py --discover-source-packs --require-complete-dependencies`
- Report current source-pack files and declared runtime outputs:
  - `python scripts/content_pack_inventory.py`
- Export the content-pack inventory as JSON:
  - `python scripts/content_pack_inventory.py --json`
- Report active pack identity preview:
  - `python scripts/content_pack_inventory.py --pack-identity-preview`
- Export active pack identity preview as JSON:
  - `python scripts/content_pack_inventory.py --pack-identity-preview --json`
- Report the runtime-output resolver input index:
  - `python scripts/content_pack_inventory.py --runtime-output-index`
- Export the runtime-output resolver input index as JSON:
  - `python scripts/content_pack_inventory.py --runtime-output-index --json`
- Report narrative runtime-output query inputs:
  - `python scripts/content_pack_inventory.py --narrative-runtime-outputs`
- Export narrative runtime-output query inputs as JSON:
  - `python scripts/content_pack_inventory.py --narrative-runtime-outputs --json`
- Report runtime resolver input readiness:
  - `python scripts/content_pack_inventory.py --runtime-resolver-readiness`
- Export runtime resolver input readiness as JSON:
  - `python scripts/content_pack_inventory.py --runtime-resolver-readiness --json`
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
- Report QuestLoader handoff contract preview:
  - `python scripts/content_pack_inventory.py --quest-loader-handoff-contract`
- Export QuestLoader handoff contract preview as JSON:
  - `python scripts/content_pack_inventory.py --quest-loader-handoff-contract --json`
- Report QuestLoader promotion readiness:
  - `python scripts/content_pack_inventory.py --quest-loader-promotion-readiness`
- Export QuestLoader promotion readiness as JSON:
  - `python scripts/content_pack_inventory.py --quest-loader-promotion-readiness --json`
- Review the future runtime resolver promotion contract:
  - `docs/development/content/CONTENT_PACK_RUNTIME_RESOLVER_CONTRACT_V1.md`
- Validate content-pack registry/inventory contracts:
  - `python -m pytest tests/shared/test_content_pack_registry.py tests/shared/test_content_pack_inventory.py tests/scripts/test_content_pack_manifest.py -q`
