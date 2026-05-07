# Design Layering Strategy V1

## Status

This document is the current canonical direction for combat-design layering.
Older five-color and full mixed-pool documents are historical/reference material
unless they are explicitly restated here.

Current principle:

```text
Keep the philosophical tension. Remove the per-turn operation burden.
```

## Canonical Layers

### Discipline / Career / 学科职业

The discipline or career owns the primary combat play pattern.

- Owns starting deck identity, the main combat loop, and the core card pool.
- Defines the main mechanism grammar players execute turn by turn.
- Should be readable as an STS-like deck: draw cards, spend energy, play cards,
  read enemy intent, choose rewards.
- May contain one or two clean mechanism axes per card, but should not ask the
  ideal system to become a second combat class.

### Ideal / 理想

The ideal owns personality, value tendency, reward ecology, and sources of
conflict.

- Shapes what rewards feel tempting, costly, or identity-defining.
- Carries philosophical pressure through reward choices, run growth, event
  offers, and long-term preference.
- Should not become a hidden moral score, punishment track, or recurring combat
  chore.
- Preserves ideal conflict through visible reward exchange, not moral
  punishment or hidden punishment.

### Ideal Card Package / 理想卡包

An ideal card package is a shared deck ecology niche, not a second career.

- Can add reward-pack texture shared across compatible disciplines.
- Should expose enabler, payoff, glue, and fail-state value when it is package
  shaped.
- May bias deckbuilding and reward picks, but should not replace the discipline
  starting deck, define its own full resource economy, or require a full
  class-sized card pool.
- Should stay advisory until a human design pass decides whether any package
  becomes formal content.

### Trait / 特质

Traits are the main long-term growth carrier.

- Own long-run bias, identity imprint, unlock pressure, and build preference.
- Can make a player care more about certain rewards or packages over time.
- Should avoid adding recurring per-turn choices or hidden combat tracking.
- Are a good home for ideal imprint when the design needs meaning without more
  combat text.

### Keystone Trait / 创新点或强特质

A keystone trait is a stronger trait that sells an innovation point.

- May bend reward valuation, unlock a narrow build path, or create a strong
  long-term identity.
- Should be rare, explicit, and reviewable.
- Can carry higher build/growth complexity than ordinary traits.
- Must still avoid becoming a per-turn minigame unless that minigame is the
  discipline's primary combat identity.

### Event / 理想交换事件

Events own ideal exchange, sacrifice, and wavering.

- Offer visible exchanges between reward lanes, traits, or ideal commitments.
- Create tension by asking what the player gives up for a different reward.
- Should keep refusal viable: the player should preserve the original path
  rather than receive hidden punishment.
- Should not inject new every-turn combat operations.

## Allowed Complexity

Complexity is acceptable when it lives in layers where the player can review it
outside the repeated combat-turn execution loop.

- Build layer:
  deckbuilding bias, shared package ecology, reward-pick tradeoffs, enabler /
  payoff / glue structure, fail-state value.
- Growth layer:
  traits, keystone traits, unlock preference, long-term ideal imprint, run
  identity.
- Event layer:
  ideal exchange, sacrifice offers, wavering, visible reward swaps, campaign
  pacing decisions.
- Review/advisory layer:
  report-only complexity metrics, fixture packs, design notes, and human review
  prompts.

## Forbidden Per-Turn Complexity

The current route forbids moving philosophical expression into repeated combat
turn burden.

- No philosophical meaning stuffed into overloaded single-card text.
- No ideal system that adds recurring per-turn decisions to ordinary combat.
- No hidden ideal state or hidden punishment track.
- No moral punishment disguised as reward logic.
- No ideal card package that expands into a second career.
- No return to five-color costs plus a full mixed-color main card pool as the
  current implementation route.
- No legality, hard-gate, default synthesis, learned, or reranker authority from
  complexity evaluation outputs.

## Phase-One Target

The recommended first production-facing slice is intentionally narrow.

- One discipline / career.
- At least three ideals.
- Ideal card packages as shared deck ecology niches, not second careers.
- Traits as the main long-term growth carrier.
- Events as the primary place for ideal exchange, sacrifice, and wavering.

## Historical Material

The five-color ideal work remains useful as personality and value-reference
material. It is not the current implementation source of truth for:

- five-color costs;
- a full mixed-color main card pool;
- ideal identity as a second combat class;
- per-turn philosophical operation load.

Use `docs/design/core/FIVE_COLOR_HIGH_LEVEL_DESIGN_V1.md` and related ideal
documents as reference only. This document is the current canonical layering
strategy until it is explicitly superseded.
