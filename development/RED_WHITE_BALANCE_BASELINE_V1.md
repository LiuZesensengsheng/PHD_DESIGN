# Red White Balance Baseline V1

## Goal

This document defines the first playable balance baseline for the currently implemented red and white card pools.

This is not final balance. It is a controlled first pass intended to:

- reduce obvious over-efficiency
- buff obvious low-payoff white setup cards
- keep existing archetype identities intact
- preserve current implementation shape and testability

## Scope

Included:

- implemented red cards in `data/cards/red/`
- implemented white cards in `data/cards/white/`
- numeric-only balance changes

Excluded:

- incomplete white placeholder rows
- redesigning card identities
- new mechanics
- full multi-color meta balance

## Budget Rules

### Red

- `1` energy common attack baseline: around `6-8` direct damage
- frontier first-play bonus should usually be worth about `+2 to +4`
- a common card that both develops board state and creates extra cards must pay for that flexibility through lower raw output or higher cost
- draw, energy gain, and temporary card generation should not stack at common without a visible efficiency tradeoff
- power cards that scale repeated cheap actions should be costed conservatively

### White

- `0` energy common defense should be modest and mostly setup-oriented
- move/sort cards should not out-damage dedicated attack cards unless their condition is hard
- pointer engine setup must be affordable enough to actually enable the archetype
- endpoint and reposition payoff cards should reward setup, but not overshoot generic attacks by too much
- white rare payoff should feel stronger once setup exists, but baseline setup cards must remain playable

## First Pass Changes

### Red changes

| Card | Change | Reason |
|---|---|---|
| `red_defense_and_strike` | `6/6` to `5/5` | Mixed common was too efficient as both defense and damage |
| `red_keep_up` | damage `8` to `6` | Free-rolling damage plus energy was above common baseline |
| `red_scribble_note` | confidence `5` to `4` | Card creation plus block on a common needed a tradeoff |
| `red_scribble_small` | damage `4` to `3` | Token damage was carrying too much total package value |
| `red_note_dance` | cost `1` to `2` | Two token generation plus frontier draw was too cheap |
| `red_frontier_annotation` | `7+3` to `6+2` | Damage plus token generation exceeded normal common rate |
| `red_scribble_amplifier` | cost `1` to `2` | Token engine payoff needed more setup cost |
| `red_inspiration_blade_rain` | create `3` to `2` tokens | Token burst was too front-loaded |
| `red_scribble_finisher` | per scribble `3` to `2` | Rare finisher was spiking too hard off cheap setup |
| `red_frontier_damage_core` | cost `1` to `2` | Repeat damage scaling was too easy to deploy |
| `red_crossdomain_superconductor` | cost `2` to `3` | Cross-color discount engine needed slower access |
| `red_literature_flood` | cost `2` to `3` | Two discounted off-color attacks was too much tempo |
| `red_blind_literature` | cost `0` to `1` | Rare upside was too efficient at zero cost |
| `red_cost_burst_read` | multiplier `x3/x4` to `x2/x3` | Random burst was overshooting too often |
| `red_inspiration_preheat` | cost `2` to `3` | Ongoing draw discount engine needed more commitment |

### White changes

| Card | Change | Reason |
|---|---|---|
| `审批` | cost `1` to `0` | Setup-only card was too slow for its payoff |
| `深呼吸` | confidence `5` to `4` | Zero-cost defense needed to stay modest |
| `校正` | confidence `9` to `8` | Too efficient relative to the zero-cost baseline |
| `合规审判` | cost `2` to `1` | Setup-dependent payoff needed to become more playable |
| `继承` / `批判` | damage `6` to `5` | Reposition commons were overpaying on damage |
| `插入` | damage `4` to `5` | Endpoint-only move card was lagging behind other commons |
| `结题报告` | multiplier `2` to `3` | Reposition payoff was too low for its setup burden |
| `遍历` | cost `2` to `1` | Pointer engine entry cost was slowing the whole color down |
| `聚焦现在` | cost `3` to `2` | Rare payoff needed to come online sooner |
| `按序点名` | pointer hit `3` to `4` | Sequencing payoff was slightly low |
| `乱动·洗场爆裂` | sequence base `2` to `3` | Shuffle payoff was low for a 2-cost uncommon |
| `顶点斩` | `6/10` to `5/9` | Endpoint attack remained good without overshooting |

## Deferred Issues

These cards may still need second-pass work that is not purely numeric:

- `red_cross_amplify`
- `red_borrowed_ignition`
- `red_last_line`
- `red_frontier_continuous_draw`
- `a0b1c2d3-e4f5-6789-abcd-000000000119`
- `规整归档`

These are deferred because they are more sensitive to engine behavior, scripted effects, or missing implementation detail.
