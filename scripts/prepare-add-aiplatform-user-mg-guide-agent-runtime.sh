#!/usr/bin/env bash
# Read-only IAM inspection helper for Lane A exact-member addition preparation.
# This script NEVER mutates IAM. Any add-iam-policy-binding text below is
# NON-EXECUTABLE PREPARATION REFERENCE ONLY for a later separate human act.
set -euo pipefail

PROJECT="ai-rolodex-to-crm"
MEMBER="serviceAccount:mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
ROLE="roles/aiplatform.user"
POLICY_FILE="${TMPDIR:-/tmp}/airolodex_policy_readonly_$$.json"

cleanup() {
  rm -f "$POLICY_FILE"
}
trap cleanup EXIT

cat <<-MSG
This helper performs READ-ONLY checks for adding:
  MEMBER=$MEMBER
  ROLE=$ROLE
  PROJECT=$PROJECT

It does NOT:
  - call gcloud config set project
  - execute projects add-iam-policy-binding
  - create role bindings, remove members, change conditions
  - create service accounts or keys
  - consume issue #311 / authority ledger (CONSUMED remains NO)

Governance ceilings for a later separate human execution act (not this script):
  MAX_PROJECT_IAM_POLICY_WRITES=1
  MAX_EXACT_MEMBER_ADDITIONS=1
  MAX_ROLE_BINDINGS_CREATED=0
  MAX_MEMBER_REMOVALS=0
  MAX_CONDITION_CHANGES=0
  MAX_SERVICE_ACCOUNT_CREATES=0
  MAX_SERVICE_ACCOUNT_KEYS=0

Requirements:
  - gcloud CLI installed and authenticated
  - jq installed
  - Confirmed merged activation, fresh window, and preconditions before any human write
MSG

if ! command -v gcloud >/dev/null 2>&1; then
  echo "ERROR: gcloud CLI is required." >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required." >&2
  exit 1
fi

echo
echo "1) Active gcloud account (read-only; project passed explicitly on each call)"
gcloud auth list --filter="status:ACTIVE" --format="value(account)" || true

echo
echo "2) Downloading current project IAM policy (READ-ONLY) to $POLICY_FILE"
gcloud projects get-iam-policy "$PROJECT" \
  --project="$PROJECT" \
  --format=json >"$POLICY_FILE"

echo
echo "3) Checking whether role binding exists for $ROLE"
ROLE_COUNT="$(jq -r --arg ROLE "$ROLE" '[.bindings[]? | select(.role==$ROLE)] | length' "$POLICY_FILE")"
if [[ "$ROLE_COUNT" -ge 1 ]]; then
  echo "ROLE_BINDING_PRESENT=YES"
  echo "ROLE_BINDING_COUNT=$ROLE_COUNT"
else
  echo "ROLE_BINDING_PRESENT=NO"
  echo "ROLE_BINDING_COUNT=0"
fi

CONDITION_COUNT="$(jq -r --arg ROLE "$ROLE" '[.bindings[]? | select(.role==$ROLE) | select(.condition != null)] | length' "$POLICY_FILE")"
if [[ "$CONDITION_COUNT" -gt 0 ]]; then
  echo "ROLE_BINDING_HAS_CONDITION=YES"
else
  echo "ROLE_BINDING_HAS_CONDITION=NO"
fi

echo
echo "4) Checking whether exact member is present on $ROLE"
MEMBER_COUNT="$(jq -r --arg ROLE "$ROLE" --arg MEMBER "$MEMBER" '[.bindings[]? | select(.role==$ROLE) | .members[]? | select(.==$MEMBER)] | length' "$POLICY_FILE")"
if [[ "$MEMBER_COUNT" -ge 1 ]]; then
  echo "EXACT_MEMBER_PRESENT=YES"
  echo "EXACT_MEMBER_ROLE_BINDING_COUNT=$MEMBER_COUNT"
else
  echo "EXACT_MEMBER_PRESENT=NO"
  echo "EXACT_MEMBER_ROLE_BINDING_COUNT=0"
fi

AMBIGUOUS=NO
if [[ "$ROLE_COUNT" -eq 0 ]]; then
  AMBIGUOUS=YES
fi
if [[ "$ROLE_COUNT" -gt 1 ]]; then
  AMBIGUOUS=YES
fi
if [[ "$CONDITION_COUNT" -gt 0 ]]; then
  AMBIGUOUS=YES
fi
if [[ "$MEMBER_COUNT" -gt 1 ]]; then
  AMBIGUOUS=YES
fi
echo "CONFLICTING_OR_AMBIGUOUS_STATE=$AMBIGUOUS"

echo
echo "5) Fail-closed gate evaluation (inspection only; no write)"
if [[ "$ROLE_COUNT" -eq 0 ]]; then
  cat <<-FAIL
FAIL_CLOSED=YES
REASON=ROLE_BINDING_MISSING
DISPOSITION=BLOCKED_MAX_ROLE_BINDINGS_CREATED_IS_0
PROJECT_IAM_POLICY_WRITES=0
EXACT_MEMBER_ADDITIONS=0
AUTHORIZATION_CONSUMED=NO
NOTE=Do not run any IAM write. MAX_ROLE_BINDINGS_CREATED=0 forbids creating the role binding.
FAIL
  exit 2
fi

if [[ "$AMBIGUOUS" == "YES" ]]; then
  cat <<-FAIL
FAIL_CLOSED=YES
REASON=CONFLICTING_OR_AMBIGUOUS_STATE
DISPOSITION=BLOCKED_RETURN_FOR_REVIEW
PROJECT_IAM_POLICY_WRITES=0
EXACT_MEMBER_ADDITIONS=0
AUTHORIZATION_CONSUMED=NO
NOTE=Do not run any IAM write while member/role state is ambiguous or conditioned.
FAIL
  exit 2
fi

if [[ "$MEMBER_COUNT" -ge 1 ]]; then
  cat <<-SAT
DISPOSITION=ALREADY_SATISFIED_NO_WRITE
EXACT_MEMBER_PRESENT=YES
PROJECT_IAM_POLICY_WRITES=0
EXACT_MEMBER_ADDITIONS=0
AUTHORIZATION_CONSUMED=NO
NOTE=Exact member already present. No write is necessary or authorized by this helper.
SAT
  exit 0
fi

cat <<-PASS
DISPOSITION=ELIGIBLE_FOR_LATER_SEPARATE_HUMAN_EXECUTION
ROLE_BINDING_PRESENT=YES
EXACT_MEMBER_PRESENT=NO
CONFLICTING_OR_AMBIGUOUS_STATE=NO
PROJECT_IAM_POLICY_WRITES=0
EXACT_MEMBER_ADDITIONS=0
AUTHORIZATION_CONSUMED=NO
ISSUE_311_OR_LEDGER_CONSUMED=NO
PASS

cat <<-INSTR

============================================================
NON-EXECUTABLE PREPARATION REFERENCE ONLY
============================================================
The following command is documented for human operators AFTER:
  - merged Lane A activation artifact
  - fresh pre-write revalidation
  - current time inside a valid authorization window
  - separate one-shot authority consumption record
  - explicit human execution act

This helper does NOT execute it. Copy/paste execution is intentionally
outside this script's control flow.

  gcloud projects add-iam-policy-binding "${PROJECT}" \\
    --project="${PROJECT}" \\
    --member="${MEMBER}" \\
    --role="${ROLE}"

Post-write verification reference (also non-executed here):

  gcloud projects get-iam-policy "${PROJECT}" \\
    --project="${PROJECT}" \\
    --format=json \\
  | jq -r --arg ROLE "${ROLE}" --arg MEMBER "${MEMBER}" \\
      '[.bindings[]? | select(.role==\$ROLE) | .members[]? | select(.==\$MEMBER)] | length'

Until actual authority consumption by a separate human execution act:
  AUTHORIZATION_CONSUMED=NO
  ISSUE_311_OR_LEDGER_CONSUMED=NO
============================================================
INSTR

exit 0
