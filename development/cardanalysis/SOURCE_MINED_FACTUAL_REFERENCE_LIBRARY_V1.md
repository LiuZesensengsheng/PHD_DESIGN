# Source-Mined Factual Reference Library V1

- Library: `source_mined_factual_reference_library_v1`
- Contract: `cardanalysis_case_input_v1`
- Status: low-authority external fact reference library
- Runtime impact: none

## Purpose

This library stores factual, source-mined references from public game resources
so future `cardanalysis` reports can reason from concrete examples without
pretending the examples are reviewed project evidence.

The library is intentionally evidence-only. It does not define official project
cards, enemies, campaign pacing, mechanics, package rules, or UI behavior.

## Source Boundary

All V1 cases in this library use:

- `source.source_type = "source_mined_reference"`
- `source.evidence_tier = "source_mined"`
- `source.review_status = "unreviewed_reference"`
- `authority.authority_boundary = "advisory_context_only"`

Every case must include a public `source_url` when available and must forbid
`reviewed_evidence_claim`.

## Batch 1 Coverage

The first batch uses public Slay the Spire Wiki pages as mechanical-fact
references. It covers:

- card-count anti-spam pressure;
- boss passive chip and damage-cap pressure;
- status insertion and deck pollution;
- temporary card generation;
- exhaust package enablers and fail-state risk;
- block retention payoff;
- poison burst payoff;
- draw/cost randomization;
- hand retention and hand-clog pressure;
- card-play limit curses;
- boss split and rebirth phases;
- summoned-minion pressure;
- multi-hit and wound-pressure encounters.

These cases are useful as source-aware examples for future review packets, not
as design authority.

## Batch 2 Coverage

The second batch continues public Slay the Spire Wiki factual references with a
card-package emphasis. It covers:

- exhaust payoff chains;
- status/curse payoff and relief;
- Shiv generation and support-density payoff;
- passive poison clocks;
- temporary defensive spikes with delayed costs;
- first-card repeat sequencing;
- ongoing power generation;
- focus spike decay;
- repeat-density scaling;
- zero-cost recursion;
- discard retrieval;
- draw-pile search plus double-play payoff.

These are still source-mined facts only. They do not promote package ratios,
formal card text, card pools, status runtimes, or search behavior.

## Batch 3 Coverage

The third batch shifts toward enemy pressure and campaign-phase examples:

- early elite preparation windows and debuff clocks;
- boss status pollution;
- temporary card loss through minions;
- charged boss defense checks;
- boss minion summons and debuff layers;
- summon caps and summon-board scaling;
- health-threshold execute pressure;
- starter boss mode shifts;
- attack-driven intent volatility.

These cases are external factual references for future review questions. They
do not define project enemy data, monster stats, runtime AI, boss phases, or
campaign pacing.

## Batch 4 Coverage

The fourth batch returns to card and package mechanics with public Slay the
Spire Wiki factual references. It covers:

- draw-lock plus cost-reset burst turns;
- selected retain and cross-turn hand planning;
- discard enablers and unplayable discard payoffs;
- delayed copy generation and topdeck discount planning;
- next-card repeat effects across Skill, Power, and Attack examples;
- card-to-energy and stored-resource cashout;
- energy or draw now with future Void/Burn pollution;
- high-cost payoff support-ratio pressure.

These cases remain source-mined and unreviewed. They do not define formal card
data, package ratios, runtime copy logic, status runtime, energy rules, or
default synthesis behavior.

## Batch 5 Coverage

The fifth batch completes the first `80` source-mined factual reference target.
It uses public Slay the Spire Wiki references for Defect and Watcher mechanics:

- Orb-slot capacity, Focus tradeoffs, and first-Orb passive repeat;
- unique-Orb draw payoff and Frost-draw glue;
- draw-pile-size energy, pure draw, and targeted draw-pile search;
- Scry topdeck filtering;
- Wrath-entry draw and retain-cost payoff;
- fatal-kill deck upgrade reward bridges;
- extra-turn timing and ramping energy;
- Block/Scry and Attack/Scry/Draw multi-role glue.

These cases stay low-authority source-mined facts only. They do not define
formal card text, runtime timing, Orb rules, Scry UI, campaign reward policy,
hard gates, learned paths, or default synthesis behavior.

## Validation

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/source_mined_factual_reference_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_source_mined_factual_reference_library_v1.py -q
```
