# Data Pipeline Guardrails V1

This document defines the repository data pipelines that should be protected by
automated tests.

## Goal

Not every CSV or JSON file in the repository is a formal production pipeline.
This document distinguishes between:

- runtime-source pipelines that need hard guardrails
- editor/import pipelines that need structure validation
- design-only specs that should not be treated as active source-of-truth chains

## Pipeline Levels

### Level A: Runtime Source Pipelines

These pipelines feed runtime content directly. They require hard pytest
guardrails.

#### Card Pipeline

- Editable source:
  - `data/cards/<color>/cards_*.csv`
  - `data/cards/<color>/effects_*.csv`
- Runtime artifact:
  - `data/cards/<color>/cards_generated.json`
- Current active packs:
  - `red`
  - `white`
  - `theorist`

Required guardrails:

- source CSV files must exist
- generated runtime JSON must exist
- CSV -> JSON regeneration must match committed runtime output
- effect-side card references such as `card_id_to_create` must resolve to known card IDs before runtime

#### TA Enemy Pipeline

- Editable source:
  - `data/combat/ta/species_ta.csv`
  - `data/combat/ta/skills_ta.csv`
  - `data/combat/ta/encounters_ta.csv`
- Runtime artifacts:
  - `data/combat/species.json`
  - `data/combat/skills.json`
  - `data/questlines/encounters_ta.json`

Required guardrails:

- TA CSV source files must exist
- TA runtime entries must all be traceable to CSV source rows
- regenerating TA payloads from CSV must match committed runtime JSON subsets
- species rows must reference valid skill IDs through `skills_json`, `opener`, and `weights_json`
- encounter rows must reference valid species IDs through `enemies_json` and task-host task/action payloads

### Level B: Editor / Import Pipelines

These pipelines are not the direct runtime source, but are still active content
entry paths. They need structure validation in pytest.

#### Slack Event Draft Pipeline

- Editable source:
  - `data/events_drafts/slack_moyu_draft.csv`
- Import/validation scripts:
  - `scripts/validate_events_draft.py`
  - `scripts/import_events_draft_to_events_src.py`

Required guardrails:

- each active draft CSV must validate successfully
- required text fields and effects DSL must parse

#### Gossip Draft Pipeline

- Editable source:
  - `data/events_drafts/gossip_draft.csv`
- Export/maintenance script:
  - `scripts/export_gossip_json_to_draft.py`

Required guardrails:

- draft CSV must exist
- required display fields must remain present
- row IDs and positive weights must remain valid
- boolean flags must stay parseable

#### Line Bubbles Draft Pipeline

- Editable source:
  - `data/flavor_drafts/line_bubbles/*.csv`
- Import/validation scripts:
  - `scripts/validate_line_bubbles_draft.py`
  - `scripts/import_line_bubbles_draft_to_src.py`

Required guardrails:

- draft CSV files must validate successfully
- IDs, required fields, phases, and weights must remain valid

### Level C: Design Specs

Design docs that mention CSV or JSON formats are not automatically part of the
runtime pipeline. They should not be tested as source-of-truth chains until
they become active implementation inputs.

Examples:

- enemy schema planning docs
- future paper/thesis CSV specs
- content planning sheets not wired into runtime or import scripts

## Current Test Entry

The current consolidated contract test lives in:

- `tests/scripts/test_data_pipeline_contracts.py`

It is responsible for keeping the active Level A and Level B pipelines under
automatic protection.

## Maintenance Rule

When a new content pipeline becomes active, update both:

1. this document
2. `tests/scripts/test_data_pipeline_contracts.py`

Do not add runtime-facing content pipelines without also adding a guardrail.
