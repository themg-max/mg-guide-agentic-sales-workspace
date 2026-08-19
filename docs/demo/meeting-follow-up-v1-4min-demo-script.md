# ~4 minute demo script — meeting_follow_up_v1

```text
ARTIFACT=docs/demo/meeting-follow-up-v1-4min-demo-script.md
DURATION_TARGET=3:45–4:15
WORKFLOW=meeting_follow_up_v1
TRUTH_BOUNDARY=docs/demo/meeting-follow-up-demo-v1.md
```

**Presenter rule:** every spoken value must match the live judge runner packet
for the selected scenario. No story-polish aliases. Synthetic data only.

## Runtime prep (before record)

```bash
export PYTHONPATH=src MEETING_CONTEXT_GEMINI_MODE=stub JUDGE_MODE=local
python -m mg_guide.judge_surface.server
# POST http://127.0.0.1:<port>/demo/meeting-follow-up
# body: {"scenario":"SUCCESS"} then {"scenario":"AMBIGUOUS_CONTACT"}

# Optional parallel terminals for Google Cloud proof:
gcloud run services describe mg-guide-agentic-sales-workspace-judge \
  --region=us-east4 --project=mg-devpost
# Firestore proof already green via scripts/nw005/run_stage_b_wave1_smoke.py
```

Hosted URL (IAP — human 2FA if using browser):

`https://mg-guide-agentic-sales-workspace-judge-nu73xamzbq-uk.a.run.app`

If IAP blocks recording, use local judge parity + Cloud Console screenshots.

---

## Beat sheet

| T | Section | On screen | Spoken |
| --- | ---: | --- | --- |
| 0:00–0:25 | Problem | Sales inbox / empty CRM note | After a discovery call, reps still retype notes, hunt the contact, and guess the next stage. That’s slow and error-prone. |
| 0:25–0:55 | Workflow | Architecture diagram | MG Guide runs an agentic `meeting_follow_up_v1` slice: Gemini extracts context, ADK sequences specialized agents, and a deterministic OL3 policy gate decides what is allowed. |
| 0:55–2:10 | SUCCESS | Judge SUCCESS response + card | Watch a synthetic transcript flow through Meeting Context → Relationship Context → Follow-Up Planning. Policy allows the proposed note and stage intent. The MG Guide card shows the completed next-step state. External unauthorized effects stay zero on this demo path. |
| 2:10–3:10 | Fail-closed | Judge AMBIGUOUS_CONTACT | Now identity is ambiguous. Agents still propose, but OL3 blocks writes: `AMBIGUOUS_CONTACT`, workflow blocked, needs-review. Zero unauthorized CRM effects. Governance over autonomy. |
| 3:10–3:40 | Architecture / governance | Mermaid or layer table | Gemini 3.5 Flash proposes; Google ADK orchestrates; OL3 authorizes; Cloud Run hosts the judge; Firestore holds audit evidence; CRM tools sit behind the gate. |
| 3:40–4:05 | Google Cloud proof | Console / gcloud / smoke JSON | Visible proof: Cloud Run Ready in `mg-devpost` us-east4; Firestore Stage B create/read/verify/delete PASS; live Vertex Gemini extract PASS. |
| 4:05–4:15 | Close | Logo + repo | Fortified Enterprise Fleet: autonomous sales follow-up that fail-closes when trust is missing. |

---

## Scenario call payloads

### SUCCESS

```http
POST /demo/meeting-follow-up
Content-Type: application/json

{"scenario":"SUCCESS","view":"html"}
```

Call out fields:

- `workflow_status: completed`
- `resolution_outcome.status: matched`
- `policy_decision.note_write: allowed`
- `policy_decision.stage_write: allowed`
- `external_effects: 0`
- `cloud_mutation: NONE`
- card / `ux_experience` next-step brief

### FAIL-CLOSED

```http
POST /demo/meeting-follow-up
Content-Type: application/json

{"scenario":"AMBIGUOUS_CONTACT","view":"html"}
```

Call out fields:

- `workflow_status: blocked`
- `reason_codes: ["AMBIGUOUS_CONTACT"]`
- `note_write: not_attempted` / `stage_write: not_attempted`
- `external_effects: 0`
- needs-review salesperson guidance

---

## B-roll / cutaways

1. `docs/architecture/meeting-follow-up-v1-competition-architecture.md` diagram
2. Terminal: Unit3 ADK harness PASS markers
3. Terminal: Gemini live proof `schema_valid=true`
4. Cloud Run service Ready in console
5. Firestore smoke RESULT=PASS (then deleted — stage_b_smoke)

## Recording checklist

- [ ] Mic levels + screen 1080p
- [ ] No secrets / tokens / private script IDs on screen
- [ ] SUCCESS then FAIL-CLOSED order
- [ ] Architecture beat includes OL3 + CRM boundary
- [ ] Cloud proof visible (console or CLI)
- [ ] Final cut ≤ 4:15 unless platform allows longer

## Non-claims (do not say)

- Do not claim live production CRM writes
- Do not claim real customer data
- Do not claim Marketplace/source reconciliation completed
- Do not imply agents bypass policy
