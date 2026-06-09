# Cardanalysis Canonical Route Map V1

## Purpose

Keep the slimmed `cardanalysis` surface AI-readable after route consolidation.

This map names the current user-facing routes, embedded-only evaluators, and
retired wrappers. `cardanalysis_tool_facade_v1` is the top-level Codex-facing
route map over these routes; it is a routing layer, not a new scoring owner.

## Boundary

All routes in this map keep the existing `report_only` /
`advisory_context_only` boundary unless their underlying schema validator already
owns stricter contract validation.

This map does not:

- write runtime card data,
- promote generated drafts into formal cards,
- create hard gates,
- change score weights or default synthesis,
- enable learned/reranker behavior,
- upgrade speculative/source-mined/human-curated material into reviewed evidence.

## Canonical User-Facing Routes

| Area | Canonical Route | Use For |
| --- | --- | --- |
| Tool facade | `scripts/run_cardanalysis_tool_facade.py` | Query the five Codex-facing actions: generate/ingest, exam, Chinese review-pack, feedback, and iterate. |
| Complete-card draft schema | `scripts/validate_complete_card_draft.py` | Validate or template `complete_card_draft_v1`; optionally export temporary owner input for health review. |
| Programmatic draft generation | `scripts/run_programmatic_complete_card_draft_generation.py` | Generate or ingest complete-card draft attempts through an explicit provider. |
| Composition-guided 12-card package | `scripts/run_programmatic_complete_card_draft_composition_guided_medium_package.py` | Build single or batch Chinese-readable 12-card review packages. |
| 30-card candidate pool / strong builds | `scripts/run_programmatic_complete_card_draft_strong_build_pool.py` | Build and inspect the 30-card candidate pool and strong-build lines. |
| Strong-build playout | `scripts/run_programmatic_complete_card_draft_strong_build_playout.py` | Run report-only playout probe, deterministic observation, or observation readout stages. |
| Engineering data-method probe | `scripts/run_engineering_data_method_cardanalysis_probe.py` | Run the report-only Engineering data-method axis probe through the retained cardanalysis evaluator. |
| Advisory complete-card exams | `scripts/run_programmatic_complete_card_draft_advisory_exam.py` | Run retained value/diversity/similarity/composition/generalization/provider comparison readouts. |
| STS1 reference readouts | `scripts/run_programmatic_complete_card_draft_sts1_reference_readout.py` | Run retained STS1 case-alignment, role-map, or strong-deck-principle readouts. |
| Multi-character classic skeleton exam | `scripts/run_programmatic_complete_card_draft_multi_character_classic_build_skeleton_exam.py` | Compare candidate pools or draft packages against STS1 classic build skeletons. |
| Autonomous exploration review packet | `scripts/run_programmatic_complete_card_draft_autonomous_exploration.py` | Produce report-only exploration/review packets; not promotion authority. |
| Engineering cardpool review packet | `scripts/run_engineering_cardpool_review_pack.py` | Produce the report-only Chinese Engineering cardpool review packet and snapshot for human review. |
| Cardanalysis inventory reports | `scripts/run_cardanalysis_report.py` | Run case-progress, coverage-gap, evidence-quality, or feature-projection reports. |
| Cardanalysis slimming inventory | `scripts/run_cardanalysis_capability_surface_inventory.py` | Inspect current broad/narrow surface size and archive-candidate signals. |

## Embedded-Only Or Library-Level Surfaces

These surfaces remain active but should not grow new standalone wrapper scripts
without a route-map update and focused tests:

- `programmatic_complete_card_draft_energy_gain_safety_exam.py`
- `programmatic_complete_card_draft_poison_value_calibration_exam.py`
- `programmatic_complete_card_draft_medium_package_expansion.py`
- `programmatic_complete_card_draft_composition_guided_medium_package_batch.py`
- `programmatic_complete_card_draft_nested_exam_artifacts.py`

The former mechanism-axis evaluation handoff, owner-report/evidence, and
card-package-health preparation chain is retired from active code. Current
mechanism-axis input preparation stops at search, design brief, and package
seed, then routes card work through the facade-backed generate/ingest, exam,
review-pack, feedback, and iterate actions.

Mechanism-axis search, design-brief, and package-seed scripts are supporting
input-preparation routes for `cardanalysis_tool_facade_v1`'s
`generate_or_ingest` action. They are not separate top-level cardanalysis
workflows in this route map.

`scripts/run_llm_draft_prompt_application.py` is also a supporting
`generate_or_ingest` route. It records prompt-patch context and owner/model
supplied external draft intake without calling an LLM or promoting cards.

## Retired Standalone Routes

The retired route list is maintained in
`tools/combat_analysis/docs/CARDANALYSIS_SLIMMING_ARCHIVE_CANDIDATES_V1.md`.
Those names are historical context only. They should not reappear under
`scripts/` unless a new accepted decision reverses the consolidation.

## Validation

Route-map guard:

```powershell
python -m pytest tests/toolkit/combat_analysis/test_cardanalysis_canonical_route_map_v1.py -q
```

Facade guard:

```powershell
python -m pytest tests/toolkit/combat_analysis/test_cardanalysis_tool_facade_v1.py tests/scripts/test_run_cardanalysis_tool_facade.py -q
```

General graph guard:

```powershell
python scripts/validate_capability_graph.py --json
```
