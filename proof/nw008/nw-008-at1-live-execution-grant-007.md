# NW-008 AT-1 -- Live Execution Grant 007 (AUTHORIZED)

```text
GRANT_ID=NW008_AT1_LIVE_EXECUTION_007
GRANT_TYPE=ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION
ARTIFACT_KIND=ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION_GRANT
OWNER_LANE=VS Code / Orchestrator + Human GHL Space Owner
BRANCH=impl/nw008-at1-safe-environment-readiness

TRACK_A_CLOSEOUT_SHA=57f4fd390ba0705fb819a36028e6db02d4f1c09e
MERGED_AT1_EXECUTOR_SHA=998564cdfac6c24d5a414289798979a7f6220082
MERGED_EXECUTOR_MAIN_REACHABLE=YES
TRACK_B_FINAL_REVIEW_HEAD=835d86f64bd75b4983cf5e92f25b5fc7da439cc0
PR64_MERGE_SHA=a016b2040257a529d70951212033b604ae4c982f
AUTHORIZED_DRAFT_SHA=9051679699e981ce60aefb37716a470bb336b0a9

TARGET_LOCATION_CLASS=BUSINESS_ACTIVE_GHL_LOCATION
LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION_VERIFIED=YES
AUTHORIZED_RECORD_CLASS=SYNTHETIC_ONLY
NON_SYNTHETIC_RECORD_MUTATION_AUTHORIZED=NO

MODELED_GHL_READS=4
MODELED_GHL_WRITES=2
MODELED_TOTAL_GHL_CALLS=6

NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1

SEARCH=NO
LIST=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO
ALTERNATE_OPERATION=NO
COMPENSATING_MUTATION=NO

ENVIRONMENT_READY=YES
AT1_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_COMPLETE=NO

GRANT_STATE=AUTHORIZED_ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
SELF_ACTIVATION=FORBIDDEN
HUMAN_COUNTERSIGNATURE=APPROVED
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_APPROVER=THEMG@themiliare-group.com
APPROVED_AT_UTC=2026-08-17T11:38:17Z
EXPIRES_AT_UTC=2026-08-17T12:38:17Z
RECORDED_AT_UTC=2026-08-17T11:38:17Z
```

## Purpose

Authorize — for one shot only — the live AT-1 execution package for the synthetic
contact/opportunity on the business-active GHL location under the live-location
synthetic-only exception.

This countersigned grant:

1. Resolves the exact merged/reviewed bounded AT-1 executor SHA reachable from
   `origin/main`.
2. Confirms Track A `ENVIRONMENT_READY=YES` from closeout
   `57f4fd390ba0705fb819a36028e6db02d4f1c09e`.
3. Confirms the private execution package has all six AT-1 input-contract
   bindings/fingerprint inputs present.
4. Freezes one-shot caps, preconditions, write semantics, and public-proof rules.
5. Records the human countersignature that authorizes exactly one bounded live
   AT-1 attempt under those frozen caps.

```text
GRANT_STATE=AUTHORIZED_ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_COMPLETE=NO
GHL_CALLS_EXECUTED=0
MUTATION_CALLS_EXECUTED=0
```

## Continuity

1. Track A closeout
   (`57f4fd390ba0705fb819a36028e6db02d4f1c09e`) set
   `ENVIRONMENT_READY=YES` with `AT1_EXECUTION_AUTHORIZED=NO`.
2. Human final-stage correction bound
   `NW008_GHL_AUTHORIZED_FINAL_STAGE_PRIVATE_V1` as
   `ACTIVE_HUMAN_AUTHORIZED`.
3. Write-credential readiness recorded
   `contacts.write` + `opportunities.write` present with
   `create-note` / `update-opportunity` schemas available.
4. PR #64 merged the bounded AT-1 executor to `main`
   (`a016b2040257a529d70951212033b604ae4c982f`).
5. Hardened executor implementation subject retained as
   `998564cdfac6c24d5a414289798979a7f6220082` (ancestor of `origin/main`;
   file content matches `origin/main` and Track B head
   `835d86f64bd75b4983cf5e92f25b5fc7da439cc0`).
6. Draft Grant 007 package recorded at
   `9051679699e981ce60aefb37716a470bb336b0a9` and is the sole authorized draft
   subject of this countersignature.

No private identifier may be printed, committed, or otherwise published.

## Merged executor resolution

```text
MERGED_AT1_EXECUTOR_SHA=998564cdfac6c24d5a414289798979a7f6220082
MERGED_EXECUTOR_SUBJECT_PATH=src/integrations/ghl/bounded_at1_executor.py
MERGED_EXECUTOR_MAIN_REACHABLE=YES
ANCESTOR_CHECK=git merge-base --is-ancestor MERGED_AT1_EXECUTOR_SHA origin/main -> SUCCESS
```

Resolved executor contract (verified at the merged SHA):

```text
ORDER=get-contact,get-opportunity,create-note,get-note,update-opportunity,get-opportunity
MODELED_GHL_READS=4
MODELED_GHL_WRITES=2
MODELED_TOTAL_GHL_CALLS=6
NOTE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_RETRY=YES
NO_RAW_REST=YES
NO_ALTERNATE_OPERATION=YES
NO_COMPENSATING_MUTATION=YES
```

Input contract fields (values private only):

```text
location_id
contact_id
opportunity_id
expected_initial_stage_id
authorized_final_stage_id
expected_note_content_or_fingerprint
```

## Private execution package (presence only)

Verified privately; values are **not** published:

```text
PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
PRIVATE_LOCATION_BINDING_PRESENT=YES

PRIVATE_CONTACT_BINDING_REF=NW008_GHL_CONTACT_PRIVATE_V1
PRIVATE_CONTACT_BINDING_PRESENT=YES

PRIVATE_OPPORTUNITY_BINDING_REF=NW008_GHL_OPPORTUNITY_PRIVATE_V1
PRIVATE_OPPORTUNITY_BINDING_PRESENT=YES

PRIVATE_PIPELINE_BINDING_REF=NW008_GHL_PIPELINE_PRIVATE_V1
PRIVATE_PIPELINE_BINDING_PRESENT=YES

PRIVATE_EXPECTED_INITIAL_STAGE_BINDING_REF=NW008_GHL_EXPECTED_INITIAL_STAGE_PRIVATE_V1
PRIVATE_EXPECTED_INITIAL_STAGE_BINDING_PRESENT=YES

PRIVATE_AUTHORIZED_FINAL_STAGE_BINDING_REF=NW008_GHL_AUTHORIZED_FINAL_STAGE_PRIVATE_V1
PRIVATE_AUTHORIZED_FINAL_STAGE_BINDING_PRESENT=YES
PRIVATE_AUTHORIZED_FINAL_STAGE_STATUS=ACTIVE_HUMAN_AUTHORIZED

PRIVATE_EXPECTED_NOTE_BINDING_REF=NW008_GHL_EXPECTED_NOTE_PRIVATE_V1
EXPECTED_NOTE_CONTENT_OR_FINGERPRINT_PRESENT=YES

PRIVATE_BINDING_PUBLICATION=NO
```

Credential source (no PIT printed):

```text
DIRECT_GHL_SECRET_SOURCE=GCP_SECRET_MANAGER:GHL_MCP_PRIVATE_TOKEN
GCP_PROJECT=ai-rolodex-to-crm
EXECUTION_SURFACE=GHL_ANTHROPIC_V2_MCP
EXECUTION_ENDPOINT=https://services.leadconnectorhq.com/mcp/anthropic/v2
```

## Frozen one-shot caps

```text
MODELED_GHL_READS=4
MODELED_GHL_WRITES=2
MODELED_TOTAL_GHL_CALLS=6

NOTE_WRITE_ATTEMPTS_MAX=1
NOTE_WRITES_SUCCEEDED_MAX=1
STAGE_WRITE_ATTEMPTS_MAX=1
STAGE_WRITES_SUCCEEDED_MAX=1

SEARCH=NO
LIST=NO
PAGINATION=NO
RETRY=NO
RAW_REST_FALLBACK=NO
ALTERNATE_OPERATION=NO
COMPENSATING_MUTATION=NO
AUTOMATIC_CLEANUP=NO
```

Allowed operation order only:

```text
1.get-contact
2.get-opportunity
3.create-note
4.get-note
5.update-opportunity
6.get-opportunity
```

## Precondition semantics (before first write)

Fresh reads must prove all of the following before either write:

```text
contact binding exact
opportunity binding exact
live location exact
pipeline exact
contact/opportunity relationship exact
current stage == expected_initial_stage_id
```

If any mismatch:

```text
NOTE_WRITE_ATTEMPTS=0
STAGE_WRITE_ATTEMPTS=0
STOP
NO_WRITE
NO_RETRY
```

`EXPECTED_INITIAL_STAGE_VERIFIED` remains
`NO_PENDING_FRESH_PREEXECUTION_READ` until those precondition reads succeed under
an authorized execution window.

## Write semantics

### create-note

```text
ATTEMPTS_MAX=1
EXACT_EXPECTED_NOTE_CONTENT_OR_FINGERPRINT_REQUIRED=YES
```

### get-note

```text
EXACT_READBACK_REQUIRED=YES
```

If note write or note readback fails:

```text
STOP
NO_STAGE_WRITE
NO_RETRY
NO_COMPENSATING_MUTATION
```

### update-opportunity

```text
ATTEMPTS_MAX=1
STAGE_TARGET=exact authorized_final_stage_id only
ALTERNATE_STAGE=FORBIDDEN
```

### final get-opportunity

```text
EXACT_READBACK_REQUIRED=YES
REQUIRED_STAGE=authorized_final_stage_id
```

If stage write or final readback fails:

```text
STOP
NO_RETRY
NO_COMPENSATING_MUTATION
```

## Record-class boundary

```text
AUTHORIZED_RECORD_CLASS=SYNTHETIC_ONLY
NON_SYNTHETIC_RECORD_MUTATION_AUTHORIZED=NO
TARGET_LOCATION_CLASS=BUSINESS_ACTIVE_GHL_LOCATION
LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION_VERIFIED=YES
PRODUCTION_CUSTOMER_MUTATION=FORBIDDEN
```

## Proof destination

After this countersigned execution:

```text
RESULT_ARTIFACT=proof/nw008/nw-008-at1-live-execution-result-007.md
```

Public proof **must not** contain:

```text
contact ID
opportunity ID
location ID
pipeline ID
stage IDs
PIT / token material
raw GHL payload
protected customer data
```

Public proof may contain only sanitized counters, dispositions, fingerprints /
presence flags, and stop codes.

## Human countersignature (performed)

The human GHL space owner countersigns the draft at
`9051679699e981ce60aefb37716a470bb336b0a9` and authorizes exactly one live
synthetic AT-1 execution under the frozen caps above. Authorization expires 60
minutes after countersignature. A missing, expired, or ambiguous countersignature
means no external call is authorized.

```text
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_APPROVER=THEMG@themiliare-group.com
HUMAN_COUNTERSIGNATURE=APPROVED
APPROVED_AT_UTC=2026-08-17T11:38:17Z
EXPIRES_AT_UTC=2026-08-17T12:38:17Z
AUTHORIZED_DRAFT_SHA=9051679699e981ce60aefb37716a470bb336b0a9
GRANT_STATE=AUTHORIZED_ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_COMPLETE=NO
```

Required countersignature statement (inserted verbatim):

```text
I authorize one and only one live synthetic AT-1 execution under
NW008_AT1_LIVE_EXECUTION_007.

This authorization is bound to:

Grant 007 draft:
9051679699e981ce60aefb37716a470bb336b0a9

Track A closeout:
57f4fd390ba0705fb819a36028e6db02d4f1c09e

Merged bounded AT-1 executor:
998564cdfac6c24d5a414289798979a7f6220082

Live-location synthetic-only exception and the private execution
bindings referenced by Grant 007.

I authorize exactly the following operation order and no other
business operations:

1. get-contact
2. get-opportunity
3. create-note
4. get-note
5. update-opportunity
6. get-opportunity

I authorize at most one create-note dispatch attempt and at most
one update-opportunity dispatch attempt.

The first two reads must freshly verify the exact synthetic contact,
opportunity, live location, target pipeline, contact/opportunity
relationship, and expected initial stage before either write.

The note write must use only the privately frozen expected note
content/fingerprint.

The opportunity update must use only the privately bound,
human-authorized final stage.

I authorize no search, list, pagination, retry, alternate operation,
raw REST fallback, compensating mutation, or automatic cleanup.

No non-synthetic customer or prospect record may be mutated.

A failure or mismatch at any step is terminal and authorizes no
retry or unmodeled transport.

Public proof must not publish private IDs, the PIT, raw GHL payloads,
or protected customer data.

This authorization permits the bounded AT-1 attempt only. It does
not itself establish AT1_COMPLETE=YES; completion must be established
from the post-execution Result 007 proof.

APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
HUMAN_APPROVER=THEMG@themiliare-group.com
HUMAN_COUNTERSIGNATURE=APPROVED
APPROVED_AT_UTC=2026-08-17T11:38:17Z
EXPIRES_AT_UTC=2026-08-17T12:38:17Z

AUTHORIZED_DRAFT_SHA=
9051679699e981ce60aefb37716a470bb336b0a9

GRANT_STATE=
AUTHORIZED_ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION

OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_COMPLETE=NO
```

## Explicit non-actions prior to transport

```text
DID_NOT_EXECUTE_GET_CONTACT=YES
DID_NOT_EXECUTE_GET_OPPORTUNITY=YES
DID_NOT_EXECUTE_CREATE_NOTE=YES
DID_NOT_EXECUTE_GET_NOTE=YES
DID_NOT_EXECUTE_UPDATE_OPPORTUNITY=YES
DID_NOT_CALL_GHL_NETWORK=YES
DID_NOT_PRINT_PIT=YES
DID_NOT_PUBLISH_PRIVATE_BINDING_IDS=YES
DID_NOT_CLAIM_AT1_COMPLETE=YES
```

## STOP

```text
STOP_CODE=NW008_AT1_LIVE_EXECUTION_007_AUTHORIZED_AWAITING_ONE_SHOT_RUN
GRANT_STATE=AUTHORIZED_ONE_SHOT_LIVE_SYNTHETIC_AT1_EXECUTION
OPERATOR_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_EXECUTION_AUTHORIZED=YES_WITHIN_GRANT
AT1_COMPLETE=NO
ENVIRONMENT_READY=YES
MERGED_AT1_EXECUTOR_SHA=998564cdfac6c24d5a414289798979a7f6220082
MERGED_EXECUTOR_MAIN_REACHABLE=YES
AUTHORIZED_DRAFT_SHA=9051679699e981ce60aefb37716a470bb336b0a9
APPROVED_AT_UTC=2026-08-17T11:38:17Z
EXPIRES_AT_UTC=2026-08-17T12:38:17Z
PRIVATE_LOCATION_BINDING_PRESENT=YES
PRIVATE_CONTACT_BINDING_PRESENT=YES
PRIVATE_OPPORTUNITY_BINDING_PRESENT=YES
PRIVATE_EXPECTED_INITIAL_STAGE_BINDING_PRESENT=YES
PRIVATE_AUTHORIZED_FINAL_STAGE_BINDING_PRESENT=YES
EXPECTED_NOTE_CONTENT_OR_FINGERPRINT_PRESENT=YES
GHL_CALLS_EXECUTED=0
MUTATION_CALLS_EXECUTED=0
PRIVATE_BINDING_PUBLICATION=NO
NEXT=ONE_SHOT_BOUNDED_AT1_LIVE_EXECUTION_THEN_RESULT_007
```
