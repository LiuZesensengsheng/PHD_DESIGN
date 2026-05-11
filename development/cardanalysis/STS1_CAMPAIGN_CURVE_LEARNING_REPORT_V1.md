# STS1 Campaign Curve Learning Report V1

## Purpose

This report captures source-mined and design-reference lessons from `Slay the
Spire 1` campaign pacing for future report-only card-package evaluation.

The focus is campaign power curve, not card design. The report asks:

- when a package must function,
- which encounter types expose different weaknesses,
- how growth resources change the risk budget,
- how a package can look coherent in isolation but fail a real roguelike
  deckbuilder campaign.

## Authority Boundary

This report is advisory context only.

It does not:

- modify runtime campaign,
- design new cards,
- create formal card data,
- create hard gates,
- claim reviewed evidence,
- claim a complete STS1 ontology,
- merge STS1 campaign pacing with Darkest Dungeon stress, virtue, or affliction
  loops.

STS1 campaign curve material here is kept separate from `stress_resolve_model_v1`.
DD1-style stress carryover remains a different pressure model. This report only
uses STS1-style map, encounter, deck-growth, and run-resource pacing.

## Source Status

Source tier: `source_mined_design_reference`.

Useful source anchors:

- [Map locations](https://slay-the-spire.fandom.com/wiki/Map_locations): room
  types, shops, rest sites, treasure, elites, bosses, and reward categories.
- [Elites](https://slay-the-spire.fandom.com/wiki/Elites): elite rewards and act
  elite lists.
- [Bosses](https://slay-the-spire.fandom.com/wiki/Bosses): act boss lists,
  pre-boss rest-site structure, and boss rewards.
- [Rest Sites](https://slaythespire.wiki.gg/wiki/Rest_Sites): rest/smith default
  options and boss-preceding rest-site note.
- [The Merchant](https://slaythespire.wiki.gg/wiki/Merchant): shop as the gold
  sink for cards, relics, potions, and card removal.
- [Ironclad](https://slay-the-spire.fandom.com/wiki/Ironclad),
  [Silent](https://slay-the-spire.fandom.com/wiki/Silent),
  [Defect](https://slay-the-spire.fandom.com/wiki/Defect), and
  [Watcher](https://slay-the-spire.fandom.com/wiki/Watcher): character starting
  relics, starter-deck pressure, and high-level strategy notes.

These sources support factual orientation. They are not project-reviewed balance
evidence.

## Core Curve Thesis

STS1's campaign curve is not a smooth increase in enemy numbers. It is a sequence
of changing questions:

1. Act 1 asks whether the deck can become functional before elite pressure converts
   greed into HP loss.
2. Act 2 asks whether the deck can survive a harder transition while adding
   scaling, multi-enemy answers, status tolerance, and recovery discipline.
3. Act 3 asks whether the deck's mature plan can handle specialized constraints
   without being too narrow, too slow, too action-heavy, too power-heavy, or too
   dependent on one scripted line.

The campaign therefore evaluates a package by online timing, not only by final
combo quality. A package can be coherent and still be campaign-unfit if it misses
the window where the run needs immediate output, recovery control, or matchup
adaptation.

## Act Pressure Changes

### Act 1

Act 1 is the starter-deck repair act.

Normal combats are not merely filler. They provide the first card rewards and
health-tax signals. A deck that refuses early damage, block, or simple draw because
it wants a later engine will often lose the right to take elites.

Act 1 elites test early functionality from different angles:

- `Gremlin Nob` pressures skill-heavy or non-damage setup plans.
- `Lagavulin` pressures decks that cannot convert a preparation window into enough
  damage before capability decay matters.
- `Three Sentries` pressure draw quality, status pollution tolerance, and multi-target
  pacing.

Act 1 bosses ask for a first real deck identity:

- `Slime Boss` rewards burst and split timing.
- `The Guardian` asks for attack/block rhythm and mode awareness.
- `Hexaghost` asks whether the deck can scale or race a visible clock.

Campaign lesson: an Act 1-compatible package needs a first useful turn, enough
frontload to win ordinary fights, and at least one credible elite-facing answer
before it can ask for a speculative payoff.

### Act 2

Act 2 is the transition shock.

The deck has more cards and relics, but enemy pressure rises faster than many
incomplete packages mature. Act 2 punishes the run that used Act 1 rewards to build
a nice future plan without enough immediate defense, AoE, draw smoothing, or
scaling bridge.

Act 2 elites expose wider capability gaps:

- `Book of Stabbing` pressures single-target defense and damage race endurance.
- `Gremlin Leader` pressures target priority, add control, and AoE or burst access.
- `Slavers` / `Taskmaster` pressure immediate opening turns and multi-enemy damage
  intake.

Act 2 bosses ask the deck to reorient:

- `Bronze Automaton` tests delayed burst survival and artifact/minion disruption.
- `The Champ` tests phase-change discipline and controlled burst after setup.
- `The Collector` tests add pressure, scaling, and long-fight stability.

Campaign lesson: Act 2 is where "online later" becomes dangerous. A package needs
midgame function, not just eventual ceiling. It should show how the deck survives
while assembling the engine.

### Act 3

Act 3 is the specialization and constraint act.

A mature deck should now have a real plan, but Act 3 asks whether that plan is
too narrow. Normal fights and elites can challenge action count, power count,
draw order, multi-enemy output, intangible or mitigation windows, scaling races,
and status handling.

Act 3 elites check mature-package texture:

- `Giant Head` rewards decks that can exploit a delayed burst window instead of
  only surviving.
- `Nemesis` pressures timing, status tolerance, and output into awkward windows.
- `Reptomancer` pressures fast add control and explosive opening defense.

Act 3 bosses are final reorientation checks:

- `Awakened One` pressures power-heavy scaling and asks whether the deck has another
  mode.
- `Time Eater` pressures action-heavy lines, infinite-adjacent plans, and low-choice
  card spam.
- `Donu and Deca` pressure scaling, multi-target management, and sustained defense.

Campaign lesson: Act 3 does not merely reward the highest ceiling. It asks whether
the ceiling still leaves flexible choices under specific constraints.

## Encounter Tier Requirements

### Normal Combats

Normal combats ask for low-cost consistency:

- Can the deck kill or stabilize without spending rare resources every fight?
- Does the package improve ordinary draw quality, or does it add blanks until the
  payoff appears?
- Does the deck keep HP high enough to choose upgrades and elites later?

Normal fights are also card-reward intake. They pressure the player to patch current
problems rather than draft only toward an imagined final shell.

### Elites

Elites are route bets. They convert deck readiness into relic acceleration, but the
cost is HP, potion use, and sometimes future route restriction.

Elites ask:

- Is there enough frontload for Act 1?
- Is there enough defense and add handling for Act 2?
- Is the mature plan flexible enough for Act 3 constraints?
- Can the deck spend a potion or HP now and still recover before the boss?

The important package question is not "can this package beat one known elite in a
curated deck?" It is "does this package leave the run with an elite-taking plan
before the relic snowball falls behind?"

### Bosses

Bosses are act-end reorientation tests. They are visible on the map, and the room
before each Act 1-3 boss is a rest site, so the player can plan rest versus smith.

Bosses ask:

- Can the deck carry a plan through a longer fight?
- Does it have enough scaling or burst for the specific boss texture?
- Does it need a final upgrade before the boss, and can it afford that instead of
  healing?
- Does the plan survive a phase shift, add wave, artifact, power punish, action
  punish, or multi-enemy setup?

Campaign lesson: bosses validate whether Act rewards formed a coherent run plan,
not whether a single card package has a perfect best-case turn.

## Player Growth Resources

### Cards

Cards are both power and pollution. Early card rewards must patch immediate
requirements; later rewards must increase density, scaling, or matchup coverage
without diluting the deck's main plan.

Campaign implication: card-package evaluation should ask whether a package adds
useful cards at the time they would realistically be picked.

### Relics

Relics are often the reward for elite risk, treasure rooms, shops, events, and boss
chests. They can turn marginal packages into strong ones, but package evaluation
should not assume a specific relic unless that dependency is explicit.

Campaign implication: relic dependency is acceptable as a note, not as hidden proof
that a package is generally online.

### Removal And Compression

Removal is a route resource, not a free cleanup step. Shops can provide card
removal, some events or relics can help, and in-combat exhaust/filtering can reduce
effective pollution. These are not interchangeable.

Campaign implication: exactness, loop, and high-density packages need compression
truthfulness. A compact final shell should not be treated as a starter-deck route
unless removal, transform, exhaust, draw, or retain assumptions are named.

### Upgrades

Upgrades are usually bought with rest-site opportunity cost. The same fire can heal
or smith, so upgrade-hungry packages must show why their upgrade timing is worth the
lost recovery.

Campaign implication: "needs two upgrades before function" is a campaign risk, even
if the final upgraded package is elegant.

### Gold And Shops

Gold buys flexibility: cards, relics, potions, and removal. A package that requires
shop removal and shop relics at the same time may be overclaiming the route budget.

Campaign implication: shop dependency should be represented as a recovery/resource
window risk, not hidden behind package-health success.

### Potions

Potions are one-fight bridges. They are especially important for early elites and
dangerous transition fights, but they cannot be counted as repeatable package
function.

Campaign implication: potion support can justify taking a risk once. It should not
erase a repeated elite-check or boss-check failure.

## Package Online Timing

### Early Available

An early-available package has useful output before the full engine exists.

Healthy early signs:

- immediate damage, block, or draw smoothing,
- non-payoff cards that still advance ordinary fights,
- partial support that improves elite readiness,
- low upgrade and relic dependency.

Risk signs:

- the first useful card is a payoff,
- support cards are dead before a rare or upgrade appears,
- the package asks Act 1 to wait.

### Midgame Forming

A midgame-forming package should be credible during Act 2.

Healthy midgame signs:

- survival bridge while scaling comes online,
- answer to multi-enemy or burst pressure,
- enough draw/energy/card-flow support to reduce variance,
- visible plan for boss reorientation.

Risk signs:

- the package only handles single-target slow fights,
- adding support increases setup tax faster than payoff,
- Act 2 elites require off-package cards that the report hides.

### Late Ceiling

A late-ceiling package should win mature fights without flattening all texture.

Healthy late signs:

- ceiling is earned by setup and resource management,
- action, power, and draw constraints still matter,
- fail states remain playable,
- different bosses ask for different lines.

Risk signs:

- the package becomes a single repeated script,
- it ignores too many encounter constraints,
- it only works after unrealistic compression,
- it has no answer when a boss attacks its preferred play pattern.

## How STS1 Punishes Bad Campaign Fit

### Too Slow

Slow packages lose HP in normal combats, skip elites, or reach Act 2 without enough
relic acceleration. STS1 punishes them before their late payoff can prove anything.

### Too Greedy

Greedy packages take payoff, upgrades, or relic assumptions before bridge and
stabilization. They often look strong in final-shell review and weak in route review.

### Too Narrow

Narrow packages answer one family of fights but fail when the act changes the
question. The most visible failures are single-target only, boss-only, power-only,
action-spam-only, or exactness-only plans.

### Over-Combo

Over-combo packages have real fantasy but insufficient route proof. They require too
many pieces, too much compression, too many upgrades, or too much draw alignment
before the campaign has paid for them.

## Recovery And Risk Windows

STS1 keeps risk interesting by placing recovery choices near power choices:

- A rest site can heal or upgrade.
- A shop can buy immediate power, future scaling, a potion, or removal.
- A route can choose more elites for relic acceleration or fewer elites for safety.
- A potion can protect a risky elite, but then the next fight may lack that bridge.
- Boss-visible routing lets the player plan, but also makes wrong priorities costly.

Campaign implication: card-package evaluation should ask whether the package creates
healthy choices inside these windows. A package is risky when it collapses the choice
into "must smith or die", "must remove or fail", "must find a shop", or "must spend
potions every elite".

## Four Character Curve Differences

### Ironclad

Ironclad starts with the highest HP and Burning Blood, so he can often convert HP into
early aggression and elite pressure. His curve supports frontload, strength scaling,
exhaust, self-damage, block conversion, and recovery through combat rewards.

Package implication: Ironclad packages can spend health or setup more credibly than
Silent, but they still need Act 1 damage and Act 2 scaling/defense bridges.

### Silent

Silent has a larger starter deck and weaker upfront damage, but strong card flow,
mitigation, poison, discard, retain, and late-game control. Source notes describe her
Act 1 as especially pressured if damage density is not fixed.

Package implication: Silent packages need early damage or mitigation patches before
claiming poison/control late ceiling. A beautiful late package can be campaign-bad if
it does not solve Act 1 elite access.

### Defect

Defect's Cracked Core and orbs provide early passive output, while focus, orb slots,
powers, and scaling engines create strong late positions. The curve risk is setup:
some Defect packages spend turns becoming powerful while Act 2 and Act 3 ask for
immediate defense, AoE, or burst.

Package implication: Defect packages should declare their first functional turn and
their fallback while powers/orbs/focus assemble.

### Watcher

Watcher has a strong starter deck, Wrath burst, stance control, Scry, Retain, and
high ceiling. The curve risk is not lack of power; it is commitment timing. Wrath can
end fights quickly, but bad stance exit timing can turn strength into damage taken.

Package implication: Watcher packages can be pickier and smaller, but must show exit
discipline, fail states, and anti-runaway texture for stance loops or Divinity plans.

## Lessons For Future Card Package Exams

Future `card_package_exam` integration should not ask only whether a package is
coherent. It should also ask:

1. Does the package produce useful Act 1 function before payoff?
2. Does it survive Act 2 transition pressure while forming?
3. Does it have a mature Act 3 ceiling with constraint flexibility?
4. Which normal, elite, and boss checks expose its first failure?
5. Which growth resource is being over-assumed: card rewards, relics, removal,
   upgrades, shops, gold, or potions?
6. Does the package's online timing match the character's natural curve?
7. Are recovery windows preserved as choices, or collapsed into mandatory rescue
   steps?

The short version: STS1 evaluates packages across the campaign by forcing them to
be partially useful before they are complete.

