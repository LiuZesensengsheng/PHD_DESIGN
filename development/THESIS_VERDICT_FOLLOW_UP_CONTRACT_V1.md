# Thesis Verdict Follow-Up Contract V1

## Goal

- Make thesis verdict application order explicit after write-path and block-mutation seams landed.
- Prevent future drift in reject/accept/major/minor follow-up sequencing.

## Contract Order

1. Unlock blocking judgment input.
2. Remove direct verdict-owned blocks.
3. Record the verdict in session state.
4. Apply paper-tag mutations.
5. Apply round-level block cleanup.
6. Branch into one of:
   - combat handoff
   - non-combat follow-up
7. Refresh forced-DDL state only for reject/accept paths.

## Why This Matters

- The ordering is now visible in code instead of being hidden in one long method body.
- Contract tests can assert the most expensive sequencing assumptions directly.
- Later host narrowing can target smaller, more explicit checkpoints.

## Coverage

- `tests/campaign/test_thesis_verdict_follow_up_contract.py`
  - reject path ordering
  - major revision combat handoff ordering
