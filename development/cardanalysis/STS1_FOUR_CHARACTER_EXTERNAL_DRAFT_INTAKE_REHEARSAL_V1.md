# STS1 Four Character External Draft Intake Rehearsal V1

## Purpose

`sts1_four_character_external_draft_intake_rehearsal_v1` is a report-only
four-role wrapper around `external_draft_intake_rehearsal_v1`.

It answers:

```text
Can Silent, Ironclad, Defect, and Watcher all run the external/owner-supplied
draft intake rehearsal with readiness checks, ready-only prompt-application
intake, rejected-attempt non-intake behavior, and optional batch handoff?
```

## Workflow Position

```text
sts1_exam_target_v1
  + card_package_variant_set_v1
  + complete_card_draft_v1 owner-filled fixtures
  + sts1_four_character_exam_v1 embedded axis/package inputs
  -> external_draft_intake_rehearsal_v1 per character
  -> sts1_four_character_external_draft_intake_rehearsal_v1
```

Each character receives three temporary rehearsal submissions:

- one owner-ready external-style draft copied from the healthy fixture;
- one intentionally rejected slot-mismatch draft;
- one simulated ready external-style draft.

The rejected submission must stop after
`external_draft_submission_readiness_v1`; only the two ready submissions may
create `llm_draft_prompt_application_v1` records and flow into
`exam_iteration_generated_attempt_batch_run_v1`.

## What It Writes

The CLI writes:

- `sts1_four_character_external_draft_intake_rehearsal_v1_report.md`;
- `sts1_four_character_external_draft_intake_rehearsal_v1_snapshot.json`;
- `sts1_four_character_external_draft_intake_rehearsal_v1_manifest.json`;
- `characters/<character>/` nested `external_draft_intake_rehearsal_v1`
  artifacts;
- `characters/<character>/readiness/attempt_###/` readiness artifacts for
  every submission;
- `characters/<character>/prompt_applications/attempt_###/` artifacts only for
  ready submissions;
- `characters/<character>/batch_run/` ready-intake batch artifacts;
- `external_draft_submissions/` temporary rehearsal draft and metadata inputs.

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

The temporary draft files are rehearsal inputs only. They are not runtime card
data, formal cards, reviewed evidence, or training promotion material.

## Entrypoints

```powershell
python scripts/run_sts1_four_character_external_draft_intake_rehearsal.py --output-dir tmp/combat_analysis/sts1_four_character_external_draft_intake_rehearsal_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_four_character_external_draft_intake_rehearsal_v1.py tests/scripts/test_run_sts1_four_character_external_draft_intake_rehearsal.py -q
```

## Interpretation

A clean run means the owner/external draft intake boundary can be rehearsed for
all four STS1 characters: bad submissions are rejected before intake, ready
submissions create report-only intake records, and ready intakes can enter the
generated-attempt batch feedback loop. It still does not prove autonomous LLM
generation quality, card balance, reviewed evidence status, or promotion
readiness.
