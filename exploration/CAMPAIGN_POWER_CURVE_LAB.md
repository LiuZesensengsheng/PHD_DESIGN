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

### 2026-04-27 Round 2

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What is the smallest checkpoint suite that makes the abstract curve vocabulary
    usable for later encounter validation without adding monster numbers or pass/fail
    authority?
- Model increment:
  - Added four example `curve_checkpoint` records for `starter`, `build`, `pivot`,
    and `mature`.
  - Bound each checkpoint to a design question, player-state focus, enemy pressure
    request, validation need, interpretation notes, and explicit non-authority notes.
- Assumptions:
  - Checkpoints should use qualitative pressure bands first; scalar ranges can come
    later only after the team has real campaign pacing evidence.
  - A checkpoint is useful when it explains what an encounter should reveal, not when
    it says whether the deck passed.
  - `late` is intentionally deferred until the model has a better handle on mature
    phase fail-state and anti-infinite language.
- Risks:
  - The examples may look more certain than they are if later reports omit
    `evidence_state` and `authority_boundary`.
  - Mature-phase pressure can easily become hidden numeric tuning if future work jumps
    straight to enemy stats.
- Next round entry:
  - Add a compact `checkpoint_evidence_state` vocabulary so future checkpoints can
    distinguish hypothetical, reviewed, playtest-observed, and stale assumptions.

### 2026-04-27 Round 3

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - How should a curve checkpoint state its evidence maturity so designers do not
    mistake a hypothesis for a reviewed or playtest-observed baseline?
- Model increment:
  - Added `checkpoint_evidence_state` as a compact report-only vocabulary.
  - Added default rules for evidence labels, freshness, allowed use, stale triggers,
    and non-authority boundaries.
  - Added a small payload extension that can be attached to future checkpoints.
- Assumptions:
  - The first checkpoint examples remain `hypothesis_draft` until reviewed against
    campaign economy, reward pacing, and encounter observations.
  - Evidence maturity should change how cautiously a checkpoint is used, not whether
    a deck or encounter passes.
- Risks:
  - `playtest_observed` could be read as a tuning target if future reports omit the
    observation scope and sample caveats.
  - `reviewed_design` could become stale silently when reward pacing, card pools, or
    campaign round counts change.
- Next round entry:
  - Define a small `mechanism_online_timing` rubric that maps `absent`,
    `assembling`, `conditional_online`, `online`, and `over_online` to evidence needs
    by phase.

### 2026-04-27 Round 4

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - How should the model describe mechanism online timing by phase without turning
    online labels into pass/fail authority?
- Model increment:
  - Added `mechanism_online_timing` as a phase-aware rubric.
  - Mapped `absent`, `assembling`, `conditional_online`, `online`, and `over_online`
    to allowed phase reads and evidence needs.
  - Added transition evidence rules for moving between online labels.
- Assumptions:
  - Most healthy decks should not be expected to be `online` before `pivot`.
  - `conditional_online` is a useful honesty label and should not be treated as a
    weaker pass/fail grade.
  - `over_online` is a review prompt for encounter texture, not proof that the player
    mechanism is invalid.
- Risks:
  - Future encounter work could overuse the rubric as a readiness checklist unless
    reports keep `evaluation_mode=report_only`.
  - `starter` and `early` labels may need revision once actual campaign reward pacing
    is observed.
- Next round entry:
  - Define how `economy_state` and `compression_state` should modify online timing,
    especially removal, upgrade, shop, transform, and in-combat exhaust assumptions.

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

### Mechanism Online Timing Rubric

`mechanism_online_timing` is a report-only interpretation layer over
`mechanism_online_state`. It describes what evidence is needed for an online label at
each phase.

It should not answer "is the deck good enough?" It should answer "what kind of online
claim is honest for this phase and evidence state?"

#### Label Meanings

| Label | Timing Meaning | Evidence Needed |
| --- | --- | --- |
| `absent` | No meaningful mechanism identity is visible yet. | No support/payoff relationship, no repeated trigger pattern, or only generic frontload/defense. |
| `assembling` | Pieces exist, but the deck is still paying setup, density, or bridge costs. | At least one support/payoff link plus visible missing prerequisites. |
| `conditional_online` | The mechanism works in some fights or draw states, but depends on timing, compression, enemy state, or resource alignment. | Named prerequisites, named failure mode, and at least one credible activation path. |
| `online` | The mechanism shapes most relevant encounters in the phase without exact luck. | Support/payoff density, draw/resource access, survival window, and fallback evidence. |
| `over_online` | The mechanism can flatten intended pressure or bypass encounter texture. | High repeatability plus low remaining constraint; still report-only and never a legality verdict. |

#### Phase Expectations

| Phase | Normal Honest Labels | Suspicious Labels | Evidence Notes |
| --- | --- | --- | --- |
| `starter` | `absent`, rare `assembling` | `conditional_online`, `online`, `over_online` | A starter checkpoint should not require mechanism identity. If a mechanism appears, it is usually a tutorial/scripted exception or unusually strong starter package. |
| `early` | `absent`, `assembling` | `online`, `over_online` | First identity hints can appear, but claims should focus on frontload, block, and first support links. |
| `build` | `assembling`, early `conditional_online` | `over_online` | This is the first phase where support/payoff, bridge-before-payoff, and package density can justify a conditional claim. |
| `pivot` | `conditional_online`, narrow `online`, remaining `assembling` | `over_online` without review notes | The model should ask whether the mechanism survives light disruption and whether missing compression or economy evidence keeps it conditional. |
| `mature` | `online`, `conditional_online`, review-only `over_online` | `absent` without strong compensating frontload/scaling | Mature decks should show either a functioning plan or an explicit reason why a non-mechanism plan still answers pressure. |
| `late` | `online`, `over_online`, strong `conditional_online` | `absent`, weak `assembling` | Late checks may include anti-infinite notes, but those notes cannot declare a player loop invalid. |

#### Transition Evidence

Use these evidence shifts when changing labels:

| Transition | Needed Evidence | Common False Positive |
| --- | --- | --- |
| `absent -> assembling` | A support/payoff relationship, repeated trigger, or named package identity appears. | One exciting payoff card without bridge, support, or survival. |
| `assembling -> conditional_online` | The deck has at least one credible activation path plus named missing prerequisites. | Assuming the best draw sequence is the normal case. |
| `conditional_online -> online` | Activation works across common draw states or has enough draw, selection, energy, compression, and survival support. | Counting discard filtering as persistent compression or ignoring first-cycle survival. |
| `online -> over_online` | Repeatability and low constraint begin to flatten enemy pressure or matchup texture. | Treating every loop, infinite, or high-ceiling combo as degenerate by category. |
| `over_online -> online` | Added costs, constraints, matchup pressure, or player choices keep texture visible. | Hiding anti-infinite concerns because the deck still has some fail states. |
| `online -> conditional_online` | New evidence shows route dependency, compression burden, unreliable survival, or narrow matchup coverage. | Downgrading because one encounter archetype pressures the deck as intended. |

#### Evidence Fields

Future checkpoints may attach:

```json
{
  "mechanism_online_timing": {
    "label": "conditional_online",
    "phase": "pivot",
    "activation_paths": ["support_density_plus_draw_bridge"],
    "missing_prerequisites": ["removal_route", "first_cycle_survival"],
    "phase_read": "appropriate_but_needs_validation",
    "transition_from_prior_phase": "assembling_to_conditional_online",
    "reason_codes": [
      "payoff_supported_but_compression_unknown",
      "light_disruption_should_reveal_brittleness"
    ],
    "authority_boundary": "report_only_not_readiness_gate"
  }
}
```

Required conventions:

- `phase_read` must be advisory language, not `pass` or `fail`.
- `missing_prerequisites` should remain visible instead of being folded into a scalar.
- `activation_paths` should name why the mechanism can happen, not only that it scored
  above a threshold.
- `over_online` must include reason codes for remaining constraints or texture risks.
- A label change should preserve prior uncertainty when economy or compression context
  is still unknown.

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
      "evidence_state": {
        "label": "hypothesis_draft",
        "freshness": "new",
        "allowed_use": "discussion_seed",
        "missing_evidence": ["campaign_economy_review", "playtest_observation"],
        "authority_boundary": "not_a_gate"
      },
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

## Checkpoint Evidence State

`checkpoint_evidence_state` states how mature a checkpoint is. It is report-only
metadata, not a confidence gate.

The evidence state should answer:

- is this checkpoint a new hypothesis, a design-reviewed assumption, or playtest
  observation?
- what evidence is missing before it should guide encounter validation?
- what changed conditions would make it stale?
- how may downstream tools or designers use it without treating it as authority?

### Labels

| Label | Meaning | Allowed Use |
| --- | --- | --- |
| `hypothesis_draft` | A first-pass model assumption with no reviewed campaign evidence yet. | Use as a discussion seed and checklist prompt only. |
| `source_aligned` | The checkpoint is aligned with existing report-only docs or cardanalysis signals, but not reviewed as campaign pacing. | Use for planning candidate validation questions. |
| `reviewed_design` | A designer or main-agent review accepted the checkpoint language for a known campaign slice. | Use as a temporary encounter-design reference, still advisory. |
| `playtest_observed` | Playtest or replay observations support the checkpoint within a named scope. | Use as stronger evidence for future checkpoint refinement, not as a hard target. |
| `stale_assumption` | The checkpoint was once useful but may no longer match current card pools, economy, rewards, or encounter pacing. | Keep visible as history; do not use for new validation without review. |
| `superseded` | A newer checkpoint replaces this one. | Keep only for traceability and migration notes. |

### Minimum Fields

```json
{
  "checkpoint_evidence_state": {
    "label": "hypothesis_draft",
    "freshness": "new",
    "evidence_refs": [],
    "missing_evidence": [
      "campaign_economy_review",
      "reward_pacing_review",
      "encounter_observation"
    ],
    "stale_triggers": [
      "phase_round_band_changed",
      "reward_pacing_changed",
      "card_pool_changed",
      "enemy_pressure_axis_changed"
    ],
    "allowed_use": "discussion_seed",
    "authority_boundary": "not_a_gate"
  }
}
```

### Freshness Labels

| Label | Meaning |
| --- | --- |
| `new` | Added this session or not yet revisited. |
| `current` | Recently checked against the named evidence refs. |
| `watch` | Still usable, but a known change may invalidate it soon. |
| `stale` | Should not guide new encounter work until reviewed. |

### Allowed Use Labels

| Label | Meaning |
| --- | --- |
| `discussion_seed` | Helps frame a design conversation; no implementation should rely on it. |
| `validation_prompt` | Can suggest what an encounter or replay should observe. |
| `temporary_design_reference` | Can guide a narrow design pass until the next review. |
| `historical_note_only` | Retained for continuity, not active planning. |

### Rules

- Every new checkpoint starts as `hypothesis_draft`.
- `source_aligned` needs at least one named source doc, report-only signal, or reviewed
  design note.
- `reviewed_design` needs explicit human or main-agent review context.
- `playtest_observed` must name observation scope, such as deck type, phase, encounter
  family, or replay batch.
- `stale_assumption` should be preferred over silent deletion when the model may need
  historical context.
- Higher evidence maturity does not create pass/fail authority.
- Missing evidence should remain `unknown` or named explicitly; do not convert it into
  zero burden.
- A checkpoint with `authority_boundary` other than `not_a_gate` is outside V1.

The current V0 checkpoint examples should be treated as `hypothesis_draft` until a
later run reviews them against campaign economy and reward pacing.

## Curve Checkpoint Examples V0

These examples are deliberately qualitative. They are not balance targets and do not
authorize content, gates, or monster numbers.

Each checkpoint should answer:

- what design question is this round asking?
- which player strength dimensions matter most?
- which enemy pressure dimensions are being requested?
- what evidence is missing before the checkpoint should guide real encounters?
- what authority boundary prevents the checkpoint from becoming a pass/fail decision?

### `starter_round_1_baseline_survival_v0`

```json
{
  "curve_checkpoint": {
    "checkpoint_id": "starter_round_1_baseline_survival_v0",
    "phase": "starter",
    "round_index_hint": 1,
    "evaluation_mode": "report_only",
    "design_question": "Can the starting deck answer basic pressure without a mechanism?",
    "player_state_focus": [
      "frontload",
      "block_reliability",
      "fail_state_resilience"
    ],
    "expected_player_shape": {
      "frontload": "low_to_medium",
      "scaling": "low",
      "block_reliability": "low_to_medium",
      "draw_velocity": "low",
      "energy_burst": "low",
      "deck_compression": "none",
      "removal_progress": "none",
      "mechanism_online_rate": "absent",
      "combo_reachability": "absent",
      "fail_state_resilience": "starter_baseline"
    },
    "enemy_pressure_request": {
      "frontload_damage": "low_to_medium",
      "defense_check": "low",
      "multi_enemy_pressure": "optional_low",
      "status_pollution": "avoid",
      "mechanism_disruption": "avoid",
      "anti_infinite_pressure": "avoid"
    },
    "encounter_validation_need": [
      "starter_damage_baseline_visibility",
      "starter_block_baseline_visibility",
      "no_mechanism_required"
    ],
    "interpretation_notes": [
      "do_not_expect_mechanism_identity",
      "do_not_punish_low_draw_velocity",
      "frontload_or_block_failure_is_a_review_prompt_not_a_gate"
    ],
    "authority_boundary": "advisory_context_only"
  }
}
```

Design reading:

- This checkpoint is for baseline encounter readability, not archetype validation.
- It should reveal whether starter friction is visible and survivable.
- It should avoid status pollution and disruption because those test later deck
  maturity, not the opening curve.

### `build_round_5_identity_assembly_v0`

```json
{
  "curve_checkpoint": {
    "checkpoint_id": "build_round_5_identity_assembly_v0",
    "phase": "build",
    "round_index_hint": 5,
    "evaluation_mode": "report_only",
    "design_question": "Is the deck assembling a real identity or only carrying payoff cards?",
    "player_state_focus": [
      "frontload",
      "draw_velocity",
      "mechanism_online_rate",
      "fail_state_resilience"
    ],
    "deck_maturity_focus": [
      "support_density",
      "payoff_density",
      "bridge_before_payoff",
      "off_axis_drag"
    ],
    "expected_player_shape": {
      "frontload": "medium",
      "scaling": "low_to_medium",
      "block_reliability": "medium_or_gap_visible",
      "draw_velocity": "low_to_medium",
      "energy_burst": "low_or_conditional",
      "deck_compression": "low_or_unknown",
      "removal_progress": "low_or_unknown",
      "mechanism_online_rate": "assembling",
      "combo_reachability": "low",
      "fail_state_resilience": "partial"
    },
    "enemy_pressure_request": {
      "frontload_damage": "medium",
      "defense_check": "medium",
      "multi_enemy_pressure": "low_to_medium",
      "status_pollution": "low",
      "draw_disruption": "avoid_or_low",
      "mechanism_disruption": "avoid"
    },
    "encounter_validation_need": [
      "payoff_only_detection",
      "bridge_or_support_gap_visibility",
      "first_identity_pressure_without_hard_counter"
    ],
    "interpretation_notes": [
      "mechanism_not_online_is_expected_for_many_decks",
      "payoff_present_without_bridge_should_report_assembly_gap",
      "enemy_pressure_should_not_require_final_shell"
    ],
    "authority_boundary": "advisory_context_only"
  }
}
```

Design reading:

- The checkpoint separates an actual assembling identity from a deck that only drafted
  a high-ceiling payoff.
- Enemy pressure can ask for consistency, but should not yet hard-counter missing
  compression or exact combo reachability.
- This is the first checkpoint where package health language can be useful, especially
  `slot_fit`, `payoff_timing`, and `bridge_before_payoff`.

### `pivot_round_8_conditional_online_v0`

```json
{
  "curve_checkpoint": {
    "checkpoint_id": "pivot_round_8_conditional_online_v0",
    "phase": "pivot",
    "round_index_hint": 8,
    "evaluation_mode": "report_only",
    "design_question": "Can the deck keep its main mechanism active under light disruption?",
    "player_state_focus": [
      "mechanism_online_rate",
      "combo_reachability",
      "draw_velocity",
      "deck_compression",
      "fail_state_resilience"
    ],
    "expected_player_shape": {
      "frontload": "medium",
      "scaling": "medium",
      "block_reliability": "medium",
      "draw_velocity": "medium_or_named_gap",
      "energy_burst": "conditional_or_gap_visible",
      "deck_compression": "low_to_medium_or_route_dependent",
      "removal_progress": "low_to_medium_or_unknown",
      "mechanism_online_rate": "conditional_online",
      "combo_reachability": "conditional",
      "fail_state_resilience": "must_be_visible"
    },
    "enemy_pressure_request": {
      "frontload_damage": "medium",
      "defense_check": "medium",
      "draw_disruption": "low_to_medium",
      "energy_tax": "low",
      "status_pollution": "low_to_medium",
      "mechanism_disruption": "low_to_medium",
      "anti_infinite_pressure": "avoid_or_trace_only"
    },
    "encounter_validation_need": [
      "conditional_online_claim_visibility",
      "compression_route_gap_visibility",
      "fallback_line_under_disruption"
    ],
    "interpretation_notes": [
      "light_disruption_should_reveal_brittleness_without_becoming_a_hard_counter",
      "missing_removal_context_should_remain_unknown",
      "route_dependent_online_is_an_honesty_label_not_a_failure"
    ],
    "authority_boundary": "advisory_context_only"
  }
}
```

Design reading:

- This checkpoint is the first real mechanism pressure point.
- It should expose whether the deck is conditionally online, online-if-compressed, or
  still payoff-only.
- It should preserve compression distinctions: removal, transform, exhaust, discard
  filtering, and draw selection are not equivalent.

### `mature_round_12_ceiling_and_recovery_v0`

```json
{
  "curve_checkpoint": {
    "checkpoint_id": "mature_round_12_ceiling_and_recovery_v0",
    "phase": "mature",
    "round_index_hint": 12,
    "evaluation_mode": "report_only",
    "design_question": "Does the deck have ceiling, defense, and recovery when the main plan misses?",
    "player_state_focus": [
      "scaling",
      "block_reliability",
      "mechanism_online_rate",
      "combo_reachability",
      "fail_state_resilience"
    ],
    "expected_player_shape": {
      "frontload": "medium_or_solved_by_plan",
      "scaling": "medium_to_high",
      "block_reliability": "medium_to_high_or_named_gap",
      "draw_velocity": "medium_to_high",
      "energy_burst": "conditional_to_high",
      "deck_compression": "medium_or_route_dependent",
      "removal_progress": "medium_or_gap_visible",
      "mechanism_online_rate": "online_or_strong_conditional",
      "combo_reachability": "credible_or_route_dependent",
      "fail_state_resilience": "required_visible"
    },
    "enemy_pressure_request": {
      "frontload_damage": "medium",
      "scaling_race": "medium_to_high",
      "defense_check": "medium_to_high",
      "burst_check": "medium",
      "multi_enemy_pressure": "medium",
      "mechanism_disruption": "medium",
      "anti_infinite_pressure": "trace_or_low_report_only"
    },
    "encounter_validation_need": [
      "ceiling_vs_scaling_race",
      "defensive_reliability_under_pressure",
      "main_plan_miss_recovery",
      "anti_infinite_notes_without_authority"
    ],
    "interpretation_notes": [
      "anti_infinite_pressure_is_not_a_loop_invalidity_verdict",
      "strong_ceiling_without_fail_state_should_report_review_need",
      "enemy_numbers_remain_out_of_scope"
    ],
    "authority_boundary": "advisory_context_only"
  }
}
```

Design reading:

- Mature pressure can combine scaling, defense, burst, and disruption.
- This checkpoint should not jump to final monster values. It only defines what a
  later encounter archetype should reveal.
- A strong mechanism with poor fail-state resilience should produce a review note, not
  a blocking verdict.

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
