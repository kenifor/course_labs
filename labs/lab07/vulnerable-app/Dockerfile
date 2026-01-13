FROM python:3.11-slim

WORKDIR /app

# Fix: Minimize installed packages - remove unnecessary build tools
# Keep only essential runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Only include if actually needed by your app
        # build-essential libjpeg-dev zlib1g-dev libxml2-dev libxslt1-dev \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Fix: Create non-root user and set ownership
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app

# Fix: Switch to non-root user
USER appuser

EXPOSE 8080

# Fix: Set production environment
ENV FLASK_ENV=production
ENV DEBUG=false

# Fix: Add HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

CMD ["python", "app.py"]
