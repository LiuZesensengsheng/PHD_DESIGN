# Virtue Affliction Architecture Blueprint V1

## Purpose

Define the report-only architecture for a DD1-inspired virtue/affliction design
model before any implementation work starts.

This blueprint turns the research and math model into an architecture plan:
which layers exist, which artifacts move between them, how the cardanalysis
capability graph should see the model, and what must stay out of scope.

This is not runtime gameplay architecture. It does not design formal cards,
write runtime data, add hard gates, or change default generation, learning,
synthesis, reranker, campaign curve, or core exam behavior.

## Problem

The project now has two DD1-only documents:

- `DD1_STRESS_VIRTUE_AFFLICTION_RESEARCH_V1.md`
- `VIRTUE_AFFLICTION_DESIGN_MODEL_V1.md`

They identify the useful design structure and propose a math-backed evaluator,
but they do not yet define a future implementation architecture. Without an
architecture boundary, later work could easily drift into one of three bad
shapes:

1. a runtime stress system hidden inside gameplay code,
2. a second report-only model that duplicates `stress_resolve_model_v1`,
3. a graph registration that claims authority before the model has fixtures and
   tests.

## Constraints

- Learn from Darkest Dungeon 1 only.
- Keep source references as `source_mined` or `design_reference`, not reviewed
  evidence.
- Stay under the cardanalysis north-star loop:
  `case -> normalized case -> feature projection -> capability/model head -> application`.
- Reuse the existing capability dependency/conflict graph vocabulary.
- Prefer report-only contracts before code.
- Preserve `advisory_context_only`.
- Keep capability graph changes minimal and limited to report-only coverage
  unless a later consumer integration is approved.
- Do not edit default entrypoints.
- Do not enter campaign runtime, combat runtime, or card package generation.

## Complexity

Essential complexity:

- The model has stateful time evolution: stress buildup, threshold, branch,
  state persistence, contagion, recovery, and future cost.
- The model crosses local and party levels: one character's state can affect
  others.
- It must be comparable with `stress_resolve_model_v1` without stealing that
  model's broader ownership.
- It needs enough math to avoid hand-wavy design language, but not so much math
  that it pretends to be tuned gameplay.

Accidental complexity to avoid:

- source-specific DD1 naming and exact values;
- DD2 relationship/affinity modeling;
- runtime implementation;
- consumer or authority graph edges before the owner module and report artifact
  exist;
- score-like outputs that look like hard gates.

## Options

| Option | Shape | Cost | Benefit | Main Risk |
| --- | --- | --- | --- | --- |
| A. Fold into `stress_resolve_model_v1` now | Add virtue/affliction as a subsection of existing stress/resolve docs and future evaluator. | Low surface count. | Keeps stress ownership centralized. | Loses threshold-branch specificity and makes DD1 learning harder to inspect. |
| B. Standalone report-only model head later | Keep docs now; later add a narrow owner module, CLI, fixture, report, and graph node. | Moderate. | Preserves DD1 threshold-branch structure and graph clarity. | Could duplicate stress/resolve if not review-gated. |
| C. Runtime-first system design | Begin designing combat/campaign mechanics directly. | High. | Faster path to playable behavior. | Violates current boundaries and skips advisory validation. |

## Risks

- The architecture may overfit to DD1 and miss this project's tone.
- The model may duplicate `stress_resolve_model_v1`.
- Future graph registration could make the model look more authoritative than
  it is.
- Numeric metrics could be misused as hard pass/fail gates.
- A future implementation could accidentally feed default synthesis or reranker
  paths.

## Recommendation

Choose Option B, but split it into phases.

The model should become a standalone report-only head only after it has:

1. a stable owner module,
2. a CLI that emits report/snapshot/manifest,
3. fixtures that prove DD1-derived inputs cannot claim reviewed status,
4. report output that avoids `overall_pass` and `hard_gates`,
5. minimal graph coverage that does not imply consumer integration.

Until then, keep this work as architecture docs plus a model contract.

## Counter-Review

The strongest counterargument is that this should simply be part of
`stress_resolve_model_v1`. That may become correct later. The reason not to fold
it in immediately is that the threshold branch has distinct evaluation
questions: suspense, positive break, negative break, contagion, agency loss, and
long-term consequence. Those deserve a clean model first. If the future
implementation finds that the distinction adds little value, merge the useful
metrics back into `stress_resolve_model_v1` and do not promote a separate
capability.

## Decision Summary

Adopt a phased, report-only architecture. Keep DD1 virtue/affliction as a
separate architecture and model head with only minimal report-only graph
coverage. Later implementation may add explicit consumers, but only with graph
review and explicit non-authority boundaries.

## Layered Architecture

```text
Source Reference Layer
  -> Case Normalization Layer
  -> Feature Projection Layer
  -> Model Head Layer
  -> Report/Application Layer
  -> Governance Graph Layer
```

### Source Reference Layer

Role:

- Holds DD1 research notes and source-mined references.
- Preserves source status and uncertainty.
- Prevents DD1 material from being treated as reviewed project evidence.

Artifacts:

- `dd1_stress_virtue_affliction_research_v1`
- source URLs and design notes

Rules:

- DD1-derived entries must remain `source_mined` or `design_reference`.
- DD1 values are examples, not project tuning.
- DD2 material is out of scope for this architecture.

### Case Normalization Layer

Role:

- Adapts source notes or future owner-written examples into
  `cardanalysis_case_input_v1`.
- Keeps provenance, review status, and forbidden uses visible.

Future artifact:

- `normalized_design_case`

Allowed `design_object.object_type`:

- `stress_resolve_model`
- `experience_pattern`
- or a later reviewed `stress_threshold_loop` type if repeated cases need it.

Rules:

- Do not add a new object type until existing case-input vocabulary is
  insufficient.
- Do not normalize source-mined DD1 material as `reviewed`.

### Feature Projection Layer

Role:

- Converts normalized cases into metric-ready features.
- Keeps model math independent from raw source phrasing.

Future artifact:

- `virtue_affliction_feature_projection`

Feature groups:

- `stress_sources`
- `recovery_sources`
- `threshold_definition`
- `branch_probability_modifiers`
- `positive_break_effects`
- `negative_break_effects`
- `contagion_edges`
- `agency_loss_modes`
- `long_term_costs`
- `forbidden_uses`

Rules:

- Projection is report-only.
- Projection should expose missing fields as `unknown`, not infer false
  certainty.
- Projection must preserve source trace.

### Model Head Layer

Role:

- Owns the math-backed advisory evaluation.
- Computes or estimates metrics from the projection.
- Emits dimension findings and transferability notes.

Future owner path if implemented:

- `tools/combat_analysis/design_engine/virtue_affliction_design_model.py`

Future CLI if implemented:

- `scripts/run_virtue_affliction_design_model.py`

Future tests if implemented:

- `tests/toolkit/combat_analysis/test_virtue_affliction_design_model_v1.py`
- `tests/scripts/test_run_virtue_affliction_design_model.py`

Output artifact:

- `virtue_affliction_design_report`

Rules:

- Output must include `evaluation_mode=report_only`.
- Output must include `authority_boundary=advisory_context_only`.
- Output must not include `overall_pass` or `hard_gates`.
- Output must not create formal cards or runtime data.

### Report/Application Layer

Role:

- Presents the model's findings to humans.
- Supports design review, future architecture discussion, and comparison with
  `stress_resolve_model_v1`.

Allowed applications:

- human-facing advisory report,
- architecture review,
- future design prompt context with forbidden uses visible.

Forbidden applications:

- default synthesis,
- learned/reranker default behavior,
- card legality,
- hard gate promotion,
- runtime gameplay mutation.

### Governance Graph Layer

Role:

- Tracks provider/consumer ownership, conflicts, invalidation, and review gates.
- Prevents the model from silently overlapping with existing stress/resolve or
  campaign pacing work.

The live graph has only the registry-derived report-only surface node and report
artifact. The richer edges below remain a future registration plan.

## Current Minimal Graph Coverage

Registered now:

- `virtue_affliction_design_model_v1` as a canonical report-only surface
  capability.
- `virtue_affliction_design_report` as its advisory report artifact.
- authority dependencies shared by all report-only registry surfaces.

Not registered now:

- `virtue_affliction_feature_projection`.
- consumer edges from normalized cases or feature projection.
- review-gated edges with `stress_resolve_model_v1`.
- conflicts with default synthesis, runtime data, or hard-gate promotion as
  concrete graph nodes.
- any default entrypoint, generation, learned, reranker, runtime, campaign
  curve, or core-exam integration.

## Future Graph Registration Plan

Register richer edges only after a later integration review decides this model
has live consumers or overlap with `stress_resolve_model_v1`.

### Proposed Capability Node

```yaml
id: virtue_affliction_design_model_v1
kind: capability
display_name: Virtue Affliction Design Model V1
owner_path: tools/combat_analysis/design_engine/virtue_affliction_design_model.py
status: draft
trust_tier: report_only
object_types:
  - stress_resolve_model
  - experience_pattern
write_scope:
  - docs/development/cardanalysis/VIRTUE_AFFLICTION_DESIGN_MODEL_V1.md
  - docs/development/cardanalysis/VIRTUE_AFFLICTION_ARCHITECTURE_BLUEPRINT_V1.md
  - tools/combat_analysis/design_engine/virtue_affliction_design_model.py
  - scripts/run_virtue_affliction_design_model.py
  - tests/toolkit/combat_analysis/test_virtue_affliction_design_model_v1.py
  - tests/scripts/test_run_virtue_affliction_design_model.py
parallel_safety: medium
notes:
  - DD1-only source-mined/design-reference learning.
  - Report-only threshold-branch evaluator.
  - Review-gated with stress_resolve_model_v1.
```

### Proposed Artifact Nodes

```yaml
id: virtue_affliction_feature_projection
kind: artifact
status: draft
trust_tier: report_only
```

```yaml
id: virtue_affliction_design_report
kind: artifact
status: draft
trust_tier: report_only
```

```yaml
id: decision_dd1_values_not_project_tuning
kind: decision
status: draft
trust_tier: decision_frozen
```

### Proposed Edges

| Source | Relation | Target | Severity | Reason |
| --- | --- | --- | --- | --- |
| `virtue_affliction_design_model_v1` | `depends_on` | `decision_report_only_surfaces_not_authoritative` | hard | The output cannot become authority. |
| `virtue_affliction_design_model_v1` | `depends_on` | `decision_dd1_values_not_project_tuning` | hard | DD1 numbers and labels are not project defaults. |
| `virtue_affliction_design_model_v1` | `optional_depends_on` | `stress_resolve_summary` | soft | Broader stress context can improve wording. |
| `virtue_affliction_design_model_v1` | `consumes` | `virtue_affliction_feature_projection` | hard | Future implementation reads projected features. |
| `virtue_affliction_design_model_v1` | `provides` | `virtue_affliction_design_report` | hard | The report is the only model output. |
| `virtue_affliction_design_model_v1` | `review_gated_with` | `stress_resolve_model_v1` | soft | Prevent duplicate stress-threshold ownership. |
| `virtue_affliction_design_model_v1` | `review_gated_with` | `campaign_power_curve_report_v1` | soft | Required only if campaign pacing is discussed. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `default_synthesis_path` | hard | Report cannot drive default content generation. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `runtime_data_generation` | hard | Report cannot write runtime payloads. |
| `virtue_affliction_design_model_v1` | `conflicts_with` | `hard_gate_promotion` | hard | Report cannot become pass/fail authority. |

## Future Module Boundary

If implemented, place the model under `design_engine`, not `design_studio`.

Reason:

- It is an analysis/report head, not an owner-filled package drafting surface.
- It may later be consumed by autonomous design evaluation or evidence bundles.
- `design_engine` already owns several report-only advisory surfaces.

Do not let `design_engine` import from `design_studio` for this work.

Suggested module responsibilities:

| Module | Responsibility |
| --- | --- |
| `virtue_affliction_design_model.py` | Pure report model and snapshot construction. |
| `run_virtue_affliction_design_model.py` | CLI wrapper, template writing, output directory handling. |
| fixture JSON | Minimal DD1-derived source-mined/design-reference input and counterexamples. |
| tests | Boundary rejection, report shape, metric finding presence, no hard gates. |

## Data Flow

```text
input JSON or normalized case
-> source status guard
-> projection adapter
-> metric estimator
-> dimension classifier
-> transferability classifier
-> report/snapshot/manifest
```

### Source Status Guard

Must reject:

- `reference_family = "darkest_dungeon_1"` with `evidence_tier = "reviewed"`;
- missing `authority_boundary`;
- forbidden-use omissions for runtime, formal-card, hard-gate, and default
  synthesis paths.

### Projection Adapter

Should produce:

- stress source counts and labels,
- recovery source counts and labels,
- threshold visibility,
- branch probability fields,
- positive and negative break effects,
- contagion map,
- long-term consequence fields.

### Metric Estimator

Should estimate:

- `stress_growth_rate`
- `time_to_threshold`
- `branch_entropy`
- `outcome_contrast`
- `threshold_drama_score`
- `positive_break_value`
- `negative_break_cost`
- `stress_contagion_rate`
- `cascade_reproduction`
- `agency_preservation`
- `long_term_cost`

Metrics may be qualitative when numeric inputs are absent. Use `unknown` rather
than inventing false precision.

The current implementation also emits an advisory index layer:

- `pressure_readability_index`
- `buildup_answerability_index`
- `threshold_suspense_index`
- `reversal_integrity_index`
- `affliction_integrity_index`
- `contagion_runaway_risk_index`
- `agency_floor_index`
- `carryover_weight_index`
- `psychological_loop_health_index`

These indices are explanatory math, not gates. They support
`interpretive_conclusions` such as `healthy_psychological_state_loop`,
`bad_agency_erasing_loop`, `bad_reward_farming_loop`, and
`weak_or_non_psychological_loop`. A later integration must not treat these
labels or numeric values as runtime tuning, default synthesis input, learned
targets, or pass/fail authority.

### Dimension Classifier

Required dimensions:

- `stress_buildup`
- `threshold_drama`
- `positive_break`
- `negative_break`
- `team_contagion`
- `long_term_consequence`
- `agency_preservation`

Labels:

- `strong`
- `mixed`
- `weak`
- `unsafe`
- `unknown`

### Report Writer

Must write:

- Markdown report,
- JSON snapshot,
- JSON manifest.

Must not write:

- runtime data,
- formal card data,
- hard-gate verdicts,
- default synthesis hints.

## Phased Rollout

### Phase 0: Docs Architecture

Status: complete on the current branch.

Scope:

- research report,
- math model contract,
- architecture blueprint.

Validation:

```powershell
git diff --check
py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q
```

### Phase 1: Contract Fixture Prototype

Scope:

- add fixture input shape under `tests/fixtures/combat_analysis`;
- add no runtime integration;
- keep fixture source tier `source_mined` or `design_reference`.

Validation:

```powershell
py -3.11 -m pytest tests/shared/test_text_encoding_guards.py -q
```

Add fixture-specific tests only when code exists.

### Phase 2: Report-Only Model Head

Status: complete on the current branch.

Scope:

- add owner module,
- add CLI,
- add template writer,
- add report/snapshot/manifest output,
- add tests proving source-status rejection and no hard gates.

Validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_virtue_affliction_design_model_v1.py tests/scripts/test_run_virtue_affliction_design_model.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```

### Phase 3: Minimal Graph Coverage

Status: complete on the current branch.

Scope:

- register the report-only capability and report artifact required by registry
  coverage in `tools/combat_analysis/capability_graph_registry.py`;
- add graph tests;
- do not add consumers, default paths, runtime paths, or hard gates.

Validation:

```powershell
python scripts/validate_capability_graph.py
py -3.11 -m pytest tests/toolkit/combat_analysis/test_capability_graph_registry_v1.py -q
```

### Phase 4: Application Integration Review

Scope:

- decide whether the report feeds `evaluation_autonomous_design_model_v1`,
  `cardanalysis_evidence_bundle_v1`, or stays standalone.
- if it gains stress-threshold ownership overlap, add a review-gated edge with
  `stress_resolve_model_v1`.

Validation:

- use the owning tests for every consumer named in the integration.
- do not add default generation or reranker behavior.

## Architecture Guardrails

- `virtue_affliction_design_model_v1` must remain report-only.
- No output field named `overall_pass`.
- No output field named `hard_gates`.
- No runtime data output path.
- No formal card text.
- No default synthesis, learned, or reranker behavior.
- No DD2 relationship/affinity scope creep.
- DD1 values are not project tuning.
- Any future consumer or ownership-overlap graph registration must be
  review-gated with `stress_resolve_model_v1`.

## Open Questions

- Should future implementation fold the model into `stress_resolve_model_v1`
  after the first report prototype?
- Should `stress_threshold_loop` become a new normalized case object type, or
  can `stress_resolve_model` plus feature hints cover the need?
- Which project-specific examples should eventually become reviewed internal
  cases before this model informs design decisions?
- Should metrics remain qualitative forever, or should numeric calibration wait
  for playtest data?
