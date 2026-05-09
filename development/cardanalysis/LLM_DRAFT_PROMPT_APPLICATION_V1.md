# LLM Draft Prompt Application V1

`llm_draft_prompt_application_v1` is a report-only intake surface for the STS1
card draft loop.

It records:

- the selected `card_package_draft_handoff_v1` prompt context;
- optional `exam_iteration_prompt_patch_proposal_v1` advice applied before the
  next attempt;
- external generation metadata supplied by the owner or an approved outer
  process;
- one externally supplied `complete_card_draft_v1` file, validated through
  `llm_complete_card_draft_attempt_v1`.

It does not call an LLM API, generate complete card text, write runtime card
data, promote formal cards, create hard gates, claim reviewed evidence, or
enable default learned/reranker behavior.

## Chain Position

```text
card_package_draft_handoff_v1
  + optional exam_iteration_prompt_patch_proposal_v1
  + external complete_card_draft_v1 file
  -> llm_draft_prompt_application_v1
  -> llm_complete_card_draft_attempt_v1
  -> exam_iteration_generated_attempt_batch_run_v1 or exam_iteration_run_v1
```

The surface is intentionally an audit packet, not a synthesis endpoint. It makes
future real LLM attempts reversible and inspectable before any downstream exam
comparison.

## Artifacts

The CLI writes:

- `llm_draft_prompt_application_v1_report.md`
- `llm_draft_prompt_application_v1_snapshot.json`
- `llm_draft_prompt_application_v1_manifest.json`
- nested `handoff/` artifacts for the base draft handoff;
- nested `attempt/` artifacts for the supplied complete-card draft attempt.

## Boundary Assertions

Snapshots and manifests explicitly record:

- `llm_api_called=False`
- `complete_card_draft_generated=False`
- `complete_card_draft_generated_by_runtime=False`
- `formal_cards_promoted=False`
- `runtime_card_definition_created=False`
- `reviewed_evidence_claim_created=False`
- `hard_gate_created=False`
- `default_synthesis_changed=False`
- `learned_or_reranker_enabled=False`

Generation metadata may name an external provider, model, prompt id, and attempt
label, but it may not claim runtime generation, promotion, reviewed evidence, or
default synthesis changes.

## Commands

```powershell
python scripts/run_llm_draft_prompt_application.py --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --prompt-patch <exam_iteration_prompt_patch_proposal_v1_snapshot.json> --generation-metadata <external_generation_metadata.json> --output-dir tmp/combat_analysis/llm_draft_prompt_application_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_llm_draft_prompt_application_v1.py tests/scripts/test_run_llm_draft_prompt_application.py -q
```

## Next Use

Use this surface before running a bounded generated-attempt batch when an owner or
approved external process has produced one or more draft files. It keeps prompt
patch advice and draft intake evidence together without making autonomous
generation claims.
