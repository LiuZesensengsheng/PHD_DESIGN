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
  - route-resolved block cleanup now terminates in lifecycle-owned return resolution plus `CampaignBoardMutationService.remove_resolved_route_block(...)`
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
- `contexts/campaign/services/gossip_flow_app_service.py`
  - gossip modal lock ownership now routes only through `ModalCoordinator`
  - on-hide unlock no longer depends on the private `CampaignState._unlock_gossip_inputs()` seam
  - current direct raw `_input_locked` fallback writes after the cut: `0`
- `contexts/campaign/services/thesis_blueprint_app_service.py`
  - switched from broad `CampaignState` assumptions to `TaskAreaBlueprintHost`
  - thesis blueprint follow-up now uses explicit task-area seams for meta prep and saved-tier cleanup
  - current direct `self.state.*` touches after the cut: `0`
- `contexts/campaign/services/thesis_meta_service.py`
  - phase-2 thesis convergence delegated main write-path persistence to `ThesisWritePathService`
  - current direct `self.state.*` touches after the cut: `10`
  - status: no longer the highest-priority dependency hotspot in this refactor line
- `contexts/campaign/services/track_block_service.py`
  - phase-3 kept the stable task-area facade but split internal rules into:
    - `TrackLayoutRules`
    - `_TrackDdlSnakeRules`
    - `_TrackFusionRules`
  - later compat cleanup removed the old `_next_id()` state seam and the synthetic fused-id fallback
  - fused block id allocation now routes through the stable `allocate_campaign_block_id()` host seam
  - current direct `self.state.*` touches after the cut: `24`
  - current stance: future task-area edits should prefer those helper boundaries instead of widening the facade again
- `contexts/campaign/services/campaign_state_service_bundle.py`
  - reward opening now funnels through one grouped seam:
    - `CampaignState.open_reward(...)`
    - `CampaignRewardServiceGroup.open_reward(...)`
  - direct host aliases `state.reward` / `state.post_combat_reward` were removed
  - reward cleanup now also routes through explicit host seam
    `reset_reward_runtime_state()`
  - thesis/social direct host aliases were later removed as well:
    - thesis runtime/services now route through `state.thesis_services.*`
    - social runtime/services now route through `state.social_services.*`
  - selected interaction direct aliases were later removed as well:
    - `state.lifecycle_binding`
    - `state.block_click_orchestrator`
    - `state.event_input_orchestrator`
  - `CampaignState` request/host seams now route through grouped interaction
    ownership instead:
    - `state.interaction_services.lifecycle_binding`
    - `state.interaction_services.block_click_orchestrator`
    - `state.interaction_services.event_input_orchestrator`
  - retained direct shell/runtime seams vs review-next direct aliases are now
    documented in:
    - `docs/development/CAMPAIGN_DIRECT_SEAM_POLICY_V1.md`
  - current stance: future reward entry/cancellation work should start from the
    grouped reward seam instead of restoring service aliases on `CampaignState`

## Remaining Hotspots

- `contexts/campaign/services/thesis_slice.py`
  - current direct `self.state.*` touches: `39`
  - status: still the main remaining campaign-side dependency hotspot
  - reason: it behaves as a convenience facade across multiple thesis seams, so further narrowing should wait for a concrete follow-up rather than another cleanliness-only pass

## Lower-ROI Targets For Now

- `contexts/campaign/services/campaign_mouse_event_service.py`
  - current direct `self.state.*` touches: `3`
  - reason: this is no longer a real dependency hotspot after the intent split; keep it watched as an adapter/orchestration seam, not as a primary narrowing target

## Conclusion

- Worth continuing:
  - orchestration-heavy startup flows
  - modal-to-transition seams
  - state-machine boundary helpers with stable collaborator contracts
- Stable enough after this refactor line:
  - `track_block_service` as a task-area facade with smaller internal rule units
  - `thesis_meta_service` as a UI/orchestration seam over a dedicated write path
- Not worth forcing right now:
  - another `track_block_service` abstraction pass without new task-area behavior pressure
  - a second thesis facade rewrite without a concrete identity or writer-collision trigger
- Rule of thumb:
  - prefer narrow host protocols that expose business-intent methods
  - if a protocol starts needing many internal fields, stop and add a thin `CampaignState` seam method instead
