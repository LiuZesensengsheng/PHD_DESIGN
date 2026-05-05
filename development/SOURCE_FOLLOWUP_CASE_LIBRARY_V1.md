# Source Followup Case Library V1

- Library: `source_followup_case_library_v1`
- Contract: `cardanalysis_case_input_v1`
- Status: bootstrap case library for blocked source followups
- Runtime impact: none

## Purpose

This library gives source-mined and generated followup items a safe review
exit. It turns queue targets into human-curated review notes without promoting
the source material to reviewed evidence.

The library is intentionally narrow. It records what a reviewer should inspect
next, which assumptions remain unresolved, and which consumers may use the case
as advisory context. It does not decide whether the original hypothesis is true,
balanced, viable, or ready for family promotion.

## Source Targets

The V1 bootstrap handles the current `source_followup` items emitted by
`coverage_guided_case_queue_v1`:

- `generated_chain_fatigue_hypothesis_case_v1`
- `generated_hypothesis_private_leak_case_v1`
- `generated_loop_safety_break_hypothesis_case_v1`
- `generated_pollution_market_hypothesis_case_v1`

The long-running case-library lane also adds followup review notes for:

- `generated_defense_reflect_hypothesis_case_v1`
- `generated_draw_heat_budget_hypothesis_case_v1`
- `generated_energy_instability_hypothesis_case_v1`
- `generated_recovery_window_validator_enemy_case_v1`
- `generated_redirect_collision_hypothesis_case_v1`
- `generated_search_public_target_hypothesis_case_v1`
- `generated_summon_expiry_hypothesis_case_v1`
- `generated_status_decay_transfer_hypothesis_case_v1`
- `generated_temporary_generation_memory_budget_hypothesis_case_v1`
- `generated_transform_pool_exhaust_hypothesis_case_v1`
- `source_mined_anti_infinite_soft_pressure_enemy_case_v1`
- `source_mined_chain_fatigue_reference_case_v1`
- `source_mined_draw_disruption_enemy_case_v1`
- `source_mined_charge_decay_reference_case_v1`
- `source_mined_mode_cooldown_reference_case_v1`
- `source_mined_draw_external_reset_reference_case_v1`
- `source_mined_discard_reserve_reference_case_v1`
- `source_mined_charge_decay_reference_v2_case_v1`
- `source_mined_mode_lockout_reference_v2_case_v1`
- `source_mined_gremlin_nob_skill_punish_frontload_reference_case_v1`
- `source_mined_jaw_worm_frontload_defense_reference_case_v1`
- `source_mined_position_zone_reference_case_v1`
- `source_mined_position_zone_reference_v2_case_v1`
- `source_mined_public_thread_reference_case_v1`
- `source_mined_stress_cost_reference_case_v1`
- `source_mined_social_texture_case_v1`
- `source_mined_starter_agency_route_choice_reference_case_v1`
- `source_mined_starter_cultist_scaling_clock_case_v1`
- `source_mined_starter_first_three_encounter_mix_case_v1`
- `source_mined_summon_slot_reference_case_v1`
- `source_mined_threshold_overflow_reference_v2_case_v1`
- `source_mined_reference_case_v1`
- `late_round_15_texture_review`

Each followup case stores the original target id and queue id under
`contexts.campaign` and `contexts.experience.source_followup`.

## Contract Use

The fixture pack continues to use the shared normalized case contract:

- `source.source_type = "design_note"`
- `source.evidence_tier = "human_curated"`
- `source.review_status = "review_needed"`
- `authority.authority_boundary = "advisory_context_only"`

The followup cases use existing fields only:

| Followup meaning | Existing field convention |
| --- | --- |
| Original queue item | `contexts.campaign.queue_id` |
| Original source case | `contexts.campaign.target_case_id` and `contexts.experience.source_followup.target_case_id` |
| Review plan | `contexts.experience.source_followup.review_questions` |
| Evidence still needed | `contexts.experience.source_followup.human_curated_evidence_needed` |
| Review risk | `observed_behavior.failure_modes`, `labels.negative`, and `labels.uncertain` |
| Candidate hints | `feature_hints` |
| Authority limits | `known_limits` and `authority.forbidden_uses` |

These are review-note conventions inside the shared contract, not a second
schema.

## Authority Boundary

All V1 cases remain below reviewed authority.

They must not be used for:

- reviewed evidence claims;
- hard-gate promotion;
- reviewed mechanism-family promotion;
- default synthesis or recommendation;
- evaluator logic changes;
- capability graph or report-only registry changes;
- runtime, persistence, UI, or learned/reranker paths.

The fixture pack therefore includes `reviewed_evidence_claim` in
`authority.forbidden_uses` even though its immediate source type is
`design_note`. This preserves the boundary that the underlying target cases are
generated hypotheses.

## Fixture Pack

The V1 fixture pack lives at:

```text
tests/fixtures/combat_analysis/source_followup_case_library_v1/
```

Coverage:

- chain fatigue followup review note;
- private leak followup review note;
- loop safety break followup review note;
- pollution market followup review note.
- defense reflect followup review note;
- draw heat budget followup review note;
- energy instability followup review note;
- recovery window validator followup review note;
- redirect collision followup review note;
- search public target followup review note;
- summon expiry followup review note;
- status decay transfer followup review note;
- temporary generation memory budget followup review note;
- transform pool exhaust followup review note;
- anti-infinite soft pressure followup review note;
- chain fatigue reference followup review note;
- draw disruption enemy followup review note;
- charge decay reference followup review note.
- mode cooldown reference followup review note;
- draw external reset reference followup review note;
- discard reserve reference followup review note;
- charge decay v2 reference followup review note;
- mode lockout v2 reference followup review note;
- position zone reference followup review note;
- public thread reference followup review note;
- stress cost reference followup review note.
- social texture followup review note;
- campaign pressure reference followup review note;
- late-round texture followup review note.
- Gremlin Nob skill-punish frontload reference followup review note;
- Jaw Worm frontload defense reference followup review note;
- position zone v2 reference followup review note;
- starter agency route-choice reference followup review note;
- starter Cultist scaling-clock reference followup review note;
- starter first-three encounter mix followup review note;
- summon slot reference followup review note;
- threshold overflow reference followup review note;
- defense reflect counterplay deepening followup review note;
- draw heat budget stop-point deepening followup review note;
- energy instability stabilize deepening followup review note;
- loop safety break breakpoint deepening followup review note;
- pollution market washout deepening followup review note;
- recovery window validator relief deepening followup review note;
- redirect collision lane-pressure deepening followup review note.
- chain fatigue branch-cap deepening followup review note;
- chain fatigue offramp recovery deepening followup review note;
- private leak redaction-boundary deepening followup review note;
- private leak escalation-cap deepening followup review note;
- search public target visibility deepening followup review note;
- search public target consent-cost deepening followup review note;
- summon expiry warning-window deepening followup review note;
- status decay transfer destination deepening followup review note;
- temporary generation cleanup-checkpoint deepening followup review note;
- transform pool exhaust refresh-policy deepening followup review note;
- defense reflect damage-ceiling deepening followup review note;
- draw heat recovery-cooldown deepening followup review note;
- energy instability debt-floor deepening followup review note;
- loop safety break reset-audit deepening followup review note;
- pollution market price-floor deepening followup review note.
- recovery window validator rebuild-budget deepening followup review note;
- recovery window validator pressure-reentry deepening followup review note;
- redirect collision resolution-order deepening followup review note;
- redirect collision partial-value deepening followup review note;
- defense reflect enemy-signal deepening followup review note;
- draw heat hand-clog deepening followup review note;
- energy instability refund-loop deepening followup review note;
- private leak source-reliability deepening followup review note;
- chain fatigue counterplay-signal deepening followup review note;
- loop safety break terminal-payoff deepening followup review note;
- pollution market sink-capacity deepening followup review note;
- search public target pool-staleness deepening followup review note;
- status decay transfer counterplay deepening followup review note;
- summon expiry support-density deepening followup review note;
- temporary generation expire-value deepening followup review note.
- anti-infinite soft-pressure visibility deepening followup review note;
- chain fatigue reference meter-readability deepening followup review note;
- charge decay reference spend-timing deepening followup review note;
- charge decay v2 reference threshold-warning deepening followup review note;
- discard reserve reference access-window deepening followup review note;
- draw disruption enemy recovery-signal deepening followup review note;
- draw external reset reference-boundary deepening followup review note;
- Gremlin Nob skill-punish escape-line deepening followup review note;
- Jaw Worm frontload defense recovery-line deepening followup review note;
- mode cooldown reference reentry-signal deepening followup review note;
- mode lockout v2 reference soft-lock escape deepening followup review note;
- position zone reference entry-cost deepening followup review note;
- position zone v2 reference overlap-rule deepening followup review note;
- public thread reference moderation-window deepening followup review note;
- campaign pressure reference review-lens deepening followup review note.
- chain fatigue exit-value audit followup review note;
- chain fatigue reset-visibility followup review note;
- defense reflect block-source separation followup review note;
- defense reflect overkill-waste followup review note;
- draw heat priority-queue followup review note;
- draw heat dead-draw recovery followup review note;
- energy instability volatility-preview followup review note;
- energy instability debt-recovery choice followup review note;
- private leak consent-scope followup review note;
- private leak delayed-reveal followup review note;
- loop safety break fail-closed followup review note;
- pollution market burden-entry visibility followup review note;
- recovery window validator frequency-audit followup review note;
- redirect collision fallback-preview followup review note;
- search public target relevance-decay followup review note.
- chain fatigue floor negative-control followup review note;
- chain fatigue branching-trace followup review note;
- defense reflect multihit-intent followup review note;
- defense reflect carryover-leak followup review note;
- draw heat reshuffle-pressure followup review note;
- draw heat discard-mitigation followup review note;
- energy instability floor-ceiling band followup review note;
- energy instability payoff-timing split followup review note;
- private leak audience-containment followup review note;
- private leak repair-path followup review note;
- loop safety break fallback-cashout followup review note;
- pollution market sink-scarcity signal followup review note;
- recovery window archetype-sensitivity followup review note;
- redirect collision multitarget-conflict followup review note;
- search public target refresh-cost followup review note.
- chain fatigue resource-blend followup review note;
- chain fatigue enemy-pressure interlock followup review note;
- defense reflect no-attack-intent followup review note;
- defense reflect delayed-cashout followup review note;
- draw heat hand-size breakpoint followup review note;
- draw heat skip-draw agency followup review note;
- energy instability stabilizer-density followup review note;
- energy instability temporary-energy expiry followup review note;
- private leak contradictory-source followup review note;
- private leak social-cooldown followup review note;
- loop safety break visible-threshold followup review note;
- pollution market cleanup-timing followup review note;
- recovery window telegraph-honesty followup review note;
- redirect collision enemy-intent mismatch followup review note;
- search public target pool-ownership followup review note.
- chain fatigue visible-token burden followup review note;
- defense reflect damage-attribution followup review note;
- draw heat voluntary-discard timing followup review note;
- energy instability conservation-audit followup review note;
- private leak recency-decay followup review note;
- loop safety break nested-loop conflict followup review note;
- loop safety break precommit-warning followup review note;
- pollution market reward-contamination boundary followup review note;
- pollution market delayed-payback followup review note;
- recovery window partial-recovery value followup review note;
- recovery window failed-recovery negative-control followup review note;
- redirect collision no-target fallback followup review note;
- redirect collision preview-token economy followup review note;
- search public target false-positive boundary followup review note;
- search public target repeat-search fatigue followup review note.
- status decay transfer duration-visibility followup review note;
- status decay transfer stack-compression followup review note;
- status decay transfer return-path followup review note;
- summon expiry countdown-visibility followup review note;
- summon expiry replacement-collision followup review note;
- summon expiry support-orphan followup review note;
- temporary generation provenance-visibility followup review note;
- temporary generation choice-load cap followup review note;
- temporary generation expiry-zone followup review note;
- transform pool exhaust preview followup review note;
- transform pool exhaust refresh-cost followup review note;
- transform pool exhaust no-transform negative-control followup review note;
- social texture scope-quarantine followup review note;
- stress cost reference threshold-visibility followup review note;
- late-round texture authority-boundary followup review note.
- starter agency route-choice lock-in warning followup review note;
- starter agency route-choice recovery-option followup review note;
- starter agency route-choice information-cost followup review note;
- starter Cultist scaling-clock telegraph followup review note;
- starter Cultist scaling-clock slow-deck negative-control followup review note;
- starter Cultist scaling-clock reward-pressure followup review note;
- starter first-three encounter role-clarity followup review note;
- starter first-three encounter variance-guard followup review note;
- starter first-three encounter reward-read followup review note;
- summon slot ownership followup review note;
- summon slot overflow-preview followup review note;
- summon slot support-density boundary followup review note;
- threshold overflow warning-band followup review note;
- threshold overflow partial-overflow value followup review note;
- threshold overflow floor negative-control followup review note.
- chain fatigue action-ceiling followup review note;
- chain fatigue failsoft-pause followup review note;
- defense reflect cap-visibility followup review note;
- defense reflect block-retention conflict followup review note;
- draw heat overdraw-waste followup review note;
- draw heat reorder-relief followup review note;
- energy instability forecast-window followup review note;
- energy instability payback-visibility followup review note;
- private leak audit-trail quarantine followup review note;
- private leak third-party amplification followup review note;
- loop safety break exit-reward preview followup review note;
- pollution market cost-signal followup review note;
- recovery window relapse-signal followup review note;
- redirect collision priority-preview followup review note;
- public-target search pool-exhaust negative-control followup review note.
- chain fatigue reset-abuse boundary followup review note;
- defense reflect non-damage pressure boundary followup review note;
- draw heat bottleneck-payoff timing followup review note;
- energy instability banked-energy boundary followup review note;
- private leak rebuttal-window followup review note;
- loop safety break external-trigger collision followup review note;
- loop safety break no-loop negative-control followup review note;
- pollution market cleanup-offer visibility followup review note;
- pollution market burden-sink negative-control followup review note;
- recovery window resource-type split followup review note;
- recovery window overheal-waste signal followup review note;
- redirect collision self-target protection followup review note;
- redirect collision simultaneous-swap negative-control followup review note;
- public-target search permission-boundary followup review note;
- public-target search stale-cache warning followup review note.
- chain fatigue cross-turn carryover warning followup review note;
- chain fatigue shared-counter collision followup review note;
- defense reflect status-damage exclusion followup review note;
- defense reflect pierce-damage boundary followup review note;
- draw heat retain-conflict followup review note;
- draw heat hand-limit preview followup review note;
- energy instability refund-source attribution followup review note;
- energy instability dead-turn negative-control followup review note;
- private leak consent-disclosure contrast followup review note;
- private leak overcorrection-penalty followup review note;
- loop safety break manual-abort agency followup review note;
- pollution market reward-tier scaling followup review note;
- recovery window deck-speed sensitivity followup review note;
- redirect collision target-disappears fallback followup review note;
- public-target search ranking-transparency followup review note.
- chain fatigue nonrepeat-sequence negative-control followup review note;
- chain fatigue payoff-chain exception-boundary followup review note;
- defense reflect overblock no-attack negative-control followup review note;
- defense reflect retaliation-source boundary followup review note;
- draw heat zero-cost cycle negative-control followup review note;
- draw heat shuffle-boundary signal followup review note;
- energy instability refund-chain abuse negative-control followup review note;
- energy instability external-source boundary followup review note;
- private leak public-record contrast followup review note;
- private leak anonymous-source reliability followup review note;
- loop safety break interrupt-timing boundary followup review note;
- pollution market temporary-pollution boundary followup review note;
- recovery window status-cleanup vs heal boundary followup review note;
- redirect collision optional-redirect decline followup review note;
- public-target search noisy-metadata boundary followup review note.
- chain fatigue source-tag clarity followup review note;
- chain fatigue payoff-window compression followup review note;
- defense reflect block-loss tradeoff followup review note;
- defense reflect enemy-scaling interaction followup review note;
- draw heat optional-stop signal followup review note;
- draw heat card-quality tradeoff followup review note;
- energy instability overdraft-forecast followup review note;
- energy instability stabilizer-tax followup review note;
- private leak repair-timing followup review note;
- private leak reward-exchange boundary followup review note;
- loop safety break soft-cap visibility followup review note;
- pollution market cleanup-price disclosure followup review note;
- recovery window pressure-ramp after relief followup review note;
- redirect collision queue-order disclosure followup review note;
- public-target search failed-search value-floor followup review note.
- chain fatigue interruptible-sequence followup review note;
- chain fatigue reward-density pressure followup review note;
- defense reflect counterattack-intent preview followup review note;
- defense reflect block-floor requirement followup review note;
- draw heat hand-filtering pressure followup review note;
- draw heat delayed-heat tick followup review note;
- energy instability multi-turn debt amortization followup review note;
- energy instability minimum-output floor followup review note;
- private leak audience-visibility followup review note;
- private leak consequence-scaling followup review note;
- loop safety break partial-refund followup review note;
- pollution market reward-preview symmetry followup review note;
- recovery window player-choice density followup review note;
- redirect collision target-lock preview followup review note;
- public-target search duplicate-result followup review note.
- chain fatigue loop-vs-combo sample-pair followup review note;
- chain fatigue external-pressure stopline followup review note;
- defense reflect attack-type sample-pair followup review note;
- defense reflect stall break-even followup review note;
- draw heat shuffle-cycle sample-pair followup review note;
- draw heat payload-vs-cantrip followup review note;
- energy instability burst-recovery sample-pair followup review note;
- energy instability support-dependency followup review note;
- private leak opt-in consent sample-pair followup review note;
- private leak visibility-delay sample-pair followup review note;
- loop safety break repeat-source mixing followup review note;
- loop safety break reward-preservation sample-pair followup review note;
- pollution market short-term long-term cost-pair followup review note;
- pollution market cleanup-access sample-pair followup review note;
- recovery window pre-spike signal-pair followup review note;
- recovery window status-pressure pair followup review note;
- redirect collision ally-enemy target-pair followup review note;
- redirect collision prevented-value sample-pair followup review note;
- public-target search open-pool vs filtered-pair followup review note;
- public-target search decline-option sample-pair followup review note.
- chain fatigue witness-set sufficiency followup review note;
- chain fatigue counterexample-coverage followup review note;
- defense reflect witness-set sufficiency followup review note;
- defense reflect counterexample-boundary followup review note;
- draw heat witness-set sufficiency followup review note;
- draw heat counterexample-scope followup review note;
- energy instability witness-set sufficiency followup review note;
- energy instability counterexample-boundary followup review note;
- private leak witness-set sufficiency followup review note;
- private leak counterexample-scope followup review note;
- loop safety break witness-set sufficiency followup review note;
- loop safety break counterexample-boundary followup review note;
- pollution market witness-set sufficiency followup review note;
- pollution market counterexample-scope followup review note;
- recovery window witness-set sufficiency followup review note;
- recovery window counterexample-boundary followup review note;
- redirect collision witness-set sufficiency followup review note;
- redirect collision counterexample-scope followup review note;
- public-target search witness-set sufficiency followup review note;
- public-target search counterexample-boundary followup review note.
- chain fatigue review-packet readiness followup review note;
- defense reflect review-packet readiness followup review note;
- draw heat review-packet readiness followup review note;
- energy instability review-packet readiness followup review note;
- private leak review-packet readiness followup review note;
- loop safety break review-packet readiness followup review note;
- pollution market review-packet readiness followup review note;
- recovery window review-packet readiness followup review note;
- redirect collision review-packet readiness followup review note;
- public-target search review-packet readiness followup review note;
- status decay transfer review-packet readiness followup review note;
- summon expiry review-packet readiness followup review note;
- temporary generation review-packet readiness followup review note;
- transform pool exhaust review-packet readiness followup review note;
- late-round texture review-packet readiness followup review note.
- mechanism failure mode followup review notes for loop collapse, draw heat,
  energy instability, status pollution, temporary generation, hidden tracking,
  over-tutor, redirect priority opacity, false recovery, and no-value fail
  states.
- mechanism failure mode followup review notes for reset ambiguity, reward
  mismatch, forced discard, deck-thin draw loops, support hostage dependencies,
  refund timing races, cleanup no-sink traps, source stacking opacity, temporary
  choice paralysis, delayed expiry, status stack-split and cleanse-order risks,
  transform identity/value-floor collapse, recovery reward bait, public-search
  private leaks, redirect value feedback opacity, and reflect counterplay tax.
- mechanism failure mode followup review notes for cross-source chain leaks,
  delayed-payoff starvation, nested loop interrupts, invisible soft caps,
  non-attack reflect lockout, self-damage reflect attribution, shuffle
  blindness, energy debt memory, burst overcap waste, pollution reward
  contamination and cleanup timing traps, temporary zone overflow and duplicate
  token flood, status duration and ownership edge cases, transform scarcity and
  locked-archetype breaks, recovery relapse, search pool exhaustion, and
  redirect priority inversion.
- mechanism failure mode followup review notes for abort-penalty opacity,
  manual-abort loss aversion, overblock deadlocks, mulligan-pressure collapse,
  minimum-output false floors, cleanup choice tax, expiry-order conflicts,
  counterplay-delay mismatch, transform reroll-chase traps, and slow-deck
  recovery-window punish cases.
- mechanism failure mode followup review notes for hidden exit cost,
  stall thresholds, redraw exhaustion, rollback safety, source-auth drift,
  safe-stop reward gaps, batching penalties, narrow relief bands, multi-hop
  priority drift, lookup-confidence traps, latency gaps, expiry forecast gaps,
  stop-loss timing, support orphan chains, and chain reentry dropoff.
- mechanism failure mode followup review notes for exit-momentum rebound,
  stall ceilings, redraw fatigue, rollback lockouts, provenance conflicts,
  rebound-gap safe stops, cleanup batch limits, relief-band wobble, multi-hop
  echo drift, and stale-confidence search.

The cases may help report-only scanners, feature projection, and advisory
discovery surfaces ask better next-review questions. They do not create
reviewed evidence.

## Round 25 Mechanism Failure Coverage

Round 25 adds a compact mechanism-failure slice over existing generated
followup targets. It is meant to accumulate review questions around failure
modes, not to decide mechanism legality or promote any hypothesis:

- loop collapse and stall loops;
- draw heat overflow, choice-load, and no-value draw;
- energy volatility with dead float and debt whiplash;
- pollution sink failure and source opacity;
- temporary generation expiry and provenance loss;
- status duration drift and transform dead offers;
- false recovery, over-tutor search, and hidden redirect priority.

All cases remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Round 26 Mechanism Failure Coverage

Round 26 continues the mechanism-failure slice over generated followup targets
with another compact advisory-only batch. It focuses on failure-mode review
questions for:

- chain reset ambiguity and loop-break reward mismatch;
- draw heat forced-discard agency loss and deck-thin self-loops;
- energy support-hostage and refund-timing races;
- pollution cleanup no-sink traps and source stacking opacity;
- temporary generation choice paralysis and delayed expiry surprises;
- status stack-split exploits and cleanse-order conflicts;
- transform identity loss and low-rarity value-floor collapse;
- recovery-window reward bait;
- public-target search private-info leakage;
- redirect prevented-value feedback opacity;
- defense reflect counterplay tax.

All cases remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Round 27 Mechanism Failure Coverage

Round 27 continues the mechanism-failure lane with a 20-case advisory-only
batch. It focuses on review questions for:

- chain cross-source discount leaks and delayed-payoff starvation;
- loop nested-interrupt leaks and invisible soft caps;
- defense reflect non-attack lockout and self-damage attribution confusion;
- draw heat delayed-shuffle blindness;
- energy debt memory burden and burst-overcap waste;
- pollution reward-contamination misreads and cleanup-timing traps;
- temporary generation zone overflow and duplicate-token flood;
- status negative-duration and owner-swap confusion;
- transform scarcity spirals and locked-archetype breaks;
- recovery-window frontloaded relapse;
- public-target search pool-exhaustion blindness;
- redirect priority inversion.

All cases remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Round 28 Mechanism Failure Coverage

Round 28 continues the mechanism-failure lane with a 10-case advisory-only
batch. It focuses on review questions for:

- chain fatigue abort-penalty opacity;
- loop safety manual-abort loss aversion;
- defense reflect overblock deadlocks;
- draw heat mulligan-pressure collapse;
- energy instability false minimum-output floors;
- pollution market cleanup-choice tax;
- temporary generation expiry-order conflicts;
- status decay transfer counterplay-delay mismatch;
- transform pool reroll-chase traps;
- recovery-window slow-deck punish cases.

All cases remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Round 29 Mechanism Failure Coverage

Round 29 continues the mechanism-failure lane with a 15-case advisory-only
batch. It focuses on review questions for:

- chain fatigue hidden exit cost and reentry dropoff;
- defense reflect stall thresholds;
- draw heat redraw exhaustion;
- energy instability rollback safety;
- private leak source-auth drift;
- loop safety safe-stop reward gaps;
- pollution market cleanup batching penalties;
- recovery-window relief that is too narrow;
- redirect multi-hop priority drift;
- public-target search lookup-confidence traps;
- status decay transfer counterplay latency gaps;
- temporary generation expiry forecast gaps;
- transform pool exhaust stop-loss timing;
- summon expiry support orphan chains.

All cases remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Round 30 Mechanism Failure Coverage

Round 30 continues the mechanism-failure lane with a 10-case advisory-only
batch. It focuses on review questions for:

- chain fatigue exit-momentum rebound;
- defense reflect stall ceilings;
- draw heat redraw fatigue;
- energy instability rollback lockouts;
- private leak provenance conflicts;
- loop safety safe-stop rebound gaps;
- pollution market cleanup batch limits;
- recovery-window relief-band wobble;
- redirect collision multi-hop echo drift;
- public-target search stale confidence.

This completes the requested `mechanism failure modes +90` lane. All cases
remain `design_note / human_curated / review_needed` and
`advisory_context_only`.

## Validation

```bash
python scripts/validate_cardanalysis_case_input.py --input tests/fixtures/combat_analysis/source_followup_case_library_v1
py -3.11 -m pytest tests/toolkit/combat_analysis/test_source_followup_case_library_v1.py -q
```
