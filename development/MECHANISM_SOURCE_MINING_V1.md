# Mechanism Source Mining V1

## Purpose

Collect external game mechanics as abstract mechanism-axis candidates for
`mechanism_axis_discovery_v1`.

The goal is not to build a lore or rules encyclopedia. The goal is to turn useful
mechanic patterns into comparable discovery candidates:

- mechanism fantasy
- player choice
- foundation/base-axis dependencies
- parameter response targets
- fail-state value
- package potential
- identity override risk

## Collection Rule

Translate source mechanics into abstract axes instead of copying named mechanics.

Examples:

- Monster Train floor capacity becomes `floor_capacity_lineup`.
- Dicey Dungeons dice/equipment slots become `dice_slot_allocation`.
- Balatro jokers become `joker_rule_rewrite`.
- Hearthstone Discover becomes `discover_option_selection`.
- Dominion trashing becomes `removal_thinning_conversion`.

## Source Families

The first seed pack covers:

- lane/floor construction: Monster Train
- countdown and status timing: Wildfrost
- dice/value allocation: Dicey Dungeons
- hand-shape and rule modifiers: Balatro
- stack/reaction and graveyard reuse: Magic: The Gathering
- generated choice and hidden reaction: Hearthstone
- material ladder and chain response: Yu-Gi-Oh!
- action economy and deck thinning: Dominion
- sacrifice and ability transfer: Inscryption
- position redirection: Into the Breach
- inventory adjacency: Backpack Hero

## Current Fixture Pack

`tests/fixtures/combat_analysis/mechanism_axis_discovery_v1/mechanism_axis_source_mining_pack1_v1.json`

Current size:

- `20` cross-game candidates
- `1` intentional generic draw/energy negative case

## Review Rules

- Keep source refs in `evidence_refs`.
- Do not treat source-mining candidates as reviewed viability evidence.
- Do not promote a source-mining candidate into a mechanism family without adding
  reviewed contrasts.
- Do not make project-temperament claims in source mining. That belongs to a later
  temperament-fit layer.
- Keep generic draw/energy/discard/compression power separate from named mechanism
  identity unless the base axis is explicitly the mechanism, such as
  `discard_velocity` or `removal_thinning_conversion`.

## First-Pass Validation

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_mechanism_axis_discovery_v1.py tests/scripts/test_run_mechanism_axis_discovery.py -q
```

Optional local artifact check:

```powershell
python scripts/run_mechanism_axis_discovery.py --input tests/fixtures/combat_analysis/mechanism_axis_discovery_v1 --output-dir tmp/combat_analysis/mechanism_axis_discovery_source_mining_check
```
