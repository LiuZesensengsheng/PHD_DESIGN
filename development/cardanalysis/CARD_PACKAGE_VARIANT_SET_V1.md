# Card Package Variant Set V1

## Purpose

`card_package_variant_set_v1` is the report-only contract for the backup stage in the
LLM/owner card-package workflow.

It sits between target/axis selection and complete card text:

```text
sts1 target -> mechanism axes -> package variants -> complete card draft -> package exam
```

It answers:

```text
Which package backup should be expanded into complete_card_draft_v1 next?
```

It does not generate formal cards or write runtime card data.

## What It Contains

Each variant set includes:

- source, authority, and forbidden-use metadata;
- a target reference to `sts1_exam_target_v1`;
- a generation brief;
- two or more variants;
- card-like slot prompts for each variant;
- a scorecard for axis fit, role coverage, fun texture, strength-band fit, combo
  potential, risk visibility, and draftability;
- risk notes and next draft instructions.

The validator sorts variants by advisory score and names a recommended variant for
the next `complete_card_draft_v1` expansion.

## Boundary

All V1 variant sets use:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`

The selected variant is only a recommended backup. It is not a promoted card package,
reviewed evidence, legality decision, or hard gate.

## Current Fixture

The first fixture is:

```text
tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json
```

It compares three Silent backups:

- `poison_clock_retain_bridge`: recommended, bridge-before-payoff package;
- `shiv_pressure_poison_pivot`: watch variant with soup/frontload risk;
- `delayed_catalyst_exactness`: high-ceiling variant with exactness risk.

## Entrypoints

```powershell
python scripts/validate_card_package_variant_set.py --write-template tmp/combat_analysis/card_package_variant_set_template.json
python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json
python scripts/validate_card_package_variant_set.py --input tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --write-report tmp/combat_analysis/card_package_variant_set_report.md
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_package_variant_set_v1.py tests/scripts/test_validate_card_package_variant_set.py -q
```

## Stop Lines

Pause for human review before any follow-up:

- writes runtime card data;
- turns a variant into formal card definitions without `complete_card_draft_v1`;
- promotes a variant as reviewed evidence;
- changes hard gates, default synthesis, learned behavior, or reranker behavior.

