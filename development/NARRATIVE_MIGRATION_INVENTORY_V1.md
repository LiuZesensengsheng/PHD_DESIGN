# Narrative Migration Inventory V1

## Goal

This document is the `Phase 1` output for `Narrative Pipeline V1`.

It answers three practical questions:

- what content still lives only on the legacy campaign-event path
- what the active tutorial questline already covers
- what should and should not be treated as migration progress

## Inventory Snapshot

### Legacy Campaign Event Route

Location:

- `contexts/campaign/infrastructure/events/`

Current inventory:

- `8` JSON event files
- `21` total legacy choices

These files are still the only source for the old campaign-event runtime route.

### Active Tutorial Runtime Route

Location:

- `data/questlines/questline_tutorial.json`

Current inventory:

- `1` active tutorial questline
- `5` nodes
- `12` runtime choices
- `15` description pages

Current node IDs:

- `node_1_onboarding`
- `node_2_lab_intro`
- `node_2_first_contact`
- `node_2_dust_archive_intro`
- `node_2_post_archive_reward`

### Orthogonal Draft / Source Route

Location:

- `data/events_src/packs/slack/`

Current inventory:

- `19` slack events
- `57` slack choices

This pack is a separate random-event content path.

It is not migration coverage for the old tutorial / prologue campaign events.

## Coverage Classification

There is currently no legacy narrative unit that is fully migrated by ID and by
behavior into the active tutorial questline.

Current classification totals:

- `already covered`: `0`
- `partially covered`: `5`
- `not yet covered`: `3`

| Legacy unit | Title | Status | Active overlap | Notes |
| --- | --- | --- | --- | --- |
| `001_prologue_mentor_meeting` | `与导师的第一次会面` | `partially covered` | `node_1_onboarding` | Same mentor-office setup family, but not direct ID or consequence parity. |
| `supervisor_summons` | `导师的召唤` | `partially covered` | `node_1_onboarding` | Current tutorial still opens on a mentor summons / briefing beat, but does not reproduce the dorm-message setup. |
| `q001_tutorial_project_start` | `一份“光荣”的使命` | `partially covered` | `node_1_onboarding` | This is the closest semantic overlap. The current node preserves the project-briefing + rebellion-to-combat shape, but not the old legacy IDs or exact outcome set. |
| `q002_days_with_senior_01_is_it_fun` | `一次试探` | `partially covered` | `node_2_lab_intro`, `node_2_first_contact` | Current tutorial includes lab introduction and first contact with the project, but not the same senior-probing dialogue. |
| `q002_days_with_senior_02_no_girlfriend` | `深夜八卦` | `not yet covered` | none | No direct equivalent in the active tutorial pack. |
| `q002_days_with_senior_03_where_is_thesis` | `致命问题` | `not yet covered` | none | No thesis-pressure conversation is present in the active tutorial runtime path. |
| `q002_days_with_senior_04_code_crash` | `代码崩溃` | `partially covered` | `node_2_first_contact`, `node_2_dust_archive_intro` | Current tutorial keeps the "error -> ask for help or self-handle -> move deeper into the scenario" family, but drops the old conditional outcomes and legacy combat IDs. |
| `q002_days_with_senior_05_wrap_up` | `阶段性“胜利”` | `not yet covered` | none | Current tutorial has no milestone wrap-up event equivalent yet. |

## Important Negative Finding

The active runtime questline does not directly reference the legacy campaign
event IDs.

That means:

- the new tutorial runtime path is not secretly loading these old IDs
- current overlap is semantic overlap only
- deleting the legacy route now would still drop real content

## Remaining Live Legacy References

The old campaign-event path is still reachable from legacy-side code and tests.

Current known references:

- `contexts/campaign/application/campaign_service.py`
- `run_headless_campaign.py`
- `tests/campaign/test_event_loading.py`

This is why the legacy route should be frozen, not deleted, at `Phase 1`.

## Migration Conclusion

`Phase 1` establishes that the project currently has:

- one real tutorial runtime mainline under `data/questlines/`
- one still-populated legacy campaign-event content route
- one orthogonal slack event source pack that should not be confused with
  tutorial migration progress

The correct `Phase 2` move is therefore:

- define the normalized narrative source schema under `data/narrative_src/`
- keep runtime loading on `data/questlines/*.json`
- avoid deleting legacy content until a later parity phase proves coverage

## Phase 5 Update

`2026-04` tutorial migration status:

- `data/narrative_drafts/tutorial/questline_tutorial.draft.json` is now the
  writable draft entry.
- `data/narrative_src/packs/tutorial/*` is now populated (not header-only).
- `scripts/build_narrative_runtime.py --check` confirms the source build payload
  matches `data/questlines/questline_tutorial.json`.

This means the active tutorial runtime content is now represented in normalized
source with parity.

Legacy tutorial/prologue campaign events are still not fully covered by ID, so
legacy retirement should proceed in batches.

## Phase 7 Batch 1 (Retired Entry Points)

The first retirement batch removes legacy narrative execution entry points while
keeping legacy event JSON as reference data:

- removed `run_headless_campaign.py`
- removed `tests/campaign/test_event_loading.py`
- removed `tests/campaign/test_campaign_vertical_slice.py`
- removed legacy campaign-event runtime modules:
  - `contexts/campaign/application/campaign_service.py`
  - `contexts/campaign/domain/event.py`
  - `contexts/campaign/domain/event_repository.py`
  - `contexts/campaign/infrastructure/json_event_repository.py`

Remaining legacy JSON and localization files under
`contexts/campaign/infrastructure/` are still kept for migration traceability
until a later archival batch.
