# External Draft Intake Packet V1

## Purpose

`external_draft_intake_packet_v1` is a report-only pre-intake packet for an
owner-approved external `complete_card_draft_v1` submission.

It answers:

```text
If a human approves one external/LLM draft attempt later, what exactly should
come back, how should it be labeled, and which exam commands should process it?
```

It is not a generation endpoint.

## Workflow Position

```text
card_package_draft_handoff_v1
  + optional exam_iteration_prompt_patch_proposal_v1
  -> external_draft_intake_packet_v1
  -> external or owner-approved complete_card_draft_v1 file
  -> llm_draft_prompt_application_v1
  -> exam_iteration_generated_attempt_batch_run_v1
```

## What It Writes

The CLI writes:

- `external_draft_intake_packet_v1_report.md`
- `external_draft_intake_packet_v1_snapshot.json`
- `external_draft_intake_packet_v1_manifest.json`
- `external_generation_metadata_template.json`
- nested `handoff/` artifacts for the base `card_package_draft_handoff_v1`

The packet records required slots, allowed draft source shapes, authority
metadata, prompt-patch lanes, and follow-up intake commands. It does not include
or produce card text.

## Boundary

This packet does not:

- call an LLM API;
- generate complete card drafts;
- collect an external draft file;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable learned or reranker behavior.

The metadata template explicitly sets runtime-generation and promotion flags to
`False`. Any later draft must still pass `complete_card_draft_v1` validation and
enter through `llm_draft_prompt_application_v1`.

## Entrypoints

```powershell
python scripts/run_external_draft_intake_packet.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --output-dir tmp/combat_analysis/external_draft_intake_packet_current
python scripts/run_external_draft_intake_packet.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --prompt-patch <exam_iteration_prompt_patch_proposal_v1_snapshot.json> --packet-label attempt_002_external_repair --output-dir tmp/combat_analysis/external_draft_intake_packet_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_external_draft_intake_packet_v1.py tests/scripts/test_run_external_draft_intake_packet.py -q
```

## Interpretation

A clean packet means the system has prepared a safe intake lane for a future
human-approved external draft. It does not prove autonomous generation quality
or authorize the runtime to generate cards.
