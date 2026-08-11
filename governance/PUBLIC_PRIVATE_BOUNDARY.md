# Public / private boundary

## Public repository (this repo)

**May contain**

- Sanitized architecture and competition docs
- Contracts, schemas, and synthetic fixtures
- Public governance profile and proof schemas
- Implementation, tests, and public proof for authorized phases
- Competition ledger and AI collaboration log entries

**Must not contain**

- Private `.ai` lane inventory or active-lane internals
- Private filesystem paths from the control-plane workstation
- Secrets, tokens, credentials, or private keys
- Internal-only service endpoints
- Private GCP project/resource identifiers not intended for public disclosure
- Customer / production CRM data
- Private proof digests or inherited authorization packages from other pilots
- DataHub (or other pilot) allowlist admissions reused as authority here

## Private control plane (not this repo)

Retains:

- Governance source authority and current-phase decisions
- Human adoption dispositions and implementation grants
- Lane lifecycle, closeout, and private proof packets
- Any non-public operational detail

## Authority reminders

| Claim | Valid? |
| --- | --- |
| Public docs exist ⇒ production ready | **No** |
| PR merged ⇒ deployment authorized | **No** |
| Agent proposed a CRM write ⇒ write allowed | **No** |
| Synthetic fixture passed ⇒ production data authorized | **No** |
| Repository adopted for competition implementation ⇒ GHL/IAM authorized | **No** |

## Cross-boundary flow

```text
Private governance grant
        ↓
Public bounded topic branch (exact scope)
        ↓
Deterministic validation + proof return
        ↓
Public PR review/merge
        ↓
Separate activation grant (if ever)
```
