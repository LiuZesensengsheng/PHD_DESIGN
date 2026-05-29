# Design Archive

- Status: Active
- Owner: Team
- Scope: archived-design-docs
- Canonical: No
- Supersedes: none
- Superseded By: none
- Implemented In: none
- Last Reviewed: 2026-05-17

## Purpose

This directory stores design documents that should not be part of the default implementation read path.

Archive does not mean useless. It means:

- the doc is superseded by a newer active spec, or
- the doc is retained only as reference/history, or
- the doc needs owner review before reuse.

## Archived Batches

### 2026-05-17 Design Governance Batch 1

| Old Path | New Path | Reason |
| --- | --- | --- |
| `docs/design/ideal/RED_IDEAL_CARD_DESIGN_V1.md` | `docs/design/archive/ideal/RED_IDEAL_CARD_DESIGN_V1.md` | Superseded by red v2. |
| `docs/design/ideal/WHITE_IDEAL_CARD_DESIGN_V1.md` | `docs/design/archive/ideal/WHITE_IDEAL_CARD_DESIGN_V1.md` | Superseded by white v2/v3. |
| `docs/design/ideal/WHITE_IDEAL_CARD_DESIGN_V2.md` | `docs/design/archive/ideal/WHITE_IDEAL_CARD_DESIGN_V2.md` | Superseded by white v3. |

Reverted from this batch:

| Path | Reason |
| --- | --- |
| `docs/design/campaign/ACKNOWLEDGEMENTS_SYSTEM.md` | Owner wants to keep the acknowledgements reference doc in the campaign design directory. |

## Cleanup Review Queue

- [CLEANUP_CANDIDATES.md](CLEANUP_CANDIDATES.md) lists possible future archive/delete candidates.
- That file is a review queue only; do not treat it as owner approval.

## Restore Rule

If an archived doc becomes useful again, do not silently move it back into a hot directory. First decide whether it is:

- `Reference`
- `Draft`
- `Future`
- `Active`

Then update the relevant design README and wiki page.
