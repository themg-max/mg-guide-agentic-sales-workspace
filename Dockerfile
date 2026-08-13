# syntax=docker/dockerfile:1

# NW-007 judge-safe Cloud Run surface container packaging.
# This Dockerfile only defines the image; it does not build, push, deploy,
# or mutate any cloud resource.  Cloud Build / push / deployment are deferred
# to the separately authorized B2 execution lane.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    MEETING_CONTEXT_GEMINI_MODE=stub

WORKDIR /app

# Install pinned runtime dependencies.  google-adk is required by existing
# orchestration code; pytest is omitted from the production image.
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

ENV PYTHONPATH=/app/src

EXPOSE 8080

USER nobody

CMD ["python", "-m", "mg_guide.judge_surface.server"]
