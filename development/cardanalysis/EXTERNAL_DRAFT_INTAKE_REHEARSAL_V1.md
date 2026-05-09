# External Draft Intake Rehearsal V1

`external_draft_intake_rehearsal_v1` is a report-only orchestration surface for
owner-approved external `complete_card_draft_v1` submissions.

It answers:

```text
If one or more external draft files are supplied, which are ready for
prompt-application intake, which should be rejected, and can the ready ones be
fed into the generated-attempt batch loop without calling an LLM?
```

It is not a generation endpoint.

## Workflow Position

```text
card_package_draft_handoff_v1
  + optional exam_iteration_prompt_patch_proposal_v1
  -> external_draft_intake_packet_v1
  -> external_draft_submission_readiness_v1 per supplied draft
  -> llm_draft_prompt_application_v1 for ready drafts only
  -> optional exam_iteration_generated_attempt_batch_run_v1
  -> external_draft_intake_rehearsal_v1
```

## What It Does

The rehearsal:

- builds one `external_draft_intake_packet_v1` from the selected draft handoff;
- checks each supplied draft and metadata file with
  `external_draft_submission_readiness_v1`;
- creates `llm_draft_prompt_application_v1` artifacts only for ready attempts;
- records rejected attempts and their readiness issues without creating intake
  artifacts for them;
- optionally runs `exam_iteration_generated_attempt_batch_run_v1` when at least
  two ready intakes and package-exam inputs are supplied.

## What It Writes

The CLI writes:

- `external_draft_intake_rehearsal_v1_report.md`
- `external_draft_intake_rehearsal_v1_snapshot.json`
- `external_draft_intake_rehearsal_v1_manifest.json`
- nested `packet/` artifacts;
- nested `readiness/attempt_###/` artifacts for every submitted draft;
- nested `prompt_applications/attempt_###/` artifacts only for ready drafts;
- optional nested `batch_run/` artifacts.

## Boundary

This rehearsal does not:

- call an LLM API;
- generate complete card drafts;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- change default synthesis behavior;
- enable learned or reranker behavior.

Rejected attempts remain advisory readiness reports. Ready attempts are intake
records only and still require human review before any content promotion.

## Entrypoints

```powershell
python scripts/run_external_draft_intake_rehearsal.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --generation-metadata <external_generation_metadata.json> --output-dir tmp/combat_analysis/external_draft_intake_rehearsal_current
python scripts/run_external_draft_intake_rehearsal.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft <attempt_001_complete_card_draft_v1.json> --generation-metadata <attempt_001_metadata.json> --draft <attempt_002_complete_card_draft_v1.json> --generation-metadata <attempt_002_metadata.json> --axis-search <mechanism_axis_search_bundle_v1.json> --package-seed <card_package_proposal_v1.json> --output-dir tmp/combat_analysis/external_draft_intake_rehearsal_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_external_draft_intake_rehearsal_v1.py tests/scripts/test_run_external_draft_intake_rehearsal.py -q
```

## Interpretation

A rehearsal with a batch run proves that approved external draft files can flow
through the report-only intake and exam feedback loop. It does not prove
autonomous LLM generation quality, balance, reviewed evidence status, or runtime
promotion readiness.
