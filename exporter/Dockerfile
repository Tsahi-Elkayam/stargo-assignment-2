# Multi-stage build for optimized image
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 exporter && \
    mkdir -p /app/config && \
    chown -R exporter:exporter /app

# Set working directory
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/exporter/.local

# Copy application code
COPY --chown=exporter:exporter src/ ./src/

# Set Python path
ENV PATH=/home/exporter/.local/bin:$PATH
ENV PYTHONPATH=/app

# Switch to non-root user
USER exporter

# Expose metrics port
EXPOSE 8000

# Health check - use dynamic PORT from environment
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", 8000)}/health')" || exit 1

# Set working directory to src for proper imports
WORKDIR /app/src

# Run the application
CMD ["python", "main.py"]
