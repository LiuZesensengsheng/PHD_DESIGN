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

The old `CampaignView` runtime-ui compatibility hooks have now been removed.

`CampaignState` currently owns dispatch order around the remaining campaign UI ingress:

1. modal dispatch
2. input-lock guard
3. keyboard/mouse/button/hover adapters

That means retained/runtime UI work must now stay local to the concrete
view/rendering/widget path instead of depending on a generic `CampaignView`
compat hook layer.

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
- `phone_widget_store.py`

`ui_node.py` is the current concrete retained-node primitive. Older runtime
widget experiments such as `runtime_ui.py` and `phone_widget.py` are no longer
present in the active tree; do not recreate them unless a concrete local widget
slice needs that owner.

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
- stop and ask for a state/service seam before adding business branching
- do not import campaign thesis/transition services into runtime widgets
- do not write `persistent` from runtime widgets

## Current Code Ownership

The current ownership split is:

- `ui_node.py`: retained node primitive used by local UI/editor surfaces
- `phone_widget_store.py`: compatibility export for UI editor override storage
- `CampaignView`: presentation host only, without generic runtime-ui compat hooks
- `CampaignRenderFrameContext`: campaign-only one-frame render input bundle, not a widget tree or runtime UI owner
- `CampaignState`: lifecycle host and dispatch ordering
- `contexts/campaign/services/*`: business/orchestration ownership

## Verification

V1 is protected by focused contract tests covering:

- campaign event routing now reaches business adapters directly after modal/input-lock checks
- shared UI override polling stays on the state/view host path without a runtime-ui shim layer
- removed `CampaignView` runtime-ui compat hooks do not reappear
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
