# Cardanalysis Four Character Style Tension Goal V1

## Purpose

Define the next cardanalysis capability target for package style, choice
pressure, and anti-hexagon review across the four STS1 characters.

This goal is about building a reusable exam capability, not about promoting any
generated card package as final content.

## Goal

Build a report-only four-character style tension exam that can read
`complete_card_draft_v1` packages and produce Chinese-readable advisory output
for:

1. whether a package has a clear lane identity,
2. whether its axes create real resource or timing conflict,
3. whether the player must choose between short-term survival and long-term
   payoff,
4. whether attack, defense, draw, energy, and scaling are becoming a flat
   all-rounder bundle,
5. whether a 12-card package is trying to carry too many axes,
6. whether a 30-card candidate pool can support multiple routes without losing
   strong-build density.

## Capability Target

Primary new capability:

```text
programmatic_complete_card_draft_style_tension_readout_v1
```

The V1 output should include:

- `axis_conflict_index`
- `hexagon_risk`
- `choice_pressure_index`
- `tempo_vs_scaling_tension`
- `attack_defense_split`
- `opportunity_cost_visibility`
- `lane_identity_focus`

The readout is advisory only. It must not change score weights, create hard
gates, write runtime card data, promote formal cards, enable learned or
reranker behavior, or claim generated/speculative material as reviewed evidence.

## Four Character Scope

V1 must be able to evaluate packages for:

- `ironclad`
- `silent`
- `defect`
- `watcher`

The shared metric model should stay common, while each character may have a
small axis vocabulary and conflict hint table.

Examples:

- Ironclad: strength, exhaust, block/body, self-damage/heal.
- Silent: poison, shiv, discard, retain.
- Defect: frost, lightning, dark, focus, power setup, orb slots.
- Watcher: wrath/calm, scry, retain, mantra/divinity, burst windows.

## Package Scale Interpretation

Use package size when interpreting axis focus:

- 12-card medium package: prefer one primary axis plus light support.
- Around 30-card candidate pool: allow two to three routes, but require strong
  build lanes, support cards, failure floors, and weak-link visibility.
- 50-card role pool or larger: future work may judge broader character ecology,
  but V1 should not require this scale.

## Success Criteria

V1 is successful when:

1. Existing four-character complete-card draft fixtures can be evaluated by one
   CLI.
2. The output includes a machine snapshot, manifest, and Chinese review packet.
3. The Chinese packet lists actual card names and rules text for human review.
4. The output clearly distinguishes assistant-authored code, program-generated
   readout, program/generated draft input, and LLM/API usage status.
5. The readout flags obvious hexagon/goodstuff packages and low-choice packages.
6. The readout gives next-iteration advisory metadata without changing any
   existing score or generation default.
7. Focused tests cover all four characters plus at least one synthetic
   all-rounder/low-choice negative control.

## Execution Slices

1. Goal and scope document.
2. Minimal style-tension capability head over `complete_card_draft_v1`.
3. CLI and focused tests.
4. Capability graph and runbook registration.
5. Generate a current four-character Chinese review packet in `tmp/`.
6. Later slice: feed style-tension advisory metadata into the next generator
   provider without changing score weights or default synthesis.

## Boundary Assertions

The capability must keep these assertions true:

- `report_only`
- `advisory_context_only`
- `runtime_card_data_written = False`
- `formal_cards_promoted = False`
- `hard_gate_created = False`
- `score_weight_changed = False`
- `default_synthesis_changed = False`
- `llm_api_called = False`
- `learned_or_reranker_enabled = False`
- `source_mined_or_speculative_promoted_to_reviewed = False`

## Human Review Question

The first useful human review question should be:

```text
这四个角色的候选包里，哪一组最像“有风格、有代价、有选择”的卡包，
哪一组最像“什么都能做但不够有身份”的六边形卡包？
```
