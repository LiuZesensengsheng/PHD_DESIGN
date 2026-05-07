# Thesis Block Mutation Consolidation V1

## Goal

- Remove thesis block-list mutations from scattered flow services.
- Keep current thesis UI and state-level seams stable.
- Make thesis round/block mutation ownership more explicit without a full aggregate rewrite.

## Landed Seam

- Added `contexts/campaign/services/thesis_block_mutation_service.py`
- The new seam now owns:
  - review-chain activation for a submitted round
  - writing-block removal by id
  - round-block removal after a verdict
  - next dormant round activation

## Delegation Changes

- `ThesisSubmissionFlowService`
  - no longer mutates `state._blocks` directly for review-chain wake-up or writing-block removal
- `ThesisJudgmentFlowService`
  - no longer mutates `state._blocks` directly for remove-by-id or round cleanup
- `ThesisRoundService`
  - keeps round-tag helpers
  - delegates active block mutations to the shared block seam

## Why This Cut Matters

- It concentrates thesis block mutation semantics in one place.
- It narrows the set of files that can silently drift thesis round behavior.
- It makes the next verdict-order and invariant-test cuts cheaper.

## Next Recommended Cut

- `Thesis Verdict Follow-Up Contract V1`
  - make reject/accept/major/minor follow-up order even more explicit now that block mutation ownership is centralized
