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
- `contexts/shared/infrastructure/content_pack_inventory.py` provides a
  report-only inventory over discovered source packs, their source files, and
  declared runtime outputs. It is a resolver input/audit surface, not runtime
  activation.
- Active data-pipeline guards should consume `ContentPackRegistry` and
  `ContentPackInventory` when validating source-pack identity and declared
  runtime outputs. Narrative source packs should continue to prove runtime
  parity with `build_narrative_runtime.py --all --check`.
- Event source packs may be registry/inventory visible before they declare
  runtime outputs. In V1 this is an explicit report-only state, not a missing
  runtime loader implementation.

## Command Runbook

- Validate current source-pack manifests and dependency completeness:
  - `python scripts/content_pack_manifest.py --discover-source-packs --require-complete-dependencies`
- Report current source-pack files and declared runtime outputs:
  - `python scripts/content_pack_inventory.py`
- Export the content-pack inventory as JSON:
  - `python scripts/content_pack_inventory.py --json`
- Validate content-pack registry/inventory contracts:
  - `python -m pytest tests/shared/test_content_pack_registry.py tests/shared/test_content_pack_inventory.py tests/scripts/test_content_pack_manifest.py -q`
