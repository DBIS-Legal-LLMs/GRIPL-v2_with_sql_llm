# ─────────────────────────────────────────────
# Stage 1 – build
# ─────────────────────────────────────────────

FROM python:3.11-slim AS builder

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install \
    --default-timeout=1200 \
    --prefix=/install \
    -r requirements.txt



# ─────────────────────────────────────────────
# Stage 2 – runtime
# ─────────────────────────────────────────────

FROM python:3.11-slim AS runtime


WORKDIR /app


COPY --from=builder /install /usr/local


COPY app/ ./app/


COPY scripts/ ./scripts/


EXPOSE 8082


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082"]