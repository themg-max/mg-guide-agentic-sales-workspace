#!/usr/bin/env python3
"""NW-005 Stage B Wave 1 authorized Firestore smoke runner.

Authorized by: MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1
Target: mg-devpost / devpost-google-contest / us-east4 / workflow_runs
Run ID: run_nw006_success_001

Call graph:
1. create workflow_runs/run_nw006_success_001
2. exact get same document
3. validate schema
4. verify exact run_id
5. recompute readback content fingerprint using Stage A logic
6. require triple equality of content fingerprints
7. exact delete same document
8. exact get same document expecting NOT_FOUND
9. STOP

This script uses Application Default Credentials. No service-account JSON keys.
Only synthetic fixture data is used.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from mg_guide.firestore_audit.firestore_store import (
    AUTHORIZED_COLLECTION,
    AUTHORIZED_DATABASE,
    AUTHORIZED_LOCATION,
    AUTHORIZED_PROJECT,
    FirestoreAuditStore,
    FirestoreAuditStoreError,
    WAVE1_RUN_ID,
)
from mg_guide.firestore_audit.models import ProjectionContext
from mg_guide.firestore_audit.project import project_workflow_run_audit

RUN_ID = WAVE1_RUN_ID
PROJECT = AUTHORIZED_PROJECT
DATABASE = AUTHORIZED_DATABASE
LOCATION = AUTHORIZED_LOCATION
COLLECTION = AUTHORIZED_COLLECTION
AUTHORIZATION_ID = "MG_GUIDE_NW005_FIRESTORE_AUDIT_TEST_PROJECT_PROOF_V1"

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_PATH = REPO_ROOT / "fixtures" / "nw005" / "packets" / "packet-success.completed.json"


def _load_packet():
    return json.loads(PACKET_PATH.read_text(encoding="utf-8"))


def _project_audit():
    packet = _load_packet()
    recorded_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ctx = ProjectionContext(
        recorded_at=recorded_at,
        fixture_id="packet-success.completed.json",
        source_refs=("fixtures/nw005/packets/packet-success.completed.json",),
        writer_component="mg_guide.firestore_audit.firestore_store",
        writer_component_version="0.1.0-stage-b",
        writer_mode="firestore_test_project",
    )
    return project_workflow_run_audit(packet, ctx)


def _cleanup(store: FirestoreAuditStore) -> bool:
    """Attempt cleanup and return whether the document is NOT_FOUND."""
    try:
        store.delete_exact(RUN_ID)
    except Exception:
        pass
    try:
        store.require_not_found_after_delete(RUN_ID)
        return True
    except Exception:
        return False


def main() -> int:
    started_at = datetime.now(timezone.utc).isoformat()

    result = {
        "AUTHORIZATION_ID": AUTHORIZATION_ID,
        "BASELINE_MERGE_SHA": "1d9ff931dd431ce04f47ad907b08252b433d23c9",
        "IMPLEMENTATION_HEAD_SHA": None,
        "RUN_ID": RUN_ID,
        "PROJECT": PROJECT,
        "DATABASE": DATABASE,
        "LOCATION": LOCATION,
        "COLLECTION": COLLECTION,
        "FIRESTORE_CREATE_ATTEMPTED": "YES",
        "FIRESTORE_CREATE_VERIFIED": "NO",
        "FIRESTORE_READBACK_VERIFIED": "NO",
        "RUN_ID_MATCH": "NO",
        "SCHEMA_VALID_AFTER_READBACK": "NO",
        "EXPECTED_PROJECTED_CONTENT_FINGERPRINT": None,
        "STORED_CONTENT_FINGERPRINT": None,
        "RECOMPUTED_READBACK_CONTENT_FINGERPRINT": None,
        "CONTENT_FINGERPRINT_MATCH": "NO",
        "DELETE_ATTEMPTED": "NO",
        "DELETE_VERIFIED": "NO",
        "DELETE_GET_NOT_FOUND": "NO",
        "STAGE_B_DOCUMENT_CREATES": 0,
        "STAGE_B_DOCUMENT_READS": 0,
        "STAGE_B_DOCUMENT_DELETES": 0,
        "STAGE_B_NETWORK_CALLS": 0,
        "STAGE_B_AUTHORIZED_MUTATING_EXTERNAL_EFFECTS": 0,
        "REAL_CUSTOMER_DATA": 0,
        "GHL_LIVE_CALLS": 0,
        "CLEANUP_STATUS": "NOT_ATTEMPTED",
        "RESULT": "FAIL",
        "STARTED_AT": started_at,
        "COMPLETED_AT": None,
        "ERROR": None,
    }

    try:
        audit = _project_audit()
        expected_fp = audit["integrity"]["content_fingerprint"]
        result["EXPECTED_PROJECTED_CONTENT_FINGERPRINT"] = expected_fp

        store = FirestoreAuditStore(
            project=PROJECT,
            database=DATABASE,
            collection=COLLECTION,
            retention_mode="stage_b_smoke",
        )

        store.create_exact(RUN_ID, audit)
        result["FIRESTORE_CREATE_VERIFIED"] = "YES"

        readback = store.get_exact(RUN_ID)
        if readback is None:
            raise FirestoreAuditStoreError(
                "FIRESTORE_NOT_FOUND_AFTER_CREATE",
                "document missing immediately after create",
            )

        verification = store.verify_readback(readback, RUN_ID, expected_fp)
        result["FIRESTORE_READBACK_VERIFIED"] = "YES"
        result["RUN_ID_MATCH"] = "YES" if verification["run_id_match"] else "NO"
        result["SCHEMA_VALID_AFTER_READBACK"] = "YES" if verification["schema_valid"] else "NO"
        result["STORED_CONTENT_FINGERPRINT"] = verification["stored_content_fingerprint"]
        result["RECOMPUTED_READBACK_CONTENT_FINGERPRINT"] = verification[
            "recomputed_content_fingerprint"
        ]
        result["CONTENT_FINGERPRINT_MATCH"] = (
            "YES"
            if verification["stored_content_fingerprint"]
            == verification["recomputed_content_fingerprint"]
            == expected_fp
            else "NO"
        )

        result["DELETE_ATTEMPTED"] = "YES"
        store.delete_exact(RUN_ID)
        result["DELETE_VERIFIED"] = "YES"

        store.require_not_found_after_delete(RUN_ID)
        result["DELETE_GET_NOT_FOUND"] = "YES"
        result["CLEANUP_STATUS"] = "SUCCESS"
        result["RESULT"] = "PASS"

    except Exception as exc:
        result["ERROR"] = f"{type(exc).__name__}: {exc}"
        result["CLEANUP_STATUS"] = "ATTEMPTING"
        cleanup_ok = _cleanup(store) if "store" in locals() else False
        result["CLEANUP_STATUS"] = "SUCCESS" if cleanup_ok else "FAILURE"
        if cleanup_ok:
            result["DELETE_GET_NOT_FOUND"] = "YES"

    finally:
        if "store" in locals():
            result["STAGE_B_DOCUMENT_CREATES"] = store.creates
            result["STAGE_B_DOCUMENT_READS"] = store.reads
            result["STAGE_B_DOCUMENT_DELETES"] = store.deletes
            result["STAGE_B_NETWORK_CALLS"] = store.creates + store.reads + store.deletes
            result["STAGE_B_AUTHORIZED_MUTATING_EXTERNAL_EFFECTS"] = (
                store.creates + store.deletes
            )

        result["COMPLETED_AT"] = datetime.now(timezone.utc).isoformat()
        result["IMPLEMENTATION_HEAD_SHA"] = (
            (REPO_ROOT / ".git")
            .joinpath("refs", "heads", "feat", "nw005-stage-b-firestore-smoke")
            .read_text(encoding="utf-8")
            .strip()
            if (REPO_ROOT / ".git").is_dir()
            else None
        )

    print(json.dumps(result, indent=2))
    return 0 if result["RESULT"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
