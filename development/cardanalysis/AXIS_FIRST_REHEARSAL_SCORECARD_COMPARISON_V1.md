# Axis-First Rehearsal Scorecard Comparison V1

## Purpose

`axis_first_rehearsal_scorecard_comparison_v1` is a report-only comparison for
two supplied `complete_card_draft_v1` files that both start from the same
axis-first STS1 character context.

It answers:

```text
When a fresh owner/Codex-supplied draft enters the axis-first rehearsal path,
does the existing scorecard delta show improvement, regression, or an exam
visibility gap relative to the fixture baseline for that character lane?
```

## Workflow Position

```text
mechanism_axis_search_bundle_v1
  -> mechanism_axis_design_brief_v1
  -> card_package_proposal_v1 seed
  -> sts1_exam_target_v1
  -> card_package_variant_set_v1
  -> baseline complete_card_draft_v1
  -> latest complete_card_draft_v1
  -> axis_first_draft_writing_rehearsal_v1 for each draft
  -> autonomous_card_package_design_run_v1 for each draft
  -> card_design_scorecard_delta_report_v1
  -> axis_first_rehearsal_scorecard_comparison_v1
```

The surface is deliberately narrow. It rebuilds both rehearsals from supplied
files, compares their existing scorecards, and records both raw scorecard case
matching and an advisory attempt lane. The lane is derived from shared
axis-search, design-brief, package-seed, target, variant-set, and selected
variant identity, so distinct draft package case ids can still be compared as
the same exam lane without pretending they are the same case.

## Current Silent Result

The first fresh Codex-supplied Silent attempt is:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/
  silent_axis_first_codex_poison_retain_shiv_attempt_v1.json
```

The harder same-lane Silent sensitivity attempt is:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/
  silent_axis_first_codex_poison_retain_shiv_harder_attempt_v1.json
```

It validates as `complete_card_draft_v1`, remains `owner_supplied_draft` /
`review_needed`, and receives the same advisory score as the Silent fixture
baseline:

- baseline score: `92.78 strong`
- latest score: `92.78 strong`
- scorecard aggregate delta: `0.0`
- scorecard delta status: `stable_no_material_delta`
- attempt lane: `axis_first_attempt_lane_2119350afcc4`
- attempt lane status: `matched_attempt_lane`
- attempt lane claim status: `same_lane_no_material_delta`
- lane sensitivity status: `content_changed_score_static`
- lane text similarity: `0.704`
- lane sensitivity warning: `lane_content_changed_without_score_movement`
- content visibility status: `content_change_not_reflected_in_scorecard`
- affected scorecard dimensions:
  `axis_alignment`, `failure_state_quality`, `fun_tension`,
  `strength_risk_control`, `sts1_like_fit`
- highest-change slot: `axis_enabler_signal` (`venom_mark` -> `toxic_cue`)
- scorecard visibility patch status:
  `patch_recommended_for_scorecard_visibility`
- top patch lane: `axis_alignment_content_delta_visibility`
- scorecard dimension visibility notes:
  `scorecard_dimension_notes_available`
- largest next gap: `lane_review_sensitivity`

The important finding is not that the content improved. The comparison now
recognizes both drafts as the same Silent axis-first attempt lane, while still
recording that the raw scorecard case ids differ. The lane-level review also
detects that card ids, card names, and rules text changed while aggregate score,
dimension averages, and issue movement stayed static. The next gap is therefore
`lane_review_sensitivity`: before writing another harder attempt, inspect the
scorecard or exam blind spots that let same-lane content changes disappear.

The content-change signal is intentionally advisory. It decomposes same-lane
changes by package slot, numeric profile, trigger keywords, setup tax, role
tags, and rules-text token similarity. For the current Silent pair it recommends
exam visibility patches such as:

- `surface_same_lane_content_delta_in_scorecard_notes`
- `add_rules_texture_contrast_to_fun_tension_review`
- `add_low_roll_recovery_contrast_to_failure_state_review`
- `add_numeric_profile_delta_to_strength_risk_review`
- `add_trigger_word_contrast_to_sts1_like_review`

The comparison also emits an advisory `scorecard_visibility_patch_plan`. This
turns the raw content-change signals into prioritized future scorecard patch
lanes without changing current scores or weights. The current top lanes are:

- `axis_alignment_content_delta_visibility`
- `fun_tension_rules_texture_visibility`
- `failure_state_low_roll_visibility`
- `strength_numeric_profile_visibility`
- `sts1_like_trigger_word_visibility`

Those lanes are also projected into `scorecard_dimension_visibility_notes`.
These notes are grouped by existing scorecard dimensions, include a
`visibility_lane`, and carry a structured `content_delta_summary`. They preserve
the current score and dimension averages while making static-score blind spots
visible. For the current Silent pair the first note says `axis_alignment` should
surface the `axis_enabler_signal` change from `venom_mark` to `toxic_cue` even
though the axis-alignment score stayed static. The notes also cover the
`character_identity` / character-texture lane when rules texture, package tags,
or role tags move without score movement.

The harder attempt keeps the same axis-first lane but stresses exactness, setup
tax, fail-state quality, and strength-risk visibility. In that comparison the
lane review reports `content_changed_score_changed`, so the notes can explain
which dimensions moved rather than only naming a static-score blind spot.

## Current Ironclad Result

The second role now uses the axis search result directly instead of the older
four-character fixture's strength-first target. The searched Ironclad axes are:

- `exhaust`
- `block_engine`
- `strength_scaling`

The baseline and fresh supplied drafts are:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/
  ironclad_exhaust_block_strength_exam_draft_v1.json
  ironclad_axis_first_codex_exhaust_block_strength_attempt_v1.json
```

Both drafts validate as `complete_card_draft_v1`, remain
`owner_supplied_draft` / `review_needed`, and replay through the same
axis-first comparison lane. The current comparison again reports a static
aggregate score while content changed, so the next gap remains
`lane_review_sensitivity`. The important new coverage is that scorecard
visibility notes now recognize axis-relevant same-slot changes for non-Silent
lanes, including exhaust, block, and strength language, without changing scores
or weights.

## Current Defect Result

The third role uses a Defect axis-search request tuned for high decision density
and readable orb state. The searched Defect axes are:

- `orb_control`
- `frost_control`
- `power_focus_scaling`

The baseline and fresh supplied drafts are:

```text
tests/fixtures/combat_analysis/complete_card_draft_v1/
  defect_orb_focus_frost_exam_draft_v1.json
  defect_axis_first_codex_orb_focus_frost_attempt_v1.json
```

Both drafts validate as `complete_card_draft_v1`, remain
`owner_supplied_draft` / `review_needed`, and replay through the same
axis-first comparison lane. The comparison intentionally preserves a static
score while surfacing Defect-specific content movement: `calibrated_channel` to
`cold_start_signal` changes the enabler's orb/frost/focus texture, first-play
trigger wording, block/draw profile, and setup tax. The resulting dimension
visibility notes include axis alignment, character texture, STS1-like fit,
strength risk, combo risk, fun tension, and failure-state lanes without changing
score weights or authority.

## Boundary

This surface does not:

- call an LLM API;
- generate complete-card draft text at runtime;
- write runtime card data;
- promote formal cards;
- create hard gates;
- claim reviewed evidence;
- enable default LLM generation;
- enable default synthesis;
- enable learned or reranker behavior.

The fresh Codex-supplied draft is unreviewed report-only material. It exists to
exercise the exam loop and reveal the next capability gap.

## Entrypoints

```powershell
python scripts/run_axis_first_rehearsal_scorecard_comparison.py --axis-search tests/fixtures/combat_analysis/mechanism_axis_design_brief_v1/silent_axis_search_bundle_snapshot_v1.json --design-brief tests/fixtures/combat_analysis/mechanism_axis_package_seed_v1/silent_axis_design_brief_snapshot_v1.json --package-seed <card_package_proposal_v1.json> --target tests/fixtures/combat_analysis/sts1_exam_target_v1/silent_poison_retain_shiv_exam_target_v1.json --variant-set tests/fixtures/combat_analysis/card_package_variant_set_v1/silent_poison_retain_shiv_variant_set_v1.json --baseline-draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_poison_retain_shiv_exam_draft_v1.json --latest-draft tests/fixtures/combat_analysis/complete_card_draft_v1/silent_axis_first_codex_poison_retain_shiv_attempt_v1.json --output-dir tmp/combat_analysis/axis_first_rehearsal_scorecard_comparison_current
py -3.11 -m pytest tests/toolkit/combat_analysis/test_axis_first_rehearsal_scorecard_comparison_v1.py tests/scripts/test_run_axis_first_rehearsal_scorecard_comparison.py -q
```

Use `scripts/run_mechanism_axis_package_seed.py` to create the package seed from
the current design brief before running the comparison command.

The emitted `scorecard_dimension_visibility_notes` can be passed to:

```powershell
python scripts/run_card_design_scorecard.py --input <supported_exam_or_iteration_snapshot.json> --visibility-notes <axis_first_rehearsal_scorecard_comparison_v1_snapshot.json> --output-dir tmp/combat_analysis/card_design_scorecard_with_visibility_notes_current
python scripts/run_card_design_scorecard_delta_report.py --input <baseline_card_design_scorecard_v1_snapshot.json> --input <latest_card_design_scorecard_v1_snapshot.json> --visibility-notes <axis_first_rehearsal_scorecard_comparison_v1_snapshot.json> --output-dir tmp/combat_analysis/card_design_scorecard_delta_report_with_visibility_notes_current
```

## Interpretation

A clean comparison means the fresh supplied draft can be replayed through the
axis-first exam loop and compared against the fixture baseline. It does not prove
autonomous card-design quality, balance, reviewed evidence status, or promotion
readiness.

The next capability gap is lane-level review sensitivity. Repeated attempts can
now be grouped into one axis-first exam lane, and the Silent, Ironclad, and
Defect pairs show changed card content without score movement. The loop can now
name which scorecard dimensions should become more observant before claiming
design-quality movement.
