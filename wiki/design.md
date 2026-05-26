# Design Wiki

- Status: Active
- Owner: Team
- Scope: design-navigation
- Canonical: No
- Supersedes: none
- Superseded By: none
- Implemented In: none
- Last Reviewed: 2026-05-17

## Purpose

This page is the human-facing map for game design docs. For implementation work, follow the linked active specs and runtime data contracts.

## Current Design Entrypoints

| Area | Start Here | Current Posture |
| --- | --- | --- |
| Cross-system principles | [DESIGN_NORTH_STAR_V1.md](../design/DESIGN_NORTH_STAR_V1.md) | Active north star. |
| Design doc governance | [DESIGN_DOC_GOVERNANCE_V1.md](../development/architecture/DESIGN_DOC_GOVERNANCE_V1.md) | Active governance rule. |
| Design document index | [docs/design/README.md](../design/README.md) | Active design index. |
| Ideal/card design | [ideal/README.md](../design/ideal/README.md) | Pilot-governed. Red and white are active; green is draft. |
| Campaign/tutorial design | [campaign/README.md](../design/campaign/README.md) | Pilot-governed. Tutorial questline is active; many systems remain draft/reference. |
| Enemy/encounter design | [enemydesigon/README.md](../design/enemydesigon/README.md) | Pilot-governed. TA rollout has active implementation mapping. |
| Archived design docs | [archive/README.md](../design/archive/README.md) | Not in the default implementation read path. |
| Cleanup candidates | [CLEANUP_CANDIDATES.md](../design/archive/CLEANUP_CANDIDATES.md) | Review queue only; not approval to delete. |

## Runtime Anchors

| Runtime Area | Source |
| --- | --- |
| Red cards | `data/cards/red/` |
| White cards | `data/cards/white/` |
| Tutorial narrative source | `data/narrative_src/packs/tutorial/` |
| Tutorial runtime questline | `data/questlines/questline_tutorial.json` |
| TA combat source pack | `data/combat/ta/` |
| TA runtime encounters | `data/questlines/encounters_ta.json` |

## Cleanup Policy

Old design docs are handled in small batches:

1. Keep active specs and runtime anchors visible.
2. Propose clear P2 material first: temp files, duplicated old drafts, corrupted notes, or raw packages whose extracted/source form remains.
3. Prefer marking `Draft`, `Reference`, `Future`, `Archived`, or `Superseded` before deleting design material with unclear value.
4. Do not let Future or Archive docs into the default implementation read path.

Delete only after owner confirmation. Deleted docs remain recoverable from git history, but git history is not a substitute for review.
