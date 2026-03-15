# Runtime Nodes vs Domain Boundaries V1

## Goal

Clarify why the project is evolving toward Godot-like runtime nodes inside
pygame while still keeping DDD-style domain/application boundaries.

This document is not a full architecture spec. It exists to answer one narrow
question:

- what should be modeled as runtime nodes
- what should stay in orchestration/domain layers
- why both are needed at the same time

## Core Thesis

The project carries two different kinds of complexity:

1. runtime/world complexity
2. business/rule complexity

Runtime nodes are good at the first kind.
DDD-style domain/application structure is better at the second kind.

The project should not force one model to absorb both.

## What Runtime Nodes Are For

Runtime nodes are best used to express:

- parent/child attachment
- draw order and scene layering
- visibility and lifecycle
- local transforms such as position, shake, scale, and alpha
- hit-testing and local interaction hosting
- reusable runtime widgets and scene elements

Examples in this project:

- campaign-side phone widget
- fish or phone anchors attached to a scene layer
- layered background elements that may shake, slide, or fade
- prompts or floating runtime interaction shells

In short:

- nodes should model runtime structure
- nodes should host local interaction and presentation state

## What Should Not Be Solved By Nodes Alone

Runtime nodes should not become the default home for:

- thesis submission rules
- campaign route-resolution policy
- reward-chain business decisions
- encounter transition contracts
- repository boundaries
- save/load schema evolution
- cross-context orchestration

These are not primarily scene-graph problems.
They are business, persistence, or orchestration problems.

## Why DDD / Orchestration Still Matters

DDD-style boundaries remain useful because the project is not only a scene.
It is also a rule-heavy simulation with:

- campaign progression
- thesis runtime state
- combat rules and task hosts
- reward and transition flows
- content contracts and save compatibility

These areas need:

- explicit invariants
- readable write paths
- narrower dependencies
- testable rule ownership
- stable cross-state contracts

That work belongs mainly in:

- domain objects
- application/orchestration services
- infrastructure adapters

not in the runtime node tree itself.

## Recommended Split

### Runtime Node World

Use nodes for:

- scene layers
- runtime widgets
- attachment points
- local transforms
- visual lifecycle
- local input handling

Examples:

- `contexts/campaign/ui_runtime/ui_node.py`
- future scene-layer nodes for background/overlay attachments

### Domain / Application World

Use domain + orchestration for:

- rule truth
- use-case sequencing
- contract enforcement
- cross-state transitions
- save/load consistency
- content validation

Examples:

- `contexts/campaign/domain/`
- `contexts/campaign/services/`
- `contexts/shared/domain/contracts.py`

## Why This Is The Current Evolution Path

The project is intentionally moving toward:

- Godot-like runtime organization inside pygame

but not toward:

- replacing domain/application boundaries with node scripts

That is because:

1. node-style runtime structure improves scene/UI clarity
2. orchestration/domain boundaries protect long-term system changeability
3. the project's complexity is split across both runtime and business layers
4. AI collaboration works better when each kind of complexity has a clear home

## Practical Review Rule

When deciding where a new piece of logic should live, ask:

1. Is this mainly about runtime attachment, transform, visibility, or local interaction?
   - prefer a runtime node
2. Is this mainly about rules, sequencing, contracts, or persistence?
   - prefer domain/application/infrastructure

If the answer is "both", split the concerns instead of forcing one layer to own
everything.

## Current Caution

Node adoption is good for the project only if it does not become:

- a new universal dumping ground
- a replacement for orchestration
- a hidden dependency graph where any node can mutate anything

Likewise, DDD-style layering is good only if it does not fight the genuine
runtime needs of a game scene.

The target is a mixed but disciplined architecture:

- runtime nodes for runtime structure
- orchestration for process complexity
- domain for rule truth
- infrastructure for external implementation details

## Current Conclusion

The project should continue pursuing:

- runtime-node growth for campaign-side scene and widget organization
- explicit domain/application boundaries for business/rule-heavy systems

The architectural goal is not "nodes versus DDD".
The goal is:

- use nodes where the world needs structure
- use DDD/orchestration where the business needs truth and control
