# Design Complexity Evaluation V1

## Purpose

`design_complexity_evaluation_v1` is a report-only metric tree for reviewing
whether a card, package, trait, ideal reward exchange, or small system proposal
is spending too much complexity.

The tool is intentionally conservative about the combat loop:

```text
draw cards -> spend energy -> play cards -> read enemy intent -> choose rewards
```

V1 does not decide legality, power level, card text, or runtime implementation.
It only reports where complexity is being spent and whether that spending is
compatible with the current STS-like core loop.

## Boundary

The output always keeps:

- `schema_version = design_complexity_evaluation_v1`
- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`
- `hard_gate_impact = none`

V1 does not:

- modify runtime cards or traits;
- modify `case_input_contract.py`;
- modify evaluator heads;
- modify capability graph or report-only registry ownership;
- change hard gates, default synthesis, learned, or reranker paths.

## Metric Tree

The V1 tree has six nodes.

### `read_complexity`

Question:

```text
Can the player understand the main effect in one or two seconds?
```

Budget rule:

- one primary mechanism axis;
- at most one secondary mechanism axis;
- no more than two preconditions before the main effect is legible.

### `turn_execution_complexity`

Question:

```text
Does this make each combat turn harder to execute?
```

Budget rule:

- avoid recurring new per-turn decisions;
- avoid hidden state;
- avoid multiple delayed triggers on one card.

This is the most important guardrail. Complexity can live in build, trait,
ideal reward, and review layers more safely than inside every combat turn.

### `build_complexity`

Question:

```text
How much deckbuilding or reward-path burden does this add?
```

Budget rule:

- package complexity is acceptable when it has clear enabler, payoff, glue, and
  fail-state value;
- incomplete packages should declare missing roles rather than pretending to be
  production-ready.

### `state_tracking_complexity`

Question:

```text
Does this require extra memory, hidden state, or UI tracking?
```

Budget rule:

- prefer visible cards, traits, rewards, and existing combat state;
- hidden counters and off-screen memory should be treated as review risks.

### `production_complexity`

Question:

```text
How much authoring, tuning, and review surface does this create?
```

Budget rule:

- keep authoring slices small enough for focused tests and review;
- do not turn one idea into a many-surface production commitment too early.

### `fun_health_counterweight`

Question:

```text
Does the added complexity buy agency, payoff texture, fail-state value, or matchup elasticity?
```

This is a positive counterweight, not a bypass. Strong fun-health texture can
justify a watch-level idea, but it should not excuse overloaded per-turn combat.

## Status Labels

`complexity_budget_status` values:

- `within_budget`: small enough to continue as advisory design context;
- `watch`: readable, but needs review before production;
- `over_budget`: should be split or moved out of per-turn combat before
  production.

The status is advisory. It is not a hard gate.

## Supported Inputs

The CLI accepts:

- a `design_complexity_evaluation_input_v1` JSON file;
- a single design-unit JSON object;
- a JSON array of design-unit objects;
- a `card_package_proposal_v1` JSON file;
- a directory containing any of the above JSON files.

Card package proposals are converted into package design units so existing
package drafts can be checked without inventing another contract.

## Entrypoints

```bash
python scripts/run_design_complexity_evaluation.py --write-template <path>
python scripts/run_design_complexity_evaluation.py --input <design-unit-or-card-package-json-or-dir> --output-dir <dir>
py -3.11 -m pytest tests/toolkit/combat_analysis/test_design_complexity_evaluation_v1.py tests/scripts/test_run_design_complexity_evaluation.py -q
```

## Design Intent

The core product rule is simple:

```text
Do not make every combat turn more complicated just to express ideal/personality depth.
```

Ideal tension, research identity, traits, card packages, and campaign reward
exchanges can carry philosophical and strategic weight. The player should not
pay that cost by having to parse overloaded single-card text or hidden state on
every turn.
