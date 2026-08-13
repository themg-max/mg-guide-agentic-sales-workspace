# NW-007 — Cloud Run Judge-Surface Deployment & Access Authorization Packet

NW007_AUTHORIZATION_ID=MG_GUIDE_NW007_CLOUD_RUN_JUDGE_SURFACE_V1
PACKET_KIND=CLOUD_RUN_DEPLOYMENT_AND_ACCESS_AUTHORIZATION_REQUEST

This packet is **PLANNING ONLY**. It requests a bounded human authorization
decision for a judge-safe Cloud Run deployment of the existing
`meeting_follow_up_v1` vertical slice. Nothing in this packet is applied.

Hard constraints for this packet:

- DO NOT deploy Cloud Run.
- DO NOT create or modify IAM.
- DO NOT create a service account.
- DO NOT create service-account keys.
- DO NOT create or update secrets.
- DO NOT configure IAP.
- DO NOT perform Firestore writes.
- DO NOT touch GHL/CRM.

Durable baseline (NW-005 Stage B, verified on `origin/main`):

- NW005_STAGE_B_PR=23
- NW005_STAGE_B_FINAL_HEAD=36da854d2e3104694dbfbc7cdb56c5bf8f0d1c78
- NW005_STAGE_B_MERGE_SHA=24115e3e75b833721629dfc9667c0f5b49aeb11c
- NW005_STAGE_B_MERGED_AT=2026-08-13T14:26:45Z
- NW005_STAGE_B_RESULT=PASS

---

## Phase 0 — Target Binding

PROJECT=mg-devpost
PROJECT_CLASSIFICATION=DEDICATED_TEST_NON_PRODUCTION

REGION=us-east4
(matches NW-005 Firestore AUTHORIZED_LOCATION=us-east4)

SERVICE_NAME=mg-guide-agentic-sales-workspace-judge
SERVICE_CLASS=JUDGE_SAFE_SYNTHETIC_NON_PRODUCTION

ACCESS_MODE=AUTHENTICATED_JUDGES
PREFERRED_ACCESS_CONTROL=IAP_GOOGLE_GROUP
PUBLIC_UNAUTHENTICATED_ACCESS=NO

SYNTHETIC_DATA_ONLY=YES
REAL_CUSTOMER_DATA=NO
GHL_CRM_MUTATION=NO
FIRESTORE_RUNTIME_WRITES=NO

DEPLOYMENT_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SERVICE_ACCOUNT_CREATION_AUTHORIZED=NO
SERVICE_ACCOUNT_KEY_CREATION_AUTHORIZED=NO
SECRET_MANAGER_MUTATION_AUTHORIZED=NO
IAP_CONFIGURATION_AUTHORIZED=NO

CURRENT_STATE=PROPOSED_NOT_AUTHORIZED
HUMAN_SIGNATURE=PENDING
SELF_ACTIVATION=FORBIDDEN

---

## Phase 1 — Read-Only Runtime Inspection (resolved)

Inspection was read-only; no code was changed. Values that could not be
verified from the repository are recorded as UNKNOWN.

| Key | Value | Evidence |
| --- | --- | --- |
| RUNTIME_ENTRYPOINT | CLI modules only: `python -m orchestration` (`src/orchestration/runner.py` deterministic fixture runner), `python -m mg_guide.meeting_follow_up_card` (`src/mg_guide/meeting_follow_up_card/cli.py`), and agent harness `__main__` modules. No long-running service entrypoint exists. | `src/orchestration/runner.py` (`main()`, `if __name__ == "__main__"`), `src/mg_guide/meeting_follow_up_card/cli.py`, `src/agents/*/__main__.py` |
| HTTP_SERVER_PRESENT | NO | No Flask/FastAPI/uvicorn/gunicorn/starlette/aiohttp dependency in `pyproject.toml` or `requirements.txt`; no WSGI/ASGI application in `src/`. |
| CONTAINERFILE_PRESENT | NO | No `Dockerfile`, `.dockerignore`, `compose.yaml`, `cloudbuild.yaml`, Cloud Run `service.yaml`, `Procfile`, or `app.yaml` in the repository. |
| CURRENT_GEMINI_AUTH_MODE | STATIC_API_KEY (Gemini Developer API) | `src/agents/meeting_context/providers/gemini_adk_provider.py`: live mode reads the `GEMINI_API_KEY` env var and passes it as the client credential to `google.genai.Client` (see `client_kwargs` construction in `_call_gemini_generate`); default `MEETING_CONTEXT_GEMINI_MODE=stub` requires no credential. |
| VERTEX_AI_SUPPORTED_BY_CURRENT_RUNTIME | NO (not wired in code) | The provider only constructs a `genai.Client` with the static key credential; there is no `vertexai=True` / project+location client path in the current runtime. google-genai as a library supports Vertex AI, but the existing code path does not use it. |
| STATIC_API_KEY_REQUIRED | YES for `MEETING_CONTEXT_GEMINI_MODE=live`; NO for `stub` (judge default) | `GeminiAdkConfig.from_env()` + `_call_gemini_generate()` in `gemini_adk_provider.py`. |
| SECRET_MANAGER_REQUIRED | YES if live Gemini mode is deployed (API key must be stored in Secret Manager, never in env plaintext); NO for stub-mode judge surface | `.env.example` (key placeholder only), no Secret Manager wiring exists. |
| FIRESTORE_REQUIRED_FOR_RUNTIME | NO | The judge surface replays deterministic synthetic fixtures (`fixtures/nw005`, `fixtures/nw006`) through the in-repo policy/state-machine/card mapper; no Firestore read or write is on that path. |
| FIRESTORE_REQUIRED_FOR_JUDGE_DEMO | NO | NW-005 Stage B already produced `proof/nw005/stage-b/nw005-persistence-proof-v1.md`; persistence is proven and does not need re-activation in the judge demo. |

Runtime/dependency facts relevant to the deployment shape:

- Python `>=3.9` (`pyproject.toml`, `.python-version`).
- Pinned runtime deps: `google-adk==1.18.0`, `google-cloud-firestore==2.27.0`,
  `jsonschema==4.23.0`, `PyYAML==6.0.2`; optional extra `gemini`:
  `google-genai>=1.0.0` (needed only for live Gemini mode).
- Google ADK runtime (`src/agents/adk_runtime/runtime.py`) orchestrates
  Meeting Context Agent -> Relationship Context Agent via
  `google.adk` Runner/SequentialAgent/InMemorySessionService and **fails
  closed** when the package is unavailable. The ADK path uses the fixture or
  stub Gemini provider; it does not itself require Gemini credentials.
- MG Guide card mapper/renderer: `src/mg_guide/meeting_follow_up_card/`
  (`mapper.py` packet -> card model, `render_text.py`, `render_html.py`);
  verified against `fixtures/nw006/expected/card-*.json` snapshots.
- NW-005 Firestore adapter: `src/mg_guide/firestore_audit/firestore_store.py`
  — bounded create/get/delete/verify against
  `mg-devpost` / `devpost-google-contest` / `workflow_runs` / `us-east4`
  (Wave 1 smoke only). **MUST NOT be automatically activated** by the judge
  surface: its existence is not a runtime requirement; the judge surface must
  not import or call it.

Deployment-shape implication (for the eventual implementation PR, not this
one): a minimal HTTP adapter (e.g., a stdlib or framework endpoint) and a
container artifact (Dockerfile) **do not yet exist** and would be new,
separately-scoped code. This packet authorizes none of that code.

---

## Phase 2 — Proposed Cloud Run Binding

Single Cloud Run service, single region, no traffic splitting, no custom
domain, no CDN, no VPC connector, no Cloud SQL, no background jobs.

- Service: `mg-guide-agentic-sales-workspace-judge`
- Project/region: `mg-devpost` / `us-east4`
- Ingress: internal-and-cloud-load-balancing compatible with IAP
  (final ingress setting to be recorded in the implementation packet).
- Invocation: authenticated only; `PUBLIC_UNAUTHENTICATED_ACCESS=NO`.
- Data plane: synthetic fixtures only (`fixtures/`), no live CRM, no live
  Firestore, no customer data.

---

## Phase 3 — Runtime Identity Plan (proposed, not created)

RUNTIME_SERVICE_ACCOUNT=mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com
(proposed name; NOT created)

RUNTIME_CREDENTIAL_SOURCE=CLOUD_RUN_SERVICE_IDENTITY_METADATA
(Cloud Run attached service identity via the metadata server / ADC)

SERVICE_ACCOUNT_JSON_KEY=FORBIDDEN
No service-account JSON keys will be created or distributed under any
circumstance.

PROPOSED_RUNTIME_PERMISSIONS (minimum, derived from code inspection):

| Mode | Proposed permissions | Rationale |
| --- | --- | --- |
| Judge default: `MEETING_CONTEXT_GEMINI_MODE=stub` | **NONE** beyond the Cloud Run service identity itself. Zero GCP API calls on the request path. | Stub mode + fixtures + in-repo deterministic policy + card mapper require no network egress to GCP. |
| Optional live Gemini via existing API-key path | `roles/secretmanager.secretAccessor` on exactly one secret holding `GEMINI_API_KEY` | Live mode reads the key from env; the key must come from Secret Manager, never committed or passed as plaintext env. |
| Optional live Gemini via Vertex AI | `roles/aiplatform.user` (project-scoped) — **NOT currently supported by the runtime code**; would require a code change to use the Vertex path of google-genai, plus a separate authorization. | Recorded as the preferred long-term credential-free path, but out of scope for NW-007 because `VERTEX_AI_SUPPORTED_BY_CURRENT_RUNTIME=NO`. |

Unresolved authorization requirement (recorded, NOT executed):

- If live Gemini mode is approved for the judge surface, a Secret Manager
  secret for the Gemini API key must be created and bound under a separate
  explicit approval. **No secret is created by this packet.**
  UNRESOLVED_REQUIREMENT=GEMINI_API_KEY_SECRET_IF_LIVE_MODE_APPROVED

FIRESTORE permissions: **NONE** for the NW-007 judge runtime.
NW-005 persistence proof
(`proof/nw005/stage-b/nw005-persistence-proof-v1.md`) is sufficient evidence;
Firestore writes are not activated merely because the adapter exists.

---

## Phase 4 — Judge Access Plan (proposed, not applied)

Intended judge flow:

```
Judge Google identity
  -> authenticated access boundary (IAP, Google group membership)
  -> Cloud Run service: mg-guide-agentic-sales-workspace-judge
  -> synthetic meeting_follow_up_v1 (fixture-selected scenario)
  -> deterministic policy result (no live mutation)
  -> MG Guide Meeting Follow-Up card (mapped payload + rendered view)
```

JUDGE_GOOGLE_GROUP=UNKNOWN
(no judge Google group is verifiable from this repository; must be supplied
by the human approver at authorization time)

JUDGE_ACCESS_BINDING=PROPOSED_NOT_APPLIED
IAP_ENABLED=NO
IAP_CONFIGURATION_STATUS=NOT_AUTHORIZED

This packet does not modify group membership, does not modify IAM, and does
not configure IAP.

Fallback if IAP proves infeasible in the window: Cloud Run invoker IAM bound
to the judge Google group only (still `PUBLIC_UNAUTHENTICATED_ACCESS=NO`).
Any fallback requires the same human signature; it is not self-selectable.

---

## Phase 5 — Minimal Judge Surface (proposed, not implemented)

Smallest deployable interface:

- `GET /health` — Cloud Run liveness/provenance; returns service name, version/commit,
  scenario catalog hash. No dynamic state. (`GET /healthz` retained as an optional
  local/container compatibility alias; exact-path `/healthz` may be reserved by the
  Google Front End and is not the external Cloud Run gate.)
- `POST /demo/meeting-follow-up` — accepts **only** a scenario selector
  bounded to a fixed synthetic catalog; runs the deterministic pipeline and
  returns the visible outputs below. **No arbitrary `run_id`, no arbitrary
  transcript, no arbitrary customer input** unless separately authorized.

Required visible outputs per demo response:

1. workflow status (final state from `contracts/workflow_states.yaml`)
2. contact/opportunity resolution outcome
3. follow-up proposal
4. deterministic policy decision (reason codes from the policy evaluator)
5. MG Guide card payload/view (mapper output + rendered card)
6. audit/provenance summary (in-memory, per-request; no persistence)

Explicitly excluded controls:

- No mutation controls.
- No CRM write button.
- No policy re-evaluation button.
- No arbitrary `run_id`.
- No arbitrary transcript/customer input.

NW-008 readiness scenarios (defined here, implemented in a later PR):

| Scenario | Source fixture family | Expected visible outcome |
| --- | --- | --- |
| SUCCESS | `fixtures/nw006/packets/packet-success.completed.json` | completed workflow, resolved contact+opportunity, follow-up proposal, approved policy decision, success card |
| STAGE_CHANGE_DENIED | `fixtures/nw006/packets/packet-stage-change-denied.completed_with_review.json` | completed_with_review, denied stage-change intent with policy reason codes, review card |
| AMBIGUOUS_CONTACT (optional third) | `fixtures/nw006/packets/packet-ambiguous-contact.blocked.json` | blocked workflow, ambiguous-contact resolution outcome, no mutation intents, blocked card |

---

## Phase 6 — Cost / Scale / Cleanup Bounds (proposed, not applied)

MIN_INSTANCES=0
MAX_INSTANCES=1
JUDGE_SURFACE_ONLY=YES
CONCURRENCY=low single-digit (finalize at implementation; bounded by
MAX_INSTANCES=1)
CPU_ALLOCATION=REQUEST_TIME_ONLY (no always-on CPU)

DEPLOYMENT_LIFETIME=COMPETITION_BOUNDED
POST_HACKATHON_CLEANUP_REQUIRED=YES
- delete the Cloud Run service
- delete the runtime service identity (if created)
- remove any judge IAM/IAP bindings (if applied)
- delete the Gemini API-key secret (if created under separate approval)
ROLLBACK_REQUIRED=YES
- rollback = delete the service; no traffic migration needed (single
  service, judge-only audience, scale-to-zero)

None of these settings are applied by this packet.

---

## Phase 7 — Authorization Decision Block

REQUESTED_DECISION=AUTHORIZED_FOR_NW007_DEPLOYMENT

REQUESTED_SCOPE=
- create/deploy one bounded Cloud Run judge service
  (`mg-guide-agentic-sales-workspace-judge`, `mg-devpost`, `us-east4`,
  min 0 / max 1 instances, request-time CPU)
- create/attach one dedicated runtime service identity if approved
  (`mg-guide-devpost-runtime@mg-devpost.iam.gserviceaccount.com`)
- grant only explicitly enumerated runtime permissions (default: none;
  Secret Manager accessor only if live-Gemini mode is separately approved)
- configure authenticated judge access (preferred: IAP + judge Google group)
  if approved
- execute bounded health and synthetic workflow smoke checks
  (`GET /health`, the defined SUCCESS and STAGE_CHANGE_DENIED scenarios)

NOT_REQUESTED:
- Firestore runtime writes
- GHL/CRM mutation
- production data
- broad project IAM
- service-account keys
- unrelated Secret Manager changes
- production promotion

CURRENT_DECISION=AWAITING_HUMAN_SIGNATURE
HUMAN_SIGNATURE=PENDING

STOP_CODE=NW007_CLOUD_RUN_JUDGE_SURFACE_AUTHORIZATION_READY_FOR_REVIEW
