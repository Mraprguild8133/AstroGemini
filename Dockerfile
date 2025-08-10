# Multi-stage Docker build for Telegram Gemini AI Bot
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_external.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_external.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN groupadd -r botuser && useradd -r -g botuser botuser

# Create app directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY main.py .
COPY bot.py .
COPY gemini_service.py .
COPY together_service.py .
COPY rate_limiter.py .
COPY config.py .
COPY webhook_server.py .
COPY webhook_main.py .

# Create logs directory
RUN mkdir -p /app/logs

# Change ownership to non-root user
RUN chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/', timeout=5)" || exit 1

# Default command (can be overridden)
CMD ["python", "main.py"]