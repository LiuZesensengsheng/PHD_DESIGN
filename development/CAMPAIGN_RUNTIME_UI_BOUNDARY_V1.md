# Campaign Runtime UI Boundary V1

## Goal

Make the runtime widget/node boundary explicit so a UI-focused collaborator can
work inside `contexts/campaign/ui_runtime/` without having to own campaign
orchestration details.

## Why This Exists

The project is moving toward Godot-like retained runtime widgets inside
pygame, but campaign still carries heavy business sequencing in
`CampaignState` and `services/`.

That mixed mode is fine only if the ownership line is explicit.

Without that line, runtime widgets easily become another place where route
resolution, thesis rules, transition wiring, or persistent writes get hidden.

## Current Runtime UI Surface

The current runtime UI boundary is centered on these view hooks:

- `CampaignView.handle_runtime_ui_event(event)`
- `CampaignView.update_runtime_ui(dt)`
- `CampaignView.render_runtime_ui(surface)`

`CampaignState` currently owns dispatch order around those hooks:

1. modal dispatch
2. input-lock guard
3. runtime UI event handling
4. keyboard/mouse/button/hover adapters

That means runtime widgets may consume local interaction, but they are still
hosted by the campaign lifecycle rather than becoming their own application
layer.

## What Runtime UI Owns

`contexts/campaign/ui_runtime/` is the right home for:

- retained node trees
- local hover/open/close state
- local animation timing
- local hit-testing
- local widget composition
- runtime-only debug overlays
- asset/layout override helpers used only by runtime widgets

Current examples:

- `ui_node.py`
- `runtime_ui.py`
- `phone_widget.py`
- `phone_widget_store.py`

## What Runtime UI Must Not Own

Runtime widgets must not become the home for:

- block click routing
- thesis submission rules
- meeting/reward/modal ownership policy
- transition payload construction
- persistent save writes
- cross-state navigation
- campaign business sequencing

If a runtime widget needs a business consequence, it should stop at a host seam
owned by `CampaignState` or a campaign orchestration service.

## Practical Rules For UI Work

When a UI collaborator touches `ui_runtime`, the safe default is:

- keep new logic local if it only changes runtime presentation or local widget interaction
- use `CampaignView` runtime hooks for retained widget wiring
- stop and ask for a state/service seam before adding business branching
- do not import campaign thesis/transition services into runtime widgets
- do not write `persistent` from runtime widgets

## Current Code Ownership

The current ownership split is:

- `runtime_ui.py`: retained runtime widget tree assembly and local dispatch
- `phone_widget.py`: local widget state, hover, animation, and local click behavior
- `CampaignView`: runtime widget host hooks for event/update/render
- `CampaignState`: lifecycle host and dispatch ordering
- `contexts/campaign/services/*`: business/orchestration ownership

## Verification

V1 is protected by focused contract tests covering:

- runtime UI event consumption short-circuits downstream business adapters
- runtime UI update runs through the state/view host path
- view runtime hooks delegate to the retained runtime UI module
- `PhoneWidget` local notification interaction stays widget-local
- runtime debug toggle remains local and non-consuming

## Non-Goals

This cut does not:

- migrate all campaign UI into a node tree
- create a generic engine-wide scene graph
- move campaign orchestration into widget scripts
- replace `CampaignState` as the lifecycle host

## Next Cut

This boundary is now part of the minimum campaign UI handoff pack.

Further follow-up should be targeted widget/runtime seams or hotspot cleanup,
not another broad runtime-boundary pass.
