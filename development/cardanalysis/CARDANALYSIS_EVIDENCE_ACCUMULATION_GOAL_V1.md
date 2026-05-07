# Cardanalysis Evidence Accumulation Goal V1

## Purpose

This goal defines a long-running, low-authority evidence accumulation lane for
`cardanalysis`.

The lane exists to make future design review better informed. It does not let
Codex define official card designs, decide design direction, promote reviewed
evidence, modify runtime, or change hard-gate behavior.

## Goal

Grow the normalized `cardanalysis_case_input_v1` evidence library through small,
source-aware batches so report-only tools can inspect more mechanism, package,
enemy-pressure, and campaign-phase examples.

Target scale:

- `500` total normalized cases for the first useful plateau.
- `1000-1200` cases for stable medium-term coverage.
- `2000+` cases only after source and review workflows stay healthy.

The current priority is coverage-guided case accumulation, not new evaluator
logic.

## Priority Lanes

1. Mechanism failure modes:
   loop collapse, over-tutor, draw heat, status pollution, temporary-generation
   burden, hidden tracking, and no-value fail states.
2. Card-package health and collapse:
   enabler, payoff, glue, fail-state value, counterplay, density, and support
   ratios.
3. Enemy pressure cases:
   frontload defense checks, status pressure, energy tax, draw disruption,
   summon pressure, scaling races, boss phase shifts, and anti-infinite soft
   pressure.
4. Campaign phase cases:
   starter, build, pivot, mature, late, and recovery-pressure windows.
5. Source followups:
   convert generated or source-mined followups into human-curated review-note
   cases without reviewed promotion.

## Batch Rules

Each long-running batch should stay small:

- add `10-20` cases at most;
- target one queue family or a tight adjacent pair;
- prefer a new small JSON shard over editing a large fixture file;
- update only focused docs/tests for the touched fixture family;
- rerun coverage after the batch lands.

## Source Tiers

`reviewed_fixture / reviewed / accepted`:

- only after explicit human review;
- never promoted automatically by Codex.

`playtest_observation`:

- internal run, test, or replay observation;
- must still preserve uncertainty if not human-reviewed.

`source_mined_reference`:

- external wiki, database, source repository, public run log, guide, or forum;
- must include `source_url` when available;
- must include a retrieval or provenance marker in context or `known_limits`;
- must forbid `reviewed_evidence_claim`.

`design_note / human_curated / review_needed`:

- Codex or human synthesis from a source or queue target;
- may organize observations, but cannot claim reviewed authority.

`generated_hypothesis / speculative`:

- candidate line only;
- cannot become reviewed or default synthesis input without explicit review.

## Network Collection Rules

Network sources are allowed for evidence accumulation, but they are not project
truth by themselves.

Preferred order:

1. mechanical fact sources such as game wikis, card text pages, patch notes, or
   open data files;
2. run logs or public datasets when provenance is clear;
3. high-quality player guides or discussions as interpretation only;
4. generated hypotheses as leads only.

External sources must preserve:

- `source_url`;
- `source_type`;
- `evidence_tier`;
- `review_status`;
- a short statement of what was observed;
- `known_limits` explaining review and source risk.

Do not copy long passages from sources into fixtures. Summarize the observation
in project vocabulary and cite the source URL.

## Required Authority Boundary

Every case produced under this goal must keep:

```text
authority.authority_boundary = advisory_context_only
```

Forbidden uses should include the relevant subset of:

- `hard_gate_promotion`
- `legality_decision`
- `default_synthesis_path`
- `reviewed_evidence_claim` for non-reviewed cases
- `runtime_card_authority`
- `runtime_campaign_authority`
- `monster_stat_tuning_authority`

## Validation Loop

For each batch, run:

```powershell
python scripts/validate_cardanalysis_case_input.py --input <touched-fixture-dir>
py -3.11 -m pytest <focused-fixture-test> -q
python scripts/run_cardanalysis_coverage_gap_report.py --input tmp/combat_analysis/coverage_gap_current_template.json --output-dir tmp/combat_analysis/coverage_gap_current
python scripts/run_coverage_guided_case_queue.py --input tmp/combat_analysis/coverage_gap_current --output-dir tmp/combat_analysis/case_queue_current
python scripts/validate_architecture.py
python scripts/check_text_encoding.py
python scripts/validate_capability_graph.py
git diff --check
```

Use the exact focused test for the fixture family being modified.

## Stop Lines

This goal must not:

- define official cards;
- modify runtime;
- modify formal card data;
- modify formal enemy data;
- modify UI or save structure;
- modify `capability_graph_registry.py` without a real implemented consumer;
- modify `report_only_surface_registry.py`;
- promote cases to reviewed evidence;
- introduce hard gates;
- enable default synthesis, learned behavior, or reranker defaults;
- treat external source-mined material as project-reviewed truth.

