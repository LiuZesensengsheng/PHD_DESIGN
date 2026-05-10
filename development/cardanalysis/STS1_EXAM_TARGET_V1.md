# STS1 Exam Target V1

## Purpose

`sts1_exam_target_v1` is a report-only contract for the target side of an STS1
card-package design exam.

It answers:

```text
What character, axis, card-shape, reference-anchor, and rubric constraints should a
draft package obey before it becomes complete card text?
```

It does not claim a complete STS1 ontology and does not decide whether a card should
enter the game.

## What It Contains

Each target includes:

- source, authority, and forbidden-use metadata;
- game and character identity;
- character design tenets, texture goals, risk tolerances, and anti-goals;
- preferred primary axes, secondary axes, support axes, and rejected axes;
- card count, cost, type, rarity, role, numeric, and upgrade guidelines;
- STS1 reference anchors and risk patterns;
- exam rubric dimensions and readiness questions.

## Boundary

All V1 targets use:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`

Required forbidden uses include:

- `hard_gate_promotion`
- `legality_decision`
- `default_synthesis_path`
- `formal_card_promotion`
- `runtime_card_definition`
- `reviewed_evidence_claim`
- `complete_sts1_ontology_claim`

## Current Fixture

The first target fixture is:

```text
tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json
```

It focuses Silent around:

- primary axis: `poison`;
- secondary axes: `retain`, `shiv`;
- support axes: `draw_engine`, `discard_cycle`, `block_engine`, `copy_exactness`.

## Entrypoints

```powershell
python scripts/validate_sts1_exam_target.py --write-template tmp/combat_analysis/sts1_exam_target_template.json
python scripts/validate_sts1_exam_target.py --input tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json
py -3.11 -m pytest tests/toolkit/combat_analysis/test_sts1_exam_target_v1.py tests/scripts/test_validate_sts1_exam_target.py -q
```

## Stop Lines

Pause for human review before any follow-up:

- writes runtime card data;
- promotes STS1 target constraints to hard gates;
- claims a complete STS1 ontology;
- promotes source-mined or owner material as reviewed evidence;
- changes default synthesis, learned behavior, or reranker behavior.

