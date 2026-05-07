# Mechanism Axis Search Bundle V1

## Purpose

`mechanism_axis_search_bundle_v1` is a report-only programmatic search surface for
candidate mechanism axes.

It exists to move the first pass from "LLM lists plausible axes" to "program
enumerates, scores, and explains axes from existing contracts and evidence."

The output is advisory context only. It is not a formal design conclusion, a card
package proposal, reviewed evidence, a hard gate, a default synthesis path, or a
learned/reranker promotion.

## Authority Boundary

Every request and bundle uses:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `hard_gate_impact = none`

Boundary assertions must remain false:

- `formal_card_generated`
- `hard_gate_created`
- `default_synthesis_changed`
- `learned_or_reranker_enabled`

## Program-Owned Work

The program owns:

1. Enumerating candidate axes from
   `tools/combat_analysis/design_engine/mechanism_axis_contracts.py`.
2. Pulling STS1 character affinity, current capability, reviewed-case count, and open
   gap notes from `STS1_CORE_MECHANISM_AXIS_MAP_V1.md`.
3. Pulling reviewed positive/negative contrast behavior from
   `tests/fixtures/combat_analysis/mechanism_axis_viability_v1/`.
4. Pulling fun, strength, fatigue, and confidence signals from
   `tests/fixtures/combat_analysis/deck_fun_benchmark_v1/`.
5. Pulling foundation-axis language from
   `CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`.
6. Calculating `score_components`, `overall_score`, `recommended_support_axes`,
   `evidence_refs`, and `risk_notes`.

## LLM-Owned Work

The LLM may only:

- read the program output;
- quote or summarize evidence refs;
- write a short design brief that clearly says it is advisory.

The LLM must not:

- invent candidate axes outside program enumeration;
- change program scores;
- treat the bundle as a formal design conclusion;
- claim reviewed-evidence promotion.

## Request Contract

Required fields:

- `schema_version = mechanism_axis_search_request_v1`
- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `character_id`
- `design_goal`
- `candidate_scope`

Supported `candidate_scope` values:

- `sts1_reviewed_axes`
- `all_valid_mechanism_families`

The first fixture uses Silent with high decision density, visible clock and branch
choice texture, medium setup tax, and avoidance of generic goodstuff or payoff-only
plans.

## Bundle Contract

The snapshot schema is `mechanism_axis_search_bundle_v1` and includes:

- `candidate_axes`
- `recommended_main_axes`
- `rejected_axes`
- `llm_boundary`
- `boundary_assertions`

Each candidate includes:

- `axis_id`
- `overall_score`
- `score_components`
- `recommended_support_axes`
- `evidence_refs`
- `risk_notes`
- `evidence_summary`

Score components:

- `character_fit`
- `reviewed_evidence_depth`
- `positive_negative_contrast_quality`
- `package_role_completeness`
- `foundation_axis_fit`
- `identity_swallowing_risk`
- `fun_health_signal`
- `compression_risk`
- `support_axis_compatibility`
- `open_gap_penalty`

Higher values are better for fit/evidence/fun/support components. Higher values are
riskier for `identity_swallowing_risk`, `compression_risk`, and `open_gap_penalty`.
The `overall_score` subtracts those risk components by using `1 - risk`.

## Evidence Sources

The V1 implementation consumes:

- `tools/combat_analysis/design_engine/mechanism_axis_contracts.py`
- `docs/development/cardanalysis/STS1_CORE_MECHANISM_AXIS_MAP_V1.md`
- `tests/fixtures/combat_analysis/mechanism_axis_viability_v1/`
- `tests/fixtures/combat_analysis/deck_fun_benchmark_v1/`
- `docs/development/cardanalysis/CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`

The evidence refs in output preserve source paths and case refs so a reviewer can
inspect the underlying row, fixture, or taxonomy term.

## Entrypoints

Focused validation:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_search_v1.py tests/scripts/test_run_mechanism_axis_search.py -q
```

Generate the current Silent search bundle:

```powershell
python scripts/run_mechanism_axis_search.py --input tests/fixtures/combat_analysis/mechanism_axis_search_v1/silent_high_agency_visible_clock_v1.json --output-dir tmp/combat_analysis/mechanism_axis_search_current
```

Write a request template:

```powershell
python scripts/run_mechanism_axis_search.py --write-template tmp/combat_analysis/mechanism_axis_search_request_template.json
```

Write a constrained design brief from a search snapshot:

```powershell
python scripts/run_mechanism_axis_design_brief.py --input tmp/combat_analysis/mechanism_axis_search_current/silent_sts1_reviewed_axes_328508221e_mechanism_axis_search_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_design_brief_current
```

Write a role-level package proposal seed from the current design brief:

```powershell
python scripts/run_mechanism_axis_package_seed.py --input tmp/combat_analysis/mechanism_axis_design_brief_current/silent_sts1_reviewed_axes_328508221e_design_brief_mechanism_axis_design_brief_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_package_seed_current
```

Validate the generated seed as a `card_package_proposal_v1`:

```powershell
python scripts/validate_card_package_proposal.py --input tmp/combat_analysis/mechanism_axis_package_seed_current --json
```

Run the report-only chain exam:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_report_only_chain_v1.py -q
```

Focused validation for the brief consumer:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_design_brief_v1.py tests/scripts/test_run_mechanism_axis_design_brief.py -q
```

## Constrained Design Brief Consumer

`mechanism_axis_design_brief_v1` is the first downstream glue layer. It reads only a
`mechanism_axis_search_bundle_v1` snapshot and writes a short advisory brief.

It must preserve these assertions:

- `axis_ids_source = mechanism_axis_search_bundle_v1`
- `axis_ids_invented = false`
- `scores_modified = false`
- `formal_card_generated = false`
- `card_package_proposal_generated = false`
- `reviewed_evidence_claim_created = false`

The brief may summarize why the program-ranked axes are discussion candidates, but it
must copy axis IDs, scores, support axes, rejected-axis reasons, and evidence refs from
the source bundle. It is not a package proposal and must not introduce card names,
costs, numbers, or rules text.

## Role-Level Package Seed Consumer

`mechanism_axis_package_seed_v1` is the next downstream glue layer. It reads only a
`mechanism_axis_design_brief_v1` snapshot and writes a speculative
`card_package_proposal_v1` seed.

The seed must stay role-level:

- `source_type = generated_hypothesis`
- `evidence_tier = speculative`
- `review_status = hypothesis_draft`
- `authority_boundary = advisory_context_only`
- `forbidden_uses` includes `reviewed_evidence_claim`

It may create anchor/enabler/glue/payoff/fail-state/defense slot descriptions. It must
not create formal card names, costs, damage/block numbers, rules text, runtime card
data, reviewed evidence, hard gates, default synthesis, learned/reranker behavior, or
release authority.

The package seed chooses its primary and secondary axes from the source design brief
only. For the first Silent fixture, that produces `poison` as the primary axis and
`retain`, `shiv` as secondary axes.

## Report-Only Chain Exam

`test_mechanism_axis_report_only_chain_v1.py` exercises the full V1 chain in memory:

1. Build `mechanism_axis_search_bundle_v1` from the Silent request fixture.
2. Build `mechanism_axis_design_brief_v1` from the search payload.
3. Build `mechanism_axis_package_seed_v1` from the brief payload.
4. Normalize the seed as `card_package_proposal_v1`.

The exam asserts that search remains the score and axis authority, the brief copies
program output rather than inventing axes or scores, and the package seed remains a
generated-hypothesis role skeleton with no formal card fields or hard-gate/default
synthesis/learned authority.

## V1 Scope

V1 prioritizes STS1 reviewed axes. The first consumer fixture is Silent-oriented, but
the implementation enumerates from the full mechanism family contract and can score
other reviewed STS1 families.

The Silent fixture covers at least:

- `poison`
- `shiv`
- `discard_cycle`
- `draw_engine`
- `retain`
- `copy_exactness`
- `block_engine` adjacency

## Stop Lines

Pause and request human review if a follow-up would modify:

- runtime;
- formal card or enemy data;
- UI/save;
- capability graph registry;
- report-only registry;
- hard gates;
- default synthesis;
- learned or reranker behavior;
- mechanism viability scoring logic.

Also pause if a change would promote this output to reviewed evidence or release
authority.
