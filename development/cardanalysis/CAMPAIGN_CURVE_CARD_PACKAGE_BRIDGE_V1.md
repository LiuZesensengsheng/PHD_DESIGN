# Campaign Curve Card Package Bridge V1

## Purpose

`campaign_curve_card_package_bridge_v1` is a minimum report-only contract draft for
connecting STS1 campaign curve learning to future card-package exams.

It exists to help answer:

```text
Does this package become useful at the right campaign time, with the right resource
assumptions, against normal, elite, and boss pressure?
```

It does not design cards or change runtime campaign behavior.

## Authority Boundary

This bridge is advisory context only.

It must not:

- create hard gates,
- modify campaign runtime,
- write runtime card data,
- promote formal cards,
- claim reviewed STS1 evidence,
- claim a complete STS1 ontology,
- enable default synthesis, learned behavior, or reranker behavior.

The bridge consumes STS1 campaign curve language as source-mined/design-reference
context and keeps it separate from Darkest Dungeon stress, virtue, and affliction
models.

## Problem

Current card-package evaluation can describe axis alignment, package density, slot
fit, bridge-before-payoff sequencing, and package-health labels. That is necessary
but not sufficient for a roguelike deckbuilder campaign.

A package may be coherent in a static handoff and still fail because:

- it does nothing before Act 2 pressure arrives,
- it cannot take Act 1 elites,
- it assumes too many upgrades, removals, shops, or relics,
- it beats one boss texture but folds to another,
- it has a high late ceiling that flattens encounter texture once online.

The missing layer is a small bridge from package health into campaign timing.

## Constraints

- Keep the first version document-only and report-only.
- Reuse existing cardanalysis vocabulary where possible.
- Do not add runtime campaign code.
- Do not add hard gates.
- Do not add a new scoring authority over `card_package_health_v1`,
  `deck_compression_report_v1`, `mechanism_fun_health_v1`, or
  `campaign_power_curve_report_v1`.
- Keep STS1 source-mined material below reviewed-evidence authority.
- Keep DD1 stress/resolve concepts out of this bridge.

## Complexity

Essential complexity:

- Campaign fitness is temporal. The same card package can be too slow in Act 1,
  useful in Act 2, and too narrow in Act 3.
- Encounter tiers ask different questions. Normal fights test consistency and HP
  leakage, elites test route-risk conversion, bosses test reorientation.
- Growth resources are not fungible. A removal, upgrade, relic, shop purchase, card
  reward, and potion each solve different campaign problems.
- Character lanes differ. Silent, Ironclad, Defect, and Watcher have different
  starter pressure, setup tolerance, and ceiling risks.

Accidental complexity to avoid:

- inventing a full STS1 route simulator,
- treating source-mined examples as reviewed evidence,
- duplicating the existing package-health evaluator,
- turning campaign advice into a hard pass/fail layer.

## Options

### Option A: Add A Narrow Bridge Contract

Add this document as the minimum shape for future report-only integration. Keep all
fields advisory and map them to existing package-health, compression, fun/health, and
campaign-power vocabulary.

Upside:

- improves package exam interpretation without implementation churn,
- preserves boundaries,
- creates stable wording for future fixtures or snapshots.

Downside:

- does not automatically catch failures until a later implementation consumes it.

### Option B: Fold Campaign Timing Into Card Package Health

Add online timing and act-pressure language directly to `card_package_health_v1`.

Upside:

- fewer named artifacts.

Downside:

- blurs package coherence with campaign reachability,
- risks making package health too broad,
- makes later route/resource dimensions harder to isolate.

### Option C: Wait For Full Campaign Simulation

Do nothing until a route or encounter simulator exists.

Upside:

- avoids speculative structure.

Downside:

- loses the immediate lesson from STS1 that package fitness depends on online timing,
- lets future package exams keep overvaluing final-shell coherence.

## Risks

- The bridge could grow into a second package-health evaluator.
- Agents could treat source-mined STS1 examples as reviewed evidence.
- The vocabulary could become a hidden hard gate if later reports expose pass/fail
  language.
- The bridge could overfit STS1 and become hostile to this project's own campaign
  identity.

Mitigations:

- keep `evaluation_mode=report_only`,
- require `authority_boundary=advisory_context_only`,
- store source status on the payload,
- report reason codes and risks instead of pass/fail,
- map each dimension to an existing owner where possible.

## Recommendation

Use Option A: a narrow bridge contract.

The bridge should be a future optional input or derived advisory section for
`card_package_exam_v1`. It should not replace package health. It should translate
package-health output into campaign questions:

- Does the package help early enough?
- Which act exposes the first risk?
- Which encounter tier breaks it?
- Which growth resource is over-assumed?
- Does the character lane make the timing better or worse?

## Counter-Review

The recommendation is useful only if later agents keep it small. If the bridge starts
adding encounter stats, route probabilities, final grades, or card-design commands,
it should be stopped and split back into report-only notes.

The bridge also should not force every package to be Act 1-ready. Some packages are
valid late packages. The required discipline is to label them honestly as late,
route-dependent, or support-dependent, not to reject them.

## Decision Summary

Create `campaign_curve_card_package_bridge_v1` as a document-only, report-only
minimum contract draft.

It is worth doing now because the current STS1 exam loop already evaluates complete
packages, but it needs a shared vocabulary for campaign timing risk before future
autonomous draft attempts begin optimizing only for package coherence.

## Minimum Payload Draft

Future implementation can use a compact payload shaped like this:

```json
{
  "campaign_curve_card_package_bridge": {
    "contract_version": "campaign_curve_card_package_bridge_v1",
    "evaluation_mode": "report_only",
    "authority_boundary": "advisory_context_only",
    "source_status": "source_mined_design_reference",
    "source_confidence": "not_reviewed_evidence",
    "target_context": {
      "reference_game": "sts1",
      "character": "silent",
      "primary_axis": "poison",
      "secondary_axes": ["retain", "shiv"]
    },
    "online_timing": {
      "early_available": "partial",
      "midgame_forming": "credible",
      "late_ceiling": "strong_if_supported",
      "first_functional_window": "act1_late",
      "notes": ["needs_act1_damage_patch_before_poison_payoff"]
    },
    "encounter_tier_readiness": {
      "normal_combat": {
        "label": "watch",
        "reason_codes": ["early_cards_must_not_be_blanks"]
      },
      "elite": {
        "label": "watch",
        "reason_codes": ["act1_elite_frontload_gap"]
      },
      "boss": {
        "label": "credible",
        "reason_codes": ["late_scaling_and_control_visible"]
      }
    },
    "growth_resource_assumptions": {
      "cards": ["needs_bridge_before_payoff"],
      "relics": ["no_specific_relic_assumed"],
      "upgrades": ["one_key_upgrade_watch"],
      "removal": ["starter_pollution_visible"],
      "gold_and_shop": ["shop_not_required_for_function"],
      "potions": ["potion_can_bridge_elite_once_not_repeatably"]
    },
    "recovery_window_read": {
      "rest_vs_smith_tension": "medium",
      "shop_dependency": "low",
      "elite_path_dependency": "medium",
      "potion_dependency": "low"
    },
    "curve_risk_flags": [
      "act1_elite_check_failure",
      "payoff_before_survival_bridge"
    ],
    "exam_integration": {
      "card_package_exam_use": "advisory_risk_section_only",
      "hard_gate_impact": "none",
      "recommended_human_review_questions": [
        "What does this package do before its payoff appears?",
        "Which act first punishes the package?",
        "Which growth resource is being assumed?"
      ]
    }
  }
}
```

## Risk Type Taxonomy

These risk types are report-only reason codes.

| Risk Type | Meaning | Typical Review Question |
| --- | --- | --- |
| `too_slow` | The package pays setup tax before it contributes enough damage, block, draw, or control. | What does the package do in the first few fights? |
| `too_narrow` | The package answers one pressure family while hiding weakness to other act or boss questions. | Which elite or boss texture invalidates the plan? |
| `frontload_too_high` | The package over-solves early damage while failing to build scaling, defense, or late texture. | Does early output convert into a real Act 2/3 plan? |
| `late_scaling_runaway` | The package's mature state becomes a low-choice script that flattens encounter texture. | Are action, power, boss, and matchup constraints still meaningful? |
| `recovery_window_collapse` | The package turns rest, shop, potion, or route choices into mandatory rescue steps. | Can the run still choose between heal, upgrade, shop, and elite routes? |
| `elite_check_failure` | The package cannot justify elite risk at the point when relic acceleration matters. | Which act elite exposes the first failure? |
| `act1_elite_check_failure` | The package lacks early damage, block, or status tolerance for Gremlin Nob, Lagavulin, or Sentries-style checks. | Can it take an Act 1 elite without perfect potion support? |
| `act2_transition_shock` | The package survives Act 1 but lacks AoE, defense, scaling bridge, or add control for Act 2. | What changed when the second act started? |
| `boss_reorientation_failure` | The package cannot adapt to a boss phase, add wave, action limit, power punish, or scaling race. | What is the alternative line when the boss attacks the primary plan? |
| `payoff_before_survival_bridge` | The package selects payoff before bridge, stabilizer, or density slots are credible. | Which support card should arrive before the finisher? |
| `resource_plan_fantasy` | The package assumes too many upgrades, removals, shops, relics, or potions. | Which assumed resource is least guaranteed? |
| `compression_route_overclaim` | A thin final shell is treated as generally reachable without removal or effective-compression evidence. | How does the starter deck become this clean? |
| `potion_crutch` | Potion use is counted as repeatable package function rather than a one-fight bridge. | Does the same package still function after the potion is spent? |
| `upgrade_dependency_spike` | The package needs key upgrades before it can function and therefore competes with healing. | Can it afford to smith instead of rest? |
| `multi_enemy_blindness` | The package handles single-target fights while ignoring add waves or spread pressure. | What happens when the encounter asks for target priority or AoE? |
| `status_or_disruption_fragility` | The package collapses when statuses, burns, draw disruption, artifact, or debuffs disturb the line. | Does the package have filtering, redundancy, or fail-state value? |
| `character_curve_mismatch` | The package asks a character to solve the wrong timing problem for that lane. | Does this fit Silent, Ironclad, Defect, or Watcher starter pressure? |

## Evaluation Dimensions For Card Package Exams

Future `card_package_exam_v1` integration can add these advisory dimensions without
changing pass/fail authority.

| Dimension | Reads From Existing Surfaces | Report-Only Question |
| --- | --- | --- |
| `early_functionality` | package density, slot fit, payoff timing | Does the package do useful work before the engine is complete? |
| `act1_elite_readiness` | frontload, starter pollution, potion notes | Can the package justify early elite risk without perfect draws? |
| `act2_transition_buffer` | survival patch, AoE/add handling, scaling bridge | Does the package survive the Act 2 pressure jump while forming? |
| `act3_constraint_flex` | fun/health matchup elasticity, degeneracy pressure | Does the mature package remain flexible under specialized constraints? |
| `normal_fight_hp_leak` | fail state, setup tax, early output | Does ordinary combat tax too much HP before rewards compound? |
| `elite_conversion_plan` | elite risk flags, relic assumptions, potion use | Does elite risk convert into relic acceleration or just consume recovery? |
| `boss_reorientation` | payoff texture, alternate line, phase handling | What does the package do when a boss attacks its preferred plan? |
| `growth_resource_budget` | removal, upgrades, gold, relics, potions | Which resource assumptions are required before the package works? |
| `online_timing_truthfulness` | bridge-before-payoff, first functional turn | Is the package labeled early, mid, or late honestly? |
| `recovery_window_cost` | rest/smith, shop, route, potion dependency | Does the package preserve recovery choices? |
| `compression_burden` | deck compression and removal model | Does the package overclaim reachability from a clean final shell? |
| `character_curve_fit` | STS1 exam target character lane | Does the package match that character's starter pressure and ceiling risk? |
| `partial_solve_value` | fail state, normal combat usefulness | Are incomplete package pieces still valuable? |
| `anti_runaway_texture` | mechanism fun/health degeneracy pressure | Does late scaling leave meaningful encounter texture? |

## Relationship To Existing Cardanalysis Surfaces

`card_package_health_v1` remains the owner of package coherence:

- density,
- slot fit,
- closure fit,
- motif fit,
- payoff timing,
- soup suppression,
- starter pollution and compression interaction,
- bridge-before-payoff.

`deck_compression_and_removal_model_v1` remains the owner of reachability and
starter-pollution honesty.

`mechanism_fun_health_v1` remains the owner of agency, setup tax, fail state,
variance pressure, combo aspiration, degeneracy pressure, and matchup elasticity.

`campaign_power_curve_report_v1` remains the project campaign pacing surface. This
bridge should not redefine that surface or tune encounter implementation.

`card_package_exam_v1` can eventually consume this bridge as a summary appendix or
prompt/handoff risk section. It must not expose `overall_pass`, `overall_fail`, or
hard-gate language from this bridge.

## Minimum Integration Advice

When a future package exam includes this bridge, the report should include:

1. a one-line online timing label,
2. the first act window that exposes risk,
3. one normal-combat read,
4. one elite read,
5. one boss reorientation read,
6. the most expensive growth-resource assumption,
7. at most three curve risk flags,
8. human-review questions instead of final verdicts.

The bridge should prefer concise, inspectable risk language over a numeric score.

