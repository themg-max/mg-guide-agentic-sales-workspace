# R2 — Deployed Source Content Retrieval (Read-Only)

```text
ARTIFACT=.ai/proof/addon-deployed-source-authority-readonly-live-20260818/r2-deployed-source-content-retrieval.md
UNIT=ADDON_DEPLOYED_SOURCE_AUTHORITY_READONLY_LIVE_R2
LANE=gov/addon-deployed-source-authority-readonly-live-002
OWNER=VS Code / operator
MODE=private_read_only_redacted
CREATED_AT_LOCAL=2026-08-18T19:49:45-04:00
CREATED_AT_UTC=2026-08-18T23:49:45Z
GOVERNANCE_GATE=PASS_WITH_GUARDS
R1C_BINDING_REVIEW=APPROVE
```

## 0. Mandatory preflight

```text
PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
BRANCH=gov/addon-deployed-source-authority-readonly-live-002
BRANCH_IS_MAIN=NO
WORKTREE_LANE_MATCH=YES
UNRELATED_CHANGES=NO
KNOWN_PROOF_ONLY=YES
  - .ai/proof/addon-deployed-source-authority-readonly-live-20260818/deployed-source-authority-live-evidence.md
  - .ai/proof/addon-deployed-source-authority-readonly-live-20260818/r2-deployed-source-content-retrieval.md
```

## 1. R1c binding gate (re-verified, redacted)

Operator-supplied R1c binding review markers were re-checked against private
local captures under `~/.config/mg-guide-c2b/` **without printing private IDs**.

```text
C2B_R1C_DEPLOYMENT_MATCH_COUNT=1
C2B_R1C_MATCHED_APPS_SCRIPT_R1=YES
C2B_R1C_MATCHED_VERSION_NUMBER=47
ADDON_SOURCE_AUTHORITY_BINDING_RESOLVED=YES
PRIVATE_DEPLOYMENT_ID_PRINTED=NO
MARKETPLACE_DEPLOYMENT_ID_NONEMPTY=YES
MARKETPLACE_ID_EQUALS_MATCHED_DEPLOYMENT=YES
MARKETPLACE_ID_SHA256_12=8b9178b9f536
BOUND_SCRIPT_ID_SHA256_12=443d99b5b08b
BOUND_SCRIPT_ID_LEN=57
PROJECT_TITLE=MG_GUIDE Workspace Add-on
DEPLOYMENT_UPDATE_TIME=2025-09-30T00:49:46.065Z
MANIFEST_FILE_NAME=appsscript
ENTRY_POINT_TYPE=ADD_ON
```

Gate decision: **PROCEED** (markers exact: `MATCH_COUNT=1`, `APPS_SCRIPT_R1=YES`, `VERSION=47`).

## 2. Authorization boundary

### Authorized and performed

```text
OAUTH_TOKEN_REFRESH=YES          # local token.json only; scopes unchanged
API_projects.get=YES             # read-only project metadata
API_projects.getContent=YES      # read-only HEAD source content
LOCAL_TEMP_CAPTURE=YES           # ~/.config/mg-guide-c2b/r2-private/ (mode 700/600)
FILE_INVENTORY=YES
DETERMINISTIC_SHA256=YES
REPO_COMPARISON_READONLY=YES
ADDITIVE_REDACTED_PROOF=YES
```

### Not authorized and not performed

```text
projects.updateContent=NO
deployment_create_update_delete=NO
clasp_push=NO
clasp_deploy=NO
Marketplace_mutation=NO
OAuth_scope_changes=NO
IAM_IAP_changes=NO
token_output=NO
private_deployment_id_output=NO
runtime_routing_changes=NO
reconciliation_write=NO
API_WRITE_CALLS=0
R2_MUTATION_COUNT=0
```

OAuth scopes used (readonly only):

```text
https://www.googleapis.com/auth/script.projects.readonly
https://www.googleapis.com/auth/script.deployments.readonly
```

## 3. Project identity match

Bound Apps Script `scriptId` (from R1a matched deployment config) was compared
to the clasp binding in the intended source repository checkout
`themg-max/A.I-Rolodex---Context` (local path, branch `main`,
HEAD `9b689f1f85fdea0b8c2306cfe09886b0e6da652d`) using SHA-256 prefixes only.

```text
R2_PROJECT_IDENTITY_MATCH=YES
CLASP_SCRIPT_ID_SHA256_12=443d99b5b08b
BOUND_SCRIPT_ID_SHA256_12=443d99b5b08b
CONTENT_SCRIPT_ID_MATCHES_BOUND=YES
PROJECT_CREATE_TIME=2025-08-27T22:52:45.762Z
PROJECT_HEAD_UPDATE_TIME=2025-12-18T15:10:04.198Z
```

## 4. projects.getContent result

```text
R2_GETCONTENT=PASS
HTTP_STATUS=200
GETCONTENT_SURFACE=projects.getContent (current project HEAD content)
NOTE=Apps Script API getContent returns HEAD project files, not a version-pinned snapshot.
BOUND_DEPLOYMENT_VERSION=47
HEAD_AFTER_BOUND_VERSION=YES
  deployment_updateTime=2025-09-30T00:49:46.065Z
  project_head_updateTime=2025-12-18T15:10:04.198Z
```

### File inventory (names/types/digests only)

```text
R2_FILE_COUNT=5
```

| Deployed name | Type | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `BrandedMeetingSummaries.gs` | SERVER_JS | 11531 | `40a536f14b253c163d992c3f015d2d7501547421d2cb028d6fbc01ecfd55a3e4` |
| `Code` | SERVER_JS | 10790 | `7f9d9f8aa99abdd5ba9ef3bdbc932eab6350f26f6557415b5ca8f82d742d84dd` |
| `appsscript` | JSON | 2747 | `6652496d67ea02314d96f01f7272aabb9cbf3214f4edb56e857833c89dedb26b` |
| `search-widget` | HTML | 740 | `0d17991610a7a16cdddf25069614965f991c69a14123c9f7776386e35fa18309` |
| `sm-code` | SERVER_JS | 2656 | `b0974c69e6e02cfdaa79d59a8e5998af095dfdf964fc960c89a5b2d88be9f9ed` |

### Aggregate source digests (deterministic)

```text
R2_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
DIGEST_METHOD=sha256 over length-prefixed UTF-8 blobs of (name\\n type\\n source) sorted by (name,type)
R2_SOURCE_MANIFEST_DIGEST=50b5556bf68974d43ef04c7e142b7ba5bc590ac96ac40bdba5438599eecd0158
MANIFEST_METHOD=sha256 over sorted lines of name\\0type\\0file_sha256\\n
```

Private capture location (not committed):

```text
~/.config/mg-guide-c2b/r2-private/getcontent-raw.json
~/.config/mg-guide-c2b/r2-private/inventory.json
~/.config/mg-guide-c2b/r2-private/comparison.json
~/.config/mg-guide-c2b/r2-private/files/   # local extract for operator only
```

## 5. Repo comparison (read-only, deterministic)

```text
COMPARISON_BASIS=clasp-root intended filenames in themg-max/A.I-Rolodex---Context main HEAD
                 vs Apps Script projects.getContent HEAD
R2_REPO_COMPARISON=DRIFT
EXACT_COUNT=1
DIGEST_MISMATCH_COUNT=2
MISSING_IN_REPO_COUNT=2
```

### Per-file comparison

| Deployed name | Intended repo path | Status | Deployed SHA-256 (12) | Repo SHA-256 (12) |
| --- | --- | --- | --- | --- |
| `BrandedMeetingSummaries.gs` | `BrandedMeetingSummaries.gs` | **MISSING_IN_REPO** | `40a536f14b25` | — |
| `Code` | `Code.gs` | **DIGEST_MISMATCH** | `7f9d9f8aa99a` | `363684ce6ffe` |
| `appsscript` | `appsscript.json` | **DIGEST_MISMATCH** | `6652496d67ea` | `2c7f981952a8` |
| `search-widget` | `search-widget.html` | **EXACT_MATCH** | `0d17991610a7` | `0d17991610a7` |
| `sm-code` | `sm-code.gs` | **MISSING_IN_REPO** | `b0974c69e6e0` | — |

### Repo-only root script-ish files (not exact content matches to deployed set)

```text
Code.js            sha256=2b19ac995d51...  (not equal to Code.gs; not in deployed set)
appsScript.gs      sha256=765815fd110a...  (different symbol set from deployed sm-code)
test-cors.html     sha256=ec9cbe643057...  (not in deployed set)
```

### Function-name inventory (no source bodies)

```text
deployed Code functions:
  onHomepage, createSheetHomepageWithMenu, onGmailContext, onCalendarEventOpen,
  buildAgentCard, callAgentService, createErrorCard, syncCalendarToSheet

repo Code.gs functions:
  onHomepage, onGmailContext, onCalendarEventOpen, buildAgentCard,
  callAgentService, clearChatHistory, createErrorCard

deployed BrandedMeetingSummaries.gs functions:
  processMeetingsForDomain, processMeetingsForUser, getServiceAccountToken,
  createBrandedSummary, extractSection

deployed sm-code functions:
  syncCalendarToSheet, createNotificationResponse

repo appsScript.gs functions (unrelated name; not treated as sm-code authority):
  onOpen, triggerHourlyPublisher, fetchPendingPosts, publishPost,
  createTimeDrivenTriggers
```

### Manifest structural drift (redacted; no endpoints/IDs printed)

```text
addOns.common.name=AI Rolodex Assistant (both)
logoUrl=IDENTICAL (redacted)
homepageTrigger=onHomepage (both)
gmail.trigger=onGmailContext (both)
calendar.eventOpenTrigger=onCalendarEventOpen (both)
advancedServices=IDENTICAL_SET (9 services)
oauthScopes_deployed_count=13
oauthScopes_repo_count=8
oauthScopes_deployed_only=
  - https://www.googleapis.com/auth/calendar.addons.current.event.readonly
  - https://www.googleapis.com/auth/cloud-platform
  - https://www.googleapis.com/auth/gmail.addons.current.message.readonly
  - https://www.googleapis.com/auth/script.container.ui
  - https://www.googleapis.com/auth/spreadsheets
oauthScopes_repo_only=(none)
urlFetchWhitelist_deployed_count=2
urlFetchWhitelist_repo_count=1
urlFetchWhitelist_exact=NO
urlFetchWhitelist_values=REDACTED
```

## 6. Required return block

```text
R2_PROJECT_IDENTITY_MATCH=YES
R2_GETCONTENT=PASS
R2_FILE_COUNT=5
R2_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
R2_REPO_COMPARISON=DRIFT
R2_PRIVATE_IDS_PRINTED=NO
R2_TOKEN_VALUES_PRINTED=NO
R2_MUTATION_COUNT=0
CHANGED_PATHS=
  .ai/proof/addon-deployed-source-authority-readonly-live-20260818/r2-deployed-source-content-retrieval.md
VALIDATION=PASS_WITH_DRIFT
BLOCKERS=NONE_FOR_R2_RETRIEVAL
NEXT_GATE=DEPLOYED_SOURCE_RECONCILIATION_PLANNING
```

## 7. Success-condition check

```text
R2_GETCONTENT=PASS                 # required
R2_PRIVATE_IDS_PRINTED=NO          # required
R2_TOKEN_VALUES_PRINTED=NO         # required
R2_MUTATION_COUNT=0                # required
R2_REPO_COMPARISON=DRIFT           # informs next gate only
```

## 8. Interpretation (no remediation performed)

1. **Binding is solid**: Marketplace deployment ID equals the matched Apps Script
   deployment; version **47**; project identity matches clasp `scriptId`.
2. **HEAD source was retrieved successfully** via read-only `projects.getContent`.
3. **Deployed/HEAD source is not an exact match** to the intended clasp-root
   files on `A.I-Rolodex---Context` `main`:
   - 1 exact file (`search-widget`)
   - 2 digest mismatches (`Code`, `appsscript`)
   - 2 deployed files absent from repo (`BrandedMeetingSummaries.gs`, `sm-code`)
   - repo also carries extra root files not present in deployed content
4. **HEAD is newer than the bound version timestamp** (`2025-12-18` project
   update vs `2025-09-30` deployment/version update). Version-47 bytes are not
   separately fetchable via the authorized `getContent` surface; reconciliation
   planning must account for HEAD-vs-version ambiguity if version-pinned
   authority is required.
5. **No mutation** of Apps Script, deployments, Marketplace, OAuth scopes, IAM,
   or runtime routing occurred.

## 9. Next gate

```text
NEXT_GATE=DEPLOYED_SOURCE_RECONCILIATION_PLANNING
```

Reconciliation planning is out of scope for R2. This artifact only establishes
read-only retrieval, digests, and deterministic drift evidence.
