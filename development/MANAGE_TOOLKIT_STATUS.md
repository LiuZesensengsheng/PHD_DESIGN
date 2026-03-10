# Manage Toolkit Status

`scripts/manage_toolkit/` has been removed.

## Current Rules

- New runtime code must not import from `scripts/manage_toolkit/`
- Shared runtime-safe constants live in [constants/tooling.py](/D:/PHD_SIMULATER/constants/tooling.py)
- Do not recreate `scripts/manage_toolkit/` as a project utility layer

## Outcome

The former analyzer / checker / executor / manager stack was fully retired.

Any future tooling should either:

1. live as a focused standalone script under `scripts/`, or
2. move into a clearly scoped shared package only if it is genuinely reused.
