# Design Cleanup Candidates

- Status: Draft
- Owner: Team
- Scope: design-cleanup-review
- Canonical: No
- Supersedes: none
- Superseded By: none
- Implemented In: none
- Last Reviewed: 2026-05-17

## Purpose

This is a review queue, not a deletion instruction.

Nothing listed here should be deleted until the owner confirms the action.

## Suggested Actions

| Candidate | Current Signal | Suggested Action | Risk |
| --- | --- | --- | --- |
| `docs/design/ideal/RED_CARD_SLOT_MATRIX_V0.tmp.csv` | Looks like a temporary copy beside `RED_CARD_SLOT_MATRIX_V0.csv` and `RED_CARD_SLOT_MATRIX_V0_ZH.csv`. | Confirm whether it is redundant; delete if no unique rows matter. | Low, but compare with the non-temp CSV first. |
| `docs/design/enemydesigon/TA_TASK_CHAINING_V1.md` | Text appears corrupted or badly transcoded. TA chore-chain behavior is now better represented by `TA_TASK_HOST_MINIMUM_V1.md`, `TA_IMPLEMENTABILITY_MAPPING_V1.md`, and runtime TA data. | Prefer rewrite or archive after owner review; delete only if it contains no recoverable unique design. | Medium, because it may preserve old intent despite bad text. |
| `docs/design/IDEAL_SYSTEM_DESIGN_v8.0_FINAL.md` | Filename says FINAL, but text appears encoding-corrupted and it is referenced by other design docs. | Do not delete now. First extract any still-useful design claims into active docs, then archive or replace. | High, because other docs cite it. |
| `docs/design/campaign/ACKNOWLEDGEMENTS_SYSTEM_v2.md` | Current retained draft for acknowledgements; old v1 has been archived. | Keep for now. Revisit after campaign systems get a current active spec. | Medium. |
| `docs/design/Animate/RUN_CAMPAIGN_RUNTIME_EFFECTS_INVENTORY.xlsx` | Binary spreadsheet exists beside `.csv` and `.md` exports. | Confirm which file is source of truth. If CSV/MD are enough, archive or delete the xlsx later. | Medium, because spreadsheets may contain hidden sheets/formatting. |
| `docs/design/ends/结局2.xlsx` | Binary spreadsheet with unclear index status. | Add to design wiki/index or archive after owner review. | Medium. |

## Next Good Archive Batch

Good candidates for a second archive batch after review:

1. Old paper-line docs if `PAPER_LINE_CURRENT_SPEC.md` is the active source of truth.
2. Old combat/future docs already under `希望未来能实现的设计/` if they are not part of the near-term design surface.
3. Topic drafts that have no runtime/data/test anchor and no owner plan.

Keep deletes separate from archive moves.
