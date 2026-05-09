# STS1 Owner-Approved External Draft Batch Manifest V1

## Purpose

`sts1_owner_approved_external_draft_batch_manifest_v1` is a report-only
replacement surface for the fixture-backed four-character external draft intake
rehearsal.

It answers:

```text
Can Silent, Ironclad, Defect, and Watcher replace simulated rehearsal
submissions with owner-approved external complete_card_draft_v1 files while
preserving readiness checks, ready-only prompt-application intake, rejected
non-intake behavior, and optional generated-attempt batch feedback?
```

## Workflow Position

```text
owner-approved manifest
  + sts1_exam_target_v1
  + card_package_variant_set_v1
  + sts1_four_character_exam_v1 embedded axis/package inputs
  -> external_draft_intake_rehearsal_v1 per character
  -> sts1_owner_approved_external_draft_batch_manifest_v1
```

The manifest lists real supplied draft and metadata files per STS1 character.
Each submission must carry explicit owner approval metadata:

- `approval_status: owner_approved_for_report_only_intake`;
- `approval_scope: report_only_intake` or
  `owner_supplied_report_only_intake`;
- `approved_by`;
- all runtime-generation, promotion, hard-gate, reviewed-evidence, default
  synthesis, learned, and reranker flags set false.

Each generation metadata file must also use:

- `source_kind: external_or_owner_supplied_file`;
- `metadata_review_status: unreviewed_generation_metadata`;
- an explicit report-only `human_approval_scope`;
- all forbidden boundary flags set false.

## Behavior

- The surface loads the manifest and requires all four STS1 characters.
- It builds the per-character `card_package_draft_handoff_v1`.
- It runs `external_draft_submission_readiness_v1` before any intake.
- It creates `llm_draft_prompt_application_v1` only for ready submissions.
- It keeps rejected submissions as readiness-only artifacts.
- It hands two or more ready intakes per character to
  `exam_iteration_generated_attempt_batch_run_v1`.

## Boundary

This surface does not:

- call an LLM API;
- generate complete card text;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default synthesis;
- enable learned or reranker behavior.

Owner approval here means approval to enter the report-only intake and exam
feedback loop. It is not approval to promote cards, write runtime data, or claim
reviewed evidence.

## Entrypoints

```powershell
python scripts/run_sts1_owner_approved_external_draft_batch_manifest.py --write-template tmp/combat_analysis/sts1_owner_approved_external_draft_batch_manifest_template.json
python scripts/run_sts1_owner_approved_external_draft_batch_manifest.py --manifest <owner_approved_batch_manifest.json> --output-dir tmp/combat_analysis/sts1_owner_approved_external_draft_batch_manifest_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_owner_approved_external_draft_batch_manifest_v1.py tests/scripts/test_run_sts1_owner_approved_external_draft_batch_manifest.py -q
```

## Interpretation

A clean run means the four-character external draft intake path can now swap
fixture-backed rehearsal drafts for owner-approved supplied files. It still does
not prove autonomous LLM card-design quality, balance, reviewed evidence status,
or promotion readiness.
