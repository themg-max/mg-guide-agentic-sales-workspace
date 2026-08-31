/**
 * CardService builders — presentation only.
 * Values come from the judge backend response; no policy/CRM logic here.
 *
 * UX v2: result-first salesperson journey.
 *   Follow-up ready -> Processing status -> What we heard -> Relationship
 *   -> CRM -> Follow-up draft -> Open Draft in Gmail -> Audit and integrity.
 * EMAIL_AUTO_SEND=FORBIDDEN. The compose action only opens an editable draft.
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
 * Homepage: product-first Meeting Follow-Up entry.
 * Primary CTA processes the approved synthetic meeting; judge-only
 * fail-closed scenarios live in a separate secondary section.
 * @return {CardService.Card}
 */
function buildHomeCard() {
  var primary = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRIMARY_CAPABILITY)
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>Meeting Follow-Up</b><br>Turn a completed meeting into ' +
          'relationship context, CRM-ready documentation, and a follow-up draft.'
      )
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>Competition mode</b><br>Approved synthetic transcript · ' +
          'governed CRM boundary'
      )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Process Meeting Follow-Up')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'SUCCESS' })
        )
    );

  var judgeTests = CardService.newCardSection()
    .setHeader('Judge test scenarios')
    .addWidget(
      CardService.newTextParagraph().setText(
        'Fail-closed test scenarios for judges. No CRM writes on this path.'
      )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Ambiguous contact')
        .setTextButtonStyle(CardService.TextButtonStyle.TEXT)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'AMBIGUOUS_CONTACT' })
        )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Policy guardrail')
        .setTextButtonStyle(CardService.TextButtonStyle.TEXT)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'STAGE_CHANGE_DENIED' })
        )
    );

  return CardService.newCardBuilder()
    .setHeader(brandHeader_())
    .addSection(primary)
    .addSection(judgeTests)
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
        'Processing approved synthetic scenario <b>' +
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
 * Render judge JSON into the result-first follow-up experience.
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
  var scenario = String(payload.scenario || '');
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

  var crmDisplay = crmNoteDisplay_(ux);
  var draft = ux.follow_up_draft || {};
  var draftReady =
    String(ux.ux_state) === 'COMPLETED' && String(draft.status) === 'READY';

  var builder = CardService.newCardBuilder().setHeader(brandHeader_());
  if (String(ux.ux_state) === 'NEEDS_REVIEW') {
    builder.addSection(buildNeedsReviewSection_(ux, crmDisplay));
  } else {
    builder.addSection(buildFollowUpReadySection_(ux, draft, crmDisplay));
  }
  builder.addSection(buildProcessingStatusSection_(ux, payload, stages));
  builder.addSection(buildWhatWeHeardSection_(ux));
  builder.addSection(buildRelationshipSection_(ux));
  builder.addSection(buildCrmSection_(ux, crmDisplay));
  if (draftReady) {
    builder.addSection(buildDraftPreviewSection_(draft));
    builder.addSection(buildComposeSection_(scenario));
  }
  builder.addSection(
    buildAuditIntegritySection_(
      stages,
      policy,
      audit,
      uxAudit,
      ux,
      externalEffects,
      liveCrm
    )
  );
  return builder.build();
}

/**
 * Success overview: concise status grid first.
 * @param {Object} ux
 * @param {Object} draft
 * @param {string} crmDisplay
 * @return {CardService.CardSection}
 */
function buildFollowUpReadySection_(ux, draft, crmDisplay) {
  var rel = ux.relationship_context || {};
  return CardService.newCardSection()
    .setHeader('Follow-up ready')
    .addWidget(CardService.newTextParagraph().setText('<b>FOLLOW-UP READY</b>'))
    .addWidget(kv_('Transcript', 'Processed'))
    .addWidget(kv_('Meeting', ux.summary ? 'Understood' : 'Not available'))
    .addWidget(
      kv_('Relationship', rel.contact_resolved ? 'Matched' : 'Needs review')
    )
    .addWidget(kv_('CRM note', crmDisplay))
    .addWidget(
      kv_(
        'Follow-up draft',
        String(draft.status) === 'READY' ? 'Ready' : 'Not available'
      )
    );
}

/**
 * Needs-review overview: no compose action is ever rendered here.
 * @param {Object} ux
 * @param {string} crmDisplay
 * @return {CardService.CardSection}
 */
function buildNeedsReviewSection_(ux, crmDisplay) {
  var needs = ux.needs_review || {};
  var rel = ux.relationship_context || {};
  return CardService.newCardSection()
    .setHeader('Needs review')
    .addWidget(CardService.newTextParagraph().setText('<b>NEEDS REVIEW</b>'))
    .addWidget(kv_('Relationship', relationshipDisplay_(rel.resolution_status)))
    .addWidget(kv_('CRM', crmDisplay))
    .addWidget(kv_('Draft', 'Not created'))
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>Why:</b> ' + (needs.reason || 'Follow-up requires review.')
      )
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        String(needs.explicit_next_action || '')
      )
    );
}

/**
 * @param {Object} ux
 * @param {Object} payload
 * @param {Array} stages
 * @return {CardService.CardSection}
 */
function buildProcessingStatusSection_(ux, payload, stages) {
  var recorded = 0;
  for (var i = 0; i < stages.length; i++) {
    if ((stages[i] || {}).status) {
      recorded++;
    }
  }
  return CardService.newCardSection()
    .setHeader('Processing status')
    .addWidget(kv_('UX_STATE', ux.ux_state))
    .addWidget(kv_('Workflow', payload.workflow_status))
    .addWidget(kv_('Stages recorded', recorded + ' of ' + stages.length));
}

/**
 * @param {Object} ux
 * @return {CardService.CardSection}
 */
function buildWhatWeHeardSection_(ux) {
  var proposed = ux.proposed_follow_up || {};
  var section = CardService.newCardSection()
    .setHeader('What we heard')
    .addWidget(kv_('Summary', ux.summary));
  if (compact_(proposed.needs)) {
    section.addWidget(kv_('Key needs', compact_(proposed.needs)));
  }
  if (compact_(proposed.objections)) {
    section.addWidget(kv_('Objections', compact_(proposed.objections)));
  }
  section.addWidget(kv_('Salesperson next step', ux.salesperson_next_step));
  return section;
}

/**
 * Relationship match display. Raw provider IDs are never rendered.
 * @param {Object} ux
 * @return {CardService.CardSection}
 */
function buildRelationshipSection_(ux) {
  var rel = (ux || {}).relationship_context || {};
  return CardService.newCardSection()
    .setHeader('Relationship')
    .addWidget(kv_('Status', relationshipDisplay_(rel.resolution_status)))
    .addWidget(kv_('Match basis', rel.match_basis))
    .addWidget(kv_('candidate_count', rel.candidate_count));
}

/**
 * CRM truth row. Display wording always comes from the backend
 * crm_note_status contract; policy permission is never execution proof.
 * @param {Object} ux
 * @param {string} crmDisplay
 * @return {CardService.CardSection}
 */
function buildCrmSection_(ux, crmDisplay) {
  var section = CardService.newCardSection()
    .setHeader('CRM')
    .addWidget(kv_('CRM note', crmDisplay));
  if (String(ux.ux_state) === 'NEEDS_REVIEW') {
    var needs = ux.needs_review || {};
    section.addWidget(
      CardService.newTextParagraph().setText(
        String(
          needs.zero_unauthorized_effects_message || 'No CRM changes were made.'
        )
      )
    );
  } else {
    section.addWidget(
      CardService.newTextParagraph().setText(
        'Policy permission is not execution proof. No live CRM write was performed.'
      )
    );
  }
  return section;
}

/**
 * Approved follow-up draft preview (server-generated projection only).
 * @param {Object} draft
 * @return {CardService.CardSection}
 */
function buildDraftPreviewSection_(draft) {
  var recipient = String(draft.recipient_email || '');
  if (draft.recipient_name) {
    recipient = String(draft.recipient_name) + ' <' + recipient + '>';
  }
  return CardService.newCardSection()
    .setHeader('Follow-up draft')
    .addWidget(kv_('To', recipient))
    .addWidget(kv_('Subject', draft.subject))
    .addWidget(
      CardService.newTextParagraph().setText(bodyPreview_(draft.body_text))
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        'Human review and send required. MG Guide never sends automatically.'
      )
    );
}

/**
 * Compose action — opens an editable Gmail draft. The human domain user is
 * the only sender; this button never sends email.
 * @param {string} scenario
 * @return {CardService.CardSection}
 */
function buildComposeSection_(scenario) {
  return CardService.newCardSection()
    .setHeader('Send follow-up')
    .addWidget(
      CardService.newTextParagraph().setText(
        'Opens an editable Gmail draft. You review it and decide whether to send.'
      )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Open Draft in Gmail')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setComposeAction(
          CardService.newAction()
            .setFunctionName('createFollowUpDraft')
            .setParameters({ scenario: scenario }),
          CardService.ComposedEmailType.STANDALONE_DRAFT
        )
    );
}

/**
 * Technical audit and integrity detail, below the primary experience.
 * @return {CardService.CardSection}
 */
function buildAuditIntegritySection_(
  stages,
  policy,
  audit,
  uxAudit,
  ux,
  externalEffects,
  liveCrm
) {
  var section = CardService.newCardSection().setHeader('Audit and integrity');
  for (var i = 0; i < stages.length; i++) {
    var stage = stages[i] || {};
    var title = String(stage.title || '').replace(' result card', '');
    section.addWidget(
      kv_(String(i + 1) + '. ' + title, stage.status)
    );
  }
  section
    .addWidget(kv_('policy.note_write', policy.note_write))
    .addWidget(kv_('policy.stage_write', policy.stage_write))
    .addWidget(kv_('policy.reason_codes', compact_(policy.reason_codes)))
    .addWidget(
      kv_(
        'Audit status',
        uxAudit.display || uxAudit.final_disposition || audit.final_disposition
      )
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        'UX_STATE=' +
          String(ux.ux_state || '') +
          ' · external_effects=' +
          String(externalEffects) +
          ' · LIVE_CRM_EXECUTION=' +
          String(liveCrm) +
          ' · CRM_MUTATIONS_PERFORMED=NO · EMAIL_AUTO_SEND=FORBIDDEN'
      )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Back to MG Guide home')
        .setOnClickAction(CardService.newAction().setFunctionName('onHomepage'))
    );
  return section;
}

/**
 * CRM note display wording from backend truth only. Fails closed: VERIFIED
 * wording is impossible without a backend live-execution report.
 * @param {Object} ux
 * @return {string}
 */
function crmNoteDisplay_(ux) {
  var status = (ux || {}).crm_note_status || {};
  var state = String(status.state || '');
  var live =
    (ux.permitted_action_result &&
      ux.permitted_action_result.LIVE_CRM_EXECUTION) ||
    'NOT_PERFORMED';
  var displays = {
    NOT_EXECUTED: 'CRM note not executed in competition mode',
    BLOCKED: 'CRM update blocked. No change performed.',
    VERIFIED: 'CRM note verified',
    UNKNOWN: 'CRM note status unavailable. No CRM change confirmed.',
  };
  if (state === 'VERIFIED' && String(live) !== 'PERFORMED') {
    state = 'UNKNOWN';
  }
  if (!displays[state]) {
    state = 'UNKNOWN';
  }
  return displays[state];
}

/**
 * @param {*} status
 * @return {string}
 */
function relationshipDisplay_(status) {
  var raw = String(status || '');
  var known = {
    matched: 'Matched',
    ambiguous: 'Ambiguous',
    not_found: 'Not found',
  };
  return known[raw] || raw || '—';
}

/**
 * @param {*} text
 * @return {string}
 */
function bodyPreview_(text) {
  var body = String(text || '');
  if (body.length <= 240) {
    return body;
  }
  return body.substring(0, 239).replace(/\s+$/, '') + '…';
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
