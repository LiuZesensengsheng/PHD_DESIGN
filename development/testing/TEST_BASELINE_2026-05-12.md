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
- After the 2026-05-13 source-scan and repeated-summary optimization slice,
  full suite runtime on this workstation is about `3m18s`
  (`py -3.11 -m pytest -q --durations=60 --durations-min=0.05`).
- After the second low-risk fixture-sharing pass, full suite runtime on this
  workstation is about `3m10s`
  (`py -3.11 -m pytest -q --durations=60 --durations-min=0.05`).
- After the focused cardanalysis reranker/shadow reuse pass, full suite runtime
  on this workstation is about `3m00s`
  (`py -3.11 -m pytest -q --durations=60 --durations-min=0.05`).
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

## 2026-05-13 Optimization Notes

Completed low-risk speedups:

- `scripts/check_combat_compat_zero.py` now caches text reads and filters AST
  parsing to files that contain relevant method/import tokens.
- `tests/combat/test_combat_mainline_allowlist_v1.py` uses the same cached
  source-scanning pattern for its guard assertions.
- `tests/shared/test_text_encoding_guards.py` computes the repository text
  encoding report once per module instead of once per assertion.
- `scripts/run_sts_catalog_holdout_benchmark.py` no longer evaluates the same
  benchmark twice just to establish artifact completeness.
- The repeated modelization/holdout benchmark tests now share module-scoped
  summary fixtures where the asserted payload is identical.
- Additional ranking export and reranker tests now share repeated module-scoped
  datasets or summaries where the asserted payload is identical:
  - STS catalog holdout ranking export;
  - pick ranking export and pairwise reranker;
  - reviewed retrieval ranking export and pairwise reranker.
- `modelization_shadow_report` now reuses already-built holdout/retrieval
  training summaries and evaluation datasets when the shadow training/evaluation
  inputs are identical.
- Holdout and reviewed-retrieval pairwise reranker training now precomputes raw
  and standardized row feature values per training fold instead of recomputing
  them for every pairwise delta.
- `run_sts_catalog_holdout_benchmark.py` passes its shadow evaluation dataset
  into the shadow summary builder and reuses the training summary when the input
  also serves as the shadow training input.

Observed impact:

- `scripts/check_combat_compat_zero.py` dropped from about `15s` to about
  `0.5s` on this workstation.
- The combined compat-zero + combat allowlist guard pack dropped from about
  `35s` to about `2s`.
- The first full-suite pass dropped from about `4m10s` to about `3m18s`.
- The second fixture-sharing pass dropped the full suite further to about
  `3m10s`.
- The focused cardanalysis reranker/shadow reuse pass dropped the full suite
  further to about `3m00s`.

Representative cardanalysis observations:

- `build_modelization_shadow_summary(report_id="shadow_probe")` dropped from
  about `13.3s` to about `5.4s` on this workstation.
- The aggregate holdout pairwise reranker training profile dropped from about
  `2.4s` to about `0.7s`.
- The reviewed retrieval pairwise reranker training profile dropped from about
  `2.1s` to about `1.0s`.

Remaining slowest tests are still concentrated in cardanalysis/combat-analysis
holdout benchmark scripts, holdout pairwise reranker integration paths, and
headless campaign/shared flows. Further cardanalysis reductions should focus on
benchmark/runtime design or snapshot reuse, not deleting coverage.

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
