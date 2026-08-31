/**
 * Gmail follow-up draft — human-controlled compose action.
 *
 * Contract markers:
 *   EMAIL_AUTO_SEND=FORBIDDEN
 *   DRAFT_CREATION_REQUIRES_USER_ACTION=YES
 *   FINAL_SEND_REQUIRES_HUMAN=YES
 *
 * This file must never call any Gmail API that sends or replies to mail.
 * The human domain user remains the only sender. Draft content comes from the
 * backend's deterministic follow_up_draft projection of already approved
 * fields; Apps Script stays a thin presentation and routing adapter.
 */

/**
 * Compose action callback for the "Open Draft in Gmail" button.
 *
 * Re-fetches the deterministic judge projection for the same approved
 * synthetic scenario (no state store, no cached credentials, no CRM data)
 * and opens the standard editable Gmail compose window. Fails closed by
 * throwing a code-prefixed error; no draft is created on any failure.
 *
 * @param {Object} e
 * @return {CardService.ComposeActionResponse}
 */
function createFollowUpDraft(e) {
  var params = (e && e.parameters) || {};
  var scenario = params.scenario || '';
  if (!scenario) {
    throw new Error('DRAFT_NOT_AVAILABLE: Missing scenario.');
  }

  var payload = fetchMeetingFollowUp_(scenario);
  var ux = payload.ux_experience || {};
  if (String(ux.ux_state) !== 'COMPLETED') {
    throw new Error(
      'DRAFT_NOT_AVAILABLE: Follow-up is not ready for this result.'
    );
  }

  var draft = ux.follow_up_draft || {};
  if (String(draft.status) !== 'READY') {
    throw new Error('DRAFT_NOT_AVAILABLE: No approved follow-up draft.');
  }

  var recipient = String(draft.recipient_email || '').trim();
  var subject = String(draft.subject || '').trim();
  var body = String(draft.body_text || '');
  if (!recipient || !subject || !body.trim()) {
    throw new Error('DRAFT_NOT_AVAILABLE: Draft fields incomplete.');
  }

  var gmailDraft = GmailApp.createDraft(recipient, subject, body);
  return CardService.newComposeActionResponseBuilder()
    .setGmailDraft(gmailDraft)
    .build();
}
