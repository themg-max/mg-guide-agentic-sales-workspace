# Human Activation Decision — MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1

Public sanitized record of the human activation decision for the canonical-location
synthetic-record read proof. Exact record IDs, PIT/token values, and private
allowlist contents are **not** published here.

---

## Decision packet

```text
DECISION=AUTHORIZED_FOR_EXECUTION

AUTHORIZATION_ID=MG_GUIDE_GHL_CANONICAL_LOCATION_SYNTHETIC_READ_PROOF_V1
WORKFLOW=meeting_follow_up_v1

HUMAN_APPROVER=Aaron Chandler
HUMAN_APPROVAL_ROLE=repository maintainer / CRM operator
HUMAN_APPROVED_AT_UTC=2026-08-12T02:02:01Z

SYNTHETIC_CONTACT_BOUND=YES
SYNTHETIC_OPPORTUNITY_BOUND=YES
RELATIONSHIP_VERIFIED=YES
PRIVATE_ALLOWLIST_COMPLETE=YES

SECRET_EXISTS=YES
SECRET_ACCESS_ALREADY_PROVISIONED=YES
PIT_CANONICAL_LOCATION_VERIFIED=YES
IAM_CHANGE_REQUIRED=NO

AUTHORIZED_OPERATIONS=
  get-contact exact allowlisted synthetic contact MAX=1
  get-opportunity exact allowlisted synthetic opportunity MAX=1
  get-pipelines pipeline metadata only

DENIED_OPERATIONS=
  search-contacts-advanced
  search-opportunity
  search-opportunities-advanced
  create-note
  update-opportunity
  update-opportunity-status
  email
  sms
  raw REST
  any non-allowlisted record ID
  all CRM writes

CONTACT_RECORD_READ_BUDGET=1
OPPORTUNITY_RECORD_READ_BUDGET=1
GHL_WRITES_ALLOWED=0
REAL_CUSTOMER_RECORD_READS_ALLOWED=0

PUBLIC_DISCLOSURE_OF_EXACT_IDS=NO
TOKEN_VALUE_RECORDING=NO

AUTHORITY_EXPANSION=NO
DEPLOYMENT_AUTHORIZED=NO
GEMINI_ADK_AUTHORIZED=NO

HUMAN_SIGNATURE=APPROVED
CURRENT_GRANT_STATE=AUTHORIZED_FOR_EXECUTION
```

---

## Explicit authority

| Operation | Scope | Max |
| --- | --- | --- |
| `get-contact` | exact allowlisted synthetic contact ID only | 1 |
| `get-opportunity` | exact allowlisted synthetic opportunity ID only | 1 |
| `get-pipelines` | pipeline metadata only | unbounded metadata read within this grant |

## Explicit denials

- all broad searches (`search-contacts-advanced`, `search-opportunity`, `search-opportunities-advanced`)
- all non-allowlisted record IDs
- all CRM writes
- `create-note`, `update-opportunity`, `update-opportunity-status`
- email / SMS
- raw REST
- real customer / prospect record reads
- deployment, Gemini/ADK, IAM/secret mutation, authority expansion

## Execution posture for this public binding step

| Field | Value |
| --- | --- |
| `execution_status` | `AUTHORIZED_NOT_EXECUTED` |
| `activation_gate` | `AUTHORIZED_FOR_EXECUTION` |
| `GHL_LIVE_CALLS` | `0` |
| `GHL_WRITES` | `0` |
| `STOP_CODE` | `NONE` |

This human-binding / activation-decision commit **does not** execute any live GHL call.
Live execution requires a separate bounded run against the private allowlist only.
