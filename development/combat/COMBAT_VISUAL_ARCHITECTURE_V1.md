# Combat Visual Architecture V1

## Purpose

This document records the current combat-only visual architecture baseline.
It is a catalog and ownership map for visual effects, not a request to build a
shared visual engine.

The active direction is:

- keep combat visuals local to `contexts/combat`
- keep pygame as the rendering substrate
- route gameplay-facing visual triggers through narrow command seams
- keep `CombatView` as the presentation shell that wires owners together
- add richer effects only after their lifecycle and render pass are named

## Current Owners

### Presentation Shell

`contexts/combat/mvc/views/combat_view.py`

- owns the headed pygame screen and asset/font resources
- wires subviews, visual state, the FX controller, visual passes, and the
  render pipeline
- retains compatibility wrappers for older view-facing calls
- keeps compatibility properties for older render-feedback comparison values

### Render Pipeline

`contexts/combat/mvc/views/render_pipeline.py`

- owns the frame pass order for headed combat
- updates animation lifetimes before drawing
- calls visual owners, the FX controller, `CombatView`, and subview rendering
  methods in a fixed order
- remains combat-only and does not introduce a shared renderer runtime

### Render Feedback State

`contexts/combat/mvc/views/render_feedback_state.py`

- owns render-facing last-value comparison state:
  - player stress
  - legacy single enemy health
  - player and enemy confidence
  - per-enemy health map
  - paper tag count
- detects stress, enemy-health, confidence, and paper-tag deltas before the FX
  update pass
- syncs comparison values after `display.flip()`
- remains a headed combat presentation state owner, not combat runtime
  authority

### Overlay Pass

`contexts/combat/mvc/views/overlay_pass.py`

- owns headed overlay rendering for:
  - phase banner
  - enemy-action banner
  - queue-lock banner
  - game-over overlay
- owns game-over overlay timing state
- remains a render-pass owner, not runtime phase or combat-end authority

### Targeting Pass

`contexts/combat/mvc/views/targeting_pass.py`

- owns headed rendering for the drag targeting arrow
- reads `CombatTargetingInteractionState` as input
- keeps targeting arrow curve and arrowhead drawing out of `CombatView`
- remains a local render-pass owner, not combat targeting authority

### Visual Effects Runtime State

`contexts/combat/mvc/views/visual_effects_state.py`

- owns short-lived combat visual lifetimes:
  - `damage_numbers`
  - `hit_particles`
  - `heal_particles`
  - `played_cards`

This is the current runtime-state anchor for combat FX. New short-lived effects
should either fit here explicitly or introduce a similarly narrow combat-only
state owner.

### Actor Feedback State

`contexts/combat/mvc/views/actor_feedback_state.py`

- owns actor-local visual lifetimes:
  - player and enemy shake
  - player and enemy wobble
- owns shake/wobble offset calculations used by actor rendering
- remains a headed combat presentation state owner, not gameplay authority

### Targeting Interaction State

`contexts/combat/mvc/views/targeting_interaction_state.py`

- owns local headed card interaction state:
  - hovered and dragged card index
  - drag start/current positions
  - card and enemy hit rects
  - targeting arrow start and hovered target id
- owns hover, drag-threshold, target-hit, and drag-end play-info shaping
- remains local UI interaction state, not combat runtime targeting authority

### Visual Effects Commands

`contexts/combat/mvc/views/visual_effects_commands.py`

- defines the headed combat command seam for visual feedback
- currently covers:
  - card flyout
  - floating numbers
  - hit particles
  - heal particles

Business or runtime presentation paths should prefer this command seam over
calling concrete view/private FX methods directly.

### Visual Feedback Mapper

`contexts/combat/mvc/views/visual_feedback_mapper.py`

- maps render-facing combat deltas to headed visual feedback commands
- keeps floating-number, particle, shake, and wobble shaping out of
  `CombatRenderFeedbackState`
- remains a temporary headed mapper until those facts are promoted to runtime
  presentation events

### FX Controller

`contexts/combat/mvc/views/fx_controller.py`

- mutates `CombatVisualEffectsState`
- updates short-lived FX lifetimes
- renders particles, floating numbers, and played-card flyouts
- remains a presentation component, not gameplay authority

### Presentation Event Consumer

`contexts/combat/mvc/views/presentation_consumer.py`

- maps `CombatPresentationEvent` payloads to headed visual commands
- currently maps `card_played` into `queue_card_flyout`
- keeps pending card render data outside the combat runtime model

## Current Render Pass Order

The headed combat frame currently uses this practical pass order:

1. detect render-facing state deltas
2. update FX, actor animations, and hand animations
3. scene layers
4. actors
5. pre-hand particles
6. hand and HUD
7. phase, enemy-action, and queue-lock banners
8. short-lived FX: floating numbers, particles, and heal particles
9. played-card flyout
10. targeting arrow
11. game-over overlay
12. display flip
13. sync last render-facing comparison values

Pass order matters. New effects should state which pass they belong to before
implementation.

## Effect Catalog

| Effect | Trigger Source | Command / Owner | Runtime State | Render Pass |
| --- | --- | --- | --- | --- |
| Card flyout | `card_played` presentation event, with pending headed card data | `HeadedCombatPresentationConsumer` -> `CombatVisualEffectsCommands.queue_card_flyout` | `played_cards` | played-card flyout pass after HUD |
| Played-card 2.5D pose | card flyout rendering | `_FxController.render_played_cards` + `draw_card(..., pose=...)` | `played_cards` | played-card flyout pass after HUD |
| Floating number | `CombatRenderFeedbackState` stress, health, confidence, or tag delta detection | `CombatVisualFeedbackMapper` -> `CombatVisualEffectsCommands.start_floating_number` | `damage_numbers` | short-lived FX pass after banners |
| Hit particles | damage or critical feedback | `CombatVisualFeedbackMapper` -> `CombatVisualEffectsCommands.spawn_hit_particles` | `hit_particles` | pre-hand and post-banner particle passes |
| Heal particles | healing or positive feedback | `CombatVisualFeedbackMapper` -> `CombatVisualEffectsCommands.spawn_heal_particles` | `heal_particles` | short-lived FX pass after banners |
| Actor shake | render-facing damage/stress feedback | `CombatVisualFeedbackMapper` -> `CombatActorFeedbackCommands.start_actor_shake` | `CombatActorFeedbackState` shake state | actor rendering |
| Actor wobble | render-facing stress/confidence feedback | `CombatVisualFeedbackMapper` -> `CombatActorFeedbackCommands.start_actor_wobble` | `CombatActorFeedbackState` wobble state | actor rendering |
| Targeting arrow | drag / targeting interaction state | `CombatTargetingInteractionState` + `CombatTargetingPass` | `CombatTargetingInteractionState` drag/targeting state | targeting pass after FX |
| Turn and enemy banners | renderable state banners | `CombatRenderPipeline` -> `CombatOverlayPass.render_banners` | renderable state payloads | banner pass after HUD |
| Game-over overlay | renderable game-over state | `CombatRenderPipeline` -> `CombatOverlayPass.render_game_over` | `CombatOverlayPass.game_over_start_time` | final overlay pass |

## Event Mapping Baseline

The current preferred headed event mapping is:

```text
CombatSession presentation event
  -> HeadedCombatPresentationConsumer
  -> CombatVisualEffectsCommands
  -> CombatVisualEffectsState
  -> CombatRenderPipeline pass
```

Only `card_played` fully uses this route today. Damage, healing, confidence,
stress, and paper-tag feedback now use `CombatRenderFeedbackState` for
render-facing state-delta detection, then `CombatVisualFeedbackMapper` for
headed visual command shaping.

That mixed state is acceptable for this baseline, but new combat visual effects
should choose one of these paths explicitly:

- presentation event -> visual command, for runtime facts that already have a
  presentation event
- render-facing delta detector -> visual command, for temporary headed-only
  feedback that has not yet moved to presentation events
- local interaction state -> render pass, for drag, hover, and targeting
  visuals that are purely headed UI behavior

## Next Migration Slices

1. Route more actor-local feedback through `CombatActorFeedbackState` only when
   a concrete actor feedback family needs it.
2. Keep card hover/drag/targeting behavior inside `CombatTargetingInteractionState`
   unless it becomes a retained widget owner later.
3. Split short-lived FX pass details further only when another effect family
   makes the current pass too broad.
4. Add a data-backed effect catalog only after at least two effect families need
   authoring data. Do not introduce `EffectSpec` first.

## Guardrails

- Do not introduce an engine-wide visual runtime from combat work.
- Do not make combat runtime/domain code import pygame or headed view modules
  to trigger a visual effect.
- Do not add new direct calls from services or runtime orchestration into
  `_FxController` private methods.
- Keep `CombatVisualEffectsCommands` as the narrow seam for headed visual
  commands until a real need for `VisualIntent` appears.
- Update this document when adding a new combat visual effect family or moving
  an existing effect to a different pass.

## Last Updated

- `2026-05-19`
