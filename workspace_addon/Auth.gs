/**
 * Auth helpers for MG Guide competition add-on.
 *
 * Contract: MG_GUIDE_ADDON_OIDC_IDENTITY_TOKEN_V1
 * RAW_IDENTITY_TOKEN_LOGGING = FORBIDDEN
 */

/**
 * Build UrlFetch headers for the judge backend.
 * Never logs token values, lengths tied to token content dumps, or raw JWT text.
 *
 * @return {Object} headers map
 */
function buildJudgeAuthHeaders_() {
  var headers = {
    Accept: 'application/json',
  };

  if (!shouldSendIdentityToken_()) {
    return headers;
  }

  var token = null;
  try {
    token = ScriptApp.getIdentityToken();
  } catch (err) {
    // Do not interpolate token material; message only.
    throw new Error('AUTH_ERROR: Unable to obtain identity token.');
  }

  if (!token || typeof token !== 'string') {
    throw new Error('AUTH_ERROR: Identity token unavailable.');
  }

  // Structural check only — do not log the token.
  var segments = token.split('.');
  if (segments.length !== 3 || !segments[0] || !segments[1] || !segments[2]) {
    throw new Error('AUTH_ERROR: Identity token format invalid.');
  }

  headers.Authorization = 'Bearer ' + token;
  return headers;
}
