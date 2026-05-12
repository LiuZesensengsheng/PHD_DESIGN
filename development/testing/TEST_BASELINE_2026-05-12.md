# Test Baseline 2026-05-12

## Scope

This baseline supports `Test Strategy V1`.

Current task scope excludes `cardanalysis` / `combat_analysis` implementation
work. Slow tests in those areas are recorded as data, but they are not cleanup
targets for this line.

## Commands Run

- `py -3.11 -m pytest -q --durations=60 --durations-min=0.05`
- `py -3.11 scripts/run_repo_smoke_baseline.py --group cross-context`
- `py -3.11 -m pytest tests/shared/test_text_encoding_guards.py tests/test_contract_police.py tests/shared/test_naming_and_contract_guards.py -q`
- `py -3.11 -m pytest tests/combat/test_combat_mainline_smoke_pack_v1.py tests/campaign/test_campaign_transition_request_contract.py tests/shared/test_e2e_headless_encounter_smoke.py -q`

## Current Full-Suite Shape

- Full suite runtime on this workstation: about `4m10s`.
- The default full gate remains `py -3.11 -m pytest -q`.
- Full suite passed during baseline capture.

## Slowest Observations

Top slow tests were concentrated in two buckets:

1. `cardanalysis` / `combat_analysis` benchmark and modelization tests.
   - These are out of scope for this test-strategy line.
   - Several individual tests were in the `3s-13s` range.
2. repository-wide scanning guards.
   - `tests/scripts/test_check_combat_compat_zero.py::test_check_combat_compat_zero_passes_on_current_repo`
     took about `15.3s`.
   - `tests/scripts/test_check_combat_compat_zero.py::test_check_combat_compat_zero_cli_returns_success`
     took about `11.7s`.
   - `tests/combat/test_combat_mainline_allowlist_v1.py` includes several
     source-scanning assertions around `2.2s` each.

Headless campaign/shared e2e tests are slower than local unit tests but still
within a reasonable smoke-test budget. Representative calls were mostly below
`2s`.

## Existing Useful Entry Points

- `scripts/run_repo_smoke_baseline.py`
  - useful for phase or line closure
  - not optimized as the fastest developer feedback loop
- `tests/shared/test_text_encoding_guards.py`
  - catches Windows line-ending regressions quickly
- `tests/test_contract_police.py` and
  `tests/shared/test_naming_and_contract_guards.py`
  - compact architecture guardrail pack

## Recommended First Split

- `quick smoke`: tiny non-cardanalysis correctness check for fast AI feedback.
- `contract smoke`: architecture and source-scanning checks for cleanup slices.
- `repo smoke baseline`: current broader smoke groups, still useful at phase
  boundaries.
- `full suite`: final commit or line gate until the commit policy changes.

