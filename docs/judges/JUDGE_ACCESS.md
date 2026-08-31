# Judge access

```text
SURFACE=docs/judges/JUDGE_ACCESS.md
JUDGE_ACCOUNT_EMAIL=airolodex.judge@themiliare-group.com
JUDGE_ACCOUNT_TYPE=controlled competition Google Workspace account
PUBLIC_PASSWORD_STORAGE=FORBIDDEN
```

## Competition account

Email: `airolodex.judge@themiliare-group.com`

Account type: controlled competition Google Workspace account.

The password / access secret is provided privately through the Devpost testing
credentials / authorized judge instructions. It is intentionally not committed
to this public repository.

```text
PUBLIC_PASSWORD_STORAGE=FORBIDDEN
PASSWORD_IN_README=NO
PASSWORD_IN_THIS_FILE=NO
```

## How access works

1. Credentials are delivered privately through the competition testing
   instructions.
2. Judges sign in with the competition Workspace account above.
3. That Workspace identity is used to access the competition MG Guide surface
   (Gmail and/or Calendar add-on).
4. The demonstration uses synthetic / test data.
5. The judge account must not be used for unrelated services.

The Workspace add-on is a thin presentation and routing adapter. Auth details
for the adapter contract are in
[mg-guide-workspace-addon-auth-contract-v1.md](../architecture/mg-guide-workspace-addon-auth-contract-v1.md).

```text
ROLE=THIN_PRESENTATION_AND_ROUTING_ADAPTER
JUDGE_ACCOUNT_TYPE=CONTROLLED_INTERNAL_WORKSPACE
REAL_CUSTOMER_DATA=NO
```

## What to run

After signing in:

1. Open Gmail or Calendar.
2. Launch **MG Guide**.
3. Run **Meeting Follow-Up**.
4. Execute **SUCCESS**.
5. Execute **AMBIGUOUS_CONTACT**.

| Scenario | Expected behavior |
| --- | --- |
| SUCCESS | Completed follow-up plan |
| AMBIGUOUS_CONTACT | Needs-review / fail-closed; no unauthorized CRM effect |

Do not expect this public repository to publish install URLs, Marketplace
listings, private backend URLs, or deployment identifiers.

## Do not publish or request from this repo

This public tree must not contain:

- password
- identity tokens
- OAuth client secrets
- private backend URLs
- deployment IDs
- private Script IDs
- private audience values

If a testing secret is missing, use the private Devpost / operator channel.
Do not look for it in GitHub.

## Boundary

- No live HighLevel mutation on the judge demonstration path.
- No real-customer data.
- Historical CRM proof is separate from the judge demonstration.
