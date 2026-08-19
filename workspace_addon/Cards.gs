/**
 * CardService builders — presentation only.
 * Values come from the judge backend response; no policy/CRM logic here.
 */

function brandHeader_() {
  return CardService.newCardHeader()
    .setTitle(MG_GUIDE_PRODUCT_NAME)
    .setSubtitle(MG_GUIDE_ATTRIBUTION)
    .setImageUrl(MG_GUIDE_LOGO_URL)
    .setImageStyle(CardService.ImageStyle.SQUARE)
    .setImageAltText('MG Guide logo');
}

/**
 * Homepage: MG Guide branding + synthetic scenario selectors.
 * @return {CardService.Card}
 */
function buildHomeCard() {
  var intro = CardService.newCardSection()
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>Meeting Follow-Up</b><br>Turn a meeting into a governed follow-up plan.'
      )
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>Demo mode</b><br>Synthetic data · No CRM writes'
      )
    );

  var scenarios = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRIMARY_CAPABILITY)
    .addWidget(
      CardService.newTextButton()
        .setText('Run Successful Follow-Up')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'SUCCESS' })
        )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Test Ambiguous Contact')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'AMBIGUOUS_CONTACT' })
        )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Optional policy guardrail')
        .setTextButtonStyle(CardService.TextButtonStyle.TEXT)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'STAGE_CHANGE_DENIED' })
        )
    );

  return CardService.newCardBuilder()
    .setHeader(brandHeader_())
    .addSection(intro)
    .addSection(scenarios)
    .build();
}

/**
 * @param {string} code
 * @param {string} message
 * @return {CardService.Card}
 */
function buildErrorCard(code, message) {
  var human = message || 'An error occurred.';
  if (code === 'AUTH_ERROR') {
    human =
      'Authentication failed. Sign in with the controlled judge Workspace account and retry.';
  } else if (code === 'BACKEND_UNAVAILABLE') {
    human = 'MG Guide backend is unavailable. No CRM changes were made.';
  } else if (code === 'INVALID_RESPONSE') {
    human = 'The backend returned an invalid response. No CRM changes were made.';
  } else if (code === 'SCENARIO_BLOCKED') {
    human = 'That scenario is not available on the judge path. No CRM changes were made.';
  }

  var section = CardService.newCardSection()
    .setHeader('Error · ' + code)
    .addWidget(CardService.newTextParagraph().setText(human))
    .addWidget(
      CardService.newDecoratedText()
        .setTopLabel('external_effects')
        .setText('0')
    )
    .addWidget(
      CardService.newDecoratedText()
        .setTopLabel('LIVE_CRM_EXECUTION')
        .setText('NOT_PERFORMED')
    )
    .addWidget(
      CardService.newTextParagraph().setText('No CRM changes were made.')
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Back to MG Guide home')
        .setOnClickAction(CardService.newAction().setFunctionName('onHomepage'))
    );

  return CardService.newCardBuilder()
    .setHeader(brandHeader_())
    .addSection(section)
    .build();
}

/**
 * Loading card while the backend runs the synthetic scenario.
 * @param {string} scenario
 * @return {CardService.Card}
 */
function buildLoadingCard(scenario) {
  var section = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRIMARY_CAPABILITY)
    .addWidget(
      CardService.newTextParagraph().setText(
        'Running synthetic scenario <b>' +
          scenario +
          '</b>… No CRM mutation is performed during this request.'
      )
    );
  return CardService.newCardBuilder()
    .setHeader(brandHeader_())
    .addSection(section)
    .build();
}

/**
 * Render judge JSON into a concise outcome and six-stage summary.
 * @param {Object} payload
 * @return {CardService.Card}
 */
function buildResultCardFromJudgePayload(payload) {
  if (!payload || typeof payload !== 'object') {
    return buildErrorCard('INVALID_RESPONSE', 'Empty payload');
  }

  var ux = payload.ux_experience || {};
  var stages = payload.demo_stages || [];
  var policy = payload.policy_decision || {};
  var audit = payload.audit_summary || {};
  var uxAudit = ux.audit_status || {};
  var truth = payload.demo_truth || {};
  var externalEffects =
    payload.external_effects === 0 || payload.external_effects
      ? payload.external_effects
      : 0;
  var liveCrm =
    truth.LIVE_CRM_EXECUTION ||
    (ux.permitted_action_result && ux.permitted_action_result.LIVE_CRM_EXECUTION) ||
    'NOT_PERFORMED';

  if (!stages || stages.length !== 6) {
    return buildErrorCard('INVALID_RESPONSE', 'demo_stages missing');
  }

  var builder = CardService.newCardBuilder().setHeader(brandHeader_());
  builder.addSection(
    CardService.newCardSection()
      .setHeader('Outcome')
      .addWidget(
        CardService.newTextParagraph().setText(
          String(ux.ux_state) === 'NEEDS_REVIEW'
            ? 'Needs review before any follow-up can proceed.'
            : 'Follow-up plan prepared.'
        )
      )
  );
  builder.addSection(buildMeetingSummarySection_(ux));
  builder.addSection(buildRelationshipSection_(ux));
  builder.addSection(buildPolicySection_(policy));
  builder.addSection(buildStageSummarySection_(stages));
  builder.addSection(buildSalespersonNextStepSection_(ux));
  builder.addSection(buildAuditSection_(audit, uxAudit));
  builder.addSection(
    CardService.newCardSection()
      .setHeader('Integrity')
      .addWidget(
        CardService.newTextParagraph().setText(
          'UX_STATE=' +
            String(ux.ux_state || '') +
            ' · external_effects=' +
            String(externalEffects) +
            ' · LIVE_CRM_EXECUTION=' +
            String(liveCrm) +
            ' · CRM_MUTATIONS_PERFORMED=NO'
        )
      )
  );
  return builder.build();
}

/**
 * @param {Object} ux
 * @return {CardService.CardSection}
 */
function buildMeetingSummarySection_(ux) {
  return CardService.newCardSection()
    .setHeader('Meeting summary')
    .addWidget(kv_('Summary', ux.summary));
}

/**
 * @param {Object} ux
 * @return {CardService.CardSection}
 */
function buildRelationshipSection_(ux) {
  var rel = (ux || {}).relationship_context || {};
  return CardService.newCardSection()
    .setHeader('Relationship')
    .addWidget(kv_('Status', rel.resolution_status))
    .addWidget(kv_('Match basis', rel.match_basis))
    .addWidget(kv_('Candidates', rel.candidate_count));
}

/**
 * @param {Object} policy
 * @return {CardService.CardSection}
 */
function buildPolicySection_(policy) {
  policy = policy || {};
  return CardService.newCardSection()
    .setHeader('Policy')
    .addWidget(kv_('Notes', policy.note_write))
    .addWidget(kv_('Stage change', policy.stage_write))
    .addWidget(kv_('Reason', compact_(policy.reason_codes)));
}

/**
 * @param {Array} stages
 * @return {CardService.CardSection}
 */
function buildStageSummarySection_(stages) {
  var section = CardService.newCardSection().setHeader('Six-stage workflow summary');
  for (var i = 0; i < stages.length; i++) {
    var stage = stages[i] || {};
    var title = String(stage.title || '').replace(' result card', '');
    section.addWidget(kv_(String(i + 1) + '. ' + title, stage.status));
  }
  return section;
}

/**
 * @param {Object} ux
 * @return {CardService.CardSection}
 */
function buildSalespersonNextStepSection_(ux) {
  return CardService.newCardSection()
    .setHeader('Salesperson next step')
    .addWidget(kv_('Next step', (ux || {}).salesperson_next_step));
}

/**
 * @param {Object} audit
 * @param {Object} uxAudit
 * @return {CardService.CardSection}
 */
function buildAuditSection_(audit, uxAudit) {
  audit = audit || {};
  uxAudit = uxAudit || {};
  return CardService.newCardSection()
    .setHeader('Audit')
    .addWidget(
      kv_(
        'Status',
        uxAudit.display || uxAudit.final_disposition || audit.final_disposition
      )
    );
}

/**
 * @param {string} label
 * @param {*} value
 * @return {CardService.DecoratedText}
 */
function kv_(label, value) {
  var text = value === null || value === undefined || value === '' ? '—' : String(value);
  return CardService.newDecoratedText().setTopLabel(String(label)).setText(text).setWrapText(true);
}

/**
 * @param {*} value
 * @return {string}
 */
function compact_(value) {
  if (value === null || value === undefined) {
    return '';
  }
  if (Object.prototype.toString.call(value) === '[object Array]') {
    var parts = [];
    for (var i = 0; i < value.length; i++) {
      var item = value[i];
      if (item && typeof item === 'object') {
        parts.push(
          String(item.summary || item.name || item.email || JSON.stringify(item))
        );
      } else {
        parts.push(String(item));
      }
    }
    return parts.join('; ');
  }
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value);
    } catch (err) {
      return String(value);
    }
  }
  return String(value);
}
