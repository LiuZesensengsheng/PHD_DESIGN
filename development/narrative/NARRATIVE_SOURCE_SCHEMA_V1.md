# Narrative Source Schema V1

## Goal

This document is the concrete `Phase 2` contract for normalized narrative
source packs under:

```text
data/narrative_src/packs/<pack>/
```

It makes the V1 schema explicit enough that:

- humans know which file owns which concern
- AI can add content without inventing new ad hoc columns
- build tooling can be added later without redesigning the source model again

The reference implementation for this contract lives in:

- `scripts/narrative_src_io.py`

## Directory Contract

Each normalized narrative pack must contain exactly these files:

```text
manifest.json
nodes.csv
choices.csv
consequences.csv
conditions.csv
locales_zh_CN.csv
_draft_id_map.csv
```

## Manifest Contract

`manifest.json` owns pack-level metadata only.

Required keys:

- `schema_version`
- `pack_id`
- `display_name`
- `default_locale`
- `status`
- `entry_node_id`
- `runtime_questline_id`
- `runtime_questline_name`
- `runtime_outputs`
- `notes`

Current allowed `status` values:

- `phase2_schema_stub`
- `active_source`

`phase2_schema_stub` means:

- the schema is real and guarded
- the pack may still be only a skeleton
- runtime is still loading `data/questlines/*.json`

## CSV Ownership

### `nodes.csv`

Owns:

- stable node IDs
- node type
- title locale key
- description-page locale-key expansion data
- dialogue-line locale-key expansion data

Columns:

- `node_id`
- `node_type`
- `title_key`
- `description_key_prefix`
- `description_count`
- `line_key_prefix`
- `line_count`
- `choice_after_line`
- `note`

Current allowed `node_type` values:

- `EVENT`
- `DIALOGUE`

`description_key_prefix` and `description_count` rules:

- when `description_count > 0`, build expands:
  - `<prefix>.01`
  - `<prefix>.02`
  - ...

`line_key_prefix` and `line_count` rules:

- when `line_count > 0`, build expands:
  - `<prefix>.01.speaker`
  - `<prefix>.01.text`
  - `<prefix>.02.speaker`
  - `<prefix>.02.text`
  - ...

The schema intentionally allows both descriptions and lines on the same node.
This preserves existing tutorial runtime shape.

### `choices.csv`

Owns:

- stable choice IDs
- parent node relationship
- display order
- localized choice text keys
- localized result text keys

Columns:

- `choice_id`
- `node_id`
- `choice_order`
- `text_key`
- `result_text_key`
- `note`

### `consequences.csv`

Owns:

- ordered consequence rows per choice
- only explicit whitelisted gameplay consequence families

Columns:

- `consequence_id`
- `choice_id`
- `consequence_order`
- `consequence_type`
- `goto_node_id`
- `flag_key`
- `value_bool`
- `quest_var_key`
- `player_stat_key`
- `amount_int`
- `buff_id`
- `duration_int`
- `reward_id`
- `encounter_id`
- `note`

Current allowed `consequence_type` values:

- `GOTO_NODE`
- `SET_FLAG`
- `CLEAR_FLAG`
- `MODIFY_QUEST_VARS`
- `MODIFY_PLAYER_STATS`
- `ADD_PLAYER_BUFF`
- `SHOW_REWARD`
- `START_COMBAT`

No arbitrary callback hooks or Python references belong here.

### `conditions.csv`

Owns:

- explicit availability predicates for nodes or choices
- small finite condition families
- grouped conditions without free-form scripting

Columns:

- `condition_id`
- `owner_type`
- `owner_id`
- `condition_group`
- `condition_order`
- `condition_type`
- `subject_key`
- `operator`
- `value_text`
- `value_int`
- `value_bool`
- `note`

Current allowed `owner_type` values:

- `node`
- `choice`

V1 runtime build boundary:

- `choice` owners are the only runtime-compiled path in V1.
- `node` owner rows are reserved for later phases and must fail validation in
  active source packs until node-level gating is implemented.

Current allowed `condition_type` values:

- `FLAG_EQUALS`
- `QUEST_VAR_COMPARE`
- `PLAYER_STAT_COMPARE`
- `PACK_TAG_PRESENT`

Current allowed `operator` values:

- `EQ`
- `NE`
- `GT`
- `GTE`
- `LT`
- `LTE`

Grouping rule:

- rows with the same `owner_type`, `owner_id`, and `condition_group` are
  interpreted as `AND`
- different groups may later be interpreted as `OR`
- V1 keeps the condition language finite and tabular
- V1 runtime build currently supports exactly one `condition_group` per owner
  (single AND-group only).

Condition interpretation contract (V1):

- `FLAG_EQUALS`
  - subject: `subject_key` as flag id
  - value: `value_bool` is required
  - operator: `EQ` or `NE` (empty defaults to `EQ`)
  - runtime compile target: `{ "type": "HAS_FLAG", "flag": "<subject_key>", "value": <bool> }`
- `QUEST_VAR_COMPARE`
  - subject: `subject_key` as quest-var key
  - value: `value_int` is required
  - operator: one of `EQ/NE/GT/GTE/LT/LTE` (empty defaults to `EQ`)
  - runtime compile target:
    `{ "type": "QUEST_VAR_COMPARE", "var": "<subject_key>", "operator": "<OP>", "value": <int> }`
- `PLAYER_STAT_COMPARE`
  - subject: `subject_key` as player-stat key
  - value: `value_int` is required
  - operator: one of `EQ/NE/GT/GTE/LT/LTE` (empty defaults to `EQ`)
  - runtime compile target:
    `{ "type": "PLAYER_STAT_COMPARE", "stat": "<subject_key>", "operator": "<OP>", "value": <int> }`
- `PACK_TAG_PRESENT`
  - subject: `subject_key` as pack tag id
  - value: `value_bool` is optional; default is `true`
  - operator: `EQ` or `NE` (empty defaults to `EQ`)
  - runtime compile target: `{ "type": "HAS_PACK_TAG", "tag": "<subject_key>", "value": <bool> }`

Quest runtime evaluation sources:

- flags: narrative instance-local `flags`
- quest vars: narrative instance-local `vars`
- player stats: narrative instance-local `stats`
- pack tags: narrative instance-local `pack_tags`

### `locales_zh_CN.csv`

Owns:

- localized text payloads for the pack

Columns:

- `locale_key`
- `text`
- `note`

Rules:

- locale keys must be unique inside the pack
- localized text does not belong in `nodes.csv` or `choices.csv`

### `_draft_id_map.csv`

Owns:

- traceability back to legacy event IDs or planner draft rows during migration

Columns:

- `source_kind`
- `source_id`
- `legacy_event_id`
- `node_id`
- `choice_id`
- `source_file`
- `source_row`
- `note`

Despite the historical filename, this file may track both:

- planner draft IDs
- legacy migration references

The purpose is traceability, not runtime behavior.

ID stability rule:

- importer tooling should reuse existing `choice_id` / `condition_id` /
  `consequence_id` whenever semantic content is unchanged.
- reordering rows in draft input should not, by itself, force runtime ID churn.

## Boundary Rules

The normalized source layer may own:

- stable IDs
- locale keys
- explicit conditions
- explicit consequences
- migration trace metadata

The normalized source layer may not own:

- arbitrary Python code
- UI flow scripting
- runtime save mutation logic
- combat object mutation details
- hidden references to legacy repositories

## Tutorial Pack Status In Phase 2

The initial `tutorial` pack landing is intentionally a schema-first skeleton.

That means:

- the directory and files are now real and guarded
- manifest metadata points at the active tutorial runtime artifact
- the runtime tutorial content is not yet rebuilt from this pack

Actual tutorial content migration remains a later phase.
