# WebMCP Lessons and Future Direction

This document separates what is **running now** for The WebMCP Challenge from
what we learned and what we would build next.

## Current challenge implementation

The submitted WebMCP surface is intentionally small and bounded. The live MG
Guide page exposes exactly three native tools:

1. `process_meeting_follow_up` — **ACTION**
2. `get_current_follow_up_state` — **STATE**
3. `get_follow_up_draft` — **ARTIFACT**

The challenge demo uses synthetic fixture data only. It does not ingest
arbitrary external websites, write to CRM, send email, or route the WebMCP
request through the broader MG Guide orchestrator. Every usable draft requires
human review/send authority.

## What we learned

### 1. A web page can become an agent interface without becoming an agent-only UI

The most useful WebMCP pattern for MG Guide was not adding more automation. It
was giving the existing human-facing page a small structured contract that an
agent can discover and call directly. The person and agent can therefore work
from the same visible state instead of maintaining separate UI and API mental
models.

### 2. ACTION / STATE / ARTIFACT is a useful interaction pattern

Separating the workflow into one mutating-in-page action and two read-only
inspection tools made the collaboration easier to understand and test:

- **ACTION** performs the bounded operation.
- **STATE** lets the agent inspect the current workflow without rerunning it.
- **ARTIFACT** retrieves the prepared output for human review.

This pattern also makes stale-state and multi-run behavior testable.

### 3. Fail-closed behavior is part of the product experience

`AMBIGUOUS_CONTACT` was not treated as an error to hide. It is an intentional
human handoff: identity uncertainty produces `NEEDS_REVIEW`, no draft, and
`RELATIONSHIP_REVIEW_REQUIRED`. For relationship-driven work, safe refusal is
as important as successful automation.

### 4. Browser origin and deployment behavior are part of agent reliability

Native browser agents exercise real browser security boundaries. Exact CORS
origins, canonical HTTPS routes, cache policy, and the client that actually
implements WebMCP all affected whether a technically correct tool could be
used successfully. Agent-native web architecture therefore includes browser
and deployment behavior, not only tool schemas.

### 5. Governed systems need provenance, not just more context

The next challenge for MG Guide is not simply giving an agent access to more
web content. External information needs to enter the governed environment with
source identity, user intent, timestamps, and explicit promotion rules so the
system can distinguish temporary evidence from durable relationship context.

## Future direction: governed external-information intake

A natural next step is to let a person intentionally bring useful information
from the open web into MG Guide while preserving the governance model.

The design we would pursue is:

```text
external webpage / WebMCP-capable site
        ↓
user selects or authorizes information
        ↓
source-aware intake packet
        ↓
bounded MG ingress / validation layer
        ↓
governed staging context
        ↓
MG Guide retrieval and reasoning
        ↓
human-reviewed downstream action
```

A source-aware intake packet should carry at least:

- source URL and page title;
- capture timestamp;
- explicit user intent for why the information is being brought in;
- selected content or structured tool result rather than an unrestricted page
  dump whenever possible;
- source/provenance metadata and an integrity fingerprint;
- sensitivity/classification flags;
- the bounded MG object or workflow the information may inform;
- a rule that ingestion does **not** automatically authorize external effects
  or permanent memory promotion.

The governed intake layer would validate, sanitize, classify, and stage the
information before it is available to MG Guide. Promotion into durable context
would remain a separate governed decision.

## Future direction: Chrome extension companion

We also see a Chrome extension as a useful companion to WebMCP, especially on
sites that do not yet expose native WebMCP tools.

The extension would not be a general-purpose scraper. Its role would be to
provide a user-controlled bridge from the browser into the governed intake
contract.

### Proposed extension flow

1. The user opens an external page in Chrome.
2. The extension identifies the active origin and shows what can be captured.
3. The user explicitly selects the relevant text, link, record, or page
   context and chooses an MG Guide destination/use case.
4. The extension builds the same source-aware intake packet described above.
5. The packet is sent to a bounded MG ingress endpoint.
6. MG governance validates the source, content class, destination, and allowed
   use before the information becomes retrievable context.
7. MG Guide can then use the staged evidence for tasks such as relationship
   research, meeting preparation, opportunity context, or follow-up planning.
8. Any customer-facing or system-mutating action remains separately gated and
   human controlled.

### WebMCP-first when available

If the external site exposes WebMCP, the preferred path would be to call the
site's declared structured tools instead of inferring or scraping DOM state.
The Chrome extension is most valuable as a compatibility and user-consent
bridge for the rest of the web.

```text
WebMCP-capable source
    → native structured tool result
    → governed intake packet

Non-WebMCP source
    → explicit user-selected browser context via extension
    → governed intake packet
```

Both paths converge on the same MG governance boundary.

## Why this matters for MG Guide

The current challenge proves that MG Guide can make its own web experience
agent-native. The broader opportunity is a two-way pattern:

- **outbound:** MG Guide exposes safe, typed capabilities to agents through
  WebMCP;
- **inbound:** users can intentionally bring external evidence into MG Guide
  through a provenance-preserving governed intake layer.

That would let MG Guide support richer meeting preparation, relationship
intelligence, and follow-up without turning the browser into an ungoverned data
collection channel.

## What is not claimed in the challenge submission

The following are roadmap concepts, not features represented as complete in
the WebMCP Challenge build:

- arbitrary external-web ingestion;
- a production Chrome extension;
- automatic promotion of captured web content into durable MG memory;
- WebMCP-to-MG-orchestrator routing;
- live CRM writes or autonomous email sends from the challenge tools.

The current submission remains the bounded ACTION / STATE / ARTIFACT WebMCP
workflow with synthetic data and human send authority.
