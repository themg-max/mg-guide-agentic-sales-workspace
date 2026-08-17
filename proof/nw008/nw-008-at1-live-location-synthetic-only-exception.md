# NW-008 AT-1 -- Live Location Synthetic-Only Exception

```text
DECISION_ID=NW008_AT1_LIVE_LOCATION_EXCEPTION_001
DECISION_TYPE=HUMAN_LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION
APPROVING_AUTHORITY=HUMAN_GHL_SPACE_OWNER
ISOLATED_GHL_TEST_LOCATION=NO
DEDICATED_TEST_LOCATION_AVAILABLE=NO
LIVE_GHL_LOCATION_REQUIRED=YES
LIVE_LOCATION_SYNTHETIC_ONLY_EXCEPTION_APPROVED=YES
OLD_LOCATION_BINDING=NW008_GHL_LOCATION_PRIVATE_V1
OLD_LOCATION_BINDING_STATUS=SUPERSEDED_FOR_NW008_AT1
NEW_PRIVATE_LOCATION_BINDING_REF=NW008_GHL_LIVE_LOCATION_PRIVATE_V2
NEW_PRIVATE_LOCATION_SOURCE=RESULT005_EXACT_OPPORTUNITY_RETURNED_LOCATION
SYNTHETIC_CONTACT_ONLY=YES
SYNTHETIC_OPPORTUNITY_ONLY=YES
PRODUCTION_CUSTOMER_RECORD_MUTATION_AUTHORIZED=NO
SEARCH_FOR_ALTERNATE_TARGET=NO
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
```

## Human approval statement

The approving human authority confirms that the relevant live GHL location is
business-active and non-isolated. There is no dedicated test location available
for NW-008. The location is therefore explicitly exempted from the previously
unattainable isolated-test-location prerequisite, but only under a synthetic-only
control regime.

The human approval further states that:

- the live location is business-active / non-isolated
- a dedicated test location is unavailable
- only the preverified synthetic contact/opportunity may be targeted
- no customer records may be mutated
- this exception does not authorize AT-1 mutation execution
- no alternate target search is authorized
- the old NW-008 location binding is superseded for this task, and the private
  live-location binding is rebound as `NW008_GHL_LIVE_LOCATION_PRIVATE_V2`

The approval is deliberately fail-closed: no production customer or live
non-synthetic record may be read, searched, created, updated, or mutated under
this exception. Only the preverified synthetic contact/opportunity may be used,
and only for read-only verification work that is already bounded by the private
control-plane evidence associated with Result 005.

## Private rebind evidence (sanitized public proof only)

```text
LOCATION_FP_MATCH=YES
PIPELINE_FP_MATCH=YES
STAGE_FP_MATCH=YES
PRIVATE_BINDING_PUBLICATION=NO
```

The old private location binding remains historical as
`NW008_GHL_LOCATION_PRIVATE_V1`; the live location binding for NW-008 AT-1 is
rebound privately to `NW008_GHL_LIVE_LOCATION_PRIVATE_V2` using the exact
opportunity-returned location evidence from Result 005. No raw private IDs or
payloads are published in this repository.

## STOP

```text
STOP_CODE=NW008_AT1_LIVE_LOCATION_EXCEPTION_FROZEN
LIVE_LOCATION_EXCEPTION_APPROVED=YES
AT1_EXECUTION_AUTHORIZED=NO
AT1_COMPLETE=NO
ENVIRONMENT_READY=NO
PRIVATE_BINDING_PUBLICATION=NO
```
