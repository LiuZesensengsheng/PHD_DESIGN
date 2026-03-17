# Campaign Task Area Invariant Tests V1

## Goal

Record the current focused tests that protect the most important `Task Area`
board invariants.

This is not a full test strategy document. It is a narrow guardrail note for
the current task-area tightening phase.

## Protected Invariants

### 1. No Logical Overlap On The Same Task Line

Protected by:

- `tests/campaign/test_track_block_service_overlap_guard.py`
- `tests/campaign/test_task_area_write_path_contract.py`

Meaning:

- task-area blocks on the same track must not overlap in logical
  `start_turn/duration` space

### 2. Each Task Line Ends With A DDL Block

Protected by:

- `tests/campaign/test_track_service_blueprint.py`
- `tests/campaign/test_track_service_readonly.py`
- `tests/campaign/test_task_area_invariants.py`

Meaning:

- after task-area blueprint application or stabilization, each track should end
  with a trailing `ddl` block

### 3. Event Bubbles Are Overlays, Not Blocks

Protected by:

- `tests/campaign/test_task_area_invariants.py`
- `tests/campaign/test_campaign_event_input_orchestrator.py`

Meaning:

- line-bubble interaction may open UI and consume overlay state
- it must not mutate the underlying task-area block list as if the bubble were
  a schedulable block

## Current Bottom Line

The current invariant pack is intentionally small:

- protect board geometry
- protect trailing DDL ownership
- protect overlay-vs-block separation

That is enough to support the next task-area cuts without pretending the full
aggregate model is already finished.
