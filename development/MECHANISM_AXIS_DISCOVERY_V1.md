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

### Axis Agency Preservation

The key V1 question:

- Does the named mechanism still force its own choices after it receives foundation
  support?

Good candidates benefit from foundation axes without being replaced by them.

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
`docs/development/MECHANISM_SOURCE_MINING_V1.md`.

The first source-mining fixture is:

`tests/fixtures/combat_analysis/mechanism_axis_discovery_v1/mechanism_axis_source_mining_pack1_v1.json`

Night of Full Moon has a separate PvE deckbuilder fixture:

`tests/fixtures/combat_analysis/mechanism_axis_discovery_v1/mechanism_axis_source_mining_night_of_full_moon_v1.json`

The first post-mining triage shortlist lives in:

`docs/development/MECHANISM_AXIS_PROBE_SHORTLIST_V1.md`
