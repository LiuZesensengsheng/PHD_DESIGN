# Campaign Service Dependency Hotspots V1

## Goal

Record which `contexts/campaign/services/*` modules were the best cuts for dependency narrowing in this round, and which remaining hotspots should wait until their responsibilities are smaller or more stable.

Terminology note:

- `Campaign` is the outer shell and host context
- some remaining hotspots, especially `track_block_service`, really belong to
  the campaign `Task Area` subdomain rather than to generic shell logic

## Completed Cuts

- `contexts/campaign/services/transition_helper.py`
  - switched from `state: Any` to `TransitionRequestHost`
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/campaign_route_resolution_service.py`
  - switched from `state: Any` to `RouteResolutionHost`
  - route-resolved block cleanup now goes through `CampaignState.resolve_returned_route_block()`
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/campaign_startup_hydration_service.py`
  - switched from `state: Any` to `StartupHydrationHost`
  - snapshot restore now funnels through explicit state seam methods instead of direct runtime field mutation
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/campaign_startup_effects_service.py`
  - switched from `state: Any` to `StartupEffectsHost`
  - startup board seeding now goes through explicit host methods for block creation, replacement, and board stabilization
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/thesis_publication_flow_service.py`
  - switched from `state: Any` to `PublicationFlowHost`
  - publication record and final state transition now go through narrow host methods instead of direct `CampaignState` internals
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/line_bubble_service.py`
  - switched from broad `CampaignState` assumptions to `LineBubbleHost`
  - task-area overlay lookup now reads blocks through `get_campaign_blocks()`
  - gossip lock release now goes through explicit host seams instead of `_unlock_gossip_inputs`
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/thesis_blueprint_app_service.py`
  - switched from broad `CampaignState` assumptions to `TaskAreaBlueprintHost`
  - thesis blueprint follow-up now uses explicit task-area seams for meta prep and saved-tier cleanup
  - current direct `self.state.*` touches after the cut: `0`

## Remaining Hotspots

- `contexts/campaign/services/thesis_meta_service.py`
  - current direct `self.state.*` touches: `56`
  - status: hotspot, but intentionally not in this task
  - reason: split submission flow, tier-tag mutation, and publication handoff responsibilities first; do not hide a monolith behind a wide host
- `contexts/campaign/services/track_block_service.py`
  - current direct `self.state.*` touches: `38`
  - status: hotspot, but intentionally not in this task
  - reason: mostly task-area board geometry and runtime mutation rules; do not force repository-style or facade-style abstraction here yet

## Lower-ROI Targets For Now

- `contexts/campaign/services/campaign_mouse_event_service.py`
  - current direct `self.state.*` touches: `39`
  - reason: still mixes view math, hit-testing, runtime widgets, and transition orchestration; responsibility split is higher ROI than DIP here
- `contexts/campaign/services/thesis_slice.py`
  - current direct `self.state.*` touches: `38`
  - reason: already behaves like a facade over multiple thesis services; further narrowing should follow later thesis-runtime consolidation

## Conclusion

- Worth continuing:
  - orchestration-heavy startup flows
  - modal-to-transition seams
  - state-machine boundary helpers with stable collaborator contracts
- Not worth forcing right now:
  - `thesis_meta_service` before its responsibilities are split
  - `track_block_service` while it is still dominated by task-area board geometry rules
- Rule of thumb:
  - prefer narrow host protocols that expose business-intent methods
  - if a protocol starts needing many internal fields, stop and add a thin `CampaignState` seam method instead
