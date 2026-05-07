# Coverage Guided Case Queue V1

## Purpose

Define a thin report-only planning artifact that converts a
`cardanalysis_coverage_gap_report_v1` snapshot into the next bounded
case-writing task queue.

The queue generator does not write new cases, change evaluators, generate
cards, tune runtime, or promote evidence. It only answers:

```text
Given current coverage gaps, what is the next small batch of case-writing work?
```

## Scope Boundary

In scope:

- reading a coverage-gap snapshot JSON;
- reading a coverage-gap manifest JSON that points to a snapshot;
- reading a coverage-gap output directory containing `manifest.json` or
  `snapshot.json`;
- producing a deterministic bounded queue of next case-writing tasks;
- preserving report-only authority boundaries.

Out of scope:

- modifying `coverage_gap_report.py`;
- modifying `case_input_contract.py`;
- modifying `feature_projection.py`;
- modifying capability graph or report-only registry ownership;
- writing new normalized cases;
- changing any evaluator, benchmark, synthesis, hard gate, learned, or reranker
  path.

## Inputs

The CLI supports:

- `--input <coverage-gap-snapshot.json>`
- `--input <coverage-gap-manifest.json>`
- `--input <coverage-gap-output-dir>`
- `--write-template <path>`

The input snapshot must keep:

- `schema_version = cardanalysis_coverage_gap_report_v1`
- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `hard_gate_impact = none`

If those boundaries drift, the queue generator should fail rather than silently
planning from a stronger authority surface.

## Outputs

The CLI writes:

- `case_queue_report.md`
- `snapshot.json`
- `manifest.json`

The queue snapshot keeps:

```text
schema_version = coverage_guided_case_queue_v1
evaluation_mode = report_only
authority_boundary = advisory_context_only
hard_gate_impact = none
```

Required payload sections:

- `source_coverage_gap_report_ref`
- `queue_items`
- `blocked_items`
- `batch_summary`
- `boundary_assertions`

## Queue Item Semantics

Each queue item is a bounded handoff for a future case-writing agent. It should
point to:

- one gap target,
- a recommended case count,
- a suggested source tier,
- a suggested output fixture path,
- explicit allowed and forbidden scope,
- concrete acceptance checks,
- a prompt seed that keeps the work case-library-only.

Queue items are planning seeds, not canonical product decisions.

## Gap Types

V1 emits queue items for:

- `basic_axis`
- `mechanism_axis`
- `enemy_archetype`
- `campaign_phase`
- `source_followup`
- `allowed_consumer`

`source_followup` items are review or human-curation tasks. They must not
promote source-mined or generated material directly to reviewed evidence.

## Sorting Rules

The queue is deterministic and intentionally bounded.

Primary ordering:

1. `missing` before `advisory_only`, then `thin_reviewed`
2. `basic_axis` and `mechanism_axis` before `campaign_phase`
3. `high` priority before `medium`, then `low`
4. stable lexical tie-break on target id

Special rule:

- if an enemy archetype gap includes `boss_phase_shift` and it is missing or
  advisory-only, keep it `high` or `medium`, but still case-library-only and
  never a monster-stat task

To avoid task explosion, V1 emits at most `10` queue items and pushes overflow
into `blocked_items` with a deferred reason.

## Blocked Items

`blocked_items` make unsafe or deferred planning explicit.

Current blocked categories:

- direct promotion of source-mined or generated follow-ups to reviewed evidence
- overflow tasks deferred because the queue cap was reached

This keeps queue output honest about what the next agent may and may not do.

## Boundary Assertions

The queue generator hard-codes these assertions:

- report-only only
- advisory-context-only only
- no case writing performed by this tool
- no evaluator changes
- no runtime changes
- no hard-gate or default-synthesis changes
- no graph or report-only registry ownership changes

## Suggested Workflow

1. Run the coverage-gap scanner.
2. Feed its snapshot, manifest, or output directory into this queue generator.
3. Give one queue item or one batch of adjacent queue items to a long-running
   case-writing agent.
4. Have that agent produce or extend normalized case fixtures, not evaluator
   code.
5. Re-run coverage gap after the new cases land.

## Entrypoints

```bash
python scripts/run_coverage_guided_case_queue.py --write-template <path>
python scripts/run_coverage_guided_case_queue.py --input <coverage-gap-snapshot-or-manifest-or-output-dir> --output-dir <dir>
py -3.11 -m pytest tests/toolkit/combat_analysis/test_coverage_guided_case_queue_v1.py tests/scripts/test_run_coverage_guided_case_queue.py -q
```
