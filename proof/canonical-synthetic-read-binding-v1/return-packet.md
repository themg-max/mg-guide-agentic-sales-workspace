# Return packet — MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1 (binding)

Public sanitized return packet after human synthetic-record binding and activation
decision. **No live GHL execution occurred in this unit.**

```text
SYNTHETIC_CONTACT_BOUND=YES
SYNTHETIC_OPPORTUNITY_BOUND=YES
RELATIONSHIP_VERIFIED=YES
PRIVATE_ALLOWLIST_COMPLETE=YES
PIT_CANONICAL_LOCATION_VERIFIED=YES
IAM_CHANGE_REQUIRED=NO
HUMAN_SIGNATURE=APPROVED
CURRENT_GRANT_STATE=AUTHORIZED_FOR_EXECUTION
EXECUTION_STATUS=AUTHORIZED_NOT_EXECUTED
GHL_LIVE_CALLS=0
GHL_WRITES=0
REAL_CUSTOMER_RECORD_READS=0
STOP_CODE=NONE
PUBLIC_DISCLOSURE_OF_EXACT_IDS=NO
TOKEN_VALUE_RECORDED=NO
DEPLOYMENT_AUTHORIZED=NO
GEMINI_ADK_AUTHORIZED=NO
AUTHORITY_EXPANSION=NO
```

## Budgets (authorized, not consumed this unit)

| Budget | Authorized | Consumed this unit |
| --- | --- | --- |
| Contact record reads | 1 (exact allowlisted synthetic) | 0 |
| Opportunity record reads | 1 (exact allowlisted synthetic) | 0 |
| Pipeline metadata | get-pipelines allowed | 0 |
| GHL writes | 0 | 0 |
| Real customer reads | 0 | 0 |

## Authorized operations (deferred live execution)

- `get-contact` — exact allowlisted synthetic contact — MAX=1
- `get-opportunity` — exact allowlisted synthetic opportunity — MAX=1
- `get-pipelines` — pipeline metadata only

## Denied operations (still denied)

- broad searches
- non-allowlisted IDs
- all writes (`create-note`, `update-opportunity`, `update-opportunity-status`, email/SMS)
- raw REST
- deployment / Gemini-ADK / IAM-secret mutation

## Notes

- Exact IDs remain private-control-plane only.
- This binding step stops without live CRM contact.
- A later bounded execution unit may consume the read budgets only under this grant.
