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
- generated `encounters_ta.json` must also satisfy the runtime encounter contract against active combat bundles

#### Questline / Encounter Runtime Contract

- Runtime source:
  - `data/questlines/encounters_*.json`
  - `data/questlines/questline_*.json`
- Runtime dependency bundles:
  - `data/combat/species.json`
  - `data/combat/traits.json`
  - `data/combat/skills.json`
  - `data/combat/arenas.json`
  - `data/combat/arena_traits.json`

Required guardrails:

- runtime encounter enemies must reference known species, traits, and positive levels
- runtime encounter arena definitions must reference known arena templates and arena traits
- runtime encounter species must only pull skills that resolve from `skills.json`
- runtime `chore_host` definitions must satisfy roster/reference rules, and active runtime content must use chore-only payloads
- questline `START_COMBAT.encounter_id` must resolve to an encounter loaded from active `encounters_*.json`

### Level B: Editor / Import Pipelines

These pipelines are not the direct runtime source, but are still active content
entry paths. They need structure validation in pytest.

#### Content Pack Identity

- Active source-pack manifests:
  - `data/narrative_src/packs/tutorial/manifest.json`
  - `data/events_src/packs/slack/manifest.json`
- Shared validator:
  - `scripts/content_pack_manifest.py`

Required guardrails:

- each active source pack must have a `manifest.json`
- pack ids must match their directory names
- versions, dependency lists, and deprecation flags must satisfy the minimal V1
  manifest contract
- dependency validation is shape-only in V1; no runtime dependency solver is
  implied

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

#### Narrative Source Schema Pilot

- Draft input:
  - `data/narrative_drafts/tutorial/questline_tutorial.draft.json`
- Draft validation/import scripts:
  - `scripts/validate_narrative_draft.py`
  - `scripts/import_narrative_draft_to_src.py`
- Normalized source:
  - `data/narrative_src/packs/tutorial/*`
- Source schema IO / validation module:
  - `scripts/narrative_src_io.py`
- Source -> runtime build script:
  - `scripts/build_narrative_runtime.py`

Required guardrails:

- draft format must validate
- required pack files must exist
- manifest shape must stay stable
- CSV headers must stay stable
- basic node / choice / consequence / condition reference rules must stay valid
- reading and rewriting the pack through the schema IO module must be deterministic
- source -> runtime build payload must stay in parity with
  `data/questlines/questline_tutorial.json`

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
