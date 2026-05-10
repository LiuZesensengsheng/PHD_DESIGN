# Campaign Curve Profile V1

## Purpose

`campaign_curve_profile_v1` is a report-only content contract for planning
campaign rhythm before it reaches runtime campaign implementation.

It captures:

- phase-by-phase combat, event, shop, rest, elite/hard-fight, treasure, and boss
  proportions;
- event intent mix, such as recovery, choice, risk, narrative, and build support;
- pressure axes, such as frontload, defense, multi-enemy, status, scaling, resource
  tax, recovery pressure, and anti-runaway pressure;
- expected package online timing for future `card_package_exam` interpretation.

The contract is intentionally small. It is content planning, not a route simulator.

## Authority Boundary

All V1 profiles use:

- `evaluation_mode = report_only`
- `authority_boundary = advisory_context_only`

Profiles must not:

- change runtime campaign,
- create encounter rosters or monster stats,
- write runtime card data,
- promote cards,
- create hard gates,
- claim reviewed STS1 evidence,
- enable default synthesis, learned behavior, or reranker behavior.

The current profile fixtures are STS1-inspired source-mined/design-reference
planning material. They are not copied STS1 map-generation rules.

## Relationship To Existing Surfaces

`campaign_power_curve_report_v1` remains the campaign pacing report owner.

`campaign_curve_profile_v1` is the content profile that a later report can read.
It should feed:

- `campaign_power_curve_report_v1` as pacing context,
- `campaign_curve_card_package_bridge_v1` as card-package timing context,
- future `card_package_exam_v1` advisory sections.

It should not replace:

- `card_package_health_v1`,
- `deck_compression_report_v1`,
- `mechanism_fun_health_v1`,
- `campaign_power_curve_report_v1`.

## Phase Model

V1 uses the existing project phase bands:

| Phase | Round Hint | Campaign Role |
| --- | --- | --- |
| `starter` | `0-2` | Let the player repair the starter deck and learn the run texture. |
| `early` | `3-5` | Introduce route risk and the first stronger combat checks. |
| `build` | `6-8` | Let packages form while asking for survival and role coverage. |
| `pivot` | `9-11` | Ask the player to reorient around a boss, route, or disruptive pressure. |
| `mature` | `12-14` | Check ceiling, scaling, recovery cost, and package flexibility. |
| `late` | `15+` | Keep mature builds textured without turning anti-runaway pressure into a hard gate. |

## Rhythm Fields

Each phase contains a `room_mix` over:

- `normal_combat`
- `event`
- `shop`
- `rest`
- `elite_or_hard_fight`
- `treasure`
- `boss`

The values are ratios and must sum to `1.0` per phase.

Each phase also contains an `event_intent_mix` over:

- `recovery`
- `choice`
- `risk`
- `narrative`
- `build_support`

These values are not room-generation probabilities. They describe what kind of
event texture the curve should prefer when an event slot appears.

## Base Curve

The base profile is intentionally low pressure:

- generous event and recovery space;
- low early elite/hard-fight ratio;
- boss and pivot checks present but not punitive;
- anti-runaway pressure only appears late as advisory texture.

Use it when testing whether a mechanism can enter a friendly campaign environment
without being immediately punished.

## Advanced Curve

The advanced profile is tighter but still not a stat spike:

- fewer recovery windows;
- more hard-fight and boss pressure;
- more status/disruption and resource-tax pressure;
- more explicit boss reorientation and anti-runaway texture;
- events shift from recovery/narrative toward risk/choice.

Use it when testing whether a package that passes base pacing can survive tighter
route and recovery discipline.

## Current Fixtures

Current fixtures live in:

```text
tests/fixtures/combat_analysis/campaign_curve_profile_v1/
```

They include:

- `project_base_campaign_curve_v1.json`
- `project_advanced_campaign_curve_v1.json`

## Entrypoints

Write a template:

```powershell
python scripts/validate_campaign_curve_profile.py --write-template tmp/combat_analysis/campaign_curve_profile_template.json
```

Validate the current profiles:

```powershell
python scripts/validate_campaign_curve_profile.py --input tests/fixtures/combat_analysis/campaign_curve_profile_v1
```

Write a single-profile rhythm report:

```powershell
python scripts/validate_campaign_curve_profile.py --input tests/fixtures/combat_analysis/campaign_curve_profile_v1/project_base_campaign_curve_v1.json --write-report tmp/combat_analysis/base_campaign_curve_profile_report.md
```

Focused tests:

```powershell
py -3.11 -m pytest tests/toolkit/combat_analysis/test_campaign_curve_profile_v1.py tests/scripts/test_validate_campaign_curve_profile.py -q
```

## Stop Lines

Pause for human review before any follow-up:

- modifies runtime campaign,
- converts profile ratios into hard route generation,
- creates formal card data,
- claims reviewed STS1 evidence,
- turns profile validation into card-package pass/fail authority,
- connects learned/reranker behavior by default.
