# Test Strategy V1

## Goal

Make test feedback faster and clearer during architecture refactor work without
reducing regression confidence.

This is a testing-governance line, not a delete-test line.

## Scope

In scope:

- define test tiers and stable entry points
- add pytest markers for future tagging
- add a fast non-cardanalysis smoke entry point
- record current runtime baseline and slow-test observations
- keep the existing full-suite gate intact until a later explicit decision

Out of scope for this line:

- deleting coverage just to reduce runtime
- changing cardanalysis / combat_analysis tests
- enabling pytest-xdist by default
- changing the commit gate before a separate decision-log update

## Test Tiers

### Focused

Use for the active code slice.

Examples:

- one touched module's tests
- one focused script test
- one small campaign/combat contract pack

Focused tests are required during implementation, but they do not replace the
current commit gate.

### Quick Smoke

Use for fast AI feedback before broader validation.

Default entry point:

- `py -3.11 scripts/run_test_smoke.py --profile quick`

Target runtime:

- under `30s` on the current workstation

Current purpose:

- prove that core non-cardanalysis paths still import and run
- catch common architecture and headless smoke regressions early

### Contract Smoke

Use before finishing refactor slices that affect boundaries.

Default entry point:

- `py -3.11 scripts/run_test_smoke.py --profile contract`

Current purpose:

- run compact architecture, encoding, naming, combat-compat, and campaign
  boundary checks
- catch source-scanning and guardrail regressions before the full suite

### Repo Smoke Baseline

Use at phase boundaries or when a change touches multiple subsystems.

Default entry point:

- `py -3.11 scripts/run_repo_smoke_baseline.py`

Current purpose:

- run the broader combat/campaign/cross-context/repo guard packs
- remain smaller and more diagnostic than the full suite

### Full Suite

Use for commit readiness unless the commit gate is explicitly changed.

Default entry point:

- `py -3.11 -m pytest -q`

Current status:

- required before every commit by `AGENTS.md`
- do not replace it with smoke-only validation without a later decision-log
  update

## Marker Policy

Markers describe test intent. They should not be used to hide failing tests.

Initial markers:

- `smoke`: intentionally small regression coverage
- `contract`: boundary, architecture, or source-scanning contract
- `integration`: multi-module or headless flow coverage
- `slow`: intentionally slower test that should stay out of quick feedback
- `cardanalysis`: cardanalysis / combat_analysis tests, out of scope for this
  line unless explicitly reopened
- `headed`: tests that intentionally open a real pygame window

Do not mass-tag the whole suite mechanically. Tag tests only when the owning
entry point needs the marker.

## Slow-Test Policy

Before optimizing a slow test:

1. capture data with `--durations`
2. classify whether it is slow because of data size, source scanning, fixture
   setup, subprocess calls, or headless runtime
3. preserve one representative integration path before splitting repeated
   assertions into smaller contract tests

Do not delete a slow test until an equal or stronger assertion exists elsewhere.

## Future Work

Recommended next slices:

1. add marker coverage to the tests used by `run_test_smoke.py`
2. split duplicated campaign/combat fixtures after measuring setup hotspots
3. review source-scanning tests that duplicate the same full-repo traversal
4. evaluate `pytest-xdist` only after global-state and filesystem assumptions
   are audited

