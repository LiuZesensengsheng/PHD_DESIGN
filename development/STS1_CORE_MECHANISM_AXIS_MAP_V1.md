# STS1 Core Mechanism Axis Map V1

## Purpose

This map records what the current cardanalysis mechanism-axis layer can evaluate for
`STS1`, what evidence backs that claim, and which core mechanism families are still
missing or only partially represented.

The goal is content capability planning, not stricter architecture governance.

## Scope Boundary

In scope:

- explicit `STS1` mechanism families modeled in
  `tools/combat_analysis/design_engine/mechanism_axis_contracts.py`
- reviewed mechanism-axis viability fixtures under
  `tests/fixtures/combat_analysis/mechanism_axis_viability_v1/`
- reviewed `STS1` holdout fixtures that use `mechanism_axis` intent
- near-term family gaps that would improve design and evaluation coverage

Out of scope:

- treating `STS2` as the same trust tier as reviewed `STS1`
- learned ranking or reranker default paths
- changing legality, schema, hard benchmark gates, or threshold semantics
- claiming a complete archetype taxonomy

## Trust Tiers

| Tier | Meaning | Current Surface |
| --- | --- | --- |
| Explicit contract | Family vocabulary and card-role specs are versioned and imported below `design_studio`. | `9` mechanism families, `7` viability dimensions |
| Reviewed viability | Pairwise reviewed cases check whether a mechanism shell is online, repeatable, and coherent. | `29` cases across all `9` families |
| Reviewed holdout intent | Catalog holdout fixtures use mechanism-axis intent for recovery and ranking pressure. | `62` `STS1` holdout cases across Ironclad, Silent, Watcher, and Defect |
| Project-card assist | Project card-design fixtures verify mechanism-axis ranking behavior in project card pools. | `5` reviewed mechanism-axis cases |
| Not claimed | Named archetypes without explicit family specs and reviewed contrasts. | Missing-axis backlog below |

## Current Evaluation Dimensions

The current evaluator judges mechanism viability through these dimensions:

| Dimension | What It Checks |
| --- | --- |
| `support_density` | Whether the deck has enough support pieces for the named axis. |
| `payoff_reachability` | Whether the payoff can be reached without relying on fantasy draw order. |
| `trigger_availability` | Whether the axis has enough triggers to turn on in real fights. |
| `glue_density` | Whether bridge and setup cards connect the plan instead of only adding value. |
| `repeatability` | Whether the plan can happen repeatedly instead of once. |
| `cross_support_quality` | Whether support pieces reinforce the same plan instead of competing. |
| `shell_purity` | Whether the deck is a coherent shell rather than generic goodstuff or soup. |

## Explicit STS1 Family Coverage

| Family | Character Affinity | Family Cards | Reviewed Cases | Current Capability | Main Open Gap |
| --- | --- | ---: | ---: | --- | --- |
| `exhaust` | Ironclad | 9 | 3 | Separates real exhaust shells and draw bridges from soup, payoff-only, raw draw piles, and non-exhaust loop distractions. | Does not fully own status/wound or self-damage exhaust variants. |
| `draw_engine` | Mostly Silent, cross-character utility | 12 | 3 | Separates repeatable draw support from raw draw piles and exact-payoff traps. | Grand Finale-style exactness is tested as a negative gap, not a positive axis. |
| `discard_cycle` | Silent | 10 | 2 | Separates repeatable discard/resource conversion from payoff-only or one-shot hand dumps. | Needs thicker mid-strength cases for Reflex/Tactician density, Sneaky Strike, and Concentrate tradeoffs. |
| `loop` | Cross-character, especially Ironclad/Watcher | 24 | 4 | Detects loop closure, almost-loop failure, threshold gaps, and draw-bridge density. | Strength, block, Sundial, and stance infinites are partially adjacent, not separate owned axes. |
| `orb_control` | Defect | 14 | 3 | Separates focus-backed orb control and lightning cycle from generic power soup and Thunder Strike greed. | Frost stall, dark orb burst, Claw/zero-cost, and power/focus scaling are not first-class families. |
| `poison` | Silent | 12 | 3 | Separates poison support lock from finisher-only, Catalyst burst traps, and branch-split hybrids. | Needs more cases for poison stall, Nightmare/Burst overlap, and Envenom cross-scaling boundaries. |
| `retain` | Watcher/Silent setup | 12 | 5 | Separates clean retained setup windows from hybrid soup, setup-tax tunnels, Alpha tax, and over-taxed burst plans. | Establishment is represented, but not yet a broad retained-cost-reduction axis. |
| `shiv` | Silent | 8 | 3 | Separates real shiv swarm support/glue from payoff greed, Envenom split, and raw hand-dump behavior. | Needs more block/dex/After Image and Kunai/Shuriken-style relic adjacency before claiming full shiv ecosystem coverage. |
| `stance_mantra` | Watcher | 17 | 3 | Separates stance/mantra threshold closure and divinity support from almost-loop and generic stance goodstuff. | Scry-only, pressure points, Alpha/Omega, and divinity-only burst are not standalone families. |

Current explicit coverage is therefore a strong reviewed subset of `STS1` mechanism
viability, not a complete deck-archetype universe.

## Coverage Interpretation

For `STS1`, the current system covers the most important high-signal mechanism shells
needed to tell whether a design candidate supports an online deck plan:

- Ironclad: `exhaust`, draw bridge, and loop-adjacent closure.
- Silent: `shiv`, `poison`, `draw_engine`, `discard_cycle`, and `retain`.
- Defect: `orb_control` around focus-backed control, lightning cycle, and power-soup
  contrasts.
- Watcher: `stance_mantra`, retained setup, and threshold closure.

This is enough to support meaningful mechanism-aware design discussion and reviewed
benchmarking. It is not enough to say the system understands all `STS1` archetypes.

As a planning estimate:

- explicit reviewed family coverage: `9` families
- strong reviewed contrast coverage: about half of the high-signal `STS1` mechanism
  surface
- named archetype taxonomy coverage: below half, because several famous archetypes are
  still only adjacent or absent

## Missing Core Axis Backlog

### P0: Fill First

These gaps are common, high-signal, and likely to improve card-design evaluation quickly.

| Candidate Family | Main Character | Why It Matters | First Contrasts To Add |
| --- | --- | --- | --- |
| `strength_scaling` | Ironclad | Strength is a central Ironclad scaling plan and currently appears only as adjacent loop/competing evidence. | real strength shell vs raw attack pile; Limit Break payoff-only gap; Demon Form slow scaling vs immediate support shell |
| `block_engine` | Ironclad/Silent | Block as engine/payoff is separate from survival value; it covers Body Slam, Barricade, Entrench, Footwork, Blur, and After Image adjacency. | barricade/body-slam shell vs defensive pile; dex block shell vs raw mitigation; payoff-only Body Slam gap |
| `frost_control` | Defect | Frost/focus stall is a core Defect plan and should not be collapsed into generic orb control. | frost focus shell vs lightning greed; focus payoff without orb density; defensive stall without scaling |
| `power_focus_scaling` | Defect | Creative AI, Defragment, Echo Form, Biased Cognition, and power payoffs need a path distinct from power soup. | focus scaling shell vs generic powers; Echo Form payoff-only; Awakened One risk contrast |

### P1: Add After P0

These are important but either narrower, more exactness-sensitive, or easier to confuse
with existing families.

| Candidate Family | Main Character | Why It Matters | First Contrasts To Add |
| --- | --- | --- | --- |
| `zero_cost_claw` | Defect | Claw, All for One, Scrape, and zero-cost recursion are not well represented by `orb_control`. | Claw density shell vs zero-cost soup; All for One payoff-only; Scrape draw-risk gap |
| `dark_orb_burst` | Defect | Dark orb timing is a distinct setup/release plan. | dark setup shell vs orb goodstuff; release payoff without setup; frost/dark split timing gap |
| `scry_control` | Watcher | Scry can be a control/selection engine even without full stance/mantra ownership. | scry selection shell vs stance goodstuff; payoff-only Weave/Nirvana; setup-tax gap |
| `self_damage_status` | Ironclad | Rupture, Brutality, Pain/status synergies, and wound/status packages are under-modeled. | self-damage scaling shell vs damage tax; status payoff-only; exhaust overlap conflict |
| `copy_exactness` | Silent/Watcher | Nightmare, Burst, Omniscience, and Grand Finale plans need exactness-aware positives, not only negative gap checks. | copy setup shell vs fantasy overlap; Grand Finale exactness shell vs draw pile; payoff-only copy gap |

### P2: Keep As Later Specialist Axes

These are real but should wait until the broader axes are stable.

| Candidate Family | Main Character | Why It Matters |
| --- | --- | --- |
| `pressure_points` | Watcher | Narrow standalone Watcher plan with unusual scaling rules. |
| `alpha_omega` | Watcher | High setup-tax win condition, currently only represented as a negative retain/setup tax. |
| `relic_driven_engine` | Cross-character | Many `STS1` mechanisms depend on relic breakpoints, but this crosses the card-only boundary. |
| `potion_encounter_axis` | Cross-character | Useful for evaluation, but it belongs closer to matchup/context analysis than core card mechanism families. |

## Parallel Work Shape

Each new family can be developed independently with this minimum shape:

1. Add family spec to `mechanism_axis_contracts.py`.
2. Add at least three reviewed viability contrasts:
   - clear online shell
   - payoff-only or fantasy-exactness failure
   - hybrid/goodstuff or adjacent-family confusion
3. Add one or more holdout or project-card cases only after the viability contrast reads
   correctly.
4. Keep learned/reranker paths report-only and default-off.

Recommended first parallel batch:

- Worker A: `strength_scaling`
- Worker B: `block_engine`
- Worker C: `frost_control`
- Worker D: `power_focus_scaling`

These write to mostly separate fixture files, with one coordinated edit to
`mechanism_axis_contracts.py`.

## Current Bottom Line

The current cardanalysis mechanism-axis layer is ready for STS1-style design review
around online-shell detection. It should be treated as a reviewed contrast surface with
`9` explicit families, not as a complete STS1 archetype ontology.

The next capability jump should come from adding missing families and reviewed
contrasts, not from tightening architecture rules.
