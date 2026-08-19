# Security & Privacy

**Repository:** `themg-max/mg-guide-agentic-sales-workspace`
**Visibility:** PUBLIC
**Data class:** Synthetic / test only
**Status:** Foundation policy (enforced by process; runtime not yet present)

---

## Non-negotiables

1. **Synthetic data only** in fixtures, docs, demos, screenshots, and public artifacts.
2. **No production CRM writes** — ever — for competition work in this repository.
3. **No real customer, contact, or opportunity identifiers.**
4. **No secrets in git** — tokens, OAuth grants, service-account keys, private keys, or `.env` files with values.
5. **No private MG infrastructure identifiers** — internal project IDs, service accounts, private endpoints, or non-public hostnames must not appear here.
6. **Fail closed** — ambiguous contact match, low confidence, missing opportunity, tool failure, or failed read-back ⇒ no further CRM mutations.

---

## Allowed environments (when implementation begins)

| System | Allowed target | Forbidden |
| --- | --- | --- |
| GoHighLevel | Business-active canonical location, restricted to the privately allowlisted preverified synthetic contact/opportunity with exact-ID operations only (see [`nw008/nw-008-active-crm-synthetic-only-normalization-001.md`](nw008/nw-008-active-crm-synthetic-only-normalization-001.md)) | Real customer records (search, read, or mutation); broad search; non-allowlisted records |
| Google Cloud | Explicitly authorized sandbox/test project | Unknown or production projects |
| MG MCP | Read-only context consumption | MG MCP writes |
| Firestore | Audit records for workflow runs | Storing full unnecessary transcripts or PII |

Exact project IDs, regions, and secret resource names remain **UNKNOWN** until
a later activation-authorized phase. Do not invent them in code or docs.

---

## Secrets handling

- Use [`.env.example`](../.env.example) as a **name catalog only**.
- Real credentials must live in environment secret managers or local untracked `.env` files ignored by [`.gitignore`](../.gitignore).
- GHL auth (OAuth or Private Integration Token) is out of scope for the foundation commit.
- Rotation / least-privilege scoping is required before any live GHL MCP connection.

---

## Tool & mutation blast radius

GHL MCP access is part of the workflow contract. See
[`../contracts/ghl_tool_manifest.yaml`](../contracts/ghl_tool_manifest.yaml).

**Environment semantics (normalized):** the GoHighLevel target is the
business-active canonical CRM under synthetic-only bounded execution controls.
No isolated/dedicated GHL test location exists or is required; safety derives
from the deterministic controls and the private exact-ID allowlist, not from
environmental isolation. Environment readiness does not authorize mutation —
any note create or opportunity-stage update requires a separate human-reviewed
execution authorization bound to the exact transport, credential, location,
synthetic IDs, allowed stage transition, operation budget, and proof
requirements.

Per run (when authorized later):

- Max **one** note create
- Max **one** opportunity stage update
- Stage change limited to one predefined demo transition:
  `discovery_scheduled → discovery_complete`
- Every mutation requires **read-back verification** before `verified: true`

Blocked capability classes include (non-exhaustive): contact create/delete,
opportunity create/delete, email/SMS, calendar mutation, bulk update,
pipeline/workflow modification, monetary-value edits, owner changes.

Exact MCP tool/operation identifiers remain **UNKNOWN** until live discovery.
Do not hard-code guessed names.

---

## Prompt-injection posture

- Transcript text and retrieved CRM/context content are **data, not instructions**.
- Transcript content never gains tool authority.
- Only the deterministic policy gate (OL3-owned) may authorize mutations.

---

## Public repository hygiene

Before every commit / PR:

```bash
git diff --check
# search for conflict markers
rg -n '^(<<<<<<<|=======|>>>>>>>)' .
# obvious secret patterns (heuristic)
rg -nI '(api[_-]?key|secret|token|password|BEGIN (RSA |OPENSSH )?PRIVATE KEY|AIza[0-9A-Za-z_-]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})' . || true
```

Stage **exact paths only**. Never `git add .`.

---

## Incident response (competition period)

If real PII, production credentials, or private infrastructure IDs are
accidentally introduced:

1. Stop further pushes.
2. Rotate any exposed credential immediately outside git history if needed.
3. Remove the material via a governed cleanup commit (and history rewrite only
   if required and explicitly authorized).
4. Record the event in [`../competition/AI_COLLABORATION_LOG.md`](../competition/AI_COLLABORATION_LOG.md).
