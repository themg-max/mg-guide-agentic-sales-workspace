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

## Six-stage display

Stage titles are taken from the judge `demo_stages` projection:

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
