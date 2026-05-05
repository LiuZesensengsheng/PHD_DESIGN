# Campaign Orchestration Smoke Pack V1

## Goal

Provide the default fast regression pack for future campaign orchestration
touches.

Use this before opening a broader campaign refactor or after touching any of:

- startup / cleanup
- transition requests
- block click routing
- modal locks
- thesis submission / publication follow-up
- small session-access seams

## Default Smoke Pack

```bash
python -m pytest \
  tests/campaign/test_campaign_ui_handoff_contracts.py \
  tests/campaign/test_campaign_transition_request_contract.py \
  tests/campaign/test_campaign_combat_encounter_contract.py \
  tests/campaign/test_campaign_dependency_narrowing_services.py \
  tests/campaign/test_campaign_orchestration_aggregate_invariants.py \
  -q
```

```bash
python -m pytest \
  tests/campaign/test_campaign_guardrail_flow_contracts.py \
  tests/campaign/test_reward_transition_protocol.py \
  tests/campaign/test_reward_modal_opens_once_and_unlocks_input.py \
  tests/campaign/test_thesis_innovation_placeholder_flow.py \
  tests/shared/test_transition_protocol_runtime.py \
  -q
```

## Full Confidence Check

```bash
python -m pytest tests -q
```

## Usage Rule

If the smoke pack fails:

- reopen only the seam that failed
- do not assume the right answer is another broad campaign cleanup pass
- keep UI-safe boundaries intact unless the failure proves they are insufficient
