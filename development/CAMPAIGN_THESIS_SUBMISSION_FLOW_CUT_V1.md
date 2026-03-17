# Campaign Thesis Submission Flow Cut V1

## Goal

Create one explicit thesis submission seam for the most UI-sensitive
`writing complete -> tier choice -> round submission -> review-chain activation`
flow.

## Why This Exists

Before this cut, thesis submission behavior was still split across several
places:

- `ThesisSlice.handle_non_combat_block(...)`
- `ThesisMetaService.check_and_prompt_thesis_tier(...)`
- `ThesisMetaService.open_submission_for_writing_block(...)`
- `ThesisMetaService.submit_round_from_writing(...)`
- raw `CampaignState` block/meta mutation

That meant thesis-writing interactions still depended on scattered sequencing
knowledge instead of one clear orchestration home.

## Stable Submission Seams

The current state-level thesis submission seams are now:

- `CampaignState.check_and_prompt_thesis_submission()`
- `CampaignState.request_thesis_submission_for_writing_block(block)`

`ThesisSubmissionFlowService` now owns:

- scanning for completed active thesis-writing blocks
- opening the journal tier selection prompt
- submitting a writing round from the modal callback
- removing the finished writing block
- activating matching review-chain blocks
- persisting `submitted_rounds` and `submission_history`
- stabilizing the board after submission

Rule:

- UI/runtime code may request thesis submission through the state seam
- UI/runtime code should not manually inspect `_blocks` and replay the flow

## Current Ownership

`ThesisSlice` now only detects that an active writing block was clicked and
forwards that request into the state seam.

`ThesisMetaService` still owns thesis tier/meta rules, but it no longer owns
the whole writing-block submission sequence itself.

This leaves V1 ownership as:

- tier/tag/meta rules in `ThesisMetaService`
- writing-block submission sequencing in `ThesisSubmissionFlowService`
- stable entrypoints on `CampaignState`

## Compatibility Notes

V1 intentionally keeps compatibility wrappers on `ThesisMetaService` for:

- `check_and_prompt_thesis_tier()`
- `open_submission_for_writing_block(...)`
- `submit_round_from_writing(...)`

Existing callers and tests can continue using those names during migration, but
new flow work should prefer the state seam and the dedicated submission flow
ownership.

## Non-Goals

This cut does not:

- redesign thesis into a final aggregate model
- merge publication and innovation follow-up into the same service
- remove every internal `_blocks` write from campaign code
- freeze the final DDD shape of thesis

## Verification

V1 is currently protected by focused regressions covering:

- writing-block request opens the thesis submission prompt through the seam
- round submission removes the writing block and wakes the matching review chain
- thesis judgment/publication follow-up flows still pass
- modal-lock rules still hold while publication-flow tests avoid unrelated
  startup meeting-prompt ownership when validating their own chain

## Next Cut

The next highest-value campaign handoff task is:

- `Campaign Runtime UI Boundary V1`
