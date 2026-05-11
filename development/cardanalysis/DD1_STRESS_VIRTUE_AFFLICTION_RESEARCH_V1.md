# DD1 Stress Virtue Affliction Research V1

## Purpose

Capture what is useful to learn from Darkest Dungeon 1's stress, virtue, and
affliction loop.

This is a research report only. It studies play structure and design pressure.
It does not design formal cards, write runtime data, create hard gates, change
generation or reranker behavior, or claim reviewed project evidence.

## Evidence Status

The Darkest Dungeon 1 material in this note is `source_mined` or
`design_reference` only. It is useful for vocabulary and candidate structure,
but it is not reviewed project evidence.

Checked references:

- Game Developer, "Game Design Deep Dive: Darkest Dungeon's Affliction System":
  https://www.gamedeveloper.com/design/game-design-deep-dive-i-darkest-dungeon-s-i-affliction-system
- PlayStation Blog, "Madness Awaits You...In the Darkest Dungeon":
  https://blog.playstation.com/2014/12/06/madness-awaits-youin-the-darkest-dungeon/
- Darkest Dungeon Wiki, Stress:
  https://darkestdungeon.fandom.com/wiki/Stress
- Darkest Dungeon Wiki, Affliction:
  https://darkestdungeon.fandom.com/wiki/Affliction
- Darkest Dungeon Wiki, Virtue:
  https://darkestdungeon.fandom.com/wiki/Virtue
- Darkest Dungeon Wiki, Heart attack:
  https://darkestdungeon.fandom.com/wiki/Heart_attack

## Executive Readout

Darkest Dungeon 1's stress loop is not a normal debuff stack. It is a visible
pressure track that turns repeated tactical and expedition choices into a
threshold event. At 100 stress, a hero is tested and branches into a mostly
negative affliction outcome or a rarer positive virtue outcome. That result
then changes combat control, party stability, recovery cost, and the hero's
emergent story.

The important transferable structure is:

1. stress is accumulated through many small, legible sources,
2. mitigation exists but costs tempo, supplies, roster time, or safety,
3. the 100 stress threshold creates suspense because players can see it coming,
4. the branch is asymmetric but not purely deterministic,
5. negative breaks create team contagion and long-tail cost,
6. positive breaks create reversal, relief, and role identity,
7. the loop continues after the break through recovery and future risk.

The non-transferable part is the exact DD1 tuning, vocabulary, and punitive loss
of control. Those belong to DD1's gothic roster-management fantasy and should
not be copied directly into this project's card, campaign, or exam systems.

## Mechanical Skeleton

### Stress Buildup

DD1 stress is a second damage track beside HP. It builds through combat and
expedition pressure:

- stress attacks and monster critical strikes,
- entering and traversing dungeons,
- low light and darkness,
- traps, curios, hunger, missing supplies, and obstacles,
- prolonged fights,
- seeing allies reach Death's Door or die,
- retreating from bad situations,
- quirks and trinket drawbacks.

This matters because stress is not one source. It is a cumulative environmental
and tactical readout. The player can reduce some sources with torches, scouting,
stress-heal skills, camping, fast target priority, and supply planning, but
each answer competes with money, inventory, tempo, damage output, or risk.

### Relief And Recovery

Stress can be reduced during a quest by specific skills, camping skills,
critical hits, kills, trap disarms, certain curios, and other class-specific
tools. The main reliable recovery happens in town through Abbey/Tavern stress
relief or passive weekly reduction.

This makes relief a strategic cost, not a free cleanse. A stressed hero may be
unavailable for a week, occupy a limited town slot, cost gold, or return with
side effects. Stress therefore crosses the boundary between fight tactics and
roster planning.

### The 100 Stress Check

The stress bar runs from 0 to 200 and has a major threshold at 100. When a hero
reaches that threshold, their resolve is tested. The base outcome is commonly
described as 25% virtue chance versus 75% affliction chance, with modifiers
from level mismatch, trinkets, quirks, and other effects.

The check is dramatic because it is:

- visible: the player watches the bar approach the line,
- earned: many prior choices pushed the hero closer or kept them safe,
- uncertain: the result is not known until the moment resolves,
- asymmetric: the likely outcome is bad, but the positive outcome is real,
- public: the whole party may be affected by either result,
- persistent: the state does not vanish like a one-turn debuff.

The presentation also matters. The game treats the check as a banner/splash
moment, not as a silent modifier update. The system tells the player: this is a
turning point in the story of this expedition.

### Affliction Branch

Affliction is the common negative break. It applies penalties and changes the
hero's behavior mode. Afflicted heroes may act out, move, pass, use random
skills, attack allies or themselves, refuse healing, refuse camping skills,
refuse food, interact with curios, bark at allies, and spread stress.

Several design features make affliction stronger than a normal debuff:

- The player loses partial command reliability, not just stats.
- The party receives stress from barks and behavior, so one break can push
  another hero toward a break.
- Formation, healing, camping, supplies, retreat, and curio decisions all
  become less reliable.
- Stress keeps rising after affliction.
- At 200 stress, an afflicted hero suffers a heart attack, dropping to Death's
  Door or dying if already there.
- Recovery often consumes town time, gold, and roster slots.
- Affliction history can bias future state identity, helping heroes develop
  repeated personal patterns.

The result is a cascade model: stress creates affliction, affliction creates
more stress and control failure, control failure creates more tactical danger,
and tactical danger creates more stress.

### Virtue Branch

Virtue is the rarer positive break. It turns the same threshold from collapse
into resilience. A virtuous hero is set down to about 45 stress, grants party
stress relief, gains positive stats or resistance, and may trigger helpful
start-of-turn effects such as self-healing, stress relief, or party buffs.

Virtue works because it is not a generic reward chest. It is a reversal at the
same point where the player expected collapse. The hero appears to reveal
strength under pressure. That makes the event mechanically useful and
narratively sticky.

Virtue also changes risk calculations:

- A player near 100 stress might keep pushing if they can tolerate affliction
  and has enough upside from a possible virtue.
- Virtue trinkets and stress control can support deliberate risk builds.
- A virtuous hero can stabilize the party and justify continuing an expedition.
- The positive outcome softens the cruelty of the system without removing fear.

### The 200 Stress Endpoint

The 200 stress line turns unresolved affliction pressure into lethal danger.
For afflicted heroes, heart attack moves the hero to Death's Door and resets
stress downward; if already at 0 HP, the hero dies. In base DD1, a virtuous
hero reaching 200 stress loses virtue and resets stress instead.

This second endpoint makes the loop more than one threshold. The 100 check
changes the state of play; the 200 endpoint asks whether the player can still
recover before state failure becomes death or near-death.

## Decision Effects

### Before 100 Stress

The player decides whether to:

- spend actions on stress healing or damage,
- kill stress casters first,
- use torches and supplies now or save them,
- camp early or preserve camping for later,
- retreat before the check,
- accept low-light reward pressure,
- bring trinkets that increase virtue chance or reduce stress,
- stall a fight for recovery and risk reinforcements.

The threshold is dramatic because these decisions do not merely optimize a
number. They decide whether the expedition reaches a psychological crisis.

### After Affliction

The player shifts from optimization to damage control:

- keep fighting with unreliable command,
- protect an afflicted hero from heart attack,
- decide whether an afflicted party member is now a liability,
- spend scarce recovery on one hero while others keep rising,
- retreat and accept campaign/roster stress,
- continue because quest progress is too valuable to abandon.

### After Virtue

The player reassesses risk upward:

- continue deeper,
- rely on the hero's buff or stress relief,
- use the reversal as a bridge through a boss or final hallway,
- accept that virtue expires and does not permanently solve roster stress.

## Why This Is Not A Normal Debuff

A normal debuff changes values inside an encounter. DD1's stress loop changes
the player's relationship to the party.

Key differences:

- It has buildup, threshold, branch, state, cascade, and recovery phases.
- It combines encounter tactics with expedition planning and town economy.
- It affects agency by making characters partially unreliable.
- It makes party psychology contagious.
- It gives negative and positive outcomes narrative identity.
- It persists long enough to create roster and memory consequences.
- It stays legible through a visible meter while preserving outcome suspense.

The phrase "psychological state cycle" is more accurate than "debuff." The
cycle is:

```text
pressure source -> visible stress -> mitigation choice -> threshold check ->
virtue or affliction -> party/state consequences -> recovery or escalation ->
future roster memory
```

## Transferable Structures

These structures can inform future project work:

- A visible non-HP pressure track that can be read as accumulated ordeal.
- Multiple small stress sources rather than one scripted crisis trigger.
- Threshold drama where the player can see danger coming.
- A rare positive break that is strong enough to become a story.
- A common negative break that changes behavior, not just numbers.
- Team contagion as a soft cascade, provided the player has counterplay.
- Recovery windows with real opportunity cost.
- Long-term consequence that affects future planning without becoming a hard
  progression gate.
- Character-specific response memory or identity tags, if kept advisory and
  human-reviewed.
- Evaluation dimensions that judge agency preservation, recovery, contagion,
  and threshold presentation separately.

## Structures Not To Copy Directly

Do not copy these into the project as-is:

- DD1's exact 100/200 thresholds or 25/75 base split.
- DD1's gothic affliction names, mental-health framing, or clinical-adjacent
  labels.
- Full loss-of-control act-outs if the project needs more deterministic exam
  readability.
- Hard fail gates based on a stress result.
- Runtime campaign curve changes from this research note.
- Automatic card generation, runtime data, or reranker behavior.
- Source-mined DD1 facts as reviewed evidence.
- Cascades that punish the player without visible mitigation or exit choices.

## Evaluation Dimensions For Future Model Work

The future `virtue_affliction_design_model_v1` should evaluate at least these
dimensions:

| Dimension | Question |
| --- | --- |
| `stress_buildup` | Are pressure sources legible, varied, and connected to player choices? |
| `threshold_drama` | Does the threshold create anticipation, presentation, and consequence? |
| `positive_break` | Can the rare good outcome create a real reversal without trivializing risk? |
| `negative_break` | Does the bad outcome change play meaningfully without becoming pure helplessness? |
| `team_contagion` | Can one character's state pressure the team in a readable, recoverable way? |
| `long_term_consequence` | Does the result matter beyond one turn without becoming a grind tax? |
| `agency_preservation` | Does the player retain enough planning, mitigation, and recovery control? |
| `recovery_window` | Are there mid-run and between-run ways to respond with meaningful cost? |
| `state_identity` | Do outcomes feel like character states rather than anonymous modifiers? |
| `risk_reward_tuning` | Is pushing toward the threshold sometimes rational, not always wrong? |
| `anti_debuff_depth` | Does the loop include buildup, branch, cascade, and recovery phases? |
| `authority_safety` | Is the output advisory only, with no hard gate or runtime mutation? |

## Positive Gameplay Patterns

- Visible pressure clock with multiple mitigation levers.
- Threshold check that becomes a scene, not a quiet stat update.
- Negative break that changes command reliability, party stress, and recovery
  planning.
- Positive break that turns pressure into heroism and supports comeback play.
- Recovery that costs actions, camping points, town slots, gold, or future
  roster availability.
- Party contagion that is strong enough to matter but still has counterplay.
- Character memory that makes repeated responses feel like emerging biography.

## Counterexample Patterns

- Hidden random debuff with no visible pressure buildup.
- Threshold result that only says `-20% stat` and leaves the loop unchanged.
- Failure cascade with no retreat, recovery, prevention, or partial value.
- Positive break that is so common or strong that players farm it by default.
- Negative break that removes agency so completely that decisions stop
  mattering.
- Long-term consequence that only creates busywork treatment with no strategic
  tradeoff.
- Directly importing DD1 labels and numbers without adapting to this project's
  tone, readability, and authority boundaries.

## Relationship To Existing Project Work

This report sits next to `stress_resolve_model_v1` as research input. It does
not replace that model, register a new capability graph node, or change any
default entrypoint.

The follow-up design surface is `virtue_affliction_design_model_v1`. That
contract keeps this DD1 research in the same document family while adding:

- a report-only mathematical state model,
- advisory metric definitions,
- player decision EV sketches,
- a cardanalysis-style partial-order view,
- proposed future graph nodes and edges.

The model is still DD1-only. It does not use DD2 relationship/affinity systems
as evidence or design input.

If future work promotes `virtue_affliction_design_model_v1` beyond a draft, it
should remain report-only first and declare whether it consumes:

- normalized case input,
- stress/resolve summaries,
- campaign power-curve reports,
- human-reviewed project design notes.

Any such future promotion should preserve `advisory_context_only` until a
separate reviewed process explicitly changes authority.
