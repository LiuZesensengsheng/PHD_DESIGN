# Mechanism Fun Health Evaluation V1

## Purpose

This document defines a reviewed specification for judging whether a cardanalysis
mechanism is fun and healthy after it is understood as a mechanism.

It is intentionally separate from the current mechanism-axis viability layer. The
current layer asks whether an `STS1` mechanism shell is online, coherent, and
repeatable. This document asks whether that mechanism creates good play once it is
online.

## Scope Boundary

In scope:

- `STS1` mechanism-level review language for fun and health.
- Human-reviewed, explainable dimensions that can later become fixture labels.
- Positive handling of combo, loop, and infinite aspirations.
- Degeneracy pressure only when a mechanism is low-cost, low-choice,
  low-constraint, naturally rolled into, and environment-flattening.

Out of scope:

- changing `mechanism_axis_contracts.py`
- changing current mechanism-axis viability fixtures
- changing legality, schema, hard gates, or threshold semantics
- enabling learned ranking or reranking in any default path
- treating `STS2` examples as the same trust tier as reviewed `STS1`
- claiming exact fun prediction or black-box fun scoring

## Review Model

Use this as a second-pass review after mechanism viability:

1. First ask whether the mechanism is online through the existing viability surface.
2. Then ask whether the online mechanism has good player-facing texture.
3. Keep the judgment explainable. Each concern should point to a dimension below.
4. Do not punish combo, loop, or infinite plans by category. Judge the cost,
   constraints, choice density, fail states, and matchup effects.

Suggested labels for a later reviewed pack:

- `strong_positive`: clear fun or health upside
- `healthy`: acceptable pressure with visible strengths
- `watch`: coherent but risky, narrow, or brittle
- `degenerate_risk`: likely to flatten choices or matchup texture
- `fantasy_only`: attractive dream, but not realistically reachable yet
- `not_evaluated`: insufficient reviewed evidence

These labels should stay review annotations until a later decision explicitly promotes
them.

## Dimensions

### `agency`

Definition:

Whether the mechanism gives the player meaningful choices while playing it. Agency is
high when sequencing, target selection, timing, retention, energy use, and risk
management materially affect outcomes. Agency is low when the best play is automatic,
or when the mechanism mostly asks the player to wait for a specific draw order.

Good mechanism signals:

- Multiple viable sequencing lines exist, and the better line depends on the fight.
- The player can trade speed, safety, setup, and payoff timing.
- Draw, retain, discard, stance, or orb decisions change the mechanism's outcome.

Bad mechanism signals:

- The mechanism mostly plays itself once a condition is met.
- The player is locked into one tunnel because skipping setup invalidates the payoff.
- The only meaningful decision happened in deckbuilding, not in combat.

STS1 examples:

- Positive: Silent discard-cycle engines with Acrobatics, Prepared, Reflex, and
  Tactician let the player choose when to spend hand size, energy, and discard slots.
- Positive: Watcher retain/stance plans with protect windows and delayed Wrath entry
  create timing decisions instead of only asking for a threshold card.
- Negative: Grand Finale exactness without enough draw/discard control creates a
  low-agency wait-for-hand-state puzzle.
- Negative: Alpha setup tunnels often ask the player to commit turns to the same line
  even when the encounter is demanding block, damage, or stance flexibility.

### `payoff_texture`

Definition:

Whether the payoff creates varied, legible, and satisfying outcomes rather than only
adding a larger number. Payoff texture is high when the mechanism changes combat mode,
opens multiple release patterns, or makes a payoff feel earned through visible setup.

Good mechanism signals:

- The payoff can arrive as burst, sustain, control, conversion, or safety depending
  on how the player shaped the mechanism.
- The payoff has intermediate milestones before the final spike.
- The release moment is understandable from the cards and state already in play.

Bad mechanism signals:

- The payoff is only a single large number after repetitive setup.
- The mechanism has one correct release and all other lines are traps.
- The payoff card is exciting in isolation but disconnected from the support shell.

STS1 examples:

- Positive: Poison with Noxious Fumes, Bouncing Flask, Catalyst, and Corpse Explosion
  can shift between lock, burst, and multi-enemy release.
- Positive: Defect orb-control shells can choose between Frost safety, Lightning
  pressure, and evoke timing when focus and orb slots are real resources.
- Negative: Thunder Strike greed without enough prior Lightning history turns payoff
  texture into one delayed number.
- Negative: Catalyst-only poison splits create a flashy ceiling but weak texture when
  the deck cannot build poison reliably first.

### `setup_tax`

Definition:

How much the mechanism asks the player to pay before it starts contributing. Setup tax
includes card slots, draw steps, energy, upgrades, powers, relic dependency, and turns
spent below encounter tempo. High setup tax is not automatically bad; it becomes a
problem when the mechanism cannot defend, accelerate, or compensate while setting up.

Good mechanism signals:

- Setup pieces also do useful work before the final payoff.
- The mechanism has a reasonable first functional turn under common draw orders.
- Expensive setup buys a clearly higher ceiling or more flexible future turns.

Bad mechanism signals:

- Setup consumes multiple turns while producing little damage, block, or selection.
- The mechanism needs too many exact pieces before any card becomes good.
- Setup cards compete with each other for the same turn, energy, or hand-size window.

STS1 examples:

- Positive: Establishment plus real retain support can justify setup tax because
  retained cards become cheaper while the deck still controls timing.
- Positive: Exhaust shells with Feel No Pain, Dark Embrace, and Burning Pact can make
  setup pieces contribute block or draw during the transition.
- Negative: Alpha/Beta/Omega plans carry high setup tax when the deck cannot survive
  or accelerate the staged payoff.
- Negative: Over-taxed retain burst plans that need many retained attacks, cost
  reduction, and draw all at once are vulnerable to paying setup without function.

### `fail_state`

Definition:

What happens when the mechanism misses a key draw, loses a setup card, faces an
awkward enemy, or cannot complete its preferred line. A healthy mechanism has a
recoverable fail state. A brittle mechanism collapses into dead cards, wasted turns,
or self-imposed tempo loss.

Good mechanism signals:

- Missed payoff turns still leave block, draw, scaling, or controlled setup.
- The mechanism can pivot to a smaller line without abandoning the whole plan.
- Failure is readable early enough for the player to change course.

Bad mechanism signals:

- Missing one card makes several other cards blank.
- The mechanism fails late, after the player has already paid most of the cost.
- The fallback line is generic survival with no relation to the mechanism.

STS1 examples:

- Positive: Poison lock can still progress through passive poison while the player
  blocks and waits for Catalyst or Corpse Explosion.
- Positive: Frost-backed orb control has a defensive fail state even if the damage
  release is delayed.
- Negative: Grand Finale exactness often fails into a dead rare when draw control
  misses by one card.
- Negative: Thunder Strike packages can fail into a dead payoff if Lightning history
  was too thin or too slow.

### `variance_pressure`

Definition:

How much the mechanism depends on draw order, random generation, enemy behavior, or
state timing that the player cannot reasonably control. Variance pressure is not the
same as variance. Variance is healthy when the mechanism gives the player tools to
shape it; it is unhealthy when the mechanism requires lucky alignment and has weak
recovery from misses.

Good mechanism signals:

- The mechanism contains selection, draw, retain, discard, or other smoothing tools.
- Multiple partial lines remain acceptable under different draw orders.
- Random generation creates choices rather than replacing choices.

Bad mechanism signals:

- The mechanism is judged by best-case draw order.
- One missed threshold or bottom-decked support card invalidates the turn plan.
- Random generation repeatedly chooses the player's line for them.

STS1 examples:

- Positive: Silent draw-discard engines reduce variance pressure by seeing more cards
  and turning discard into resources.
- Positive: Watcher retain plans can lower variance pressure by holding key cards for
  the right stance or Divinity window.
- Negative: Almost-loop Watcher or Ironclad shells that require one exact draw bridge
  to appear on time have high variance pressure.
- Negative: Grand Finale without enough deck-order control is a variance-heavy
  exactness dream rather than a stable mechanism.

### `combo_aspiration`

Definition:

The positive upside of a mechanism's dream state: high ceiling, memorable release,
creative assembly, and a line the player wants to pursue. Combo aspiration is a
positive dimension. Loops, infinites, exactness plans, and combo turns should score
well here when the dream is legible, earned, and exciting.

Good mechanism signals:

- The mechanism has a clear dream that is worth chasing.
- The dream state changes how the deck plays, not only how much it scores.
- The player can see partial progress toward the dream during normal play.

Bad mechanism signals:

- The mechanism has no distinctive ceiling once it is online.
- The dream is so unreachable that it functions as fantasy-only decoration.
- The payoff is strong but not aspirational because the line is automatic or flat.

STS1 examples:

- Positive: Watcher stance/mantra threshold closure into Divinity has strong combo
  aspiration when stance control and mantra support make the release chaseable.
- Positive: Ironclad or Watcher loops can be highly aspirational when resource,
  draw, and deck-size constraints make assembly a meaningful achievement.
- Negative: Raw mitigation piles may be viable survival tools but have low combo
  aspiration if they never convert defense into a memorable turn.
- Negative: Payoff-only Grand Finale or Thunder Strike shells have apparent dreams,
  but the aspiration becomes fantasy-only when the support cannot realistically reach
  the release.

### `degeneracy_pressure`

Definition:

Whether a mechanism is likely to compress combat into a low-choice dominant pattern
that flattens encounter, matchup, and deckbuilding texture. This dimension does not
penalize combo, loop, or infinite play by itself. It only penalizes lines that are
low-cost, low-choice, low-constraint, naturally rolled into, and strong enough to make
most environment questions irrelevant.

Good mechanism signals:

- The loop or combo requires visible assembly, resource care, or matchup adaptation.
- The player still makes meaningful choices after the engine turns on.
- Encounter constraints such as Time Eater, Awakened One, Artifact, multi-enemy
  fights, or damage races still matter.

Bad mechanism signals:

- The mechanism emerges from ordinary good cards without asking for real commitment.
- Once online, the best line is repetitive and nearly choice-free.
- It ignores too many enemy constraints and makes other mechanisms irrelevant.

STS1 examples:

- Positive: Dropkick-style Ironclad infinites are not automatically unhealthy when
  they require Vulnerable access, deck compression, draw closure, and risk management.
- Positive: Corruption plus exhaust payoffs can be a healthy high-ceiling engine when
  card generation, exhaust timing, and enemy pressure keep decisions alive.
- Negative: Watcher stance loops become high degeneracy pressure when the package is
  low-commitment, auto-refunding, and repeatedly turns encounters into the same
  no-cost line.
- Negative: Corruption plus Dead Branch can become high degeneracy pressure only when
  the generated chain is low-choice, self-feeding, and strong enough to erase matchup
  texture; the combo itself is not the problem.

### `matchup_elasticity`

Definition:

How well the mechanism changes shape across different encounter pressures. Matchup
elasticity is high when the mechanism has answers or meaningful tradeoffs against
fast fights, scaling fights, multi-enemy fights, Artifact, power punishers, action
punishers, and defensive races. It is low when one common pressure invalidates the
mechanism or when the mechanism ignores all pressure in the same way.

Good mechanism signals:

- The mechanism can choose faster, safer, wider, or greedier lines by matchup.
- Bad matchups create interesting adaptation instead of hard collapse.
- The mechanism has clear side-support needs that can be reviewed.

Bad mechanism signals:

- One common encounter family turns the mechanism off with little counterplay.
- The mechanism solves every encounter the same way once online.
- Matchup weaknesses are hidden behind average-case scoring.

STS1 examples:

- Positive: Orb-control shells can lean Frost for survival, Lightning for tempo, or
  evoke timing for burst when focus and slots are managed well.
- Positive: Poison shells can adapt between slow boss scaling and Corpse Explosion
  multi-enemy payoff when support density is real.
- Negative: Shiv-only packages with no adaptation can suffer against Time Eater,
  Spikers, or other action-punishing contexts despite strong hallway tempo.
- Negative: Generic power-focus soup can look good until Awakened One-style pressure
  asks whether those powers are a coherent plan or only accumulated value.

## Relationship To Current Mechanism-Axis Viability

The current mechanism-axis viability pack answers whether a mechanism shell is online.
This fun/health framework answers whether an online mechanism is desirable play.

| Existing viability dimension | Primary question | Relation to fun/health |
| --- | --- | --- |
| `support_density` | Is there enough support for the named axis? | Online check. It may inform `setup_tax`, but does not decide fun. |
| `payoff_reachability` | Can the payoff happen without fantasy draw order? | Online check. It informs `fail_state` and `combo_aspiration`. |
| `trigger_availability` | Are there enough triggers to turn the axis on? | Online check. It can reduce `variance_pressure`. |
| `glue_density` | Do bridge cards connect setup to payoff? | Online check. It can improve `agency` and `fail_state`. |
| `repeatability` | Can the plan happen more than once? | Online check. Repetition can be healthy or degenerate depending on choice and constraints. |
| `cross_support_quality` | Do support pieces reinforce the same plan? | Online and coherence check. It does not measure payoff texture by itself. |
| `shell_purity` | Is this a coherent shell rather than soup? | Online identity check. A pure shell can still be boring, brittle, or degenerate. |

Practical split:

- "Is it online?": support density, payoff reachability, trigger availability, glue
  density, repeatability, cross-support quality, shell purity.
- "Is it fun and healthy?": agency, payoff texture, setup tax, fail state, variance
  pressure, combo aspiration, degeneracy pressure, matchup elasticity.

Important consequences:

- A mechanism can be online and still unhealthy, for example a low-choice loop that
  erases matchup texture.
- A mechanism can be offline and still aspirational, for example an exactness payoff
  that needs better support before it should be judged as healthy.
- A mechanism can be infinite and healthy enough for reviewed positive treatment if
  it has meaningful constraints, assembly, choices, and matchup texture.
- A mechanism can be non-infinite and unhealthy if it is brittle, over-taxed, flat, or
  fantasy-only.

## Fixture Needs For Later Implementation

If this specification is implemented later, it should use new reviewed fixture types
instead of changing the current viability pack in place.

Recommended fixture types:

- `online_but_unhealthy`: the current viability surface would accept the shell, but
  fun/health review catches low agency, poor fail state, high degeneracy pressure, or
  weak matchup elasticity.
- `offline_but_aspirational`: the mechanism has a compelling dream, but current
  support density, reachability, trigger access, or glue makes it fantasy-only.
- `healthy_combo_or_loop`: combo, loop, or infinite cases that should be positive or
  acceptable because constraints and choices remain meaningful.
- `degenerate_loop_pressure`: narrow cases that isolate the actual degeneracy failure:
  low cost, low choice, low constraint, natural roll-in, and environment flattening.
- `setup_tax_contrast`: paired cases where similar payoffs differ because one setup
  path contributes while setting up and the other pays dead turns.
- `fail_state_contrast`: paired cases where one mechanism has a recoverable miss and
  the other collapses into dead cards or wasted turns.
- `matchup_elasticity_panel`: small reviewed panels across `STS1` encounter pressures
  such as Gremlin Nob, Book of Stabbing, Sentries, Time Eater, Awakened One, Artifact,
  multi-enemy fights, and action-punishing contexts.
- `payoff_texture_contrast`: cases that separate varied release patterns from a
  single flat payoff number.

Minimum reviewed shape per new fixture family:

1. one clearly healthy positive
2. one online-but-health-risk near neighbor
3. one fantasy-only or over-taxed failure
4. dimension annotations naming the one or two primary reasons
5. explicit notes when combo, loop, or infinite behavior is being treated positively

Trust and promotion rules:

- Keep these fixtures `STS1` reviewed until a separate decision defines another trust
  tier.
- Keep `STS2` examples separate from reviewed `STS1` trust claims.
- Keep learned or reranker use report-only/default-off unless a later human decision
  explicitly promotes it.
- Do not use this framework as a hard gate until reviewed coverage is thick enough to
  make false confidence unlikely.

## Current Bottom Line

Mechanism-axis viability is the right first question: "does this deck plan actually
function?" Mechanism fun/health is the next question: "does that functioning plan make
good play?"

The health layer should protect both sides of the design space:

- preserve ambitious combo, loop, and infinite dreams as real positives when they are
  earned and interesting
- flag brittle, flat, over-taxed, low-choice, or matchup-flattening mechanisms without
  treating the presence of combo as the failure
