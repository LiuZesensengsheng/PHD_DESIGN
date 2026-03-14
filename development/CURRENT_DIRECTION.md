# Current Direction

## North Star

- The long-term direction is `Godot-ization inside pygame`, not a full migration to Godot.
- Prefer architecture migration before engine migration.
- Keep the project memory system lightweight and file-based; do not build game-runtime memory mechanics for Codex collaboration.

## Current Priorities

- Clarify retained-UI and runtime-widget boundaries inside the existing pygame codebase.
- Preserve steady feature/content iteration speed while improving migration-ready architecture.
- Keep project memory short, searchable, and easy for Codex to resume from without chat history.
- Prefer memorable direct entrypoints (`pytest` or single-purpose scripts) over legacy aggregated tooling.

## Explicit Non-Goals

- No one-shot engine rewrite.
- No heavy memory platform or database as the source of truth for project direction.
- No large-scale UI rewrite without a clear migration or maintenance payoff.
- No hard-to-remember umbrella tooling as the default automation surface.

## Open Questions

- How far should Godot-like node/runtime patterns be pushed before they stop paying for themselves inside pygame?
- Which interactive campaign elements should move into runtime widgets first after the phone widget path?
- When hybrid search is added later, which document set should remain in the default hot index without creating retrieval noise?

## Last Updated

- `2026-03-14`
