# Narrative Pipeline Task Table V1

## Goal

Break `Narrative Pipeline V1` into a concrete rollout order that can be
executed incrementally without pausing all content work.

This table is intentionally phased.

The correct execution model is:

- establish one target path
- migrate the active tutorial path first
- validate it through build + runtime + scenario tests
- only then retire the legacy route

## North-Star Rule

Prefer:

`freeze old growth -> define source schema -> build runtime parity -> lock tests -> retire legacy`

Do not prefer:

`delete everything old first and hope the new path catches up`

## Phase 0. Freeze The Narrative Direction

Goal:

- make the target narrative path explicit before any broad deletion

Inputs:

- `docs/development/narrative/NARRATIVE_PIPELINE_V1.md`
- current narrative runtime files under `data/questlines/`
- legacy campaign event files under `contexts/campaign/infrastructure/events/`

Outputs:

- accepted pipeline document
- explicit legacy policy for the old campaign event route
- task-pool visibility for the rollout

Validation:

- document review only

## Phase 1. Inventory Active And Legacy Narrative Content

Goal:

- identify what must be migrated, what already exists in the active questline
  path, and what is still legacy-only

Inputs:

- `contexts/campaign/infrastructure/events/*.json`
- `data/events_src/packs/*`
- `data/questlines/*.json`

Outputs:

- one migration inventory table
- classification of each legacy narrative unit:
  - already covered
  - partially covered
  - not yet covered

Validation:

- a focused inventory doc or appendix

Boundary:

- do not migrate behavior yet

## Phase 2. Define The Normalized Narrative Source Schema

Goal:

- land the stable normalized source model under `data/narrative_src/`

Inputs:

- `scripts/events_draft_io.py`
- `scripts/events_effect_registry.py`
- active tutorial questline structure

Outputs:

- `manifest.json`
- `nodes.csv`
- `choices.csv`
- `consequences.csv`
- `conditions.csv`
- `locales_zh_CN.csv`
- `_draft_id_map.csv`

Validation:

- schema-focused pytest coverage
- deterministic read/write contract tests

Boundary:

- do not replace runtime loading yet

## Phase 3. Add Draft -> Source Tooling

Goal:

- support planner-friendly drafts without making drafts the runtime source of
  truth

Inputs:

- existing event draft scripts
- normalized schema from Phase 2

Outputs:

- `scripts/validate_narrative_draft.py`
- `scripts/import_narrative_draft_to_src.py`
- tests for draft validation/import parity

Validation:

- draft validation tests
- source import regression tests

Boundary:

- keep the DSL small
- do not turn drafts into a scripting language

## Phase 4. Build Source -> Runtime Compilation

Goal:

- compile normalized narrative source into active `data/questlines/*.json`
  runtime artifacts

Inputs:

- `data/narrative_src/packs/<pack>/`
- active questline runtime schema

Outputs:

- `scripts/build_narrative_runtime.py`
- generated or regenerated `questline_*.json`
- deterministic parity tests between source and runtime artifact

Validation:

- source/build contract tests
- runtime questline contract tests

Boundary:

- runtime should still only load built artifacts
- do not add hidden build steps inside runtime modules

## Phase 5. Migrate The Active Tutorial Narrative Pack

Goal:

- prove the pipeline on the currently active tutorial path before expanding it

Inputs:

- `questline_tutorial.json`
- `rewards_tutorial.json`
- current narrative runtime tests

Outputs:

- tutorial pack represented in normalized narrative source
- tutorial runtime artifact generated from source
- parity confirmation that the runtime path still behaves correctly

Validation:

- `QuestLoader` / `QuestRuntime` tests
- headless tutorial flow regression

Boundary:

- do not migrate every legacy event pack in the same cut

## Phase 6. Add Scenario Acceptance Coverage

Goal:

- move narrative confidence from "it loads" to "the intended player path works"

Suggested first canonical scenarios:

- tutorial onboarding -> combat trigger
- tutorial archive intro -> reward follow-up
- event feedback acknowledgement -> return to campaign
- reward trigger -> pending transition queue -> campaign resume

Outputs:

- headless scenario regression tests
- one small headed smoke test if needed for confidence only

Validation:

- targeted `tests/shared/` scenario flows

Boundary:

- do not try to automate every visual detail

## Phase 7. Retire Legacy Narrative Runtime Paths

Goal:

- remove the old campaign event runtime route after build parity and scenario
  coverage are proven

Primary retirement targets:

- `contexts/campaign/application/campaign_service.py`
- `contexts/campaign/domain/event.py`
- `contexts/campaign/domain/event_repository.py`
- `contexts/campaign/infrastructure/json_event_repository.py`
- `contexts/campaign/infrastructure/events/*.json`
- old headless/test entrypoints that exist only for the legacy path

Validation:

- repo smoke baseline
- quest runtime tests
- narrative scenario regression
- architecture / contract guardrails

Boundary:

- retire in batches if needed
- do not delete reference content before migration inventory says it is covered

## Suggested Execution Order

The recommended default order is:

1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 4
6. Phase 5
7. Phase 6
8. Phase 7

This should be run serially.

Do not split the mainline into multiple competing narrative architecture
branches.

## Recommended Ownership Split

Main-agent-owned work:

- source-of-truth rules
- normalized schema
- runtime build contract
- legacy retirement decisions

Good sidecar / bounded parallel work:

- draft validator implementation
- source schema fixture generation
- scenario regression case addition
- migration inventory table population

Avoid parallelizing:

- source schema redesign
- runtime artifact shape changes
- legacy retirement sequencing

## Completion Criteria

Narrative Pipeline V1 is effectively complete when:

1. active tutorial narrative content is authored from normalized source
2. runtime questline artifacts are generated by a checked-in build step
3. narrative runtime no longer depends on the legacy campaign event repository
4. scenario acceptance tests cover at least the main tutorial event/combat/reward
   path
5. old campaign event runtime files are retired or explicitly archived as
   historical reference only

## Current Recommendation

Treat `Phase 0` as ready now.

The next real implementation cut should be:

- `Phase 1 + Phase 2`

That is the smallest high-ROI start because it:

- avoids premature deletion
- avoids pretending the schema is obvious
- gives the project a stable migration map before build work begins
