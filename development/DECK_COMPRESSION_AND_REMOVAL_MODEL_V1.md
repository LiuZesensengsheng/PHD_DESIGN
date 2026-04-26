# Deck Compression And Removal Model V1

## Purpose

This document defines how cardanalysis should evaluate deck compression, starter
card pollution, removal access, transform risk, and in-combat compression for
`STS1`-style mechanism viability.

The immediate target is a design specification, not a behavior change. It should
guide a later report-only V1 payload that makes removal and compression assumptions
visible when the system claims a loop, exactness payoff, or precision engine can
come online.

## Scope

In scope:

- `deck_compression_requirement`
- `starter_pollution_tolerance`
- `removal_access_dependency`
- `in_combat_compression`
- `combo_assembly_cost`
- `deck_size_sensitivity`
- `starter_strike_defend_drag`
- `removal_vs_transform_vs_exhaust`
- how these signals affect mechanism-online and infinite-reachability claims

Out of scope for this document:

- changing `mechanism_axis_contracts.py`
- adding fixtures
- changing hard benchmark gates
- changing current fast loop or fast draft scoring behavior
- making learned/modelized ranking own legality or benchmark pass/fail

## Current System Surface

The current cardanalysis stack already has useful adjacent signals:

- `dead_card_pressure` identifies cards that look dead because payload cards lack
  package support, prerequisites, or mapped behavior.
- `mechanism_axis` viability covers support density, payoff reachability, trigger
  availability, glue density, repeatability, cross-support quality, and shell purity.
- `resource_window.compression_score` models cost and hand-resource compression such
  as zero-cost cards, resource gain, cost-shape windows, and selection support.
- `FastDraftSessionInput.discard_policy=auto_worst` can remove one current deck card
  from an allowed pool when doing so improves the fast snapshot quality.
- STS fixture and catalog notes already expose exactness, zero-cost density, discard
  timing, vulnerable uptime, and loop-frequency projection gaps.

Those capabilities are not the same as a Slay the Spire shop/event/card-removal
model. In particular:

- `dead_card_pressure` is a local deck-quality symptom, not a route model for paying
  to remove starter cards.
- `auto_worst` is an opt-in draft rule with a supplied candidate pool; it does not
  model shop removal availability, event probability, transform outcomes, opportunity
  cost, or the fact that many runs cannot remove every bad starter card before the
  combo would need to work.
- `resource_window.compression_score` is mostly in-fight cost/hand compression, not
  persistent deck thinning.
- Mechanism-axis fixtures often use curated deck-case cards. They are useful for
  identifying the mechanism shape, but they can overstate run accessibility when they
  skip the cost of removing starter Strike and Defend cards.

The main gap is therefore not "the system cannot see bad cards." The gap is that it
does not yet price the path from a real starter deck to the compact deck that many
loops and exact mechanisms require.

## Core Judgment

Many `STS1` loops are not merely "card A plus card B." They are "card A plus card B
in a deck thin enough that starter cards no longer interrupt the line."

When a curated case omits the starter deck drag, the evaluator may correctly identify
that the final shell is coherent while still overestimating how reachable that shell
is in a normal run. The future V1 model should therefore separate:

1. final-shell viability, which current mechanism-axis work already estimates
2. assembly and compression burden, which this document specifies
3. route dependency, meaning whether shops, events, transforms, or in-combat exhaust
   are required before the final-shell claim should be trusted

## Evaluation Fields

All fields should be report-only in the first implementation. Scores use `0.0` to
`1.0`, where higher usually means more of the named pressure or dependency unless
the field says otherwise.

| Field | Meaning | High Value Means |
| --- | --- | --- |
| `deck_compression_requirement` | How much persistent deck thinning or effective thinning is required before the mechanism is reliable. | The mechanism should be downgraded unless removal, transform, or exhaust support is visible. |
| `starter_pollution_tolerance` | How many starter/baseline cards the shell can carry without losing its line. | The mechanism tolerates more Strike/Defend drag before reliability falls. |
| `removal_access_dependency` | How dependent the shell is on out-of-combat removal access. | The shell is route-dependent and should not be treated as generally reachable from a starter deck. |
| `in_combat_compression` | How much the deck can thin itself during combat through exhaust, single-use cards, zero-cost recursion, selection, or hard discard cycling. | The shell has internal tools to compensate for a thicker starting deck. |
| `combo_assembly_cost` | Piece count, setup turns, energy/card draw tax, upgrades, relic assumptions, and state prerequisites required before the line is online. | The mechanism is slower or more brittle than final-shell density alone suggests. |
| `deck_size_sensitivity` | How sharply reliability falls as deck size grows. | Extra cards, especially basics, should strongly penalize reachability. |
| `starter_strike_defend_drag` | Specific drag from basic Strike and Defend cards, separated from generic dead-card pressure. | Starter basics are actively delaying or breaking the mechanism. |
| `removal_vs_transform_vs_exhaust` | Classification of which compression tools are valid for this mechanism and which ones only look equivalent. | The evaluator can explain why a route helps or fails to help. |

### `deck_compression_requirement`

This should estimate the number and quality of card slots that must be cleared before
a mechanism claim becomes credible.

Recommended V1 labels:

- `none`: normal deck growth does not materially hurt the plan.
- `low`: the plan appreciates trimming but can run through a normal deck.
- `medium`: the plan needs either multiple removals or meaningful in-combat thinning.
- `high`: the plan needs a compact deck, repeated draw, or precise card-flow control.
- `extreme`: the plan is an infinite or exactness payoff that should be treated as
  route-dependent unless strong compression evidence exists.

Signals that raise the requirement:

- infinite or near-infinite loop claims
- exact draw-pile or exact hand-size claims
- payoff cards that only work when redrawn repeatedly
- zero-cost recursion that needs a high ratio of eligible cards
- repeated evidence notes such as `infinite_line_frequency_not_measured`,
  `draw_pile_exactness_requirement_not_benchmarked`, or
  `zero_cost_density_breakpoint_not_benchmarked`

Signals that lower the requirement:

- redundant draw and selection
- self-exhausting setup cards
- repeatable in-combat exhaust that targets unwanted cards
- strong retain or deck-order control
- robust payoff that does not need repeated exact redraw

### `starter_pollution_tolerance`

This should answer: "How many starter basics can remain before the mechanism is no
longer reliable?"

Recommended V1 labels:

- `high`: starter cards are mostly acceptable filler or defensive buffer.
- `medium`: a few basics are acceptable, but excess basics slow the engine.
- `low`: basics are usually bad draws once the plan tries to go online.
- `near_zero`: the deck wants almost no irrelevant basics during the key loop window.

Important distinction:

- Low tolerance does not mean the shell is bad.
- It means the shell has a high assembly burden and must earn its online claim through
  removal access, transform quality, or in-combat compression evidence.

### `removal_access_dependency`

This should model persistent out-of-combat card removal, not draft-time `auto_worst`.

Recommended V1 payload components:

- `required_removal_count`: estimated number of basics or off-plan cards that must
  leave the deck before the mechanism is reliable.
- `removal_priority`: ordered card classes, usually `starter_strike`,
  `starter_defend`, `curse_status`, `off_axis_card`, or `expensive_payoff`.
- `access_kinds`: `shop`, `event`, `neow_bonus`, `relic`, `unknown`, or `not_needed`.
- `opportunity_cost`: whether using removal competes with buying the core card,
  buying support, upgrading, healing, or taking a relic.
- `route_risk`: `low`, `medium`, `high`, or `unknown`.

V1 should avoid pretending exact path probability is known. The first useful step is
to make the dependency explicit:

```json
{
  "removal_access_dependency": {
    "dependency_score": 0.82,
    "required_removal_count": 4,
    "removal_priority": ["starter_strike", "starter_defend"],
    "access_kinds": ["shop", "event"],
    "opportunity_cost": "high",
    "route_risk": "high",
    "notes": [
      "basic_removal_required_before_loop_claim",
      "curated_deck_skips_removal_cost"
    ]
  }
}
```

### `in_combat_compression`

In-combat compression is not the same as removal. It can make a thick deck behave
like a thinner deck after setup, but it has its own costs.

V1 should separate:

- `persistent_exhaust`: removes cards for the rest of the combat.
- `single_use_exhaust`: powers/skills that exhaust themselves after use.
- `targeted_exhaust`: can choose bad cards or specific fuel.
- `bulk_exhaust`: clears hand classes but may hit important cards.
- `discard_filtering`: improves current hand quality but does not thin future cycles.
- `draw_selection`: finds pieces but does not remove pollution by itself.
- `zero_cost_recursion`: effectively compresses energy and draw when the eligible
  card ratio is high enough.

The evaluator should report both benefit and tax:

- setup turn cost
- card draw spent finding the compressor
- energy cost
- risk of exhausting the wrong card
- whether compression arrives before the key loop needs to start

### `combo_assembly_cost`

This field should price the path from "cards exist in the deck" to "the mechanism is
online."

Inputs:

- number of required core cards
- number of support cards required before payoff
- upgrades required for cost breakpoints
- enemy-state prerequisites such as Vulnerable
- self-state prerequisites such as Calm/Wrath stance
- draw/retain/search needed to align pieces
- first-cycle survival tax
- removal or transform count needed before the combo is reliable

Suggested labels:

- `simple`: one or two pieces, little timing pressure
- `moderate`: several pieces or setup turn, but redundancy exists
- `high`: exact state or support density required
- `extreme`: infinite/exactness line that is not credible without compression proof

### `deck_size_sensitivity`

This should penalize mechanisms whose reliability falls sharply with each added card.

High sensitivity examples:

- Rushdown infinites
- Dropkick infinites
- Grand Finale exactness
- All for One chains with low zero-cost density
- Silent discard loops that need repeated Tactician/Reflex contact

Lower sensitivity examples:

- frontload packages with redundant attacks
- block engines with many defensive substitutes
- poison plans with multiple poison and stall sources
- orb/focus control plans that do not need exact repeated redraw

V1 does not need a full probability model. It should start by reporting:

- `observed_deck_size`
- `starter_basic_count`
- `off_plan_card_count`
- `estimated_safe_extra_cards`
- `sensitivity_label`

### `starter_strike_defend_drag`

Starter Strike and Defend cards deserve their own signal because they are not just
generic low-value cards:

- They are present at run start and must be removed, transformed, exhausted, or drawn
  through.
- Strike and Defend have different drag profiles.
- Some mechanisms specifically care about basic attacks or block cards.

Recommended V1 subfields:

```json
{
  "starter_strike_defend_drag": {
    "drag_score": 0.74,
    "starter_strike_count": 4,
    "starter_defend_count": 4,
    "strike_drag_label": "loop_interrupt",
    "defend_drag_label": "draw_slot_pollution",
    "exceptions": [],
    "notes": [
      "strike_output_does_not_advance_engine",
      "defend_blocks_but_breaks_redraw_loop"
    ]
  }
}
```

Strike drag tends to matter when:

- the deck no longer needs low-output attacks
- attack draws compete with loop pieces
- enemy-state setup is already solved by better attacks or powers
- the shell is not a Strike-matters exception

Defend drag tends to matter when:

- defensive basics do not advance the engine
- the deck has better block conversion
- precise draw order matters
- a loop requires every redraw to replace itself

Known exceptions should be explicit. Perfected Strike, Strike Dummy, early-act survival,
and some block-conversion plans can temporarily value starter basics. The evaluator
should not blindly mark every starter card as pollution.

## Removal Vs Transform Vs Exhaust

These three tools should never be collapsed into one "card went away" bucket.

| Tool | Persistent? | Adds Replacement? | Main Value | Main Risk |
| --- | --- | --- | --- | --- |
| Removal | Yes | No | Permanently reduces deck size and pollution. | Route/currency opportunity cost. |
| Transform | Yes | Yes | Removes a specific bad card and may create upside. | Replacement can be off-plan, high-cost, or another loop interrupt. |
| Exhaust | Combat only unless card text says otherwise | No | Thins the current combat and can enable exhaust payoffs. | Must be drawn and played; may arrive late or consume key cards. |

V1 should classify each mechanism's acceptable compression sources:

- `requires_removal`: only persistent thinning makes the online claim credible.
- `transform_ok_if_low_cost_or_on_axis`: transform helps only when the replacement is
  aligned with the shell.
- `exhaust_ok_if_targeted_and_early`: in-combat exhaust helps only when it can remove
  pollution before the loop window.
- `discard_is_not_compression`: discard filtering helps current hand quality but does
  not remove the same card from the next shuffle.
- `self_exhaust_setup_counts`: powers and one-shot skills that exhaust themselves can
  reduce later deck size after setup.

## Payload Draft

Future V1 should attach a report-only payload next to fast-card or mechanism-axis
output. The exact dataclass names can be decided later, but the payload shape should
be stable enough for fixtures and reports to reason about.

```json
{
  "deck_compression_model": {
    "contract_version": "deck_compression_and_removal_v1",
    "evaluation_mode": "report_only",
    "deck_context": {
      "observed_deck_size": 12,
      "starter_strike_count": 3,
      "starter_defend_count": 4,
      "starter_other_count": 1,
      "known_removed_cards": [],
      "known_transformed_cards": [],
      "compression_cards": ["burning_pact"],
      "route_assumption": "unknown"
    },
    "signals": {
      "deck_compression_requirement": {
        "score": 0.86,
        "label": "extreme",
        "reason_codes": ["infinite_claim", "repeat_redraw_required"]
      },
      "starter_pollution_tolerance": {
        "score": 0.12,
        "label": "near_zero",
        "reason_codes": ["basic_draws_break_loop"]
      },
      "removal_access_dependency": {
        "dependency_score": 0.80,
        "required_removal_count": 4,
        "removal_priority": ["starter_strike", "starter_defend"],
        "access_kinds": ["shop", "event", "unknown"],
        "opportunity_cost": "high",
        "route_risk": "high"
      },
      "in_combat_compression": {
        "score": 0.48,
        "sources": ["targeted_exhaust", "single_use_exhaust"],
        "taxes": ["must_draw_compressor", "setup_turn_cost"]
      },
      "combo_assembly_cost": {
        "score": 0.78,
        "label": "high",
        "pieces": ["payoff", "state_prerequisite", "draw_bridge", "compression"]
      },
      "deck_size_sensitivity": {
        "score": 0.90,
        "label": "high",
        "estimated_safe_extra_cards": 1
      },
      "starter_strike_defend_drag": {
        "drag_score": 0.74,
        "strike_drag_label": "loop_interrupt",
        "defend_drag_label": "draw_slot_pollution"
      },
      "removal_vs_transform_vs_exhaust": {
        "valid_sources": ["removal", "targeted_exhaust"],
        "conditional_sources": ["transform"],
        "invalid_equivalences": ["discard_filtering_is_not_persistent_thinning"]
      }
    },
    "reachability_adjustment": {
      "mechanism_online_claim": "downgrade_without_route_evidence",
      "infinite_reachability": "route_dependent",
      "notes": ["curated_deck_may_skip_starter_removal_cost"]
    }
  }
}
```

## Archetype Analyses

### Dropkick

Current evidence:

- Existing loop fixtures use Dropkick as a loop/threshold boundary.
- Dropkick itself is Vulnerable-gated draw and energy refund.
- Burning Pact and Pommel Strike can act as draw/compression bridges.

Compression judgment:

- `deck_compression_requirement`: high to extreme for infinite claims.
- `starter_pollution_tolerance`: low. Basics interrupt the repeated draw/refund line.
- `removal_access_dependency`: high unless the deck has strong targeted exhaust and
  enough draw to thin during combat.
- `in_combat_compression`: meaningful when Burning Pact, True Grit-style effects, or
  other exhaust tools remove off-plan cards early enough.
- `combo_assembly_cost`: high because the deck needs Vulnerable uptime, redraw, energy
  replacement, and a compact cycle.
- `deck_size_sensitivity`: high. Each extra non-loop card reduces repeat contact with
  Dropkick and the Vulnerable/draw bridge.
- `starter_strike_defend_drag`: high. Strike is redundant low output; Defend can buy
  time but does not replace itself and breaks the loop window.

Interpretation:

The current mechanism-axis layer can tell the difference between a closed Dropkick
loop and an almost-loop. It should not, by itself, claim that a run can reach the
closed loop from a starter deck without pricing basic-card removal or early exhaust
access.

### Rushdown

Current evidence:

- Existing watcher loop fixtures use Rushdown as a closure threshold.
- The positive shell is recognized as a strong low-variance infinite once assembled.

Compression judgment:

- `deck_compression_requirement`: extreme for infinite claims.
- `starter_pollution_tolerance`: near zero once the infinite line is supposed to run.
- `removal_access_dependency`: very high because Watcher infinites usually need a
  very small deck or overwhelming draw/stance redundancy.
- `in_combat_compression`: usually weaker than Ironclad exhaust lines unless the deck
  has specific one-shot setup, scry, draw, or retain tools that effectively clear the
  loop window.
- `combo_assembly_cost`: high to extreme because Rushdown must align with stance
  entry/exit, Calm/Wrath transitions, draw, and often upgrades or cost breakpoints.
- `deck_size_sensitivity`: extreme. Extra basics are not just weak; they stop the
  repeatable draw chain from replacing itself.
- `starter_strike_defend_drag`: very high except during early survival. Strike and
  Defend do not create stance transitions, do not draw through Rushdown, and do not
  sustain the loop.

Interpretation:

Rushdown is the clearest example where final-shell viability can be true while
run-level reachability is overestimated. The evaluation layer must require either
removal evidence or a named effective-compression route before treating the infinite
as generally reachable.

### Grand Finale

Current evidence:

- Existing mechanism-axis fixtures treat Grand Finale exactness as a negative gap
  against repeatable draw-discard engines.
- The deck-fun case preserves the fun spike but marks it as low-strength because
  exact sequencing and matchup brittleness remain severe.

Compression judgment:

- `deck_compression_requirement`: high to extreme. The shell needs draw-pile
  exactness, not merely a lot of draw.
- `starter_pollution_tolerance`: low. Every irrelevant card changes pile size and
  alignment, even when the card is not dead in ordinary fights.
- `removal_access_dependency`: high when the claim is "reliable Finale engine" rather
  than "occasional spectacular payoff."
- `in_combat_compression`: useful only if it creates controlled pile size and order.
  Random or late exhaust can make exactness worse.
- `combo_assembly_cost`: extreme because the line requires draw, discard, retain,
  pile-size control, and survival during setup.
- `deck_size_sensitivity`: extreme. Deck size and modulo/exactness constraints are
  central to the payoff.
- `starter_strike_defend_drag`: high. Basics may be playable, but they distort draw
  count and pile alignment.

Interpretation:

Grand Finale should not be promoted from "exactness gap" to "online mechanism" unless
the payload shows explicit deck-size control, retain/draw ordering, and removal or
controlled exhaust assumptions. Transform is especially risky because the replacement
may be generically better while still ruining exactness.

### All for One / Claw

Current evidence:

- `zero_cost_claw` is listed as a missing family because Claw, All for One, Scrape,
  and zero-cost recursion are not owned by the current `orb_control` axis.
- Existing deck-fun cases distinguish a beloved but brittle Claw recursion shell from
  a stronger All for One zero-cost loop shell.

Compression judgment:

- `deck_compression_requirement`: medium to high. The shell can tolerate more deck
  size than exact infinites if zero-cost density is high, but it suffers when basics
  crowd out eligible cards.
- `starter_pollution_tolerance`: medium-low. Starter basics are not returned by
  All for One and make Scrape-style cards less reliable.
- `removal_access_dependency`: medium. Removal helps, but adding enough zero-cost
  support can sometimes be as important as deleting every basic.
- `in_combat_compression`: moderate. Zero-cost recursion is effective compression
  only when the deck has enough eligible targets and draw to find All for One.
- `combo_assembly_cost`: high for the strong shell because it needs All for One,
  enough zero-cost cards, draw, artifact/defense answers, and enough scaling to make
  Claw matter before slow fights punish the setup.
- `deck_size_sensitivity`: medium-high. The shell is ratio-sensitive more than
  absolute-size-sensitive.
- `starter_strike_defend_drag`: medium to high. Defend can still be useful for
  survival, but both Strike and Defend dilute Scrape and All for One turns.

Interpretation:

This family needs a zero-cost density and recursion payload, not a generic loop claim.
Removal should improve the claim, transform should only help if the replacement is
zero-cost or on-axis, and exhaust should be counted only when it clears non-zero-cost
pollution before recursion turns.

### Silent Discard Loop

Current evidence:

- Existing draw/discard and discard-cycle fixtures separate real repeatable discard
  engines from raw draw piles, hand dumps, and exact-payoff traps.
- Tactician, Reflex, Acrobatics, Prepared, Calculated Gamble, Concentrate, and related
  cards create a real resource and draw loop when the ratios are correct.

Compression judgment:

- `deck_compression_requirement`: medium to high. The shell needs enough discard
  outlet/payoff contact, but discard filtering can carry some extra cards.
- `starter_pollution_tolerance`: medium-low. Silent can filter basics better than some
  classes, but starter cards still occupy draw/discard slots and reduce payoff contact.
- `removal_access_dependency`: medium. Removal is important for precision loops, less
  absolute for broader discard value shells.
- `in_combat_compression`: mixed. Discard improves hand quality but does not remove
  cards from future shuffles. Calculated Gamble-style churn is not persistent deck
  thinning unless paired with exhaust or enough draw/payoff density.
- `combo_assembly_cost`: high because the deck needs outlet/payoff ratios, draw,
  energy conversion, and sometimes retain to avoid discarding the wrong half.
- `deck_size_sensitivity`: medium-high for loops, medium for value discard.
- `starter_strike_defend_drag`: medium to high. Strike is usually the first removal
  target after frontload is covered; Defend may remain acceptable until block engines
  or discard block payoffs replace it.

Interpretation:

The current system is good at seeing discard-cycle identity. It still needs a separate
compression layer so a curated Tactician/Reflex loop is not mistaken for a run state
that can be reached without paying the starter-deck cleanup cost.

## Reachability Adjustment Rules

The future evaluator should not overwrite mechanism-axis scores. It should add an
interpretation layer:

- If mechanism viability is high and compression burden is low, keep the online claim.
- If mechanism viability is high and compression burden is high, report
  `online_if_compressed`.
- If infinite or exactness viability is high but removal/compression evidence is
  missing, report `route_dependent_infinite` instead of `generally_reachable_infinite`.
- If a curated fixture omits starter cards, report
  `curated_deck_skips_removal_cost`.
- If in-combat compression exists but arrives late or requires the same pieces as the
  combo, report `compression_tax_competes_with_assembly`.
- If transform is counted, report whether replacement quality is assumed, measured,
  or unknown.

Suggested report labels:

- `final_shell_online`
- `online_if_compressed`
- `route_dependent_online`
- `almost_loop_due_to_pollution`
- `exactness_not_reliable_at_observed_size`
- `compression_evidence_missing`

## Minimal V1 Implementation Plan

1. Add a report-only compression/removal payload below `design_engine` contracts, but
   do not change `mechanism_axis_contracts.py`.
2. Start with deterministic heuristics over known deck card ids, package hints, role
   tags, projection gaps, deck size, and optional supplied starter/removal context.
3. Preserve current fast-card and fast-draft scores; add only notes, report fields,
   or snapshot payload fields in the first implementation.
4. Treat missing removal context as `unknown`, not as zero burden.
5. Add no hard gates until reviewed fixtures exist for at least:
   Dropkick, Rushdown, Grand Finale, All for One/Claw, and Silent discard loop.
6. Calibrate with current mechanism-axis fixtures by checking whether strong final
   shells become `online_if_compressed` when their curated deck cases skip basic-card
   cleanup.
7. Keep learned/reranker paths out of the decision. They can consume exported fields
   later, but explicit contracts should own the reachability wording.

The smallest useful V1 is therefore not a simulator. It is an honesty layer that
prevents final-shell recognition from being mistaken for starter-deck-to-infinite
reachability.
