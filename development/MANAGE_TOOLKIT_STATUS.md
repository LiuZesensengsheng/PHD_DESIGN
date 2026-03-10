# Manage Toolkit Status

`scripts/manage_toolkit/` is now treated as legacy tooling.

## Current Rules

- New runtime code must not import from `scripts/manage_toolkit/`
- New tool features should not be added to this package
- Shared runtime-safe constants now live in [constants/tooling.py](/D:/PHD_SIMULATER/constants/tooling.py)
- The remaining package exists only to support any old script entrypoints that still rely on `constants.py`

## Cleanup Direction

The former analyzer / checker / executor / manager stack is no longer part of the active architecture.

Default policy:

1. Keep only the smallest surface still needed by old scripts
2. Delete unused legacy modules in batches
3. Do not treat this package as a future platform layer
