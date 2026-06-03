# Cardanalysis Legacy Module Slimming Template V1

## Purpose

This template defines how to reduce old `cardanalysis` module complexity without
changing advisory behavior.

Use it when an old module has grown around local helper functions, repeated text
scans, repeated cost/value semantics, repeated artifact wiring, or report rendering
mixed into evaluator logic.

The goal is not to make every module tiny in one pass. The goal is to make every
cleanup slice answer the same questions:

1. what repeated logic is being removed,
2. which shared layer now owns it,
3. what output contract stayed unchanged,
4. what tests prove the slice was behavior-preserving.

## Non-Negotiable Boundaries

- Keep outputs `report_only` / `advisory_context_only`.
- Do not write runtime card data.
- Do not promote formal cards.
- Do not create hard gates.
- Do not change score weights, default synthesis, learned paths, rerankers, or
  reviewed-evidence claims.
- Do not call LLM/API.
- Do not edit dated daily logs on implementation/refactor branches.
- Do not migrate helper semantics just because the names match. Match behavior
  first.

## Target Shape

Prefer this shape for old `programmatic_complete_card_draft_*` modules:

```text
input package / snapshot
        -> shared facts or artifact readers
        -> small rule table / local evaluator head
        -> payload builder
        -> report renderer / CLI artifact writer
```

The long-term direction is not one giant exam engine. It is a set of thin,
focused exam heads that consume shared facts and shared artifact helpers.

## Module Worksheet

Fill this before editing a legacy module.

| Field | Answer |
| --- | --- |
| Module path | |
| Contract version | |
| CLI path | |
| Focused tests | |
| Snapshot/report artifacts | |
| Current owner surface | |
| Report-only boundary fields | |
| Local helper families | |
| Candidate shared owner | |
| Behavior-sensitive outputs | |
| Safe first slice | |

## Helper Classification

Classify each local helper before moving or deleting it.

| Helper Type | Examples | Preferred Owner | Migration Rule |
| --- | --- | --- | --- |
| Artifact helper | manifest refs, artifact completeness | `axis_first_artifact_output.py` or a shared artifact module | Move when output shape is identical. |
| Card fact extraction | cost buckets, card text, numeric routes, poison projection, condition markers | `cardanalysis_fact_model.py` | Move only after adding focused fact tests. |
| Rule table | thresholds, labels, status mapping, reference lessons | local module or future rule-spec module | Keep local until two or more modules use identical semantics. |
| Payload assembly | model overview, package result rows, source chain | local module | Do not centralize unless the payload contract repeats exactly. |
| Report renderer | Markdown table rendering, Chinese review packet text | local or report-lane helper | Split only after snapshot/payload is stable. |
| CLI wiring | path parsing, artifact writing | script-local or shared CLI helper | Move only when multiple CLIs share identical wiring. |

## Deletion Ladder

Use the lowest safe rung first.

1. **Alias shared helper**
   Import an existing shared helper and delete the local duplicate.

2. **Add shared fact**
   Add one field to the fact model, test it, then replace local recomputation.

3. **Move local rule table**
   Move only if the exact same thresholds or labels are duplicated in multiple
   modules.

4. **Split renderer**
   Move Markdown/report construction after payload tests prove evaluator behavior
   is stable.

5. **Archive wrapper**
   Archive or delete old wrappers only when the unified route, descriptor, CLI,
   and tests all agree.

Avoid jumping directly to rung 4 or 5 unless the module is already well-covered.

## Semantics Check

Before sharing a helper, verify:

- same handling of `bool` values,
- same handling of `X` cost,
- same fallback for unknown or unplayable cost,
- same text search scope: name, id, rules, upgraded rules, tags,
- same poison projection window and clamp behavior,
- same rounding behavior,
- same source/boundary fields in snapshots and manifests.

If any item differs, either keep the helper local or give the shared helper an
explicit semantic name such as `card_cost_bucket_for_build_audit`.

## Slice Template

Each slimming PR or commit should be small enough to summarize like this:

```text
Slice:
- Module(s):
- Removed local helper(s):
- Shared owner added/reused:
- Output behavior expected to stay identical:
- Focused tests:
- Full gate:
- Net diff:
- Boundaries preserved:
```

Prefer one helper family per slice. For example:

- cost bucket helpers,
- text-search helpers,
- poison projection helpers,
- artifact manifest helpers,
- report renderer extraction.

## Validation Matrix

Minimum validation for a slimming slice:

| Change Type | Required Validation |
| --- | --- |
| Shared fact added | fact model focused tests plus every migrated consumer test |
| Local helper alias/delete | consumer focused tests plus script tests for touched CLIs |
| Payload shape touched | snapshot JSON tests and report tests |
| Report renderer moved | report text tests and snapshot tests |
| Capability graph surface touched | `python scripts/validate_capability_graph.py` |
| Any implementation/refactor branch | `python scripts/check_daily_log_branch_policy.py --base-ref origin/master` |
| Commit-ready | full `py -3.11 -m pytest -q -n auto --dist=loadscope` |

Also run:

```powershell
python scripts/check_text_encoding.py
git diff --check
```

## Recommended Batch Order

### Batch A: Shared Small Helpers

Low risk and usually net-deleting:

- repeated cost bucket helpers with identical semantics,
- repeated artifact completeness helpers,
- repeated `source_chain` boundary constants if output is identical.

### Batch B: Fact Model Consumers

Good payoff, moderate risk:

- modules that recompute card text,
- modules that recompute active numeric routes,
- modules that recompute condition/delay/multiplier markers,
- modules that recompute poison projection.

### Batch C: Rule Spec Extraction

Higher payoff but should wait until facts are stable:

- value bands,
- axis role labels,
- status label maps,
- condition-quality pattern tables,
- character skeleton role definitions.

### Batch D: Report Lane Split

Useful after payload logic is stable:

- move long Markdown builders into renderer helpers,
- keep report text tests to lock Chinese readability,
- do not recompute evaluator decisions inside renderers.

## Stop Conditions

Stop and report instead of editing when:

- the helper name matches but semantics differ,
- tests rely on historical `tmp/combat_analysis` output,
- a slice would change thresholds, score weights, or hard-gate behavior,
- a module has untracked or user-edited files in the same write scope,
- the cleanup requires deleting a route still referenced by descriptor/router tests.

## Example: Cost Bucket Cleanup

Good shared helper name:

```python
card_cost_bucket_for_build_audit(cost)
```

Why this name is safe:

- it says the helper is an audit bucket, not canonical gameplay cost,
- it captures `X` cost as a build-audit estimate,
- it avoids merging different value-audit or role-classifier semantics.

Bad shared helper name:

```python
cost_value(cost)
```

Why this is risky:

- old modules use different fallbacks,
- some treat `X` as `1.5`, some as `2`, some as `3`,
- a generic name invites accidental semantic drift.

## Desired End State

After several slices, an old exam module should mostly contain:

- contract constants,
- local rule tables that are genuinely unique,
- one evaluator head,
- one payload builder,
- one report renderer or a thin call to a renderer,
- no repeated artifact helpers,
- no repeated card fact scans,
- clear focused tests for the behavior it owns.

The expected effect is gradual: early slices may reduce only a few lines. Larger
line-count reductions should appear after multiple modules consume the same fact
model and rule-spec helpers.
