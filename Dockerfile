# ==============================================================================
# SENTINEL-AD: TNI AD Cognitive Defense & Threat Intelligence System
# Official Dockerfile - Military Intranet (MILNET) & Cloud Production Ready
# Optimized for Kartika Cyber Hackathon 2026 - Kategori 04 Siber Sosial
# ==============================================================================

FROM python:3.11-slim

# Set military tactical metadata
LABEL maintainer="Muhammad Ilham <https://github.com/muh-ilham>" \
      project="SENTINEL-AD" \
      classification="DEFENSE_GRADE_COGNITIVE_WARFARE" \
      version="2.5.0-MILNET"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_THEME_BASE=dark

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy entire application codebase
COPY . /app/

# Create non-root military operator user for defense security compliance
RUN useradd -m -u 1001 sentinel && \
    mkdir -p /app/data && \
    chown -R sentinel:sentinel /app

USER sentinel

# Expose standard Streamlit port
EXPOSE 8501

# Healthcheck to verify system readiness
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Launch Sentinel-AD Core
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
