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

A merge-planning or handoff slice that may touch implementation, fixture, CLI,
or migration files without becoming the canonical owner of a capability.

Task nodes are governance aids for parallel work. They make write contamination
and integration obligations visible to the MasterAgent, but they do not promote
their outputs to reviewed evidence, hard gates, or default recommendation
authority.

Rules:

- `write_scope` is required and must be non-empty.
- `owner_path` is not canonical evaluator ownership for a task; prefer
  `write_scope` for planning.
- task `trust_tier` must stay advisory (`report_only` or `source_mined`).
- tasks must not provide canonical summary, review, bundle, payload, or contract
  artifacts.
- tasks may provide narrow entrypoint, adapter, or migration-slice artifacts.
- task `review_gated_with` and `invalidates` edges must represent real
  integration obligations, not topic similarity.

## Edge Types

### `depends_on`

Hard dependency. The source node relies on the target node.

Use this edge only when the target is a real prerequisite in the current
implementation or canonical merge flow.

Do not use `depends_on` for thematic ancestry, future intended integration, or
because one doc conceptually inspired another.

`depends_on` is also the correct relation for contract-bound governance edges:
when a capability is constrained by a canonical contract artifact or frozen
decision, but does not read that artifact as a live runtime/report input.

### `optional_depends_on`

Soft dependency. Missing it should degrade wording or confidence, not break the
entire node.

Use this edge only when the advisory read surface is already implemented in the
current code path.

Do not register speculative or "may later" consumers here just to preserve a
planning idea. Future advisory consumers should stay in docs, daily logs, or
task-node notes until the implementation actually reads the artifact.

### `provides`

The source capability or decision produces the target artifact.

### `consumes`

The source capability reads the target artifact.

Use this edge only when the current code path reads the artifact as a live input
surface.

Do not use `consumes` for validators that merely emit or normalize the contract,
for presence-only source-surface bookkeeping, or for future planned readers that
have not yet been wired.

Do not use `consumes` for contract-preservation-only edges such as authority
boundaries or direction documents unless the current implementation truly reads
that contract artifact as input data.

### `conflicts_with`

Semantic, contract, or write-scope conflict. Use `severity=hard` for
non-parallel-safe conflicts and `severity=soft` for merge-review conflicts.

### `review_gated_with`

The nodes may evolve independently but must be reviewed together before merge.

Use this edge only when the current codebase or canonical merge flow creates a
real master-agent integration obligation:

- shared live consumer/provider behavior,
- task-to-consumer handoff semantics,
- or a currently implemented artifact interpretation boundary.

Do not use `review_gated_with` for thematic similarity, shared long-term topic
area, or future planned integration that has not been wired yet.

### `invalidates`

A change to the source node should trigger re-review or re-validation of the
target node.

Use this edge only when the target has a current revalidation obligation caused
by a live contract, consumed artifact, or implemented interpretation path.

Do not use `invalidates` for broad "might affect wording someday" adjacency.

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
- `cardanalysis_feature_projection_v1`
- `stress_resolve_model_v1`
- `campaign_experience_curve_v1`
- `campaign_advisory_bundle_v1`
- `cardanalysis_case_progress_report_v1`
- `sts1_exam_target_v1`
- `card_package_variant_set_v1`
- `card_package_draft_handoff_v1`
- `complete_card_draft_v1`
- `card_draft_failure_taxonomy_v1`
- `llm_complete_card_draft_attempt_v1`
- `exam_iteration_run_v1`
- `exam_iteration_prompt_patch_proposal_v1`
- `card_package_exam_v1`
- `sts1_four_character_exam_v1`

Artifacts:

- `cardanalysis_north_star_contract`
- `normalized_design_case`
- `feature_projection_payload`
- `case_input_validator_entrypoint`
- `existing_asset_case_adapter_entrypoint`
- `stress_resolve_summary`
- `campaign_experience_curve_summary`
- `campaign_advisory_bundle`
- `cardanalysis_case_progress_snapshot`
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
- `sts1_exam_target`
- `card_package_variant_set`
- `card_package_draft_handoff`
- `complete_card_draft_package`
- `card_draft_failure_taxonomy`
- `llm_complete_card_draft_attempt_snapshot`
- `exam_iteration_run_snapshot`
- `exam_iteration_prompt_patch_proposal`
- `card_package_exam_snapshot`
- `sts1_four_character_exam_snapshot`

Decision:

- `decision_report_only_surfaces_not_authoritative`
- `decision_cardanalysis_case_backed_multi_head_direction`

Tasks:

- `cardanalysis_case_library_infra_v1`
- `existing_asset_case_adapter_v1`

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
8. hard conflict inside an analyzed batch,
9. non-empty `write_scope` for task nodes,
10. task nodes do not claim reviewed or decision-frozen authority,
11. task nodes do not provide canonical capability artifacts.

## Outputs

### Validation Report

A text and JSON report describing:

- node counts by kind,
- edge counts by relation,
- fail and warning counts,
- concrete issues.

### Impact Report

Given one node, show:

- root kind,
- direct provided artifacts,
- direct consumer nodes,
- direct dependent nodes,
- downstream impacted nodes,
- review-gated neighbors,
- conflict neighbors.

Artifact nodes are first-class impact roots. If the queried root is an artifact,
the impact report should start from the live consumers of that artifact rather
than returning an empty downstream set.

For contract artifacts, direct dependents are often the more important signal:
they show which capabilities are constrained by the contract even when there are
no live data consumers.

For task roots, impact reports also include a `task_governance` section with:

- `planning_role=merge_planning_slice`,
- advisory handoff authority boundary,
- explicit non-promotion to canonical owner,
- write scope,
- allowed task-provided artifacts,
- review handoff neighbors.

### Parallel Batch Report

Given a set of nodes, show:

- whether they are safe to run in parallel,
- hard conflicts,
- soft conflicts,
- write-scope overlap,
- nodes that should be master-agent integrated.

When selected nodes include tasks, batch reports also show:

- selected task nodes,
- task write scopes for merge contamination review,
- task handoff edges, including whether each handoff neighbor is in the
  requested batch.

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

Use task nodes for bounded case-backed work such as case-library
normalization, adapter migration, or other narrow handoff slices where the
MasterAgent needs write-scope and review-gate visibility.

The first registered task node is `cardanalysis_case_library_infra_v1`, which
tracks the minimal normalized case validator and CLI entrypoint. It is
review-gated with mechanism discovery and autonomous design because changes to
case validation can affect their future inputs.

The second registered task node is `existing_asset_case_adapter_v1`, which
tracks a narrow legacy-fixture export slice into normalized cases without
claiming canonical ownership of the legacy surfaces themselves. It is
review-gated with mechanism discovery and autonomous design because adapter
semantics can influence how current downstream case-backed heads read migrated
mechanism evidence.

Its dependency list should track only legacy surfaces it actually adapts. After
the campaign expansion slice, that includes mechanism-axis viability, campaign
power curve, stress/resolve, and campaign experience fixtures.

New report-only model heads such as stress/resolve or campaign experience
curves should normally be capability nodes, not task nodes, once they have a
stable owner module and summary artifact. Use a task node only for the bounded
integration or migration slice around such a model.

`campaign_advisory_bundle_v1` is also a capability node because it has a stable
owner module and CLI. It provides a standalone bundle artifact and consumes the
campaign power, stress/resolve, and campaign experience summaries. It is not a
canonical report-only registry surface unless the report-only registry is
explicitly promoted later.

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
