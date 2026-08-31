#!/usr/bin/env python3
"""Deterministically enforce Agent Runtime Terraform ownership boundaries."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "infra" / "agent-runtime"
APPROVED_RUNTIME_SA = (
    "mg-guide-agent-runtime@ai-rolodex-to-crm.iam.gserviceaccount.com"
)


def fail(message: str) -> None:
    print(f"POLICY_CHECK=FAIL {message}")
    raise SystemExit(1)


def terraform_sources() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(ROOT.rglob("*.tf"))
        if ".terraform" not in path.parts
    )


def require_absent(sources: str, pattern: str, label: str) -> None:
    if re.search(pattern, sources):
        fail(label)
    print(f"{label}=PASS")


def main() -> None:
    if not ROOT.is_dir():
        fail(f"authoritative root missing: {ROOT}")

    sources = terraform_sources()
    dev_tfvars = (ROOT / "environments" / "dev.tfvars").read_text(encoding="utf-8")

    require_absent(
        sources,
        r'resource\s+"google_service_account"',
        "NO_GOOGLE_SERVICE_ACCOUNT_RESOURCE",
    )
    require_absent(
        sources,
        r'resource\s+"google_service_account_key"',
        "NO_SERVICE_ACCOUNT_KEY_RESOURCE",
    )
    require_absent(
        sources,
        r'resource\s+"google_project_iam_member"',
        "NO_PROJECT_VERTEX_IAM_RESOURCE",
    )
    require_absent(
        sources,
        r'resource\s+"google_secret_manager_[^"]+"',
        "NO_SECRET_RESOURCE",
    )
    require_absent(sources, r"mg-guide-orchestrator-app", "NO_MG_GUIDE_ORCHESTRATOR_APP")

    variable = re.search(
        r'variable\s+"runtime_service_account_email"\s*\{(?P<body>.*?)^\}',
        sources,
        re.DOTALL | re.MULTILINE,
    )
    if variable is None or re.search(r"^\s*default\s*=", variable.group("body"), re.MULTILINE):
        fail("RUNTIME_SA_VARIABLE_REQUIRED")
    print("RUNTIME_SA_VARIABLE_REQUIRED=PASS")

    if not re.search(
        r"service_account\s*=\s*var\.runtime_service_account_email\b", sources
    ):
        fail("RUNTIME_RESOURCE_USES_SA_VARIABLE")
    print("RUNTIME_RESOURCE_USES_SA_VARIABLE=PASS")

    expected_binding = (
        r'runtime_service_account_email\s*=\s*(?:\(\s*)?"'
        + re.escape(APPROVED_RUNTIME_SA)
        + r'"'
    )
    if not re.search(expected_binding, dev_tfvars, re.DOTALL):
        fail("DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA")
    print("DEV_BINDING_EQUALS_APPROVED_RUNTIME_SA=PASS")

    state_files = [
        path.relative_to(ROOT)
        for path in ROOT.rglob("*")
        if path.is_file() and (path.name.endswith(".tfstate") or ".tfstate." in path.name)
    ]
    if state_files:
        fail(f"NO_TERRAFORM_STATE_FILES ({', '.join(map(str, state_files))})")
    print("NO_TERRAFORM_STATE_FILES=PASS")


if __name__ == "__main__":
    main()
