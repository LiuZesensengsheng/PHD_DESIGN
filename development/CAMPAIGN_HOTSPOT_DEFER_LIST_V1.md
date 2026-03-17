# Campaign Hotspot Defer List V1

## Goal

Record which campaign hotspots we are intentionally not expanding during the
current UI handoff phase, so the UI collaboration scope stays controlled.

## Defer Now

### `contexts/campaign/services/thesis_meta_service.py`

Why defer:

- it still mixes tier-tag mutation, thesis meta persistence, and compatibility wrappers
- task 8 already split the most UI-sensitive submission flow out of it
- forcing another immediate split now would slow down UI handoff more than it helps

Revisit when:

- tier/meta rules start changing frequently again
- publication and innovation follow-up need another ownership split
- UI work starts needing new thesis seams that cannot be added at the state surface

### `contexts/campaign/services/track_block_service.py`

Why defer:

- it is dominated by board geometry, layout mutation, and campaign runtime rules
- it is not the best place to chase UI handoff safety right now
- abstracting it too early would likely create a wide facade without reducing real risk

Revisit when:

- board mutation rules start blocking content iteration
- multiple services need the same track/board write-path invariants
- geometry and business mutation can be split without widening the API

### `contexts/campaign/services/campaign_mouse_event_service.py`

Why defer:

- it still carries legacy hit-test and adapter baggage
- recent cuts already moved the high-ROI business branches out of it
- more cleanup now is lower ROI than letting the incoming UI developer work against the new seams

Revisit when:

- a new widget needs cleaner adapter layering
- mouse-specific code starts growing new business branches again
- view math and intent translation are ready to split further

### `contexts/campaign/services/thesis_slice.py`

Why defer:

- it is already acting as a migration-phase facade over multiple thesis services
- task 8 narrowed the most important submission path without requiring another large thesis refactor
- thesis aggregate cleanup should wait for clearer pressure from real write-path pain

Revisit when:

- thesis service ownership becomes unclear again after new features
- more than one new thesis write path has to pass through the facade
- thesis runtime invariants need stronger centralization than the current seams provide

## Not A Defer Target

These are still safe to keep evolving during UI work:

- `contexts/campaign/ui_runtime/**`
- `contexts/campaign/rendering/**`
- `contexts/campaign/view.py` for presentation-only changes
- state-level UI host seams on `CampaignState`

Rule:

- presentation growth is fine
- new business branching should still stop at a seam

## Bottom Line

The purpose of this list is not to say "never touch these files".

It is to keep the current handoff phase disciplined:

- use the seams we already cut
- avoid reopening large mixed-responsibility hotspots without a concrete trigger
- protect UI collaboration scope from expanding into another architecture pass
