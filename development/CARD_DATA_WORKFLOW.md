# Card Data Workflow

This document defines the current card-data source-of-truth rules for the project.

## Source Of Truth

For active card packs, editable source lives in per-pack CSV files:

- `data/cards/<color>/cards_*.csv`
- `data/cards/<color>/effects_*.csv`

Runtime reads only:

- `data/cards/<color>/cards_generated.json`

Legacy scattered JSON files under `data/cards/<color>/*.json` are not card-text source of truth.
They may still exist for bootstrap, migration checks, or historical reference, but they must not be used to restore current card names or descriptions.

## Current Active Packs

The active packs covered by the current pipeline health checks are:

- `red`
- `white`
- `theorist`

## Editing Workflow

When changing card content:

1. Edit the pack CSV source:
   - `cards_*.csv` for card metadata and display text
   - `effects_*.csv` for effect rows
2. Regenerate runtime JSON:
   - `python scripts/cards_csv_to_json.py --generate-all-colors`
   - or target a single pack with:
     - `python scripts/cards_csv_to_json.py --cards-csv data/cards/<color>/cards_<color>.csv --effects-csv data/cards/<color>/effects_<color>.csv --output-json data/cards/<color>/cards_generated.json`
3. Run validation tests:
   - `python -m pytest tests/scripts/test_cards_csv_to_json.py -q`
   - plus relevant card-pack runtime tests if you changed active cards

## Validation Rules

The generator now fails before runtime when source data is malformed.

Current checks include:

- duplicate `card_id`
- missing `name_key` or `description_key`
- suspicious placeholder text in display fields
- invalid `type`
- invalid `rarity`
- invalid card/effect `target`
- invalid `tags_json`
- invalid `params_json`
- effect rows pointing to unknown cards
- duplicate effect `seq` within the same card

Blank placeholder rows are ignored only when `card_id` is empty.
Once a row has a real `card_id`, it must satisfy the validation rules.

## Recovery Rules

If card text looks garbled in runtime:

1. Check the active CSV source first
2. Check `cards_generated.json` second
3. Only inspect rendering/runtime display code after source data is ruled out

Do not treat legacy bootstrap JSON files as trusted recovery sources for text.

## Notes

- `scripts/manage.py` still contains older card-management commands tied to the retired `cards_master.csv` workflow. Do not use that file as the source of truth for current card editing rules.
- The current reliable pipeline is `CSV source -> generated JSON -> runtime`.
