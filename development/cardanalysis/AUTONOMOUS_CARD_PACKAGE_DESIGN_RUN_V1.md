# Autonomous Card Package Design Run V1

## Purpose

`autonomous_card_package_design_run_v1` is a report-only record for the axis-first
card package design workflow.

It answers:

```text
Did this supplied complete-card draft actually follow the intended chain:
mechanism axis search -> constrained design brief -> package seed -> variant handoff
-> complete card draft -> attempt taxonomy -> package exam -> scorecard?
```

The important V1 behavior is provenance. The run does not create card text. It records
whether a generated or owner-supplied `complete_card_draft_v1` can be traced back to
the mechanism axes selected by the local search chain before it enters exam feedback.

## Workflow Position

```text
mechanism_axis_search_bundle_v1
  -> mechanism_axis_design_brief_v1
  -> mechanism_axis_package_seed_v1 / card_package_proposal_v1
  -> sts1_exam_target_v1
  -> card_package_variant_set_v1
  -> card_package_draft_handoff_v1
  -> supplied complete_card_draft_v1
  -> llm_complete_card_draft_attempt_v1
  -> exam_iteration_run_v1
  -> card_package_exam_v1
  -> card_design_scorecard_v1
  -> autonomous_card_package_design_run_v1
```

The source `complete_card_draft_v1` may be written by a human or by Codex in the
conversation, but this runtime surface only consumes that file. It does not call an
LLM API and does not generate draft text itself.

## Consistency Checks

V1 rejects the run if:

- the design brief axes do not match the search bundle's recommended axes;
- the package seed axes are not selected from the search bundle;
- the selected variant axes do not match the package seed;
- the draft package exam is not axis-aligned.

These checks are advisory provenance checks, not formal card legality gates.

## Boundary

This surface does not:

- write runtime card data;
- generate complete-card draft text at runtime;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- call an LLM API;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

`advisory_readout` is a design-feedback label only. Human review is still required
before any card or package can be promoted.

## Entrypoints

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_autonomous_card_package_design_run_v1.py -q
```

This surface is retained as a report-only library/fixture contract. Its former
standalone CLI wrapper is retired from default routes.

For current user-facing runs, use
`scripts/run_programmatic_complete_card_draft_generation.py`; that route writes
nested `autonomous_card_package_design_run_v1` artifacts when a complete-card
draft enters the axis-first exam chain. Use `scripts/run_mechanism_axis_package_seed.py`
to create the package seed from the current design brief before running the
generation route.

## Interpretation

A clean run means the existing supplied draft can be audited as axis-first and can be
compared through the existing exam and scorecard loop. It does not prove autonomous
card-design quality, balance, reviewed evidence status, or promotion readiness.

The former bounded draft-writing rehearsal side path is retired. Current draft
work should enter through the facade-backed generate/ingest, exam, review-pack,
feedback, and iterate routes, with this autonomous run kept as the retained
axis-first provenance record.
