# Narrative Instance Task Table V1

## Goal

Break `Narrative Instance Model V1` into an incremental rollout plan that can
land on top of the current narrative pipeline without destabilizing the active
tutorial path.

## North-Star Rule

Prefer:

`template stays static -> instance is created at runtime -> instance state is isolated -> random variation is pinned once -> routing targets one instance`

Do not prefer:

`duplicate templates per actor` or `keep one global runtime bucket and patch around it`

## Phase 0. Freeze The Model Direction

Goal:

- make the template-vs-instance distinction explicit before implementation

Inputs:

- `docs/development/NARRATIVE_PIPELINE_V1.md`
- `docs/development/NARRATIVE_INSTANCE_MODEL_V1.md`

Outputs:

- accepted architecture document
- explicit rule that runtime artifacts stay template-only

Validation:

- document review only

Boundary:

- do not change runtime code yet

## Phase 1. Define Narrative Persistent State Schema

Goal:

- standardize the save/runtime container for narrative globals and instances

Suggested persistent shape:

```text
persistent["narrative"] = {
  "globals": ...,
  "instances": ...,
}
```

Outputs:

- state-shape document
- helper access contract for:
  - globals
  - instances
  - instance lookup
  - instance creation

Validation:

- unit tests for shape normalization

Boundary:

- do not move event/dialogue routing yet

## Phase 2. Add A Typed Narrative State Store

Goal:

- stop letting runtime code hand-edit raw nested persistent dicts

Suggested module:

- `contexts/narrative/domain/narrative_state_store.py`

Outputs:

- helper methods for:
  - `get_globals()`
  - `get_instance(instance_id)`
  - `create_instance(...)`
  - `set_current_node(...)`
  - local flag/var/stat access
  - archive/complete status updates

Validation:

- unit tests for create/read/update behavior

Boundary:

- this is a typed helper/store, not a new repository layer

## Phase 3. Make NarrativeApplicationService Instance-Aware

Goal:

- move instance creation/resume policy into the narrative application layer

Suggested API:

- `create_instance(...)`
- `start_or_resume_instance(...)`

Compatibility seam:

- keep `start_session(quest_id=...)` alive temporarily by mapping it to a
  singleton instance path

Validation:

- service tests for:
  - first create
  - resume existing instance
  - singleton compatibility path

Boundary:

- do not remove tutorial compatibility yet

## Phase 4. Move QuestRuntime / QuestEngine To Instance-Local State

Goal:

- stop reading/writing singleton runtime keys such as:
  - `quest_current_node`
  - `quest_flags`
  - `quest_vars`
  - `quest_player_stats`

Outputs:

- runtime reads current node from one instance
- runtime writes local flags/vars/stats to one instance
- local runtime state no longer contaminates other instances

Validation:

- targeted runtime tests
- multi-instance isolation tests

Boundary:

- keep condition/consequence language the same for the first cut

## Phase 5. Add Transition Routing By `instance_id`

Goal:

- make campaign/event/dialogue entry target one concrete narrative instance

Outputs:

- contract keys for:
  - `narrative_instance_id`
  - optional `narrative_quest_id` as compatibility fallback
- event/dialogue state startup resumes one instance
- campaign routing can pass an instance id explicitly

Validation:

- transition-contract tests
- headless event/dialogue startup tests

Boundary:

- do not rewrite event/dialogue presentation logic in this phase

## Phase 6. Pin Random Variation At Instance Creation

Goal:

- support small deterministic differences between same-template instances

Outputs:

- `seed`
- `resolved_variant`

Validation:

- same instance reloads to the same variant
- two instances may differ when allowed by the template rules

Boundary:

- do not make runtime re-roll variant state during normal node execution

## Phase 7. Add Instance Acceptance Coverage

Goal:

- upgrade confidence from "instance structure exists" to "multi-instance
  behavior works"

Suggested first canonical scenarios:

- same template, two assistants, isolated node progress
- same template, two assistants, isolated local vars
- one instance save/load resume
- one instance pinned variation remains stable after reload

Validation:

- targeted `tests/shared/` acceptance flows

Boundary:

- do not require headed UI verification for the first cut

## Phase 8. Pilot One Real Same-Template Multi-Instance Line

Goal:

- prove the architecture on actual game content

Suggested pilot:

- template: `assistant_relation_v1`
- instances:
  - `assistant_a`
  - `assistant_b`

Outputs:

- one real same-template content path
- real route wiring into campaign block/open flow

Validation:

- content acceptance tests
- save/load verification

Boundary:

- do not migrate every narrative family in the same batch

## Phase 9. Add Explicit Global Narrative Scope When Needed

Goal:

- support shared world facts without blurring local and global state

Suggested rule:

- add explicit global-scope condition/consequence families only when product
  pressure requires them

Examples:

- `GLOBAL_FLAG_EQUALS`
- `GLOBAL_QUEST_VAR_COMPARE`

Validation:

- contract tests for local/global separation

Boundary:

- do not make one condition type silently guess scope

## Phase 10. Retire Singleton Narrative Runtime Keys

Goal:

- remove the old singleton runtime state path after instance mode is proven

Retirement targets:

- `quest_current_node`
- `quest_flags`
- `quest_vars`
- `quest_player_stats`

Validation:

- repo smoke baseline
- narrative acceptance tests
- save/load compatibility checks

Boundary:

- retire in batches if needed
- keep a deliberate migration shim only while old saves still need it

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
9. Phase 8
10. Phase 9
11. Phase 10

This should stay mostly serial.

Good parallel side work:

- tests
- docs
- pilot-content preparation

Avoid parallelizing:

- state schema redesign
- instance contract changes
- transition payload redesign

## Completion Criteria

Narrative instance architecture is effectively complete when:

1. `questline` is treated as a template, not a singleton runtime object
2. same-template multi-instance lines can coexist in one save
3. per-instance progress and local state are isolated
4. random variation is pinned once and survives load
5. campaign/event/dialogue routing can target one explicit `instance_id`
6. old singleton narrative runtime keys are retired or explicitly shimed during
   migration only

## Current Recommendation

The next real implementation cut should be:

- `Phase 1 + Phase 2 + Phase 3`

That is the smallest high-ROI start because it:

- defines the correct state model early
- avoids spreading raw nested-dict mutations
- keeps the tutorial path alive while instance support is added
