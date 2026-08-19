"""Workspace add-on thin presentation adapter (competition surface).

CardService Apps Script sources live under workspace_addon/.
This package provides pure projection + auth validation used by tests and
optional judge-surface identity-token mode.
"""

from __future__ import annotations

from .auth_contract import (
    AUTH_CONTRACT_ID,
    AuthError,
    AuthMode,
    validate_authorization_header,
)
from .cardservice_projection import (
    ERROR_AUTH,
    ERROR_BACKEND,
    ERROR_INVALID,
    ERROR_SCENARIO_BLOCKED,
    project_cardservice_home,
    project_cardservice_result,
    project_error_card,
)
from .security import assert_no_raw_token_logging, scan_text_for_token_leak

__all__ = [
    "AUTH_CONTRACT_ID",
    "AuthError",
    "AuthMode",
    "ERROR_AUTH",
    "ERROR_BACKEND",
    "ERROR_INVALID",
    "ERROR_SCENARIO_BLOCKED",
    "assert_no_raw_token_logging",
    "project_cardservice_home",
    "project_cardservice_result",
    "project_error_card",
    "scan_text_for_token_leak",
    "validate_authorization_header",
]
