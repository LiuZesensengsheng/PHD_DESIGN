# Aggregate Invariant Tests V1

## Goal

Lock the most valuable campaign-side aggregate and aggregate-candidate
invariants as executable tests instead of relying on chat memory or architectural
intent alone.

- Level: `L3 Architecture`
- Date: `2026-03-17`

## Scope

This pass does not formalize new aggregate types.

It protects the current highest-value boundaries that were already identified in
the recent DDD review:

- `Campaign` shell lifecycle boundary
- `Task Area` board partition boundary
- track-local `Thesis` progression as the leading aggregate candidate

## Invariants Locked

### 1. Shell Roundtrip Preserves Thesis Track Partition

Protected by:

- `tests/campaign/test_campaign_aggregate_invariants.py`
- `tests/campaign/test_campaign_orchestration_aggregate_invariants.py`

Key rule:

- cleanup/startup roundtrip must preserve per-track thesis partition instead of
  smearing track-local tier/meta/tag state together

What is now checked:

- track `0` and track `2` keep distinct thesis tiers after roundtrip
- submitted-round history stays attached to the correct track
- paper tags stay attached to the correct track
- persisted `_thesis_tier_map` remains partitioned by track

### 2. Track-Local Thesis Writes Stay Isolated

Protected by:

- `tests/campaign/test_campaign_aggregate_invariants.py`
- `tests/campaign/test_thesis_write_path_service.py`

Key rule:

- tier writes on one thesis track must not mutate thesis blocks or meta on other
  tracks

What is now checked:

- setting tier on track `0` does not add tier tags to track `2`
- setting tier on track `2` later does not rewrite track `0`
- per-track `current_tier` and persisted tier map remain isolated

### 3. Thesis Verdict Follow-Up Only Mutates Target Track

Protected by:

- `tests/campaign/test_campaign_aggregate_invariants.py`
- `tests/campaign/test_thesis_aggregate_invariants.py`
- `tests/campaign/test_thesis_verdict_follow_up_contract.py`

Key rule:

- reject/accept follow-up on one thesis track must not corrupt another
  submitted thesis track

What is now checked:

- target track can change tier cap / clear current tier / advance follow-up
- non-target track keeps:
  - tier
  - meta
  - paper tags
  - persisted tier-map entry

### 4. Existing Board and Shell Invariants Stay In Place

This pass also explicitly builds on earlier invariant packs instead of replacing
them:

- `tests/campaign/test_task_area_invariants.py`
  - board overlap safety
  - trailing DDL protection
  - event-bubble vs block separation
- `tests/campaign/test_campaign_orchestration_aggregate_invariants.py`
  - startup/cleanup shell roundtrip
  - route-resolution consume-once behavior
  - thesis combat-sync consume-once behavior

### 5. Task-Area Internal Rule Splits Keep Stable Board Outcomes

Protected by:

- `tests/campaign/test_track_block_service_overlap_guard.py`
- `tests/campaign/test_track_block_service_ddl.py`
- `tests/campaign/test_track_block_service_fusion_thesis_nodes.py`
- `tests/campaign/test_task_area_invariants.py`
- `tests/campaign/test_campaign_domain_events.py`

Key rule:

- task-area internals may split into smaller rule helpers, but overlap safety,
  DDL pressure behavior, fusion outcomes, and emitted domain events must remain
  stable at the facade boundary

What is now checked:

- illegal logical overlap still hard-fails in development-time guards
- DDL snake still distinguishes:
  - no-op chase
  - just-touched no-op
  - single-step eat
- thesis task-area event/combat nodes still follow the same fusion rule as
  other non-DDL blocks
- task-area fusion and DDL-eat steps still emit the expected domain events

## Validation

Focused regression pack passed:

- `python -m pytest tests/campaign/test_campaign_aggregate_invariants.py tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py tests/campaign/test_task_area_invariants.py tests/campaign/test_track_block_service_overlap_guard.py tests/campaign/test_track_block_service_ddl.py tests/campaign/test_track_block_service_fusion_thesis_nodes.py -q`

## Recommendation

Treat aggregate-candidate invariants and task-area split guardrails as "good
enough" for this refactor line.

There is no automatic next DDD step from this note.

Only reopen this line if:

- thesis identity pressure grows beyond `track_index`
- task-area rules need another behavior change that current helper boundaries
  no longer contain
