# Mechanism Axis Discovery V1

## Purpose

Explore candidate mechanism axes before card generation or card-package work.

This surface asks:

- What foundation/base axes does the mechanism need?
- Does the mechanism keep its own player choice once draw, energy, discard, removal,
  compression, retain, filter, defense, damage, scaling, or exhaust support it?
- Which parameter is worth searching first?

This document and evaluator intentionally defer project temperament matching. A later
layer can decide whether a promising axis fits the game's ideal tone.

## Scope Boundary

In scope:

- report-only mechanism-axis candidate review
- report-only candidate-axis cards as a discovery expression layer
- base-axis dependency vectors
- parameter response targets
- foundation-axis identity override risk
- first probe recommendations

Out of scope:

- generating cards
- selecting a final project temperament
- changing mechanism-axis viability gates
- changing legality, schema, threshold, or synthesis hard paths
- enabling learned/reranker defaults

## Optional Case-Backed Context

`mechanism_axis_discovery_v1` may optionally consume:

- `normalized_design_case`
- `feature_projection_payload`

These inputs are discovery context only. They may enrich:

- discovery wording,
- surfaced candidate-axis hints,
- candidate-axis card evidence status and missing-case requests,
- uncertainty notes,
- next-review direction.

They must not:

- change discovery labels or scores by themselves,
- promote source-mined or report-only material into reviewed authority,
- change mechanism-axis viability hard gates,
- claim mechanism-family ownership,
- change default synthesis or learned/reranker behavior.

## Core Concepts

### Mechanism Axis

The named decision loop or fantasy being explored, such as delayed charge/release,
discard velocity, copy exactness, dice-face allocation, sacrifice tempo, or board
position pressure.

### Foundation/Base Axis

A lower-level resource or throughput axis that many mechanisms can use:

- `draw`
- `energy`
- `discard`
- `removal`
- `compression`
- `retain`
- `filter`
- `defense`
- `damage`
- `scaling`
- `exhaust`

Foundation axes can support a mechanism. They can also claim primary identity when the
candidate explicitly names that axis, such as `discard_velocity`.

The broader design vocabulary for foundation axes, including `status`,
`search_tutor`, `temporary_generation`, `defense_block`, and
`compression_removal` aliases used in card review, lives in
`docs/development/cardanalysis/CARDANALYSIS_FOUNDATION_AXIS_TAXONOMY_V1.md`.
That taxonomy is advisory language and does not expand discovery scoring, gates,
or default synthesis behavior by itself.

### Axis Agency Preservation

The key V1 question:

- Does the named mechanism still force its own choices after it receives foundation
  support?

Good candidates benefit from foundation axes without being replaced by them.

## Candidate Axis Cards

The summary payload now includes a report-only `candidate_axis_cards` section.
Each card is still discovery output, not a canonical family or promotion claim.

Each card records:

- why the mechanism is worth exploring (`mechanism_promise`),
- which support axes it appears to need,
- what it should be compared against so generic throughput does not masquerade as
  mechanism identity,
- likely payoff window and failure modes,
- setup tax plus agency/counterplay notes,
- case/projection evidence status,
- missing reviewed cases still needed,
- the existing `recommended_next_probe` wording,
- `authority_boundary = advisory_context_only`.

This layer must stay deterministic and downstream-safe:

- it must not rewrite `discovery_label`, `score`, or `recommended_next_probe`,
- it must not promote source-mined/generated context into reviewed evidence,
- it must not imply hard-gate viability or formal family ownership,
- it must not become card generation.

## Output Labels

- `priority_probe`: candidate has preserved agency, foundation support, and a
  high-benefit parameter worth searching.
- `promising_axis`: candidate has enough structure for a small package probe but needs
  more evidence.
- `needs_parameter_probe`: candidate has mechanism shape but no clear parameter to
  search.
- `under_supported_axis`: candidate lacks explicit foundation-axis support.
- `identity_swallowed_risk`: draw, energy, discard, or another foundation axis is doing
  the real identity work.
- `review_only_candidate`: keep as discovery note until sharper evidence exists.

## Default Command

```powershell
python scripts/run_mechanism_axis_discovery.py --input tests/fixtures/combat_analysis/mechanism_axis_discovery_v1 --output-dir <dir>
```

Write a template:

```powershell
python scripts/run_mechanism_axis_discovery.py --write-template <path>
```

## Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_discovery_v1.py tests/scripts/test_run_mechanism_axis_discovery.py -q
```

## Source Mining

External game-mechanic collection lives in
`docs/development/cardanalysis/MECHANISM_SOURCE_MINING_V1.md`.

The first source-mining fixture is:

`tests/fixtures/combat_analysis/mechanism_axis_discovery_v1/mechanism_axis_source_mining_pack1_v1.json`

Night of Full Moon has a separate PvE deckbuilder fixture:

`tests/fixtures/combat_analysis/mechanism_axis_discovery_v1/mechanism_axis_source_mining_night_of_full_moon_v1.json`

The first post-mining triage shortlist lives in:

`docs/development/cardanalysis/MECHANISM_AXIS_PROBE_SHORTLIST_V1.md`

## Position Redirect Code Preflight

The first code-handoff preflight surface for a live reviewed candidate is:

`tools/combat_analysis/design_engine/position_redirect_code_preflight.py`

Run it with:

```powershell
python scripts/run_position_redirect_code_preflight.py --input tests/fixtures/combat_analysis/position_redirect_code_preflight_v1/position_redirect_code_preflight_reviewed_v1.json --output-dir <dir>
```

Validate it with:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_position_redirect_code_preflight_v1.py tests/scripts/test_run_position_redirect_code_preflight.py -q
```

This surface is a report-only go/no-go handoff for later bounded implementation. It
does not promote `position_redirect_threat_control` into a formal mechanism family and
does not change mechanism-axis contracts, hard gates, synthesis/default
recommendation, or learned/reranker defaults.
