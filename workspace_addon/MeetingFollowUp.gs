/**
 * Meeting Follow-Up routing — POST to existing judge endpoint only.
 */

/**
 * Homepage / Gmail / Calendar entry.
 * @param {Object} e
 * @return {CardService.Card}
 */
function onHomepage(e) {
  return buildHomeCard();
}

/**
 * Gmail contextual entry — same home (synthetic scenarios; no mail body reads).
 * @param {Object} e
 * @return {CardService.Card}
 */
function onGmailContext(e) {
  return buildHomeCard();
}

/**
 * Calendar contextual entry — same home (synthetic scenarios; no event reads).
 * @param {Object} e
 * @return {CardService.Card}
 */
function onCalendarEventOpen(e) {
  return buildHomeCard();
}

/**
 * Run a fixed synthetic scenario against the judge surface.
 * @param {Object} e
 * @return {CardService.ActionResponse}
 */
function runMeetingFollowUpScenario(e) {
  var params = (e && e.parameters) || {};
  var scenario = params.scenario || '';
  if (!scenario) {
    return CardService.newActionResponseBuilder()
      .setNavigation(
        CardService.newNavigation().updateCard(
          buildErrorCard('SCENARIO_BLOCKED', 'Missing scenario')
        )
      )
      .build();
  }

  try {
    var payload = fetchMeetingFollowUp_(scenario);
    var card = buildResultCardFromJudgePayload(payload);
    return CardService.newActionResponseBuilder()
      .setNavigation(CardService.newNavigation().updateCard(card))
      .build();
  } catch (err) {
    var code = 'BACKEND_UNAVAILABLE';
    var message = 'Backend unavailable.';
    var text = String((err && err.message) || err || '');
    if (text.indexOf('AUTH_ERROR') === 0) {
      code = 'AUTH_ERROR';
      message = text;
    } else if (text.indexOf('SCENARIO_BLOCKED') === 0) {
      code = 'SCENARIO_BLOCKED';
      message = text;
    } else if (text.indexOf('INVALID_RESPONSE') === 0) {
      code = 'INVALID_RESPONSE';
      message = text;
    } else if (text.indexOf('BACKEND_UNAVAILABLE') === 0) {
      code = 'BACKEND_UNAVAILABLE';
      message = text;
    }
    // Never include credentials. err.message is code-prefixed only.
    return CardService.newActionResponseBuilder()
      .setNavigation(
        CardService.newNavigation().updateCard(buildErrorCard(code, message))
      )
      .build();
  }
}

/**
 * @param {string} scenario
 * @return {Object}
 */
function fetchMeetingFollowUp_(scenario) {
  var base = getJudgeBackendBaseUrl_();
  if (!base) {
    throw new Error(
      'BACKEND_UNAVAILABLE: JUDGE_BACKEND_BASE_URL script property is not set.'
    );
  }

  var url = base + MG_GUIDE_DEMO_PATH;
  var headers = buildJudgeAuthHeaders_();
  var options = {
    method: 'post',
    contentType: 'application/json',
    headers: headers,
    payload: JSON.stringify({ scenario: scenario }),
    muteHttpExceptions: true,
  };

  var response;
  try {
    response = UrlFetchApp.fetch(url, options);
  } catch (err) {
    throw new Error('BACKEND_UNAVAILABLE: Unable to reach MG Guide backend.');
  }

  var code = response.getResponseCode();
  var bodyText = response.getContentText() || '';
  var body = null;
  if (bodyText) {
    try {
      body = JSON.parse(bodyText);
    } catch (parseErr) {
      throw new Error('INVALID_RESPONSE: Non-JSON backend body.');
    }
  }

  if (code === 401 || code === 403) {
    throw new Error('AUTH_ERROR: Backend rejected identity.');
  }
  if (code === 400 && body && body.error === 'invalid_scenario') {
    throw new Error('SCENARIO_BLOCKED: Scenario not allowed.');
  }
  if (code === 503) {
    throw new Error('BACKEND_UNAVAILABLE: Judge mode rejected or unavailable.');
  }
  if (code < 200 || code >= 300) {
    throw new Error('BACKEND_UNAVAILABLE: HTTP ' + String(code));
  }
  if (!body || typeof body !== 'object') {
    throw new Error('INVALID_RESPONSE: Empty JSON object.');
  }
  if (!body.demo_stages || !body.ux_experience || !body.policy_decision) {
    throw new Error('INVALID_RESPONSE: Missing demo projection fields.');
  }
  return body;
}
