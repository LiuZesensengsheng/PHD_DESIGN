# Robust Game Toolkit Status

`robust_game_toolkit` was a legacy support layer. The migration is complete and the root package has been removed.

## Current Rule

- New code must import shared asset infrastructure from `contexts/shared/infrastructure/assets/`
- Do not recreate `robust_game_toolkit/` as a root package

## Migration Scope

The only remaining valuable runtime pieces are:

- `AssetManager`
- `PygameLoader`
- small asset-related support types and constants

Everything else in the old package should be considered deletion-first unless a concrete runtime dependency is found.
