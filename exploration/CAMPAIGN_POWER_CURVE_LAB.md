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

### 2026-04-27 Round 5

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - How should economy and compression context modify mechanism online timing without
    pretending the model knows route probability or monster numbers?
- Model increment:
  - Added `online_timing_modifier` rules for economy and compression.
  - Split persistent route evidence from in-combat mitigation evidence.
  - Added modifier labels that can advance, delay, condition, or stale-check online
    timing claims while staying report-only.
- Assumptions:
  - Economy evidence changes the route credibility of an online claim, not the final
    shell's internal coherence.
  - Compression evidence should distinguish removal, transform, self-exhaust, targeted
    exhaust, discard filtering, draw selection, and upgrade pressure.
  - Missing route context should remain `unknown`, not become a hidden zero-cost route.
- Risks:
  - Future work could over-credit shops or events as guaranteed access unless the
    modifier keeps opportunity cost and route risk visible.
  - Transform can look like removal unless replacement quality is explicitly recorded.
- Next round entry:
  - Define 2-3 more encounter archetypes that use these modifiers, especially a
    build-phase payoff-only detector and a pivot compression-route probe.

### 2026-04-27 Round 6

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Which encounter archetypes should consume `online_timing_modifier` output first
    without turning modifier labels into monster numbers or pass/fail authority?
- Model increment:
  - Added three modifier-driven encounter archetypes:
    `build_payoff_only_detector`, `pivot_compression_route_probe`, and
    `mature_over_online_texture_probe`.
  - Bound each archetype to the modifier labels it should read, the pressure axes it
    may request, the validation question it asks, and the interpretation boundary it
    must preserve.
- Assumptions:
  - Modifier-driven archetypes should expose why an online claim is conditional,
    route-dependent, delayed, or texture-risky.
  - An archetype can ask for pressure shape, but not specific damage, health, enemy
    counts, or blocking verdicts.
- Risks:
  - `payoff_only_detector` could become a hidden deck-quality gate if reports omit
    the advisory boundary.
  - `over_online` probes may be mistaken for anti-infinite legality checks unless
    encounter notes preserve remaining constraints and texture questions.
- Next round entry:
  - Define qualitative enemy pressure phase bands so archetype pressure requests have
    consistent low/medium/high language by phase.

### 2026-04-27 Round 7

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - How should enemy pressure requests use `low`, `medium`, and `high` by phase
    without becoming monster stat guidance?
- Model increment:
  - Added `enemy_pressure_phase_band` as qualitative language for pressure intensity
    by campaign phase.
  - Added a phase band table that marks normal axes, caution axes, and out-of-phase
    pressure for `starter`, `early`, `build`, `pivot`, `mature`, and `late`.
- Assumptions:
  - Pressure bands should describe encounter questions, not numeric damage, health,
    action count, or enemy roster size.
  - A later encounter can exceed a normal band only if it records the design reason
    and evidence need.
- Risks:
  - Designers may read `high` as a stat target unless future payloads keep the
    qualitative wording visible.
  - Phase bands may need revision after economy and reward pacing are reviewed.
- Next round entry:
  - Add a compact player power reason-code taxonomy so vector changes can explain
    why a score moved without relying on scalar-only output.

### 2026-04-27 Round 8

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What reason-code vocabulary should explain player power vector changes without
    making the scalar scores authoritative?
- Model increment:
  - Added `player_power_reason_code` conventions and reusable reason-code families.
  - Split positive, negative, and uncertainty reasons so reports can preserve why a
    vector moved and what evidence is still missing.
- Assumptions:
  - Reason codes should be short, stable labels that can be grouped by axis and
    evidence scope.
  - A negative reason code should create a review prompt, not a deck failure verdict.
- Risks:
  - Too many free-form reason codes could make reports hard to compare across
    checkpoints.
  - Scalar scores may still look more precise than the supporting reasons justify.
- Next round entry:
  - Define `deck_maturity_state` labels so package assembly, payoff-only risk,
    starter pollution, and off-axis drag can be described consistently.

### 2026-04-27 Round 9

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Which `deck_maturity_state` labels are needed to describe package assembly
    without judging the deck as pass/fail?
- Model increment:
  - Added deck maturity labels for starter-heavy, identity hint, assembling identity,
    payoff-only, bridge-ready, pivot-ready, mature core, goodstuff-resilient, and
    overfocused-brittle states.
  - Added dimensions and rules for support density, payoff density,
    bridge-before-payoff, starter pollution, off-axis drag, redundancy, and fallback
    plan visibility.
- Assumptions:
  - Deck maturity is about shape and assembly evidence, not final strength.
  - A deck can be immature but healthy for its phase, or mature but brittle under a
    specific pressure profile.
- Risks:
  - `payoff_only` may sound like a verdict unless reports keep it as a package-shape
    observation.
  - Goodstuff labels may hide mechanism absence unless support/payoff evidence stays
    visible.
- Next round entry:
  - Define `economy_state` labels for upgrade, removal, shop, event, transform,
    healing pressure, route risk, and opportunity cost.

### 2026-04-27 Round 10

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Which `economy_state` labels are needed to explain route credibility without
    pretending the model knows exact campaign path probability?
- Model increment:
  - Added economy dimensions and labels for upgrade breakpoints, removal access,
    shop windows, event assumptions, transform quality, healing pressure, opportunity
    cost, and route risk.
  - Clarified that economy labels modify online timing and reachability claims, not
    deck legality or encounter readiness.
- Assumptions:
  - Economy context should preserve unknowns rather than silently treating missing
    shops, events, or gold as no burden.
  - Healing pressure can consume the same resource budget as upgrades, removals, or
    shop purchases and should be visible.
- Risks:
  - Route labels may look like probability estimates if reports omit
    `route_context_unknown`.
  - Upgrade and removal evidence may be over-credited when their opportunity costs
    are not recorded.
- Next round entry:
  - Define `compression_state` labels that distinguish persistent removal,
    transform, in-combat exhaust, discard filtering, draw selection, and deck-size
    sensitivity.

### 2026-04-27 Round 11

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Which `compression_state` labels prevent the model from treating removal,
    transform, in-combat exhaust, discard filtering, and draw selection as the same
    kind of compression?
- Model increment:
  - Added compression dimensions and labels for persistent thinning, transform
    quality, early/late exhaust, filtering-only effects, draw selection, deck-size
    sensitivity, curated-deck assumptions, and compression tax.
  - Added rules for how compression labels may affect online timing without becoming
    reachability authority.
- Assumptions:
  - Persistent removal changes campaign reachability differently from combat-only
    filtering or selection.
  - Compression benefits must name their tax: draw spent, energy spent, setup turn,
    or opportunity cost.
- Risks:
  - Combat filtering may be over-credited as permanent deck thinning.
  - Curated deck examples can hide starter cleanup cost unless explicitly labeled.
- Next round entry:
  - Add a curve checkpoint review checklist so future checkpoints can be reviewed for
    evidence, authority boundary, phase fit, and missing economy/compression context.

### 2026-04-27 Round 12

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What review checklist should every future `curve_checkpoint` satisfy before it is
    used as an encounter validation prompt?
- Model increment:
  - Added a curve checkpoint review checklist with required review areas, accepted
    review states, and minimum blocking-language checks.
  - Added explicit checks for evidence state, phase fit, player vector reasons,
    deck maturity, economy, compression, enemy pressure, archetype link, cardanalysis
    inputs, stale triggers, and authority boundary.
- Assumptions:
  - A checkpoint can be useful while incomplete, as long as its missing evidence is
    visible.
  - Checklist status should change advisory use, not create pass/fail authority.
- Risks:
  - Checklist language can drift into a gate if future tools use `complete` as a
    blocking requirement.
  - Missing economy or compression context may still be silently ignored if payloads
    omit `unknown` labels.
- Next round entry:
  - Add report-only payload variants for starter, build, pivot, and mature contexts
    so consumers can see how the same contract adapts by phase.

### 2026-04-27 Round 13

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What phase-specific report-only payload variants help consumers understand how the
    same campaign power curve contract should be used at starter, build, pivot, and
    mature checkpoints?
- Model increment:
  - Added compact payload variants for starter baseline, build assembly, pivot
    route-dependent online, and mature ceiling/recovery contexts.
  - Kept each variant qualitative, advisory, and explicit about `must_not_expose`.
- Assumptions:
  - Phase variants should reduce ambiguity for consumers without creating separate
    contracts.
  - Mature variants can mention anti-infinite pressure only as report-only trace or
    review context.
- Risks:
  - Examples may be copied as templates and treated as required fields unless future
    implementation keeps the contract version and optionality clear.
  - Pivot route-dependent examples may overfit to compression-heavy decks if future
    examples do not include non-combo plans.
- Next round entry:
  - Add a future cardanalysis field mapping that names which report-only surfaces can
    supply curve context and which fields must remain advisory.

### 2026-04-27 Round 14

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Which cardanalysis report-only surfaces can feed `campaign_power_curve_model_v1`
    fields, and what must remain advisory?
- Model increment:
  - Added a cardanalysis field mapping draft for deck compression, mechanism-axis
    discovery, card package health, design iteration brief, mechanism fun/health, and
    evidence bundle surfaces.
  - Added mapping rules that keep learned/reranker output, hard gates, legality,
    readiness, and monster numbers outside the curve model.
- Assumptions:
  - Cardanalysis can provide evidence and reason codes before the campaign curve has
    a formal implementation.
  - The curve model should consume report-only signals as context, not as authority.
- Risks:
  - Future integrations may accidentally duplicate existing report-only surfaces
    instead of mapping to the canonical owners.
  - Field mappings may look implementation-ready before fixture contracts exist.
- Next round entry:
  - Add a lab backlog and final handoff section, then run final verification and
    report whether this branch is ready for main-agent review.

### 2026-04-27 Round 15

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What backlog and review handoff should close this 10-question expansion without
    implying implementation readiness?
- Model increment:
  - Added a lab backlog with next entry points for campaign economy review, reward
    pacing review, late-phase anti-infinite wording, checkpoint evidence promotion,
    non-combo deck examples, and eventual report-only implementation planning.
  - Added review readiness language that scopes the branch to docs-only,
    report-only model review.
- Assumptions:
  - This branch is suitable for main-agent review as an exploration artifact, not as
    a runtime implementation.
  - The next highest-value review is comparing the phase/checkpoint assumptions
    against real campaign economy and reward pacing.
- Risks:
  - Backlog items could be mistaken for approved implementation tasks unless future
    work keeps them as exploration entry points.
  - Main-agent review may reject or narrow phase bands after campaign pacing evidence
    is checked.
- Next round entry:
  - Review `starter`, `early`, `build`, `pivot`, `mature`, and `late` round-band
    assumptions against current campaign economy and reward pacing, then mark the
    affected checkpoints as `source_aligned`, `review_needed`, or `stale_assumption`.

### 2026-04-27 Round 16

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - What is the smallest code implementation that turns the lab into a usable
    report-only surface without crossing into gates, runtime behavior, or monster
    numbers?
- Model increment:
  - Promoted the stable implementation target into
    `docs/development/CAMPAIGN_POWER_CURVE_MODEL_V1.md`.
  - Added `campaign_power_curve_report_v1` implementation under
    `tools/combat_analysis/design_engine/campaign_power_curve_model.py`.
  - Added `scripts/run_campaign_power_curve_report.py`, reviewed fixture inputs, core
    model tests, CLI tests, registry wiring, and evidence-bundle section support.
- Assumptions:
  - Current campaign reward and encounter data is enough to source-align starter
    baseline assumptions and keep later-phase economy/compression route context
    explicitly `unknown` or `review_needed`.
  - The first implementation should generate plain-data report artifacts only.
- Risks:
  - Campaign pacing evidence is still thin for `early`, `build`, `pivot`, `mature`,
    and `late`, so those phases remain advisory.
  - Surface registration increases maintenance cost if future work forks a duplicate
    V1 module instead of extending the canonical owner.
- Next round entry:
  - Run focused validation, fix any contract drift, and then ask main-agent review to
    compare phase/checkpoint assumptions against deeper campaign pacing evidence.

### 2026-04-27 Round 17

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - How should checkpoint `evidence_state` defaults stay honest once later-phase
    cases start citing real campaign reward and encounter sources?
- Model increment:
  - Calibrated phase-by-phase `evidence_state` defaults in the canonical
    implementation instead of treating any case with `evidence_refs` as automatically
    `source_aligned`.
  - Added phase-specific `calibration_notes`, `missing_evidence`, and late-phase
    `allowed_use=exploration_prompt` defaults to the report payload.
  - Updated reviewed fixture cases so `early`, `build`, `pivot`, `mature`, and
    `late` checkpoints now cite the current campaign sources that justify their
    advisory status.
- Assumptions:
  - Tutorial encounters/rewards are enough to source-align `starter` baseline loop
    claims.
  - Reward-service and reward-bundle surfaces justify identity/assembly language, but
    not persistent removal, upgrade, transform, or shop-route guarantees.
  - TA encounter files justify pressure-shape language for `pivot` and `mature`,
    without promoting those checkpoints past `review_needed`.
- Risks:
  - Phase calibration can still overstate confidence if future checkpoint authors omit
    `evidence_refs` or reuse `source_aligned` manually.
  - Current calibration is keyed to source visibility, not playtest depth; later
    runtime pacing evidence may still force round-band revisions.
- Next round entry:
  - Compare these calibrated defaults against real campaign block sequencing so
    `early`/`build`/`pivot` round hints reflect actual board pacing, not only reward
    and encounter surface availability.

### 2026-04-27 Round 18

- Branch: `codex/04-27-power-curve-model-lab`
- Minimal question:
  - Should the phase round bands stay as `0-1 / 2-3 / 4-6 / 7-9 / 10-13 / 14+`, or
    be realigned to the actual campaign board windows generated by startup seed and
    thesis blueprint sequencing?
- Model increment:
  - Reviewed the current startup board and confirmed that the default campaign line
    and thesis blueprint both advance in 3-turn windows (`start_turn=0,3,6,9...`).
  - Recalibrated the stable phase bands to `0-2 / 3-5 / 6-8 / 9-11 / 12-14 / 15+`
    so phase boundaries stop cutting across the current board slots.
  - Updated V1 fixtures and template ids so `build`, `pivot`, and secondary
    `mature` examples land inside their calibrated windows.
- Assumptions:
  - The right source of truth for this round is current runtime board geometry, not
    narrative node order alone.
  - A 3-turn window is the smallest honest phase unit while startup seed and thesis
    blueprint both keep `between_blocks=3`.
- Risks:
  - If startup seed cadence or thesis blueprint spacing changes later, these bands
    may go stale even if reward/encounter evidence stays the same.
  - Current calibration still reflects board pacing, not playtest-confirmed combat
    strength pacing.
- Next round entry:
  - Split checkpoint evidence more explicitly by block / reward / encounter support so
    each calibrated phase can say which source class justifies its current label.

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

Initial phase bands are hypotheses for discussion only, but the current version now
tracks the 3-turn board cadence used by startup seed and thesis blueprint spacing:

| Phase | Round Hypothesis | Design Meaning |
| --- | --- | --- |
| `starter` | `0-2` | Baseline deck and first visible board window. Player survival and starter friction dominate. |
| `early` | `3-5` | First identity hints appear in the second board window. Frontload and block reliability still matter more than full engines. |
| `build` | `6-8` | Support density and first payoff alignment matter. Mechanisms are usually assembling, not guaranteed online. |
| `pivot` | `9-11` | The run should start proving an identity. Enemy pressure can ask whether the mechanism survives disruption. |
| `mature` | `12-14` | Core deck shape should be visible. Encounters can test scaling, burst, defense, and fail-state resilience together. |
| `late` | `15+` | Finished or near-finished decks face multi-axis pressure, anti-infinite pressure, and high consequence checks. |

### Deck Maturity State Labels

`deck_maturity_state` describes the deck shell's assembly shape. It is not a
strength verdict and should not decide whether a deck passes an encounter.

Minimum dimensions:

| Dimension | Meaning |
| --- | --- |
| `maturity_label` | The best current assembly label. |
| `support_density` | How much glue, setup, trigger, bridge, or enabling support exists. |
| `payoff_density` | How many cards meaningfully reward the intended mechanism or plan. |
| `bridge_before_payoff` | Whether the deck can reach payoff conditions before the payoff is asked to carry. |
| `starter_pollution` | How much baseline starter drag remains visible. |
| `off_axis_drag` | How many cards pull the deck away from its likely identity. |
| `redundancy` | Whether the plan has substitute pieces instead of one exact line. |
| `fallback_plan` | What the deck does when the main mechanism misses or is disrupted. |

Recommended labels:

| Label | Meaning | Typical Phase Read |
| --- | --- | --- |
| `starter_heavy` | Starter basics still dominate draws and decision points. | Normal in `starter`; pressure signal by `build` if unmitigated. |
| `identity_hint` | One or two cards imply a direction, but the deck lacks density or bridge. | Normal in `early`. |
| `assembling_identity` | Support and payoff are both visible, with named missing prerequisites. | Normal in `build`. |
| `payoff_only` | A high-ceiling card exists without enough support, bridge, or survival window. | Review prompt in `build` or later. |
| `support_dense_payoff_light` | Glue is present, but the deck lacks a meaningful reward for setup. | Can be stable but may lack ceiling. |
| `payoff_dense_support_light` | Multiple payoffs compete before the deck can enable them reliably. | Common pivot risk. |
| `bridge_ready` | The deck has enough setup, draw, energy, or compression to make payoff attempts credible. | Strong `build` or early `pivot` signal. |
| `pivot_ready` | The deck can test its mechanism under light disruption and still show a fallback. | Healthy `pivot` label. |
| `mature_core` | The core shell, support, payoff, redundancy, and fallback are visible. | Expected by `mature`, still advisory. |
| `goodstuff_resilient` | No single mechanism dominates, but broad frontload/defense/scaling answers remain coherent. | Can compensate for lower mechanism identity. |
| `overfocused_brittle` | The deck is concentrated on one line and loses texture when pieces miss or are disrupted. | Review prompt, not failure. |

Labeling rules:

- Prefer the label that best explains the next validation need, not the label that
  sounds strongest.
- `payoff_only` must name the missing support, bridge, survival, compression, or
  economy evidence.
- `goodstuff_resilient` should not hide mechanism absence; it should include the
  axes that compensate for missing identity.
- `mature_core` still needs reason codes for fail-state resilience and pressure
  coverage.
- A deck can move backward when new evidence shows route burden, off-axis drag, or
  starter pollution was understated.
- Do not expose maturity labels as `pass`, `fail`, `ready`, or `blocked`.

### Economy State Labels

`economy_state` describes route evidence and resource pressure. It should explain how
upgrades, removals, shops, events, transforms, healing, and opportunity costs affect
online timing claims.

Minimum dimensions:

| Dimension | Meaning |
| --- | --- |
| `upgrade_progress` | Whether required upgrade breakpoints are absent, assumed, or visible. |
| `removal_access` | What evidence exists for persistent card removal. |
| `shop_window` | Whether a shop can plausibly solve a route need and at what opportunity cost. |
| `event_window` | Whether event help is known, unknown, or too speculative to credit. |
| `transform_quality` | Whether transforms improved alignment, hurt alignment, or remain unknown. |
| `healing_pressure` | Whether survival needs compete with upgrades, removals, or purchases. |
| `resource_surplus` | Whether the run has spare gold, upgrade windows, or routing slack. |
| `route_risk` | How uncertain the economy path remains. |

Recommended labels:

| Label | Meaning | Curve Effect |
| --- | --- | --- |
| `economy_unknown` | Route context is missing or not reviewed. | Keep online claims conditional. |
| `upgrade_breakpoint_absent` | A named upgrade requirement is not visible. | Delay the relevant timing claim. |
| `upgrade_breakpoint_visible` | A named upgrade requirement is satisfied or credibly available. | May advance only that specific claim. |
| `removal_route_visible` | Removal access or actual removal progress is recorded. | Supports compression and route credibility. |
| `removal_opportunity_cost_high` | Removal competes with buying support, upgrading, healing, or relic choices. | Holds or conditions online claims. |
| `shop_window_open` | Shop access could plausibly solve a missing route need. | Supports a route-dependent claim, not guaranteed access. |
| `shop_window_expensive` | Shop solves one need while crowding out another. | Add opportunity-cost notes. |
| `event_route_unknown` | Event help is possible but not evidenced. | Preserve unknown; do not credit as route solution. |
| `transform_quality_known_good` | Transform removed pollution and added aligned value. | Can support route credibility. |
| `transform_quality_unknown` | Transform removed a card but replacement quality is unknown. | Do not treat as pure removal. |
| `healing_pressure_high` | Survival or rest needs compete with upgrades/removals. | Delay or condition power spike assumptions. |
| `economy_surplus_visible` | Spare resource windows are visible after core needs. | May reduce route risk, still advisory. |
| `route_risk_high` | The path to claimed online state depends on uncertain economy events. | Use route-dependent labels. |

Economy-state rules:

- Unknown route context should remain `economy_unknown`, not zero burden.
- A shop or event can support `route_dependent_online`; it cannot prove
  `generally_online` without additional evidence.
- Upgrade labels should name the exact breakpoint they affect.
- Removal and transform should stay separate because transform adds replacement
  quality risk.
- Healing pressure is a first-class economy label when survival competes with power
  growth.
- Economy labels cannot emit pass/fail or hard-gate language.

### Compression State Labels

`compression_state` describes how the effective deck changes across the campaign and
inside an encounter. It must preserve the difference between persistent thinning and
combat-only mitigation.

Minimum dimensions:

| Dimension | Meaning |
| --- | --- |
| `persistent_sources` | Removal or known transform effects that change the deck outside combat. |
| `combat_sources` | Exhaust, self-exhaust, discard, draw, selection, retain, or recursion effects during combat. |
| `deck_size_sensitivity` | How much extra deck size or starter pollution hurts the mechanism. |
| `starter_basic_count` | Visible starter Strike/Defend or equivalent baseline drag. |
| `off_plan_card_count` | Non-starter cards that dilute the intended line. |
| `arrival_timing` | Whether compression arrives before the mechanism needs to work. |
| `compression_tax` | Draw, energy, setup turn, card loss, or opportunity cost paid to compress. |
| `invalid_equivalences` | Compression assumptions that must not be collapsed together. |

Recommended labels:

| Label | Meaning | Curve Effect |
| --- | --- | --- |
| `compression_unknown` | Compression context is missing. | Keep reachability conditional. |
| `no_persistent_thinning` | No out-of-combat thinning is visible. | Do not advance removal progress. |
| `removal_thinning_visible` | Actual or credible persistent removal is recorded. | Supports route-level reachability. |
| `transform_quality_known_good` | Transform removed drag and added aligned value. | Supports route credibility with note. |
| `transform_quality_unknown` | Transform happened, but replacement quality is not known. | Do not count as clean removal. |
| `self_exhaust_setup_visible` | Setup cards remove themselves after use. | Supports in-combat effective thinning. |
| `targeted_exhaust_early` | The deck can remove unwanted cards before the key online window. | Supports conditional online claims. |
| `targeted_exhaust_late` | Exhaust exists but likely arrives after the mechanism needed help. | Keep online timing conditional. |
| `discard_filtering_only` | Discard improves hand quality but does not remove future draws. | Do not count as persistent compression. |
| `draw_selection_only` | Selection finds pieces but does not thin pollution by itself. | Supports reachability only with caveats. |
| `deck_size_sensitive_high` | Reliability falls sharply with extra cards or basics. | Add route-dependent or compression-needed notes. |
| `curated_deck_skips_removal_cost` | Example shell omits starter cleanup cost. | Preserve route burden visibility. |
| `compression_tax_competes_with_assembly` | The compression tool costs the same draw, energy, or turn window the mechanism needs. | Delay or condition online timing. |

Compression-state rules:

- Removal, transform, exhaust, discard filtering, and draw selection should remain
  separate labels even when they all improve a final shell.
- Persistent removal can support `removal_progress`; discard filtering and draw
  selection cannot.
- Transform can support compression only when replacement quality is known or marked
  as unknown with explicit caveats.
- Exhaust supports online timing only when it arrives early enough and does not
  consume the same resources required by the mechanism.
- High deck-size sensitivity should downgrade broad reachability language to
  `online_if_compressed` or `route_dependent_online`.
- Curated examples should record when they skip starter-deck cleanup cost.
- Compression labels cannot produce pass/fail authority.

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

### Player Power Reason Codes

`player_power_reason_code` explains why a player strength vector moved. It should be
visible next to each scalar estimate, because the score is only useful when the
supporting evidence and uncertainty are named.

Minimum reason-code fields:

```json
{
  "code": "draw_bridge_present",
  "axis": "draw_velocity",
  "polarity": "supports",
  "evidence_scope": "deck_state",
  "phase_relevance": ["build", "pivot"],
  "uncertainty": "route_context_unknown"
}
```

Recommended fields:

| Field | Meaning |
| --- | --- |
| `code` | Stable short label such as `upgrade_breakpoint_met` or `starter_pollution_high`. |
| `axis` | One player strength vector field or `multi_axis`. |
| `polarity` | `supports`, `pressures`, `conditions`, or `unknown`. |
| `evidence_scope` | `deck_state`, `route_state`, `combat_state`, `encounter_observed`, or `assumption`. |
| `phase_relevance` | Phase labels where the reason matters most. |
| `uncertainty` | Named missing evidence, not an implied zero. |

Reusable reason-code families:

| Family | Example Codes | Typical Axes |
| --- | --- | --- |
| `frontload_access` | `efficient_attack_added`, `early_tempo_upgrade`, `frontload_still_starter_bound` | `frontload`, `fail_state_resilience` |
| `defense_reliability` | `redundant_block_sources`, `block_draw_variance`, `defense_scaling_bridge` | `block_reliability`, `fail_state_resilience` |
| `draw_and_selection` | `draw_bridge_present`, `selection_reduces_miss`, `draw_disruption_sensitive` | `draw_velocity`, `combo_reachability` |
| `energy_window` | `upgrade_breakpoint_met`, `temporary_energy_burst`, `energy_tax_sensitive` | `energy_burst`, `combo_reachability` |
| `compression_route` | `persistent_removal_seen`, `targeted_exhaust_bridge`, `discard_filtering_not_persistent` | `deck_compression`, `removal_progress`, `mechanism_online_rate` |
| `mechanism_support` | `support_before_payoff`, `payoff_without_bridge`, `trigger_density_low` | `mechanism_online_rate`, `scaling` |
| `combo_alignment` | `pieces_align_with_draw`, `state_prerequisite_missing`, `exactness_route_unknown` | `combo_reachability`, `mechanism_online_rate` |
| `fail_state_backup` | `backup_frontload_plan`, `fallback_block_plan`, `main_plan_miss_brittle` | `fail_state_resilience`, `frontload`, `block_reliability` |
| `route_uncertainty` | `shop_access_unknown`, `transform_quality_unknown`, `removal_opportunity_cost_high` | `removal_progress`, `deck_compression`, `mechanism_online_rate` |

Reason-code rules:

- Each non-zero score should have at least one supporting, conditioning, or pressure
  reason code.
- A score increase from route evidence should name whether the route is known,
  assumed, or unknown.
- Negative codes should use `pressures` or `conditions`; they should not emit
  `fail`, `reject`, or `invalid`.
- Scalar-only output is incomplete for this model. If reason codes are missing, the
  checkpoint should report `reason_codes_missing`.
- The same code may affect multiple axes, but the payload should name the affected
  axes explicitly instead of hiding the relationship in prose.
- Codes should stay stable enough for later cardanalysis mapping; one-off prose can
  live in `notes`.

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

### Economy And Compression Timing Modifiers

`economy_state` and `compression_state` modify the honesty of online timing claims.
They do not make a mechanism legal, strong, or validated by themselves.

Use modifiers when the same final-shell read could mean different campaign realities:

- the final shell is coherent, but removals are missing
- the core card is upgraded, but support density is still thin
- the deck filters well in-combat, but persistent starter pollution remains
- shop access could solve the route, but only by spending the same economy needed for
  core cards, upgrades, or survival

#### Modifier Labels

| Label | Meaning | Online Timing Effect |
| --- | --- | --- |
| `advance_online_claim` | Route or compression evidence makes an earlier online label more credible. | May move `assembling` toward `conditional_online`, or `conditional_online` toward `online`, with reasons. |
| `hold_conditional` | Evidence supports activation, but route, economy, or compression gaps remain visible. | Keep `conditional_online` even if final-shell viability looks high. |
| `delay_online_claim` | Missing route or compression evidence makes the online claim too optimistic for the phase. | Move `online` wording toward `conditional_online`, `online_if_compressed`, or `route_dependent_online`. |
| `route_dependent` | The mechanism can work, but depends on unverified shop, event, removal, transform, or upgrade access. | Keep online timing advisory and require route notes. |
| `stale_check_needed` | A prior online assumption may no longer fit current reward, economy, or card-pool pacing. | Do not use the timing claim for new encounter validation until reviewed. |

#### Economy Inputs

| Input | Can Advance Timing When | Should Delay Or Condition Timing When |
| --- | --- | --- |
| `upgrade_progress` | A required cost, damage, block, draw, or state breakpoint is already upgraded. | The upgrade competes with survival, core card purchase, or another required breakpoint. |
| `removal_access` | Actual removals happened, or route evidence makes starter cleanup plausible. | Access is unknown, unaffordable, or competing with core purchases. |
| `shop_window` | The route has a known shop window and enough economy for the needed action. | The shop is hypothetical, too late, or its opportunity cost is high. |
| `transform_access` | Replacement quality is known or bounded as on-axis/low-risk. | Replacement quality is unknown, off-axis, high-cost, or could break exactness. |
| `event_access` | The event is observed or explicitly part of a reviewed route note. | The event is only speculative and should not be counted as available. |
| `healing_pressure` | The deck can spend economy on upgrades/removal without risking survival. | Healing needs consume the same route budget needed to bring the mechanism online. |

#### Compression Inputs

| Input | Can Advance Timing When | Should Delay Or Condition Timing When |
| --- | --- | --- |
| `persistent_removal` | It lowers starter/off-axis pollution before the key phase. | The model only assumes removal because the final shell is compact. |
| `transform` | The replacement is known to be low-cost, on-axis, or harmless to exactness. | The replacement is unknown or could introduce new draw, cost, or exactness friction. |
| `self_exhaust_setup` | Setup cards remove themselves before repeat cycles matter. | The setup must be drawn late or competes with the payoff turn. |
| `targeted_exhaust` | It can remove off-plan cards early enough and safely choose targets. | It arrives after the online window or risks exhausting required pieces. |
| `bulk_exhaust` | It supports the mechanism and has bounded collateral risk. | It clears too broadly and can erase support, payoff, or defense. |
| `discard_filtering` | It improves hand quality enough to support a conditional claim. | It is being counted as persistent thinning. |
| `draw_selection` | It finds pieces without pretending the deck became smaller. | It hides starter pollution or first-cycle survival risk. |

#### Modifier Payload

Future checkpoints may attach:

```json
{
  "online_timing_modifiers": {
    "evaluation_mode": "report_only",
    "economy_modifiers": [
      {
        "source": "removal_access",
        "label": "route_dependent",
        "reason_codes": [
          "starter_basics_still_visible",
          "shop_access_unknown"
        ]
      }
    ],
    "compression_modifiers": [
      {
        "source": "targeted_exhaust",
        "label": "hold_conditional",
        "reason_codes": [
          "can_remove_pollution_in_combat",
          "must_draw_compressor_before_loop_window"
        ]
      }
    ],
    "net_timing_read": "conditional_online_route_dependent",
    "must_not_expose": ["overall_pass", "hard_gates"]
  }
}
```

Required conventions:

- `net_timing_read` should be explanatory, such as
  `conditional_online_route_dependent`, not a pass/fail verdict.
- Unknown economy access should stay `unknown`; do not silently treat it as no burden
  or guaranteed access.
- Persistent removal is stronger route evidence than discard filtering.
- Transform must record replacement-quality assumptions.
- In-combat compression can support `conditional_online`; it should only support
  `online` when arrival timing and survival cost are also visible.
- Upgrade progress can advance timing only for the specific breakpoint it solves.
- Healing pressure can delay online timing when survival consumes the same economy
  needed for removal, upgrades, or shop purchases.

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

### Enemy Pressure Phase Bands

`enemy_pressure_phase_band` is a qualitative advisory layer for archetypes and
checkpoints. It keeps pressure language consistent while avoiding monster stat
implementation.

Band meanings:

| Band | Meaning | Must Not Mean |
| --- | --- | --- |
| `avoid` | Do not use this pressure as a normal phase expectation. | The axis is illegal or can never appear. |
| `trace` | Mention only as observation or light texture. | A hidden numeric minimum. |
| `low` | Small prompt that should not dominate the encounter question. | Guaranteed low damage or trivial enemy behavior. |
| `medium` | Main pressure axis for the phase or archetype. | A fixed balance target. |
| `high` | Strong late or special-purpose validation pressure that needs a reason. | Permission to hard-counter the player. |
| `spike_only` | Use only for an explicit one-off pressure spike or scripted validation beat. | A default phase expectation. |

Default phase bands:

| Phase | Normal Medium Axes | Low Or Trace Axes | Caution / Avoid Axes |
| --- | --- | --- | --- |
| `starter` | `frontload_damage`, `defense_check` | `multi_enemy_pressure` | avoid `draw_disruption`, `energy_tax`, `mechanism_disruption`, `anti_infinite_pressure` |
| `early` | `frontload_damage`, `defense_check` | `multi_enemy_pressure`, `status_pollution` | avoid `mechanism_disruption`; keep `draw_disruption` trace only |
| `build` | `frontload_damage`, `defense_check`, `multi_enemy_pressure` | `status_pollution`, `draw_disruption`, `energy_tax` | avoid hard mechanism disruption and anti-infinite pressure |
| `pivot` | `defense_check`, `draw_disruption`, `mechanism_disruption`, `status_pollution` | `frontload_damage`, `energy_tax`, `scaling_race` | keep `anti_infinite_pressure` trace only |
| `mature` | `scaling_race`, `defense_check`, `burst_check`, `mechanism_disruption` | `draw_disruption`, `energy_tax`, `multi_enemy_pressure` | use anti-infinite pressure only as report-only low/trace |
| `late` | `scaling_race`, `burst_check`, `defense_check`, `multi_enemy_pressure` | `draw_disruption`, `energy_tax`, `mechanism_disruption`, `anti_infinite_pressure` | `high` anti-infinite pressure needs explicit review context |

Band use rules:

- A checkpoint may request only qualitative bands unless a later monster-tuning owner
  explicitly creates a numeric implementation.
- `high` should name the validation reason and the expected observation, not a
  damage or health target.
- `avoid` means "not a default ask for this phase"; it can be overridden only by a
  named tutorial, boss, elite, or special validation context.
- `spike_only` should record why the spike exists and which normal phase assumption
  it is intentionally testing.
- A pressure band cannot produce `overall_pass`, `overall_fail`, `hard_gate`, or
  readiness authority.
- If several axes are `medium` or higher, the archetype should state the primary
  design question so the encounter does not become an unfocused all-axis test.

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

### Report-Only Payload Variants

These variants show how the same contract can be narrowed by phase. They are examples,
not schemas or implementation requirements.

#### `starter_payload_variant`

```json
{
  "campaign_power_curve_model": {
    "contract_version": "campaign_power_curve_model_v1",
    "evaluation_mode": "report_only",
    "campaign_round": {"phase": "starter", "round_index": 1},
    "curve_checkpoint": {
      "checkpoint_id": "starter_round_1_baseline_survival_v0",
      "evidence_state": {"label": "hypothesis_draft"},
      "review_only_verdict": "baseline_observation_needed",
      "must_not_expose": ["overall_pass", "hard_gates", "monster_numbers"]
    },
    "player_power_state_focus": [
      "frontload",
      "block_reliability",
      "fail_state_resilience"
    ],
    "deck_maturity_state": {
      "maturity_label": "starter_heavy",
      "starter_pollution": "expected"
    },
    "mechanism_online_state": {"online_label": "absent"},
    "enemy_pressure_profile": {
      "frontload_damage": "medium",
      "defense_check": "medium",
      "status_pollution": "avoid",
      "mechanism_disruption": "avoid"
    },
    "encounter_validation_needs": [
      "baseline_survival_visibility",
      "no_mechanism_required"
    ]
  }
}
```

#### `build_payload_variant`

```json
{
  "campaign_power_curve_model": {
    "contract_version": "campaign_power_curve_model_v1",
    "evaluation_mode": "report_only",
    "campaign_round": {"phase": "build", "round_index": 5},
    "curve_checkpoint": {
      "checkpoint_id": "build_round_5_identity_assembly_v0",
      "evidence_state": {"label": "hypothesis_draft"},
      "review_only_verdict": "assembly_shape_needs_validation",
      "must_not_expose": ["overall_pass", "hard_gates", "monster_numbers"]
    },
    "player_power_state_focus": [
      "frontload",
      "draw_velocity",
      "mechanism_online_rate",
      "fail_state_resilience"
    ],
    "deck_maturity_state": {
      "maturity_label": "assembling_identity",
      "payoff_risk": "payoff_only_if_bridge_missing"
    },
    "mechanism_online_state": {"online_label": "assembling"},
    "economy_state": {"route_risk": "unknown"},
    "compression_state": {"compression_context": "unknown"},
    "encounter_archetype_id": "build_payoff_only_detector"
  }
}
```

#### `pivot_payload_variant`

```json
{
  "campaign_power_curve_model": {
    "contract_version": "campaign_power_curve_model_v1",
    "evaluation_mode": "report_only",
    "campaign_round": {"phase": "pivot", "round_index": 8},
    "curve_checkpoint": {
      "checkpoint_id": "pivot_round_8_conditional_online_v0",
      "evidence_state": {"label": "hypothesis_draft"},
      "review_only_verdict": "route_dependent_online_needs_probe",
      "must_not_expose": ["overall_pass", "hard_gates", "monster_numbers"]
    },
    "mechanism_online_state": {
      "online_label": "conditional_online",
      "missing_prerequisites": ["removal_route", "first_cycle_survival"]
    },
    "economy_state": {"route_risk": "high", "removal_access": "unknown"},
    "compression_state": {
      "deck_size_sensitivity": "high",
      "invalid_equivalences": ["discard_filtering_is_not_persistent_removal"]
    },
    "enemy_pressure_profile": {
      "draw_disruption": "medium",
      "mechanism_disruption": "medium",
      "energy_tax": "low",
      "anti_infinite_pressure": "trace"
    },
    "encounter_archetype_id": "pivot_compression_route_probe"
  }
}
```

#### `mature_payload_variant`

```json
{
  "campaign_power_curve_model": {
    "contract_version": "campaign_power_curve_model_v1",
    "evaluation_mode": "report_only",
    "campaign_round": {"phase": "mature", "round_index": 12},
    "curve_checkpoint": {
      "checkpoint_id": "mature_round_12_ceiling_and_recovery_v0",
      "evidence_state": {"label": "hypothesis_draft"},
      "review_only_verdict": "ceiling_and_recovery_need_observation",
      "must_not_expose": ["overall_pass", "hard_gates", "monster_numbers"]
    },
    "deck_maturity_state": {"maturity_label": "mature_core"},
    "mechanism_online_state": {"online_label": "online_or_strong_conditional"},
    "player_power_state_focus": [
      "scaling",
      "block_reliability",
      "combo_reachability",
      "fail_state_resilience"
    ],
    "enemy_pressure_profile": {
      "scaling_race": "medium",
      "burst_check": "medium",
      "defense_check": "medium",
      "anti_infinite_pressure": "trace"
    },
    "encounter_archetype_id": "mature_scaling_burst_and_fail_state_check"
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

## Curve Checkpoint Review Checklist

The checklist helps a designer or future tool review whether a `curve_checkpoint` is
usable as an encounter validation prompt. It is not a gate and does not authorize
monster numbers.

Checklist status labels:

| Status | Meaning |
| --- | --- |
| `not_started` | The checkpoint has not been reviewed for this area. |
| `present` | The area exists, but quality or evidence has not been reviewed. |
| `review_needed` | The area is present and has a named uncertainty. |
| `reviewed_advisory` | The area is reviewed enough for advisory planning. |
| `stale_check_needed` | A known change may invalidate the checkpoint. |
| `out_of_scope` | The area is intentionally not part of this checkpoint. |

Required review areas:

| Area | Minimum Question | Required Output |
| --- | --- | --- |
| `checkpoint_identity` | Does the checkpoint name phase, round hint, design question, and evidence state? | `checkpoint_id`, `phase`, `round_index_hint`, `design_question`, `evidence_state` |
| `authority_boundary` | Does it clearly avoid pass/fail, hard gates, and monster stat authority? | `evaluation_mode=report_only`, `authority_boundary`, `must_not_expose` |
| `phase_fit` | Does the pressure fit the phase band or name why it intentionally spikes? | `phase_read`, `enemy_pressure_phase_band`, optional `spike_reason` |
| `player_power_reasoning` | Do player vector scores carry reason codes and uncertainty? | `player_power_reason_code` entries or `reason_codes_missing` |
| `deck_maturity` | Does the checkpoint name assembly shape rather than only strength? | `maturity_label`, density notes, fallback visibility |
| `mechanism_online` | Does it state absent/assembling/conditional/online/over-online with prerequisites? | `mechanism_online_timing`, activation paths, missing prerequisites |
| `economy_context` | Are upgrades, removals, shops, events, transforms, healing, and opportunity costs known or unknown? | `economy_state` labels, `route_risk` |
| `compression_context` | Are removal, transform, exhaust, filtering, selection, and deck-size sensitivity separated? | `compression_state` labels and invalid equivalences |
| `enemy_pressure` | Does the pressure request state the encounter question, not monster numbers? | pressure axes, qualitative bands, primary validation question |
| `encounter_archetype` | Is the checkpoint tied to a validation shape or intentionally archetype-free? | `encounter_archetype_id` or `out_of_scope` note |
| `cardanalysis_inputs` | Are upstream report-only signals named without making them authority? | source surfaces, missing source evidence, `advisory_only` |
| `staleness` | What changes would make the checkpoint unreliable? | stale triggers and freshness label |
| `next_evidence` | What should the next run, review, or playtest observe? | concrete evidence need, not a verdict |

Review rules:

- A checkpoint with missing evidence can still be used as a `discussion_seed` or
  `validation_prompt` if the missing evidence is explicit.
- `reviewed_advisory` does not mean balanced, final, or ready for implementation.
- Any checkpoint that exposes `overall_pass`, `hard_gates`, `blocking_verdict`, or
  monster stat targets is outside V1.
- `stale_check_needed` should preserve the checkpoint for history while stopping it
  from being treated as current planning context.
- If economy or compression context is unknown, the checklist should say `unknown`;
  it should not leave the field blank.

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

### `build_payoff_only_detector`

- Phases: `build`
- Reads modifiers:
  - `hold_conditional`
  - `delay_online_claim`
  - early `route_dependent`
- Primary pressure:
  - `frontload_damage`
  - `defense_check`
  - low `multi_enemy_pressure`
  - low `status_pollution`
- Validation question:
  - Does the deck have support, bridge, and survival evidence behind its payoff, or
    is it carrying a high-ceiling card that cannot shape the build phase yet?
- Interpretation boundary:
  - Report `payoff_supported`, `bridge_missing`, `survival_window_missing`, or
    `route_context_unknown`; do not report pass/fail.
- Avoid:
  - requiring final-shell compression
  - punishing every non-online mechanism
  - using status or disruption high enough to test pivot assumptions too early

### `pivot_compression_route_probe`

- Phases: `pivot`
- Reads modifiers:
  - `route_dependent`
  - `stale_check_needed`
  - `hold_conditional`
- Primary pressure:
  - `draw_disruption`
  - `energy_tax`
  - `mechanism_disruption`
  - `defense_check`
  - optional low-to-medium `status_pollution`
- Validation question:
  - Is the mechanism conditionally online because of ordinary draw/resource variance,
    or because the deck still needs a credible removal, transform, or early exhaust
    route before the claim is honest?
- Interpretation boundary:
  - Report the missing route evidence directly; do not treat missing removal,
    transform quality, or early exhaust access as a failure state.
- Avoid:
  - hard counters to the exact mechanism
  - equating discard filtering with persistent deck compression
  - assuming shop, event, or transform access is guaranteed

### `mature_over_online_texture_probe`

- Phases: `mature`, `late`
- Reads modifiers:
  - `advance_online_claim`
  - `stale_check_needed`
  - `over_online`
- Primary pressure:
  - `scaling_race`
  - `burst_check`
  - `defense_check`
  - `mechanism_disruption`
  - trace or low report-only `anti_infinite_pressure`
- Validation question:
  - Does a highly repeatable mechanism still leave meaningful encounter texture,
    constraints, and recovery questions, or does it flatten the requested pressure?
- Interpretation boundary:
  - Report `texture_visible`, `constraints_visible`, `pressure_flattened_risk`, or
    `anti_infinite_review_needed`; do not declare a loop invalid.
- Avoid:
  - monster numbers
  - legality language
  - treating a high-ceiling combo as unhealthy by category

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

### Cardanalysis Field Mapping Draft

This mapping is a future integration draft. It does not create a new report-only
surface, CLI, fixture contract, or default entrypoint.

| Cardanalysis Surface | Campaign Curve Fields | Advisory Use | Must Not Do |
| --- | --- | --- | --- |
| `deck_compression_report_v1` | `compression_state`, `removal_progress`, `deck_compression`, `combo_reachability`, `online_timing_modifier` | Explain route-dependent online claims, starter pollution, curated deck cleanup cost, and invalid compression equivalences. | Do not convert compression burden into hard failure or exact route probability. |
| `mechanism_axis_discovery_v1` | `mechanism_online_state`, `mechanism_online_timing`, `mechanism_online_rate`, `combo_reachability` | Name candidate mechanism identity, foundation-axis dependency, activation paths, and missing prerequisites. | Do not select campaign phase, project temperament, legality, or encounter readiness. |
| `card_package_health_v1` | `deck_maturity_state`, `support_density`, `payoff_density`, `off_axis_drag`, `bridge_before_payoff` | Distinguish assembling identity, payoff-only risk, bridge readiness, redundancy, and slot-fit pressure. | Do not promote package health to deck pass/fail or recommendation authority. |
| `design_iteration_brief_v1` | `fail_state_resilience`, `setup_burden`, `next_evidence`, `encounter_validation_needs` | Surface setup burden, brittle fail states, backup-plan visibility, and next validation prompts. | Do not create blocking design verdicts or monster tuning requirements. |
| `mechanism_fun_health_v1` | `over_online` notes, texture risk, degeneracy signals, recovery questions | Provide advisory language for texture flattening, anti-infinite review prompts, and health discussion context. | Do not declare loops invalid or change hard gates. |
| `cardanalysis_evidence_bundle_v1` | `evidence_refs`, `source_aligned` evidence state, missing source evidence | Attach source refs and cross-surface evidence summaries. | Do not resolve conflicts as pass/fail authority. |
| learned/reranker shadow output | optional `notes` only after explicit review | Can be cited as experimental context if default-off and clearly labeled. | Must not decide phase, legality, gate status, or curve checkpoint readiness. |

Suggested mapping payload:

```json
{
  "cardanalysis_curve_mapping": {
    "contract_version": "campaign_curve_cardanalysis_mapping_draft_v1",
    "evaluation_mode": "report_only",
    "source_surface": "deck_compression_report_v1",
    "mapped_curve_fields": [
      "compression_state",
      "removal_progress",
      "online_timing_modifier"
    ],
    "reason_codes": [
      "curated_deck_skips_removal_cost",
      "discard_filtering_is_not_persistent_removal"
    ],
    "missing_evidence": ["campaign_route_context"],
    "authority_boundary": "advisory_context_only"
  }
}
```

Mapping rules:

- Use canonical report-only owners from the registry instead of creating duplicate V1
  surfaces with overlapping meaning.
- Keep `evaluation_mode=report_only` visible in any exchanged context.
- Missing cardanalysis evidence should remain `missing_evidence`, not become a zero
  score or hidden no-burden assumption.
- Learned/reranker shadow output can be cited only as explicitly reviewed context and
  must stay default-off.
- The campaign curve model may request `encounter_validation_needs`; cardanalysis
  must not turn those needs into monster stats or hard recommendations.

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

## Lab Backlog And Review Handoff

This backlog records next exploration entry points. It does not approve runtime work,
monster implementation, default recommendation changes, learned/reranker promotion, or
hard-gate behavior.

### Next Entry Points

| Priority | Entry Point | Intended Output |
| --- | --- | --- |
| `P0` | Compare phase round bands against real campaign economy and reward pacing. | Update phase assumptions and checkpoint evidence states. |
| `P0` | Review the four V0 checkpoints against campaign rewards, route choices, and encounter observations. | Mark checkpoints `source_aligned`, `review_needed`, or `stale_assumption`. |
| `P1` | Add `late` checkpoint examples after mature fail-state and anti-infinite language is reviewed. | Late-phase checkpoint draft with trace-only anti-infinite boundary. |
| `P1` | Add non-combo and goodstuff deck examples to avoid overfitting the curve model to infinites or exactness shells. | Example checkpoints for frontload/defense/scaling decks without a dominant mechanism. |
| `P1` | Add encounter archetype examples for status-heavy and multi-enemy pressure once phase bands are reviewed. | Qualitative archetype sketches with pressure-band justifications. |
| `P2` | Draft a future report-only implementation contract after main-agent review. | Contract proposal only; no CLI, fixture, or default path yet. |
| `P2` | Decide whether `campaign_power_curve_context_v1` should be exported to cardanalysis reports. | RFC or design note with owner and validation level. |

### Review Readiness

- `ready_for_main_agent_review`: yes, for docs-only exploration review.
- Review scope:
  - vocabulary completeness
  - report-only boundary
  - phase/checkpoint reasonableness
  - cardanalysis mapping sanity
  - missing economy/reward evidence
- Not ready for:
  - monster numbers
  - runtime implementation
  - hard gates
  - recommendation default changes
  - learned/reranker promotion

### Handoff Checklist

- Confirm all payload examples keep `evaluation_mode=report_only`.
- Confirm no payload exposes `overall_pass`, `hard_gates`, or blocking readiness
  verdicts.
- Confirm economy and compression unknowns remain explicit.
- Confirm encounter archetypes request validation questions rather than enemy stats.
- Confirm cardanalysis mappings reference canonical report-only surfaces.
