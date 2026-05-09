# External Draft Submission Readiness V1

`external_draft_submission_readiness_v1` is a report-only pre-intake check for a
supplied external or owner `complete_card_draft_v1` file.

It answers:

```text
Does this draft file and its external generation metadata match the previously
prepared external_draft_intake_packet_v1 closely enough to be recorded through
llm_draft_prompt_application_v1?
```

It is not a generation endpoint and it does not create the prompt-application
intake artifact.

## Workflow Position

```text
card_package_draft_handoff_v1
  + optional exam_iteration_prompt_patch_proposal_v1
  -> external_draft_intake_packet_v1
  -> external or owner-approved complete_card_draft_v1 file
  -> external_draft_submission_readiness_v1
  -> llm_draft_prompt_application_v1
```

## What It Checks

The readiness check compares:

- the `external_draft_intake_packet_v1` submission requirements;
- the supplied `complete_card_draft_v1` validation report;
- the supplied external generation metadata.

It verifies source shape, authority boundary, required slot coverage,
character/primary-axis match, required forbidden uses, and metadata boundary
flags.

## What It Writes

The CLI writes:

- `external_draft_submission_readiness_v1_report.md`
- `external_draft_submission_readiness_v1_snapshot.json`
- `external_draft_submission_readiness_v1_manifest.json`

The snapshot includes `ready_for_prompt_application_intake` and an advisory
next command. A `False` readiness result is still a normal report-only artifact:
it means the submitted draft or metadata should be revised before intake.

## Boundary

This readiness check does not:

- call an LLM API;
- generate complete card drafts;
- create `llm_draft_prompt_application_v1` intake artifacts;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default synthesis, learned behavior, or reranker behavior.

## Entrypoints

```powershell
python scripts/run_external_draft_submission_readiness.py --intake-packet tmp/combat_analysis/external_draft_intake_packet_current/external_draft_intake_packet_v1_snapshot.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --generation-metadata tmp/combat_analysis/external_draft_intake_packet_current/external_generation_metadata_template.json --output-dir tmp/combat_analysis/external_draft_submission_readiness_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_external_draft_submission_readiness_v1.py tests/scripts/test_run_external_draft_submission_readiness.py -q
```

## Interpretation

A ready result means the supplied draft is ready to be recorded as an external
prompt-application intake attempt. It does not prove design quality, reviewed
evidence status, balance, or autonomous LLM generation ability.
