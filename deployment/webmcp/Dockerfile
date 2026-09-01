# syntax=docker/dockerfile:1

# WebMCP Challenge competition adapter container packaging.
# This Dockerfile only defines the image; it does not build, push, deploy,
# or mutate any cloud resource by itself.
#
# This image serves the PUBLIC, unauthenticated, synthetic-only WebMCP
# competition surface (mg_guide.webmcp) — distinct from the authenticated
# judge_surface add-on adapter (see ../../Dockerfile). It reuses the same
# meeting_follow_up_v1 orchestration package but exposes only the bounded
# /webmcp/* routes plus the static frontend under webmcp/static/.
#
# Production topology: A.I. Rolodex landing hosts /mg-guide/ frontend;
# this service is the bounded backend (and can also serve static for local
# same-origin testing). Stateless: no server session, no sticky routing.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    MEETING_CONTEXT_GEMINI_MODE=stub \
    WEBMCP_CORS_MODE=production

WORKDIR /app

COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir \
    jsonschema==4.23.0 \
    PyYAML==6.0.2 \
    google-adk==1.18.0 \
    google-cloud-firestore==2.27.0 \
    referencing==0.35.1 \
    rpds-py==0.20.1 \
    attrs==24.2.0 \
    jsonschema-specifications==2023.12.1 \
    iniconfig==2.0.0 \
    packaging==24.2.0 \
    pluggy==1.5.0

COPY src ./src
COPY contracts ./contracts
COPY fixtures ./fixtures
COPY webmcp ./webmcp

ENV PYTHONPATH=/app/src

EXPOSE 8080

USER nobody

CMD ["python", "-m", "mg_guide.webmcp.server"]
