/**
 * Competition Workspace add-on configuration.
 * Backend URL comes from Script Properties — never hard-code private endpoints.
 */

var MG_GUIDE_PRODUCT_NAME = 'MG Guide';
var MG_GUIDE_ATTRIBUTION = 'Powered by AI Rolodex';
var MG_GUIDE_PRIMARY_CAPABILITY = 'Meeting Follow-Up';
var MG_GUIDE_DEMO_PATH = '/demo/meeting-follow-up';
var MG_GUIDE_LOGO_URL =
  'https://storage.googleapis.com/mg-devpost-assets/mg-guide/mg-guide-128x128.png';

/**
 * @return {string} Judge backend base URL without trailing slash.
 */
function getJudgeBackendBaseUrl_() {
  var props = PropertiesService.getScriptProperties();
  var base = props.getProperty('JUDGE_BACKEND_BASE_URL') || '';
  base = String(base).trim().replace(/\/+$/, '');
  return base;
}

/**
 * @return {boolean} Whether to attach an OIDC identity token.
 */
function shouldSendIdentityToken_() {
  var props = PropertiesService.getScriptProperties();
  var mode = String(props.getProperty('JUDGE_ADDON_AUTH_MODE') || 'identity_token')
    .trim()
    .toLowerCase();
  return mode !== 'off';
}
