# Cardanalysis Capability Dependency And Conflict Graph V1

## Purpose

Define a lightweight graph layer for `cardanalysis` capabilities, artifacts,
decisions, and future task planning.

This graph does not replace existing evaluators, fixtures, CLIs, or evidence
bundles. It sits above them and answers four practical questions:

1. what depends on what,
2. what conflicts with what,
3. what becomes stale after a change,
4. which work items are safe to run in parallel.

## Scope Boundary

In scope:

- `cardanalysis` capability nodes, artifact nodes, and a small number of
  decision nodes
- dependency, conflict, review-gated, and invalidation relations
- impact analysis for merge and refactor work
- parallel-work safety checks based on hard conflicts and write-scope overlap
- compatibility with the existing report-only surface registry

Out of scope:

- gameplay runtime scheduling
- graph databases or UI explorers
- full automatic task assignment
- replacing the reviewed validation matrix
- replacing canonical evaluator ownership

## Relationship To Existing Assets

This graph is an overlay on top of existing governance files:

- `CARDANALYSIS_REPORT_ONLY_SURFACE_REGISTRY_V1.md`
- `CARDANALYSIS_MECHANISM_VALIDATION_MATRIX_V1.md`
- `CARDANALYSIS_NORTH_STAR_V1.md`
- `CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`
- `tools/combat_analysis/report_only_surface_registry.py`

The report-only registry remains the canonical owner list for report-only
surfaces. The capability graph adds:

- artifact-level visibility,
- consumer/provider edges,
- conflict edges,
- review-gated edges,
- impact traversal.

The north-star and case-input documents define the direction and normalized
input contract. The graph makes them visible to future planning so case work can
be checked for downstream impact before agents start parallel implementation.

## Design Principle

The system is not a single DAG.

It is a multi-relation graph:

- `depends_on` answers "what must already exist",
- `provides` answers "what artifact does this node produce",
- `consumes` answers "what artifact does this node read",
- `conflicts_with` answers "what cannot safely evolve in parallel",
- `review_gated_with` answers "what needs master-agent integration review",
- `invalidates` answers "what should be rechecked after a change".

Dependency solves order. Conflict solves contamination.

## Node Types

### `capability`

A stable provider or consumer of analysis behavior.

Examples:

- `mechanism_fun_health_v1`
- `campaign_power_curve_report_v1`
- `cardanalysis_evidence_bundle_v1`

### `artifact`

A produced or consumed contract, summary, or review payload.

Examples:

- `deck_compression_summary`
- `mechanism_fun_health_summary`
- `cardanalysis_evidence_bundle`

### `decision`

A frozen or semi-frozen assumption that other nodes rely on.

Examples:

- `decision_report_only_surfaces_not_authoritative`

### `task`

Reserved for later planning slices. V1 documents the schema but does not yet
populate task nodes in the canonical registry.

## Edge Types

### `depends_on`

Hard dependency. The source node relies on the target node.

### `optional_depends_on`

Soft dependency. Missing it should degrade wording or confidence, not break the
entire node.

### `provides`

The source capability or decision produces the target artifact.

### `consumes`

The source capability reads the target artifact.

### `conflicts_with`

Semantic, contract, or write-scope conflict. Use `severity=hard` for
non-parallel-safe conflicts and `severity=soft` for merge-review conflicts.

### `review_gated_with`

The nodes may evolve independently but must be reviewed together before merge.

### `invalidates`

A change to the source node should trigger re-review or re-validation of the
target node.

### `supersedes`

Reserved for future replacement flows when one capability replaces another.

## Conflict Taxonomy

### Semantic Conflict

Two nodes claim the same meaning or canonical owner.

### Write Scope Conflict

Two tasks or capability edits touch the same write boundary.

### Contract Conflict

Two nodes change the same summary or payload shape from different sides.

### Decision Conflict

Two efforts assume incompatible product or architecture direction.

## Initial Node Schema

```yaml
id:
kind: capability | artifact | decision | task
display_name:
owner_path:
status: active | draft | deprecated | superseded
trust_tier: reviewed | report_only | source_mined | decision_frozen
object_types: []
write_scope: []
parallel_safety: high | medium | low
notes: []
```

## Initial Edge Schema

```yaml
source_id:
target_id:
relation:
severity: hard | soft
reason:
```

## Initial Registry Coverage

V1 should cover these canonical nodes first:

Capabilities:

- `mechanism_axis_viability_v1`
- `deck_compression_report_v1`
- `mechanism_fun_health_v1`
- `card_package_health_v1`
- `mechanism_axis_discovery_v1`
- `campaign_power_curve_report_v1`
- `position_redirect_code_preflight_v1`
- `design_iteration_brief_v1`
- `cardanalysis_evidence_bundle_v1`
- `evaluation_autonomous_design_model_v1`
- `cardanalysis_case_input_contract_v1`
- `stress_resolve_model_v1`
- `campaign_experience_curve_v1`

Artifacts:

- `cardanalysis_north_star_contract`
- `normalized_design_case`
- `feature_projection_payload`
- `case_input_validator_entrypoint`
- `stress_resolve_summary`
- `campaign_experience_curve_summary`
- `mechanism_axis_summary`
- `deck_compression_summary`
- `mechanism_fun_health_summary`
- `card_package_health_summary`
- `mechanism_axis_discovery_summary`
- `campaign_power_curve_summary`
- `position_redirect_code_preflight_summary`
- `design_iteration_summary`
- `cardanalysis_evidence_bundle`
- `evaluation_autonomous_design_review`
- `authority_boundary_contract`

Decision:

- `decision_report_only_surfaces_not_authoritative`
- `decision_cardanalysis_case_backed_multi_head_direction`

Tasks:

- `cardanalysis_case_library_infra_v1`

## Planning Semantics

### Ready Node

A node is ready for integration when:

1. its hard dependencies are satisfied,
2. it has no unresolved hard conflict with the active batch,
3. any required decision nodes are frozen or explicitly accepted.

### Parallel-Safe Batch

A batch is safe to run in parallel when:

1. no selected node pair has a hard `conflicts_with` edge,
2. write scopes do not overlap,
3. the batch does not edit the same canonical provider from multiple tasks.

Soft conflicts do not block parallel exploration, but they must be reported.

### Impact Traversal

If a capability changes, V1 impact traversal should walk:

1. capability -> provided artifacts,
2. artifact -> consumer capabilities,
3. capability -> dependent capabilities,
4. explicit review-gated or invalidated neighbors.

## Minimum Validator

The validator should check:

1. unique node ids,
2. valid edge endpoints,
3. canonical report-only surface coverage,
4. provider uniqueness for each artifact,
5. missing provider for consumed artifact,
6. missing owner path for capability node,
7. write-scope overlap inside an analyzed batch,
8. hard conflict inside an analyzed batch.

## Outputs

### Validation Report

A text and JSON report describing:

- node counts by kind,
- edge counts by relation,
- fail and warning counts,
- concrete issues.

### Impact Report

Given one node, show:

- direct provided artifacts,
- direct consumer nodes,
- downstream impacted nodes,
- review-gated neighbors,
- conflict neighbors.

### Parallel Batch Report

Given a set of nodes, show:

- whether they are safe to run in parallel,
- hard conflicts,
- soft conflicts,
- write-scope overlap,
- nodes that should be master-agent integrated.

## Suggested Rollout

### Phase 0

Document the graph vocabulary and registry contract.

### Phase 1

Add:

- `tools/combat_analysis/capability_graph_registry.py`
- `scripts/validate_capability_graph.py`
- focused registry and CLI tests
- `CARDANALYSIS_NORTH_STAR_V1.md`
- `CARDANALYSIS_CASE_INPUT_CONTRACT_V1.md`

### Phase 2

Use the graph for impact and batch checks during multi-agent planning and merge
review.

### Phase 3

Start adding task nodes for future case-backed work such as campaign pressure,
stress/resolve, BBS/social read models, mechanism expansion, and case-library
normalization.

The first registered task node is `cardanalysis_case_library_infra_v1`, which
tracks the minimal normalized case validator and CLI entrypoint. It is
review-gated with mechanism discovery and autonomous design because changes to
case validation can affect their future inputs.

## Non-Goals For V1

- no graph UI
- no automatic optimal task planner
- no runtime hot reload
- no replacement of reviewed evidence or human review

## Decision Summary

1. `cardanalysis` should use a multi-relation graph, not a single dependency DAG.
2. Capability, artifact, and decision nodes should all be first-class.
3. Conflict relation is required to control parallel-work contamination.
4. V1 should remain file-based, inspectable, and low-maintenance.
