# NW-008 AT-1 -- Final Stage Human Disposition

```text
DECISION_ID=NW008_AT1_FINAL_STAGE_HUMAN_DISPOSITION_001
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
OWNER_LANE=Human GHL Space Owner + VS Code / Orchestrator
BRANCH=impl/nw008-at1-safe-environment-readiness
RESULT_006_SHA=84c863a1c62ed7f2d6900660e007110024096a7d
RECORDED_AT_UTC=2026-08-17T10:45:13Z
```

## Decision

The human GHL space owner supplied an authoritative final-stage selection for
AT-1. That human selection supersedes any prior algorithmic / heuristic final
stage choice recorded under Grant 006.

```text
HUMAN_FINAL_STAGE_SELECTION=APPROVED
HUMAN_FINAL_STAGE_SELECTION_COUNT=1
HUMAN_FINAL_STAGE_SELECTION_AUTHORITY=YES
AUTOMATED_FINAL_STAGE_SELECTION_AUTHORITY=NO
```

## Private name-to-id reconciliation (no network)

Grant 006 private target-pipeline stage evidence was loaded from the private
control plane / session-preserved Grant 006 catalog. The human-selected stage
name was matched by exact string equality only.

```text
PRIVATE_FINAL_STAGE_NAME_RECORDED=YES
NETWORK_REEXECUTION_REQUIRED=NO
GHL_CALLS_EXECUTED_FOR_THIS_CORRECTION=0
MUTATION_CALLS_EXECUTED=0
PRIVATE_BINDING_PUBLICATION=NO
```

Exact private mapping result:

```text
HUMAN_SELECTED_STAGE_NAME_MATCH_COUNT=0
PRIVATE_FINAL_STAGE_ID_BOUND=NO
FINAL_STAGE_DIFFERS_FROM_INITIAL_STAGE=NOT_EVALUATED_NO_UNIQUE_MATCH
AUTHORIZED_FINAL_STAGE_VERIFIED=NO
```

Because `HUMAN_SELECTED_STAGE_NAME_MATCH_COUNT != 1`, execution stopped
fail-closed:

```text
STOP_CODE=NW008_HUMAN_FINAL_STAGE_PRIVATE_MAPPING_NOT_UNIQUE
```

No guess was made among near-name stages. No GHL call was performed to search
or refresh stages. No raw stage identifier is published. Per public-proof
policy, the literal human-selected stage name is retained only in the private
control-plane disposition note and is not repeated here.

## Provenance handling for prior heuristic binding

Grant 006 previously bound a non-authoritative algorithmic final stage on the
private operator surface. That historical evidence is preserved privately and
explicitly superseded for AT-1. It is not treated as the authorized final stage.

```text
PRIOR_HEURISTIC_FINAL_STAGE_BINDING_PRESERVED=YES
PRIOR_HEURISTIC_FINAL_STAGE_AUTHORITY=NO
PRIOR_HEURISTIC_FINAL_STAGE_STATUS=SUPERSEDED_NON_AUTHORITATIVE_PENDING_HUMAN_REMAP
ACTIVE_AUTHORIZED_FINAL_STAGE_STATUS=UNBOUND_PENDING_HUMAN_NAME_MAPPING
```

## Authorization gates (unchanged / fail-closed)

```text
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
ENVIRONMENT_READY=NO
READ_ONLY_ENVIRONMENT_READY=NO
```

## Required human follow-up

Return for review with one of:

1. Confirm the exact stage name as it appears in the Grant 006 private target
   pipeline catalog (unique exact match required), or
2. Authorize a separate bounded read-only stage-catalog refresh grant if the
   intended stage exists only outside the already captured private catalog.

Do not authorize AT-1 execution from this disposition.

## STOP

```text
STOP_CODE=NW008_HUMAN_FINAL_STAGE_PRIVATE_MAPPING_NOT_UNIQUE
HUMAN_SELECTED_STAGE_NAME_MATCH_COUNT=0
PRIVATE_FINAL_STAGE_ID_BOUND=NO
AUTHORIZED_FINAL_STAGE_VERIFIED=NO
NETWORK_REEXECUTION_REQUIRED=NO
MUTATION_CALLS_EXECUTED=0
PRIVATE_BINDING_PUBLICATION=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
ENVIRONMENT_READY=NO
NEXT=HUMAN_FINAL_STAGE_NAME_REVIEW_OR_SEPARATE_CATALOG_REFRESH_GRANT
```
