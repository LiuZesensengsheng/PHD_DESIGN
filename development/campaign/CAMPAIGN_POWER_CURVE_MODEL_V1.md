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

The phase bands remain reviewed assumptions, but they are now aligned to the current
campaign board cadence instead of arbitrary single-turn cuts.

Current source basis:

- startup seed places the baseline campaign line at `start_turn=0,3,6,9`
- thesis blueprints also default to `between_blocks=3`
- track normalization preserves one 3-turn window per visible block slot

That makes the current board read most naturally as 3-turn phase windows.

| Phase | Round Hint | Current Evidence State | Notes |
| --- | --- | --- | --- |
| `starter` | `0-2` | `source_aligned` | Aligns to the first visible combat window and tutorial baseline loop. |
| `early` | `3-5` | `review_needed` | Aligns to the second board window, where identity hints may appear but are not yet pacing-reviewed. |
| `build` | `6-8` | `review_needed` | Aligns to the third board window, where assembly language is credible but route economy remains untrusted. |
| `pivot` | `9-11` | `review_needed` | Aligns to the fourth board window, where disruption questions begin to make sense. |
| `mature` | `12-14` | `review_needed` | Aligns to the next full window after pivot, where ceiling/recovery reads become relevant. |
| `late` | `15+` | `hypothesis_draft` | Starts at the first late review-chain / DDL-adjacent window and remains hypothesis-only. |

Evidence-state defaults must stay phase-calibrated:

- non-starter phases do not become `source_aligned` only because they cite current
  campaign source files
- `late` defaults to `hypothesis_draft` and `allowed_use=exploration_prompt` even if
  pressure-shape sources exist
- `curve_checkpoint.evidence_state.calibration_notes` should explain which source
  surfaces justify the current label and which claims remain out of bounds
- `curve_checkpoint.evidence_state.source_support` should split current support into
  `block_support`, `reward_support`, and `encounter_support`
- `curve_checkpoint.evidence_state.source_support` is evidence/context language only;
  it must not become approval, gate, or authority vocabulary
- the current calibration expects `block_support` to be stronger than
  `reward_support` / `encounter_support` after `starter`; the later phases remain
  advisory because source visibility is uneven across those support classes

## Late And Anti-Infinite Boundary

Late checkpoints may ask whether highly repeatable mechanisms still leave encounter
texture, constraints, and recovery questions visible. That question is report-only.

`curve_checkpoint.anti_infinite_boundary` must keep this language explicit:

- `starter`, `early`, and `build`: avoid anti-infinite pressure.
- `pivot`: trace-only future repeatability note.
- `mature`: trace or low report-only texture/recovery question.
- `late`: low report-only review context.

The field must not decide loop legality, deck failure, hard-gate status, or monster
stat targets.

`checkpoint_review_checklist` must keep checklist review states separate from
authority vocabulary. The canonical authority boundary remains only:

- `advisory_context_only`

Checklist readiness should use checklist-specific labels such as
`present`, `review_needed`, `advisory_ready`, `stale_check_needed`, and
`out_of_scope`.

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
- `encounter_archetype_profile`
- `cardanalysis_curve_mapping`
- `authority_boundary=advisory_context_only`

The payload must not expose:

- `overall_pass`
- `overall_fail`
- `hard_gates`
- `blocking_verdict`
- monster stat targets

## Planning Case Coverage

The fixture suite now includes report-only campaign-planning cases for:

- Act 1 frontload survival and early elite exposure;
- hallway HP tax before rewards and recovery can compound;
- Act 2 transition shock under multi-enemy, defense, and status pressure;
- slow-scaling package risk before the package is online;
- the same slow package becoming more credible in a mature payoff window;
- recovery-window collapse from upgrade, shop, route, or heal assumptions;
- late payoff timing and texture review.
- a frontload-overfit case where Act 1 hallway and elite performance can look good
  while Act 2 growth, defense, and recovery planning remains dangerous.

These are advisory contexts for future package interpretation. They do not make
campaign power curve reports a card-package hard gate, route simulator, runtime
campaign authority, or reviewed STS1 evidence claim.

## Encounter Archetype Profiles

Archetype profiles are report-only descriptions of what an encounter should reveal.
They can name pressure axes, validation questions, interpretation boundaries, and
avoid lists. They must not define enemy rosters, monster stats, damage, health,
hard counters, or pass/fail outcomes.

Current cataloged profiles used by reviewed fixtures:

- `starter_frontload_and_defense_check`: consumes `frontload_damage`,
  `defense_check`, and optional `multi_enemy_pressure` for baseline survival
  visibility.
- `build_payoff_only_detector`: consumes frontload, defense, low multi-enemy, and
  low status pressure to expose support/bridge/survival gaps.
- `pivot_compression_route_probe`: consumes draw, energy, mechanism disruption, and
  defense pressure to keep compression route evidence visible.
- `mature_scaling_burst_and_fail_state_check`: consumes scaling, burst, defense, and
  report-only anti-infinite pressure to expose ceiling/recovery questions.
- `mature_over_online_texture_probe`: consumes mature/late pressure to ask whether a
  repeatable mechanism still leaves texture and constraints visible.
- `build_multi_enemy_pressure_spread_probe`: consumes `multi_enemy_pressure`,
  `frontload_damage`, and `defense_check` to ask whether an assembling deck can keep
  target spread, defense, and fallback visibility without requiring a final shell or
  enemy-count target.
- `pivot_status_pollution_tolerance_probe`: consumes `status_pollution`,
  `draw_disruption`, and `defense_check` to ask whether a pivot deck has tolerance,
  cleanup, draw buffer, or fallback visibility under status load.

## Closure State

V1 is ready for main-agent review as a report-only implementation surface. The
reviewed fixture suite now exercises phase calibration, checkpoint-level source
support, anti-infinite boundaries, status-heavy pressure, multi-enemy pressure, and
fixture-wide advisory boundary checks.

This does not promote the model to runtime authority, monster tuning, hard gates,
recommendation defaults, or learned/reranker behavior.

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
