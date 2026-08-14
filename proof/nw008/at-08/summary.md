# AT-8 evidence summary

- EVIDENCE_CLASS: `PARTIAL_SUPPORTING_PROOF`
- HISTORICAL_AT_COMPLETE: `NO`
- TEST_RESULT: `PASS`
- SOURCE_FIXTURE: `contracts/workflow_states.yaml#policy_thresholds+max_intents`
- INPUT_HASH: `da82e2fc52f77da09bb798a8ff96cda3a5e14166d9ec2aebe746b11840bd3a7e`
- ACTUAL_WORKFLOW_STATUS: `policy_cap_evaluation`
- AUTHORITATIVE_REASON_CODES: `[]`
- CARD_POLICY_STATE / CARD_REASON_CODE / CARD_NEXT_ACTION: `NOT_APPLICABLE` / `NOT_APPLICABLE` / `NOT_APPLICABLE`
- REMAINING_GAP: active mutation-execution trace showing second attempt refusal by policy

## Clause coverage

- `deterministic_policy_cap_enforced`: **PASS**

## Effect counters

- GHL_LIVE_CALLS=0
- GHL_READS=0
- GHL_WRITES=0
- FIRESTORE_WRITES=0
- EXTERNAL_EFFECTS=0
- REAL_CUSTOMER_DATA=0
