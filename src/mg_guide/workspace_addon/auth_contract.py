"""Apps Script OIDC identity-token auth contract for the MG Guide add-on.

Does not log token values. Does not implement IAP, API keys, or MCP auth.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Tuple

AUTH_CONTRACT_ID = "MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1"
GOOGLE_ISSUERS = frozenset({"https://accounts.google.com", "accounts.google.com"})
GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
LOCAL_DEMO_HEADER = "X-MG-Guide-Demo-Auth"
LOCAL_DEMO_VALUE = "local-demo"


class AuthMode(str, Enum):
    OFF = "off"
    IDENTITY_TOKEN = "identity_token"
    LOCAL_DEMO = "local_demo"


class AuthError(Exception):
    """Identity validation failed without exposing token material."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def as_body(self) -> Dict[str, str]:
        return {
            "error": "auth_error",
            "code": self.code,
            "message": self.message,
        }


@dataclass(frozen=True)
class AuthContext:
    mode: AuthMode
    email: Optional[str] = None
    subject: Optional[str] = None
    hosted_domain: Optional[str] = None


def auth_mode_from_env(env: Optional[Mapping[str, str]] = None) -> AuthMode:
    source = env if env is not None else os.environ
    raw = str(source.get("JUDGE_ADDON_AUTH_MODE", AuthMode.OFF.value)).strip().lower()
    try:
        return AuthMode(raw)
    except ValueError as exc:
        raise AuthError(
            "AUTH_ERROR",
            "Unsupported JUDGE_ADDON_AUTH_MODE.",
        ) from exc


def validate_authorization_header(
    headers: Mapping[str, str],
    *,
    env: Optional[Mapping[str, str]] = None,
    now: Optional[float] = None,
    jwks: Optional[Mapping[str, Any]] = None,
    allow_unverified_for_tests: bool = False,
) -> AuthContext:
    """Validate inbound auth per MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1.

    ``allow_unverified_for_tests`` skips JWKS signature verification and is only
    for unit tests that inject structurally valid synthetic JWTs. Production
    identity_token mode must keep it False.
    """
    mode = auth_mode_from_env(env)
    if mode is AuthMode.OFF:
        return AuthContext(mode=mode)

    normalized = {_norm_header(k): v for k, v in headers.items()}

    if mode is AuthMode.LOCAL_DEMO:
        demo = normalized.get(_norm_header(LOCAL_DEMO_HEADER))
        if demo != LOCAL_DEMO_VALUE:
            raise AuthError(
                "AUTH_ERROR",
                "Local demo authentication is required for this mode.",
            )
        return AuthContext(mode=mode, email="local-demo@example-demo.test")

    # identity_token
    auth = normalized.get("authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")
    token = auth.split(" ", 1)[1].strip()
    claims = _validate_identity_token(
        token,
        env=env if env is not None else os.environ,
        now=now,
        jwks=jwks,
        allow_unverified_for_tests=allow_unverified_for_tests,
    )
    return AuthContext(
        mode=mode,
        email=str(claims.get("email")) if claims.get("email") else None,
        subject=str(claims.get("sub")) if claims.get("sub") else None,
        hosted_domain=str(claims.get("hd")) if claims.get("hd") else None,
    )


def _norm_header(name: str) -> str:
    return name.lower().replace("_", "-")


def _b64url_decode(segment: str) -> bytes:
    pad = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + pad)


def _parse_jwt_unverified(token: str) -> Tuple[Dict[str, Any], Dict[str, Any], bytes, bytes]:
    parts = token.split(".")
    if len(parts) != 3 or not all(parts):
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")
    try:
        header = json.loads(_b64url_decode(parts[0]).decode("utf-8"))
        payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.") from exc
    if not isinstance(header, dict) or not isinstance(payload, dict):
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")
    signing_input = f"{parts[0]}.{parts[1]}".encode("ascii")
    signature = _b64url_decode(parts[2])
    return header, payload, signing_input, signature


def _validate_identity_token(
    token: str,
    *,
    env: Mapping[str, str],
    now: Optional[float],
    jwks: Optional[Mapping[str, Any]],
    allow_unverified_for_tests: bool,
) -> Dict[str, Any]:
    header, payload, signing_input, signature = _parse_jwt_unverified(token)
    issuer = str(payload.get("iss") or "")
    if issuer not in GOOGLE_ISSUERS:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    audience = env.get("JUDGE_ADDON_OIDC_AUDIENCE", "").strip()
    if not audience:
        raise AuthError("AUTH_ERROR", "Identity token audience is not configured.")
    token_aud = payload.get("aud")
    if isinstance(token_aud, list):
        aud_ok = audience in [str(a) for a in token_aud]
    else:
        aud_ok = str(token_aud or "") == audience
    if not aud_ok:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    skew = int(env.get("JUDGE_ADDON_OIDC_CLOCK_SKEW_SECONDS", "60") or "60")
    current = time.time() if now is None else float(now)
    exp = payload.get("exp")
    try:
        exp_f = float(exp)
    except (TypeError, ValueError) as exc:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.") from exc
    if exp_f + skew < current:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    email = payload.get("email")
    if not email or not isinstance(email, str):
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")
    if "email_verified" in payload and payload.get("email_verified") is not True:
        # Google may encode boolean or string; accept true/"true" only.
        verified = payload.get("email_verified")
        if verified is not True and str(verified).lower() != "true":
            raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    allowed_hd = env.get("JUDGE_ADDON_ALLOWED_HD", "").strip()
    if allowed_hd:
        if str(payload.get("hd") or "") != allowed_hd:
            raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    if not allow_unverified_for_tests:
        _verify_signature(header, signing_input, signature, jwks=jwks)

    return payload


def _verify_signature(
    header: Mapping[str, Any],
    signing_input: bytes,
    signature: bytes,
    *,
    jwks: Optional[Mapping[str, Any]] = None,
) -> None:
    try:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
        from cryptography.hazmat.backends import default_backend
    except ImportError as exc:  # pragma: no cover - optional runtime dep
        raise AuthError(
            "AUTH_ERROR",
            "Identity token signature verification is unavailable.",
        ) from exc

    kid = str(header.get("kid") or "")
    alg = str(header.get("alg") or "")
    if alg != "RS256" or not kid:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    keys = (jwks or _fetch_google_jwks()).get("keys") or []
    jwk = next((k for k in keys if k.get("kid") == kid), None)
    if not jwk:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.")

    try:
        n = int.from_bytes(_b64url_decode(str(jwk["n"])), "big")
        e = int.from_bytes(_b64url_decode(str(jwk["e"])), "big")
        public_key = RSAPublicNumbers(e, n).public_key(default_backend())
        public_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())
    except Exception as exc:  # noqa: BLE001 - map all crypto failures to AUTH_ERROR
        raise AuthError("AUTH_ERROR", "Identity token validation failed.") from exc


def _fetch_google_jwks() -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(GOOGLE_JWKS_URL, timeout=5) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AuthError("AUTH_ERROR", "Identity token validation failed.") from exc
