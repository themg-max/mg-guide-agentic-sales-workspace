# NW-008 Tranche D — D1 (AT-9) Governance Closeout

## Closeout truth

| Field | Value |
| --- | --- |
| Work item | NW-008 |
| Tranche | D |
| Scope | D1 / AT-9 manifest refusal gate — **governance closeout only** |
| Lane | `feat/nw008-tranche-d-d1-at9` |
| Closed at | `2026-08-14` |
| Overall NW-008 status | `IN_PROGRESS` |

## Final technical subjects

```text
A1R2=ab17da29fce5c134eb865e07c30f208e8d61b394
P1R2=64daa993b1e7a37455e0c4d41f62e55168eedc3b
```

- `A1R2` — implementation subject: D1 manifest gate authority repair.
- `P1R2` — proof subject: computed D1 proof integrity record.

## Superseded history

```text
A1=3be4309c02e2fc5e0685eadaba5a997b3cb8d81a
P1=500f50c34e84575491c1690c9d622e173e45860b
STATUS=INVALID_FOR_ACCEPTANCE

A1R=928a25995e732fc773818809d9865b8f34c58cb9
P1R=12cf1a510013abce93f128fac633972184dd239a
STATUS=SUPERSEDED_BY_GOVERNANCE_REVIEW
REASON=proof predicates were partially self-declared before A1R2/P1R2 repair
```

## Required closeout evidence

Bound to final subjects `A1R2` / `P1R2`. Durable proof artifacts:
`proof/nw008/tranche-d/proof-manifest.md`,
`proof/nw008/tranche-d/proof-return.yaml`,
`proof/nw008/tranche-d/at-09-run.json`,
`proof/nw008/tranche-d/at-09-workflow-run-audit.json`.

```text
MANIFEST_PATH=contracts/ghl_tool_manifest.yaml
MANIFEST_NODE=ghl_mcp.blocked_capability_classes
MALFORMED_MANIFEST_FAILS_CLOSED=YES
UNKNOWN_OPERATION_FAILS_CLOSED=YES
REQUESTED_OPERATION=create-contact
CAPABILITY_CLASS=contact_create
MANIFEST_BLOCKED=true
TOOL_MANIFEST_REFUSED=true
REFUSAL_LAYER=TOOL_MANIFEST
DOWNSTREAM_EXECUTOR_CALLED=false
TRANSPORT_ATTEMPTED=false
AUDIT_WARNING_RECORDED=true
AUDIT_WARNING_PROJECTED_STAGE_A=true
STAGE_B_SPY_CALLED=false
FIRESTORE_STAGE_B_INSTANTIATED=false
FIRESTORE_STAGE_B_CALLED=false
NC_D1_1=PASS
NC_D1_2=PASS
NC_D1_3=PASS
NC_D1_4=PASS
NC_D1_5=PASS
NC_D1_6=PASS
NC_D1_7=PASS
NC_D1_8=PASS
PROOF_VALIDATOR=PASS
DETERMINISTIC_PROOF_REPLAY=PASS
GHL_LIVE_CALLS=0
GHL_WRITES=0
FIRESTORE_WRITES=0
EXTERNAL_EFFECTS=0
TRANCHE_C_PROOF_MUTATED_BY_D1=NO
TRANCHE_C_TREE=33257929a2b16cf005fd5a95a914e2dc7389c71a
TARGETED_TESTS=PASS
FULL_SUITE=288_PASS
```

## Final disposition

```text
D1_RUNTIME_BEHAVIOR=GREEN
D1_PROOF_INTEGRITY=GREEN
D1_GOVERNANCE_CLOSEOUT=COMPLETE
D1_GATE_FOR_D2=TECHNICALLY_OPEN
D1_HUMAN_REVIEW_REQUIRED_BEFORE_D2=SATISFIED
D2_IMPLEMENTATION_STARTED=NO
```

## Scope statement

This closeout is governance-only. It introduces no runtime semantics changes
and no changes to `contracts/**`, `proof/nw008/tranche-c/**`, `deploy/**`,
`infra/**`, `.github/workflows/**`, IAM/secrets/cloud, GHL live transport,
Firestore Stage B activation, packet/audit schema, policy semantics, or
manifest blocked-class definitions. D2/AT-8 implementation is explicitly not
started in this lane.

## STOP

```text
STOP_CODE=NW008_TRANCHE_D_D1_GOVERNANCE_CLOSEOUT_COMPLETE_STOP_BEFORE_D2
```
