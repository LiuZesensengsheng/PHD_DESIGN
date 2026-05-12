# Campaign Direct Seam Policy V1

## Goal

Decide which remaining direct `CampaignState` service aliases are still
deliberate shell/runtime seams, and which should keep converging behind grouped
service surfaces.

This is a decision document for the current campaign cleanup line, not a
whole-campaign rewrite plan.

- Level: `L3 Architecture`
- Date: `2026-04-22`

## Problem

The current campaign cleanup already removed the clearly duplicative direct
aliases for:

- reward internals
- thesis services
- social services

That improved AI safety because those services had two equivalent access paths:

- direct `state.<service>`
- grouped `state.<group>.<service>`

The remaining direct aliases are different.

Several of them now sit on the live campaign shell path:

- frame event routing
- modal/input coordination
- turn-cycle entry
- task-area runtime mutation

The question is no longer:

- can we delete more aliases for symmetry

It is:

- which direct seams are still real shell/runtime ports
- which ones are only transition convenience and should be removed next

## Constraints

- Keep the scope inside `contexts/campaign/**`.
- Do not reopen a view/runtime extraction pass.
- Prefer AI-safe explicit ownership over symmetry-only cleanup.
- The code is largely unpublished, so transition-only compat layers are allowed
  to be deleted.
- Do not destabilize hot runtime paths just to force every access behind a
  group surface.

## Complexity

### Essential Complexity

Campaign still has three different kinds of access:

1. shell/runtime ports
2. grouped business-service ownership
3. state-level intent seams

Those are not interchangeable.

Current code evidence:

- `campaign_frame_orchestrator.py` runs an ordered event pipeline across:
  - `modal_dispatch`
  - `input_lock`
  - `keyboard_events`
  - `mouse_events`
  - `ui_button_events`
  - `pointer_hover`
- `machine.py` treats `lifecycle_machine` as the timing owner for turn
  transition and interrupt phases.
- `state.py` uses `tx` as the campaign-shell transition request port.
- `end_turn_service.py` still depends on `track` and `endturn` as task-area
  runtime collaborators.

### Accidental Complexity

The accidental complexity comes from mixing two very different situations under
the single label "direct alias":

- duplicated leaf-service access that confuses AI
- deliberate shell ports that make runtime flow easier to read

Reward/thesis/social belonged to the first bucket.

The remaining runtime-heavy aliases are not all in that bucket anymore.

## Options

### Option A: Force All Remaining Services Behind Groups

What it means:

- remove all remaining direct aliases on `CampaignState`
- require runtime code to use only `state.<group>.<service>`

Pros:

- strongest surface symmetry
- easiest single rule to explain

Cons:

- treats shell ports and leaf services as if they were the same thing
- adds nested access noise on hot runtime paths
- risks breaking code that is really depending on a shell contract, not on a
  compat alias

### Option B: Stop Now And Keep The Remaining Mixed Surface As-Is

What it means:

- keep the current remaining direct aliases
- do not define any explicit keep/remove policy

Pros:

- lowest short-term work
- avoids more cleanup churn immediately

Cons:

- leaves AI with an incomplete rule
- future cleanup will keep reopening the same question
- direct seams that are still only transitional will stay ambiguous

### Option C: Split The Remaining Direct Surface Into Policy Buckets

What it means:

- keep grouped-only ownership for leaf business-service families
- keep a small whitelist of deliberate shell/runtime direct seams
- mark a smaller next cleanup batch of transition-style aliases

Pros:

- preserves the AI win from removing duplicate leaf-service paths
- avoids destabilizing runtime pipeline readability
- gives future cleanup a concrete stop line

Cons:

- the final surface is intentionally mixed rather than perfectly uniform
- requires explicit documentation and guardrails so the distinction stays clear

## Risks

### Risk If We Over-Collapse To Groups

- shell/runtime ports become harder to scan in event and turn pipelines
- runtime code gains nested lookup noise without gaining clearer ownership
- later contributors may rebuild new direct seams ad hoc because the grouped
  version is awkward in the hot path

### Risk If We Under-Specify The Policy

- AI will keep treating all direct aliases as equally removable
- future cleanup may oscillate between "delete everything" and "restore one
  alias for convenience"

### Residual Risk Even With The Recommended Policy

- some current direct aliases are still judgment calls rather than permanent
  architecture
- `track` and a few orchestration seams remain partly transitional because the
  task-area and lifecycle hotspots are not fully settled

## Recommendation

Choose **Option C**.

Adopt the following policy.

### 1. Group-Only By Default For Leaf Service Families

These should stay grouped and should not regain direct `CampaignState` aliases:

- `reward_services.*`
- `thesis_services.*`
- `social_services.*`
- future leaf service families with the same duplicated-access shape

Rule:

- if a service is mainly a business/application leaf and already has a clear
  group owner, the group surface is canonical

### 2. Keep Direct Access For Deliberate Shell/Runtime Ports

These should remain direct for now because they act more like shell/runtime
ports than like duplicated leaf services:

- `modal`
- `tx`
- `frame_orchestrator`
- `visible_blocks`
- `lifecycle_hooks`
- `lifecycle_machine`
- `input_lock`
- `keyboard_events`
- `mouse_events`
- `ui_button_events`
- `pointer_hover`
- `modal_dispatch`
- `track`
- `endturn`

Rule:

- if the seam participates directly in lifecycle timing, event ingress,
  modal/input coordination, shell transition dispatch, or task-area runtime
  execution, direct access is acceptable and often clearer

### 3. Keep A Narrow "Review Next" Bucket

No direct `CampaignState` service aliases remain in the review-next bucket.

Historical note:

- `hit_test_service` was the final review-next direct alias
- it now stays grouped under `state.shell_services.hit_test_service`
- event-ingress callers use the explicit state host seam
  `find_clicked_campaign_block(...)`

Update on `2026-04-22`:

- the first interaction cleanup slice already removed the direct aliases for:
  - `lifecycle_binding`
  - `block_click_orchestrator`
  - `event_input_orchestrator`
- those services now stay grouped under `state.interaction_services.*`
- the second interaction cleanup slice later removed the direct aliases for:
  - `turn_orchestrator`
  - `end_turn_orchestrator`
- lifecycle and return-resolution paths now prefer state-level host seams such
  as:
  - `advance_campaign_turn()`
  - `request_end_turn(...)`
- the review-next bucket is therefore smaller than when this document was first
  written and is now empty

Update on `2026-04-24`:

- a hard-fail campaign guardrail now locks host-installed direct service
  aliases to:
  - the stable whitelist above
  - grouped-only reward/thesis/social ownership
  - the optional review-next `hit_test_service` survivor only

Update on `2026-05-12`:

- the `hit_test_service` survivor was removed from direct `CampaignState`
  aliases
- the service remains grouped under `state.shell_services.hit_test_service`
- `CampaignMouseClickIntentResolver` now calls
  `CampaignState.find_clicked_campaign_block(...)` instead of reading the
  service alias and task-area internals directly

### 4. Use State-Level Intent Seams Instead Of Re-Exporting Leaf Services

When a business action needs to stay easy to call, prefer state-level intent
seams such as:

- `request_end_turn(...)`
- `request_event_block(...)`
- `submit_thesis_round_from_writing(...)`
- `open_reward(...)`

Do not reintroduce direct leaf-service aliases just to make a call shorter.

## Counter-Review

Why not keep only `modal`, `tx`, and `track` direct and group everything else?

- because the current frame pipeline is already organized as a shell-owned
  ordered chain of direct runtime ports
- forcing those steps behind `interaction_services.*` would improve symmetry
  more than clarity

Why not keep everything direct if runtime readability matters?

- because reward/thesis/social already proved that duplicated direct access for
  leaf services increases ambiguity without adding real shell value
- AI safety improves when equivalent access paths are removed

Why is `track` still allowed to stay direct even though it is not ideal
long-term?

- because task-area writes are still concentrated there and `EndTurnService`
  still depends on it as a runtime collaborator
- removing the alias now would mostly move syntax around rather than reduce
  architectural risk

This recommendation depends on one assumption:

- the repo will treat retained direct seams as a whitelist, not as permission
  for new direct aliases to spread again

## Decision Summary

1. Direct access is no longer judged by symmetry alone.
2. Leaf service families should converge to grouped-only ownership.
3. Shell/runtime ports may remain direct when they improve execution clarity.
4. The remaining direct surface must be split into:
   - retained shell/runtime seams
   - review-next transitional seams
5. Future campaign cleanup should start from the review-next bucket instead of
   reopening thesis/social/reward direct aliases.
