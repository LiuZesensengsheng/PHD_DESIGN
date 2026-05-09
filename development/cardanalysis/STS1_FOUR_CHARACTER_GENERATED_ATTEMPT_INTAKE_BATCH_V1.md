# STS1 Four Character Generated Attempt Intake Batch V1

## Purpose

`sts1_four_character_generated_attempt_intake_batch_v1` is a report-only
orchestration surface for running the current generated-attempt feedback loop
across Silent, Ironclad, Defect, and Watcher from simulated
`llm_draft_prompt_application_v1` intake records.

It answers:

```text
Can all four STS1 character targets run the prompt-application intake path,
per-character generated-attempt batch run, and multi-character failure summary
without crossing advisory boundaries?
```

## Workflow Position

```text
sts1_exam_target_v1
  + card_package_variant_set_v1
  + four-character negative-control complete_card_draft_v1 drafts
  + healthy owner-filled draft fixtures copied into simulated generated repairs
  -> llm_draft_prompt_application_v1 per attempt
  -> exam_iteration_generated_attempt_batch_run_v1 per character
  -> exam_iteration_multi_character_batch_summary_v1
  -> sts1_four_character_generated_attempt_intake_batch_v1
```

This surface writes temporary simulated draft files under the requested output
directory. Those files are analysis fixtures only; they are not runtime card
data, formal cards, reviewed evidence, or a synthesis default.

## What It Writes

The CLI writes:

- `sts1_four_character_generated_attempt_intake_batch_v1_report.md`;
- `sts1_four_character_generated_attempt_intake_batch_v1_snapshot.json`;
- `sts1_four_character_generated_attempt_intake_batch_v1_manifest.json`;
- `characters/<character>/prompt_applications/attempt_###/` intake artifacts;
- `characters/<character>/batch_run/` per-character batch-run artifacts;
- `multi_character_summary/` summary artifacts;
- `generated_attempt_drafts/` temporary simulated draft files.

## Boundary

This surface is a simulation scaffold and feedback readout only.

It does not:

- call an LLM API;
- enable default synthesis;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable learned or reranker behavior.

Generated-attempt negative controls and simulated repair drafts remain
speculative fixtures. They must not be promoted without explicit human review.

## Entrypoints

```powershell
python scripts/run_sts1_four_character_generated_attempt_intake_batch.py --output-dir tmp/combat_analysis/sts1_four_character_generated_attempt_intake_batch_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_four_character_generated_attempt_intake_batch_v1.py tests/scripts/test_run_sts1_four_character_generated_attempt_intake_batch.py -q
```

## Interpretation

A clean run means the report-only loop can now exercise the intake-linked
generated-attempt batch path for all four STS1 characters and compare failure
movement across them. It still does not prove autonomous LLM generation quality,
balance, or card-design readiness.
