# MG Guide Workspace Add-on — Judge UX v1

```text
ARTIFACT=docs/architecture/mg-guide-workspace-addon-judge-ux-v1.md
PRODUCT=MG Guide
ATTRIBUTION=Powered by AI Rolodex
WORKFLOW=meeting_follow_up_v1
ROLE=THIN_PRESENTATION_AND_ROUTING_ADAPTER
```

## UI architecture

```text
Gmail / Calendar host
  -> workspace_addon CardService (MG Guide home)
  -> runMeetingFollowUpScenario(SUCCESS | AMBIGUOUS_CONTACT)
  -> POST /demo/meeting-follow-up  (existing judge surface)
  -> WorkflowRunner + packet + card mapper + demo_stages + ux_experience
  -> buildResultCardFromJudgePayload (field display only)
```

| Layer | Owns | Must not own |
| --- | --- | --- |
| `workspace_addon/*.gs` | Branding, scenario buttons, HTTP route, CardService layout, error cards | Policy, CRM, agents, fixtures |
| `src/mg_guide/workspace_addon/` | Testable projection + OIDC auth validator + local adapter | Workflow truth |
| `src/mg_guide/judge_surface/` | Existing competition endpoint | Apps Script UI |

## Branded card hierarchy

The header uses the MG Guide square image and the `Powered by AI Rolodex`
subtitle. The homepage presents the following copy without duplicating the
product name:

- **Meeting Follow-Up** - Turn a meeting into a governed follow-up plan.
- **Demo mode** - Synthetic data · No CRM writes.
- **Run Successful Follow-Up** and **Test Ambiguous Contact** retain the
  `SUCCESS` and `AMBIGUOUS_CONTACT` backend selectors.

The optional policy guardrail is a secondary text action. The fixed
attribution-only footer is intentionally absent.

Results keep technical truth markers in Integrity while their primary hierarchy
is Outcome, Meeting summary, Relationship, Policy, Six-stage workflow summary,
Salesperson next step, Audit, and Integrity.

The six visible stage titles are taken from the judge `demo_stages` projection:

1. Meeting ready  
2. Meeting Context  
3. Relationship Resolution  
4. Follow-Up Planning  
5. Policy Evaluation  
6. Meeting Follow-Up result  

## Error states

`AUTH_ERROR` · `BACKEND_UNAVAILABLE` · `INVALID_RESPONSE` · `SCENARIO_BLOCKED`

All error cards state **No CRM changes were made** and
`LIVE_CRM_EXECUTION=NOT_PERFORMED`.

## Auth

See `mg-guide-workspace-addon-auth-contract-v1.md`.
