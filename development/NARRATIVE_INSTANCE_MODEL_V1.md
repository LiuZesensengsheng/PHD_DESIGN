# Narrative Instance Model V1

## Goal

Define the next-step runtime model for narrative after `Narrative Pipeline V1`
so the project can support:

- one narrative template used by multiple concurrent in-save instances
- per-instance local state without cross-line contamination
- deterministic small random variation per instance
- stable save/load and AI-friendly ownership boundaries

- Level: `L3 Architecture`
- Date: `2026-04-08`

## Problem

The current narrative pipeline has successfully separated:

- draft
- normalized source
- build
- runtime artifact

But the runtime state model still behaves as if:

- one `questline` equals one running state bucket

That is good enough for the current tutorial path, but it is not good enough for
the next intended content shape:

- one narrative template
- multiple in-save instances
- each instance bound to a different actor or world object
- each instance allowed to carry small deterministic variation

Example future use case:

- `assistant_relation_v1` exists once as a template
- it is instantiated for `assistant_a`
- it is also instantiated for `assistant_b`
- the two instances must not share:
  - current node
  - local flags
  - local vars
  - local stats
  - resolved random flavor differences

The current singleton-style narrative state does not model that.

## Constraints

- Keep `data/questlines/*.json` as runtime-loaded artifacts.
- Do not turn build output into save-state output.
- Do not reopen the narrative pipeline into a scripting VM.
- Avoid a broad UI rewrite as part of this architecture step.
- Preserve the current tutorial path during migration.
- Keep contracts explicit and AI-readable.
- Prefer typed stores/helpers over a new universal repository layer.
- Keep random variation deterministic across save/load.

## Complexity

### Essential Complexity

- A narrative template and a narrative instance are not the same thing.
- Some narrative state is local to one instance.
- Some narrative state will eventually be global across instances.
- Instance creation may resolve small random differences.
- Campaign/event/dialogue routing must address one specific instance.
- Save/load must preserve instance identity and resolved variation.

### Accidental Complexity

- treating `questline_id` as if it were already an instance id
- storing all narrative runtime state in one global bucket
- hard-coding `questline_tutorial` at state-entry seams
- allowing runtime selection and instance creation to blur together
- recomputing random variation instead of pinning it once

## Options

### Option A: Namespace Runtime State By `questline_id` Only

What it means:

- keep the current runtime/template model
- replace one global bucket with one bucket per `questline_id`

Example:

```python
persistent["quest_runtime"]["questline_tutorial"] = {...}
```

Pros:

- cheapest migration
- enough if every active narrative line is a unique template
- low change surface in runtime code

Cons:

- fails when one template must exist twice in the same save
- does not model actor-bound instances
- does not solve same-template multi-instance content
- pushes future instance work into another migration later

### Option B: Separate Template From Instance Explicitly

What it means:

- keep `questline_*.json` as template artifacts
- add runtime instance state under explicit `instance_id`
- route runtime via `instance_id`, not only `questline_id`
- keep template ids and instance ids as separate concepts

Pros:

- directly matches the intended content model
- solves same-template multi-instance support cleanly
- supports actor binding, deterministic variation, and save/load
- gives AI a stable and explicit ownership model

Cons:

- larger runtime contract change
- needs transition-payload plumbing
- requires a compatibility layer for the current tutorial path

### Option C: Materialize One Template Clone Per Actor/Variant

What it means:

- duplicate questline artifacts per actor or per variant
- make each clone look like a unique template

Pros:

- avoids adding runtime instance semantics
- keeps runtime logic simpler in the short term

Cons:

- explodes content duplication
- breaks source-of-truth clarity
- makes AI content iteration worse, not better
- moves instance complexity into build/content management instead of solving it

## Risks

### If We Stay At `questline_id`-Only Runtime State

- same-template multi-instance lines will still cross-contaminate
- save/load will not distinguish actor-specific runs cleanly
- later migration cost will increase once more content depends on the wrong model

### If We Overbuild The Instance Layer Too Early

- we may add a large generic content-runtime framework before it is needed
- we may mix global state, local state, and variant rules too aggressively
- we may reopen UI/runtime seams that do not need to move yet

### Migration Risks

- save compatibility for existing tutorial progress
- accidentally moving instance-specific state into built artifacts
- random variation drifting after load if it is not pinned at creation time
- transition seams carrying only `questline_id` and not `instance_id`

## Recommendation

Choose **Option B**.

The correct next model is:

- runtime artifacts are templates
- running narrative is an instance
- instance state is isolated
- small random variation is pinned when the instance is created

### Recommended Runtime Shape

```python
persistent["narrative"] = {
    "globals": {
        "flags": {},
        "vars": {},
    },
    "instances": {
        "assistant_relation_v1__assistant_a__01": {
            "instance_id": "assistant_relation_v1__assistant_a__01",
            "questline_id": "assistant_relation_v1",
            "status": "active",
            "owner_ref": {
                "type": "assistant",
                "id": "assistant_a",
            },
            "bindings": {
                "assistant_id": "assistant_a",
            },
            "seed": 12345,
            "resolved_variant": {
                "tone": "warm",
                "intro_set": "b",
            },
            "current_node_id": "node_intro",
            "flags": {},
            "vars": {},
            "stats": {},
            "started_at_turn": 3,
            "updated_at_turn": 5,
        },
    },
}
```

### Core Model Rules

#### 1. Template Rule

`questline_*.json` owns:

- node graph
- conditions
- consequences
- localized text
- template-level ids

It must not own:

- current node
- actor binding
- resolved random variation
- save-state mutation history

#### 2. Instance Rule

`instance_id` owns:

- one running copy of one template
- local progress
- local flags / vars / stats
- owner binding
- seed
- resolved variation

#### 3. Random Rule

Allowed instance variation must be resolved once:

- at instance creation time

It must then be stored under:

- `seed`
- and/or `resolved_variant`

Runtime must not re-roll the same instance on each entry/load.

#### 4. Scope Rule

Default V1.5 recommendation:

- local narrative conditions read instance-local state first
- global narrative facts should be introduced explicitly later
- do not make runtime guess whether a condition is local or global

## Counter-Review

Why not keep it simple and only namespace by `questline_id`?

- because the user-facing future content shape is not "many different templates"
- it is "one template instantiated many times"
- that requirement is the exact point where `questline_id`-only runtime state
  stops being correct

Why not prebuild variant clones?

- because it makes content management worse than the current system
- it duplicates authoring and migration work
- it is especially bad for AI-friendly content iteration

What assumption does the recommendation depend on?

- that same-template multi-instance narrative is a real intended product
  direction, not just a hypothetical possibility

If that assumption changes, Option A may be enough.
Given the stated direction, it is not enough.

## Decision Summary

1. `questline` should be treated as a template, not as a running save-state
   object.
2. Narrative runtime should execute a specific `instance_id`.
3. Same-template multi-instance support requires explicit instance state.
4. Small random variation must be pinned at instance creation time.
5. The next engineering move is not a UI rewrite; it is an instance-aware
   runtime state model with clear transition contracts.

## Technical Design

### Terms

- `questline_id`
  - the template id loaded from `data/questlines/questline_*.json`
- `instance_id`
  - the concrete running copy inside one save
- `owner_ref`
  - the world object or actor this instance is bound to
- `bindings`
  - explicit runtime values made available to the instance
- `resolved_variant`
  - small pinned differences resolved during instance creation

### Recommended File Ownership

#### Runtime Contracts

- `contexts/shared/domain/contracts.py`

Own:

- `narrative_quest_id`
- `narrative_instance_id`
- helper getters/setters

#### Typed Persistent Access

Recommended new module:

- `contexts/narrative/domain/narrative_state_store.py`

Own:

- access to `persistent["narrative"]`
- `globals`
- `instances`
- create/get/update/archive instance helpers

This should be a typed helper/store, not a broad repository abstraction.

#### Narrative Instance Model

Recommended new module:

- `contexts/narrative/domain/instance.py`

Own:

- `NarrativeInstanceState`
- maybe a small normalization helper for instance payloads

#### Application Service

- `contexts/narrative/application/service.py`

Own:

- `create_instance(...)`
- `start_or_resume_instance(...)`
- compatibility path for the current tutorial singleton

It should not own:

- direct UI rendering
- build logic

#### Runtime Execution

- `contexts/shared/quest_engine.py`
- `contexts/shared/quest_runtime.py`

Own:

- evaluate template against one instance state
- update one instance's local node/flags/vars/stats

They should not own:

- instance creation policy
- actor binding selection
- re-randomization of variation

### Recommended Service API

Suggested minimal evolution:

```python
create_instance(
    persistent,
    *,
    questline_id: str,
    owner_ref: dict[str, str] | None = None,
    bindings: dict[str, object] | None = None,
    seed: int | None = None,
    instance_id: str | None = None,
) -> str

start_or_resume_instance(
    persistent,
    *,
    instance_id: str,
) -> NarrativeSession
```

Compatibility seam during migration:

```python
start_session(
    persistent,
    *,
    quest_id: str,
) -> NarrativeSession
```

The compatibility path may internally:

- create or reuse a singleton instance for `quest_id`

but that should be treated as migration scaffolding, not the final model.

### Transition Flow

Recommended target flow:

1. campaign logic decides which narrative instance should open
2. transition payload carries:
   - `pending_block_id`
   - `narrative_instance_id`
   - optionally `narrative_quest_id` for create-flow fallback only
3. `EventState` / `DialogueState` resumes that instance
4. `QuestRuntime` advances `current_node_id` inside that instance
5. consequences mutate that instance's local state
6. campaign return continues through the existing pending-transition contract

### Random Variation Policy

V1 recommendation:

- store both:
  - `seed`
  - `resolved_variant`

Why both:

- `seed` helps reproducibility/debugging
- `resolved_variant` makes runtime behavior explicit and stable even if variant
  logic evolves later

### Scope Policy

Recommended rollout order:

#### Stage 1

- all current narrative conditions/consequences remain instance-local

#### Stage 2

- add explicit global-scope condition/consequence families only when needed

Examples:

- `GLOBAL_FLAG_EQUALS`
- `GLOBAL_QUEST_VAR_COMPARE`

Do not overload one condition type to silently read both scopes.

### Compatibility Strategy

To avoid breaking the tutorial path too early:

- keep `questline_tutorial` as the first singleton-compatible path
- map legacy singleton runtime state into one synthetic default instance during
  migration
- only remove old singleton keys after:
  - instance-aware tests are green
  - one real multi-instance pilot is landed

### Recommended First Pilot

Use one real same-template scenario, for example:

- template: `assistant_relation_v1`
- instances:
  - `assistant_a`
  - `assistant_b`

Acceptance criteria:

- each instance keeps independent progress
- each instance keeps independent local vars/flags/stats
- save/load resumes correctly
- pinned variation does not drift after reload

## Non-Goals

This document does not recommend:

- compiling instance state into build artifacts
- replacing the narrative pipeline with a general content VM
- solving all global narrative state modeling now
- doing a broad event/dialogue UI rewrite as part of the instance step
