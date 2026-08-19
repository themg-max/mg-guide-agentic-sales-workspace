# R3 — Deployed Source Provenance Reconciliation (Read-Only)

```text
ARTIFACT=.ai/proof/addon-deployed-source-authority-readonly-live-20260818/r3-deployed-source-provenance-reconciliation.md
UNIT=ADDON_DEPLOYED_SOURCE_AUTHORITY_READONLY_LIVE_R3
LANE=gov/addon-deployed-source-authority-readonly-live-002
OWNER=VS Code / operator or bounded Codex inspection
MODE=read_only_historical_lineage_redacted
CREATED_AT_LOCAL=2026-08-18T20:13:03-04:00
CREATED_AT_UTC=2026-08-19T00:13:03Z
GOVERNANCE_GATE=PASS_WITH_GUARDS
PRIOR_R2=r2-deployed-source-content-retrieval.md
ACTION=create (additive proof only)
MUTATION_AUTHORIZED=NO
```

## 0. Mandatory preflight

### 0.1 Proof / governance worktree (artifact host)

```text
PWD=/Users/achandler/Google_DevPost/mg-guide-agentic-sales-workspace
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
```

### 0.2 Bound add-on source repository (comparison basis; inspected read-only)

R2 established the intended clasp-root comparison basis as
`themg-max/A.I-Rolodex---Context`. R3 inspected that repository without
mutating it.

```text
SOURCE_PATH=/Users/achandler/A.I-Rolodex---Context
SOURCE_ORIGIN=https://github.com/themg-max/A.I-Rolodex---Context.git
SOURCE_REPO_IDENTITY=themg-max/A.I-Rolodex---Context
SOURCE_BRANCH=main
SOURCE_HEAD=9b689f1f85fdea0b8c2306cfe09886b0e6da652d
SOURCE_MATCHES_R2_COMPARISON_BASIS=YES
SOURCE_MUTATIONS_PERFORMED=NO
```

### 0.3 Preflight decision

```text
PROOF_LANE_PREFLIGHT=PASS
SOURCE_REPO_PREFLIGHT=PASS_FOR_READONLY_INSPECTION
STOP_CONDITIONS_HIT=NO
NOTE=Proof artifacts live on mg-guide-agentic-sales-workspace governed lane;
     durable add-on source lineage is evaluated against A.I-Rolodex---Context.
```

## 1. Known authority carried forward (from R1/R2; not re-fetched)

```text
MARKETPLACE_INTEGRATION_TYPE=APPS_SCRIPT
BOUND_MARKETPLACE_VERSION=47
R1C_BINDING=PASS
R2_PROJECT_IDENTITY_MATCH=YES
R2_GETCONTENT=PASS
R2_FILE_COUNT=5
R2_REPO_COMPARISON=DRIFT
R2_MUTATION_COUNT=0
R2_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
R2_SOURCE_MANIFEST_DIGEST=50b5556bf68974d43ef04c7e142b7ba5bc590ac96ac40bdba5438599eecd0158
BOUND_SCRIPT_ID_SHA256_12=443d99b5b08b
CLASP_SCRIPT_ID_SHA256_12=443d99b5b08b
PROJECT_TITLE=MG_GUIDE Workspace Add-on
PROJECT_CREATE_TIME=2025-08-27T22:52:45.762Z
DEPLOYMENT_UPDATE_TIME_V47=2025-09-30T00:49:46.065Z
PROJECT_HEAD_UPDATE_TIME=2025-12-18T15:10:04.198Z
```

### Critical interpretation (reaffirmed)

```text
GETCONTENT_SURFACE=projects.getContent current project HEAD
GETCONTENT_IS_VERSION_47_BYTES=NO
HEAD_AFTER_BOUND_VERSION=YES
  deployment_updateTime=2025-09-30T00:49:46.065Z
  project_head_updateTime=2025-12-18T15:10:04.198Z
```

R2 HEAD digests (authoritative for Apps Script **HEAD only**):

| Deployed name | Type | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `BrandedMeetingSummaries.gs` | SERVER_JS | 11531 | `40a536f14b253c163d992c3f015d2d7501547421d2cb028d6fbc01ecfd55a3e4` |
| `Code` | SERVER_JS | 10790 | `7f9d9f8aa99abdd5ba9ef3bdbc932eab6350f26f6557415b5ca8f82d742d84dd` |
| `appsscript` | JSON | 2747 | `6652496d67ea02314d96f01f7272aabb9cbf3214f4edb56e857833c89dedb26b` |
| `search-widget` | HTML | 740 | `0d17991610a7a16cdddf25069614965f991c69a14123c9f7776386e35fa18309` |
| `sm-code` | SERVER_JS | 2656 | `b0974c69e6e02cfdaa79d59a8e5998af095dfdf964fc960c89a5b2d88be9f9ed` |

Private capture integrity re-checked locally (hashes only; **no** private
source copied into either repository):

```text
PRIVATE_R2_FILES_MATCH_R2_TABLE=YES
PRIVATE_PATH=~/.config/mg-guide-c2b/r2-private/files/
PRIVATE_SOURCE_COPIED_TO_REPO=NO
```

## 2. Authorization boundary (R3)

### Authorized and performed

```text
GIT_READONLY_LOG_SHOW_GREP_HASH=YES
LOCAL_PRIVATE_DIGEST_COMPARE=YES
STRUCTURAL_LINE_OVERLAP_METRICS_NO_BODY_PRINT=YES
ADDITIVE_REDACTED_PROOF_ARTIFACT=YES
```

### Not authorized and not performed

```text
git_edit_stage_commit=NO
clasp_pull_push_deploy=NO
projects.updateContent=NO
projects.getContent_refetch=NO
versions.get_or_version_content_api=NO
Apps_Script_deployment_changes=NO
Marketplace_changes=NO
OAuth_IAM_IAP_changes=NO
copy_private_source_into_repo=NO
runtime_changes=NO
source_reconciliation_write=NO
API_WRITE_CALLS=0
R3_MUTATION_COUNT=0
```

## 3. Historical search method (deterministic)

1. Enumerate path history on `A.I-Rolodex---Context` for:
   - `BrandedMeetingSummaries.gs`, `sm-code.gs`
   - `Code.gs`, `appsscript.json`, `search-widget.html`
   - `Code.js`, `appsScript.gs`
   - pre-flatten paths under `ai-rolodex-crm/` and `backup-crm/`
2. Collect unique git blobs via `git log --raw` / tree listing; compute
   SHA-256 over blob bytes; compare to R2 HEAD digests.
3. Confirm filename presence across `git rev-list --objects` name stream.
4. Pickaxe / `git grep` for deployed-only function symbols (names only).
5. Inspect structural commits around known operational timestamps
   (2025-09-30 bound deploy; 2025-12-18 Apps Script HEAD update) **without**
   inferring byte identity from timestamps alone.
6. Inspect nested-git import history (`ai-rolodex-crm` gitlink → folder).
7. Scan local clones/worktrees for **exact** R2 content hashes (path listing
   only on hits; no private source ingestion into git).

## 4. Repository structure chronology (durable facts)

```text
SUBMODULE_OR_GITLINK_BEFORE_IMPORT=YES
  path=ai-rolodex-crm
  mode_before=160000
  gitlink_commit=752771e8b84a7daecca79e171ffd2adebc48414b
  gitlink_object_in_parent_odb=NO
  gitlink_resolvable_in_scanned_local_clones=NO
NESTED_FOLDER_IMPORT_COMMIT=823375a28dda799dd41f35c8eaab6009f93ddc93
NESTED_FOLDER_IMPORT_DATE=2025-11-27T09:59:12-05:00
  subject=Fix nested git repo and track ai-rolodex-crm as normal folder
FLATTEN_COMMIT=e94a87f477e30b544a158a03e81739f360765376
FLATTEN_DATE=2025-11-29T10:43:14-05:00
  subject=Flatten repo structure and remove old ai-rolodex-crm folder
  effect=ai-rolodex-crm/{Code.gs,appsscript.json,search-widget.html,...}
          -> repo root + backup-crm/ copy
```

Implications:

- Pre-2025-11-27 nested repository history for clasp sources is **not**
  present as reachable git objects in the parent `A.I-Rolodex---Context` ODB
  (gitlink target missing).
- Observed root clasp file bytes on `main` are a single frozen content
  generation introduced at nested import / flatten (no subsequent content
  evolution on `main` for those paths).
- Bound deployment version **47** (`2025-09-30`) predates durable in-repo
  tracking of clasp sources (`2025-11-27`). Timestamp adjacency alone cannot
  prove version-47 bytes.

### Window checks (path-touching commits on `main`)

```text
MAIN_COMMITS_TOUCHING_CLASP_PATHS_2025-09-20..2025-10-10=0
MAIN_COMMITS_TOUCHING_CLASP_PATHS_2025-12-10..2025-12-25=0
MAIN_COMMITS_ANY_NEAR_2025-09-30=0
MAIN_COMMITS_ANY_NEAR_2025-12-18=present_but_unrelated_docs_mcp_ui_only
```

Apps Script HEAD update on `2025-12-18` has **no** correlating clasp-path
commit on `main`. Do not treat calendar coincidence as lineage.

## 5. Per-file historical findings

### 5.1 `search-widget` / `search-widget.html`

```text
R2_SHA256=0d17991610a7a16cdddf25069614965f991c69a14123c9f7776386e35fa18309
REPO_HEAD_SHA256=0d17991610a7a16cdddf25069614965f991c69a14123c9f7776386e35fa18309
EXACT_BYTE_MATCH=YES
HISTORICAL_BLOB_MATCH_IN_REPO=YES
FIRST_DURABLE_TRACKING=2025-11-27 nested import (ai-rolodex-crm/search-widget.html)
ALSO_AT=root search-widget.html; backup-crm/search-widget.html
UNIQUE_CONTENT_VERSIONS_ON_MAIN=1
CLASSIFICATION=HISTORICAL_REPO_MATCH
```

### 5.2 `Code` / `Code.gs`

```text
R2_HEAD_SHA256=7f9d9f8aa99abdd5ba9ef3bdbc932eab6350f26f6557415b5ca8f82d742d84dd
R2_BYTES=10790
REPO_MAIN_Code.gs_SHA256=363684ce6ffece62f5d7d4cb4a3c0d66923d04d00fe744597f0ea16d4dba5d35
REPO_MAIN_Code.gs_BYTES=12770
EXACT_BYTE_MATCH=NO
HISTORICAL_BLOB_MATCH_FOR_R2_DIGEST=NO
  scanned=root Code.gs, ai-rolodex-crm/Code.gs, backup-crm/Code.gs, Code.js variants
LINE_OVERLAP_JACCARD_vs_REPO_Code.gs=0.396
  unique_lines_r2=172 repo=209 intersection=108
```

Function-name inventory (no bodies):

```text
R2_HEAD_Code_functions=
  onHomepage, createSheetHomepageWithMenu, onGmailContext, onCalendarEventOpen,
  buildAgentCard, callAgentService, createErrorCard, syncCalendarToSheet
REPO_main_Code.gs_functions=
  onHomepage, onGmailContext, onCalendarEventOpen, buildAgentCard,
  callAgentService, clearChatHistory, createErrorCard
DEPLOYED_ONLY_SYMBOLS_IN_REPO_HISTORY=
  createSheetHomepageWithMenu=ABSENT (git log -S count=0; git grep main=0)
  syncCalendarToSheet=ABSENT from Code.gs/appsScript.gs paths on main
REPO_ONLY_SYMBOL_EXAMPLE=clearChatHistory
```

```text
CLASSIFICATION_OF_R2_HEAD_BYTES=POST_DEPLOYMENT_HEAD_ONLY
CLASSIFICATION_OF_REPO_PATH_RELATION=CURRENT_REPO_SUPERSESSION
NOTE=Repo Code.gs is a related but non-identical superseding tree at the
     intended clasp path; it does not reproduce Apps Script HEAD bytes and
     cannot be back-dated to version 47 by evidence in this lane.
```

### 5.3 `appsscript` / `appsscript.json`

```text
R2_HEAD_SHA256=6652496d67ea02314d96f01f7272aabb9cbf3214f4edb56e857833c89dedb26b
R2_BYTES=2747
REPO_MAIN_SHA256=2c7f981952a876695a778c41b6ee2168e0bd5a1000e4ccf109a24b6c0e458bf5
REPO_MAIN_BYTES=2380
EXACT_BYTE_MATCH=NO
HISTORICAL_BLOB_MATCH_FOR_R2_DIGEST=NO
LINE_OVERLAP_JACCARD=0.870
  unique_lines_r2=75 repo=69 intersection=67
R2_STRUCTURAL_DRIFT_FROM_R2_ARTIFACT=
  oauthScopes_deployed_count=13 vs repo_count=8
  urlFetchWhitelist_exact=NO
CLASSIFICATION_OF_R2_HEAD_BYTES=POST_DEPLOYMENT_HEAD_ONLY
CLASSIFICATION_OF_REPO_PATH_RELATION=CURRENT_REPO_SUPERSESSION
```

### 5.4 `BrandedMeetingSummaries.gs`

```text
R2_HEAD_SHA256=40a536f14b253c163d992c3f015d2d7501547421d2cb028d6fbc01ecfd55a3e4
R2_BYTES=11531
FILENAME_IN_REPO_HISTORY=NO
OBJECT_NAME_STREAM_HIT=NO
git_log_-S_processMeetingsForDomain=0
git_log_-S_createBrandedSummary=0
git_grep_main_deployed_symbols=0
LOCAL_WORKTREE_EXACT_HASH_HITS_OUTSIDE_PRIVATE_R2=NO
CLASSIFICATION=OUT_OF_BAND_SOURCE
```

Deployed-only functions (names): `processMeetingsForDomain`,
`processMeetingsForUser`, `getServiceAccountToken`, `createBrandedSummary`,
`extractSection`.

### 5.5 `sm-code` / `sm-code.gs`

```text
R2_HEAD_SHA256=b0974c69e6e02cfdaa79d59a8e5998af095dfdf964fc960c89a5b2d88be9f9ed
R2_BYTES=2656
FILENAME_sm-code.gs_IN_REPO_HISTORY=NO
NEAREST_NAME_CANDIDATE=appsScript.gs
REPO_appsScript.gs_SHA256=765815fd110aef8f1c9a409fdc328a46a0131aa726bbfb5e4a334c31297a60a3
REPO_appsScript.gs_BYTES=4593
LINE_OVERLAP_JACCARD_vs_appsScript.gs=0.058
  intersection_lines=8 (not an identity argument)
git_log_-S_createNotificationResponse=0
git_grep_main_syncCalendarToSheet=0
git_grep_main_createNotificationResponse=0
REPO_appsScript.gs_symbols=onOpen, triggerHourlyPublisher, fetchPendingPosts,
  publishPost, createTimeDrivenTriggers
CLASSIFICATION=OUT_OF_BAND_SOURCE
NOTE=Do not treat appsScript.gs as sm-code authority.
```

### 5.6 Local exact-hash sweep (supplemental)

Exact R2 content hashes located only at:

```text
~/.config/mg-guide-c2b/r2-private/files/*   # private R2 capture (expected)
search-widget.html elsewhere in Rolodex worktrees/clones (repo-lineage file)
```

No non-private worktree file matched R2 digests for `Code`, `appsscript`,
`BrandedMeetingSummaries.gs`, or `sm-code`.

## 6. Lineage determinations

### 6.1 Does current Apps Script HEAD have historical repo lineage?

```text
HEAD_TO_REPO_LINEAGE=PARTIAL
HEAD_TO_REPO_LINEAGE_DETAIL=
  search-widget     = HISTORICAL_REPO_MATCH (exact bytes in durable git history)
  Code              = POST_DEPLOYMENT_HEAD_ONLY bytes; repo path is CURRENT_REPO_SUPERSESSION (related, non-identical)
  appsscript        = POST_DEPLOYMENT_HEAD_ONLY bytes; repo path is CURRENT_REPO_SUPERSESSION (high overlap, non-identical)
  BrandedMeetingSummaries.gs = OUT_OF_BAND_SOURCE (no filename/symbol/byte lineage)
  sm-code           = OUT_OF_BAND_SOURCE (no filename/symbol/byte lineage; appsScript.gs is not a substitute)
HEAD_ENSEMBLE_EXACT_REPO_MATCH=NO
HEAD_ENSEMBLE_PROVEN_AS_SINGLE_GIT_TREE=NO
```

Partial shared ancestry is visible for `Code`/`appsscript`/`search-widget`
(common add-on surface names + partial line overlap + one exact file), but the
**HEAD ensemble** (5 files / aggregate digest
`0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117`) is **not**
reproduced by any scanned git tree.

### 6.2 Can version-47 lineage be proven from durable evidence?

```text
VERSION_47_BYTES=NOT_RECOVERED
VERSION_47_BYTES_SOURCE_AVAILABLE_IN_LANE=NO
VERSION_47_GETCONTENT=NOT_APPLICABLE (getContent returns HEAD only; already captured in R2)
VERSION_47_API_VERSION_PINNED_FETCH_PERFORMED=NO
VERSION_47_EXACT_REPO_TREE_MATCH=NO
VERSION_47_TIMESTAMP_CORRELATION_ONLY=INSUFFICIENT
VERSION47_TO_REPO_LINEAGE=UNRESOLVED
```

Fail-closed rule applied: without version-pinned bytes or an exact historical
repo tree match, version-47 ↔ repo lineage **cannot** be asserted.

Reasons version-47 remains unresolved even if HEAD were fully matched (it is not):

1. Bound deployment update (`2025-09-30`) precedes durable clasp tracking in
   parent git (`2025-11-27`).
2. Nested gitlink commit `752771e8…` is missing from the parent object database.
3. Apps Script HEAD (`2025-12-18`) is strictly after version-47; HEAD bytes are
   not a substitute for version-47 bytes.
4. No authorized version-content retrieval was performed in R2/R3.

## 7. Classification summary matrix

| Deployed artifact | R2 HEAD vs repo history | Classification |
| --- | --- | --- |
| `search-widget` | Exact digest match since 2025-11-27 | `HISTORICAL_REPO_MATCH` |
| `Code` | Digest absent; related non-identical `Code.gs` on main | HEAD bytes: `POST_DEPLOYMENT_HEAD_ONLY`; repo path: `CURRENT_REPO_SUPERSESSION` |
| `appsscript` | Digest absent; high-overlap non-identical manifest | HEAD bytes: `POST_DEPLOYMENT_HEAD_ONLY`; repo path: `CURRENT_REPO_SUPERSESSION` |
| `BrandedMeetingSummaries.gs` | No path/symbol/byte history | `OUT_OF_BAND_SOURCE` |
| `sm-code` | No path/symbol/byte history | `OUT_OF_BAND_SOURCE` |
| Version 47 ensemble | No durable byte proof | `UNRESOLVED` |

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

R2_HEAD_DIGEST_BOUND=YES
  R2_SOURCE_DIGEST=0801d4848ad0bc913755c7cdff982ae3d44f0af13686c161d98d4a0411802117
  R2_SOURCE_MANIFEST_DIGEST=50b5556bf68974d43ef04c7e142b7ba5bc590ac96ac40bdba5438599eecd0158
  R2_FILE_COUNT=5
  NOTE=Digests bind Apps Script HEAD (2025-12-18), not version 47.

VERSION_47_BYTES=NOT_RECOVERED
BRANDED_MEETING_SUMMARIES_HISTORY=NONE_IN_REPO (OUT_OF_BAND_SOURCE)
SM_CODE_HISTORY=NONE_IN_REPO (OUT_OF_BAND_SOURCE)
CODE_GS_HISTORY=SINGLE_FROZEN_CONTENT_SINCE_2025-11-27_IMPORT; R2_HEAD_DIGEST_ABSENT
APPS_SCRIPT_MANIFEST_HISTORY=SINGLE_FROZEN_CONTENT_SINCE_2025-11-27_IMPORT; R2_HEAD_DIGEST_ABSENT
SEARCH_WIDGET_HISTORY=EXACT_R2_DIGEST_SINCE_2025-11-27_IMPORT (HISTORICAL_REPO_MATCH)

HEAD_TO_REPO_LINEAGE=PARTIAL
VERSION47_TO_REPO_LINEAGE=UNRESOLVED

AUTHORITY_RECONCILIATION_STATUS=FAIL_CLOSED_PARTIAL_HEAD_LINEAGE_ONLY
MUTATION_COUNT=0
BLOCKERS=
  1) Version-47 source bytes are not available from authorized evidence surfaces used in this lane.
  2) Apps Script HEAD ensemble is not an exact historical git tree in A.I-Rolodex---Context.
  3) Two deployed files (BrandedMeetingSummaries.gs, sm-code) have zero durable repo lineage.
  4) Nested pre-import gitlink objects are missing; pre-2025-11-27 clasp history is not recoverable from parent ODB.
  5) Timestamp correlation (2025-09-30 / 2025-12-18) is insufficient to prove byte identity.

NEXT_GATE=VERSION47_BYTE_RECOVERY_OR_EXPLICIT_HEAD_VS_V47_AUTHORITY_DECISION
NEXT_GATE_NOT_ENTERED=DEPLOYED_SOURCE_AUTHORITY_DECISION_AND_RECONCILIATION_PLAN
REASON_NEXT_GATE_BLOCKED=VERSION47_TO_REPO_LINEAGE=UNRESOLVED (fail-closed)
```

## 9. Success / fail-closed check

```text
DEFENSIBLE_HEAD_LINEAGE_STATEMENT=YES (partial; matrix above)
DEFENSIBLE_VERSION47_LINEAGE_STATEMENT=NO
VERSION47_TO_REPO_LINEAGE=UNRESOLVED
SOURCE_OR_DEPLOYMENT_MUTATION=NO
PRIVATE_SOURCE_COPIED_TO_REPO=NO
RECONCILIATION_WRITE_PERFORMED=NO
R3_RESULT=FAIL_CLOSED_ON_VERSION47_WITH_PARTIAL_HEAD_FINDINGS
```

## 10. Explicit non-actions (stop before reconciliation write)

R3 stops before any source reconciliation write. Not performed:

- no repo file creation/update outside this additive proof artifact
- no clasp pull/push/deploy
- no Apps Script content or deployment mutation
- no Marketplace mutation
- no promotion of Apps Script HEAD as version-47 authority
- no treatment of `appsScript.gs` as `sm-code`
- no inference that 2025-09-30 or 2025-12-18 timestamps alone identify bytes

## 11. Operator notes for a future authorized gate (informational only)

These are **not** authorized actions in R3; listed only so the next gate can
be scoped without re-discovering blockers:

1. If Marketplace authority must remain version **47**, obtain version-pinned
   source bytes via an explicitly authorized read surface (if any exists and is
   approved), then re-run digest↔git comparison.
2. If operator elects Apps Script **HEAD** as the new authority basis, that is
   a separate authority decision (still requires reconciliation planning for
   out-of-band files and digest mismatches) — not proven here as version 47.
3. Recovering nested gitlink history (`752771e8…`) from backup media, if it
   still exists outside this parent ODB, may unlock pre-2025-11-27 clasp
   provenance — currently unavailable.

---

END R3
