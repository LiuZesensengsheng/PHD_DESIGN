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

## Validation

Focused regression pack passed:

- `python -m pytest tests/campaign/test_campaign_aggregate_invariants.py tests/campaign/test_thesis_aggregate_invariants.py tests/campaign/test_campaign_orchestration_aggregate_invariants.py tests/campaign/test_task_area_invariants.py -q`

## Recommendation

Treat aggregate-candidate invariants as "good enough" for this phase.

If DDD work continues now, the next highest-ROI step is:

1. `State Host Facade V1`

with one rule:

- only narrow services whose responsibilities are already stable
- do not reopen `TrackBlockService` or force a whole-campaign facade
