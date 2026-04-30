FROM ghcr.io/astral-sh/uv:0.5-python3.13-alpine AS builder

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev
COPY backend/src ./src


FROM ghcr.io/astral-sh/uv:0.5-python3.13-alpine AS runtime

RUN apk add --no-cache \
    bash \
    su-exec \
    shadow \
    tini \
    tzdata

ENV LANG="C.UTF-8" \
    TZ=Asia/Shanghai \
    PUID=1000 \
    PGID=1000 \
    UMASK=022

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src .
COPY webui/dist ./dist
COPY --chmod=755 entrypoint.sh /entrypoint.sh

RUN mkdir -p /home/ab && \
    addgroup -S ab -g 911 && \
    adduser -S ab -G ab -h /home/ab -s /sbin/nologin -u 911

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 37892
VOLUME ["/app/config", "/app/data"]

ENTRYPOINT ["tini", "-g", "--", "/entrypoint.sh"]
