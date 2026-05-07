# Repository Boundary Cleanup V1

## Goal

Clarify where repository boundaries are already paying off, where they should
stay intentionally narrow, and land one small code cut that reduces concrete
persistence leakage without starting a "repository everywhere" rewrite.

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Findings

### Real Repository Boundaries

These are already good repository seams and should stay that way:

- `SaveRepository` / `FileSaveRepository`
  - this is a real external IO boundary
  - the interface is small and stable
- `CombatSaveService`
  - already depends on `SaveRepository` instead of a concrete file adapter
  - this is the right shape for save/load application code

### Boundaries That Should Not Be Repository-ized Now

These are better kept as typed helpers, seam methods, or host-owned runtime
state for now:

- `CampaignSessionStore`
  - shell-owned runtime/session persistence helper
  - not evidence that a universal repository layer is missing
- `TrackBlockService`
  - still geometry-heavy and policy-heavy
  - not a good repository candidate
- `ThesisMetaService`
  - still broad, but the current pressure is write-path ownership, not external
    persistence abstraction

## Small Cut Landed

The concrete persistence leak with the best ROI was inside
`GameStateMachine` save-slot operations.

Before this cut:

- `save_slot()`
- `load_slot()`
- `list_save_slots()`
- `delete_save_slot()`

each directly constructed `FileSaveRepository(root_dir=...)` inline.

After this cut:

- `GameStateMachine` now accepts an optional
  `save_slot_service_factory`
- save-slot operations now go through one `_build_save_slot_service(...)`
  seam
- default runtime behavior is unchanged and still file-based

This keeps concrete file persistence as the default composition choice, but it
stops open-coding infrastructure construction in every save-slot method.

## Why This Cut First

This is a high-value cleanup because it:

- removes repeated concrete persistence construction from the shell entrypoint
- makes save-slot behavior easier to stub in tests
- keeps the repository boundary narrow instead of forcing runtime/session state
  behind fake repositories

## Validation

Focused regressions passed:

- `python -m pytest tests/shared/test_state_machine_save_slots.py tests/save/test_game_save_slot_service.py tests/save/test_file_save_repository.py tests/save/test_combat_save_service.py -q`

## Recommendation

Treat this repository pass as complete for now.

The next DDD follow-up, if we continue, should be:

1. `Campaign Aggregate Candidate Review`
2. `Aggregate Invariant Tests V1`
3. `State Host Facade V1`

Do not expand this into a generic repository layer for campaign runtime,
session helpers, or task-area mutation paths unless a new external data
boundary appears.
