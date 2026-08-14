# NW-007 IAP Authentication Validation Follow-up

```text
OBJECTIVE=PROVE_FRESH_SESSION_EVALUATOR_AUTHENTICATION_AND_AUTHORIZATION
EVALUATOR_ACCOUNT=buildweek-evaluator@themiliare-group.com
JUDGE_GROUP=mg-mcp-developer-mg@themiliare-group.com
EVALUATOR_JUDGE_GROUP_MEMBERSHIP=CONFIRMED
AUTHENTICATION_RESULT=PASS
AUTHORIZATION_RESULT=PASS
ROOT_CAUSE=NONE_OBSERVED_IN_FINAL_CONTROLLED_VALIDATION
PRIOR_ERROR_9_FINAL_DISPOSITION=NOT_REPRODUCED_IN_FINAL_CONTROLLED_VALIDATION
PRIOR_HTTP_400_CAUSE=INVALID_SCENARIO_SELECTOR_TYPO
SUCCESS_CRITERIA=FRESH_PRIVATE_SESSION;PROTECTED_SERVICE_INITIATES_IAP_AUTH_FLOW;EXPLICIT_EVALUATOR_ACCOUNT_SELECTED;GOOGLE_SIGN_IN_COMPLETED;IAP_REDIRECT_RETURN_COMPLETED;GET_/health_HTTP_200;HEALTH_STATUS_OK;HEALTH_JUDGE_MODE_STUB;SAME_SESSION_POST_SUCCESS_HTTP_200;SAME_SESSION_POST_SUCCESS_WORKFLOW_COMPLETED;NEGATIVE_CONTROL_REQUIRES_IAP_AUTH
CONTROLLED_SMOKE_METHOD=BROWSER_DRIVEN_SAME_SESSION_VALIDATION
DEPLOYED_CODE_CHANGE=NO
ON_SUCCESS_CAPTURE=ACCOUNT_IDENTITY;HEALTH_HTTP_STATUS;HEALTH_STATUS;HEALTH_JUDGE_MODE;SUCCESS_HTTP_STATUS;SUCCESS_WORKFLOW_STATUS;NEGATIVE_CONTROL_RESULT
ON_FAILURE_CAPTURE=FAILURE_STAGE;FAILURE_HOST;FAILURE_PATH;HTTP_STATUS;PREVIOUS_REDIRECT_HOST;NEXT_REDIRECT_HOST;ERROR_CODE_IF_PRESENT
NEVER_CAPTURE=COOKIE;AUTHORIZATION_HEADER;OAUTH_CODE;ACCESS_TOKEN;ID_TOKEN;CLIENT_SECRET;REDIRECT_TOKEN
```

## Authentication vs authorization

This validation explicitly distinguishes identity from access control.

- Authentication: the Google sign-in/IAP path must successfully establish a live user session in a fresh private browser session.
- Authorization: the authenticated user must also be a member of the judge group `mg-mcp-developer-mg@themiliare-group.com` before the protected service is allowed to serve the judge workflow.

Without both, the service remains unresolved. The validator must confirm the account identity and separately confirm the required judge-group prerequisite before treating the app behavior as valid evidence.

## Current status

```text
R2_DEPLOYMENT=COMPLETE
APPLICATION_RUNTIME=PASS
EXACT_IMAGE_SCENARIOS=PASS
AUTHENTICATED_JUDGE_ACCESS=PASS
HUMAN_OAUTH_FLOW=PASS
ERROR_9_JUDGE_ACCESS_BLOCKER=NO
ACTIVE_PRODUCT_DEVELOPMENT=YES
FINAL_SUBMISSION_PACKET=DEFER
```

This follow-up has reached the final evidence phase. The evaluator session authenticated successfully, the judge-group authorization prerequisite was confirmed, and the protected service was shown to reject direct unauthenticated access. The validation remains intentionally bounded and does not mutate the live service, app code, IAM, IAP, OAuth configuration, or secrets.

## Hard constraints

```text
DO_NOT_REDEPLOY_CLOUD_RUN=YES
DO_NOT_CHANGE_APPLICATION_CODE=YES
DO_NOT_CHANGE_IAM=YES
DO_NOT_CHANGE_IAP=YES
DO_NOT_CHANGE_OAUTH_CREDENTIALS=YES
DO_NOT_ROTATE_SECRETS=YES
```

No infrastructure changes are allowed until the diagnosis demonstrates exactly which configuration is defective and the evidence shows the correct evaluator session flow.

## Controlled browser validation plan

### 1. Fresh private-session isolation

- Open a new Incognito / private browser window.
- Ensure no reused Google session from developer or non-evaluator accounts is active.
- Confirm the browser has no stale cookies or previous service authorization state from earlier sessions.

### 2. Protected service entry and IAP challenge

- Navigate directly to the judge service protected URL.
- Verify the protected endpoint initiates the IAP auth challenge before returning application content.
- Capture the redirect chain without persisting any user secrets or tokens.

### 3. Explicit evaluator account selection

- Sign in using the confirmed evaluator account `buildweek-evaluator@themiliare-group.com`.
- Confirm the chosen account is the judge evaluator identity and not an incidental developer or personal Google session.
- If the account is not sufficient for authorization, record the path as an authorization failure rather than app failure.

### 4. Judge-group prerequisite confirmation

- Before trusting the authenticated session, confirm the evaluator is part of the required group `mg-mcp-developer-mg@themiliare-group.com`.
- If the member check is unresolved, mark `EVALUATOR_JUDGE_GROUP_MEMBERSHIP=TO_BE_CONFIRMED_BEFORE_TEST` and stop the test before claiming service access success.

### 5. OAuth callback and return-to-service

- Complete the Google sign-in callback in the same browser session.
- Verify the browser returns to the protected service and the service reaches the application route instead of remaining at the redirect boundary.

### 6. Service behavior proof

- Request `GET /health` from the authenticated session.
- Require HTTP 200 with `status=ok` and `judge_mode=stub`.
- Continue with the authenticated POST success scenario in the same session.
- Require HTTP 200 and `workflow_status=completed` with zero external effects.
- Confirm the user remains authenticated and does not fall back into a clear or re-redirect path.

### 7. Negative-control protection proof

- Sign out or clear the browser session state.
- Revisit the protected endpoint.
- Confirm the service again requires IAP authentication rather than serving protected content.

### 8. Evidence recording requirements

- Record only the necessary redirect chain, HTTP status values, and route outcomes.
- Separate authentication outcomes from authorization outcomes.
- Never persist cookies, authorization headers, OAuth codes, access tokens, ID tokens, client secrets, or redirect tokens in repo artifacts.

## Success and failure evidence contract

### On success capture

```text
ACCOUNT_IDENTITY=
HEALTH_HTTP_STATUS=
HEALTH_STATUS=
HEALTH_JUDGE_MODE=
SUCCESS_HTTP_STATUS=
SUCCESS_WORKFLOW_STATUS=
NEGATIVE_CONTROL_RESULT=
```

### On failure capture

```text
FAILURE_STAGE=
FAILURE_HOST=
FAILURE_PATH=
HTTP_STATUS=
PREVIOUS_REDIRECT_HOST=
NEXT_REDIRECT_HOST=
ERROR_CODE_IF_PRESENT=
```

### Never capture

```text
COOKIE
AUTHORIZATION_HEADER
OAUTH_CODE
ACCESS_TOKEN
ID_TOKEN
CLIENT_SECRET
REDIRECT_TOKEN
```

## Competition-development options packet

The following options are the highest-value work streams that can realistically be completed before feature freeze without reopening the infrastructure lane.

### Option 1: Judge-authentication and authorization investigation

```text
OPTION_1_STATUS=COMPLETE
COMPETITION_VALUE=VERY_HIGH
GOOGLE_TECH_VALUE=HIGH
MG_REUSABLE_VALUE=HIGH
IMPLEMENTATION_SCOPE=Diagnose the current private-session evaluator auth path; confirm the required judge-group membership; capture the IAP redirect and callback chain; validate both authentication and authorization in the same browser session without any live mutation.
DEMO_IMPACT=MEDIUM
RISK=MEDIUM
ESTIMATED_WORK=1-2 days
PROOF_REQUIRED=Fresh private-session proof showing redirect, explicit evaluator account selection, callback success, /health 200, same-session POST success 200, and a negative control that still requires IAP auth.
```

Why it matters: this option directly resolves the root cause and produces the clearest evidence path for final judge-facing confidence while preserving the approved deployment state.

### Option 2: Demo-grade workflow narrative and stage-policy clarity

```text
COMPETITION_VALUE=HIGH
GOOGLE_TECH_VALUE=MEDIUM
MG_REUSABLE_VALUE=HIGH
IMPLEMENTATION_SCOPE=Polish the guided narrative for the valid workflow states; tighten success, denied-stage, and ambiguous-contact messaging; clarify the decision flow for a judge/demo audience without changing service configuration.
DEMO_IMPACT=HIGH
RISK=LOW
ESTIMATED_WORK=1-3 days
PROOF_REQUIRED=Scenario smoke proofs and a concise demo script covering the expected user journey and policy explanations.
```

Why it matters: this option improves the product story and makes the live demo easier to explain and defend under competition conditions, with low technical risk.

### Option 3: Auditability and evidence packaging for competition review

```text
COMPETITION_VALUE=MEDIUM_HIGH
GOOGLE_TECH_VALUE=HIGH
MG_REUSABLE_VALUE=HIGH
IMPLEMENTATION_SCOPE=Add structured observability around health and workflow outcomes; package session-safe evidence and policy traces for review; prepare concise proof artifacts without exposing auth material or modifying infrastructure.
DEMO_IMPACT=MEDIUM
RISK=LOW
ESTIMATED_WORK=2-4 days
PROOF_REQUIRED=Evidence bundle showing successful scenario outcomes, no sensitive data leakage, and a clean validation narrative that separates identity, access, and workflow behavior.
```

Why it matters: this option creates durable proof hygiene and reviewer clarity without broad product changes or risky infrastructure mutation.

## Recommended next work item

```text
RECOMMENDED_NEXT_WORK_ITEM=SEE_ACTIVE_COMPETITION_WORK_LANE
```

The auth-validation proof is complete. The next step is to hand off into the active competition work lane for broader product demo narrative and policy clarity rather than continuing infrastructure auth work.

## Final validation evidence

```text
AUTHENTICATION_RESULT=PASS
AUTHORIZATION_RESULT=PASS
HEALTH_HTTP_STATUS=200
SUCCESS_HTTP_STATUS=200
SUCCESS_WORKFLOW_STATUS=completed
SUCCESS_EXTERNAL_EFFECTS=0
SUCCESS_CLOUD_MUTATION=NONE
NEGATIVE_CONTROL_RESULT=PROTECTED
CLOUD_MUTATION=NONE
```

The same authenticated evaluator session produced a successful `SUCCESS` request with HTTP 200 and `workflow_status=completed`, while a brand-new unauthenticated private window was protected by the IAP sign-in challenge and did not return app JSON directly. No cloud mutation occurred during the validation.

## Closeout signal

```text
AUTH_VALIDATION_PLAN_READY=YES
TOP_COMPETITION_WORK_OPTIONS=3
RECOMMENDED_NEXT_WORK_ITEM=SEE_ACTIVE_COMPETITION_WORK_LANE
STOP_CODE=NW007_AUTH_VALIDATION_PROOF_READY_FOR_HUMAN_MERGE
```

The lane is ready for human merge review. All validation evidence is complete, the judge-group authorization requirement is confirmed, and no infrastructure mutation is allowed beyond this documented proof state.
