# Narrative Pipeline V1

## Goal

Define one explicit pipeline for campaign-side narrative events so the project
can:

- keep one real runtime path
- give planners and AI a stable content authoring flow
- avoid parallel legacy event models drifting apart
- add stronger automated validation before narrative content reaches runtime

This document covers narrative/campaign events such as:

- dialogue-like story nodes
- event choices
- event consequences
- reward triggers
- combat-entry triggers
- return-to-campaign narrative flows

It does not cover:

- combat fact events such as `CardDrawn` or `EnemyTookDamage`
- raw pygame input events
- campaign task-area board rules

## Why This Exists

The repo currently has three partially overlapping narrative-content paths:

1. legacy flat event JSON under `contexts/campaign/infrastructure/events/`
2. draft/import content under `data/events_drafts/` and `data/events_src/`
3. active runtime questline content under `data/questlines/`

The runtime mainline already favors:

- `QuestLoader`
- `QuestRuntime`
- `NarrativeApplicationService`
- `EventState`

But the authoring and legacy layers still look split enough that humans and
Codex can reasonably ask:

- which layer is the real source of truth
- which files are safe to edit
- whether old event JSON is still a valid active path

V1 exists to answer those questions clearly.

## North-Star Rule

Prefer:

`authoring draft -> normalized narrative source -> runtime build -> questline runtime -> narrative runtime`

Do not prefer:

`edit whichever narrative file already exists and hope it reaches runtime`

## Current State

### Current Active Runtime Path

The current runtime mainline is:

- `data/questlines/*.json`
- `contexts/shared/quest_loader.py`
- `contexts/shared/quest_runtime.py`
- `contexts/narrative/application/service.py`
- `contexts/event/state.py`

### Current Legacy / Side Paths

These are not the preferred future runtime path:

- `contexts/campaign/infrastructure/events/*.json`
- `contexts/campaign/infrastructure/json_event_repository.py`
- `contexts/campaign/application/campaign_service.py`

These may still be useful for migration reference or temporary compatibility,
but they should not keep growing as active narrative-runtime sources.

### Current Draft / Import Path

The repo also already contains draft-side content tooling:

- `data/events_drafts/*.csv`
- `data/events_src/packs/*`
- `scripts/validate_events_draft.py`
- `scripts/import_events_draft_to_events_src.py`

This is useful pipeline groundwork, but it is not yet the same thing as a
fully owned runtime narrative pipeline.

## V1 Target State

V1 defines a six-layer narrative pipeline.

### 1. Authoring Draft Layer

Purpose:

- planner-friendly and AI-friendly editing surface
- human-readable Chinese copy
- lightweight content notes and simple DSLs

Suggested directory:

```text
data/narrative_drafts/
  <pack>/
    *.csv
```

Rules:

- drafts are editable source for planners
- drafts are not read by runtime
- drafts may use convenience columns that do not survive to runtime

### 2. Normalized Narrative Source Layer

Purpose:

- canonical structured source for narrative content
- diff-friendly, traceable, deterministic input to runtime build

Suggested directory:

```text
data/narrative_src/packs/<pack>/
  manifest.json
  nodes.csv
  choices.csv
  consequences.csv
  conditions.csv
  locales_zh_CN.csv
  _draft_id_map.csv
```

Rules:

- this is the target source of truth after V1 lands
- narrative runtime should not hand-read drafts directly
- authoring imports should converge here before runtime build
- import tooling should preserve stable IDs when content is semantically unchanged
  (for example: choice reorder should not force ID churn)

### 3. Runtime Build Layer

Purpose:

- compile normalized source into active runtime questline artifacts
- validate references before runtime
- guarantee deterministic output

Suggested scripts:

- `scripts/validate_narrative_draft.py`
- `scripts/import_narrative_draft_to_src.py`
- `scripts/build_narrative_runtime.py`
- `scripts/check_narrative_runtime.py`

Rules:

- build scripts own compilation and structural validation
- runtime code must not silently rebuild narrative content on demand
- build outputs should be reproducible from checked-in source files
- multi-pack build mode should fail fast on runtime ID/output collisions instead
  of silently overriding artifacts

### 4. Runtime Artifact Layer

Purpose:

- the serialized narrative payloads actually loaded by the runtime

Active directory:

```text
data/questlines/
  questline_*.json
  rewards_*.json
```

Rules:

- runtime loads these files only
- they are considered build outputs in the target model
- direct hand editing may remain temporarily possible during migration, but it
  should not be the steady-state workflow

### 5. Narrative Runtime Layer

Purpose:

- evaluate node availability
- surface visible choices
- apply consequences
- produce runtime-safe high-level transition requests

Active modules:

- `contexts/shared/quest_loader.py`
- `contexts/shared/quest_runtime.py`
- `contexts/narrative/application/service.py`

Rules:

- narrative runtime reads runtime artifacts only
- narrative runtime should output high-level consequences, not UI behavior
- runtime should not depend on legacy campaign event repositories

### 6. Presentation Layer

Purpose:

- show narrative pages
- show choices
- consume acknowledgement / continue flow
- route selected choice into narrative runtime

Active modules:

- `contexts/event/state.py`
- related event/dialogue view modules

Rules:

- presentation owns rendering and local interaction only
- presentation must not become the place where consequence rules are encoded

## Suggested Directory Shape

The target shape for narrative content should be:

```text
data/
  narrative_drafts/
    tutorial/
    slack/

  narrative_src/
    packs/
      tutorial/
        manifest.json
        nodes.csv
        choices.csv
        consequences.csv
        conditions.csv
        locales_zh_CN.csv
        _draft_id_map.csv
      slack/
        ...

  questlines/
    questline_tutorial.json
    rewards_tutorial.json
    ...
```

This keeps:

- authoring convenience
- normalized machine-friendly source
- compiled runtime artifacts

as three separate concerns.

## Ownership By Layer

### Draft Layer Owns

- planner-facing copy
- rough scenario assembly
- convenience columns
- notes for future iteration

Draft layer must not own:

- runtime-only IDs outside the stable mapping rules
- direct runtime transition payload format
- ad hoc Python logic

### Normalized Source Layer Owns

- stable node IDs
- stable choice IDs
- explicit conditions and consequences
- locale keys and pack-local localization payloads
- source traceability

Normalized source must not own:

- runtime session state
- UI presentation behavior
- arbitrary callback hooks

### Build Layer Owns

- schema validation
- reference validation
- runtime artifact generation
- deterministic output rules

Build layer must not own:

- gameplay runtime execution
- UI rendering
- save/write side effects beyond its own build outputs

### Runtime Layer Owns

- availability checks
- consequence application
- transition request surfacing
- runtime-safe interpretation of the built questline model

Runtime layer must not own:

- draft parsing
- direct editing workflows
- legacy event JSON interpretation in the steady-state model

### Presentation Layer Owns

- page flow
- option button display
- continue / acknowledge interaction
- delegation into runtime services

Presentation layer must not own:

- business sequencing rules
- cross-context persistent writes
- reward/combat payload construction details

## Narrative Capability Whitelist

V1 should keep narrative consequences explicit and intentionally small.

Allowed high-level consequence families:

- `GOTO_NODE`
- `SET_FLAG`
- `CLEAR_FLAG`
- `MODIFY_QUEST_VARS`
- `MODIFY_PLAYER_STATS`
- `ADD_PLAYER_BUFF`
- `SHOW_REWARD`
- `START_COMBAT`

Conditions should likewise stay explicit and finite, for example:

- flag checks
- quest-var comparisons
- player-stat threshold checks
- pack/tag gates when needed

Do not allow V1 narrative content to depend on:

- arbitrary Python callbacks
- direct save-file writes
- direct combat-object mutation
- direct UI-side scripting
- hidden imports into unrelated runtime modules

## Source-Of-Truth Rules During Migration

The target V1 truth model is:

- normalized narrative source under `data/narrative_src/`

But the repo is not there yet.

So the migration rules should be:

1. runtime continues loading `data/questlines/*.json`
2. no new growth should be added to legacy
   `contexts/campaign/infrastructure/events/*.json`
3. new narrative pipeline implementation work should target the normalized
   narrative-source model, not the legacy event model
4. once build parity is landed for the active tutorial path, the normalized
   source becomes the formal source of truth and runtime artifacts become build
   outputs

This avoids pretending the migration is already complete while still defining
the correct destination.

## Validation Model

V1 narrative pipeline should be protected by four validation layers.

### A. Draft Contract Validation

Protect:

- required columns
- required text fields
- DSL parsing
- draft ID uniqueness

Typical entrypoint:

- `python scripts/validate_narrative_draft.py`

### B. Source / Build Contract Validation

Protect:

- normalized-source completeness
- node/choice/consequence references
- locale-key consistency
- deterministic build output

Typical entrypoints:

- `python scripts/build_narrative_runtime.py`
- pytest contract tests for source/build parity

### C. Runtime Contract Validation

Protect:

- `questline_*.json` loadability
- condition evaluation shape
- consequence interpretation shape
- reward/combat references

Typical test areas:

- `tests/shared/test_quest_loader.py`
- `tests/shared/test_quest_runtime.py`
- `tests/shared/test_data_validation.py`

### D. Scenario Acceptance Validation

Protect:

- entering a narrative event
- selecting a valid choice
- feedback/ack flow
- reward or combat trigger
- return to campaign
- persistence of the intended outcome

Typical test style:

- headless scenario regression under `tests/shared/`

## Legacy Policy

The following should be treated as legacy after V1 is accepted:

- `contexts/campaign/application/campaign_service.py`
- `contexts/campaign/domain/event.py`
- `contexts/campaign/domain/event_repository.py`
- `contexts/campaign/infrastructure/json_event_repository.py`
- `contexts/campaign/infrastructure/events/*.json`

Legacy policy means:

- do not extend them with new narrative behavior
- use them only for migration reference or scheduled retirement work
- keep them out of new runtime design discussions

## Non-Goals

V1 does not aim to:

- build a general-purpose scripting VM
- replace combat event dispatch
- create a giant universal content pipeline for every subsystem at once
- rewrite event presentation into a node engine
- solve final narrative writing quality by architecture alone

## Recommended Next Step

The next engineering move after this document is:

1. freeze legacy narrative growth
2. define the normalized narrative-source schema
3. build the first source -> runtime compiler for the active tutorial path
4. add scenario acceptance coverage
5. then retire legacy narrative runtime routes in batches

## Current Conclusion

The project should treat narrative content as a pipeline problem, not just as a
collection of JSON files.

The correct V1 target is:

- one authoring flow
- one normalized source model
- one runtime build path
- one runtime narrative interpretation path

That is the smallest narrative architecture that is:

- DDD-enough
- AI-friendly
- extensible
- stable enough for future content growth
