# NW-008 — Safe-Environment GHL Mutation Authorization Plan

```text
WORK_ITEM=NW-008
ARTIFACT=proof/nw008/nw-008-safe-env-ghl-mutation-authorization-plan.md
ACTION=CREATE
OWNER=VS_CODE_ORCHESTRATOR
STATUS=PLANNING_ONLY
DECISION=NOT_AUTHORIZED_FOR_GHL_EXECUTION
PRIMARY_TARGET=AT-1
RUNTIME_MUTATION=NO
GHL_EXECUTION_OCCURRED=NO
FIRESTORE_EXECUTION_OCCURRED=NO
```

## Purpose and boundary

This artifact designs a possible future bounded AT-1 GHL mutation grant. It is
not an execution grant and does not authorize discovery against live records,
GHL reads, GHL writes, Firestore access, deployment, IAM changes, secret
changes, or raw REST fallback.

Environment isolation is not inferred from synthetic record status. The
canonical GHL location is not classified as a test environment, so its
privately allowlisted synthetic records do not satisfy this plan's isolated
safe-environment requirement.

## Phase A — PR #60 closeout capture

`gh pr view 60 --repo themg-max/mg-guide-agentic-sales-workspace
--json state,mergeCommit,mergedAt,headRefOid` returned:

```text
PR60_STATE=MERGED
PR60_MERGED_AT=2026-08-16T14:43:08Z
PR60_HEAD_REF_OID=f80372e7d0f1e8fd010ba451a6aaed4fd8195b09
PR60_MERGE_SHA=986455107c7b830f188cd6216f650a4f2866c78c
```

The following current-state fields were verified in
`proof/nw008/nw-008-post-at10-acceptance-reconciliation.md` on
`origin/main` at the PR #60 merge:

```text
AT1_STATUS=BLOCKED
AT3_STATUS=BLOCKED
AT6_STATUS=BLOCKED
AT7_STATUS=BLOCKED
AT10_STATUS=COMPLETE
RECOMMENDED_NEXT_AT=AT-1
```

This plan does not alter those acceptance states.

## Initial authority state

```text
STATUS=PLANNING_ONLY
DECISION=NOT_AUTHORIZED_FOR_GHL_EXECUTION

PRIMARY_TARGET=AT-1

GHL_READS_AUTHORIZED=NO
GHL_WRITES_AUTHORIZED=NO
GHL_EXECUTION_AUTHORIZED=NO

REAL_CUSTOMER_DATA_AUTHORIZED=NO
RAW_REST_AUTHORIZED=NO
IAM_MUTATION_AUTHORIZED=NO
SECRET_MUTATION_AUTHORIZED=NO
DEPLOYMENT_AUTHORIZED=NO

FIRESTORE_EXECUTION_AUTHORIZED=NO
```

## Phase C — Repository-derived GHL surface

Discovery was limited to repository-owned contracts and adapters. No GHL
transport was invoked.

The repository's `contracts/ghl_tool_manifest.yaml` identifies the
`anthropic_v2` MCP surface and the unified `execute_operation` tool. The
AT-1-relevant operation IDs on that surface are:

```text
GHL_TOOL_SURFACE=anthropic_v2.execute_operation
GHL_OPERATIONS=get-contact,get-opportunity,get-pipelines,create-note,get-note,update-opportunity
```

The current `OfflineGhlReadAdapter` has no transport and is not an AT-1
executor. It allowlists `search-contacts-advanced`, `get-contact`,
`search-opportunity`, `search-opportunities-advanced`, and `get-pipelines`;
it explicitly denies `create-note`, `update-opportunity`, and
`update-opportunity-status`. It also does not implement the `get-note` or
`get-opportunity` mutation read-backs required by the manifest. A future
execution lane must implement and review those bounded paths rather than
repurpose the offline adapter or bypass it with raw REST.

The candidate sequence uses exact privately bound synthetic contact and
opportunity IDs. It deliberately excludes broad contact or opportunity search:

```text
AT1_EXPECTED_CALL_SEQUENCE=
  1. execute_operation:get-contact [READ; exact synthetic contact ID]
  2. execute_operation:get-opportunity [READ; exact synthetic opportunity ID; verify initial stage]
  3. execute_operation:get-pipelines [READ; resolve the bound pipeline stage IDs to exact stage names]
  4. execute_operation:create-note [WRITE; one note on the exact synthetic contact]
  5. execute_operation:get-note [READ-BACK; exact created note ID and exact body match]
  6. execute_operation:update-opportunity [WRITE; pipelineStageId only]
  7. execute_operation:get-opportunity [READ-BACK; exact opportunity ID and final stage match]
```

No pagination, retry, alternate operation, search expansion, or fallback call
is included. A missing, ambiguous, failed, or mismatched result must stop the
run without any additional GHL call.

## Phase D — Safe-environment requirements

Merged repository evidence states that no isolated GHL test location is
available and that the canonical GHL location is not a test environment. The
repository proves a synthetic contact only in that canonical location under a
private read-only allowlist; it does not prove a synthetic contact in an
isolated mutation-safe location.

```text
ISOLATED_GHL_TEST_LOCATION=NO
TEST_LOCATION_ID=NOT_PROVEN
PRODUCTION_LOCATION_EXCLUDED=YES

SYNTHETIC_CONTACT_AVAILABLE=NO
SYNTHETIC_CONTACT_ID=NOT_PROVEN_IN_AN_ISOLATED_TEST_LOCATION

EXPECTED_INITIAL_STAGE=discovery_scheduled
EXPECTED_FINAL_STAGE=discovery_complete

SAFE_ENV_READY=NO
AT1_EXECUTION_AUTHORIZABLE=NO
STOP=YES
```

`PRODUCTION_LOCATION_EXCLUDED=YES` is a design boundary, not evidence that an
alternative test location exists. Before a future authorization decision, a
human-controlled private binding must prove an isolated location, exact
synthetic contact and opportunity IDs in that location, the expected initial
stage, and the allowed final stage without publishing identifiers or secrets.

## Phase E — Candidate bounds, not authorization

The candidate budget is derived directly from the seven-step sequence above:
three pre-mutation reads, two mandatory mutation read-backs, and two writes.

```text
MAX_NOTE_CREATES=1
MAX_STAGE_TRANSITIONS=1
MAX_GHL_WRITES=2

MAX_GHL_READS=5
MAX_TOTAL_GHL_CALLS=7
```

| Candidate operation | Exact operation | Maximum calls | Effect |
| --- | --- | ---: | --- |
| Contact read | `execute_operation:get-contact` | 1 | Read |
| Initial pipeline/stage read | `execute_operation:get-opportunity` | 1 | Read |
| Pipeline/stage metadata read | `execute_operation:get-pipelines` | 1 | Read |
| Note create | `execute_operation:create-note` | 1 | Write |
| Note read-back | `execute_operation:get-note` | 1 | Read |
| Stage transition | `execute_operation:update-opportunity` | 1 | Write |
| Final stage read-back | `execute_operation:get-opportunity` | 1 | Read |

For `update-opportunity`, only `pipelineStageId` may change, and only for
`discovery_scheduled -> discovery_complete`. The
`update-opportunity-status` alternate is not a stage transition and is not
allowed.

Candidate operations remain unapproved until a separate human authorization
artifact binds the exact environment, records, implementation SHA, proof
destination, expiry, and one-shot counters.

Forbidden operations and data include:

- contact create or delete;
- opportunity create or delete;
- bulk operations;
- pipeline or stage create;
- tag mutation;
- custom-field mutation;
- status, monetary-value, or owner mutation;
- email, SMS, calendar, or workflow mutation;
- raw REST or a non-manifest fallback;
- broad contact or opportunity search;
- production locations, real customers, prospects, or other non-synthetic
  records;
- any call beyond the listed operation and per-operation caps.

## Phase F — Future AT-1 proof contract

A future execution proof must establish all of the following:

1. The isolated location and exact synthetic contact and opportunity were
   privately bound before execution.
2. The synthetic contact resolved exactly; no customer or prospect record was
   read.
3. The initial opportunity stage read back as `discovery_scheduled`.
4. Exactly one note create succeeded.
5. The created note ID was read back and its body exact-matched: `PASS`.
6. Exactly one authorized stage transition changed only `pipelineStageId` from
   `discovery_scheduled` to `discovery_complete`.
7. The final opportunity stage read-back exact-matched: `PASS`.
8. The final disposition was `completed`.
9. Audit evidence preserved the ordered calls, redacted identifiers, outcomes,
   reason codes, disposition, and counters.
10. No unauthorized tool call, retry, search, fallback, or transport occurred.
11. Every per-operation and aggregate counter remained within the grant.
12. Cleanup/restore was explicit. Under these candidate caps, the dedicated
    synthetic note and final stage remain in the disposable test location;
    deletion or a restoring stage transition is not authorized.
13. No real customer data was accessed.

This plan does not authorize a Firestore audit write. If the future proof
design requires Firestore persistence, that requires a separate bounded grant;
the GHL grant must not be treated as Firestore authority.

## Initial decision

```text
SAFE_ENV_READY=NO

AT1_EXECUTION_AUTHORIZABLE=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO

GHL_EXECUTION_OCCURRED=NO
FIRESTORE_EXECUTION_OCCURRED=NO

STOP_CODE=NW008_AT1_SAFE_ENV_GHL_AUTHORIZATION_PLAN_READY_FOR_REVIEW
```
