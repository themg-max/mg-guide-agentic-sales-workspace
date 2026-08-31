# MG Guide Agent Runtime Deployment Candidate Source Proof 001

## Candidate identity

```text
ARTIFACT_ID=
  MG_GUIDE_AGENT_RUNTIME_DEPLOYMENT_CANDIDATE_SOURCE_PROOF_001
ARTIFACT_PATH=
  proof/mg-guide/agent-runtime/mg-guide-agent-runtime-deployment-candidate-source-proof-001.md
PR_CLASS=BOUNDED_PROOF

PR_379_MERGE_SHA=
  07ff5235af591cccdd1098d40240bb8c64fff05f
SOURCE_BASE_COMMIT=
  eebd09055de2e72c7dce6ebf0f202a415a362a81

ROOT_AGENT_MODULE=app.agent
ROOT_AGENT_SOURCE=
  deployment/agent-runtime/app/agent.py
ROOT_AGENT_FACTORY=
  agents.follow_up_planning.runtime.build_unit3_root_agent

REUSE_EXISTING_AGENT_GRAPH=YES
REUSE_EXISTING_DELEGATES=YES
SHARED_ROOT_AGENT_FACTORY=YES
NESTED_ADK_RUNNER=NO
```

The source candidate is the checked-in MG Guide Unit 3 business graph. Its
root is `unit3_meeting_to_follow_up_packet`, with these ordered delegates:

```text
meeting_context_agent
relationship_context_agent
follow_up_planning_agent
```

The public root factory constructs the existing ADK `SequentialAgent` and its
three deterministic delegate wrappers. It does not construct a `Runner`.
`Unit3FollowUpRuntime` reuses that factory for local execution and remains the
owner of its one local runner. The deployment entrypoint exports the shared
root directly so Agent Runtime, rather than a nested application runtime, owns
deployed execution.

The candidate contains none of the generated synthetic weather/time scaffold.

## Deterministic package manifest

The candidate was built twice from the immutable Git object named by
`SOURCE_BASE_COMMIT` using:

```text
python3 scripts/build_agent_runtime_source.py \
  --source-commit eebd09055de2e72c7dce6ebf0f202a415a362a81 \
  --output <SESSION_EPHEMERAL_ZIP>
```

The builder reads only committed Git blobs, sorts every archive path, uses the
fixed ZIP timestamp `1980-01-01T00:00:00`, stores deterministic file modes, and
uses `ZIP_STORED`. The two independent outputs were byte-identical.

```text
SOURCE_PACKAGE_SHA256=
  6dcbb700c57b0e885f02a60b0cad50b1c0478f398a7c8421656857a08aff6bab
SOURCE_PACKAGE_SIZE_BYTES=343228
SOURCE_PACKAGE_FILE_COUNT=54
SOURCE_PACKAGE_REBUILD_BYTE_IDENTICAL=YES
SOURCE_PACKAGE_COMMITTED_TO_REPOSITORY=NO
SOURCE_PACKAGE_BASE64_COMMITTED_TO_REPOSITORY=NO
```

### Included paths

```text
PACKAGE_INCLUDE_PATHS=
  app/__init__.py
  app/agent.py
  requirements.txt
  SOURCE_MANIFEST.sha256
  src/agents/__init__.py
  src/agents/adk_runtime/*.py
  src/agents/follow_up_planning/*.py
  src/agents/meeting_context/*.py
  src/agents/meeting_context/providers/*.py
  src/agents/relationship_context/*.py
  src/integrations/__init__.py
  src/integrations/ghl/read_adapter.py
  src/orchestration/__init__.py
  src/orchestration/attempt_ledger.py
  src/orchestration/models.py
  src/orchestration/policy.py
  src/orchestration/runner.py
  src/orchestration/state_machine.py
  contracts/follow_up_proposal.schema.json
  contracts/meeting_context.schema.json
  contracts/meeting_follow_up_packet.schema.json
  contracts/nw008_longitudinal_context.schema.json
  contracts/relationship_context.schema.json
  contracts/workflow_states.yaml
  fixtures/ghl/relationship-context-crm.json
  fixtures/transcript-success.expected.json
  fixtures/transcript-success.txt
```

The three included fixture files are checked-in synthetic data. The CRM
fixture declares `"source": "synthetic_only"` and uses reserved example-domain
addresses and fictional identifiers. It is included only so the initial
synthetic-only root can resolve relationship context without network access.

### Excluded paths

```text
PACKAGE_EXCLUDE_PATHS=
  .git/**
  .env
  **/credentials*
  **/service-account*
  **/*-key.json
  **/*.pem
  **/.terraform/**
  **/*.tfstate*
  **/__pycache__/**
  **/.pytest_cache/**
  artifacts/**
  **/traces/**
  proof/**
  tests/**
  private CRM fixtures/data
  evaluation trace bodies
  generated mg-guide-orchestrator weather/time scaffold
  src/integrations/ghl/highlevel_rest/**
  src/integrations/ghl/*live*
  src/integrations/ghl/*secret*
  src/integrations/ghl/*credential*
```

The offline relationship store imports
`integrations.ghl.read_adapter.OfflineGhlReadAdapter` directly. The package
therefore does not import or include the repository's live HighLevel transport,
credential, secret-access, or mutation modules.

```text
SECRETS_INCLUDED=NO
PRIVATE_DATA_INCLUDED=NO
LIVE_GHL_CODE_INCLUDED=NO
TERRAFORM_STATE_INCLUDED=NO
EVALUATION_TRACE_BODIES_INCLUDED=NO
```

## Package validation

The archive digest was checked before extraction. Validation ran in a temporary
directory with `PYTHONPATH` limited to the extracted package and its `src`
directory.

The package imported `app.agent`, loaded the public shared root, asserted the
ordered three-delegate graph, and ran one synthetic success scenario through a
single external ADK `Runner`. The final state contained a schema-valid
`meeting_follow_up_packet_v1`, intent-only mutations, and zero external
effects.

```text
PACKAGE_IMPORT=PASS
ROOT_AGENT_LOAD=PASS
SYNTHETIC_SMOKE=PASS

LIVE_GHL_ADAPTER_ENABLED=NO
GHL_CALLS=0
CRM_MUTATIONS=0
EXTERNAL_EFFECTS=0
```

No model, IAM, secret, HighLevel, CRM, Terraform apply, or Agent Runtime deploy
operation was invoked to produce this proof.

```text
DEPLOYMENT_AUTHORIZED=NO
DEPLOYMENT_EXECUTED=NO
AGENT_RUNTIME_DEPLOYMENTS=0
```
