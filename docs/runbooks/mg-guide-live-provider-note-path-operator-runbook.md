# MG Guide live provider NOTE_PATH — operator runbook

`LIVE_NOTE_WRITE=PENDING`

This runbook describes the operator procedure for the future one-shot NOTE_PATH
live note write driven by `.github/workflows/mg-guide-live-provider-note-path.yml`.

It is a procedure document. It confers no authority. Reading, reviewing, or
merging it does not authorize live execution, does not open an activation
window, and does not create Activation 003.

---

## 1. Current status

```text
LIVE_NOTE_WRITE=PENDING
LIVE_PROVIDER_EXECUTION_AUTHORIZED=NO
WORKFLOW_DISPATCH_LIVE_EXECUTION_AUTHORIZED=NO
SECRET_PAYLOAD_ACCESS_AUTHORIZED=NO
ACTIVATION_003_CREATED=NO
R5_SAME_PROCESS_MATERIALIZATION=UNRESOLVED
MERGE_OF_HARNESS_ALONE_AUTHORIZES_EXECUTION=NO
SELF_ACTIVATION=FORBIDDEN
```

No live NOTE_PATH note write has been performed. Nothing in this repository may
be presented as a completed live note write, and no proof, submission, or
external claim may state or imply otherwise while this status reads `PENDING`.

### 1.1 The workflow currently refuses

As committed, the workflow cannot reach authentication, secret access, a
provider call, or the executor entrypoint. Three independent layers refuse
before any of those:

1. The preparation-gate job refuses unconditionally and exits non-zero.
2. The execution job carries a literal, structurally unsatisfiable job
   condition, and additionally depends on the gate job that always fails.
3. The first step of the execution job refuses unconditionally, before
   checkout, before authentication, and before the executor.

None of these layers reads a workflow input, environment value, variable, or
secret. The workflow declares **no dispatch inputs**, so there is no bypass
input, and no identifier may be supplied at dispatch time
(`RAW_IDS_AS_WORKFLOW_INPUTS_ALLOWED=NO`).

If an operator dispatches the workflow today, the correct and expected outcome
is a failed run with zero authentications, zero secret payload reads, zero
provider calls, and zero CRM mutations. That failure is not a defect to be
worked around.

Making the workflow capable of live execution requires a later, separately
authorized and independently reviewed change to the workflow file that removes
the refusal layers. It cannot be achieved by configuration, by a dispatch
option, by a repository or organization variable, or by editing status text.

---

## 2. Preflight

Preflight is read-only verification. It performs no provider call, no secret
payload read, no IAM change, and no deployment. Every item must be confirmed
independently; an unverified item is a stop, not an assumption.

| # | Preflight item | Required state |
|---|---|---|
| P1 | Harness implementation merged, at a known exact merge revision | Merged and reviewed |
| P2 | Offline mapper digest closure re-run against the frozen expected values, exact string equality | PASS |
| P3 | Deterministic test matrix `T01`–`T19` | All PASS, zero real network, zero real secret access |
| P4 | Repository canonical deterministic validation and secret-pattern scan | PASS |
| P5 | R5 same-process private-origin materialization | Independently PROVEN (see §3) |
| P6 | This runbook reviewed by the executing operator | Reviewed |
| P7 | Current provider write scope re-attested by the human owner | Re-attested (see §4) |
| P8 | Fresh live-provider authorization merged, binding the exact merged harness revision | Merged (see §5) |
| P9 | No prior activation window open, and all prior run identifiers confirmed terminal | Confirmed |
| P10 | Private origin material available to the root operator as `OPERATOR_PROOF_INPUT` only | Confirmed (see §8) |

Preflight failure of any item is terminal for the attempt. Do not open an
activation window to "hold a slot" while a preflight item is outstanding: prior
activation windows expired unused precisely because a window was opened before
an execution mechanism existed, and that failure mode must not recur.

---

## 3. R5 is unresolved and blocks live execution

```text
PRIVATE_ORIGIN_GITHUB_ACTIONS_SAME_PROCESS_MATERIALIZATION=UNRESOLVED_UNTIL_PROVEN
LIVE_EXECUTION_BLOCKED_WHILE_R5_UNRESOLVED=YES
```

Whether a legitimate root-owned private origin can be materialized in the same
GitHub Actions Python process is **not proven**. Until it is proven by
independently reviewable evidence, live execution is blocked.

The following are forbidden and none of them resolves R5:

```text
CROSS_PROCESS_HANDOFF_ALLOWED=NO
CROSS_PROCESS_REFERENCE_TRANSFER_ALLOWED=NO
SERIALIZED_REFERENCE_ALLOWED=NO
CALLER_RECONSTRUCTION_ALLOWED=NO
RAW_PROVIDER_IDS_ALLOWED=NO
RAW_ID_FALLBACK_ALLOWED=NO
DEGRADE_TO_CALLER_SUPPLIED_IDENTIFIER=FORBIDDEN
```

If a legitimate same-process origin is absent, the run must refuse **before**
Secret Manager access. That refusal is terminal. A hook that merely appears to
satisfy the interface while accepting caller-reconstructed material does not
resolve R5 and must never be reported as resolving it.

---

## 4. R1 — human owner console re-attestation

```text
R1_RESOLUTION_STRATEGY=FRESH_HUMAN_OWNER_CONSOLE_REATTESTATION_BEFORE_LIVE_ACTIVATION
REQUIRE_CURRENT_CONTACTS_WRITE_SCOPE_REATTESTATION=YES
SEPARATE_WRITE_SCOPE_PROVIDER_PROBE=NO
WRITE_SCOPE_PROBE_AUTHORIZED=NO
```

The provider write scope has never been exercised over the network; the one
proven live call was read-only. The authorized note write would be the first
live write with this credential.

Therefore, immediately before live activation, the **human owner** re-attests
current write scope by direct owner console review and records that attestation.
This is a human act. It is not delegated to an agent, and it is not inferred
from a prior attestation, from documentation, or from the credential's expected
configuration.

No provider probe substitutes for it: a separate write-scope probe is not
authorized, and issuing one would consume one-shot authority.

Re-attestation is a **precondition**, not a guarantee. If the live attempt
nevertheless fails on scope, see §7.

---

## 5. Required gate chain, in order

None of these steps is released by the harness, by this runbook, or by any
review of them. Each is a separate act with its own authority, and each must be
complete before the next begins.

```text
1  Fresh live-provider authorization, merged, binding the exact merged harness revision
2  Human Activation 003
3  Consumption Record 003
4  Separate explicit human execution act
5  Exactly one workflow dispatch
```

### 5.1 Fresh live-provider authorization

A new authorization must be merged that binds the exact merged harness revision
and states at minimum:

```text
401_OR_403_ON_FIRST_PROVIDER_ATTEMPT_IS_TERMINAL=YES
AUTHORITY_RESTORED_ON_SCOPE_FAILURE=NO
AUTHORITY_RESTORED_ON_FAILURE=NO
NO_RETRY=YES
```

The implementation authorization that permitted the harness explicitly does not
authorize execution. It cannot be reused, extended, or reinterpreted for that
purpose.

### 5.2 Human Activation 003

Created only after the whole of §2 is satisfied, including merged
implementation, digest proof, proven R5, this runbook reviewed, current write
scope re-attested, and the fresh live authorization merged. Activation 003 must
not be created in advance of those preconditions.

### 5.3 Consumption Record 003

Recorded in order, after Activation 003. The activation window and the
consumption record are distinct artifacts and must not be collapsed into one.

### 5.4 Separate explicit human execution act

A distinct, explicit human act, separate from creating the authorization,
separate from the activation, and separate from the consumption record. An
agent must never perform this step, and no automation may infer it from the
existence of the preceding artifacts.

This runbook deliberately does **not** define the format, field names, filenames,
identifiers, or value grammar of any of these artifacts. Their binding formats
are set by the governing authorization at the time it is written, not here.

---

## 6. Exactly one dispatch

```text
MAX_WORKFLOW_DISPATCHES=1
```

When, and only when, every gate in §2, §4, and §5 is satisfied, the authorized
human performs **exactly one** manual `workflow_dispatch` of
`.github/workflows/mg-guide-live-provider-note-path.yml`.

- The workflow is manual-only. It has no push, pull-request, schedule, or other
  automatic trigger, and it must never be given one.
- It takes no inputs. No identifier, target, override, or mode is supplied at
  dispatch time.
- Concurrency permits one run at a time. A queued run is never cancelled and
  never automatically retried.
- A second dispatch is a new live attempt, not a continuation. It is forbidden
  under the current authority and requires its own fresh authorization chain.

The run must be observed to completion. Do not dispatch and walk away.

---

## 7. Terminal outcomes — no retry, ever

```text
NO_RETRY=YES
NO_SEARCH=YES
NO_LIST=YES
NO_PAGINATION=YES
NO_FALLBACK=YES
NO_ALTERNATE_OPERATION=YES
NO_COMPENSATING_MUTATION=YES
NO_AUTOMATIC_CLEANUP=YES
NO_GENERIC_EXECUTE=YES
NO_STAGE_MUTATION=YES

MAX_PROVIDER_CALLS=3
MAX_CONTACT_GET_ATTEMPTS=1
MAX_NOTE_CREATE_ATTEMPTS=1
MAX_NOTE_READBACK_ATTEMPTS=1
MAX_TOTAL_GHL_MUTATIONS=1
MAX_OPPORTUNITY_STAGE_TRANSITIONS=0
```

**Every outcome of the single dispatch is terminal.** Whatever happens, the
attempt ends. The operator records the sanitized result and stops.

| Outcome | Operator action |
|---|---|
| Gate failure before secret access | Terminal. Record zero secret reads and zero provider calls. Do not re-dispatch. |
| Digest mismatch | Terminal. Live authorization request is not allowed to proceed on a tolerant or partial match. |
| Private origin absent | Terminal. Refusal occurs before secret access. Never degrade to a caller-supplied identifier. |
| `401` or `403` on the first provider attempt | **Terminal.** Authority is not restored. Do not re-dispatch, do not re-attest and retry, do not probe scope. |
| Contact identity mismatch | Terminal. The note POST must not be issued. |
| Note-create uncertainty | Terminal. Do not read back, do not retry, do not issue a compensating mutation. |
| Read-back mismatch | Terminal. Record the mismatch; do not issue a second write. |
| Success | Terminal. Record the sanitized report. The authority is consumed. |

Failure never restores authority. A failed attempt consumes the one-shot
authority exactly as a successful one does. Recovery requires a new
authorization chain from §5.1, not a retry.

Explicitly forbidden after any outcome: re-dispatch, a second POST, a
compensating or corrective mutation, a delete of a created note, a search or
list to "check what happened", pagination, an alternate operation, or an
opportunity stage transition.

---

## 8. Cleanup and destruction

Cleanup is explicit and verified. Runner disposal is never relied upon.

### 8.1 Credential file

The workflow authenticates with a credentials **file** and does not export
credentials into the environment, so no ambient application default credential
is available to unrelated processes or steps. The file path is passed only to
the single executor step.

Two guarded steps always run:

1. **Delete** — workspace path guard, symlink guard, regular-file assertion,
   then explicit delete. Emits `CREDENTIAL_FILE_DELETE_ATTEMPTS=1` and
   `EXPLICIT_CREDENTIAL_CLEANUP_PERFORMED=YES`.
2. **Verify absence** — asserts the path no longer exists as a file or symlink,
   then scans for residual credential files in the workspace. Emits
   `CREDENTIAL_FILE_ABSENT_AFTER_DELETE=YES`,
   `RESIDUAL_GHA_CREDENTIAL_FILES=0`, `RUNNER_DISPOSAL_RELIED_UPON=NO`, and
   `CREDENTIAL_CLEANUP_RESULT=PASS`.

A failure or a non-zero residual count in either step is a reportable incident.
It must be recorded, not suppressed.

### 8.2 Private origin material

```text
CLASSIFICATION=OPERATOR_PROOF_INPUT
MATERIALIZATION_OWNER=ROOT_OPERATOR
MATERIALIZATION_LOCATION=ephemeral, outside the repository working tree
MATERIALIZATION_LIFETIME=single workflow run
DESTRUCTION_REQUIRED=YES
DESTRUCTION_VERIFICATION_REQUIRED=YES
COMMITTED_TO_REPO=NO
PERSISTED_AS_WORKFLOW_ARTIFACT=NO
ECHOED_TO_LOGS=NO
```

Private origin material gates a one-shot operator proof. It must never become a
dependency of the contest build, of any deployment, or of the hosted runtime. It
is destroyed with the same model as the credential file — explicit delete, path
guard, symlink guard, post-delete absence assertion, residual scan — and the
destruction is verified, not assumed.

Absence of the material fails the run closed with no dispatch of a provider
call. It never degrades to a caller-supplied identifier.

---

## 9. Safe output

`DEFAULT=DENY`. Emit only the explicitly enumerated fields below, in run logs,
in proof artifacts, in this repository, and in any external or submission
material.

**Permitted:**

```text
RUN_ID, timestamps, agent sequence status, HTTP status classes,
contact_match YES/NO, location_match YES/NO, note_id_present YES/NO,
note_contact_match YES/NO, body_digest_match YES/NO,
provider call count, mutation count, terminal result
```

**Forbidden:**

```text
provider access token or bearer token, in any form, including prefixes and lengths
credential file contents
raw contact identifier
raw location identifier
raw note identifier
full provider response body
private binding file contents
transcript-derived customer content
```

```text
RAW_RESPONSE_LOGGING=NO
AUTH_HEADER_LOGGING=NO
EXCEPTION_TRACEBACK_TO_PUBLIC_LOG=NO
DIGESTS_EMITTED_AS=MATCH_BOOLEAN_ONLY_OR_ALREADY_PUBLIC_FROZEN_VALUE
NOTE_ID_EMITTED_AS=note_id_present YES/NO
```

Emit a match boolean rather than a value even where the value looks harmless: a
raw note identifier is private-binding-adjacent, and the frozen digests are
already public, so a boolean carries the full proof value with no disclosure.

Do not screenshot, paste, or transcribe raw run output into a submission,
issue, review comment, or external form. Report the enumerated fields only.

---

## 10. Stop conditions

Stop and escalate rather than proceeding, if any of the following occurs:

- Any preflight item in §2 is unverified, stale, or fails.
- R5 is anything other than independently proven.
- The human owner write-scope re-attestation is unavailable, delegated, or
  inferred.
- Any gate artifact in §5 is missing, out of order, or reused from a prior
  attempt.
- A second dispatch, retry, fallback, alternate operation, compensating
  mutation, search, list, pagination, or stage transition appears necessary.
- The workflow appears to require a new HTTP client, credential accessor,
  serializer, digest function, transport, or a change to an already merged
  module.
- Any raw identifier, credential value, or private binding detail is about to be
  written to a log, artifact, repository file, or external surface.
- Cleanup or destruction verification does not report a clean, zero-residual
  result.

Escalation is to the authorizing human. An agent must not resolve any of these
by widening scope.

---

## 11. Status of this document

```text
RUNBOOK_CONFERS_AUTHORITY=NO
LIVE_NOTE_WRITE=PENDING
R5_SAME_PROCESS_MATERIALIZATION=UNRESOLVED
ACTIVATION_003_CREATED=NO
WORKFLOW_DISPATCHES_PERFORMED=0
PROVIDER_CALLS_PERFORMED=0
CRM_MUTATIONS_PERFORMED=0
SECRET_PAYLOAD_READS_PERFORMED=0
```
