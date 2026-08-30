# NW-008 AT1 GHL REST v3 Provider 403 Root-Cause Diagnostic 001

## 0. Artifact identity

```text
ARTIFACT_ID=
  NW008_AT1_GHL_REST_V3_PROVIDER_403_ROOT_CAUSE_DIAGNOSTIC_001
ARTIFACT_PATH=
  proof/nw008/nw-008-at1-ghl-rest-v3-provider-403-root-cause-diagnostic-001.md
CLASSIFICATION=ZERO_CALL_PRIVATE_ROOT_CAUSE_DIAGNOSTIC
PR_CLASS=proof_only
MODE=EXISTING_EVIDENCE_ONLY_NO_PROVIDER_CONTACT
OWNER=VS_CODE_MG_ORCHESTRATOR
REPOSITORY=themg-max/mg-guide-agentic-sales-workspace
RECORDED_AT_UTC=2026-08-30T00:00:00Z

GHL_REQUESTS_DURING_DIAGNOSTIC=0
GHL_REST_CALLS=0
MCP_CALLS=0
CRM_MUTATIONS=0
CRM_READS=0
SECRET_PAYLOAD_READS=0
SECRET_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0
RETRY_OF_EXECUTION_003=NO
```

This unit resolves the terminal HTTP 403 from Execution 003 using only merged
repository evidence and existing private configuration/provider-authority
records. It issues no HighLevel request, opens no socket, reads no secret
payload, and consumes no authority.

```text
MERGING_THIS_DIAGNOSTIC_CONFERS_PROVIDER_CALL_AUTHORITY=NO
MERGING_THIS_DIAGNOSTIC_CONFERS_SECRET_MUTATION_AUTHORITY=NO
MERGING_THIS_DIAGNOSTIC_CONFERS_ACTIVATION_AUTHORITY=NO
```

## 1. Authority state carried in

```text
PR_362_HEAD=efe832b766014cd0589f49e3932a7b3a7d311b75
PR_362_REVIEW_ID=5061777555
PR_362_FORMAL_VERDICT=CONTRADICTORY_EVIDENCE
PR_362_MERGE_ALLOWED=NO

AUTHORIZATION_002_REUSE_ALLOWED=NO
ACTIVATION_002_REUSE_ALLOWED=NO
CURRENT_SOURCE_OF_TRUTH=PR_365

EXECUTION_003_AUTHORITY_CONSUMED=YES
EXECUTION_003_AUTHORITY_REUSABLE=NO
```

Execution 003 terminal record
(`proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-execution-proof-003.md`):

```text
SECRET_ACCESS_RESULT=PASS
NOTE_RUNTIME_IMPERSONATION=PASS
HTTP_REQUEST_DISPATCHES=1
GHL_REST_CALLS=1
HTTP_STATUS=403
HTTP_2XX=NO
NO_RETRY=YES
CRM_MUTATIONS=0
```

## 2. Proven-healthy boundaries — not reopened

```text
WIF_PROVIDER=PASS
GITHUB_OIDC=PASS
WORKFLOW_IDENTITY=PASS
NOTE_RUNTIME_IMPERSONATION=PASS
EXPLICIT_CREDENTIAL_CLEANUP=PASS
SECRET_MANAGER_READINESS=PASS
SECRET_ACCESS=PASS

PRIVATE_BINDING_PRESENT=YES
CONTACT_ID_MATERIALIZED=YES
LOCATION_ID_MATERIALIZED=YES
LOCATION_ID_NON_PLACEHOLDER=YES
LOCATION_ID_SCALAR=YES
BINDING_READINESS=PASS

REOPENED_BY_THIS_DIAGNOSTIC=NONE
MODIFIED_BY_THIS_DIAGNOSTIC=NONE
```

None of the above was altered, re-derived, or weakened to explain the 403.

## 3. Evidence base (merged artifacts only)

```text
E1=proof/nw008/nw-008-at1-ghl-rest-v3-bounded-read-execution-proof-003.md
E2=proof/nw008/nw-008-at1-ghl-rest-v3-pit-subaccount-binding-validation-execution-proof-001.md
E3=proof/nw008/nw-008-at1-ghl-rest-v3-stage-provider-contract-validation-execution-proof-002.md
E4=proof/nw008/nw-008-at8-ghl-rest-exact-synthetic-contact-live-read-execution-002.md
E5=proof/nw008/nw-008-at1-ghl-credential-location-diagnostic-result-005.md
E6=proof/nw008/nw-008-at1-ghl-credential-location-reconciliation.md
E7=proof/nw008/nw-008-at1-write-credential-readiness.md
E8=proof/nw008/nw-008-at1-secret-manager-exact-access-execution-proof-001.md
E9=proof/nw008/nw-008-at1-secret-manager-readiness-reconciliation-proof-001.md
E10=proof/nw008/nw-008-at1-ghl-private-target-binding-readiness-proof-001.md
E11=proof/nw008/nw-008-fresh-private-binding-reconciliation-001.md
E12=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
E13=docs/nw008/nw-008-at8w15-ai-rolodex-backend-ghl-capability-reference-assessment-001.md
E14=proof/nw008/nw-008-at1-ghl-rest-v3-provider-error-evidence-remediation-001.md
E15=contracts/ghl_tool_manifest.yaml
E16=src/integrations/ghl/highlevel_rest/live_note_transport.py
E17=src/integrations/ghl/highlevel_rest/live_note_http_client.py
```

### 3.1 The complete provider-outcome ledger for the REST v3 path

| Attempt | Date UTC | Operation | Version header | Credential resource | Status |
| --- | --- | --- | --- | --- | --- |
| E3 CALL_1 | 2026-08-28 | `GET /opportunities/{private id}` | `v3` | `MG_GUIDE_PIT_GHL` v1 | `403` |
| E2 CALL_1 | 2026-08-29 | `GET /locations/{private id}` | `v3` | `MG_GUIDE_PIT_GHL` v1 | `403` |
| E1 (Exec 003) | 2026-08-30 | `GET /contacts/{private id}` | `v3` | `MG_GUIDE_PIT_GHL` v1 | `403` |
| E4 (AT-8 002) | earlier unit | `GET /contacts/{same private id}` | `v3` | **not** `MG_GUIDE_PIT_GHL` (see 5.2) | **`2xx`** |

```text
MG_GUIDE_PIT_GHL_PROVIDER_ATTEMPTS=3
MG_GUIDE_PIT_GHL_PROVIDER_SUCCESSES=0
MG_GUIDE_PIT_GHL_DISTINCT_ENDPOINT_FAMILIES_ATTEMPTED=3
MG_GUIDE_PIT_GHL_DISTINCT_ENDPOINT_FAMILIES_SUCCEEDED=0
```

Three unrelated endpoint families, three definitive 403s, zero successes. A
failure that is invariant across contacts, opportunities, and locations is not
an endpoint-, path-, or per-scope-level failure.

## 4. Required resolutions

```text
PIT_ACTIVE=UNKNOWN
PIT_BOUND_LOCATION_MATCH=UNKNOWN
PIT_CONTACT_READ_CAPABILITY=UNKNOWN

PIT_TOKEN_CLASS=
  DESIGNATED_LOCATION_SCOPED_HIGHLEVEL_PRIVATE_INTEGRATION_TOKEN_
  BEARER_REST_V3;
  ACTUAL_PAYLOAD_CLASS_UNVERIFIED

CONTACT_ENDPOINT_ALLOWED_FOR_TOKEN_CLASS=YES
AUTHORIZATION_SCHEME_MATCH=YES
VERSION_HEADER_CONTRACT_MATCH=YES
ENDPOINT_PATH_CONTRACT_MATCH=YES
EXPECTED_LOCATION_BINDING_MATCH=YES
```

### 4.1 `PIT_ACTIVE=UNKNOWN`

Secret Manager metadata proves resource health only, never provider-side
activation:

```text
SECRET_NAME=MG_GUIDE_PIT_GHL
SECRET_VERSION=1
SECRET_VERSION_STATE=ENABLED            # E9
SECRET_PAYLOAD_PRESENT=YES              # E8
SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN # E12
PROVIDER_SIDE_ACCEPTANCE_EVER_OBSERVED=NO
```

`ENABLED` + non-empty payload is a Secret Manager fact. It is not evidence that
the payload is an active HighLevel credential. E12 records this gap verbatim as
`LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN`.

### 4.2 `PIT_BOUND_LOCATION_MATCH=UNKNOWN`

E2 was purpose-built to answer exactly this question and could not:

```text
E2_QUESTION=DOES_MG_GUIDE_PIT_GHL_RESOLVE_THE_BOUND_LOCATION
E2_RESULT=HTTP_403_NO_LOCATION_ENVELOPE
PIT_TARGET_SUB_ACCOUNT_BINDING_MATCH=UNKNOWN
LOCATION_ENVELOPE_PRESENT=NOT_EVALUATED
```

Per PR285 semantics preserved in E2, a non-2xx never establishes a binding
mismatch. It remains `UNKNOWN`, not `NO`.

### 4.3 `PIT_CONTACT_READ_CAPABILITY=UNKNOWN`

Scope evidence exists but attaches to the **integration**, not to this secret's
payload:

```text
SCOPE_EVIDENCE_SOURCE=
  HUMAN_OWNER_CONSOLE_REVIEW_OF_MG_GUIDE_API_V2_PRIVATE_INTEGRATION   # E7
PRIVATE_INTEGRATION_NAME=MG_Guide
CONTACTS_READONLY_PRESENT=YES
CONTACTS_WRITE_PRESENT=YES
OPPORTUNITIES_READONLY_PRESENT=YES
OPPORTUNITIES_WRITE_PRESENT=YES
LOCATIONS_READONLY_PRESENT=YES
GHL_SCOPE_REMEDIATION_REQUIRED=NO                                     # E14

SCOPE_ATTESTATION_CREDENTIAL_SURFACE_AT_TIME_OF_REVIEW=
  GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN                            # E7
SCOPE_ATTESTATION_BINDS_TO_MG_GUIDE_PIT_GHL_PAYLOAD=NO
```

The scopes were verified against the MG_Guide private integration while the
recorded execution credential surface was `GHL_MCP_PRIVATE_TOKEN`. Nothing ties
that attestation to the payload of `MG_GUIDE_PIT_GHL` version 1. Capability of
the failing credential is therefore `UNKNOWN` — and, given 0/3, unlikely.

### 4.4 Request-contract predicates are all `YES` — proven by a prior success

E4 (AT-8 Live-Read Execution 002) dispatched exactly one HighLevel REST v3
request against the **same endpoint and the same private synthetic contact
binding** that Execution 003 later used:

```text
E4_METHOD=GET
E4_ROUTE=/contacts/{same exact private synthetic contact}
E4_EXACT_ROUTE_ONLY=YES
E4_QUERY_PARAMETERS_PRESENT=NO
E4_API_VERSION=v3
E4_EXPECTED_SCOPE=contacts.readonly
E4_AUTH_SCHEME=BEARER
E4_EXACT_CONTACT_GET_EXECUTED=YES
E4_CONTACT_ID_MATCH=YES
E4_LOCATION_ID_MATCH=YES
E4_LIVE_READ_VERIFIED=YES
E4_FAIL_CLOSED=NO
```

This single artifact discharges four predicates at once:

```text
VERSION_HEADER_CONTRACT_MATCH=YES
  # Version: v3 is provider-accepted on GET /contacts/{id}; it returned 2xx.

ENDPOINT_PATH_CONTRACT_MATCH=YES
  # The identical path shape and exact-ID route returned 2xx.

AUTHORIZATION_SCHEME_MATCH=YES
  # Bearer-prefixed PIT is the accepted scheme (E15 records that a raw PIT
  # without the Bearer prefix returns 401 invalid_token; E16 sends Bearer).

CONTACT_ENDPOINT_ALLOWED_FOR_TOKEN_CLASS=YES
  # A location-scoped HighLevel PIT with contacts.readonly is permitted to
  # read GET /contacts/{id}; E4 is the direct demonstration.
```

Execution 003 sent the frozen header set from E16:

```text
Authorization: Bearer <PIT>     # value never published
Version: v3
Accept: application/json
QUERY_PARAMETERS=NONE
REQUEST_BODY=NONE
allow_redirects=False
```

That set is byte-equivalent in contract terms to the one that succeeded in E4.
The request contract is therefore excluded as the cause.

### 4.5 `EXPECTED_LOCATION_BINDING_MATCH=YES`

Resolved privately by fingerprint correlation against already-published
fingerprints. No raw identifier was read out, printed, or written:

```text
TOKEN_ACCESSIBLE_LOCATION_FP=
  5e14ac52bf73156914fc2a017415561e619f76f911c9e509316825f39c5fd614   # E5
SUPERSEDED_NW008_GHL_LOCATION_PRIVATE_V1_FP=aa53db90f0dad317        # E5

CURRENT_PRIVATE_BINDING_LOCATION_FINGERPRINT=
  5e14ac52bf73156914fc2a017415561e619f76f911c9e509316825f39c5fd614   # E11
LOCATION_FP_MATCH_GRANT008_POST_CORRECTION=YES                       # E11

CURRENT_BINDING_EQUALS_TOKEN_ACCESSIBLE_LOCATION=YES
CURRENT_BINDING_EQUALS_SUPERSEDED_V1_LOCATION=NO
EXPECTED_LOCATION_BINDING_MATCH=YES
```

The August-17 location mismatch (`LOCATION_BINDING_MATCH=NO`, E5) was
remediated: the binding was moved onto the location that the working credential
demonstrably reads. That historical defect is closed and is **not** the cause of
the current 403.

## 5. Competing hypotheses — tested and excluded

### 5.1 Excluded: Cloudflare edge / non-browser User-Agent block

E15 records a real prior observation on this exact host:

```text
CF-05 (E15): "HTTP clients need browser-like User-Agent to avoid Cloudflare
1010 on services.leadconnectorhq.com."
OBSERVED_HISTORICALLY=PYTHON_URLLIB_403_ERROR_1010
```

E17 uses `urllib.request` and sets no `User-Agent`, so this hypothesis had a
genuine surface. It is nonetheless excluded by the recorded response evidence:

```text
E2_PROVIDER_CONTENT_TYPE_CLASS=JSON
E2_PROVIDER_ERROR_ENVELOPE_PRESENT=YES
E2_PROVIDER_ERROR_CODE_PRESENT=YES
E2_PROVIDER_ERROR_MESSAGE_PRESENT=YES
E1_RESPONSE_PARSEABLE=YES
E1_RESPONSE_BODY_LENGTH=718
```

A Cloudflare 1010 interstitial is an HTML document, not a JSON body carrying a
provider error code and message. E2's 403 was an application-layer HighLevel
response, which means this client's User-Agent reached HighLevel's application
layer rather than being stopped at the edge. Execution 003's 718-byte parseable
body is consistent with the same application-layer envelope, not an HTML block
page.

```text
CLOUDFLARE_EDGE_BLOCK_HYPOTHESIS=EXCLUDED
EXCLUSION_CONFIDENCE=MEDIUM_HIGH
EXCLUSION_BASIS=APPLICATION_LAYER_JSON_ERROR_ENVELOPE_OBSERVED
RESIDUAL=
  Execution 003 did not publish its own CONTENT_TYPE_CLASS; exclusion for that
  specific call is inferred from identical client, identical header set, and
  identical edge.
```

Note also `PROVIDER_CORRELATION_ID_PRESENT=YES` in E2 carries **no** diagnostic
weight: `cf-ray` is in the correlation-ID alias set in E16, and Cloudflare
fronts HighLevel on both success and failure paths.

### 5.2 Excluded: `Version: v3` is the wrong API version value

E13 records a genuine, merged discrepancy against the AI Rolodex reference
implementation:

```text
SOURCE_VERSION_HEADER_VALUE=2021-07-28
NW008_VERSION_HEADER_VALUE=v3
VERSION_HEADER_NAME_MATCH=YES
VERSION_HEADER_VALUE_MATCH=NO
```

This is excluded as the cause of the 403, on two independent grounds:

1. **Direct refutation.** E4 proves `Version: v3` returns 2xx on the exact
   failing endpoint with the exact failing target binding.
2. **Reference is not authority.** E13 itself records
   `PROVES_DEPLOYED_GHL_CONNECTIVITY=NO` for that source — it is a static
   capability reference, never a proven live call. E13 explicitly forbids the
   silent substitution and defers the question to a separate governed unit.

```text
VERSION_HEADER_HYPOTHESIS=EXCLUDED_AS_CAUSE_OF_403
VERSION_HEADER_DISCREPANCY_STILL_OPEN_AS_SEPARATE_CONTRACT_QUESTION=YES
CHANGING_VERSION_HEADER_TO_SOLVE_THIS_403=NOT_INDICATED
```

Changing the frozen version header here would be an unproven change to a
contract that has a recorded 2xx, made to chase a fault that lies elsewhere.

### 5.3 Excluded: missing HighLevel scopes

```text
GHL_SCOPE_REMEDIATION_REQUIRED=NO   # E14, human owner console review
```

Scope remediation was already ruled out by the human GHL space owner. Further,
a scope gap cannot produce a uniform 403 across contacts, opportunities, **and**
locations when the integration holds read scopes on all three.

### 5.4 Excluded: identity, impersonation, and secret-access plane

```text
GITHUB_OIDC=PASS
WORKFLOW_IDENTITY=PASS
NOTE_RUNTIME_IMPERSONATION=PASS
SECRET_ACCESS_RESULT=PASS
```

Execution 003 reached the provider and received a definitive application-layer
response. Everything upstream of the HighLevel authorization decision worked.

### 5.5 Excluded: private target binding

```text
BINDING_READINESS=PASS
CONTACT_LOCATION_SAME_INTENDED_SYNTHETIC_TARGET=YES      # E10
OPPORTUNITY_CONTACT_RELATION_BOUND=YES                   # E10
EXPECTED_LOCATION_BINDING_MATCH=YES                      # 4.5
E4_CONTACT_ID_MATCH=YES / E4_LOCATION_ID_MATCH=YES       # E4
```

E4 read that exact contact and confirmed both its identity and its location.
The target is real, reachable, and correctly bound.

### 5.6 Surviving hypothesis: the credential material itself

Every excluded hypothesis is a constant across the success and the failures.
Exactly one variable differs between E4 (2xx) and E1/E2/E3 (403 × 3):

```text
CREDENTIAL_RESOURCE_ON_ALL_FAILING_CALLS=
  projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1     # E1,E2,E3

CREDENTIAL_RESOURCE_ON_EVERY_PROVEN_SUCCESSFUL_HIGHLEVEL_INTERACTION=
  GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN (project ai-rolodex-to-crm)
  # E5 (get-opportunity HTTP 200), E7, and live results 006/007/008

TWO_RESOURCES_ARE_DISTINCT=YES                                  # E12
SEALED_FROM_HISTORICAL_MCP_ID=NO                                # E12
DEVPOST_SECRET_COPY_REQUIRED=NO                                 # E12
LIVE_NOTE_REST_SECRET_PAYLOAD_IDENTITY_VERIFIED=UNKNOWN         # E12
HISTORICAL_MCP_PIT_REUSABLE_FOR_REST=UNKNOWN                    # E12
```

E12 already names this gap as an open governed unknown and specifies the exact
evidence needed to close it:

> "Durable public proof, or a redacted operator attestation, naming which
> resource the AT8 REST v3 `GET /contacts/{id}` live-read actually used."

That evidence has never been produced. `MG_GUIDE_PIT_GHL` was created as a
*dedicated* REST resource, deliberately not sealed from the historical MCP
resource, and its payload was never validated against the provider before being
placed on the one-shot execution path.

## 6. Root cause

```text
ROOT_CAUSE_CLASS=CREDENTIAL_AUTHORIZATION_REJECTION

ROOT_CAUSE=
  MG_GUIDE_PIT_GHL_VERSION_1_CREDENTIAL_NOT_ACCEPTED_FOR_THE_BOUND_GHL_CONTACT_READ

ROOT_CAUSE_CONFIDENCE=HIGH

ROOT_CAUSE_DETAIL=
  THE_CREDENTIAL_MATERIAL_BOUND_TO_THE_REST_V3_PATH
  (projects/831270426395/secrets/MG_GUIDE_PIT_GHL/versions/1)
  IS_NOT_AN_ACCEPTED_HIGHLEVEL_AUTHORIZATION_FOR_THE_BOUND_LOCATION.
  ITS_PAYLOAD_IDENTITY_WAS_NEVER_VERIFIED_AGAINST_THE_PROVIDER,
  IT_IS_A_DISTINCT_RESOURCE_FROM_THE_CREDENTIAL_THAT_PRODUCED_EVERY
  PROVEN_SUCCESSFUL_HIGHLEVEL_INTERACTION,
  AND_IT_HAS_PRODUCED_ZERO_SUCCESSES_IN_THREE_DEFINITIVE_ATTEMPTS
  ACROSS_THREE_UNRELATED_ENDPOINT_FAMILIES.

ROOT_CAUSE_FAILING_COMPONENT=CREDENTIAL_MATERIAL
ROOT_CAUSE_NOT_REQUEST_CONTRACT=YES
ROOT_CAUSE_NOT_LOCATION_BINDING=YES
ROOT_CAUSE_NOT_IDENTITY_PLANE=YES
ROOT_CAUSE_NOT_SECRET_ACCESS_PLANE=YES
ROOT_CAUSE_NOT_SCOPE_CONFIGURATION=YES
ROOT_CAUSE_NOT_EDGE_WAF=YES
```

### 6.1 Why confidence is `high`

The conclusion is branch-independent. E12 leaves open which resource E4 used;
both branches land on the same failing component:

```text
BRANCH_A=E4_USED_GHL_MCP_PRIVATE_TOKEN
  => same endpoint, same version header, same target, different credential,
     opposite outcome. The credential is the differing variable.

BRANCH_B=E4_USED_MG_GUIDE_PIT_GHL
  => the same credential succeeded then and 403s now on three endpoint
     families. The credential has since ceased to be accepted.

BOTH_BRANCHES_IMPLICATE=CREDENTIAL_MATERIAL
BOTH_BRANCHES_SHARE_REPAIR_CLASS=YES
```

### 6.2 What remains `UNKNOWN` below the root cause

The failing component is exact. Its internal defect is not yet discriminated:

```text
SUB_CAUSE=UNKNOWN
SUB_CAUSE_CANDIDATES=
  PAYLOAD_IS_A_PIT_FOR_A_DIFFERENT_LOCATION_OR_SUB_ACCOUNT |
  PAYLOAD_IS_A_REVOKED_OR_SUPERSEDED_PIT |
  PAYLOAD_IS_A_TOKEN_OF_A_DIFFERENT_CLASS_OR_INTEGRATION |
  PAYLOAD_IS_MALFORMED_OR_A_PLACEHOLDER

SUB_CAUSE_CONFIDENCE=low
SUB_CAUSE_RESOLVABLE_WITHOUT_PROVIDER_CALL=YES_BY_OPERATOR_ATTESTATION
```

Discriminating the sub-cause is **not** a prerequisite for the repair: every
candidate is remediated by the same bounded operator action in section 7.

## 7. Repair

```text
REPAIR_REQUIRED=YES
REPAIR_CLASS=credential_permission
REPAIR_EXECUTED_BY_THIS_UNIT=NO
REPAIR_AUTHORIZED_BY_THIS_UNIT=NO
```

`credential_permission` is selected over `token_location_binding` because the
NW-008 side of the binding is proven correct (section 4.5) — the defect is in
the credential presented, not in the location the runtime targets. It is not
`request_contract` (section 5.2), and not `provider_configuration` (section
5.4).

### 7.1 Smallest bounded repair — operator lane, zero provider calls

```text
REPAIR_ID=
  NW008_AT1_GHL_REST_V3_CREDENTIAL_PAYLOAD_RECONCILIATION_001
REPAIR_OWNER=HUMAN_GHL_SPACE_OWNER + HUMAN_GCP_SECRET_OWNER
REPAIR_SURFACE=HIGHLEVEL_CONSOLE + GCP_SECRET_MANAGER
REPAIR_GHL_API_CALLS=0
REPAIR_CRM_MUTATIONS=0
```

Step 1 — attestation (no mutation, no payload publication):

```text
R1=Confirm in the HighLevel console that the MG_Guide API v2.0 Private
   Integration is ACTIVE and bound to the location whose SHA-256 fingerprint is
   5e14ac52bf73156914fc2a017415561e619f76f911c9e509316825f39c5fd614.
R2=Confirm contacts.readonly remains present on that integration.
R3=Attest, without publishing any token material, whether the payload currently
   stored in MG_GUIDE_PIT_GHL version 1 is that integration's PIT.
R3_OUTPUT=PIT_ACTIVE, PIT_BOUND_LOCATION_MATCH, PIT_CONTACT_READ_CAPABILITY
```

Step 2 — conditional, and only under a separate authorization:

```text
IF R3 = NO  -> add ONE new MG_GUIDE_PIT_GHL version containing the correct
               active MG_Guide PIT, then re-seal the runtime resource pointer
               to that exact version.
IF R3 = YES -> the stored PIT is the right integration but is not accepted;
               issue a fresh PIT on that integration and add ONE new version.

SECRET_MUTATION_REQUIRES_SEPARATE_AUTHORIZATION=YES
SECRET_VERSION_ADDS_MAX=1
SECRET_VERSIONS_DESTROYED=0
SECRET_VERSIONS_DISABLED=0
IAM_CHANGES=0
PIT_ROTATION_OF_GHL_MCP_PRIVATE_TOKEN=FORBIDDEN
REPOINTING_RUNTIME_TO_GHL_MCP_PRIVATE_TOKEN=FORBIDDEN   # E12 prohibition
VERSION_HEADER_EDIT=FORBIDDEN_IN_THIS_REPAIR
ENDPOINT_OR_ROUTE_EDIT=FORBIDDEN_IN_THIS_REPAIR
PRIVATE_BINDING_EDIT=FORBIDDEN_IN_THIS_REPAIR
```

The repair touches exactly one thing: the credential material. Nothing in the
proven-healthy set is modified.

### 7.2 Authorization boundary

```text
THIS_ARTIFACT_STOPS_AT=AUTHORIZATION_BOUNDARY
SECRET_MUTATION_PERFORMED=NO
CONSOLE_ACTION_PERFORMED=NO
NEXT_HUMAN_DECISION_REQUIRED=YES
```

Secret Manager version creation and HighLevel console changes are consequential
mutations requiring their own least-privilege authorization. This diagnostic
proposes; it does not execute.

## 8. Post-repair path (not authorized by this artifact)

Only after the repair lands with its own proof:

```text
CREATE=NW008_AT1_GHL_REST_V3_BOUNDED_READ_AUTHORIZATION_004
CREATE=NW008_AT1_GHL_REST_V3_BOUNDED_READ_HUMAN_ACTIVATION_004
CREATE=FRESH_RUN_ID
AUTHORIZATION_003_REUSE_ALLOWED=NO
ACTIVATION_003_REUSE_ALLOWED=NO
RUN_ID_003_REUSE_ALLOWED=NO

THEN=EXACTLY_ONE_NEW_GET
OPERATION=GET /contacts/{exact private synthetic contact}
HTTP_REQUEST_DISPATCHES_MAX=1
RETRY=FORBIDDEN
SEARCH=FORBIDDEN
LIST=FORBIDDEN
FALLBACK=FORBIDDEN
ALTERNATE_TARGET=FORBIDDEN
CRM_MUTATIONS_MAX=0

SUCCESS_GATES=
  HTTP_2XX=YES
  CONTACT_ID_MATCH=YES
  LOCATION_ID_MATCH=YES

ON_ALL_GATES_PASS=
  NEXT=AGENT_FLEET_SYNTHETIC_TRANSCRIPT_WRITE_ACCEPTANCE
ON_ANY_GATE_FAIL=
  TERMINAL_FAIL_CLOSED; NO_RETRY; FRESH_DIAGNOSTIC_REQUIRED
```

## 9. Incidental finding — disclosure hygiene (separate from the 403)

While resolving section 4.5 from private configuration, one merged public
artifact was found to contain a raw HighLevel location identifier in plaintext:

```text
LEAK_FILE=docs/nw008/nw-008-at8k-ghl-rest-live-note-runtime-construction-path-design-001.md
LEAK_LINE=344
LEAK_FIELD=GHL_LOCATION_ID
LEAK_VALUE_REPRODUCED_HERE=NO
LEAK_CORRELATES_TO_CURRENT_BOUND_LOCATION=YES
SEVERITY=MEDIUM
RELATED_TO_THE_403=NO
DISPOSITION=SEPARATE_REMEDIATION_UNIT_RECOMMENDED
```

This contradicts the `RAW_LOCATION_ID_PUBLISHED=NO` posture asserted across the
NW-008 proof set. It is recorded here so it is not lost; it is out of scope for
this diagnostic and is not remediated by this unit.

## 10. Disclosure boundary

```text
PIT_VALUE_PUBLISHED=NO
PIT_VALUE_READ=NO
ACCESS_TOKEN_PUBLISHED=NO
AUTHORIZATION_HEADER_PUBLISHED=NO
RAW_CONTACT_ID_PUBLISHED=NO
RAW_LOCATION_ID_PUBLISHED=NO
RAW_OPPORTUNITY_ID_PUBLISHED=NO
SECRET_PAYLOAD_READ=NO
SECRET_PAYLOAD_PUBLISHED=NO
PROVIDER_ERROR_MESSAGE_PUBLISHED=NO
PROVIDER_REQUEST_OR_CORRELATION_ID_PUBLISHED=NO
FULL_PROVIDER_RESPONSE_PUBLISHED=NO
```

Only fingerprints already published in merged NW-008 artifacts are restated.
The section 4.5 correlation was computed locally against an already-merged
value and only its boolean outcome is recorded.

## 11. Diagnostic result

```text
GHL_REQUESTS_DURING_DIAGNOSTIC=0
CRM_MUTATIONS=0

PIT_ACTIVE=UNKNOWN
PIT_BOUND_LOCATION_MATCH=UNKNOWN
PIT_CONTACT_READ_CAPABILITY=UNKNOWN
PIT_TOKEN_CLASS=
  DESIGNATED_LOCATION_SCOPED_HIGHLEVEL_PRIVATE_INTEGRATION_TOKEN_
  BEARER_REST_V3; ACTUAL_PAYLOAD_CLASS_UNVERIFIED
CONTACT_ENDPOINT_ALLOWED_FOR_TOKEN_CLASS=YES
AUTHORIZATION_SCHEME_MATCH=YES
VERSION_HEADER_CONTRACT_MATCH=YES
ENDPOINT_PATH_CONTRACT_MATCH=YES
EXPECTED_LOCATION_BINDING_MATCH=YES

ROOT_CAUSE_CLASS=CREDENTIAL_AUTHORIZATION_REJECTION
ROOT_CAUSE=
  MG_GUIDE_PIT_GHL_VERSION_1_CREDENTIAL_NOT_ACCEPTED_FOR_THE_BOUND_GHL_CONTACT_READ
ROOT_CAUSE_CONFIDENCE=HIGH
SUB_CAUSE=UNKNOWN

REPAIR_REQUIRED=YES
REPAIR_CLASS=credential_permission

STOP=AWAIT_HUMAN_CREDENTIAL_ATTESTATION_AND_SEPARATE_REPAIR_AUTHORIZATION
NEXT=
  REVIEW_AND_MERGE_THIS_DIAGNOSTIC
  THEN_NW008_AT1_GHL_REST_V3_CREDENTIAL_PAYLOAD_RECONCILIATION_001
  THEN_FRESH_AUTHORIZATION_004_AND_ACTIVATION_004
```

## 12. Stop

```text
STOP
NO_PROVIDER_CALL_MADE
NO_RETRY_OF_EXECUTION_003
NO_AUTHORITY_CONSUMED
NO_SECRET_MUTATED
NO_PROVEN_HEALTHY_BOUNDARY_MODIFIED
```
