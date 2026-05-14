# Control Card Production Trial Plan V1

## Purpose

`control_card_production_trial_plan_v1` records the next cardanalysis priority:
use the existing report-only control discipline plus ideal chain to produce
human-facing control card-package versions, then compare them with the exam,
diagnostic, and evidence layers.

This plan turns the near-term focus from adding more blocked downstream
scaffolds to producing concrete control package candidates that a human can
review, choose, and later turn into playable prototype work.

## Current Capability Baseline

The control pipeline can already:

- define a control discipline plus ideal temperament input contract;
- generate six report-only candidate package skeletons;
- rank those candidates with a deterministic advisory exam;
- explain the ranking through diagnostic notes;
- index source snippets and weak-evidence flags for auditability;
- preserve human-review, repair-plan, draft-request, and draft-submission
  scaffolds while the owner is unavailable.

The missing near-term value is not another blocked readiness step. The missing
value is a stronger human-facing production packet that shows several concrete
control-package versions, why they might be fun, how strong they may become,
and which one or two deserve playable prototyping.

## Trial Scope

The V1 production trial is control-only.

It should produce three to five report-only control package versions. Each
version should include:

- package id and one-sentence play promise;
- mechanism axis and ideal temperament source;
- intended player loop;
- card-role slots such as enabler, payoff, glue, defense, fail-state, and
  optional build-around;
- eight to twelve semi-formal card concept slots;
- combo map and anti-combo notes;
- fun evaluation;
- strength evaluation;
- expected strength curve across early, middle, and late run phases;
- complexity-budget notes;
- generic-goodstuff drift risk;
- second-career risk;
- evidence and review questions;
- recommended next action.

Semi-formal card concept slots may name a card-like idea, cost band, role, and
mechanical intent. They must not become official card text or runtime card
data.

## Candidate Lanes

The first production trial should cover these lanes, unless the owner supplies
a different control temperament packet:

- `white_order_fail_state`: reliable answer timing, fail-state recovery, and
  mistake containment.
- `blue_truth_forecast`: visible future information, delayed precision, and
  planned answer windows.
- `green_depth_compound_stability`: long-horizon control, compounding stability,
  and controlled recovery without becoming a second career.
- `resource_tempo_denial`: control through constrained enemy/player tempo,
  only if it stays readable and avoids hard-lock play.
- `hand_future_planning`: hand-shaping and future-turn planning, only if it
  creates decisions rather than generic value smoothing.

The first three lanes are the default preservation set from the current
candidate-batch exam. The last two are optional comparison probes.

## Suggested Workflow

### Step 1. Owner Input Packet

Write a compact owner-facing input packet for the production trial:

- target game feel for control;
- forbidden play patterns;
- desired run curve;
- desired difficulty and cognitive load;
- example cards or moments the owner likes;
- example cards or moments the owner dislikes;
- number of versions to produce;
- whether semi-formal concept slots are enough or whether the owner wants a
  separate external-draft request packet.

If the owner is unavailable, use the current control discipline plus ideal pilot
as provisional context and mark the packet as `awaiting_owner_review`.

### Step 2. Produce Package Versions

For each selected lane, write one report-only package version. The production
format should be human-readable first, machine-checkable second.

Each package should make the play promise visible before the details. It should
also name which parts are allowed preparation and which parts require human
approval before any later draft text or runtime implementation.

### Step 3. Compare Versions

Run or manually apply the existing report-only comparison vocabulary:

- candidate-batch exam dimensions;
- diagnostic failure probes;
- evidence snippet readiness;
- card package health dimensions where the package is complete enough;
- fun, strength, strength-curve, and complexity notes.

The comparison should recommend one or two packages for playable prototype
preparation, but it must not promote them.

### Step 4. Human-Facing Decision Packet

Prepare a final packet with:

- ranked package versions;
- keep, revise, reject, or merge suggestions;
- risks to inspect first;
- questions the owner can answer quickly;
- recommended first playable prototype target;
- cannot-advance list.

The packet should be useful even if the owner only has a short review window.

## Boundaries

The trial remains `report_only` and `advisory_context_only`.

It must not:

- write runtime card data;
- modify official card data;
- generate final official card text;
- promote or reject candidates as an authority;
- treat rankings as authoritative;
- claim reviewed evidence when the owner has not reviewed it;
- create hard gates;
- change existing scorecard weights;
- call an external LLM/API from repository tooling;
- enable default synthesis;
- enable learned or reranker behavior.

The trial may:

- produce human-readable concept slots;
- recommend review order;
- compare fun, strength, risk, and curve expectations;
- preserve an owner-unavailable scaffold;
- prepare a later complete-card draft request packet after owner review.

## Owner-Unavailable Mode

When the owner is unavailable:

- set the trial status to `awaiting_owner_review`;
- keep all owner decision fields empty or explicitly placeholder;
- keep `blocked_by_owner_review = true`;
- record allowed preparation such as formatting, comparison, and evidence
  indexing;
- record cannot-advance items such as official card text, runtime data, and
  playable prototype implementation;
- do not claim acceptance, review, or promotion.

This mode should still leave enough structure for automation to wait, compare,
and prepare the next packet without pretending the design has been approved.

## Stop Condition

The first trial is complete when the repository has a human-facing report-only
packet with:

- three to five control package versions;
- fun evaluation for every version;
- strength and strength-curve evaluation for every version;
- risk and evidence notes for every version;
- one or two recommended playable-prototype candidates;
- explicit blocked and cannot-advance sections.

After that, the next decision is whether to build a repair-plan generator for
the selected package versions or a complete-card draft request packet. The
preferred next step is the complete-card draft request packet if the owner has
chosen one or two package versions; otherwise continue with repair planning and
comparison.

