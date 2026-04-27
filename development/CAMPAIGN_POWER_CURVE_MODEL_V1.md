# Campaign Power Curve Model V1

## Purpose

`campaign_power_curve_model_v1` is a report-only planning model for campaign
encounter design. It helps describe player power, mechanism timing, deck maturity,
economy context, compression context, enemy pressure, and encounter validation needs
around a campaign round.

The model is advisory. It must not become a hard gate, recommendation default path,
learned/reranker authority, or monster-number implementation.

## Current Campaign Evidence

This spec is source-aligned with the current campaign and combat-analysis surfaces:

- Campaign board blocks carry `start_turn`, `duration`, `block_type`, `tags`, and
  optional `encounter_id`.
- Current block vocabulary includes combat, event, shop, boss/elite-like, and DDL
  concepts, but shop economy is not yet a reviewed removal/upgrade route model.
- Tutorial rewards include card-pool picks and resources. Reward services and the
  bundle-style post-combat flow also expose inspiration, trait, and card-pick paths.
- Current campaign rewards do not provide enough evidence to treat removal, transform,
  upgrade, or shop access as guaranteed route solutions.
- Existing encounter data includes tutorial boss/normal encounters and TA encounters
  with single, duo, multi-enemy, elite, countdown, and chore-host pressure shapes.
- Those encounter files support pressure-shape language, not late-phase pacing proof,
  mature checkpoint promotion, or monster-number authority.
- Cardanalysis report-only surfaces already cover deck compression, package health,
  design iteration, mechanism-axis discovery, mechanism fun/health, and evidence
  bundles. They can provide context, not authority.

## Strict Boundary

In scope:

- report-only payloads and CLI artifacts
- phase and checkpoint vocabulary
- qualitative pressure bands
- advisory cardanalysis field mapping
- fixtures and tests that lock non-authority behavior

Out of scope:

- hard gates or pass/fail authority
- recommendation default changes
- learned/reranker promotion
- formal monster stats, damage, health, or enemy roster tuning
- runtime encounter implementation

## Phase Bands

The phase bands remain reviewed assumptions until campaign pacing data is deeper.

| Phase | Round Hint | Current Evidence State | Notes |
| --- | --- | --- | --- |
| `starter` | `0-1` | `source_aligned` | Current campaign can represent opening turns and baseline combat/reward loops. |
| `early` | `2-3` | `review_needed` | Reward services show identity-hint paths, but early reward spacing and observation are not yet reviewed. |
| `build` | `4-6` | `review_needed` | Card-pick rewards support assembly language, but removal, upgrade, and shop routes remain untrusted. |
| `pivot` | `7-9` | `review_needed` | TA encounter data supports disruption-pressure language, not honest compression/removal route claims. |
| `mature` | `10-13` | `review_needed` | Mature pressure shapes are source-visible, but ceiling/recovery checkpoints are not playtest-observed. |
| `late` | `14+` | `hypothesis_draft` | Late pressure is only shape-aligned; checkpoint timing and anti-infinite wording still need dedicated review. |

Evidence-state defaults must stay phase-calibrated:

- non-starter phases do not become `source_aligned` only because they cite current
  campaign source files
- `late` defaults to `hypothesis_draft` and `allowed_use=exploration_prompt` even if
  pressure-shape sources exist
- `curve_checkpoint.evidence_state.calibration_notes` should explain which source
  surfaces justify the current label and which claims remain out of bounds

## Required Payload Sections

Every generated payload should include:

- `contract_version=campaign_power_curve_report_v1`
- `model_version=campaign_power_curve_model_v1`
- `evaluation_mode=report_only`
- `hard_gate_impact=none`
- `campaign_round`
- `curve_checkpoint`
- `player_power_state`
- `deck_maturity_state`
- `mechanism_online_state`
- `economy_state`
- `compression_state`
- `enemy_pressure_profile`
- `encounter_validation_needs`
- `cardanalysis_curve_mapping`
- `authority_boundary=advisory_context_only`

The payload must not expose:

- `overall_pass`
- `overall_fail`
- `hard_gates`
- `blocking_verdict`
- monster stat targets

## Review Readiness

`ready_for_main_agent_review`: yes, for report-only model and implementation review.

Not ready for:

- monster numbers
- runtime encounter implementation
- hard gates
- default recommendation path changes
- learned/reranker default-on behavior

## Validation

Minimum focused validation for this surface:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_power_curve_model_v1.py tests/scripts/test_run_campaign_power_curve_report.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_report_only_surface_registry_v1.py tests/toolkit/combat_analysis/test_cardanalysis_evidence_bundle_v1.py -q
py -3.11 -m pytest tests/toolkit/combat_analysis/test_architecture_boundaries.py tests/shared/test_text_encoding_guards.py -q
git diff --check
```
