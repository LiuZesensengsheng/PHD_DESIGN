# Cardanalysis Tool Facade V1

## Purpose

`cardanalysis_tool_facade_v1` is the top-level Codex-facing map for the
slimmed cardanalysis system.

It does not replace the existing generators, validators, exams, or review-pack
builders. It names the small set of user workflows Codex should reach for first,
then points each workflow to the current canonical route.

## Reset Goal

As of 2026-06-08, the active slimming goal is not to preserve every historical
report-only surface. The goal is to make `cardanalysis` usable as a compact
tool with one obvious path:

```text
generate_or_ingest -> exam -> review_pack -> feedback -> iterate
```

Success means Codex can design or ingest a candidate card package, run the
current report-only exams, produce a Chinese human review packet, accept human
feedback, and prepare the next iteration without understanding old internal
sidechains.

The target shape is:

- keep the five facade actions stable,
- keep direct schema validators and canonical exam/review routes stable,
- keep library code only when a facade route calls it or a retained test proves
  a live contract,
- delete historical wrappers, generated artifact fixtures, sidecar reports,
  and advisory chains that no longer feed the facade,
- reduce the surrounding `cardanalysis` surface toward roughly 120k lines before
  broad new design capability expansion resumes.

This target accepts some historical-report capability loss when the capability
does not serve the current tool path. It does not accept losing the authority
boundary, validation boundary, or human-review loop.

## Actions

| Action | Chinese Name | Use For |
| --- | --- | --- |
| `generate_or_ingest` | 生成或接入草稿 | Validate, generate, or ingest `complete_card_draft_v1` through an explicit provider. |
| `exam` | 考试 | Run report-only card package, advisory, STS1 reference, similarity, composition, and strong-build exams. |
| `review_pack` | 中文审核包 | Produce Chinese-readable 12-card, 30-card, strong-build, or exploration review material. |
| `feedback` | 反馈接入 | Convert human, closed-test, or paper-play observations into advisory input for the next round. |
| `iterate` | 下一轮迭代 | Feed provider comparison and advisory exam readouts back as next-round metadata. |

`generate_or_ingest` also records supporting input-preparation routes for
mechanism-axis search, design brief, package seed, and package-proposal
validation. It also records the external draft prompt-application intake command
for owner/model-supplied complete-card drafts. These are support commands for
preparing inputs, not separate top-level cardanalysis workflows.

## Boundary

The facade preserves the existing cardanalysis authority boundary:

- report-only / advisory-context-only,
- no runtime card data writes,
- no formal card promotion,
- no hard gates,
- no score weight or default synthesis changes,
- no learned/reranker behavior,
- no LLM/API call,
- no promotion of speculative, source-mined, or human-curated material into
  reviewed evidence.

## CLI

List the action map:

```powershell
python scripts/run_cardanalysis_tool_facade.py --list-actions
```

Print the full machine-readable map:

```powershell
python scripts/run_cardanalysis_tool_facade.py --json
```

Inspect one action:

```powershell
python scripts/run_cardanalysis_tool_facade.py --action review_pack
python scripts/run_cardanalysis_tool_facade.py --action review_pack --json
```

Print command templates for one action:

```powershell
python scripts/run_cardanalysis_tool_facade.py --action review_pack --commands
python scripts/run_cardanalysis_tool_facade.py --action exam --commands
```

The `review_pack` and `exam` command lists also include the Engineering
cardpool review packet and Engineering data-method probe. These remain
report-only/advisory-context-only draft review surfaces, not runtime card data
or formal card promotion.

Print input-preparation and generation command templates:

```powershell
python scripts/run_cardanalysis_tool_facade.py --action generate_or_ingest --commands
```

Check that the facade still points to live scripts:

```powershell
python scripts/run_cardanalysis_tool_facade.py --check
python scripts/run_cardanalysis_tool_facade.py --check --json
```

## Slimming Rule

Future deletion should be facade-guided:

- keep surfaces that directly serve one of the five facade actions,
- demote implementation-only helpers to library or fixture surfaces,
- delete historical wrappers, duplicate wrapper tests, duplicate
  report/snapshot/manifest writers, and overlarge historical fixture/report
  surfaces that do not serve the facade.

The facade is a routing layer, not a new scoring owner.
