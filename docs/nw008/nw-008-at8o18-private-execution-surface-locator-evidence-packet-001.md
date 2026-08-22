# NW-008 AT-8O18 - Private Execution-Surface Locator Evidence Packet 001

```text
UNIT=NW008_AT8O18_PRIVATE_EXECUTION_SURFACE_LOCATOR_EVIDENCE_PACKET_001
PR_CLASS=planning_only
MODE=PRIVATE_EXECUTION_SURFACE_LOCATOR_EVIDENCE_ONLY
ARTIFACT_OWNER=VS_CODE_ORCHESTRATOR

PREDECESSOR_UNIT=
NW008_AT8O17_PRIVATE_EXECUTION_SURFACE_METADATA_INSPECTION_EXECUTION_PACKET_001

PREDECESSOR_REVIEWED_HEAD=
079658a29b1682f606582d9d913950eaf7e60354

PREDECESSOR_MERGE_COMMIT=
3c8c5f462a2a7ac2d0d4152579f60118808f4021

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0

EXECUTION_SURFACE_LOCATOR_FOUND=NO
PACKET_DISPOSITION=FAIL_CLOSED_LOCATOR_NOT_PROVEN
STOP_FOR_GOVERNANCE_REVIEW=YES
```

## 1. Purpose and evidence boundary

AT8O18 searches only permitted non-dispatch evidence for an exact,
connector-safe locator for the private execution-surface metadata/schema
interface and operation. It does not request an AT8O16 metadata field from a
private interface and does not invoke a private data operation.

The packet is limited to identifying:

```text
CONNECTOR_OR_INTERFACE_SAFE_ALIAS
OPERATION_SAFE_ALIAS
SOURCE_CLASS
SCHEMA_OR_DESCRIPTOR_LOCATION
METADATA_PLANE_VS_DATA_PLANE_BOUNDARY
LOCATOR_SOURCE_AUTHORITY
```

No other private metadata, schema fact, record value, principal, credential,
access policy, or operational detail is sought or returned.

## 2. Permitted evidence surfaces used

| Evidence surface | Read-only method | Result |
| --- | --- | --- |
| Merged MG Guide repository artifacts | Tracked-tree content search at `origin/main` containing predecessor merge `3c8c5f462a2a7ac2d0d4152579f60118808f4021` | AT8O15-AT8O17 define requested aliases and authority boundaries but no concrete locator value. |
| Merged repository history | `git log origin/main -S` for `connector_or_interface_safe_alias` and `operation_safe_alias` | Only AT8O15, AT8O16, and AT8O17 introduced or repeated the field names; none supplies a locator value. |
| GitHub repository source review | Read-only code search of `themg-max/mg-guide-agentic-sales-workspace` | Exact alias-field searches returned only AT8O15, AT8O16, and AT8O17. |
| Merged MG MCP repo-review record | AT8O9 lines 130-150 | Recorded read-only searches returned zero results for the earlier exact-retrieval locator/contract queries; absence inference is explicitly forbidden. |
| Merged MG MCP approved-docs record | AT8O9 lines 139-150 and AT8O10 lines 59-73 | The recorded approved-docs search returned zero results for the earlier exact-retrieval contract query; no live MG MCP query is represented by AT8O18. |
| Merged decision history | AT8O3, AT8O10, AT8O16, and AT8O17 | Establishes policy and authority classes, not a concrete connector/interface or operation locator. |
| Already-approved/public connector documentation | Public repository documentation and tracked contracts | Public GHL and repository schemas describe other authorized surfaces; none is evidenced as the AT8O16 private execution-surface metadata/schema interface. |

No MG MCP interface is exposed to this AT8O18 orchestrator session. AT8O18
therefore relies only on the merged record of prior read-only MG MCP searches
and does not claim a new MG MCP repo, approved-docs, or decision-history query.

## 3. Evidence observations

### 3.1 Source class

The AT8O16 authorization directly identifies the authorized source class:

```text
SOURCE_CLASS=PRIVATE_EXECUTION_SURFACE_METADATA
SOURCE_CLASS_PROVEN=YES
SOURCE_CLASS_EVIDENCE_AUTHORITY=AT8O16_MERGED_AUTHORIZATION_DECISION
```

This proves the authorized class only. It does not identify a concrete
interface, operation, resource, endpoint, descriptor, or owner.

### 3.2 Public/private boundary

The merged public/private boundary establishes that the private control plane
retains governance source authority and non-public operational detail. It also
forbids internal-only service endpoints and private control-plane paths from
this public repository.

```text
PRIVATE_CONTROL_PLANE_CLASS_EXISTS=YES
PRIVATE_CONTROL_PLANE_CONCRETE_IDENTIFIER=NOT_SURFACED
PUBLIC_REPOSITORY_MAY_DISCLOSE_INTERNAL_ONLY_ENDPOINT=NO
PUBLIC_REPOSITORY_MAY_DISCLOSE_PRIVATE_CONTROL_PLANE_PATH=NO
```

The policy boundary is not a locator. It explains why a concrete private
locator may legitimately be absent from public artifacts.

### 3.3 MG MCP role evidence

Merged governance evidence identifies MG MCP as a read-only organizational
context/retrieval surface when separately authorized. AT8O3 and AT8O10
explicitly leave private authority-index capability, concrete resource,
runtime interface, and private retrieval model unresolved.

```text
MG_MCP_ROLE_CLASS_IDENTIFIED=YES
MG_MCP_EXACT_AT8O16_CONNECTOR_IDENTIFIED=NO
MG_MCP_EXACT_AT8O16_OPERATION_IDENTIFIED=NO
MG_MCP_EXACT_AT8O16_DESCRIPTOR_LOCATION_IDENTIFIED=NO
```

MG MCP's general role cannot be promoted into the exact AT8O16 locator without
reviewable connector and operation evidence.

### 3.4 Public connector documentation

The repository contains public HighLevel/GHL contracts and implementation
documentation, but AT8O16 forbids HighLevel calls and authorizes
`PRIVATE_EXECUTION_SURFACE_METADATA`, not the CRM data plane. No merged
authority artifact binds a public HighLevel operation to the AT8O16 inspection.

```text
PUBLIC_HIGHLEVEL_CONNECTOR_IS_AT8O16_LOCATOR=NOT_PROVEN
PUBLIC_REPOSITORY_SCHEMA_IS_AT8O16_PRIVATE_DESCRIPTOR=NOT_PROVEN
```

AT8O18 does not infer a private locator from an unrelated public connector.

## 4. Exact locator result

```text
CONNECTOR_OR_INTERFACE_SAFE_ALIAS=NOT_PROVEN
OPERATION_SAFE_ALIAS=NOT_PROVEN
SOURCE_CLASS=PRIVATE_EXECUTION_SURFACE_METADATA
SCHEMA_OR_DESCRIPTOR_LOCATION=NOT_PROVEN
METADATA_PLANE_VS_DATA_PLANE_BOUNDARY=NOT_PROVEN
LOCATOR_SOURCE_AUTHORITY=NOT_PROVEN

EXECUTION_SURFACE_LOCATOR_FOUND=NO
PACKET_DISPOSITION=FAIL_CLOSED_LOCATOR_NOT_PROVEN
```

`METADATA_PLANE_VS_DATA_PLANE_BOUNDARY=NOT_PROVEN` means the policy distinction
is known, but no exact connector contract proves how the concrete interface
enforces that distinction.

`LOCATOR_SOURCE_AUTHORITY=NOT_PROVEN` means no authoritative source for an exact
safe locator was surfaced. It does not mean that no authoritative locator
source exists.

## 5. Locator acceptance rule

`EXECUTION_SURFACE_LOCATOR_FOUND=YES` would require one reviewable evidence
chain that supplies all of the following without private inspection dispatch:

1. a connector-safe, non-principal, non-secret interface alias;
2. an operation-safe, non-principal, non-secret operation alias;
3. the authorized source class;
4. a connector-safe schema or descriptor location;
5. an explicit metadata-plane versus private-data-plane separation; and
6. the source authority governing those locator facts.

The evidence must also establish that reading the descriptor does not invoke a
private data operation or request any AT8O16 metadata field from the private
interface. No permitted evidence chain satisfies these requirements in AT8O18.

## 6. Fail-closed interpretation

```text
LOCATOR_ABSENCE_INFERRED=NO
PRIVATE_INTERFACE_NONEXISTENCE_INFERRED=NO
BROADER_AUTHORITY_AUTOMATICALLY_REQUESTED=NO
```

The result is a discoverability conclusion only. It does not establish that the
locator, interface, operation, or descriptor does not exist. AT8O18 does not
automatically request broader authority.

Because the exact locator is not proven, no AT8O16 dispatch can be safely
prepared from this packet.

## 7. Preserved authorization state

```text
AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO
```

Repository searches, history review, and review of already-merged evidence do
not meet either authorization's dispatch definition.

## 8. Hard blocks and non-actions

```text
AT8O16_INSPECTION_DISPATCH=BLOCKED
AT8O12_INSPECTION_DISPATCH=BLOCKED
PRIVATE_DATA_OPERATION_INVOCATION=BLOCKED
AUTHORITY_RECORD_VALUE_RETRIEVAL=BLOCKED
EXACT_PRINCIPAL_LOOKUP=BLOCKED
ADC_INSPECTION=BLOCKED
IAM_INSPECTION_OR_MUTATION=BLOCKED
SERVICE_ACCOUNT_IMPERSONATION=BLOCKED
MG_MCP_MUTATION=BLOCKED
HIGHLEVEL_CALL=BLOCKED
CRM_MUTATION=BLOCKED

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
```

No deployment, Token Creator authorization, credential access, secret access,
private descriptor request, or private source probe is performed.

## 9. Validation and stop state

Only this AT8O18 artifact may be staged:

```text
git diff --check
PYTHONPATH=src .venv/bin/python scripts/verify_phase1_deterministic.py
```

```text
ARTIFACTS_CHANGED=1
ARTIFACT_PATH=docs/nw008/nw-008-at8o18-private-execution-surface-locator-evidence-packet-001.md
SRC_CHANGES=0
TEST_CHANGES=0
WORKFLOW_CHANGES=0
DEPLOY_OR_INFRA_CHANGES=0

EXECUTION_SURFACE_LOCATOR_FOUND=NO
PACKET_DISPOSITION=FAIL_CLOSED_LOCATOR_NOT_PROVEN

AT8O16_AUTHORIZATION_STATE=AVAILABLE
AT8O16_INSPECTION_ATTEMPTS_USED=0
AT8O16_INSPECTION_DISPATCHED=NO

AT8O12_AUTHORIZATION_STATE=AVAILABLE
AT8O12_INSPECTION_ATTEMPTS_USED=0
ORIGINAL_AT8O12_INSPECTION_DISPATCHED=NO

IMPLEMENTATION_PERFORMED=NO
EXTERNAL_EFFECTS=0
STOP_FOR_GOVERNANCE_REVIEW=YES
```

AT8O18 stops for governance review without dispatch, mutation, or authority
consumption.
