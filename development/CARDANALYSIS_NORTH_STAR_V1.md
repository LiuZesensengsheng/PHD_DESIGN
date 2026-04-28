# Cardanalysis North Star V1

## Purpose

Define the stable product and architecture direction for `cardanalysis` before
the analysis surface expands further.

The goal is not to freeze every future metric. The goal is to keep new case
work, evaluator work, modelization work, and autonomous design work aligned
around one small contract.

## North Star

`cardanalysis` should become a low-maintenance, case-backed, multi-head design
analysis system for:

1. discovering promising mechanism axes,
2. evaluating mechanism viability and fun/health,
3. evaluating and iterating card packages,
4. reasoning about campaign pacing and encounter pressure,
5. supporting autonomous design exploration without becoming final authority.

The system should spend most future effort on reviewed case accumulation and
case normalization, not on endlessly growing hand-written rules.

## Working Loop

The preferred long-term loop is:

```text
case -> normalized case -> feature projection -> capability/model head -> application
```

Where:

- `case` is the source observation, fixture, reference, or design note.
- `normalized case` is the common input DTO that protects consumers from source
  drift.
- `feature projection` is the reusable translation from case evidence into
  analysis features.
- `capability/model head` is a focused evaluator, report, benchmark, reranker,
  or later learned head.
- `application` is design iteration, autonomous exploration, merge review, or a
  human-facing report.

## Authority Boundary

Report-only surfaces are advisory context. They may inform design review,
ranking, exploration, and follow-up planning, but they must not become hard
pass/fail authority.

Hard gates remain explicit, reviewed, and test-locked. A learned or report-only
head must not decide legality, schema validity, synthesis eligibility, or final
promotion on its own.

The current canonical authority wording is:

```text
advisory_context_only
```

## Capability Layers

### Case Layer

Stores reviewed fixtures, source-mined references, design notes, and playtest
observations in a source-aware format.

This layer should preserve provenance and uncertainty. It should not pretend
that source-mined or speculative evidence is reviewed evidence.

### Feature Projection Layer

Translates normalized cases into reusable feature payloads.

This layer is the anti-corruption boundary between messy external/game-specific
material and stable internal evaluators.

### Capability Head Layer

Owns focused analysis behavior.

Examples:

- `mechanism_axis_viability_v1`
- `mechanism_fun_health_v1`
- `deck_compression_report_v1`
- `card_package_health_v1`
- `campaign_power_curve_report_v1`
- `evaluation_autonomous_design_model_v1`

Each head should stay narrow enough that it can be tested and replaced.

### Application Layer

Combines advisory outputs into useful workflows.

Examples:

- design iteration briefs,
- autonomous design reviews,
- evidence bundles,
- multi-agent task planning,
- future design exploration sessions.

Applications may combine evidence. They should not silently seize canonical
ownership from the underlying capability heads.

### Governance Graph Layer

The capability dependency/conflict graph tracks:

- dependency,
- provider/consumer ownership,
- conflict,
- invalidation,
- parallel-work safety.

It is a planning and contamination-control layer, not a replacement for the
actual evaluators or reviewed case evidence.

## Near-Term Priorities

1. Keep `report-only` authority boundaries stable.
2. Establish a shared case input contract for new evidence.
3. Register case/input and feature-projection artifacts in the capability graph.
4. Grow reviewed case packs where they improve coverage or expose failure modes.
5. Use the graph to split multi-agent work before implementation starts.

## Explicit Non-Goals

- Do not build a monolithic all-knowing evaluator.
- Do not require every old fixture to migrate before new work can proceed.
- Do not promote source-mined references into reviewed evidence.
- Do not hard-code every possible future fun, balance, or flavor dimension in V1.
- Do not replace human design judgment with a report-only score.
- Do not let autonomous design generate default content without explicit review
  and promotion.

## Success Criteria

V1 is successful when:

1. new case work has a clear input shape,
2. new model/evaluator heads can state which artifacts they consume and provide,
3. parallel agents can be checked for dependency and conflict before they start,
4. the system can add or remove dimensions without rewriting every evaluator,
5. reviewed case growth becomes more valuable than manual rule tweaking.

## Relationship To Existing Assets

Existing fixtures, reports, CLIs, and benchmarks remain valid.

This north star adds direction and vocabulary. It does not force an immediate
migration of current assets. New case-like work should use the case input
contract unless a focused evaluator has a stronger local fixture schema.
