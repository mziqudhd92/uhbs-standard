# UHBS grading toolkit — validate TPS/scorecards and run the UHBS-Lab harness.
# Build:  docker build -t uhbs:4.4.2 .
# Run:    docker run --rm -v "$PWD:/work" -w /work uhbs:4.4.2 validate-scorecard ./scorecard.json
#
# MCP (uhbs-mcp) is intentionally NOT in this image — AI hosts should install
# uhbs[mcp] on the host. See docs/tooling/mcp.md.
FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="UHBS"
LABEL org.opencontainers.image.description="Universal Honeypot Benchmarking Standard — CLI + Lab harness"
LABEL org.opencontainers.image.version="4.4.2"
LABEL org.opencontainers.image.source="https://github.com/uhbs/uhbs-standard"
LABEL org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UHBS_ROOT=/opt/uhbs \
    UHBS_SCHEMA_DIR=/opt/uhbs/schemas

WORKDIR /opt/uhbs

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 --shell /usr/sbin/nologin uhbs

COPY pyproject.toml constraints.txt README.md LICENSE ./
COPY src ./src
COPY schemas ./schemas
COPY templates ./templates
COPY docs/conformance/fixtures ./docs/conformance/fixtures

RUN pip install --no-cache-dir -c constraints.txt ".[lab]" \
    && uhbs --version \
    && uhbs-lab --list-protocols | grep -qx mcp \
    && uhbs validate-scorecard \
        docs/conformance/fixtures/cowrie-low-interaction.scorecard.json

WORKDIR /work
RUN mkdir -p /work && chown uhbs:uhbs /work
USER uhbs

VOLUME ["/work"]
ENTRYPOINT ["uhbs"]
CMD ["--help"]
