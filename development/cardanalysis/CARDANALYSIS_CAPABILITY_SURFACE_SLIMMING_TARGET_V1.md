# Cardanalysis Capability Surface Slimming Target V1

## Problem

The current cardanalysis surface has grown from a focused report-only design
assistant into a large capability cluster. The risk is no longer only line count.
The larger risk is capability sprawl:

- new abilities keep being added as new modules, CLIs, tests, fixtures, reports,
  and docs;
- old abilities remain active-looking even after a newer route replaces them;
- humans and agents cannot easily answer which route is canonical;
- future engineering cardpool work may add another layer of one-off generators,
  exams, and reports unless the ownership model is tightened now.

The system already has useful governance pieces: capability graph, report-only
registry, hosted router, unified repair-stage CLI, shared artifact helpers, and
the slimming template. They now need to become an active slimming loop, not just
documentation around a growing system.

## Constraints

- Keep cardanalysis outputs `report_only` / `advisory_context_only`.
- Do not write runtime card data.
- Do not promote generated drafts into formal cards.
- Do not create hard gates.
- Do not change score weights, default synthesis, learned paths, rerankers, or
  reviewed-evidence claims.
- Do not call LLM/API as part of cleanup.
- Do not edit dated daily logs on implementation/refactor branches.
- Prefer real net deletion over large move-only diffs.
- Preserve behavior before deleting historical routes.

## Complexity

### Current Measured Surface

Measured from tracked files on branch `codex/06-03-cardanalysis-fact-model-engine`
after commit `ffe4b78e`.

Line counts are planning measurements, not release accounting. Different tools
may count final newlines and generated/current branch additions differently; use
them for trend, ranking, and deletion-candidate selection.

| Surface | Files | Lines |
| --- | ---: | ---: |
| Full `tools/combat_analysis` tracked surface | 499 | 264,072 |
| Python under `tools/combat_analysis` | 291 | 201,032 |
| `tools/combat_analysis/design_studio/*.py` | 172 | 140,644 |
| Broad named cardanalysis surface, including tools/scripts/tests/docs/data | 651 | 240,057 |
| Narrow `programmatic_complete_card_draft*` chain | 183 | 88,235 |

Broad named cardanalysis surface split:

| Area | Files | Lines |
| --- | ---: | ---: |
| Related `tools/combat_analysis` Python | 128 | 101,950 |
| Related `design_studio` Python | 116 | 94,543 |
| Related `scripts` Python | 97 | 15,591 |
| Related Python tests | 221 | 42,787 |
| Related test fixtures/data/docs | 152 | 37,453 |
| Related tools docs/data non-Python | 53 | 42,276 |

The live capability graph currently validates cleanly, but it also shows the
scale of the surface:

| Capability Graph Item | Count |
| --- | ---: |
| Artifact nodes | 113 |
| Capability nodes | 99 |
| Task nodes | 2 |
| Decision nodes | 2 |
| Active nodes | 216 |
| `report_only` trust-tier nodes | 208 |
| Owner paths under `design_studio` | 92 |

### Main Hotspots

The largest current `design_studio` modules are concentrated in generated draft,
repair iteration, exam/readout, and hosted expansion paths:

| Module | Lines |
| --- | ---: |
| `programmatic_complete_card_draft_composition_guided_medium_package.py` | 3,158 |
| `programmatic_complete_card_draft_hosted_expansion_run.py` | 3,046 |
| `axis_first_rehearsal_scorecard_comparison.py` | 2,277 |
| `programmatic_complete_card_draft_generation.py` | 2,248 |
| `programmatic_complete_card_draft_targeted_provider_repair_iteration.py` | 1,975 |
| `reviewed_retrieval_shadow_compare.py` | 1,953 |
| `programmatic_complete_card_draft_strong_build_pool.py` | 1,915 |
| `programmatic_complete_card_draft_residual_provider_repair_iteration.py` | 1,859 |
| `programmatic_complete_card_draft_value_poison_calibration_iteration.py` | 1,847 |
| `sts1_ironclad_multi_axis_medium_package_batch.py` | 1,701 |

### Essential Complexity

These parts are real and should stay:

- case/input contracts;
- complete-card draft schema validation;
- STS1 and package exam heads;
- generated-hypothesis draft intake;
- Chinese human-review packets;
- report-only boundary assertions;
- capability graph and report-only registry;
- focused tests that protect output contracts;
- strong-build, value, similarity, role, and composition exams once they are
  table-driven and reachable through a canonical route.

### Accidental Complexity

These parts should shrink:

- one CLI wrapper per historical stage;
- one script test per wrapper when the wrapper only delegates;
- repeated manifest/snapshot/report writer code;
- repeated card fact extraction in every exam;
- repeated cost/value/condition text scans with slightly different local names;
- historical repair modules named by iteration round instead of stage role;
- docs and entrypoint lists that keep old routes looking equally canonical;
- tests that depend on historical `tmp/combat_analysis` outputs.

## Options

### Option 1: Keep Adding Capabilities And Rely On Docs

This is the default drift path. It has low immediate cost, but it lets every new
ability create a new module, CLI, test, fixture, report, and doc page.

This option is not acceptable long term. It keeps cardanalysis useful in the
short term but makes future engineering cardpool work harder to reason about.

### Option 2: Big Rewrite Into One Exam Engine

This could eventually reduce a large amount of code. It is too risky now because
the design rules are still changing: value-per-energy, condition quality,
similarity, role ratio, strong-build detection, and mechanism-axis fit are still
being calibrated.

This option should remain a future possibility, not the next step.

### Option 3: Semi-Engineized Slimming Loop

Adopt the current target shape:

```text
thin exam head
    -> shared fact model
    -> rule table / descriptor
    -> shared artifact writer
    -> canonical CLI/router route
```

Each cleanup slice must remove one concrete duplicated surface and prove the
canonical route still works.

This is the recommended path.

## Risks

- A line-count target can encourage deleting useful tests or fixtures. That is
  the wrong optimization.
- Moving helpers too early can merge semantics that only look similar.
- A unified route can hide behavior drift if descriptor parity is not tested.
- Old docs can keep deleted or deprecated paths alive in user behavior.
- Large generated reports can make diffs look productive while increasing the
  real ability surface.

## Recommendation

Use a two-level target: capability visibility first, then real deletion.

### Target Shape

Cardanalysis should have four visible layers:

| Layer | Purpose | Should Own |
| --- | --- | --- |
| Contracts | Input/output schemas and boundary rules | schema validators, report-only contracts |
| Facts | Shared extraction and normalized observations | cost buckets, card text facts, role tags, condition markers |
| Exams | Thin evaluators over facts and rule tables | value, similarity, role ratio, strong-build, axis-fit readouts |
| Routes | Canonical CLIs/router/capability pack | default entrypoints, stage descriptors, owner review packets |

Anything outside these layers should be marked as one of:

- canonical active;
- experimental active;
- historical/archive candidate;
- replaced by route;
- fixture/data only;
- docs only.

### Size Targets

These targets are not commit promises. They are the direction of travel for the
next slimming arc.

| Surface | Current | Healthy Target | Expected Net Deletion |
| --- | ---: | ---: | ---: |
| Broad named cardanalysis surface | 240k | 140k-170k | 70k-100k |
| `design_studio` Python | 140k | 70k-90k | 50k-70k |
| Narrow complete-card draft chain | 88k | 35k-50k | 35k-50k |
| Script wrappers | 15.6k | 5k-8k | 7k-10k |
| Python tests for wrappers/stages | 42.8k | 25k-32k | 10k-17k |

The first few cleanup commits may be smaller. The large deletion only appears
after wrappers, route descriptors, artifact writers, and repeated tests are
merged.

### Next Slimming Loop

1. Build a generated capability inventory report.
   - Fields: capability id, owner path, line count, route/CLI, status, trust
     tier, tests, write scope, router reachable, archive candidate.
   - Source: capability graph registry, tracked file sizes, runbook entries.

2. Mark route status.
   - `canonical`: default route humans/agents should use.
   - `delegated`: old wrapper or helper route that forwards to canonical route.
   - `historical`: kept only for output-history comparison.
   - `archive_candidate`: replacement exists and tests cover it.

3. Delete by families, not by random files.
   - More thin CLI wrappers after unified route parity is proven.
   - Duplicated wrapper tests that only check delegation.
   - Repeated report/snapshot/manifest writer helpers.
   - Repeated local card fact scans after shared fact tests are in place.
   - Historical repair stage modules only after descriptor and output parity are
     locked.

4. Keep a per-slice deletion summary.
   - Removed duplicate logic.
   - New or reused owner.
   - Behavior expected unchanged.
   - Focused tests and full gate.
   - Net line deletion.

## Counter-Review

This plan does not immediately delete tens of thousands of lines. That is
intentional. The biggest current risk is deleting a route whose replacement is
not actually canonical, or moving local helpers whose semantics differ.

The plan is still stricter than normal documentation because it creates a
repeatable deletion loop:

- ability inventory makes hidden sprawl visible;
- route status prevents old paths from looking equally active;
- descriptor parity makes wrapper deletion safer;
- shared fact tests make evaluator slimming safer;
- each PR must show real net deletion or explain why it only prepared deletion.

## Decision Summary

Adopt Option 3: semi-engineized slimming.

The near-term cardanalysis architecture target is:

```text
contracts + shared facts + thin exam heads + canonical routes
```

The next implementation slice should not add new card-design ability. It should
produce the capability inventory and route-status report, then use that report to
delete the next duplicated wrapper/report/test family with a measurable net
deletion.

Treat this as a system health task required before large engineering cardpool
generation resumes. Otherwise the project will keep accumulating useful but
hard-to-locate abilities, and cardanalysis will become harder to trust exactly
when we need it to generalize.
