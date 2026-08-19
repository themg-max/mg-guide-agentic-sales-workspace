# R4 — Version-47 Pinned Source Recovery (Read-Only)

```text
ARTIFACT=.ai/proof/addon-deployed-source-authority-readonly-live-20260818/r4-version47-pinned-source-recovery.md
UNIT=ADDON_DEPLOYED_SOURCE_AUTHORITY_READONLY_LIVE_R4
LANE=gov/addon-deployed-source-authority-readonly-live-002
OWNER=VS Code / operator
MODE=private_read_only_redacted_version_pinned_recovery
CREATED_AT_LOCAL=2026-08-18T20:59:29-04:00
CREATED_AT_UTC=2026-08-19T00:59:29Z
GOVERNANCE_GATE=PASS_WITH_GUARDS
PRIOR_R3=r3-deployed-source-provenance-reconciliation.md
ACTION=create (additive proof only)
MUTATION_AUTHORIZED=NO
RECONCILIATION_WRITE=NO
```

## 0. Mandatory preflight

### 0.1 Proof / governance worktree (artifact host)

```text
******
GIT_TOPLEVEL=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
ORIGIN=https://github.com/themg-max/mg-guide-agentic-sales-workspace.git
BRANCH=gov/addon-deployed-source-authority-readonly-live-002
BRANCH_IS_MAIN=NO
HEAD=9440ce09e9c9048df262dbb708f0aeceecd56d2f
WORKTREE_LANE_MATCH=YES
UNRELATED_MUTATIONS=NO
KNOWN_PROOF_ONLY_PATHS=
  .ai/proof/addon-deployed-source-authority-readonly-live-20260818/deployed-source-authority-live-evidence.md
  .ai/proof/addon-deployed-source-authority-readonly-live-20260818/r2-deployed-source-content-retrieval.md
  .ai/proof/addon-deployed-source-authority-readonly-live-20260818/r3-deployed-source-provenance-reconciliation.md
  .ai/proof/addon-deployed-source-authority-readonly-live-20260818/r4-version47-pinned-source-recovery.md
```

### 0.2 Bound add-on source repository (comparison basis; inspected read-only)

```text
SOURCE_PATH=/Users/achandler/A.I-Rolodex---Context
SOURCE_ORIGIN=https://github.com/themg-max/A.I-Rolodex---Context.git
SOURCE_REPO_IDENTITY=themg-max/A.I-Rolodex---Context
SOURCE_BRANCH=main
SOURCE_HEAD=9b689f1f85fdea0b8c2306cfe09886b0e6da652d
SOURCE_MUTATIONS_PERFORMED=NO
```

### 0.3 Preflight decision

```text
PROOF_LANE_PREFLIGHT=PASS
SOURCE_REPO_PREFLIGHT=PASS_FOR_READONLY_INSPECTION
STOP_CONDITIONS_HIT=NO
```

## 1. Known authority carried forward

```text
R1C_BINDING=PASS
BOUND_MARKETPLACE_VERSION=47
BOUND_SCRIPT_ID_SHA256_12=443d99b5b08b
PROJECT_TITLE=MG_GUIDE Workspace Add-on
DEPLOYMENT_UPDATE_TIME_V47=2025-09-30T00:49:46.065Z
R2_GETCONTENT_HEAD=PASS
R2_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
R2_HEAD_TO_REPO=DRIFT
R3_HEAD_TO_REPO_LINEAGE=PARTIAL
R3_VERSION47_TO_REPO_LINEAGE=UNRESOLVED
R3_MUTATION_COUNT=0
R3_NEXT_GATE=VERSION47_BYTE_RECOVERY_OR_EXPLICIT_HEAD_VS_V47_AUTHORITY_DECISION
```

## 2. Authorization boundary (R4)

### Authorized and performed

```text
OAUTH_TOKEN_REFRESH=YES          # local token.json only; scopes unchanged
API_projects.versions.list=YES   # read-only
API_projects.versions.get=YES    # version 47 metadata
API_projects.getContent=YES      # versionNumber=47 pinned + HEAD control
LOCAL_TEMP_CAPTURE=YES           # ~/.config/mg-guide-c2b/r4-private/ (mode 700/600)
DETERMINISTIC_SHA256=YES
REPO_COMPARISON_READONLY=YES
HISTORICAL_BLOB_HASH_SEARCH=YES
ADDITIVE_REDACTED_PROOF=YES
```

### Not authorized and not performed

```text
projects.updateContent=NO
versions.create=NO
deployment_create_update_delete=NO
clasp_push=NO
clasp_deploy=NO
clasp_pull_into_repo=NO
Marketplace_mutation=NO
OAuth_scope_changes=NO
IAM_IAP_changes=NO
token_output=NO
private_deployment_id_output=NO
private_script_id_output=NO
copy_private_source_into_repo=NO
runtime_routing_changes=NO
reconciliation_write=NO
API_WRITE_CALLS=0
R4_MUTATION_COUNT=0
```

OAuth scopes used (readonly only):

```text
https://www.googleapis.com/auth/script.projects.readonly
https://www.googleapis.com/auth/script.deployments.readonly
```

## 3. Version catalog confirmation

```text
VERSIONS_LIST=PASS
VERSION_COUNT_LISTED=58
MAX_VERSION_LISTED=61
VERSION_47_IN_LIST=YES
VERSIONS_GET_47=PASS
VERSION_47_CREATE_TIME=2025-09-30T00:49:45.738Z
NOTE=createTime aligns with bound deployment updateTime (~2025-09-30T00:49:46Z)
```

## 4. projects.getContent versionNumber=47

```text
R4_GETCONTENT_V47=PASS
HTTP_STATUS=200
GETCONTENT_SURFACE=projects.getContent?versionNumber=47
GETCONTENT_IS_VERSION_47_BYTES=YES
CONTENT_SCRIPT_ID_MATCH=YES
CONTENT_SCRIPT_ID_SHA256_12=443d99b5b08b
R4_FILE_COUNT=4
R4_SOURCE_DIGEST=f27bd8e6ad7dfcd262bb8a7dc470135451d0624e7898da969d8206e5f4a13aa5
R4_SOURCE_MANIFEST_DIGEST=6eab9d8361480a75a1e995348b96815addf15910597bfe43b8c247a29ac45bbf
DIGEST_METHOD=sha256 over length-prefixed UTF-8 blobs of (name\n type\n source) sorted by (name,type)
MANIFEST_METHOD=sha256 over sorted lines of name\0type\0file_sha256\n
```

### File inventory (names/types/digests only)

| Deployed name | Type | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `BrandedMeetingSummaries.gs` | SERVER_JS | 5738 | `f4851f8900835e3d91edfc8564e189606935272feb2a4f124c2565b897007063` |
| `Code` | SERVER_JS | 12882 | `a1d896f7d891060959915e52313d83e1df2dd298866d181eaed1f6e3f333d688` |
| `appsscript` | JSON | 2435 | `7abb65aa76e9e3b87b4259717455f43131af414a323ba39f95527ba5fbc72076` |
| `search-widget` | HTML | 740 | `0d17991610a7a16cdddf25069614965f991c69a14123c9f7776386e35fa18309` |

### Function-name inventory (no source bodies)

```text
v47 BrandedMeetingSummaries.gs:
  processRecentMeetingsAndAttachSummaries, createBrandedSummary, extractSection

v47 Code:
  onHomepage, onGmailContext, onCalendarEventOpen, buildAgentCard,
  callAgentService, clearChatHistory, createErrorCard

v47 sm-code:
  ABSENT_FROM_VERSION_47
```

Private capture location (not committed):

```text
~/.config/mg-guide-c2b/r4-private/getcontent-v47-raw.json
~/.config/mg-guide-c2b/r4-private/versions-list.json
~/.config/mg-guide-c2b/r4-private/versions-get-47.json
~/.config/mg-guide-c2b/r4-private/r4-result.json
~/.config/mg-guide-c2b/r4-private/files/   # operator-only extract
```

## 5. HEAD control (reconfirm R2; not version 47)

```text
R4_GETCONTENT_HEAD_CONTROL=PASS
HEAD_MATCHES_R2_DIGEST=YES
HEAD_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
HEAD_FILE_COUNT=5
V47_EQUALS_HEAD=NO
```

### Per-file V47 vs HEAD

| Name | Status | V47 SHA-256 (12) | HEAD SHA-256 (12) | V47 bytes | HEAD bytes |
| --- | --- | --- | --- | ---: | ---: |
| `BrandedMeetingSummaries.gs` | DIGEST_MISMATCH | `f4851f890083` | `40a536f14b25` | 5738 | 11531 |
| `Code` | DIGEST_MISMATCH | `a1d896f7d891` | `7f9d9f8aa99a` | 12882 | 10790 |
| `appsscript` | DIGEST_MISMATCH | `7abb65aa76e9` | `6652496d67ea` | 2435 | 2747 |
| `search-widget` | EXACT_MATCH | `0d17991610a7` | `0d17991610a7` | 740 | 740 |
| `sm-code` | ONLY_IN_HEAD | — | `b0974c69e6e0` | — | 2656 |

Interpretation: Marketplace-bound version **47** is a **distinct 4-file ensemble**
from current Apps Script HEAD (5 files). HEAD must not be treated as version 47.

## 6. V47 ↔ repo comparison (read-only, deterministic)

```text
COMPARISON_BASIS=clasp-root intended filenames in themg-max/A.I-Rolodex---Context main HEAD
                 vs Apps Script projects.getContent versionNumber=47
R4_V47_REPO_COMPARISON=DRIFT
EXACT_COUNT=1
DIGEST_MISMATCH_COUNT=2
MISSING_IN_REPO_COUNT=1
```

| Deployed name | Intended repo path | Status | V47 SHA-256 (12) | Repo SHA-256 (12) |
| --- | --- | --- | --- | --- |
| `BrandedMeetingSummaries.gs` | `BrandedMeetingSummaries.gs` | **MISSING_IN_REPO** | `f4851f890083` | — |
| `Code` | `Code.gs` | **DIGEST_MISMATCH** | `a1d896f7d891` | `363684ce6ffe` |
| `appsscript` | `appsscript.json` | **DIGEST_MISMATCH** | `7abb65aa76e9` | `2c7f981952a8` |
| `search-widget` | `search-widget.html` | **EXACT_MATCH** | `0d17991610a7` | `0d17991610a7` |

### Historical blob search (hash-only; no bodies printed)

```text
BrandedMeetingSummaries.gs  historical_blob_match=NO
Code                        historical_blob_match=NO
appsscript                  historical_blob_match=NO
search-widget               historical_blob_match=YES  match_commit=3381db2560fb
V47_ALL_HISTORICAL_EXACT_MATCH=NO
V47_ANY_HISTORICAL_EXACT_MATCH=YES (search-widget only)
```

## 7. Lineage determinations (R4 closes R3 unresolved item)

### 7.1 Version-47 bytes

```text
VERSION_47_BYTES=RECOVERED
VERSION_47_BYTES_SOURCE=projects.getContent?versionNumber=47
VERSION_47_API_VERSION_PINNED_FETCH_PERFORMED=YES
VERSION_47_FILE_COUNT=4
VERSION_47_SOURCE_DIGEST=f27bd8e6ad7dfcd262bb8a7dc470135451d0624e7898da969d8206e5f4a13aa5
VERSION_47_EQUALS_HEAD=NO
VERSION_47_CONTAINS_SM_CODE=NO
```

### 7.2 Version-47 ↔ repo lineage

```text
VERSION47_TO_REPO_LINEAGE=PARTIAL
VERSION47_TO_REPO_LINEAGE_DETAIL=
  search-widget              = HISTORICAL_REPO_MATCH (exact bytes)
  Code                       = RELATED_NON_IDENTICAL (digest mismatch vs Code.gs; no historical blob match)
  appsscript                 = RELATED_NON_IDENTICAL (digest mismatch; no historical blob match)
  BrandedMeetingSummaries.gs = OUT_OF_BAND_SOURCE (missing in repo; no historical blob match)
VERSION47_ENSEMBLE_EXACT_REPO_MATCH=NO
VERSION47_ENSEMBLE_PROVEN_AS_SINGLE_GIT_TREE=NO
```

Fail-closed rule retained for **ensemble authority**: version-47 bytes are now
known and digest-bound, but they are **not** reproduced by any scanned git tree
in `A.I-Rolodex---Context`. Partial lineage only.

### 7.3 HEAD vs V47 authority (fact statement only; no authority election)

```text
HEAD_VS_V47=DISTINCT
HEAD_FILE_COUNT=5
V47_FILE_COUNT=4
SM_CODE_PRESENT_IN=HEAD_ONLY
MARKETPLACE_BOUND_VERSION_REMAINS=47
NO_AUTHORITY_ELECTION_PERFORMED=YES
NO_RECONCILIATION_WRITE=YES
```

## 8. Required return block

```text
WORKTREE_IDENTITY=
  proof_repo=themg-max/mg-guide-agentic-sales-workspace
  proof_branch=gov/addon-deployed-source-authority-readonly-live-002
  proof_head=9440ce09e9c9048df262dbb708f0aeceecd56d2f
  source_repo=themg-max/A.I-Rolodex---Context
  source_branch=main
  source_head=9b689f1f85fdea0b8c2306cfe09886b0e6da652d
  source_path=/Users/achandler/A.I-Rolodex---Context

R1C_BINDING=PASS
BOUND_MARKETPLACE_VERSION=47

R4_GETCONTENT_V47=PASS
VERSION_47_BYTES=RECOVERED
R4_FILE_COUNT=4
R4_SOURCE_DIGEST=f27bd8e6ad7dfcd262bb8a7dc470135451d0624e7898da969d8206e5f4a13aa5
R4_SOURCE_MANIFEST_DIGEST=6eab9d8361480a75a1e995348b96815addf15910597bfe43b8c247a29ac45bbf

R4_HEAD_CONTROL=PASS
HEAD_MATCHES_R2_DIGEST=YES
V47_EQUALS_HEAD=NO

R4_V47_REPO_COMPARISON=DRIFT
VERSION47_TO_REPO_LINEAGE=PARTIAL
HEAD_TO_REPO_LINEAGE=PARTIAL (unchanged from R3)

R4_PRIVATE_IDS_PRINTED=NO
R4_TOKEN_VALUES_PRINTED=NO
R4_MUTATION_COUNT=0
API_WRITE_CALLS=0
PRIVATE_SOURCE_COPIED_TO_REPO=NO
RECONCILIATION_WRITE_PERFORMED=NO

R4_RESULT=PASS_RECOVERY_WITH_PARTIAL_REPO_LINEAGE
SOURCE_AUTHORITY_INVESTIGATION=CLOSED_FOR_COMPETITION
COMPETITION_DEMO_BLOCKED_BY_SOURCE_AUTHORITY=NO

BLOCKERS_FOR_RECONCILIATION_WRITE (informational; not entered)=
  1) Version-47 ensemble is not an exact historical git tree in A.I-Rolodex---Context.
  2) BrandedMeetingSummaries.gs remains out-of-band relative to durable repo history.
  3) Code/appsscript are related non-identical supersessions at intended clasp paths.
  4) HEAD (incl. sm-code) is distinct from Marketplace-bound version 47.
  5) No reconciliation mutation is authorized in this lane.

NEXT_GATE=COMPETITION_ACCEPTANCE (meeting_follow_up_v1 vertical slice)
NEXT_GATE_NOT_ENTERED=DEPLOYED_SOURCE_AUTHORITY_DECISION_AND_RECONCILIATION_PLAN
REASON_RECONCILIATION_NOT_ENTERED=
  R4 stop rule: record PASS/fail-closed recovery result and close source-authority
  investigation for the competition unless it directly blocks the demo.
  Source-authority drift does not block the synthetic meeting_follow_up_v1 demo.
```

## 9. Success / fail-closed check

```text
VERSION_47_PINNED_FETCH=PASS
VERSION_47_BYTES_DIGEST_BOUND=YES
DEFENSIBLE_VERSION47_BYTE_STATEMENT=YES
DEFENSIBLE_VERSION47_ENSEMBLE_REPO_LINEAGE=NO (partial only; fail-closed on ensemble match)
SOURCE_OR_DEPLOYMENT_MUTATION=NO
PRIVATE_SOURCE_COPIED_TO_REPO=NO
RECONCILIATION_WRITE_PERFORMED=NO
R4_RESULT=PASS_RECOVERY_WITH_PARTIAL_REPO_LINEAGE
SOURCE_AUTHORITY_CLOSED_FOR_COMPETITION=YES
```

## 10. Explicit non-actions (stop before reconciliation write)

R4 stops before any source reconciliation write. Not performed:

- no repo file creation/update outside this additive proof artifact
- no clasp pull/push/deploy
- no Apps Script content or deployment mutation
- no Marketplace mutation
- no promotion of HEAD as version-47 authority
- no promotion of version-47 as reconciled repo authority
- no copy of private source into either repository
- no runtime routing changes

## 11. Competition handoff

```text
SOURCE_AUTHORITY_INVESTIGATION=CLOSED
COMPETITION_PRIORITY_SHIFT=YES
HERO_WORKFLOW=meeting_follow_up_v1
DEMO_DEPENDENCY_ON_ADDON_SOURCE_RECONCILIATION=NO
NEXT=cloud acceptance / Gemini+ADK proof / e2e SUCCESS+FAIL-CLOSED scenarios
```

---

END R4
