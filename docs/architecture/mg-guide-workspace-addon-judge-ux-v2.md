# MG Guide Workspace Add-on — Judge UX v2 (Follow-Up Draft)

```text
ARTIFACT=docs/architecture/mg-guide-workspace-addon-judge-ux-v2.md
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
WORKFLOW=meeting_follow_up_v1
ROLE=THIN_PRESENTATION_AND_ROUTING_ADAPTER
SUPERSEDES_DISPLAY_OF=mg-guide-workspace-addon-judge-ux-v1.md
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
CURRENT_TRANSCRIPT_SOURCE=synthetic_fixture
LIVE_CRM_EXECUTION=NOT_PERFORMED
EMAIL_AUTO_SEND=FORBIDDEN
```

## 1. What v2 changes

v1 rendered the judge run like a harness (six stage evidence sections first,
outcome last). v2 renders it like a product: result first, draft preview and a
human-controlled Gmail compose action in the primary journey, and technical
audit/integrity detail below.

No backend workflow, policy, fixture, or CRM behavior changes. The only new
backend surface is a deterministic view-model projection
(`ux_experience.follow_up_draft`, `ux_experience.crm_note_status`) derived from
already approved fields. No model invocation is added.

## 2. UI architecture

```text
Gmail / Calendar host
  -> workspace_addon CardService (MG Guide home)
  -> Process Meeting Follow-Up (scenario=SUCCESS)
       | Judge test scenarios: Ambiguous contact / Policy guardrail
  -> POST /demo/meeting-follow-up  (existing judge surface)
  -> WorkflowRunner + packet + card mapper + demo_stages + ux_experience
       -> ux_experience.follow_up_draft   (deterministic, server-side)
       -> ux_experience.crm_note_status  (narrow display contract)
  -> buildResultCardFromJudgePayload (field display only)
  -> Open Draft in Gmail
       -> createFollowUpDraft (ComposeAction)
       -> re-fetch same approved synthetic scenario
       -> validate ux_state=COMPLETED + follow_up_draft.status=READY
       -> GmailApp.createDraft(recipient, subject, body_text)
       -> ComposeActionResponse (standard editable compose window)
```

The compose callback never sends. Forbidden APIs in `workspace_addon/*.gs`:
`GmailApp.sendEmail`, `MailApp.sendEmail`, `GmailMessage.reply[All]`,
`GmailThread.reply[All]`, `draft.send()`.

```text
EMAIL_AUTO_SEND=FORBIDDEN
DRAFT_CREATION_REQUIRES_USER_ACTION=YES
FINAL_SEND_REQUIRES_HUMAN=YES
```

## 3. Home card (v2)

| Element | Content |
| --- | --- |
| Primary message | **Meeting Follow-Up** — Turn a completed meeting into relationship context, CRM-ready documentation, and a follow-up draft. |
| Truth marker (small) | **Competition mode** — Approved synthetic transcript · governed CRM boundary |
| Primary CTA | **Process Meeting Follow-Up** (`scenario=SUCCESS`) |
| Secondary section | **Judge test scenarios** — Ambiguous contact, Policy guardrail (fail-closed, retained) |

"No CRM writes" is a truth boundary, not the visual headline.

## 4. SUCCESS result order

1. **Follow-up ready** — status grid: Transcript `Processed` · Meeting
   `Understood` · Relationship `Matched` · CRM note (backend display) ·
   Follow-up draft `Ready`.
2. **Processing status** — UX_STATE, workflow, stages recorded.
3. **What we heard** — summary, key needs, objections, salesperson next step.
4. **Relationship** — Matched/needs review + match basis. Raw provider IDs are
   never rendered.
5. **CRM** — `crm_note_status.display` from backend truth only.
6. **Follow-up draft** — recipient display name/email, subject, short body
   preview, "human review and send required" marker.
7. **Send follow-up** — `Open Draft in Gmail` compose action (exactly one).
8. **Audit and integrity** — six-stage status summary, policy fields, audit
   status, integrity line
   (`UX_STATE=… · external_effects=0 · LIVE_CRM_EXECUTION=NOT_PERFORMED · CRM_MUTATIONS_PERFORMED=NO · EMAIL_AUTO_SEND=FORBIDDEN`).

## 5. NEEDS_REVIEW result order

1. **Needs review** — `NEEDS REVIEW`; Relationship `Ambiguous`; CRM
   `CRM update blocked. No change performed.`; Draft `Not created`; human
   `Why:` reason; explicit next action.
2. Processing status, What we heard, Relationship, CRM (zero-effects message).
3. Audit and integrity.

No compose action is rendered for any `NEEDS_REVIEW` result.

## 6. Deterministic follow-up draft projection

`project_ux_experience` now emits `ux_experience.follow_up_draft`:

```json
{
  "status": "READY | NOT_AVAILABLE",
  "recipient_name": "…",
  "recipient_email": "…",
  "subject": "…",
  "body_text": "…",
  "source": "meeting_follow_up_v1",
  "requires_human_send": true
}
```

Permitted inputs (only): `meeting_context.prospect.name/email`,
`meeting_context.agent.name`, `meeting_context.title`, `summary`,
`proposed_follow_up.summary/needs/objections`, `salesperson_next_step`.

Never used: raw CRM IDs, provider responses, secret material, private
reasoning, unsupported advice, invented facts.

Rules:

- `READY` requires `ux_state=COMPLETED` and a resolved prospect email.
- `NEEDS_REVIEW` (including `AMBIGUOUS_CONTACT`) ⇒ `NOT_AVAILABLE`; a blocked
  or ambiguous relationship never gets a compose action.
- Deterministic formatting: `Follow-up: <meeting title>` subject; fixed body
  template (greeting → thank-you → meeting summary paragraph → next step →
  adjustment offer → agent sign-off).

## 7. CRM note status contract

`ux_experience.crm_note_status = {"state", "display"}` with narrow mapping:

| State | Display | Reachable in competition mode |
| --- | --- | --- |
| `NOT_EXECUTED` | CRM note not executed in competition mode | Yes (COMPLETED) |
| `BLOCKED` | CRM update blocked. No change performed. | Yes (NEEDS_REVIEW) |
| `VERIFIED` | CRM note verified | **No** — requires explicit durable verified-effect evidence (`crm_effect.verified=true` + `evidence=provider_readback`) AND `LIVE_CRM_EXECUTION=PERFORMED` |
| `UNKNOWN` | CRM note status unavailable. No CRM change confirmed. | Fail-closed fallback |

Policy permission (`policy.note_write=allowed`), `proposed_note`, note
intents, or workflow completion are never execution proof. The presentation
layer additionally fails closed: a `VERIFIED` claim with
`LIVE_CRM_EXECUTION!=PERFORMED` renders as `UNKNOWN`.

## 8. OAuth scope surface (least privilege)

Added: `https://www.googleapis.com/auth/gmail.addons.current.action.compose`.

Not added (forbidden on this adapter): `https://mail.google.com/`,
`gmail.send`, `gmail.modify`, any Drive scope, any Admin scope.

The new scope changes the authorization surface: existing test installations
must re-authorize before the compose action works (see proof artifact).

## 9. State / payload design

Design A (chosen): the compose callback re-fetches the deterministic judge
projection for the same approved synthetic scenario and reads the
server-generated `follow_up_draft`. No state store, no cached credentials, no
serialized CRM capability, no raw provider IDs cross the Apps Script boundary.
If a future design needs state storage, that requires a separate scope review.

## 10. Boundaries (unchanged)

```text
TRANSCRIPT_SOURCE_CONTRACT=TRANSCRIPT_SOURCE_ENVELOPE_V1
CURRENT_TRANSCRIPT_SOURCE=synthetic_fixture
GMAIL_BODY_READS=NO
CALENDAR_EVENT_CONTENT_READS=NO
DRIVE_SCOPE=NO
REAL_WORKSPACE_TRANSCRIPT_READ=NO
GOOGLE_WORKSPACE_TRANSCRIPT_ADAPTER=FUTURE_NOT_IMPLEMENTED
CURRENT_LIVE_CRM_EXECUTION=NOT_PERFORMED
R5_CAN_CLOSE_WITH_CURRENT_SURFACE=NO
```

The add-on never becomes the private-origin owner. Future live CRM effect
path remains: agent/fleet output → deterministic policy → legitimate
private-origin materialization → bounded HighLevel NOTE_PATH → verified
provider readback → sanitized effect result → add-on display.
