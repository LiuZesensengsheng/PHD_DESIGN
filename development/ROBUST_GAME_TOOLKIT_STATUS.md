# Robust Game Toolkit Status

`robust_game_toolkit` is now treated as a legacy support layer.

## Current Rule

- Do not add new functionality to `robust_game_toolkit/`
- New code must import shared asset infrastructure from `contexts/shared/infrastructure/assets/`
- The old package exists only as a compatibility layer during migration

## Migration Scope

The only remaining valuable runtime pieces are:

- `AssetManager`
- `PygameLoader`
- small asset-related support types and constants

Everything else in the old package should be considered deletion-first unless a concrete runtime dependency is found.
