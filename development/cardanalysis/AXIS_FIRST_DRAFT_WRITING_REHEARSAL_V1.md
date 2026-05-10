# Axis-First Draft Writing Rehearsal V1

## Purpose

`axis_first_draft_writing_rehearsal_v1` is a report-only record for the first
bounded owner/Codex-supplied draft writing step in the axis-first card package
workflow.

It answers:

```text
Was this supplied complete-card draft written from the mechanism axis search,
design brief, package seed, variant set, and draft handoff context, and did it
flow back through the autonomous card package design exam chain?
```

The surface does not write card text. It records the axis-first writing context,
the supplied draft metadata, and the nested `autonomous_card_package_design_run_v1`
result.

## Workflow Position

```text
mechanism_axis_search_bundle_v1
  -> mechanism_axis_design_brief_v1
  -> mechanism_axis_package_seed_v1 / card_package_proposal_v1
  -> sts1_exam_target_v1
  -> card_package_variant_set_v1
  -> card_package_draft_handoff_v1
  -> owner/Codex-supplied complete_card_draft_v1
  -> autonomous_card_package_design_run_v1
  -> axis_first_draft_writing_rehearsal_v1
```

This is the first explicit bridge between the user's intended workflow and the
existing exam loop: draft writing remains outside runtime synthesis, but the
draft can no longer appear as an isolated file with no axis-first provenance.

## Inputs

The rehearsal consumes:

- `mechanism_axis_search_bundle_v1`;
- `mechanism_axis_design_brief_v1`;
- `card_package_proposal_v1` package seed;
- `sts1_exam_target_v1`;
- `card_package_variant_set_v1`;
- a selected `card_package_draft_handoff_v1`;
- a supplied `complete_card_draft_v1`;
- optional draft-writing metadata naming the owner/Codex writing session.

Draft-writing metadata may name `source_kind`, `writer_label`,
`writing_session_id`, and `attempt_label`. It may not claim runtime generation,
runtime card-data writes, promotion, hard gates, reviewed evidence, default
synthesis, default LLM generation, learned behavior, or reranker behavior.

## Outputs

The CLI writes:

- `axis_first_draft_writing_rehearsal_v1_report.md`
- `axis_first_draft_writing_rehearsal_v1_snapshot.json`
- `axis_first_draft_writing_rehearsal_v1_manifest.json`
- nested `autonomous_card_package_design_run/` artifacts.

The snapshot includes:

- source chain ids for search, brief, seed, target, variant, handoff, draft, and
  nested autonomous run;
- handoff prompt context and required slots used for drafting;
- draft-writing metadata;
- axis-chain consistency checks;
- package exam and scorecard summary from the nested autonomous run;
- report-only boundary assertions.

## Boundary

This surface does not:

- call an LLM API;
- generate complete-card draft text at runtime;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

`rehearsal_next_step` is advisory feedback only. Human review is still required
before any card or package can be promoted.

## Entrypoints

```powershell
python scripts/run_axis_first_draft_writing_rehearsal.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --design-brief tests/fixtures/combat_analysis/mechanism_axis_package_seed_v1/silent_axis_design_brief_snapshot_v1.json --package-seed <card_package_proposal_v1.json> --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --draft-writing-metadata <draft_writing_metadata.json> --output-dir tmp/combat_analysis/axis_first_draft_writing_rehearsal_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_axis_first_draft_writing_rehearsal_v1.py tests/scripts/test_run_axis_first_draft_writing_rehearsal.py -q
```

Use `scripts/run_mechanism_axis_package_seed.py` to create the package seed from
the current design brief before running the command.

## Interpretation

A clean rehearsal means the supplied draft was auditable as an axis-first attempt
and could enter the existing package exam and scorecard loop. It does not prove
autonomous card-design quality, reviewed evidence status, balance quality, or
promotion readiness.

The next capability gap is repeating this rehearsal across additional characters
or comparing multiple rehearsals with scorecard delta and failure movement.
