# Mechanism Axis Probe Shortlist V1

## Purpose

Select the first mechanism-axis candidates worth turning into reviewed probes.

This is the step after source mining. It does not generate cards and does not decide
final project temperament. It only chooses which axes deserve the next reviewed
contrast or minimal package sketch.

## Current Deprioritized Sources

Based on design direction feedback, do not spend the next probe batch on:

- Night of Full Moon werewolf-style self-attack / rage / transformation loops
- Night of Full Moon mechanic-style gadget / assembly / device loops

Reason:

- These are not currently reading as fun or aligned enough to justify first-batch
  probe work.
- They may remain as later references, but they should not displace stronger
  candidate axes in this round.

## First Probe Batch

| Priority | Candidate | Source | Why This Moves Forward | First Probe |
| --- | --- | --- | --- | --- |
| 1 | `night_full_moon_prayer_countdown_queue_v1` | Night of Full Moon | Strong delayed-payoff structure, visible countdown, survival/setup tension, and good failure value. | Compare delayed prayer with countdown support vs payoff-only delayed burst. |
| 2 | `night_full_moon_elemental_status_rotation_v1` | Night of Full Moon | Good bridge from element identity into parameter search: stack count, element alignment, payoff timing. | Compare frost/burn/lightning alignment shell vs generic spell damage pile. |
| 3 | `dicey_dungeons_dice_slot_allocation_v1` | Dicey Dungeons | Very clean player agency: allocate imperfect random values into constrained slots. | Compare value-allocation choices vs raw random damage. |
| 4 | `into_the_breach_position_redirect_v1` | Into the Breach | High-agency tactical axis with small actions solving large threats. | Compare push/redirect threat control vs direct damage-only control. |
| 5 | `balatro_joker_rule_rewrite_v1` | Balatro | Strong rule-modifier pattern; useful for thinking about run-level identity without copying poker. | Compare rule-rewrite package vs generic multiplier stacking. |
| 6 | `monster_train_floor_capacity_lineup_v1` | Monster Train | Spatial/slot pressure creates package identity and clear support/payoff roles. | Compare floor/slot lineup package vs generic unit stat pile. |
| 7 | `dominion_removal_thinning_conversion_v1` | Dominion | Directly connects to our deck compression/removal model and starter-pollution questions. | Compare removal-as-identity package vs generic draw compression. |
| 8 | `hearthstone_discover_option_selection_v1` | Hearthstone | Gives choice density without simply increasing hand size; useful for adaptive PvE design. | Compare constrained option selection vs raw draw/filter. |

## Hold For Later

- `night_full_moon_action_point_tempo_budget_v1`
  - Useful, but easy to collapse into generic energy tuning.
- `night_full_moon_blessing_rule_modifier_v1`
  - Useful, but overlaps with Balatro-style rule rewrite and may be better as a
    run-layer modifier after core combat axes are clearer.
- `night_full_moon_counter_reaction_window_v1`
  - Useful, but needs UI/readability work before it should become a first-batch
    content probe.
- `night_full_moon_spell_mana_type_engine_v1`
  - Useful, but currently too close to generic spell energy/draw soup unless paired
    with a sharper type payoff.

## Next Work

The next implementation batch should add reviewed probe fixtures for the first 3-4
shortlisted axes:

1. `prayer_countdown_queue`
2. `elemental_status_rotation`
3. `dice_slot_allocation`
4. `position_redirect_threat_control`

Each probe should include:

- one online shell
- one payoff-only or generic-throughput negative
- one adjacent-axis confusion case

Keep this as reviewed exploration evidence, not a hard-gated mechanism-family
promotion.
