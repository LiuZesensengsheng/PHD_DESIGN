# Campaign Power Curve Lab

## Purpose

Establish `campaign_power_curve_model_v1` as a report-only planning model for
campaign encounter design.

The model should help designers ask:

- how strong should the player be around campaign round N?
- which player mechanisms can reasonably be online by that phase?
- what enemy pressure is appropriate for that phase?
- what encounter archetype should validate the current curve hypothesis?

This is an exploration document. It does not change runtime behavior, hard gates,
recommendation defaults, learned/reranker paths, or monster numeric implementation.

## Strict Boundary

In scope:

- report-only curve checkpoint payload drafts
- phase vocabulary and transition assumptions
- player power and enemy pressure vectors
- encounter archetype sketches for future validation
- future cardanalysis interface notes

Out of scope:

- hard gates or pass/fail authority
- recommendation default path changes
- learned/reranker promotion
- formal enemy number tuning
- runtime monster implementation

## Working Log

### 2026-04-27

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What is the smallest report-only contract that can connect campaign round,
    player power state, mechanism online timing, deck compression, enemy pressure,
    and encounter validation without becoming a gate?
- Model increment:
  - Created the first `campaign_power_curve_model_v1` vocabulary.
  - Added required entities, vectors, phase labels, transition rules, report-only
    payload draft, encounter archetypes, and a future cardanalysis interface draft.
- Assumptions:
  - Round bands below are initial hypotheses, not balance targets.
  - `deck_compression` and `removal_progress` should separate persistent thinning
    from in-combat filtering or exhaust.
  - Enemy pressure should be expressed as a vector request before any monster number
    implementation exists.
- Risks:
  - The model could drift into an implicit pass/fail score if future payloads expose
    `overall_pass`, `hard_gates`, or blocking language.
  - Phase bands may be wrong until compared with real campaign economy, reward, and
    encounter pacing.
  - Encounter archetypes may become too generic unless later runs bind them to a small
    reviewed set of curve checkpoints.
- Next round entry:
  - Define 3-5 concrete `curve_checkpoint` examples for starter, build, pivot, and
    mature phases, still report-only and without monster numbers.

## Model V1

### Entity Vocabulary

| Entity | Meaning |
| --- | --- |
| `campaign_round` | The campaign position being evaluated. Minimum fields: `round_index`, `phase`, `route_context`, `boss_or_elite_pressure_hint`, and optional reward/economy notes. |
| `player_power_state` | The current player strength vector and its reason codes. It summarizes output, defense, draw, energy, resilience, and online mechanism readiness. |
| `deck_maturity_state` | How complete the deck shell is: starter pollution, support/payoff density, redundancy, off-axis drag, and whether the deck is still drafting identity. |
| `mechanism_online_state` | Whether a mechanism is absent, assembling, conditionally online, online, or over-online. It should record prerequisites instead of only a score. |
| `economy_state` | Upgrade, removal, transform, shop, event, healing, and resource opportunity context. This is route evidence, not exact route probability. |
| `compression_state` | Persistent and in-combat compression status. It separates removal, transform, self-exhaust, targeted exhaust, discard filtering, draw selection, and deck-size sensitivity. |
| `enemy_pressure_profile` | A report-only vector request for enemy behavior pressure by phase. It is not a monster stat block. |
| `encounter_archetype` | A reusable validation shape, such as early frontload check or pivot disruption check. It names the question an encounter should answer. |
| `curve_checkpoint` | A snapshot that binds one campaign round/phase to player state, enemy pressure request, validation need, risks, and next evidence needed. |

### Phase Labels

Initial phase bands are hypotheses for discussion only:

| Phase | Round Hypothesis | Design Meaning |
| --- | --- | --- |
| `starter` | `0-1` | Baseline deck and first reward pressure. Player survival and starter friction dominate. |
| `early` | `2-3` | First identity hints appear. Frontload and block reliability still matter more than full engines. |
| `build` | `4-6` | Support density and first payoff alignment matter. Mechanisms are usually assembling, not guaranteed online. |
| `pivot` | `7-9` | The run should start proving an identity. Enemy pressure can ask whether the mechanism survives disruption. |
| `mature` | `10-13` | Core deck shape should be visible. Encounters can test scaling, burst, defense, and fail-state resilience together. |
| `late` | `14+` | Finished or near-finished decks face multi-axis pressure, anti-infinite pressure, and high consequence checks. |

### Player Strength Vector

Scores are report-only `0.0-1.0` estimates. Higher means more of the named capability.
Every score should carry reason codes.

| Field | High Value Means |
| --- | --- |
| `frontload` | The player can solve early threats quickly before the deck is fully online. |
| `scaling` | The player can grow damage, defense, or advantage over longer fights. |
| `block_reliability` | Defensive output is repeatable enough across common draw states. |
| `draw_velocity` | The deck can see more cards, cycle faster, or select needed cards. |
| `energy_burst` | The deck can temporarily exceed normal energy limits or cheat cost windows. |
| `deck_compression` | The deck is effectively smaller through removal, transform, exhaust, self-exhaust, or highly reliable selection. |
| `removal_progress` | Persistent starter/off-axis cleanup has actually happened or has credible route evidence. |
| `mechanism_online_rate` | The core mechanism becomes active often enough to shape encounter planning. |
| `combo_reachability` | Required pieces, states, draw, energy, and compression can align in time. |
| `fail_state_resilience` | The deck can still function when the main plan misses, is disrupted, or arrives late. |

### Enemy Pressure Vector

Enemy pressure also uses report-only `0.0-1.0` estimates or labels. It describes what
an encounter asks, not exact damage numbers.

| Field | High Value Means |
| --- | --- |
| `frontload_damage` | The encounter pressures first-cycle survival and early answer quality. |
| `scaling_race` | The enemy gets worse over time and asks whether player scaling arrives fast enough. |
| `status_pollution` | The encounter adds statuses, curses, or dead draws that stress deck maturity. |
| `draw_disruption` | The encounter blocks, delays, punishes, or scrambles draw/card access. |
| `energy_tax` | The encounter taxes energy, tempo, or action availability. |
| `multi_enemy_pressure` | Multiple bodies or priorities split damage, block, targeting, and tempo. |
| `defense_check` | The encounter asks for reliable mitigation instead of only damage. |
| `burst_check` | The encounter asks whether the deck can answer a large short-window threat. |
| `mechanism_disruption` | The encounter attacks setup assumptions, prerequisites, or repeat windows. |
| `anti_infinite_pressure` | The encounter adds friction against unbounded loops without declaring the loop invalid. |

## Transition Rules

### Power Spike Rules

A player power spike should be reported when at least one of these changes is visible:

- `frontload` rises because the deck gains efficient early damage or tempo.
- `block_reliability` rises because defense is no longer dependent on one draw state.
- `draw_velocity` or `energy_burst` rises enough to change average setup timing.
- `mechanism_online_rate` rises from assembling to conditionally online or online.
- `fail_state_resilience` rises because the deck gains a backup plan, not only a
  higher ceiling.

Power spikes should not be reported from payoff cards alone unless support, draw,
energy, compression, and survival evidence make the payoff reachable.

### Mechanism Online Rules

`mechanism_online_state` should use these labels:

- `absent`: no meaningful mechanism identity yet.
- `assembling`: support or payoff exists, but prerequisites are incomplete.
- `conditional_online`: the mechanism works when draw, energy, enemy state, or
  compression lines up.
- `online`: the mechanism shapes most relevant encounters without exact draw luck.
- `over_online`: the mechanism threatens to bypass intended encounter pressure and
  should be monitored with report-only anti-infinite notes.

Mechanism online timing should consider:

- support/payoff density
- draw and selection access
- energy or cost breakpoints
- upgrade assumptions
- removal and deck compression
- enemy-state prerequisites
- whether the player can survive the setup window

### Compression And Removal Rules

Persistent removal changes the campaign curve differently from in-combat filtering:

- `removal_progress` improves route-level reachability and lowers starter pollution.
- `deck_compression` improves when the deck becomes smaller or effectively smaller.
- `draw_velocity` can improve hand quality without actually improving persistent
  `removal_progress`.
- discard filtering is not persistent compression by itself.
- transform should be treated as route evidence only when replacement quality is known
  or explicitly marked unknown.
- targeted early exhaust can support a conditional online claim, but late exhaust may
  arrive after the mechanism needed to work.

Compression should alter curve interpretation before it alters any score authority:

- high mechanism viability plus low compression burden: `final_shell_online`
- high mechanism viability plus high compression burden: `online_if_compressed`
- infinite or exactness claim without route evidence: `route_dependent_online`
- curated deck that skips starter cards: `curated_deck_skips_removal_cost`

### Enemy Pressure By Phase

| Phase | Default Pressure Shape |
| --- | --- |
| `starter` | Low complexity. Use `frontload_damage` and `defense_check` lightly to verify baseline survival and starter friction. |
| `early` | Add modest `multi_enemy_pressure` or `status_pollution` only when frontload and block have plausible answers. |
| `build` | Start asking for draw/energy/block consistency. Pressure should reveal whether the deck is assembling or just carrying payoff cards. |
| `pivot` | Introduce `mechanism_disruption`, `draw_disruption`, or `energy_tax` in small doses to test conditional online claims. |
| `mature` | Combine `scaling_race`, `burst_check`, and `defense_check` to validate whether the deck has both ceiling and fallback. |
| `late` | Use multi-axis pressure including `anti_infinite_pressure`, but keep it report-only and avoid declaring player loops invalid by model output alone. |

## Report-Only Payload Draft

```json
{
  "campaign_power_curve_model": {
    "contract_version": "campaign_power_curve_model_v1",
    "evaluation_mode": "report_only",
    "campaign_round": {
      "round_index": 7,
      "phase": "pivot",
      "route_context": "unknown",
      "notes": ["round_band_is_initial_hypothesis"]
    },
    "curve_checkpoint": {
      "checkpoint_id": "pivot_mechanism_online_probe_v1",
      "design_question": "Can the deck keep its mechanism active under light disruption?",
      "review_only_verdict": "needs_encounter_validation",
      "must_not_expose": ["overall_pass", "hard_gates"]
    },
    "player_power_state": {
      "frontload": {"score": 0.52, "reason_codes": ["first_attack_upgrade"]},
      "scaling": {"score": 0.61, "reason_codes": ["payoff_present"]},
      "block_reliability": {"score": 0.45, "reason_codes": ["block_draw_variance"]},
      "draw_velocity": {"score": 0.58, "reason_codes": ["repeatable_draw_support"]},
      "energy_burst": {"score": 0.30, "reason_codes": ["no_stable_energy_engine"]},
      "deck_compression": {"score": 0.40, "reason_codes": ["some_self_exhaust"]},
      "removal_progress": {"score": 0.25, "reason_codes": ["starter_basics_remain"]},
      "mechanism_online_rate": {"score": 0.50, "reason_codes": ["conditional_online"]},
      "combo_reachability": {"score": 0.46, "reason_codes": ["missing_compression_route"]},
      "fail_state_resilience": {"score": 0.42, "reason_codes": ["backup_plan_partial"]}
    },
    "deck_maturity_state": {
      "maturity_label": "assembling_identity",
      "support_density": "medium",
      "payoff_density": "low",
      "starter_pollution": "medium",
      "off_axis_drag": "medium"
    },
    "mechanism_online_state": {
      "online_label": "conditional_online",
      "prerequisites": ["support_density", "draw_velocity", "compression_route"],
      "missing_evidence": ["removal_route", "first_cycle_survival"]
    },
    "economy_state": {
      "upgrade_pressure": "medium",
      "removal_access": "unknown",
      "shop_opportunity_cost": "unknown",
      "route_risk": "unknown"
    },
    "compression_state": {
      "persistent_sources": ["unknown_removal"],
      "combat_sources": ["self_exhaust", "draw_selection"],
      "invalid_equivalences": ["discard_filtering_is_not_persistent_removal"]
    },
    "enemy_pressure_profile": {
      "frontload_damage": 0.45,
      "scaling_race": 0.45,
      "status_pollution": 0.35,
      "draw_disruption": 0.30,
      "energy_tax": 0.20,
      "multi_enemy_pressure": 0.35,
      "defense_check": 0.50,
      "burst_check": 0.35,
      "mechanism_disruption": 0.40,
      "anti_infinite_pressure": 0.10
    },
    "encounter_validation_needs": [
      "light_disruption_without_hard_counter",
      "first_cycle_survival_check",
      "fallback_plan_visibility"
    ]
  }
}
```

## Encounter Archetypes

### `starter_frontload_and_defense_check`

- Phases: `starter`, `early`
- Primary pressure:
  - `frontload_damage`
  - `defense_check`
  - optional low `multi_enemy_pressure`
- Validation question:
  - Can a starter or early deck survive and answer basic threats without requiring a
    full mechanism?
- Avoid:
  - status-heavy disruption
  - anti-infinite pressure
  - mechanics that punish a mechanism before it could reasonably exist

### `pivot_mechanism_disruption_probe`

- Phases: `build`, `pivot`
- Primary pressure:
  - `mechanism_disruption`
  - `draw_disruption`
  - `status_pollution`
  - moderate `defense_check`
- Validation question:
  - Is the mechanism truly online, or only present as payoff fantasy?
- Avoid:
  - hard counters
  - pressure that invalidates every deck without the same answer
  - interpreting the encounter result as a pass/fail model decision

### `mature_scaling_burst_and_fail_state_check`

- Phases: `mature`, `late`
- Primary pressure:
  - `scaling_race`
  - `burst_check`
  - `defense_check`
  - late-only report-only `anti_infinite_pressure`
- Validation question:
  - Does the deck have ceiling, defense, and recovery when the main plan misses?
- Avoid:
  - monster numbers in this model document
  - treating anti-infinite pressure as proof that an infinite is invalid

## Future Cardanalysis Interface Draft

The campaign power curve model can consume report-only signals from cardanalysis, but
it should not become a ranking, legality, or hard-gate owner.

Potential inputs:

- `deck_compression_report_v1`
  - use for `deck_compression`, `removal_progress`, starter pollution, and
    route-dependent online notes
- `mechanism_axis_discovery_v1` and mechanism viability reports
  - use for candidate mechanism identity, foundation-axis dependency, and online
    prerequisite notes
- `card_package_health_v1`
  - use for support/payoff/glue density and off-axis drag
- `design_iteration_brief_v1`
  - use for setup burden, fail-state risk, and next validation needs

Potential output context for cardanalysis:

```json
{
  "campaign_curve_context": {
    "contract_version": "campaign_power_curve_context_v1",
    "evaluation_mode": "report_only",
    "round_index": 7,
    "phase": "pivot",
    "player_strength_focus": ["mechanism_online_rate", "fail_state_resilience"],
    "enemy_pressure_request": ["mechanism_disruption", "defense_check"],
    "encounter_validation_need": "light_disruption_without_hard_counter",
    "authority_boundary": "advisory_context_only"
  }
}
```

Interface rules:

- Do not expose `overall_pass`, `hard_gates`, or blocking verdicts.
- Do not let learned/reranker output decide campaign phase, legality, or encounter
  readiness.
- Treat missing campaign economy context as `unknown`, not as zero burden.
- Prefer reason codes and validation questions over scalar-only scores.
