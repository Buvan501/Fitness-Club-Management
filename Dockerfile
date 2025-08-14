FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=8000

WORKDIR /app

# System deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    libjpeg62-turbo-dev \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Ensure entrypoint is executable
RUN chmod +x /app/docker-entrypoint.sh

# Entrypoint initializes DB and roles, then launches the server
ENTRYPOINT ["/app/docker-entrypoint.sh"]

# Expose port
EXPOSE 8000

# Healthcheck (simple)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
 CMD curl -fsS http://localhost:${PORT}/ || exit 1

# Run with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--workers", "3", "--timeout", "120"]


