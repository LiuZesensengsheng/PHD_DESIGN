# Card Package Exam V1

## Purpose

`card_package_exam_v1` is a report-only exam chain for the workflow:

```text
mechanism-axis search -> package seed -> complete card drafts -> package-health feedback
```

It is intended for STS1-style design simulation where an LLM or owner proposes full
card drafts under model-selected axes, then the local model evaluates package health.

## What V1 Does

V1 consumes:

- a `mechanism_axis_search_bundle_v1` snapshot;
- a generated-hypothesis `card_package_proposal_v1` package seed;
- one or more `complete_card_draft_v1` packages.
- optionally, exactly one `campaign_curve_profile_v1` profile for advisory
  campaign curve fit notes.

V1 outputs:

- axis alignment status;
- per-draft package-health label;
- embedded `card_package_health_v1` summary;
- optional `campaign_curve_fit` risk tags and human review questions;
- an advisory outcome.

## What V1 Does Not Do

V1 does not:

- choose final cards for the game;
- write runtime card data;
- create formal card promotion;
- claim reviewed evidence;
- create hard gates;
- enable default synthesis, learned behavior, or reranker behavior.

## Current STS1 Exam Fixture

The first fixture is:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json
```

It tests the current Silent path:

- primary axis: `poison`;
- secondary axes: `retain`, `shiv`;
- complete draft cards: `5`;
- package-health expected label: `healthy_package`.

## Entrypoints

```powershell
python scripts/run_card_package_exam.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --package-seed <generated-card-package-proposal-v1.json> --draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --output-dir tmp/combat_analysis/card_package_exam_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_card_package_exam_v1.py tests/scripts/test_run_card_package_exam.py -q
```

Use `scripts/run_mechanism_axis_package_seed.py` to generate the package seed from the
current mechanism-axis design brief fixture before running the exam.

## Interpretation

An outcome like `draft_package_ready_for_human_review` means:

- the draft package is axis-aligned;
- package-health evaluation did not classify it as payoff-only, generic-goodstuff,
  overstuffed, or brittle exactness;
- human review is still required before any promotion.

## Optional Campaign Curve Fit

`--campaign-curve-profile` adds a report-only `campaign_curve_fit` section. It
translates package-health and draft-structure signals into campaign timing questions
against the selected profile:

- online timing label;
- curve risk tags such as `too_slow`, `too_narrow`,
  `recovery_window_collapse`, `elite_check_failure`, and
  `act2_transition_shock`;
- recommended human review questions.

This section is advisory only. It does not change `advisory_outcome`, create hard
gates, modify runtime campaign, or claim reviewed STS1 evidence.

## Campaign Curve Fit Example Fixtures

Reusable examples live in:

```text
tests/fixtures/combat_analysis/card_package_exam_curve_fit_v1/
```

The first manifest covers:

- a healthy/golden Silent draft against the advanced campaign curve profile;
- a high setup-tax negative control that should surface `too_slow`,
  `recovery_window_collapse`, and `act2_transition_shock`.

These fixtures are for exam interpretation only. They remain report-only and do not
define new cards, runtime campaign behavior, hard gates, or reviewed STS1 evidence.
