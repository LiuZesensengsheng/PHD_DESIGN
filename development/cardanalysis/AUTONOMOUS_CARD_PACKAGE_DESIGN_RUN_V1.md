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
python scripts/run_autonomous_card_package_design_run.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --design-brief tests/fixtures/combat_analysis/mechanism_axis_package_seed_v1/silent_axis_design_brief_snapshot_v1.json --package-seed <card_package_proposal_v1.json> --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/autonomous_card_package_design_run_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_autonomous_card_package_design_run_v1.py tests/scripts/test_run_autonomous_card_package_design_run.py -q
```

Use `scripts/run_mechanism_axis_package_seed.py` to create the package seed from the
current design brief before running the command.

## Interpretation

A clean run means the existing supplied draft can be audited as axis-first and can be
compared through the existing exam and scorecard loop. It does not prove autonomous
card-design quality, balance, reviewed evidence status, or promotion readiness.

The next capability gap is a bounded owner-approved draft-writing session that uses
the axis search and handoff artifacts as its prompt context, then submits the resulting
draft file back through this run.
