# NW-008 - Transcript-to-Runner Composition Closure 001

```text
ARTIFACT_ID=NW008_TRANSCRIPT_TO_RUNNER_COMPOSITION_CLOSURE_001
ARTIFACT_KIND=OFFLINE_DETERMINISTIC_COMPOSITION_PROOF
MODE=SYNTHETIC_ONLY

LIVE_GHL_READ_CALLS=0
LIVE_GHL_WRITE_CALLS=0
CRM_MUTATIONS=0
ONE_SHOT_GRANT_CREATED=NO
EXECUTION_AUTHORIZED=NO
GRANT_PREPARATION_READY=NO
SUBMISSION_READY=NO
```

Normalized proof boundary:

```text
FIXTURE_PROVIDER_SEMANTIC_INFERENCE_CLAIMED=NO
PROCESSOR_ENTRYPOINT_EXECUTED=YES
PROCESSOR_OUTPUT_BOUND_TO_SOURCE_TRANSCRIPT_HASH=YES
PROCESSOR_OUTPUT_TO_CANONICAL_NOTE_DERIVATION=YES
CANONICAL_NOTE_TO_RUNNER_BINDING=YES
PR253_PREWRITE_SEAL_BINDING=YES
LIVE_GEMINI_EXTRACTION_PROVEN=NO
```


## Composition boundary

`TranscriptToRunnerComposition.build` accepts a synthetic transcript and invokes
the actual `MeetingContextAgent.for_fixture_mode().run` entrypoint. It captures
the canonical JSON bytes of that output, then derives the canonical note bytes
from those captured bytes only.

The composition API accepts only the six exact CRM/stage target fields. It does
not accept an expected-note field. It creates the `BoundedAt1Input` internally
with:

```text
BoundedAt1Input.transcript_content = source transcript bytes
BoundedAt1Input.expected_note_content_or_fingerprint = derived canonical note bytes
```

Immediately before constructing the PR253 bounded runner, the composition
recomputes and validates:

```text
source transcript SHA256
processor-output SHA256
canonical note bytes from processor output
canonical note SHA256
runner transcript exact-byte equality
runner expected-note exact-byte equality
```

The offline transport wrapper records the arguments received by PR253's
`_seal_prewrite_provenance` hook and verifies that it received those same source
transcript and canonical-note bytes and SHA256 digests.

## Deterministic evidence

```text
SOURCE_TRANSCRIPT_PRESENT=YES
SOURCE_TRANSCRIPT_SHA256_CAPTURED=YES
TRANSCRIPT_PROCESSOR_INVOKED=YES
TRANSCRIPT_PROCESSOR_OUTPUT_CAPTURED=YES
CANONICAL_NOTE_DERIVED_FROM_PROCESSOR_OUTPUT=YES
CANONICAL_NOTE_SHA256_CAPTURED=YES
RUNNER_EXPECTED_NOTE_BYTES_EQUAL_DERIVED_NOTE_BYTES=YES
RUNNER_EXPECTED_NOTE_SHA256_EQUAL_DERIVED_NOTE_SHA256=YES
PR253_PREWRITE_SEAL_RECEIVES_SAME_TRANSCRIPT=YES
PR253_PREWRITE_SEAL_RECEIVES_SAME_CANONICAL_NOTE=YES
INDEPENDENT_NOTE_INJECTION_PATH_USED=NO
```

## Fail-closed coverage

`tests/orchestration/test_transcript_to_runner_composition.py` proves each
condition fails before a synthetic transport dispatch:

```text
TRANSCRIPT_CHANGED_AFTER_DERIVATION=FAIL
DERIVED_NOTE_CHANGED_BEFORE_RUNNER=FAIL
RUNNER_NOTE_DIFFERS_FROM_PROCESSOR_OUTPUT=FAIL
MISSING_PROCESSOR_PROVENANCE=FAIL
MISSING_TRANSCRIPT_HASH=FAIL
MISSING_DERIVED_NOTE_HASH=FAIL
```

The successful case preserves the exact six-operation PR253 order and one
note-write/one stage-write attempt bound. No search, list, pagination, retry,
fallback, cleanup, or compensating mutation is introduced.
