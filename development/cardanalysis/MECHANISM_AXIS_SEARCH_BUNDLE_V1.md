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

Write an evaluation-autonomous-design handoff input from the package seed:

```powershell
python scripts/run_mechanism_axis_evaluation_handoff.py --input tmp/combat_analysis/mechanism_axis_package_seed_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1.json --output-dir tmp/combat_analysis/mechanism_axis_evaluation_handoff_current
```

Run the existing evaluation autonomous design model from that handoff:

```powershell
python scripts/run_evaluation_autonomous_design_model.py --input tmp/combat_analysis/mechanism_axis_evaluation_handoff_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff.json --output-dir tmp/combat_analysis/evaluation_autonomous_design_from_axis_handoff_current
```

Write a report-only owner-report request packet from the handoff:

```powershell
python scripts/run_mechanism_axis_owner_report_requests.py --input tmp/combat_analysis/mechanism_axis_evaluation_handoff_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff.json --output-dir tmp/combat_analysis/mechanism_axis_owner_report_requests_current
```

Write a report-only owner-report input readiness plan from the request packet:

```powershell
python scripts/run_mechanism_axis_owner_report_input_plan.py --input tmp/combat_analysis/mechanism_axis_owner_report_requests_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_report_requests_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_report_input_plan_current
```

Check whether the current package seed may enter the card-package generation exam:

```powershell
python scripts/run_mechanism_axis_generation_exam_readiness.py --input tmp/combat_analysis/mechanism_axis_owner_report_input_plan_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_report_requests_input_plan_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_generation_exam_readiness_current
```

Write a report-only owner evidence queue from the readiness blockers:

```powershell
python scripts/run_mechanism_axis_owner_evidence_queue.py --input tmp/combat_analysis/mechanism_axis_generation_exam_readiness_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_generation_exam_readiness_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_evidence_queue_current
```

Write empty owner evidence intake templates from the current owner evidence queue:

```powershell
python scripts/run_mechanism_axis_owner_evidence_intake_packet.py --input tmp/combat_analysis/mechanism_axis_owner_evidence_queue_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_evidence_queue_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_owner_evidence_intake_packet_current
```

Write a report-only card package health owner input scaffold from the current package
seed and intake packet:

```powershell
python scripts/run_mechanism_axis_card_package_health_scaffold.py --package-seed tmp/combat_analysis/mechanism_axis_package_seed_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1.json --intake-packet tmp/combat_analysis/mechanism_axis_owner_evidence_intake_packet_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_evaluation_handoff_owner_evidence_intake_packet_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current
```

Check whether that scaffold has enough owner-filled material for a later input-writing
step:

```powershell
python scripts/run_mechanism_axis_card_package_health_readiness.py --input tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current/silent_sts1_reviewed_axes_328508221e_design_brief_package_seed_v1_card_package_health_owner_input_scaffold_snapshot.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_readiness_current
```

Write a temporary `card_package_health_v1` input from a fully owner-filled scaffold:

```powershell
python scripts/run_mechanism_axis_card_package_health_input_writer.py --input tmp/combat_analysis/mechanism_axis_card_package_health_scaffold_current/<filled_scaffold_snapshot>.json --output-dir tmp/combat_analysis/mechanism_axis_card_package_health_input_writer_current
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

## Evaluation Handoff Consumer

`mechanism_axis_evaluation_handoff_v1` reads a generated-hypothesis
`card_package_proposal_v1` seed and writes an
`evaluation_autonomous_design_model_v1` input seed.

It is a bridge, not a new evaluator. It may:

- map role-level package slots into the evaluator's package skeleton fields;
- carry primary/secondary mechanism axes into `mechanism_candidate`;
- request the canonical missing owner reports:
  `mechanism_axis_discovery_summary`, `mechanism_fun_health_summary`,
  `card_package_health_summary`, `deck_compression_summary`, and
  `design_iteration_summary`;
- preserve a `mechanism_axis_summary` optional context section.

It must not generate or score owner reports, formal cards, runtime card data, hard
gates, default synthesis, learned/reranker behavior, or reviewed-evidence claims.
The existing `evaluation_autonomous_design_model_v1` remains the downstream
orchestrator and still cannot promote beyond human-review wording.

## Owner Report Request Packet

`mechanism_axis_owner_report_requests_v1` reads an
`evaluation_autonomous_design_model_v1` handoff input and emits a report-only request
packet for missing canonical owner reports.

It may list requests for:

- `mechanism_axis_discovery_summary`
- `mechanism_fun_health_summary`
- `card_package_health_summary`
- `deck_compression_summary`
- `design_iteration_summary`

Each request item names the canonical owner surface, CLI script, minimum inputs, input
gap notes, source axes, role-level package skeleton roles, and forbidden actions.

It must not generate owner reports, score owner reports, create formal cards, create
runtime data, claim reviewed evidence, create hard gates, change default synthesis, or
enable learned/reranker behavior. Its purpose is routing and missing-input clarity
before the card-package-generation exam, not evaluation.

## Owner Report Input Plan

`mechanism_axis_owner_report_input_plan_v1` reads a
`mechanism_axis_owner_report_requests_v1` snapshot and emits a report-only readiness
plan for the requested owner-report inputs.

It may:

- name fields that can be safely prefilled from the handoff, such as source axes,
  mechanism candidate refs, and role-level package skeleton roles;
- name blocked inputs that still require owner or human-supplied review material;
- mark whether the owner CLI can safely run now.

It must not write owner input files, run owner reports, score owner reports, invent
deck-case refs, invent card-like package slots, claim reviewed evidence, create formal
cards, change runtime data, create hard gates, change default synthesis, or enable
learned/reranker behavior.

For the first Silent package seed, every canonical owner report remains blocked on
missing owner-specific inputs. That is intentional: the plan is a readiness map, not an
evidence generator.

## Generation Exam Readiness

`mechanism_axis_generation_exam_readiness_v1` reads a
`mechanism_axis_owner_report_input_plan_v1` snapshot and answers whether the current
role-level package seed may proceed to a card-package generation exam.

It may:

- summarize each canonical owner report's input/report status;
- produce blockers for missing owner inputs or missing owner report outputs;
- name the next safe step before any generation exam starts.

It must not start the generation exam, generate formal cards, write runtime data, run
owner reports, score owner reports, claim reviewed evidence, create hard gates, change
default synthesis, or enable learned/reranker behavior.

For the first Silent package seed, readiness is
`blocked_on_owner_report_inputs`: no owner report input is ready and no canonical owner
report output is present.

## Owner Evidence Queue

`mechanism_axis_owner_evidence_queue_v1` reads a
`mechanism_axis_generation_exam_readiness_v1` snapshot and turns readiness blockers
into explicit owner evidence requests.

It may:

- list required evidence material for each blocked canonical owner report;
- name acceptable source types, such as reviewed fixtures or human-reviewed design
  notes;
- distinguish owner input gaps from owner output gaps.
- rank owner input gaps by how directly they unblock a reviewable card-package
  generation exam.

It must not generate evidence, write owner input files, run owner reports, score owner
reports, claim reviewed evidence, create formal cards, create runtime data, create hard
gates, change default synthesis, or enable learned/reranker behavior.

For the first Silent package seed, the queue contains input/output gaps for mechanism
discovery, fun health, package health, deck compression, and design iteration.

The V1 `design_unlock_plan` treats the highest-value parallel evidence lanes as:

1. `card_package_health_summary`: card-like slots and package coherence.
2. `mechanism_axis_discovery_summary`: grounded mechanism loop and foundation-axis
   dependencies.
3. `mechanism_fun_health_summary`: fun-health and fatigue signals.
4. `deck_compression_summary`: deck context and setup-tax pressure.
5. `design_iteration_summary`: post-owner synthesis review after upstream owner
   summaries exist.

These ranks are planning metadata only. They do not generate evidence, write owner
inputs, promote reviewed evidence, or start the generation exam.

## Owner Evidence Intake Packet

`mechanism_axis_owner_evidence_intake_packet_v1` reads a
`mechanism_axis_owner_evidence_queue_v1` snapshot and emits empty intake templates for
human or owner-supplied evidence.

It may:

- carry queue item IDs, owner surfaces, required material, acceptable sources, and
  blocker detail into intake items;
- preserve the owner evidence queue's design-unlock ranks and parallel-agent lanes so
  reviewers know which intake templates most directly unblock the card-package
  generation exam;
- create empty fields for reviewer identity, source refs, evidence notes, source tier,
  review status, and required material values;
- attach an acceptance checklist that asks for traceable source material, tier-aware
  wording, and no score or axis override.

It must not fill evidence fields, write owner input files, run owner reports, score
owner reports, claim reviewed evidence, create formal cards, create runtime data,
create hard gates, change default synthesis, or enable learned/reranker behavior.

For the first Silent package seed, the intake packet contains ten empty templates: one
input-gap and one output-gap template for each canonical owner report section.

The V1 `intake_filling_plan` keeps `card_package_health_summary` first, followed by
mechanism discovery, fun health, deck compression, and then design iteration. It is
still a blank intake packet: all evidence fields remain empty until an owner or human
reviewer supplies real traceable material.

## Card Package Health Input Scaffold

`mechanism_axis_card_package_health_scaffold_v1` reads a generated-hypothesis package
seed and the empty owner evidence intake packet, then writes a blank owner input
scaffold for `card_package_health_v1`.

It may:

- copy source axes and role-level package slots from the package seed;
- copy the `card_package_health_summary` owner-input required material from the intake
  packet;
- provide role/slot/tag hints that an owner can use while filling real card-like
  material.

It must not fill evidence fields, write a runnable `card_package_health_v1` fixture,
run the card package health CLI, generate formal cards, create runtime card data,
claim reviewed evidence, create hard gates, change default synthesis, or enable
learned/reranker behavior.

For the first Silent package seed, the scaffold contains five role-level slot
templates copied from the package seed, but every owner fill field remains empty and
`ready_to_run_card_package_health_cli` remains false.

## Card Package Health Scaffold Readiness

`mechanism_axis_card_package_health_readiness_v1` reads a
`mechanism_axis_card_package_health_scaffold_v1` snapshot and reports whether owner or
human-filled fields are complete enough for a later input-writing step.

It may:

- list missing owner fill fields per role-level slot template;
- list missing owner evidence material such as `card_like_candidate_slots`,
  `role_tags`, `package_tags`, `setup_tax_notes`, expected label, and review notes;
- mark `ready_to_write_card_package_health_input` true only after all slot fields and
  owner material values are present.

It must not write a runnable `card_package_health_v1` input, run the card package
health CLI, generate formal cards, create runtime card data, claim reviewed evidence,
create hard gates, change default synthesis, or enable learned/reranker behavior.

For the first Silent package seed, the empty scaffold is
`blocked_on_card_like_slot_fields`; it has five slot templates, zero ready slots, and
six missing owner material groups.

## Card Package Health Input Writer

`mechanism_axis_card_package_health_input_writer_v1` reads a fully owner-filled
`mechanism_axis_card_package_health_scaffold_v1` snapshot and writes a temporary
`card_package_health_v1` input JSON.

It may:

- require the same readiness calculation used by
  `mechanism_axis_card_package_health_readiness_v1`;
- map owner-filled card-like slot labels, role tags, package tags, slot tags, setup
  tax, and exactness dependency into the existing `card_package_health_v1` case
  contract;
- write a temporary input under `tmp/` for a later explicit owner-report run.

It must not write an official reviewed fixture, run the card package health CLI,
generate formal cards, create runtime card data, claim reviewed evidence, create hard
gates, change default synthesis, or enable learned/reranker behavior.

The empty Silent scaffold is rejected with `blocked_on_card_like_slot_fields`. A filled
scaffold can write a valid `card_package_health_v1` input, but that input remains
owner-supplied draft material until human review promotes it through the normal
evidence process.

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
