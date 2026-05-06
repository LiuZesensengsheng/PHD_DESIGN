# Cardanalysis Foundation Axis Taxonomy V1

## Purpose

Define the shared low-level mechanism vocabulary used when designing or reviewing
cards, packages, and candidate mechanism axes.

This document is a design-language layer. It helps reviewers ask better questions
about support axes, resource throughput, and identity risk. No hard gate is created,
and it does not add a scoring rule, synthesis path, registry entry, or formal card
family.

## Authority Boundary

The taxonomy is:

- advisory context only;
- safe input for mechanism-axis discussion, case review, package review, and future
  report-only feature projection;
- not reviewed evidence by itself;
- not legality, promotion, hard-gate, default synthesis, learned, or reranker
  authority.

Canonical authority wording remains:

```text
advisory_context_only
```

## Core Terms

`Foundation axis` means a low-level resource, throughput, or friction axis that many
advanced mechanisms depend on. A foundation axis can be the named mechanism, but only
when the design still creates its own local choices.

`Advanced mechanism` means the named decision loop, fantasy, or package identity that
uses foundation axes. Examples include delayed charge/release, copy exactness,
position redirect, curse pollution, stance switching, summon lifecycle, or threshold
payoff.

`Identity override risk` means the foundation axis is doing the real design work. If
the named mechanism can be replaced with "more draw", "more energy", "more damage", or
"more scaling" without losing the decision loop, the advanced mechanism has been
swallowed.

`Primary-right foundation axis` means a foundation axis is intentionally the named
mechanism. Examples include discard velocity, block engine, draw engine, or exhaust
shells. These are healthy only when they ask axis-specific questions rather than
becoming generic value.

## Canonical Foundation Axis IDs

Use these IDs in docs, normalized case labels, fixture notes, and review packets when
the axis is the relevant low-level design language.

| Axis ID | Design Role | Common Failure Modes | Advanced Mechanism Relationship | Review Questions |
| --- | --- | --- | --- | --- |
| `draw` | Increases hand access and option velocity. | Overdraw clutter, tempo loss, draw-only turns, decision fatigue. | Supports exactness, combo, charge setup, discard, and tutor lines; can become `draw_engine` when access choice is the point. | What converts the extra cards into action? What is the pressure cost of spending a turn drawing? |
| `discard` | Converts hand contents into triggers, filtering, or resource motion. | Empty-hand lock, forced self-tax, outlet density without recovery, payoff-before-fuel mismatch. | Supports discard velocity, graveyard/recall, status cleanup, and hand-shape puzzles; can claim primary identity when discard choice remains local. | Is discard optional and meaningful? What replenishes the hand after an outlet-heavy turn? |
| `energy` | Sets action budget, burst timing, and spend sequencing. | Energy soup, hoarding past the release window, refund loops, false abundance, hard rollback feel. | Supports expensive payoffs, combo turns, charge release, and multi-card turns; can be primary only when spend timing is the decision. | What makes spending now different from spending later? What prevents extra energy from replacing the mechanism? |
| `exhaust` | Removes cards from future cycles or converts one-time material into fuel. | Free thinning, irreversible traps, payoff-only deletion, exhaust as generic compression. | Supports sacrifice, status cleanup, exhaust shells, deck-shaping, and once-per-combat bursts. | What is lost permanently? Does the player understand the future-cycle cost before exhausting? |
| `defense_block` | Buys survival time and creates stabilization windows. | Stall without closure, invulnerable loops, block crowding out progress, defense as generic goodstuff. | Supports delayed payoff, body-slam conversion, retain setup, frost/control, and counterattack mechanisms. | How does survival convert into progress? What pressure breaks pure stall? |
| `damage` | Provides closure, frontload, burst, or payoff release. | Raw rate eclipses the mechanism, unanswerable burst, damage-only goodstuff, no-value fail state. | Often the payoff endpoint for charge, scaling, stance, poison, summon, and exactness. | Is the damage earned by the mechanism? What happens when the payoff misses? |
| `status` | Adds burdens, tags, counters, debuffs, or modifier state that can be paid off or cleaned up. | Hidden tax, mandatory cleanup, unclear owner/lineage, burden cards becoming pure punishment or free fuel. | Supports curse/pollution, poison, self-damage, wound/status packages, and enemy pressure. | Who owns the status, how long does it last, and what makes cleanup a choice? |
| `search_tutor` | Chooses a target card, answer, or zone-specific object instead of relying on random access. | Scripted turns, bullet bloat, reveal/target-zone ambiguity, toolbox overfit. | Supports exactness, combo assembly, silver bullets, delayed payoff, and package consistency. | What is the cost of certainty? What is the fallback when the target is irrelevant? |
| `retain` | Moves a card or state across turns to create planned windows. | Setup-tax tunnel, hoarding, trap turns, retained cards crowding hand texture. | Supports delayed release, exactness, defense setup, stance timing, and burst windows. | What is worth holding, and what pressure makes holding costly? |
| `filter` | Improves selection quality without necessarily increasing total resources. | Fake agency, excessive scry/filter loops, hidden math, filter replacing draw tension. | Supports draw, exactness, stance, tutor, and combo setup while keeping variance readable. | What choice does the filter expose? Does it reduce variance without erasing uncertainty? |
| `compression_removal` | Changes deck density, friction, or future-cycle reliability. | Perfect consistency, frictionless loops, over-removal, deleting all weak texture, compression mistaken for identity. | Supports thin-deck combo, exhaust, transform, tutor, and package-health evaluation. | What friction remains? Does the mechanism still work in a normal deck size? |
| `temporary_generation` | Creates bounded temporary options, cards, objects, or summons. | Execution load, option overload, origin/duration ambiguity, generated options becoming the whole plan. | Supports discover-like choice, summon lifecycle, copy/transform, status creation, and tactical pivots. | How many temporary choices appear, how long do they last, and what keeps them from replacing the core deck? |
| `scaling` | Changes rate over time through strength, focus, counters, stacks, or repeated triggers. | Runaway growth, slow soup, off-axis scaling swallowing identity, no pressure clock. | Supports power/focus, strength, poison, block, damage, summon, and status plans. | What starts the scaling, what caps or pressures it, and what is the payoff window? |

## How Foundation Axes Support Advanced Mechanisms

Advanced mechanisms usually need foundation support in one of five roles:

| Support Role | Meaning | Example Question |
| --- | --- | --- |
| Fuel | Provides the resource needed to try the mechanism. | Does the mechanism have enough draw, energy, or status material to turn on? |
| Access | Helps find the right piece or window. | Is search, filter, retain, or draw doing setup work without deciding the whole route? |
| Safety | Lets the player survive while the mechanism matures. | Does defense/block buy time without becoming a stall-only plan? |
| Conversion | Turns low-level throughput into the named payoff. | What converts discard, exhaust, damage, or scaling into the mechanism's promise? |
| Constraint | Keeps throughput from becoming automatic. | What cap, pressure, decay, cost, or opportunity cost preserves choice? |

## Preventing Identity Swallowing

Use this quick test before treating a candidate as an advanced mechanism:

1. Name the local decision in one sentence.
2. Remove the foundation throughput words from the pitch.
3. Ask whether the same card would still be interesting with average draw, energy,
   damage, defense, and scaling.
4. Compare the candidate against a generic goodstuff version using the same
   foundation axes.
5. Require at least one local failure state that is not simply "numbers were too low".

If the answer is "the card is only interesting because it draws more, makes more
energy, blocks more, deals more damage, or scales harder", the foundation axis is
probably the identity. That can still be valid, but it should be reviewed as a
foundation-primary mechanism such as discard velocity, block engine, draw engine, or
exhaust shell rather than disguised as a new advanced mechanism.

## Card Design And Evaluation Checklist

When reviewing a card or package, ask:

1. Which foundation axes does it touch?
2. Which one, if any, claims primary identity?
3. What advanced mechanism choice remains after those axes are accounted for?
4. What support role does each foundation axis play: fuel, access, safety,
   conversion, or constraint?
5. What turns low-level throughput into payoff?
6. What pressure, cap, decay, cost, or counterplay prevents automatic value?
7. What is the no-value or partial-value fail state?
8. Does the mechanism still read clearly when draw, energy, block, damage, and scaling
   are average rather than exceptional?
9. Does the package need reviewed evidence for a boundary that is currently only
   human-curated or source-mined?

## Relationship To Existing Surfaces

`MECHANISM_AXIS_DISCOVERY_V1` already asks whether foundation axes support or swallow a
candidate mechanism. This taxonomy gives that question a broader design vocabulary,
including status, search/tutor, temporary generation, and compression/removal
boundaries that are not all first-class evaluator semantics.

`MECHANISM_CASE_LIBRARY_V1` may hold advisory normalized cases that illustrate boundary
questions. Those cases remain case-library evidence only and must preserve
`advisory_context_only` authority.

`STS1_CORE_MECHANISM_AXIS_MAP_V1` remains a reviewed family-coverage map. This taxonomy
does not claim new reviewed STS1 family coverage.

## Reviewed Evidence Still Needed

The V1 taxonomy is usable as shared language, but the following still need stronger
reviewed evidence before making robust design-quality claims:

- status owner/lineage cases that separate burden, payoff, and cleanup value;
- search/tutor cases that compare useful certainty against scripted or overfit turns;
- temporary-generation cases with bounded option count, duration, and origin clarity;
- retain/filter cases that distinguish planning from setup-tax tunnels;
- compression/removal cases with deck-size and friction breakpoints;
- energy/scaling cases that show when throughput becomes identity override;
- defense/block and damage cases that connect survival, closure, and pressure without
  collapsing into generic rate.
