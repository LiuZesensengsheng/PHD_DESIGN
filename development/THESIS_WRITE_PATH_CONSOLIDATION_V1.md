# Thesis Write-Path Consolidation V1

## Goal

- Reduce scattered thesis write paths without opening a full thesis DDD rewrite.
- Keep existing campaign/thesis entrypoints stable for current callers and tests.
- Move high-frequency thesis mutations behind one explicit write owner.

## Landed Seam

- Added `contexts/campaign/services/thesis_write_path_service.py`
- `ThesisMetaService` now keeps:
  - tier-selection modal/UI flow
  - compatibility wrappers for existing callers
- `ThesisWritePathService` now owns:
  - thesis meta creation/defaulting
  - title/subtitle/title-meta backfill
  - thesis tier tag writes across thesis blocks
  - runtime/session tier persistence
  - submission tier-cap persistence
  - submitted-round and submission-history writes
  - publication history persistence

## Current Call Flow

1. UI or flow service calls existing thesis seam on `CampaignState` / `ThesisMetaService`.
2. `ThesisMetaService` keeps the orchestration-facing API stable.
3. `ThesisWritePathService` performs the actual runtime/meta/persistent mutation.

## Explicitly Not In Scope

- Full thesis aggregate redesign
- Rewriting thesis round/block removal into a new aggregate model
- UI rewrite or node-tree migration work
- Publication reward/combat follow-up redesign

## Next Recommended Cut

- Keep the same strategy and shrink one more mutation hotspot:
  - round activation/removal
  - review-chain block wake-up
  - other thesis block-list mutations that still live inline in flow services
