# Card Package Health Evaluation V1

## Purpose

Define the minimum V1 review language for judging whether a card package is healthy
as a package.

This document is a specification only. It does not change code, fixtures, schemas,
thresholds, gates, or default entrypoints.

The package health question is narrow:

- Does the package have enough density, role fit, sequencing, and evidence-backed
  anchoring to read as a coherent package instead of goodstuff or soup?

It is not the same question as:

- whether a mechanism is online,
- whether the play pattern is fun,
- whether a compact combo is reachable from a starter deck,
- whether a learned reranker should prefer it.

## Scope Boundary

In scope:

- Reviewed `STS1` package-health language for cardanalysis.
- `package_density`, `slot_fit`, `closure_fit`, `motif_fit`, `payoff_timing`, and
  anti-soup interpretation.
- Starter pollution and compression assumptions when they affect package health.
- Bridge-before-payoff sequencing.
- Primary and secondary anchor uncertainty.
- Boundaries with mechanism viability, fun/health, and deck compression specs.

Out of scope:

- changing legality, schema, gate, or threshold behavior
- changing package similarity benchmark gates
- adding fixtures
- changing `DEFAULT_ENTRYPOINTS.md`
- enabling learned/reranker paths by default
- treating `STS2` examples as the same trust tier as reviewed `STS1`

## Existing Evidence Surface

V1 should be built from existing surfaces rather than inventing a new system:

- `PACKAGE_SIMILARITY_BENCHMARK_V0.md`
  - family hit, slot fit, closure fit, motif fit, and artifact completeness
- `DECK_SKELETON_SIDECAR_V1.md`
  - current shell, primary anchor, secondary anchor, missing slots, priority actions,
    suggested packages, avoid-now boundaries, confidence, open questions
- `DECK_SKELETON_EVIDENCE_BRIDGE_V1.md`
  - anchor evidence, package evidence, priority evidence, draft closure evidence,
    projection gaps, uncertainty sources
- `MECHANISM_FUN_HEALTH_EVALUATION_V1.md`
  - player-facing health dimensions after a mechanism is online
- `DECK_COMPRESSION_AND_REMOVAL_MODEL_V1.md`
  - starter pollution, route dependency, and compression reachability assumptions

V1 package health should therefore be a small interpretation layer over existing
signals, not a new benchmark authority.

## Review Sequence

Use this order when reviewing a package:

1. Mechanism viability asks whether the mechanism shell can come online.
2. Package health asks whether the card package is coherent, well-slotted, sequenced,
   and not just soup.
3. Fun/health asks whether the online package creates good play.
4. Deck compression/removal asks whether the package is reachable from a realistic
   deck state or only from a curated compact shell.

Package health can report risk at any step, but it should not overwrite the owning
layer's decision.

## V1 Output Labels

These labels are review language, not hard gates:

| Label | Meaning |
| --- | --- |
| `healthy_package` | The package has coherent density, slot fit, sequencing, and anchor evidence. |
| `watch_package` | The package is coherent but has a visible density, slot, timing, or uncertainty risk. |
| `fragile_package` | The package depends on thin margins, unresolved starter pollution, or payoff-before-bridge sequencing. |
| `soup_risk` | The package reads more like goodstuff, hybrid soup, or adjacent-family blur than a package. |
| `not_evaluated` | Evidence is insufficient or outside the reviewed V1 trust tier. |

## Dimensions

### `package_density`

Definition:

Whether the package has enough on-axis cards and repeated role support to hold its
identity through ordinary draws.

Healthy signals:

- Core cards, bridge cards, payoff cards, and support cards reinforce the same
  package.
- The package has enough density that one missed draw does not erase identity.
- Local density and cross-density point in the same direction.
- Off-axis cards are either temporary support, explicit pivots, or marked as pollution.

Risk signals:

- One payoff card is doing most of the identity work.
- Support is broad but shallow, so the package reads as generic value.
- Local density is low and the package depends on a few perfect draws.
- Starter or off-plan cards occupy enough draw slots to dilute package contact.

Boundary:

`package_density` is not the same as mechanism `support_density`. A package can have
enough support to turn on one mechanism but still be too thin as a reusable draft or
deck skeleton package.

### `slot_fit`

Definition:

Whether the package's cards occupy the right structural jobs and whether missing jobs
remain visible.

Use the existing deck skeleton slot language:

- `bridge`
- `stabilizer`
- `payoff`
- `density`
- `conversion`
- `survival_patch`
- `pivot_option`

Healthy signals:

- Bridge and stabilizer work are represented before payoff greed.
- Payoff cards have enough setup and support to be live.
- Missing slots stay visible instead of being hidden by a high-level package label.
- Suggested packages map to the right missing slot.

Risk signals:

- The package has multiple payoffs but no bridge.
- Stabilizers are absent and survival_patch is treated as someone else's problem.
- Pivot cards are mistaken for primary package density.
- The evaluator hides a missing slot because a nearby good card has the same broad
  package tag.

Boundary:

`slot_fit` is a package-health read. It does not decide card legality, schema validity,
or benchmark pass/fail gates.

### `closure_fit`

Definition:

Whether a package can close an actual reviewed sequence rather than only looking
coherent in a static snapshot.

Healthy signals:

- A draft or evidence trace shows closed-loop health improving.
- The trace reduces structural gaps.
- The package's priority actions are supported by pick-like evidence.
- Bridge arrives before payoff when the package requires staged assembly.

Risk signals:

- Closure is inferred only from card names or broad tags.
- A package improves a score while leaving the same open questions unresolved.
- The package asks for a payoff upgrade before its bridge, stabilizer, or density
  slots are credible.
- Closure evidence is absent but the report still sounds certain.

Boundary:

`closure_fit` can reuse the existing package similarity closure indicator. This spec
does not change `closure_fit_rate` or its benchmark threshold.

### `motif_fit`

Definition:

Whether the package preserves the expected fun/risk motifs and projection gaps that
make its health interpretation inspectable.

Use the existing motif vocabulary as evidence:

- positive examples:
  `anchor_alignment_visible`, `primary_shell_readable`,
  `payoff_upgrade_staged`, `shell_thickening_before_payoff`,
  `pivot_option_visible`, `draft_closure_improved`, `bridge_before_payoff`
- risk examples:
  `survival_patch_needed`, `stabilizer_needed`, `projection_gap_retained`,
  `secondary_anchor_uncertainty`, `pivot_boundary_visible`,
  `greed_boundary_visible`, `high_energy_strain_visible`,
  `identity_low_confidence`

Healthy signals:

- The package's positive motifs are visible and tied to evidence.
- Risk motifs are preserved when the evidence is thin.
- Projection gaps remain explicit in reports and snapshots.

Risk signals:

- The package loses its motif identity and becomes generic synergy language.
- Known risks disappear from the report after aggregation.
- A low-confidence package is described with high-confidence language.

Boundary:

`motif_fit` is not a precise fun score. It is evidence that the package health read
kept the right reasons visible.

### `payoff_timing`

Definition:

Whether payoff cards enter after the package can support them, and whether their
release window is useful rather than stranded.

Healthy signals:

- Payoff is staged after bridge, density, and survival needs are addressed.
- The package has intermediate value before the final payoff.
- Resource, draw, retain, or compression support reaches the payoff window in time.
- The payoff can be delayed without turning the rest of the package into blanks.

Risk signals:

- Payoff is recommended before bridge or stabilizer.
- The package has a high ceiling but weak first functional turn.
- Payoff competes with the same energy, draw, or hand slot required to assemble it.
- Starter pollution or deck size sensitivity makes payoff contact unreliable.

Boundary:

`payoff_timing` overlaps with mechanism fun/health `setup_tax` and `fail_state`, but
package health only asks whether the package is staged correctly. It does not decide
whether the play pattern is fun once staged.

### `anti_goodstuff` / `soup_suppression`

Definition:

Whether the evaluator can keep a real package distinct from generic good cards,
hybrid soup, or adjacent-family blur.

Healthy signals:

- The primary package remains readable even when useful off-axis cards are present.
- Secondary anchors are visible but do not erase the primary anchor.
- Forbidden or off-plan package hits stay low.
- Hybrid cases keep uncertainty notes instead of forcing a clean label.

Risk signals:

- Generic draw, block, or damage cards are treated as package proof.
- Two adjacent packages are merged into a confident but false package read.
- Goodstuff piles receive the same package-health language as reviewed shells.
- Soup risks are hidden because the package has several individually strong cards.

Boundary:

Soup suppression is not a command to punish every hybrid. It should preserve real
secondary anchors and pivots while refusing fake certainty.

### Starter Pollution And Compression Interaction

Definition:

Whether starter cards, off-plan cards, deck size, and compression assumptions are
visible when they materially affect package health.

Healthy signals:

- Starter Strike/Defend drag is named when it reduces package contact.
- Removal, transform, exhaust, discard filtering, and draw selection are not treated
  as equivalent.
- Effective compression is present before the package depends on it.
- Exceptions are explicit, for example Strike-matters or early survival cases.

Risk signals:

- A curated compact deck is reviewed as if it were a normal route state.
- Discard filtering is counted as persistent thinning.
- Transform is counted as clean removal without replacement-risk notes.
- A loop or exactness package ignores basic-card drag.

Boundary:

Deck compression owns reachability wording such as `online_if_compressed` or
`route_dependent_online`. Package health should report that pollution or compression
pressure weakens package confidence, but should not replace the compression model.

### Bridge-Before-Payoff

Definition:

Whether the package obeys the assembly order required by its own structure.

Healthy signals:

- Bridge or density patches arrive before payoff upgrades.
- Draft closure evidence records bridge first and payoff/conversion later.
- `not_now` boundaries keep greed from becoming the next priority.
- Reports explain why a bridge is the right next package move.

Risk signals:

- The package adds a finisher while still missing bridge or stabilizer slots.
- The evaluator treats payoff excitement as closure.
- Bridge cards are present by tag but do not actually connect setup to payoff.
- The package's best card makes the package more brittle.

Boundary:

Bridge-before-payoff is a package sequencing rule. It is compatible with high-ceiling
combo packages; it only asks that the route to the payoff is evidence-backed.

### Primary And Secondary Anchor Uncertainty

Definition:

Whether the package's main identity and nearby pivot are both represented honestly.

Healthy signals:

- The primary anchor is supported by retrieval or reviewed anchor evidence.
- The secondary anchor is visible when evidence supports it.
- Thin-margin notes such as `thin_margin_secondary_anchor:*` remain in the output.
- Low confidence stays low when anchors are split.

Risk signals:

- Secondary anchor evidence is erased to make the primary package look cleaner.
- A secondary anchor is promoted to primary because it is generically strong.
- Dual-anchor uncertainty is flattened into a single high-confidence package.
- Pivot options are treated as immediate payoff upgrades.

Boundary:

Anchor uncertainty is not a failure by itself. It becomes a package-health risk when
the output hides the uncertainty or acts as if the split is solved.

## Minimal V1 Payload

A later report-only implementation can use a compact payload like this:

```json
{
  "card_package_health": {
    "contract_version": "card_package_health_v1",
    "evaluation_mode": "report_only",
    "overall_label": "watch_package",
    "primary_anchor": {
      "anchor_id": "sts1_silent:poison_clock",
      "evidence_supported": true
    },
    "secondary_anchor": {
      "anchor_id": "sts1_silent:frontload_tempo",
      "evidence_supported": true,
      "uncertainty_notes": ["thin_margin_secondary_anchor:frontload_tempo"]
    },
    "dimensions": {
      "package_density": {
        "label": "medium",
        "reason_codes": ["primary_shell_readable", "density_still_thin"]
      },
      "slot_fit": {
        "label": "watch",
        "missing_slots": ["stabilizer", "density"]
      },
      "closure_fit": {
        "label": "not_evaluated",
        "reason_codes": ["no_draft_closure_trace"]
      },
      "motif_fit": {
        "label": "healthy",
        "positive_motifs": ["primary_shell_readable", "pivot_option_visible"],
        "risk_motifs": ["secondary_anchor_uncertainty"]
      },
      "payoff_timing": {
        "label": "watch",
        "reason_codes": ["payoff_after_density_needed"]
      },
      "soup_suppression": {
        "label": "healthy",
        "reason_codes": ["secondary_anchor_kept_as_pivot"]
      },
      "starter_pollution_compression": {
        "label": "watch",
        "reason_codes": ["starter_drag_unknown", "compression_context_missing"]
      },
      "bridge_before_payoff": {
        "label": "watch",
        "reason_codes": ["bridge_needed_before_finisher"]
      }
    },
    "projection_gaps": ["poison_tick_breakpoint_precision"],
    "boundaries": [
      "does_not_change_mechanism_viability",
      "does_not_claim_fun_score",
      "does_not_price_removal_route"
    ]
  }
}
```

This payload is intentionally report-only and should not be used as a hard gate in V1.

## Boundary With Other Specs

### Mechanism Viability

Mechanism viability answers:

- Is the named mechanism online, repeatable, and coherent?

Package health answers:

- Does the card package around that mechanism have enough density, slot fit,
  sequencing, and anchor evidence to be a healthy package?

Example split:

- A `Dropkick` loop can be mechanism-online in a curated shell.
- Package health can still mark it `watch_package` if bridge-before-payoff,
  starter pollution, or anchor uncertainty is unresolved.

### Fun/Health

Fun/health answers:

- Does the online mechanism create good play texture?

Package health answers:

- Is the package assembled and evidenced well enough to be judged as a package?

Example split:

- A shiv package can have strong package density and slot fit.
- Fun/health may still flag action-punisher matchups, low agency, or degeneracy
  pressure.

### Deck Compression And Removal

Deck compression answers:

- Is the package reachable from a realistic deck state, or does it require removal,
  transform, or in-combat compression?

Package health answers:

- Does starter pollution or missing compression weaken the package read?

Example split:

- A Rushdown package can show a clear primary anchor and bridge-before-payoff logic.
- Deck compression owns the stronger claim that the infinite is
  `route_dependent_online` unless removal or effective compression evidence exists.

## Minimum Review Checklist

For V1 docs or later reviewed cases, check only these questions:

1. Is the primary anchor evidence-backed?
2. Is any secondary anchor preserved as uncertainty or pivot evidence?
3. Are package density and missing slots visible?
4. Does payoff come after bridge, density, or stabilizer needs?
5. Are closure claims backed by draft or evidence traces?
6. Are fun/risk motifs and projection gaps still visible?
7. Are starter pollution and compression assumptions called out when relevant?
8. Is goodstuff or soup suppressed without hiding real hybrid evidence?

If the answer requires new thresholds, learned ranking, route simulation, or STS2 trust
promotion, it is outside this V1 spec.

## Current Bottom Line

Card package health V1 should make one thing clear: a package is healthy when its
identity, slots, sequencing, anchors, and uncertainty are evidence-backed.

It should not become a new authority over legality, benchmark gates, fun scoring,
compression reachability, or learned ranking.
