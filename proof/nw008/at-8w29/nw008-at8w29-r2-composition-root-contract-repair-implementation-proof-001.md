UNIT=NW008_AT8W29_R2_COMPOSITION_ROOT_CONTRACT_REPAIR_IMPLEMENTATION_001
AUTHORIZATION_PR=209
AUTHORIZATION_MERGE_COMMIT=6657ca9e427cc243f56f4532586fa3971ebfe9b7
AUTHORIZATION_STATE=CONSUMED
AUTHORIZATION_REUSABLE=NO
AUTHORIZATION_TRANSFERABLE=NO

CHANGED_PATHS=
- src/integrations/ghl/highlevel_rest/live_note_runtime.py
- tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
- proof/nw008/at-8w29/nw008-at8w29-r2-composition-root-contract-repair-implementation-proof-001.md

CREDENTIAL_OWNERSHIP_REPAIR=PASS
SHARED_RUNTIME_CREDENTIAL_OBJECT=YES
SHARED_SECRET_MANAGER_CLIENT=YES
C4_AND_B2_SHARED_CLIENT=YES

STORE_LIFECYCLE_REPAIR=PASS
POST_STORE_FAILURE_CLOSE_GUARANTEE=YES
SUCCESSFUL_STORE_OWNERSHIP_TRANSFER=YES

CASE_B2_SECRET_ACQUISITION_FAILURE=PASS
CASE_HTTP_CLIENT_CONSTRUCTION_FAILURE=PASS
CASE_TRANSPORT_CONSTRUCTION_FAILURE=PASS
CASE_ADAPTER_CONSTRUCTION_FAILURE=PASS
CASE_SUCCESS=PASS

DETERMINISTIC_TEST_COMMANDS=
- PYTHONPATH=src uv run --no-project --with pytest==8.3.5 --with PyYAML==6.0.2 --with jsonschema==4.23.0 python -m pytest tests/integrations/ghl/highlevel_rest/test_live_note_runtime.py
- PYTHONPATH=src uv run --no-project --with pytest==8.3.5 --with PyYAML==6.0.2 --with jsonschema==4.23.0 python -m pytest tests/integrations/ghl/highlevel_rest/test_live_note_credential_provider.py tests/integrations/ghl/test_at1_commitment_key_provider.py tests/integrations/ghl/highlevel_rest/test_note_path_at1_execution_store.py
- PYTHONPATH=src uv run --python 3.11 --no-project --with-requirements requirements.txt python scripts/verify_phase1_deterministic.py
- PYTHONPATH=src uv run --python 3.11 --no-project --with-requirements requirements.txt python -m pytest -q
DETERMINISTIC_TESTS=PASS

LIVE_SECRET_READS=0
IMPERSONATION_ATTEMPTS=0
TOKEN_MINTS=0
SQLITE_LIVE_OPENS=0
HIGHLEVEL_CALLS=0
HTTP_REQUEST_DISPATCHES=0
CRM_MUTATIONS=0
IAM_MUTATIONS=0
DEPLOYMENTS=0

R2_EXECUTION_PERFORMED=NO
RESULT=PASS
STOP_CODE=NONE
