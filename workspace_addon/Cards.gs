/**
 * CardService builders — presentation only.
 * Values come from the judge backend response; no policy/CRM logic here.
 */

function brandHeader_() {
  return CardService.newCardHeader()
    .setTitle(MG_GUIDE_PRODUCT_NAME)
    .setSubtitle(MG_GUIDE_ATTRIBUTION);
}

function brandFooter_() {
  return CardService.newFixedFooter().setPrimaryButton(
    CardService.newTextButton()
      .setText(MG_GUIDE_ATTRIBUTION)
      .setOnClickAction(CardService.newAction().setFunctionName('onHomepage'))
  );
}

/**
 * Homepage: MG Guide branding + synthetic scenario selectors.
 * @return {CardService.Card}
 */
function buildHomeCard() {
  var intro = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRODUCT_NAME)
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>' + MG_GUIDE_PRODUCT_NAME + '</b><br>' + MG_GUIDE_ATTRIBUTION
      )
    )
    .addWidget(
      CardService.newTextParagraph().setText(
        'Primary experience: <b>' +
          MG_GUIDE_PRIMARY_CAPABILITY +
          '</b>. Synthetic competition scenarios only. LIVE_CRM_EXECUTION=NOT_PERFORMED.'
      )
    );

  var scenarios = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRIMARY_CAPABILITY)
    .addWidget(
      CardService.newTextButton()
        .setText('Run SUCCESS')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'SUCCESS' })
        )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Run AMBIGUOUS_CONTACT')
        .setTextButtonStyle(CardService.TextButtonStyle.FILLED)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'AMBIGUOUS_CONTACT' })
        )
    )
    .addWidget(
      CardService.newTextButton()
        .setText('Run STAGE_CHANGE_DENIED (optional)')
        .setTextButtonStyle(CardService.TextButtonStyle.TEXT)
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName('runMeetingFollowUpScenario')
            .setParameters({ scenario: 'STAGE_CHANGE_DENIED' })
        )
    );

  var truth = CardService.newCardSection()
    .setHeader('Truth boundary')
    .addWidget(
      CardService.newTextParagraph().setText(
        'No live CRM writes. external_effects stay 0 on this judge path. CRM mutations are not performed.'
      )
    );

  return CardService.newCardBuilder()
    .setHeader(brandHeader_())
    .addSection(intro)
    .addSection(scenarios)
    .addSection(truth)
    .setFixedFooter(brandFooter_())
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
    .setFixedFooter(brandFooter_())
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
 * Render judge JSON into six-stage + result cards.
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

  var summary = CardService.newCardSection()
    .setHeader(MG_GUIDE_PRODUCT_NAME + ' · ' + MG_GUIDE_PRIMARY_CAPABILITY)
    .addWidget(
      CardService.newTextParagraph().setText(
        '<b>' + MG_GUIDE_PRODUCT_NAME + '</b><br>' + MG_GUIDE_ATTRIBUTION
      )
    )
    .addWidget(kv_('Scenario', String(payload.scenario || '')))
    .addWidget(kv_('UX_STATE', String(ux.ux_state || '')))
    .addWidget(kv_('workflow_status', String(payload.workflow_status || '')));
  builder.addSection(summary);

  for (var i = 0; i < stages.length; i++) {
    builder.addSection(buildStageSection_(i, stages[i]));
  }

  builder.addSection(
    buildOutcomeSection_(ux, policy, audit, uxAudit, externalEffects, liveCrm)
  );

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

  builder.setFixedFooter(brandFooter_());
  return builder.build();
}

/**
 * @param {number} index
 * @param {Object} stage
 * @return {CardService.CardSection}
 */
function buildStageSection_(index, stage) {
  stage = stage || {};
  var evidence = stage.evidence || {};
  var title = String(stage.title || '');
  title = title.replace(' result card', '');
  if (index === 5 && title === 'Meeting Follow-Up') {
    title = 'Meeting Follow-Up result';
  }
  var section = CardService.newCardSection()
    .setHeader(String(index + 1) + '. ' + title)
    .addWidget(kv_('Stage status', String(stage.status || '')));

  if (index === 0) {
    section.addWidget(kv_('title', evidence.title));
    section.addWidget(kv_('source', evidence.source));
    section.addWidget(kv_('participants', compact_(evidence.participants)));
  } else if (index === 1) {
    section.addWidget(kv_('summary', evidence.summary));
    section.addWidget(kv_('needs', compact_(evidence.needs)));
    section.addWidget(kv_('extraction_confidence', evidence.extraction_confidence));
  } else if (index === 2) {
    section.addWidget(kv_('resolution_status', evidence.resolution_status));
    section.addWidget(kv_('match_basis', evidence.match_basis));
    section.addWidget(kv_('candidate_count', evidence.candidate_count));
    section.addWidget(kv_('current_stage', evidence.current_stage));
  } else if (index === 3) {
    section.addWidget(kv_('note_intents', compact_(evidence.note_intents)));
    section.addWidget(kv_('stage_intents', compact_(evidence.stage_intents)));
    section.addWidget(
      kv_('note_execution_attempted', evidence.note_execution_attempted)
    );
    section.addWidget(
      kv_('stage_execution_attempted', evidence.stage_execution_attempted)
    );
  } else if (index === 4) {
    section.addWidget(kv_('note_write', evidence.note_write));
    section.addWidget(kv_('stage_write', evidence.stage_write));
    section.addWidget(kv_('reason_codes', compact_(evidence.reason_codes)));
  } else {
    var framing = evidence.framing || {};
    var brief = evidence.brief || {};
    var integrity = evidence.integrity || {};
    section.addWidget(kv_('card_state', evidence.card_state));
    section.addWidget(kv_('workflow_status', evidence.workflow_status));
    section.addWidget(kv_('headline', framing.headline || brief.headline));
    section.addWidget(kv_('body', framing.body));
    section.addWidget(kv_('next_action', brief.next_action));
    section.addWidget(kv_('no_crm_changes_made', framing.no_crm_changes_made));
    section.addWidget(kv_('external_effects', integrity.external_effects));
    section.addWidget(kv_('LIVE_CRM_EXECUTION', evidence.LIVE_CRM_EXECUTION));
  }
  return section;
}

/**
 * @return {CardService.CardSection}
 */
function buildOutcomeSection_(ux, policy, audit, uxAudit, externalEffects, liveCrm) {
  ux = ux || {};
  policy = policy || {};
  audit = audit || {};
  uxAudit = uxAudit || {};
  var rel = ux.relationship_context || {};
  var proposed = ux.proposed_follow_up || {};

  var section = CardService.newCardSection()
    .setHeader('Meeting Follow-Up result')
    .addWidget(kv_('UX_STATE', ux.ux_state))
    .addWidget(kv_('Meeting summary', ux.summary))
    .addWidget(kv_('Relationship status', rel.resolution_status))
    .addWidget(kv_('match_basis', rel.match_basis))
    .addWidget(kv_('candidate_count', rel.candidate_count))
    .addWidget(
      kv_(
        'Proposed follow-up',
        proposed.headline || proposed.summary || 'See stage evidence'
      )
    )
    .addWidget(kv_('policy.note_write', policy.note_write))
    .addWidget(kv_('policy.stage_write', policy.stage_write))
    .addWidget(kv_('policy.reason_codes', compact_(policy.reason_codes)))
    .addWidget(kv_('Salesperson next step', ux.salesperson_next_step))
    .addWidget(
      kv_(
        'Audit status',
        uxAudit.display || uxAudit.final_disposition || audit.final_disposition
      )
    )
    .addWidget(kv_('external_effects', externalEffects))
    .addWidget(kv_('LIVE_CRM_EXECUTION', liveCrm));

  if (String(ux.ux_state) === 'NEEDS_REVIEW') {
    var needs = ux.needs_review || {};
    var block = needs.block_context || {};
    section.addWidget(
      CardService.newTextParagraph().setText(
        '<b>Needs review:</b> ' + String(needs.reason || '')
      )
    );
    section.addWidget(
      CardService.newTextParagraph().setText(
        String(
          needs.zero_unauthorized_effects_message ||
            'No CRM changes were made. Unauthorized effects: 0.'
        )
      )
    );
    var codes = block.reason_codes || policy.reason_codes || [];
    if (codes.indexOf('AMBIGUOUS_CONTACT') >= 0) {
      section.addWidget(
        CardService.newTextParagraph().setText(
          'Resolve contact identity before any CRM write.'
        )
      );
    } else if (needs.explicit_next_action) {
      section.addWidget(
        CardService.newTextParagraph().setText(String(needs.explicit_next_action))
      );
    }
  } else {
    var completed = ux.completed || {};
    section.addWidget(
      CardService.newTextParagraph().setText(
        String(
          completed.body ||
            'Governed follow-up intents are prepared. No live CRM write was performed.'
        )
      )
    );
  }

  section.addWidget(
    CardService.newTextButton()
      .setText('Back to MG Guide home')
      .setOnClickAction(CardService.newAction().setFunctionName('onHomepage'))
  );
  return section;
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
