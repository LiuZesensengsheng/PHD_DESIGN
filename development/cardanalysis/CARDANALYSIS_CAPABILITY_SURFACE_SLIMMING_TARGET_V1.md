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
current pool/review-package generation, and exam/readout paths:

| Module | Lines |
| --- | ---: |
| `programmatic_complete_card_draft_composition_guided_medium_package.py` | 3,158 |
| `programmatic_complete_card_draft_generation.py` | 2,248 |
| `programmatic_complete_card_draft_strong_build_pool.py` | 1,915 |

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

### Completed Deletion Slices

- Retired the former stress/experience report-only side heads:
  `stress_resolve_model_v1` and `campaign_experience_curve_v1`.
- Retired the learned/reranker/shadow diagnostic family:
  `pick_ranking_pairwise_reranker_v1`,
  `reviewed_retrieval_pairwise_reranker_v1`,
  `sts_catalog_holdout_pairwise_reranker_v1`,
  `reviewed_retrieval_shadow_compare_v1`,
  `sts_catalog_holdout_shadow_compare_v1`, and
  `modelization_shadow_report_v1`.
- Kept the deterministic STS holdout benchmark and deterministic ranking exports as
  the active reference route for catalog-recovery learning and validation.
- Retired the former `bounded_candidate_shadow_v1` sidecar, including its standalone
  contract fixtures, CLI, tests, and doc page.
- Retired the former Design Candidate Scout single-session/batch sidecar, including
  its engine modules, artifact reader, CLI, fixtures, tests, and doc page. Current
  report-only evidence reads should stay in mechanism-axis viability, deterministic
  STS holdout/ranking exports, fun-proxy calibration, and enemy-design probes.
- Retired the historical `programmatic_complete_card_draft` repair-stage execution
  chain: fourth-pass, targeted-provider, residual-provider, value/poison,
  retain-semantics, retain style-tension, condition-quality, and value-position
  stage modules, their unified old CLI, descriptor, dedicated tests, and active
  capability graph nodes. The hosted router still reads old snapshots but now
  stops and asks for human/current-route review instead of suggesting retired
  stage commands.
- Retired the hosted expansion/candidate repair family and the old hosted
  router: the former one-command hosted expansion, candidate-pool repair plan,
  candidate-pool repair generation, value/diversity repair generation, their
  CLI wrappers, dedicated tests, active graph nodes, and runbook entrypoints are
  gone. Current 30-card and 12-card review work should use the explicit
  strong-build pool, independent advisory exams/readouts, package composition
  profile, and composition-guided medium package routes.
- Retired the old one-command closed-loop/capability-pack/closed-test-pack
  wrapper family: closed-loop smoke, iteration-plan, capability-pack, and
  closed-test-pack scripts/modules/tests/docs are gone. Human-feedback validation
  remains active and now uses supplied closed-test-shaped snapshots or focused
  fixture inputs instead of generating the retired large wrapper output.
- Retired the standalone CLI wrappers for the energy-gain safety and poison-value
  calibration readouts. Their evaluator modules and focused toolkit tests remain
  active because the composition-guided medium-package route embeds both readouts
  as advisory context; the deleted wrapper scripts, script tests, and standalone
  manifest writers no longer make them look like separate current routes.
- Retired the standalone medium-package expansion/repair routes and the old
  Silent-only classic skeleton exam route. The 5-card-to-12-card medium expansion
  logic remains only as an embedded helper for the strong-build pool, while the
  multi-character classic skeleton exam is the canonical STS1 skeleton-alignment
  route, including Silent.

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

### 2026-06-08 Reset Goal: Codex-Usable Tool-First Slimming

The active slimming goal is reset from "delete as much cardanalysis code as
possible" to "make cardanalysis easy for Codex to use without reading internal
implementation details, then delete everything that no longer supports that
tool surface."

This is not a promise that deletion alone will create stronger card-design
ability. Deletion is valuable only when it removes route noise, duplicate
wrappers, stale report surfaces, and historical fixtures that make the current
tool hard to choose and hard to trust. The target ability is a compact,
repeatable workflow that Codex can call first, not a large internal system that
Codex must study before every design request.

The desired external shape is a small, stable tool facade:

```text
generate_or_ingest -> exam -> review_pack -> feedback -> iterate
```

Codex should be able to answer ordinary card-design requests by starting from
`scripts/run_cardanalysis_tool_facade.py`, selecting one of those five actions,
and following the returned command templates. It should not need to browse
dozens of historical report-only modules before it can decide which command to
run.

This reset changes the priority order:

1. First, make the facade trustworthy and complete enough for routine use.
2. Second, classify every live-looking route as canonical, supporting,
   delegated, registry-only, fixture-only, or archive candidate.
3. Third, delete or demote anything that is not needed by the facade, retained
   contracts, focused tests, or reviewed case evidence.
4. Fourth, only after route noise is low, continue semi-engineizing repeated
   exam logic through shared facts, descriptors, and artifact writers.

### Target State

The ideal `cardanalysis` shape is layered, with each layer having one job:

| Layer | Job | Keep Criteria | Delete/Demote Criteria |
| --- | --- | --- | --- |
| Facade | The Codex-facing action map and command templates. | It directly answers which command to run for generate/ingest, exam, review, feedback, or iterate. | It is another top-level workflow that duplicates a facade action. |
| Contracts | Input/output schemas, validators, and trust-boundary checks. | It protects `complete_card_draft_v1`, report-only authority, or human-feedback intake. | It validates only a retired historical artifact shape. |
| Engines | Shared fact extraction, descriptors, exam heads, and artifact writers. | It is called by canonical routes or protects a retained focused contract. | It only supports a retired wrapper or one obsolete report. |
| Reports | Chinese review packs, score/readout summaries, and advisory evidence. | It is human-readable and reachable from the facade. | It is an old standalone side report with no current route. |
| Fixtures/tests | Small examples that prove contracts and current behavior. | It is minimal, deterministic, and directly tied to a retained route. | It is a large generated snapshot or tmp-dependent historical output. |

### Line-Count Target

Line count is a pressure gauge, not the actual goal. The current practical
target is:

- broad named cardanalysis surface: move toward roughly `120k` lines;
- `tools/combat_analysis` Python: keep shrinking after route noise is classified;
- direct wrapper scripts/tests: continue deleting first because they create the
  most user-facing confusion per line;
- large generated fixtures/reports: compress, shrink, or retire when they no
  longer prove a live contract.

The next "good enough" slimming band is roughly `110k` to `125k` broad named
cardanalysis lines, with the remaining surface explicitly classified. Reaching
that band matters less than ensuring a new Codex session can operate the system
from the facade without opening old route-history documents.

### Execution Phases

1. Route noise audit: remove or classify remaining `registry_only` and
   non-facade active-looking routes.
2. Wrapper deletion: retire standalone CLIs and one-test-per-wrapper coverage
   when the wrapper only delegates to a canonical route.
3. Artifact cleanup: replace tmp-dependent and overlarge historical fixtures
   with minimal contract fixtures.
4. Shared report/artifact cleanup: keep one artifact writer path where practical
   and delete duplicate manifest/snapshot writers.
5. Engine consolidation: table-drive repeated exams only after the retained
   route shape is clear.

### Route Noise Audit Status

The first route-noise pass classifies retained non-facade surfaces instead of
leaving them as ambiguous `registry_only` entries:

- `calibration_support`: retained benchmark or health-calibration surfaces such
  as mechanism viability, mechanism fun health, and card package health.
- `evidence_support`: retained evidence normalization such as the cardanalysis
  evidence bundle.
- `non_facade_design_support`: retained broader design-support surfaces such as
  autonomous design review and campaign power-curve context.
- `contract_reference`: retained docs/contracts that describe inputs but are
  not executable routes.
- `decision_record`: graph decision nodes that document architectural
  constraints.

After this pass, `registry_only` should be treated as a real audit smell rather
than an expected bucket. If a future capability lands there, either route it
through the facade, give it an explicit support class, or archive/delete it.

### Non-Goal Clarification

Slimming does not mean every report-only capability must be preserved. If a
report-only route does not feed the facade, does not protect a current contract,
and is not retained as reviewed evidence or a small fixture, it may be deleted.
The report-only boundary is still mandatory for what remains: retained outputs
must stay advisory and must not become runtime card data, hard gates, official
card promotion, learned reranking, LLM/API calls, or reviewed-evidence upgrades.

### Practical Completion Signals

This target is considered good enough for the next design phase when all of the
following are true:

- `python scripts/run_cardanalysis_tool_facade.py --check` passes and covers the
  current Codex-facing routes plus their input-preparation support routes.
- A new Codex session can use the facade docs and commands to choose the next
  command for generate/ingest, exam, Chinese review-pack, feedback, or iterate
  without opening old route-history documents.
- The broad named cardanalysis surface is at or below about 120k lines, with
  direct-entrypoint noise reduced first and the remaining non-facade surfaces
  explicitly classified.
- New card-design ability is added behind an existing facade action unless a
  route-map update explicitly justifies a new action.
- Historical report-only work remains readable as library, fixture, or archive
  context, but does not look like a current default workflow.
- The retained loop still works: complete-card draft validation, programmatic or
  external draft intake, STS1/package exams, 12-card Chinese review packs,
  30-card/strong-build readouts, human feedback, and next-round advisory
  iteration.

The target is not to erase every report-only module. The target is to stop
report-only sprawl from being the interface.

The capability surface inventory should treat facade input-preparation commands
as `supporting_route`, not `direct_entrypoint`. This keeps mechanism-axis
search, design brief, package seed, and similar setup commands visible to Codex
without making them look like independent top-level workflows.

The inventory should also treat a small number of unified report/tool commands
as `canonical_report_route`. Examples include the cardanalysis facade,
cardanalysis report multiplexer, capability-surface inventory, and STS1
four-character exam command. These are stable tools Codex can call directly;
they should not be counted as legacy direct-entrypoint sprawl.

Schema and input-contract validators should be classified as
`contract_validator_route`. A validator route is allowed to remain directly
callable when it protects an input contract, but it should not be mistaken for a
separate card-design workflow.

Capability graph artifact nodes should be classified as `graph_artifact`, not
`registry_only`. Artifact rows such as `complete_card_draft_package` or
`card_package_exam_snapshot` are graph vocabulary, not live capability routes.
This keeps `registry_only` focused on active-looking capability owners that may
need deletion, demotion, or explicit route-map treatment.

Retired standalone commands whose library contracts are still consumed by a
facade-backed route should be classified as `supporting_library`. For example,
`exam_iteration_run_v1` and `exam_iteration_prompt_patch_proposal_v1` support
external draft intake and legacy single-attempt feedback records, but they are
not Codex-facing routes. They should stay out of `registry_only` unless their
remaining consumers disappear.

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

### 2026-06-08 Active Goal: Facade-First 12w Slimming

The active goal is reset to match the current branch state and the user's
near-term need: make `cardanalysis` usable as a compact Codex-callable tool
first, then keep deleting historical report-only sprawl until the broad named
surface is about 120k lines.

The tool path remains:

```text
generate_or_ingest -> exam -> review_pack -> feedback -> iterate
```

This goal is not "delete everything report-only." It is "delete or demote
everything that makes Codex need to understand old internal sidechains before it
can use the tool."

Current branch measurements after the latest route-retirement passes:

| Surface | Current | 12w Target | Remaining Reduction |
| --- | ---: | ---: | ---: |
| Broad named cardanalysis surface | 136,521 | about 120,000 | about 16,500 |
| `tools/combat_analysis` Python | 128,989 | about 110,000-120,000 | about 9,000-19,000 |
| `design_studio` Python | 77,182 | about 65,000-70,000 | about 7,000-12,000 |
| Narrow complete-card draft chain | 43,627 | about 35,000-40,000 | about 4,000-9,000 |
| Registry-only rows | 75 rows | sharply lower/no active-looking route noise | classify, delete, or demote |

Execution priority:

1. Keep the facade complete, live, and easy to query.
2. Retire default-route wrappers that no longer belong to the canonical
   complete-card generation/exam/review loop.
3. Remove matching script-level route tests when toolkit contract tests already
   protect the retained library surface.
4. Downgrade historical report-only routes to library/fixture/archive status
   instead of leaving them active-looking in runbooks.
5. Consolidate repeated report/snapshot/manifest writers only after route noise
   is removed.
6. Compress or remove oversized historical fixtures after a representative
   fixture and contract test remain.

The 12w target must not be reached by deleting current complete-card schema,
programmatic generation, composition-guided 12-card package, 30-card
strong-build pool, core STS1/value/similarity/composition exams, Chinese review
packets, or human-feedback intake surfaces.

After the 12w target is reached, decide whether to continue toward a stricter
9w-11w target. That second target should require more semi-engineization of
shared facts and exam descriptors; it should not be attempted by deleting the
current Chinese review and strong-build design loop.

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
